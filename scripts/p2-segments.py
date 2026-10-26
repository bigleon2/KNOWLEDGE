#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.7)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL

p2-segments.py — Phase P2 : traduction ciblée PAR SEGMENTS de lignes (zh→fr)
pour les fichiers récalcitrants (templates HTML, fichiers compactés par le LLM
document-entier). Substitution in-place ligne à ligne : la densité de lignes
est préservée PAR CONSTRUCTION.

Mécanique :
  1. Scanne les lignes contenant du chinois (U+4E00-U+9FFF).
  2. Groupe les lignes consécutives en blocs (moins d'appels).
  3. Chaque bloc → LLM (garde : même nombre de lignes en sortie, sinon
     fallback ligne par ligne).
  4. Substitution par position (de la fin vers le début).
  5. Journal p2-segments-etat.json (idempotent : re-jeu = SKIP si 0 zh).

Usage : python3 scripts/p2-segments.py F1 [F2 ...] [--racine DIR] [--workers N]
Codes retour : 0 OK · 1 échecs partiels · 2 usage invalide.
"""
import hashlib
import json
import re
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

BASE = Path("/home/z/my-project")
WORKTREE = BASE / ".staging" / "KNOWLEDGE-publish"
ETAT = BASE / "scripts" / "p2-segments-etat.json"
ZH = re.compile(r"[\u4e00-\u9fff]")
MAX_BLOC_CAR = 9_000  # limite de sortie LLM par bloc

PROMPT_SEG = (
    "Tu es un traducteur technique français expert. Le texte suivant contient des lignes "
    "avec du chinois. Renvoie EXACTEMENT les mêmes lignes, dans le même ordre, avec le "
    "MÊME NOMBRE de lignes, en traduisant UNIQUEMENT les segments chinois en français "
    "(noms propres translittérés en pinyin entre parenthèses). Ne traduis pas le code "
    "(balises HTML, CSS, JS, clés JSON) sauf les chaînes visibles (title, alt, "
    "placeholder, textes affichés, libellés). Ne fusionne jamais de lignes, n'en "
    "supprime aucune, n'en ajoute aucune. Renvoie UNIQUEMENT les lignes traduites."
)


def sh256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


SEG_CJK = re.compile(r"[\u4e00-\u9fff][\u4e00-\u9fff\u3000-\u303f\uff00-\uffef，。：；！？、（）「」《》·…—a-zA-Z0-9 %/-]*")


ESSAIS_DEF = int(__import__("os").environ.get("P2_ESSAIS", "5"))


def appelle_llm(fragment: str, out_json: Path, essais: int = None) -> str:
    essais = essais or ESSAIS_DEF
    out_json.parent.mkdir(parents=True, exist_ok=True)
    time.sleep(2.0)  # throttle
    enveloppe = f"<LIGNES À TRADUIRE>\n{fragment}\n</LIGNES À TRADUIRE>\n\nRenvoie UNIQUEMENT les lignes traduites (même nombre)."
    dernier = None
    for essai in range(1, essais + 1):
        try:
            cmd = ["z-ai", "chat", "-p", enveloppe, "--system", PROMPT_SEG, "-o", str(out_json)]
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=240)
            if r.returncode != 0:
                raise RuntimeError(f"z-ai rc={r.returncode}")
            data = json.loads(out_json.read_text(encoding="utf-8"))
            c = data["choices"][0]["message"]["content"]
            if not c or len(c.strip()) < 2:
                raise RuntimeError("réponse vide")
            t = c.strip()
            if t.startswith("```"):
                fin = t.find("\n", 3)
                t = t[fin + 1 :] if fin > 0 else t[3:]
                if t.endswith("```"):
                    t = t[:-3]
            return t.rstrip()
        except Exception as exc:
            dernier = exc
            if essai < essais:
                if "Failed to make API" in str(exc):
                    time.sleep(45)  # pause anti-rafale
                time.sleep(12 * essai)
    raise RuntimeError(f"après {essais} essais : {dernier}")


def blocs_de_lignes(lignes: list):
    """Groupe les indices de lignes zh en blocs consécutifs (max MAX_BLOC_CAR)."""
    idx = [i for i, l in enumerate(lignes) if ZH.search(l)]
    blocs, courant, volume = [], [], 0
    prev = None
    for i in idx:
        if prev is not None and i - prev > 1:
            blocs.append(courant); courant, volume = [], 0
        if volume + len(lignes[i]) > MAX_BLOC_CAR and courant:
            blocs.append(courant); courant, volume = [], 0
        courant.append(i); volume += len(lignes[i]); prev = i
    if courant:
        blocs.append(courant)
    return blocs


def traite_fichier(rel: str, racine: Path, journal: dict, lock: threading.Lock) -> str:
    p = racine / rel
    texte = p.read_text(encoding="utf-8", errors="replace")
    lignes = texte.split("\n")
    blocs = blocs_de_lignes(lignes)
    n_zh = sum(len(ZH.findall(l)) for l in lignes)
    entree = {"fichier": rel, "zh_avant": n_zh, "blocs": len(blocs)}
    if n_zh == 0:
        entree["statut"] = "NO-OP"
        journal[rel] = entree
        return "NO-OP"
    echecs_bloc = []
    # Traitement des blocs en parallèle (2 threads — throttle global)
    def traite_bloc(indices):
        avant_bloc = [lignes[i] for i in indices]
        reponse = appelle_llm("\n".join(avant_bloc), BASE / "scripts" / "outputs" / f"p2s-{hashlib.sha1(rel.encode()).hexdigest()[:12]}.json")
        lignes_rep = reponse.split("\n")
        if len(lignes_rep) != len(avant_bloc):
            raise RuntimeError(f"compte lignes {len(avant_bloc)} → {len(lignes_rep)}")
        for j, i in enumerate(indices):
            if ZH.search(lignes_rep[j]) and not ZH.search(avant_bloc[j]):
                continue  # ne jamais introduire de chinois là où il n'y en avait pas
            lignes[i] = lignes_rep[j]
    with ThreadPoolExecutor(max_workers=2) as ex:
        futurs = {ex.submit(traite_bloc, b): b for b in blocs}
        for f in as_completed(futurs):
            b = futurs[f]
            try:
                f.result()
            except Exception as exc:
                echecs_bloc.append((b, str(exc)[:150]))
    # Fallback : échecs de blocs → ligne par ligne
    for b, _err in echecs_bloc:
        for i in b:
            try:
                rep = appelle_llm(lignes[i], BASE / "scripts" / "outputs" / f"p2s1-{hashlib.sha1(rel.encode()).hexdigest()[:12]}.json")
                if rep.count("\n") == 0 and len(rep) > 1:
                    lignes[i] = rep
            except Exception:
                pass  # ligne conservée telle quelle (résiduel documenté)
    n_apres = sum(len(ZH.findall(l)) for l in lignes)
    with lock:
        p.write_text("\n".join(lignes), encoding="utf-8")
        entree["zh_apres"] = n_apres
        entree["echecs_bloc"] = len(echecs_bloc)
        entree["sha_apres"] = sh256(p)
        entree["statut"] = "TRADUIT" if n_apres == 0 else ("TRADUIT-RESIDUEL" if n_apres < n_zh else "INCHANGE")
        journal[rel] = entree
        ETAT.write_text(json.dumps(journal, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  [{entree['statut']}] {rel} : zh {n_zh} → {n_apres} ({len(blocs)} blocs, {len(echecs_bloc)} éch. bloc)")
    return entree["statut"]


def traite_intra(rel: str, racine: Path, journal: dict, lock: threading.Lock) -> str:
    """Mode intra : traduit chaque segment chinois isolé (fragment court),
    substitution positionnelle fin→début — le code non-chinois est préservé
    byte-identique par construction."""
    p = racine / rel
    texte = p.read_text(encoding="utf-8", errors="replace")
    segments = list(SEG_CJK.finditer(texte))
    segments = [m for m in segments if len(ZH.findall(m.group(0))) >= 1]
    n_zh = len(ZH.findall(texte))
    entree = {"fichier": rel, "zh_avant": n_zh, "segments": len(segments), "mode": "intra"}
    if not segments:
        entree["statut"] = "NO-OP"
        journal[rel] = entree
        return "NO-OP"
    # Dedup des segments identiques (1 appel par texte unique) + mapping
    uniques = {}
    for m in segments:
        uniques.setdefault(m.group(0), None)
    trad_map = {}
    echecs = 0
    items = list(uniques.keys())
    with ThreadPoolExecutor(max_workers=2) as ex:
        futurs = {ex.submit(appelle_llm, s, BASE / "scripts" / "outputs" / f"p2i-{hashlib.sha1(rel.encode()).hexdigest()[:10]}.json"): s for s in items}
        for f in as_completed(futurs):
            s = futurs[f]
            try:
                rep = f.result().strip().replace("\n", " ")
                # Garde : la traduction ne doit pas (re)contenir de chinois
                if rep and not ZH.search(rep) and len(rep) >= 1:
                    trad_map[s] = rep
                else:
                    echecs += 1
            except Exception:
                echecs += 1
    # Substitution positionnelle fin → début
    resultat = texte
    for m in reversed(segments):
        t = trad_map.get(m.group(0))
        if t:
            resultat = resultat[: m.start()] + t + resultat[m.end() :]
    n_apres = len(ZH.findall(resultat))
    with lock:
        p.write_text(resultat, encoding="utf-8")
        entree["zh_apres"] = n_apres
        entree["segments_traduits"] = len(trad_map)
        entree["sha_apres"] = sh256(p)
        entree["statut"] = "TRADUIT" if n_apres == 0 else ("TRADUIT-RESIDUEL" if n_apres < n_zh else "INCHANGE")
        journal[rel] = entree
        ETAT.write_text(json.dumps(journal, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  [{entree['statut']}] {rel} : zh {n_zh} → {n_apres} ({len(trad_map)}/{len(items)} segments, {echecs} éch.)")
    return entree["statut"]


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2
    racine = WORKTREE
    if "--racine" in args:
        i = args.index("--racine")
        racine = Path(args[i + 1])
        del args[i : i + 2]
    journal = json.loads(ETAT.read_text(encoding="utf-8")) if ETAT.exists() else {}
    lock = threading.Lock()
    echecs = 0
    mode_intra = "--intra" in args
    args = [a for a in args if a != "--intra"]
    for rel in args:
        p = racine / rel
        if not p.exists():
            print(f"  [ABSENT] {rel}")
            continue
        n = sum(len(ZH.findall(l)) for l in p.read_text(encoding="utf-8", errors="replace").split("\n"))
        if n == 0:
            print(f"  [SKIP no-op] {rel}")
            continue
        if mode_intra:
            statut = traite_intra(rel, racine, journal, lock)
        else:
            statut = traite_fichier(rel, racine, journal, lock)
        if statut in ("INCHANGE",):
            echecs += 1
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main())
