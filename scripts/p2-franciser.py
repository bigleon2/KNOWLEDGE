#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.7)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (R4)

p2-franciser.py — Phase P2 (directive 10 tâches, tâche 2) : francisation
idempotente des skills du dépôt distant (worktree publication).

Mécanique :
  1. SCAN   : détecte les fichiers .md/.json contenant des caractères chinois
              (U+4E00-U+9FFF) sous skills/ (SKILL.md + references/).
  2. SCEAU  : SHA-256 de chaque fichier avant traitement (zéro-régression R2).
  3. TRAITE : traduction zh→fr via CLI `z-ai chat` (subprocess, pas de shell),
              prompt système strict (structure Markdown + code + frontmatter
              préservés) ; 2e passe automatique sur résiduels ; vérifications
              post-traduction (frontmatter intact, résiduels zh).
  4. ETAT   : scripts/p2-etat.json — journal par fichier (statut, résiduels,
              SHAs avant/après) → reprise de lot + idempotence (fichier sans
              chinois au scan = SKIP no-op).

Usage :
  python3 scripts/p2-franciser.py --scan [--racine DIR] [--json OUT]
  python3 scripts/p2-franciser.py --sceau F1 F2 ...   (écrit p2-sceau-avant.json)
  python3 scripts/p2-franciser.py --traite F1 F2 ... [--racine DIR]

Codes retour : 0 OK · 1 échec traitement · 2 usage invalide.
"""
import hashlib
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

BASE = Path("/home/z/my-project")
WORKTREE = BASE / ".staging" / "KNOWLEDGE-publish"
ETAT = BASE / "scripts" / "p2-etat.json"
SCEAU = BASE / "scripts" / "p2-sceau-avant.json"
ZH = re.compile(r"[\u4e00-\u9fff]")
MAX_ARGS_CHARS = 12_000  # seuil de morcelage (limite de sortie du LLM ≈ 4k tokens)

PROMPT_SYS = (
    "Tu es un traducteur technique français expert. Traduis en FRANÇAIS tous les "
    "segments en chinois de ce document, en préservant STRICTEMENT :\n"
    "1. La structure Markdown (titres, listes, tableaux, liens, emphases, blocs de citation).\n"
    "2. La MISE EN FORME DES LIGNES : une ligne source correspond à une ligne cible — ne fusionne "
    "JAMAIS plusieurs lignes en une seule, ne réorganise pas, ne résume pas, ne supprime rien, "
    "n'ajoute aucun commentaire ni note du traducteur, aucune phrase d'introduction ni de clôture.\n"
    "3. Les blocs de code (Python, JS, shell, SQL, HTML/CSS) : ne traduis NI le code ni les "
    "clés JSON ; traduis UNIQUEMENT les chaînes de caractères et commentaires chinois qu'ils contiennent.\n"
    "4. Le frontmatter YAML : traduis seulement les VALEURS textuelles chinoises, jamais les clés.\n"
    "5. Les chemins de fichiers, URLs, commandes, noms de variables, regex, formats.\n"
    "6. Ponctuation chinoise (，。：；「」【】（）) → ponctuation française (, . : ; « » ()).\n"
    "Si le document est un JSON : renvoie UNIQUEMENT le JSON brut complet (aucun code fence, "
    "aucun texte autour), avec les clés inchangées et seulement les valeurs chinoises traduites.\n"
    "Contenu : traduis le sens avec précision et naturel ; translittère les noms propres "
    "chinois en pinyin (ex : 高考 → gaokao) avec une courte explication française entre "
    "parenthèses la première occurrence. Renvoie UNIQUEMENT le document traduit intégral."
)


def sh256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def contient_zh(p: Path) -> int:
    try:
        t = p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return -1
    return len(ZH.findall(t))


def scan(racine: Path):
    files = sorted(racine.glob("skills/**/*.md")) + sorted(racine.glob("skills/**/*.json"))
    return [(f.relative_to(racine).as_posix(), contient_zh(f)) for f in files if contient_zh(f) > 0]


def morceler(texte: str):
    """Découpe par sections '## ' en gardant l'en-tête courant (fichiers volumineux)."""
    if len(texte) <= MAX_ARGS_CHARS:
        return [texte]
    parties, courant = [], []
    for ligne in texte.splitlines(keepends=True):
        if ligne.startswith("## ") and courant and sum(len(x) for x in courant) > MAX_ARGS_CHARS // 2:
            parties.append("".join(courant))
            courant = []
        courant.append(ligne)
    if courant:
        parties.append("".join(courant))
    return parties


def appelle_llm(fragment: str, out_json: Path, essais: int = 5) -> str:
    out_json.parent.mkdir(parents=True, exist_ok=True)
    import time
    time.sleep(2.0)  # throttle global — évite le rate-limit de l'API
    # Wrapper explicite : le contenu ne doit JAMAIS être interprété comme une
    # instruction ou une question (cas observé : réponse « true » sur du YAML)
    enveloppe = (
        "<DOCUMENT À TRADUIRE>\n" + fragment + "\n</DOCUMENT À TRADUIRE>\n\n"
        "Renvoie UNIQUEMENT le document ci-dessus traduit (intégral, même structure, "
        "mêmes lignes) — jamais un avis, jamais une confirmation, jamais une réponse courte."
    )
    dernier = None
    for essai in range(1, essais + 1):
        try:
            cmd = ["z-ai", "chat", "-p", enveloppe, "--system", PROMPT_SYS, "-o", str(out_json)]
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=240)
            if r.returncode != 0:
                raise RuntimeError(f"z-ai rc={r.returncode} : {r.stderr[:200]}")
            data = json.loads(out_json.read_text(encoding="utf-8"))
            contenu = data["choices"][0]["message"]["content"]
            if not contenu or len(contenu.strip()) < 20:
                raise RuntimeError(f"réponse LLM vide ou triviale ({len((contenu or '').strip())} car.)")
            return contenu
        except Exception as exc:
            dernier = exc
            if essai < essais:
                if "Failed to make API" in str(exc):
                    time.sleep(45)  # pause anti-rafale (fenêtre rate-limit)
                time.sleep(12 * essai)  # backoff long (rate-limit API : 12/24/36/48 s)
    raise RuntimeError(f"après {essais} essais : {dernier}")


INSTR_RESIDUEL = (
    "\n\n[INSTRUCTION COMPLÉMENTAIRE : il reste des caractères chinois dans ce document — "
    "traduis-les TOUS en français, y compris s'ils se trouvent dans des chaînes de "
    "caractères HTML/JS/CSS (attributs title, alt, placeholder, textes visibles, "
    "libellés d'interface), dans des tableaux ou des valeurs YAML. Ne garde du chinois "
    "que les noms propres (translittérés en pinyin). Renvoie le document intégral traduit, "
    "même structure, mêmes lignes.]"
)


def strip_fences(texte: str) -> str:
    """Retire une enveloppe ```markdown/```json éventuelle renvoyée par le LLM."""
    t = texte.strip()
    if t.startswith("```"):
        fin = t.find("\n", 3)
        t = t[fin + 1 :] if fin > 0 else t[3:]
        if t.rstrip().endswith("```"):
            t = t.rstrip()[:-3]
    return t.rstrip() + "\n"


def traite_fichier(rel: str, racine: Path, journal: dict) -> str:
    p = racine / rel
    avant = p.read_text(encoding="utf-8", errors="replace")
    sha_avant = sh256(p)
    n_zh = len(ZH.findall(avant))
    entree = {
        "fichier": rel,
        "zh_avant": n_zh,
        "sha_avant": sha_avant,
    }
    # Garde structure : frontmatter et compte de lignes
    fm_avant = avant.startswith("---\n")
    parties = morceler(avant)
    traduits, pass2 = [], 0
    try:
        traduits = [appelle_llm(part, BASE / "scripts" / "outputs" / f"p2-{hashlib.sha1(rel.encode()).hexdigest()[:12]}.json") for part in parties]
        # Passe 2 PAR MORCEAU : tout morceau avec chinois résiduel est re-traduit
        # avec instruction ciblée (gère les fichiers morcelés et le chinois dans le code)
        for i, part_tr in enumerate(traduits):
            if len(ZH.findall(part_tr)) > 0:
                rejet = appelle_llm(part_tr + INSTR_RESIDUEL, BASE / "scripts" / "outputs" / f"p2-{hashlib.sha1(rel.encode()).hexdigest()[:12]}.json")
                if len(ZH.findall(rejet)) < len(ZH.findall(part_tr)) and len(rejet) > len(part_tr) * 0.6:
                    traduits[i] = rejet
                    pass2 += 1
        resultat = strip_fences("".join(traduits))
        # Garde JSON valide (evals/trigger_evals.json)
        if rel.endswith(".json"):
            m1, m2 = resultat.find("{"), resultat.rfind("}")
            if m1 > 0 or (m2 > 0 and m2 < len(resultat) - 2):
                resultat = resultat[m1 : m2 + 1]  # extraction du corps JSON
            try:
                json.loads(resultat)
            except Exception as exc:
                raise RuntimeError(f"JSON invalide post-traduction : {exc}")
        # Passe 3 filet : fichier entier (si court) encore résiduel
        residuel = len(ZH.findall(resultat))
        if residuel > 0 and len(resultat) <= MAX_ARGS_CHARS:
            traduits2 = appelle_llm(
                resultat + INSTR_RESIDUEL,
                BASE / "scripts" / "outputs" / f"p2-{hashlib.sha1(rel.encode()).hexdigest()[:12]}.json",
            )
            if len(ZH.findall(traduits2)) < residuel and len(traduits2) > len(resultat) * 0.6:
                resultat, pass2 = traduits2, pass2 + 1
        entree["zh_apres"] = len(ZH.findall(resultat))
        entree["passe2"] = pass2
        if entree["zh_apres"] == 0:
            entree["statut"] = "TRADUIT"
        else:
            entree["statut"] = "TRADUIT-RESIDUEL"  # noms propres documentés — re-jeu = SKIP
        # Garde anti-régression : frontmatter préservé, volume plausible
        if fm_avant and not resultat.startswith("---\n"):
            raise RuntimeError("frontmatter perdu")
        if len(resultat) < len(avant) * 0.5:
            raise RuntimeError(f"volume suspect ({len(resultat)} vs {len(avant)} car.)")
        # Garde densité de lignes (structure préservée) pour les .md
        if not rel.endswith(".json"):
            l_av, l_ap = avant.count(chr(10)), resultat.count(chr(10))
            if l_av > 10 and not (l_av * 0.75 <= l_ap <= l_av * 1.35):
                raise RuntimeError(f"densité de lignes altérée ({l_av} → {l_ap})")
        p.write_text(resultat, encoding="utf-8")
        entree["sha_apres"] = sh256(p)
        # statut déjà posé (TRADUIT / TRADUIT-RESIDUEL selon résiduels zh)
    except Exception as exc:
        # Restauration byte-identique en cas d'échec partiel
        p.write_text(avant, encoding="utf-8")
        entree["statut"] = "ECHEC"
        entree["erreur"] = str(exc)[:300]
    journal.setdefault("traitements", {})[rel] = entree
    ETAT.write_text(json.dumps(journal, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  [{entree['statut']}] {rel} : zh {n_zh} → {entree.get('zh_apres', '?')}"
          + (f" — ERREUR {entree['erreur']}" if entree["statut"] == "ECHEC" else ""))
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
    if args[0] == "--scan":
        items = scan(racine)
        out = None
        if "--json" in args:
            out = Path(args[args.index("--json") + 1])
            out.write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
        total = sum(n for _, n in items)
        print(f"{len(items)} fichiers avec chinois ({total} car. zh) — racine {racine}")
        for rel, n in items:
            print(f"  {n:>6} {rel}")
        return 0
    if args[0] == "--sceau":
        sceau = {rel: sh256(racine / rel) for rel in args[1:]}
        SCEAU.write_text(json.dumps(sceau, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")
        print(f"sceau écrit : {len(sceau)} fichiers → {SCEAU}")
        return 0
    if args[0] == "--traite":
        journal = json.loads(ETAT.read_text(encoding="utf-8")) if ETAT.exists() else {}
        dejat = journal.get("traitements", {})
        force = "--force" in args
        args = [a for a in args if a != "--force"]
        workers = 1
        if "--workers" in args:
            i = args.index("--workers")
            workers = int(args[i + 1])
            del args[i : i + 2]
        cibles = []
        for rel in args[1:]:
            p = racine / rel
            statut_pre = dejat.get(rel, {}).get("statut")
            if statut_pre in ("TRADUIT", "TRADUIT-RESIDUEL") and not force:
                print(f"  [SKIP déjà traité] {rel} ({statut_pre})")
                continue
            if contient_zh(p) == 0:
                print(f"  [SKIP no-op] {rel} : 0 caractère chinois")
                continue
            cibles.append(rel)
        echecs = []
        # Exécution séquentielle ou parallèle (appels LLM indépendants par fichier)
        import threading
        lock = threading.Lock()

        def un(rel):
            with lock:
                statut = traite_fichier(rel, racine, journal)
            return rel, statut

        if workers > 1 and len(cibles) > 1:
            with ThreadPoolExecutor(max_workers=workers) as ex:
                futurs = {ex.submit(un, rel): rel for rel in cibles}
                for f in as_completed(futurs):
                    rel, statut = f.result()
                    if statut == "ECHEC":
                        echecs.append(rel)
        else:
            for rel in cibles:
                _, statut = un(rel)
                if statut == "ECHEC":
                    echecs.append(rel)
        if echecs:
            print(f"  ECHECS ({len(echecs)}) : " + ", ".join(echecs))
            return 1
        return 0
    print("usage : --scan | --sceau F... | --traite F...")
    return 2


if __name__ == "__main__":
    sys.exit(main())
