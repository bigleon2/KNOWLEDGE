#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""resume-youtube — Orchestrateur (D005).
Usage :
  python3 resume_youtube.py --url <url_playlist_ou_video> --out <dir> [--n-max N] [--no-summaries]
Étapes : playlist (ou vidéo unique) -> transcripts multi-moteurs -> résumés -> rapport.md
Idempotent : relancer ne refait que ce qui manque (KO-L001). Honnêteté R3 partout.
"""
import argparse
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def run(cmd):
    print("$ " + " ".join(cmd), flush=True)
    return subprocess.run([sys.executable] + cmd, capture_output=True, text=True)


def fetch_video_meta(url):
    """Vidéo unique : extraction titre via <title> de la watch page (métadonnées minales)."""
    m = re.search(r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})", url)
    if not m:
        return None
    vid = m.group(1)
    p = subprocess.run(["curl", "-sL", "--max-time", "30", "-A", "Mozilla/5.0",
                        "https://www.youtube.com/watch?v=" + vid + "&hl=fr"],
                       capture_output=True, text=True, timeout=40)
    mt = re.search(r"<title>([^<]*)</title>", p.stdout or "")
    title = mt.group(1).replace(" - YouTube", "").strip() if mt else vid
    return {"playlist_id": "", "title": title, "n_videos": 1,
            "videos": [{"index": "1", "videoId": vid, "title": title, "duration": "",
                        "author": "", "url": "https://www.youtube.com/watch?v=" + vid}]}


def write_report(out, playlist, resumes, verification=None):
    vids = {v["videoId"]: v for v in playlist.get("videos", [])}
    verif = {}
    if verification:
        try:
            verif = {r["videoId"]: r for r in
                     json.load(open(verification, encoding="utf-8")).get("videos", [])}
        except Exception:
            verif = {}
    by_level = {}
    lines = ["# Rapport — {}".format(playlist.get("title") or "Vidéos YouTube"), "",
             "Source : {}".format(playlist.get("playlist_id") or "-"),
             "Vidéos : {}".format(len(resumes)), ""]
    for r in resumes:
        v = vids.get(r["videoId"], {})
        lvl = r.get("niveau_preuve", "metadata")
        by_level[lvl] = by_level.get(lvl, 0) + 1
        lines += ["## {}. {}".format(v.get("index", "-"), r.get("title", "")),
                  "- Chaîne : {} | Durée : {} | [Lien]({})".format(
                      v.get("author", "?"), v.get("duration", "?"), r.get("url", "")),
                  "- Niveau de preuve : **{}**".format(lvl), "",
                  str(r.get("resume", "")).strip(), ""]
        pk = r.get("points_cles") or []
        if pk:
            lines.append("**Points clés :**")
            lines += ["- {}".format(str(x).strip()) for x in pk]
            lines.append("")
        vv = verif.get(r["videoId"])
        if vv:
            anc = [a for a in vv.get("ancrage", []) if a.get("horodatage")]
            lines.append("**Anti-hallucination :** statut **{}** — {}".format(
                vv.get("statut", "?"), vv.get("raison", "")))
            if anc:
                lines.append("- Ancrage horodaté (G3) : " + " ; ".join(
                    "{} @ {}".format(a["point"][:60], a["horodatage"]) for a in anc[:4]))
            lines.append("")
    lines += ["---", "", "## Synthèse des niveaux de preuve", ""]
    for k, n in sorted(by_level.items()):
        lines.append("- {}: {} vidéo(s)".format(k, n))
    if verif:
        lines += ["", "## Vérification anti-hallucination (G1-G5)", ""]
        st = {}
        for vv in verif.values():
            st[vv.get("statut", "?")] = st.get(vv.get("statut", "?"), 0) + 1
        for k, n in sorted(st.items()):
            lines.append("- {}: {} vidéo(s)".format(k, n))
        lines += ["", "> Gardes : G1 ancrage (pas de transcript -> NON-VÉRIFIÉ), "
                  "G2 votes LLM réels par affirmation (R3), G3 ancrage horodaté, "
                  "G4 citations verbatim, G5 enveloppe honnête."]
    lines += ["", "> Honnêteté R3 : aucun contenu fabriqué. Les résumés « metadata » sont des "
              "inférences de titre uniquement ; les « transcript » reposent sur les sous-titres "
              "réels ; les « description » sur les métadonnées enrichies."]
    path = os.path.join(out, "rapport.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--n-max", type=int, default=0)
    ap.add_argument("--no-summaries", action="store_true")
    ap.add_argument("--max-repasses", type=int, default=1,
                    help="repasses anti-hallucination max (G5 revision_requise)")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    tr_dir = os.path.join(a.out, "transcripts")
    videos_json = os.path.join(a.out, "videos.json")
    resumes_json = os.path.join(a.out, "resumes.json")

    # 1) playlist ou vidéo unique
    if "list=" in a.url:
        cmd = [os.path.join(HERE, "fetch_playlist.py"), "--url", a.url, "--out", videos_json]
        if a.n_max:
            cmd += ["--n-max", str(a.n_max)]
        r = run(cmd)
    else:
        meta = fetch_video_meta(a.url)
        if not meta:
            print("ERREUR: URL ni playlist ni vidéo reconnue", file=sys.stderr)
            sys.exit(2)
        with open(videos_json, "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)
        r = None
    if r and r.returncode != 0:
        print(r.stdout + r.stderr, file=sys.stderr)
    playlist = json.load(open(videos_json, encoding="utf-8"))
    print("playlist: {} vidéos".format(playlist["n_videos"]))

    # 2) transcripts
    r = run([os.path.join(HERE, "fetch_transcripts.py"), "--videos", videos_json, "--out", tr_dir])
    print((r.stdout or "")[-1500:])

    # 3) résumés
    if not a.no_summaries:
        for _ in range(3):  # passes successives jusqu'à stabilisation (idempotent)
            r = run([os.path.join(HERE, "summarize.py"), "--videos", videos_json,
                     "--transcripts", tr_dir, "--out", resumes_json])
            print((r.stdout or "")[-800:])
            if "TERMINE: 0 nouveaux" in (r.stdout or ""):
                break

    # 3.5) VÉRIFICATION ANTI-HALLUCINATION (exigence 2026-10-04 — gardes G1-G5)
    resumes = json.load(open(resumes_json, encoding="utf-8")) if os.path.exists(resumes_json) else []
    verif_json = os.path.join(a.out, "verification.json")
    if resumes and not a.no_summaries:
        for repasse in range(1 + max(0, a.max_repasses)):
            r = run([os.path.join(HERE, "verify_summary.py"), "--videos", videos_json,
                     "--transcripts", tr_dir, "--resumes", resumes_json,
                     "--out", verif_json,
                     "--max-repasses", str(a.max_repasses)])
            print((r.stdout or "")[-1200:])
            try:
                vj = json.load(open(verif_json, encoding="utf-8"))
                need = [x["videoId"] for x in vj.get("videos", []) if x.get("revision_requise")]
            except Exception:
                need = []
            if not need or repasse >= a.max_repasses:
                break
            # repasse de synthèse uniquement sur les vidéos révisables (idempotent)
            for vid in need:
                rp = os.path.join(tr_dir, vid + ".json")
                if os.path.exists(rp):
                    r = run([os.path.join(HERE, "summarize.py"), "--videos", videos_json,
                             "--transcripts", tr_dir, "--out", resumes_json,
                             "--force-video", vid])
                    print((r.stdout or "")[-500:])

    # 4) rapport
    resumes = json.load(open(resumes_json, encoding="utf-8")) if os.path.exists(resumes_json) else []
    path = write_report(a.out, playlist, resumes,
                        verification=verif_json if os.path.exists(verif_json) else None)
    print("RAPPORT:", path)


if __name__ == "__main__":
    main()
