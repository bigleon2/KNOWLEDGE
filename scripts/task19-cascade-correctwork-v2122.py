#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""task19-cascade-correctwork-v2122.py — Cascade KO-L004 : PM correct-work v2.12.1 → v2.12.2.

Fenêtre 15 (Task 19, session web-220878ed, trace 1a221c134d34e9d1) : la montée
PATCH v2.12.2 du skill correct-work (§1.4bis « Re-jeux et cache de verdicts »)
exige la génération MÉCANIQUE du PM vivant correspondant (pattern delta verrouillé
des cascades précédentes — task72/77/78/84) : substitutions verrouillées
(assert occurrence), archivage R4 byte-identité de l'ancien PM vers
@historique/prompts-maitres/correct-work/, corpus maintenu à 9 fichiers.

Idempotent : si le PM v2.12.2 existe déjà → NO-OP (rc=0, message NO-OP).
Usage : python3 task19-cascade-correctwork-v2122.py [BASE]   (défaut : /home/z/my-project)
Codes retour : 0 = OK ou NO-OP · 1 = FAIL (ancre absente, vérifications).
"""
import shutil
import subprocess
import sys
from pathlib import Path

BASE = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/home/z/my-project")
CORPUS = BASE / "skills" / "@mon-ecosysteme"
HIST = BASE / "skills" / "@historique" / "prompts-maitres" / "correct-work"
OLD = CORPUS / "PROMPT-MAITRE-CORRECT-WORK-v2.12.1.md"
NEW = CORPUS / "PROMPT-MAITRE-CORRECT-WORK-v2.12.2.md"

SECTION_14BIS = """### §1.4bis Re-jeux et cache de verdicts (v2.12.2)

Les re-passes de correct-work re-exécutent des contrôles MÉCANIQUES (arbitres, scanners, batteries) dont les entrées n'ont pas changé entre deux passages. Conformément au hook R2-CACHE de gen-plan (source unique — `scripts/cache-verdicts.py`, jamais de seconde implémentation — R4), correct-work applique la frontière suivante :

1. **Autorisé** : les contrôles mécaniques SANS valeur de preuve finale (re-jeux intermédiaires de rounds de correction, scans répétés à cibles inchangées, vérifications exploratoires) peuvent passer par `python3 scripts/cache-verdicts.py run -- <commande> --cibles <fichiers>` — le re-jeu restitue le verdict figé (rc + stdout) avec le marqueur `REJEU SANS RÉ-APPEL` ; la mention « rejeu (cache) » est consignée dans le sous-rapport du bloc concerné ;
2. **Interdit** : le VERDICT FINAL d'un bloc ou du projet, le mode AVEUGLE (Second Opinion — l'absence de premier verdict est son principe), et toute preuve de certification (idempotence ×2 d'un livrable, verdict producteur) — l'exécution réelle reste la norme de preuve (même frontière que R2-CACHE gen-plan : « un verdict figé n'est JAMAIS une preuve en soi ») ;
3. **Invalidation** : automatique par la clé du wrapper (SHA-256 commande + état taille/mtime_ns des cibles) — toute cible modifiée change la clé et force la ré-exécution réelle ; `--force` disponible pour la re-vérification réelle à la demande ;
4. **Idempotence préservée** : le second passage d'une preuve d'idempotence (×2) reste TOUJOURS une exécution réelle — le cache ne sert qu'aux re-jeux INTRA-exécution qui ne portent pas preuve.

"""

LIGNE_HIST_V2122 = "| v2.12.2 | 2026-11-28 | Re-jeux et cache de verdicts (§1.4bis — directive fenêtre 15 « analyse si mes skills gen-plan, correct-work et clone-chat utilisent des caches sémantiques … optimise-les s'il le faut », trace 1a221c134d34e9d1) : contrôles mécaniques NON-preuve via `scripts/cache-verdicts.py` à entrées inchangées — JAMAIS le verdict final, le mode AVEUGLE ni une preuve d'idempotence ×2 ; invalidation automatique par état des cibles (clé SHA-256 taille/mtime_ns) ; frontière « un verdict figé n'est JAMAIS une preuve en soi » alignée R2-CACHE gen-plan (source unique R4) ; matrice §12 +1 ligne v2.12.2. PATCH. Cascade KO-L004 : PM v2.12.2 (delta verrouillé task19), KB, @historique R4 v2.12.1, invariants ECO_SKILLS ×2 arbres, rescellement archive ×2, replay arbitres. |\n"

LIGNE_MATRICE_V2122 = "| v2.12.2 | Re-jeux et cache de verdicts (§1.4bis) — contrôles mécaniques non-preuve via `cache-verdicts.py`, verdict final / mode AVEUGLE / preuves ×2 toujours réels | ✓ §1.4bis |\n"


def main() -> int:
    if NEW.is_file():
        print("NO-OP : PM v2.12.2 déjà présent (idempotence).")
        return 0
    if not OLD.is_file():
        print(f"FAIL : PM source absent : {OLD}")
        return 1
    t = OLD.read_text(encoding="utf-8")

    def sub(old: str, new: str, n: int = 1) -> None:
        nonlocal t
        c = t.count(old)
        assert c >= n, f"ancre absente ou insuffisante ({c} < {n}) : {old[:80]!r}"
        t = t.replace(old, new, n)

    # 1 — description §1.1 (ligne 55) : matrice + hook de cache
    sub("la matrice de couverture des versions v1.0.0 → v2.12.0 (best-of, §12), le mode PROJET « bloc par bloc » PAR DÉFAUT (v2.12.0), et les métriques de performance.",
        "la matrice de couverture des versions v1.0.0 → v2.12.2 (best-of, §12), le mode PROJET « bloc par bloc » PAR DÉFAUT (v2.12.0), le hook de cache de verdicts (§1.4bis, v2.12.2), et les métriques de performance.")
    # 2 — description YAML-like du PM (ligne 272) : ligne §1.4bis
    sub("  mode PROJET « bloc par bloc » PAR DÉFAUT (v2.12.0 — ex-option `--bloc` v2.9.0 : correct-work(projet) ≡ correct-work (projet) --bloc, vérification bloc par bloc, verdict par bloc),\n",
        "  mode PROJET « bloc par bloc » PAR DÉFAUT (v2.12.0 — ex-option `--bloc` v2.9.0 : correct-work(projet) ≡ correct-work (projet) --bloc, vérification bloc par bloc, verdict par bloc),\n  re-jeux et cache de verdicts (§1.4bis, v2.12.2 : contrôles mécaniques NON-preuve via `scripts/cache-verdicts.py` à entrées inchangées — JAMAIS le verdict final ni le mode AVEUGLE),\n")
    # 3 — insertion section §1.4bis avant §1.5
    sub("### §1.5 Couplage gen-plan (obligatoire — v2.7.0)",
        SECTION_14BIS + "### §1.5 Couplage gen-plan (obligatoire — v2.7.0)")
    # 4 — table historique : ligne v2.12.2 après v2.12.0
    i = t.find("| v2.12.0 | 2026-11-20 |")
    assert i >= 0, "ligne historique v2.12.0 absente"
    fin = t.find("\n", i) + 1
    t = t[:fin] + LIGNE_HIST_V2122 + t[fin:]
    # 5 — matrice §12 : ligne v2.12.2 après v2.12.0
    j = t.find("| v2.12.0 | Mode PROJET « bloc par bloc » PAR DÉFAUT (≡ `--bloc`")
    assert j >= 0, "ligne matrice v2.12.0 absente"
    finj = t.find("\n", j) + 1
    t = t[:finj] + LIGNE_MATRICE_V2122 + t[finj:]

    NEW.write_text(t, encoding="utf-8")

    # Vérifications mécaniques
    tt = NEW.read_text(encoding="utf-8")
    for marqueur in ("§1.4bis Re-jeux et cache de verdicts (v2.12.2)",
                     "re-jeux et cache de verdicts (§1.4bis, v2.12.2",
                     "v1.0.0 → v2.12.2",
                     "| v2.12.2 | 2026-11-28 |",
                     "| v2.12.2 | Re-jeux et cache de verdicts (§1.4bis)"):
        assert marqueur in tt, f"marqueur absent du nouveau PM : {marqueur!r}"

    # Archivage R4 byte-identité de l'ancien PM
    HIST.mkdir(parents=True, exist_ok=True)
    dst = HIST / OLD.name
    if dst.is_file():
        assert dst.read_bytes() == OLD.read_bytes(), "homologue @historique divergent"
    else:
        shutil.copy2(OLD, dst)
    OLD.unlink()
    # git mv de l'archivage si dépôt
    try:
        subprocess.run(["git", "add", "-A", str(dst.relative_to(BASE)), str(NEW.relative_to(BASE)),
                        str(OLD.relative_to(BASE))], cwd=BASE, capture_output=True)
    except Exception:
        pass
    print(f"OK : PM v2.12.2 généré ({len(tt.splitlines())} lignes) ; v2.12.1 archivé R4 "
          f"byte-identité vers @historique/prompts-maitres/correct-work/ ; corpus maintenu à "
          f"{len(sorted(CORPUS.glob('*.md')))} fichiers.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
