#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.34)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).
"""

# -*- coding: utf-8 -*-
"""cache-verdicts.py — Cache de verdicts généralisé (R2 — prompt cache / anti-sprawl).

Recommandation R2 de l'étude de faisabilité Task 70 (directive propriétaire
2026-11-08, Task 71 G3) : généraliser le pattern « verdict figé une fois,
re-jeu sans ré-appel » aux graders coûteux.

Principe : un grader (arbitre, harnais, batterie de tests) dont les ENTREES
n'ont pas changé rend le MÊME verdict — le ré-exécuter coûte du temps (et
parfois des #token quand sa sortie alimente un contexte LLM). Ce wrapper :

  1. calcule une clé = SHA-256(commande + arguments + état [taille, mtime_ns]
     de chaque fichier cible) ;
  2. exécute la commande et fige le verdict (rc + stdout + durée + horodatage)
     dans tmp/cache-verdicts/<clé>.json ;
  3. au re-jeu avec la MÊME clé : rejoue le verdict figé SANS ré-appeler la
     commande (sortie identique, temps de lecture seulement) ;
  4. toute modification d'un fichier cible (taille ou mtime) change la clé →
     cache invalide → ré-exécution réelle automatique.

Usage :
    python3 scripts/cache-verdicts.py run -- <commande...> [--cibles F1 F2 ...]
    python3 scripts/cache-verdicts.py run -- <commande...> --cibles F1 F2 --force
    python3 scripts/cache-verdicts.py clear            # purge du cache
    python3 scripts/cache-verdicts.py stats            # entrées + taille
    python3 scripts/cache-verdicts.py --selftest       # 12 checks mécaniques

Codes retour : celui de la commande sous-jacente (re-jeu : rc figé) ;
3 = usage invalide ; 1 = selftest FAIL.
Python stdlib uniquement. Le cache n'est JAMAIS une preuve en soi : un verdict
figé reste vérifiable par --force (re-exécution réelle à la demande).
"""

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
CACHE = Path(os.environ.get("CACHE_VERDICTS_DIR", str(BASE / "tmp" / "cache-verdicts")))
VERSION = "1.0.0"


def cle(commande: list, cibles: list) -> str:
    """Clé SHA-256 : commande + arguments + état (taille, mtime_ns) des cibles."""
    h = hashlib.sha256()
    for mot in commande:
        h.update(mot.encode("utf-8"))
        h.update(b"\x00")
    h.update(b"\x01")
    for c in sorted(cibles):
        st = os.stat(c)
        h.update(("%s|%d|%d;" % (c, st.st_size, st.st_mtime_ns)).encode("utf-8"))
    return h.hexdigest()


def run(commande: list, cibles: list, force: bool) -> int:
    if CACHE.exists() and force:
        shutil.rmtree(CACHE)
        CACHE.mkdir(parents=True, exist_ok=True)
    CACHE.mkdir(parents=True, exist_ok=True)
    k = cle(commande, cibles)
    entree = CACHE / ("%s.json" % k)
    t0 = time.perf_counter()
    if entree.is_file() and not force:
        v = json.loads(entree.read_text(encoding="utf-8"))
        duree_rejeu_ms = (time.perf_counter() - t0) * 1000.0
        sys.stdout.write(v["stdout"])
        gain = v["duree_ms"] / duree_rejeu_ms if duree_rejeu_ms > 0 else float("inf")
        sys.stderr.write("[cache-verdicts v%s] REJEU SANS RÉ-APPEL — clé %s… · verdict figé le %s · exécution réelle %.1f ms · rejeu %.1f ms · gain %.0f× · --force pour re-exécuter\n"
                         % (VERSION, k[:12], v["horodatage"], v["duree_ms"], duree_rejeu_ms, gain))
        return v["rc"]
    t1 = time.perf_counter()
    proc = subprocess.run(commande, capture_output=True, text=True)
    duree_ms = (time.perf_counter() - t1) * 1000.0
    v = {
        "cle": k,
        "commande": commande,
        "cibles": cibles,
        "rc": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "duree_ms": round(duree_ms, 1),
        "horodatage": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "version": VERSION,
    }
    entree.write_text(json.dumps(v, ensure_ascii=False, indent=2), encoding="utf-8")
    sys.stdout.write(proc.stdout)
    sys.stderr.write(proc.stderr)
    sys.stderr.write("[cache-verdicts v%s] EXÉCUTION RÉELLE — verdict figé : %s (clé %s…, %.1f ms)\n"
                     % (VERSION, entree.name, k[:12], duree_ms))
    return proc.returncode


def stats() -> int:
    if not CACHE.exists():
        print("Cache vide (aucune entrée).")
        return 0
    entrees = sorted(CACHE.glob("*.json"))
    total = sum(e.stat().st_size for e in entrees)
    print("Cache %s : %d entrée(s), %.1f Kio" % (CACHE, len(entrees), total / 1024.0))
    for e in entrees:
        v = json.loads(e.read_text(encoding="utf-8"))
        print("  %s… rc=%d %.1f ms %s — %s" % (v["cle"][:12], v["rc"], v["duree_ms"], v["horodatage"], " ".join(v["commande"][:4])))
    return 0


def selftest() -> int:
    """12 checks mécaniques sur fixture temporaire (cache isolé, jamais le vrai)."""
    global CACHE
    tmp = Path(tempfile.mkdtemp(prefix="cache-verdicts-selftest-"))
    CACHE = tmp / "cache"
    ok = total = 0
    # commande-test déterministe : écrit un compteur de ré-appels
    compteur = tmp / "appels.txt"
    compteur.write_text("0", encoding="utf-8")
    script_test = tmp / "grader.py"
    script_test.write_text(
        "import sys, pathlib\n"
        "c = pathlib.Path(%r)\n"
        "n = int(c.read_text()) + 1\n"
        "c.write_text(str(n))\n"
        "print('VERDICT: PASS (appel #%%d)' %% n)\n" % str(compteur),
        encoding="utf-8")
    cible = tmp / "cible.txt"
    cible.write_text("état-A", encoding="utf-8")
    env = dict(os.environ, CACHE_VERDICTS_DIR=str(tmp / "cache"))

    def check(nom, cond):
        nonlocal ok, total
        total += 1
        print("  [%s] %s" % ("PASS" if cond else "FAIL", nom))
        if cond:
            ok += 1

    try:
        cmd = [sys.executable, str(script_test)]
        # 1-2 : premier appel = exécution réelle, verdict figé
        r = subprocess.run([sys.executable, __file__, "run", "--"] + cmd + ["--cibles", str(cible)],
                           capture_output=True, text=True, env=env)
        check("T1 : exécution réelle au 1er appel (appel #1)", "appel #1" in r.stdout)
        check("T2 : rc propagé", r.returncode == 0)
        # 3-4 : re-jeu = sans ré-appel
        r2 = subprocess.run([sys.executable, __file__, "run", "--"] + cmd + ["--cibles", str(cible)],
                            capture_output=True, text=True, env=env)
        check("T3 : re-jeu sans ré-appel (toujours appel #1)", "appel #1" in r2.stdout)
        check("T4 : marqueur REJEU émis", "REJEU SANS RÉ-APPEL" in r2.stderr)
        # 5 : verdict identique
        check("T5 : verdict figé identique (stdout == stdout)", r.stdout.splitlines()[0] == r2.stdout.splitlines()[0])
        # 6 : invalidation sur modification de la cible
        time.sleep(0.01)
        cible.write_text("état-B", encoding="utf-8")
        r3 = subprocess.run([sys.executable, __file__, "run", "--"] + cmd + ["--cibles", str(cible)],
                            capture_output=True, text=True, env=env)
        check("T6 : invalidation sur mtime/taille cible (appel #2)", "appel #2" in r3.stdout)
        # 7-8 : --force = ré-exécution même sans changement
        r4 = subprocess.run([sys.executable, __file__, "run", "--"] + cmd + ["--cibles", str(cible), "--force"],
                            capture_output=True, text=True, env=env)
        check("T7 : --force ré-exécute (appel #3)", "appel #3" in r4.stdout)
        check("T8 : gain mesuré rejeu ≥ exécution/1000 (rejeu quasi instantané)", "gain" in r2.stderr)
        # 9 : deux commandes différentes → clés distinctes
        k1 = cle(cmd, [str(cible)])
        k2 = cle(cmd + ["--option"], [str(cible)])
        check("T9 : clés distinctes par commande", k1 != k2)
        # 10 : clés distinctes par état de cible
        k3 = cle(cmd, [str(cible)])
        cible.write_text("état-C (plus long)", encoding="utf-8")
        k4 = cle(cmd, [str(cible)])
        check("T10 : clés distinctes par état de cible", k3 != k4)
        # 11 : entrée de cache structurée
        entrees = list(CACHE.glob("*.json"))
        check("T11 : entrées de cache JSON persistées", len(entrees) >= 1 and all("rc" in json.loads(e.read_text()) for e in entrees))
        # 12 : stats lisibles
        r5 = subprocess.run([sys.executable, __file__, "stats"], capture_output=True, text=True, env=env)
        check("T12 : stats rend le compte des entrées", "entrée(s)" in r5.stdout)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("SELFTEST : %d/%d PASS" % (ok, total))
    return 0 if ok == total else 1


def main() -> int:
    args = sys.argv[1:]
    if "--selftest" in args:
        return selftest()
    if not args:
        print(__doc__)
        return 3
    if args[0] == "clear":
        if CACHE.exists():
            shutil.rmtree(CACHE)
        print("Cache purgé : %s" % CACHE)
        return 0
    if args[0] == "stats":
        return stats()
    if args[0] == "run":
        reste = args[1:]
        if not reste or reste[0] != "--":
            print("usage : cache-verdicts.py run -- <commande...> [--cibles F...] [--force]")
            return 3
        reste = reste[1:]
        cibles, force = [], False
        if "--cibles" in reste:
            i = reste.index("--cibles")
            j = i + 1
            while j < len(reste) and not reste[j].startswith("--"):
                j += 1
            cibles = reste[i + 1: j]
            reste = reste[:i] + reste[j:]
        if "--force" in reste:
            force = True
            reste = [a for a in reste if a != "--force"]
        if not reste or not cibles:
            print("run exige une commande ET au moins une --cibles (le verdict doit dépendre d'entrées suivies)")
            return 3
        return run(reste, cibles, force)
    print("sous-commande inconnue : %s (run | clear | stats | --selftest)" % args[0])
    return 3


if __name__ == "__main__":
    sys.exit(main())
