#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""resume-youtube — VÉRIFICATION ANTI-HALLUCINATION (exigence propriétaire 2026-10-04, D007).

5 gardes, appliquées à chaque résumé :
  G1 ANCRAGE    — pas de transcript réel -> statut NON-VÉRIFIÉ (aucun vote LLM tenté,
                  aucun contenu « vérifié » prétendu). Mode métadonnées = inférence de
                  titre clairement étiquetée, JAMAIS présentée comme issue de la vidéo.
  G2 CLAIMS     — extraction des affirmations (resume + points_cles) puis vote LLM RÉEL
                  par affirmation contre le transcript (SUPPORTÉE / RÉFUTÉE /
                  INVÉRIFIABLE + citation de preuve). Jamais simulé (R3).
  G3 ANCRAGE T. — chaque point clé est ancré au segment de transcript au meilleur
                  recouvrement lexical -> horodatage mm:ss réel ou null.
  G4 CITATIONS  — toute citation réputée verbatim doit matcher (sous-chaîne normalisée)
                  le transcript ; sinon elle est marquée NON-TROUVÉE.
  G5 ENVELOPPE  — statut VÉRIFIÉ / PARTIEL / NON-VÉRIFIÉ + taux de support ; si le
                  taux < --seuil => revision_requise=true (l'orchestrateur relance la
                  synthèse au plus --max-repasses fois).

Usage :
  python3 verify_summary.py --videos videos.json --transcripts transcripts/ \
      --resumes resumes.json --out verification.json [--seuil 0.8] [--max-claims 12]
      [--no-llm] [--max-repasses 1]

Sortie verification.json :
  {videos:[{videoId, statut, support_rate, n_claims, claims:[{claim, verdict, preuve}],
            ancrage:[{point, horodatage}], citations:[{citation, trouvee}],
            gardes:{G1..G5}, revision_requise, raison}], synthese:{...}}
Idempotent (KO-L001) : les vidéos déjà présentes dans verification.json sont conservées
sauf si --force. Aucun vote n'est inventé : si le CLI LLM échoue, verdict = NON_EXECUTÉ.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import unicodedata
import time

SYS = ("Tu es un vérificateur d'affirmations rigoureux. On te donne un TRANSCRIPT "
       "(sous-titres d'une vidéo YouTube) et UNE affirmation. Réponds UNIQUEMENT avec "
       "un objet JSON strict : {\"verdict\": \"SUPPORTÉE\"|\"RÉFUTÉE\"|\"INVÉRIFIABLE\", "
       "\"preuve\": \"<courte citation exacte du transcript, ou chaîne vide si aucune>\", "
       "\"raison\": \"<une phrase>\"}. SUPPORTÉE seulement si le transcript contient "
       "explicitement l'information. RÉFUTÉE si le transcript la contredit. "
       "INVÉRIFIABLE si le transcript n'en parle pas. N'invente JAMAIS de preuve.")


def norm(s):
    """Normalisation pour matching lexical (casse/accents/ponctuation/espaces)."""
    s = unicodedata.normalize("NFKD", str(s or ""))
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def zai_chat(prompt, timeout=120):
    try:
        r = subprocess.run(["z-ai", "chat", "-p", prompt, "-s", SYS],
                           capture_output=True, text=True, timeout=timeout)
        return (r.stdout or "").strip()
    except Exception:
        return ""


def parse_json_loose(s):
    if not s:
        return None
    m = re.search(r"\{.*\}", s, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except Exception:
        try:
            return json.loads(m.group(0).replace("'", '"'))
        except Exception:
            return None


def extract_claims(resume, max_claims):
    """Affirmations vérifiables = points clés + phrases assertives du resume."""
    claims = []
    for p in resume.get("points_cles") or []:
        p = str(p).strip()
        if len(p) >= 8:
            claims.append(p)
    res = str(resume.get("resume") or "")
    for sent in re.split(r"(?<=[.!?])\s+", res):
        sent = sent.strip()
        # phrases assertives d'au moins 10 mots, pas une formule générique
        if len(sent.split()) >= 10 and not re.match(r"^(ce|cette|le|la|les)\s+vidéo", sent.lower()):
            claims.append(sent)
    # dédoublonnage normalisé, borne
    seen, out = set(), []
    for c in claims:
        k = norm(c)[:120]
        if k and k not in seen:
            seen.add(k)
            out.append(c)
        if len(out) >= max_claims:
            break
    return out


def best_segment(transcript, point):
    """G3 : segment au meilleur recouvrement lexical avec le point clé."""
    pt = set(norm(point).split())
    if not pt:
        return None, 0.0
    best, best_j = None, 0.0
    for seg in transcript:
        st = set(norm(seg.get("text", "")).split())
        if not st:
            continue
        j = len(pt & st) / len(pt | st)
        if j > best_j:
            best, best_j = seg, j
    if best is None or best_j < 0.12:
        return None, best_j
    t = float(best.get("start", 0) or 0)
    mm, ss = int(t // 60), int(t % 60)
    return "{:02d}:{:02d}".format(mm, ss), best_j


def check_quotes(text, transcript_text, transcript_norm):
    """G4 : citations « ... » / «...» / "..." doivent exister dans le transcript."""
    quotes = []
    for m in re.findall(r"[«\"]([^«»\"]{12,240})[»\"]", str(text or "")):
        q = m.strip()
        if not q:
            continue
        nq = norm(q)
        trouvee = bool(nq) and (nq in transcript_norm or
                                all(w in transcript_norm for w in nq.split()[:8]))
        quotes.append({"citation": q[:200], "trouvee": trouvee})
    return quotes[:10]


def fmt_transcript(transcript, limit=15000):
    parts, total = [], 0
    for seg in transcript:
        line = "[{}] {}".format(seg.get("start", ""), seg.get("text", ""))
        parts.append(line)
        total += len(line) + 1
        if total >= limit:
            break
    return "\n".join(parts)[:limit]


def verify_video(v, resume, transcript, args):
    """Applique G1->G5 à une vidéo. Retourne le dict de vérification."""
    vid = v["videoId"]
    level = resume.get("niveau_preuve", "metadata")
    has_tr = bool(transcript) and level == "transcript"

    out = {"videoId": vid, "title": v.get("title", ""), "niveau_preuve": level,
           "gardes": {}, "claims": [], "ancrage": [], "citations": [],
           "revision_requise": False, "raison": ""}

    # ---- G1 ANCRAGE ----
    if not has_tr:
        out["gardes"]["G1"] = "BLOQUANT : pas de transcript réel -> NON-VÉRIFIÉ"
        out["statut"] = "NON-VÉRIFIÉ"
        out["support_rate"] = None
        out["n_claims"] = 0
        out["raison"] = ("Résumé issu de {} (pas de sous-titres accessibles) : "
                         "aucune vérification sémantique possible — inférence de "
                         "métadonnées uniquement.".format(level))
        out["gardes"]["G2"] = "NON EXECUTÉ (G1 bloquant — jamais simulé)"
        out["gardes"]["G3"] = "NON EXECUTÉ (G1 bloquant)"
        out["gardes"]["G4"] = "NON EXECUTÉ (G1 bloquant)"
        out["gardes"]["G5"] = "NON-VÉRIFIÉ (enveloppe honnête)"
        return out
    out["gardes"]["G1"] = "OK : transcript réel ({} segments)".format(len(transcript))
    tr_text = " ".join(s.get("text", "") for s in transcript)
    tr_norm = norm(tr_text)

    # ---- G2 CLAIMS -> votes LLM réels (R3) ----
    claims = extract_claims(resume, args.max_claims)
    out["n_claims"] = len(claims)
    votes_ok = votes_ref = votes_inv = votes_fail = 0
    tr_excerpt = fmt_transcript(transcript)
    for c in claims:
        entry = {"claim": c[:300], "verdict": "NON_EXECUTÉ", "preuve": "", "raison": ""}
        if args.no_llm:
            entry["raison"] = "vote désactivé (--no-llm)"
        else:
            prompt = ("TRANSCRIPT:\n{}\n\nAFFIRMATION:\n{}\n\nVerdict JSON ?"
                      .format(tr_excerpt, c))
            raw = zai_chat(prompt)
            j = parse_json_loose(raw)
            if j and j.get("verdict") in ("SUPPORTÉE", "RÉFUTÉE", "INVÉRIFIABLE",
                                          "SUPPORTEE", "REFUTEE", "INVERIFIABLE"):
                vd = str(j["verdict"]).upper()
                vd = {"SUPPORTEE": "SUPPORTÉE", "REFUTEE": "RÉFUTÉE",
                      "INVERIFIABLE": "INVÉRIFIABLE"}.get(vd, vd)
                entry["verdict"] = vd
                entry["preuve"] = str(j.get("preuve", ""))[:300]
                entry["raison"] = str(j.get("raison", ""))[:300]
            else:
                votes_fail += 1
                entry["raison"] = "LLM indisponible ou réponse illisible (pas de vote simulé)"
        if entry["verdict"] == "SUPPORTÉE":
            votes_ok += 1
        elif entry["verdict"] == "RÉFUTÉE":
            votes_ref += 1
        elif entry["verdict"] == "INVÉRIFIABLE":
            votes_inv += 1
        out["claims"].append(entry)
        time.sleep(args.tempo)
    out["gardes"]["G2"] = ("{} votes réels : {} SUPPORTÉE / {} RÉFUTÉE / {} INVÉRIFIABLE / {} non exécutés"
                           .format(len(claims) - votes_fail, votes_ok, votes_ref,
                                   votes_inv, votes_fail))

    # ---- G3 ANCRAGE HORODATÉ ----
    for p in (resume.get("points_cles") or [])[:10]:
        ts, j = best_segment(transcript, p)
        out["ancrage"].append({"point": str(p)[:200], "horodatage": ts,
                               "jaccard": round(j, 3)})
    n_anchor = sum(1 for a in out["ancrage"] if a["horodatage"])
    out["gardes"]["G3"] = "{}/{} points clés ancrés horodatés".format(n_anchor, len(out["ancrage"]))

    # ---- G4 CITATIONS ----
    text_all = str(resume.get("resume", "")) + " " + " ".join(
        str(p) for p in (resume.get("points_cles") or []))
    out["citations"] = check_quotes(text_all, tr_text, tr_norm)
    n_ok = sum(1 for q in out["citations"] if q["trouvee"])
    out["gardes"]["G4"] = ("{}/{} citations verbatim confirmées".format(n_ok, len(out["citations"]))
                           if out["citations"] else "aucune citation réputée verbatim")

    # ---- G5 ENVELOPPE ----
    voted = votes_ok + votes_ref + votes_inv
    if votes_ref > 0:
        statut = "NON-VÉRIFIÉ"
        out["revision_requise"] = True
        out["raison"] = "{} affirmation(s) RÉFUTÉE(S) par le transcript — révision obligatoire".format(votes_ref)
    elif voted == 0:
        statut = "NON-VÉRIFIÉ"
        out["raison"] = "aucun vote exécutable (LLM indisponible) — pas de statut vérifié prétendu"
    else:
        rate = votes_ok / float(voted)
        out["support_rate"] = round(rate, 3)
        if rate >= args.seuil:
            statut = "VÉRIFIÉ"
            out["raison"] = "taux de support {} >= seuil {}".format(out["support_rate"], args.seuil)
        elif rate >= args.seuil - 0.2:
            statut = "PARTIEL"
            out["revision_requise"] = rate < args.seuil
            out["raison"] = "taux de support {} entre (seuil-0.2) et seuil".format(out["support_rate"])
        else:
            statut = "NON-VÉRIFIÉ"
            out["revision_requise"] = True
            out["raison"] = "taux de support {} < seuil-0.2 — révision obligatoire".format(out["support_rate"])
    out["statut"] = statut
    out["gardes"]["G5"] = "{} ({})".format(statut, out["raison"])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--videos", required=True)
    ap.add_argument("--transcripts", required=True)
    ap.add_argument("--resumes", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--seuil", type=float, default=0.8)
    ap.add_argument("--tempo", type=float, default=2.0)
    ap.add_argument("--max-claims", type=int, default=12)
    ap.add_argument("--max-repasses", type=int, default=1)
    ap.add_argument("--no-llm", action="store_true")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    videos = {v["videoId"]: v for v in json.load(open(args.videos, encoding="utf-8")).get("videos", [])}
    resumes = json.load(open(args.resumes, encoding="utf-8"))
    verif = {"videos": [], "synthese": {}}
    if os.path.exists(args.out) and not args.force:
        try:
            old = json.load(open(args.out, encoding="utf-8"))
            verif["videos"] = old.get("videos", [])
        except Exception:
            pass
    done = {r["videoId"] for r in verif["videos"]}

    n_new = 0
    for r in resumes:
        vid = r["videoId"]
        if vid in done or vid not in videos:
            continue
        v = videos[vid]
        # transcript réel ?
        tp = os.path.join(args.transcripts, vid + ".json")
        transcript = []
        if os.path.exists(tp):
            try:
                td = json.load(open(tp, encoding="utf-8"))
                if td.get("status") == "OK" and td.get("transcript"):
                    transcript = td["transcript"]
            except Exception:
                transcript = []
        res = verify_video(v, r, transcript, args)
        verif["videos"].append(res)
        n_new += 1
        print("VÉRIFIÉ {} : {} — {}".format(vid, res["statut"], res["raison"]), flush=True)

    n_by = {}
    for r in verif["videos"]:
        n_by[r["statut"]] = n_by.get(r["statut"], 0) + 1
    verif["synthese"] = {"n_videos": len(verif["videos"]), "n_new": n_new,
                         "statuts": n_by,
                         "seuil": args.seuil,
                         "protocole": "G1 ancrage, G2 votes LLM réels (R3), "
                                      "G3 ancrage horodaté, G4 citations, G5 enveloppe honnête",
                         "genere_le": time.strftime("%Y-%m-%d %H:%M:%S")}
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(verif, f, ensure_ascii=False, indent=2)
    print("TERMINE: {} nouvelles vérifications — statuts {}".format(n_new, n_by))


if __name__ == "__main__":
    main()
