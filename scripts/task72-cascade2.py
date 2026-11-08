#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.36)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).
"""

"""task72-cascade2.py — Cascade KO-L004 v3.39.0, volet 2 : README corpus + sceaux @historique.

Édite (substitutions verrouillées count==1, abandon sans écriture) :
  1. README corpus (@mon-ecosysteme/README.md) : révision v2.1.19 (chaîne conservée,
     v2.1.18 passe en « Précédent — ») + arborescence §2 PROMPT-MAITRE-GEN-PLAN
     v3.35.2 → v3.39.0 (lag hérité des cascades v3.36.0→v3.38.0 résorbé) ;
  2. README @historique (@historique/README.md) : §5 49 → 50 PMs + complément
     cascade Task 72 + ligne de sceau SHA-256 pour PROMPT-MAITRE-GEN-PLAN-v3.38.0.md.

Idempotent ×2 (déjà appliqué détecté). Le SHA du PM archivé est recalculé du fichier
réel (jamais pré-écrit — règle d'or n°5).
"""
import hashlib
import sys
from pathlib import Path

RACINE = Path("/home/z/my-project")
README_CORPUS = RACINE / "skills" / "@mon-ecosysteme" / "README.md"
README_HISTO = RACINE / "skills" / "@historique" / "README.md"
PM_ARCHIVE = RACINE / "skills" / "@historique" / "prompts-maitres" / "gen-plan" / \
    "PROMPT-MAITRE-GEN-PLAN-v3.38.0.md"


def sub(texte: str, old: str, new: str, label: str) -> str:
    c = texte.count(old)
    if c != 1:
        print(f"ABANDON : {label} — motif trouvé {c} fois (attendu 1)")
        sys.exit(2)
    return texte.replace(old, new, 1)


REVISION_V219 = (
    "> **Révision v2.1.19 (2026-11-08, Task 72 G1 — session web-ecef7f80, directives "
    "propriétaire « Chantier R1 : re-curation progressive disclosure de gen-plan » [trace "
    "1a1b79af6dcff4c5] + complémentaires 1a1b7b297b7b4975 (skill re-curation implémenté d'un "
    "script — plan Task 72) et 1a1b7fe1c7238e8d (fenêtre native AFFICHE-PLAN))** : gen-plan "
    "v3.38.0→v3.39.0 (**re-curation progressive disclosure R1** — 9 blocs déplacés R4 "
    "byte-identité vers references/ [journal-versions · regles-or + leçons KO · disciplines-"
    "mobilisation · protocoles-detailles] + append contingences grille-token.md, résumés "
    "NOUVEAUX inline ; SKILL.md 104,0 → 29,95 Kio [−71,2 % #token, CRITIQUE → INTERMÉDIAIRE] ; "
    "E7-DISP point 6 « fenêtre native » : la fenêtre des étapes du plan s'affiche via le "
    "mécanisme natif de l'agent dédié à ce rôle [Z.ai : liste de tâches TodoWrite/TodoRead] au "
    "début de l'exécution du plan d'actions + mise à jour à chaque fin d'étape — canal "
    "supplémentaire, points 4/5 et garde P1-P5 inchangés) ; PM v3.39.0 généré mécaniquement "
    "KO-L004 (delta verrouillé scripts/delta-genplan-v3390.json — §1.8/§1.9/§1.12/§1.16 → "
    "résumés compacts miroirs du SKILL.md, intégraux reportés in extenso en §9.7-§9.10, "
    "aucune duplication intra-PM, §9.2 grille-token à jour), v3.38.0 archivé "
    "`@historique/prompts-maitres/gen-plan/` (mv byte-identité R4, SHA scellé §5 README "
    "@historique — 50 PMs) ; SHARED v1.7.34 / PM-INSTALL v1.9.10 recalibrés (générateur) ; "
    "propagation §0 v1.7.34 (69 skills + 173 scripts + 2 agents, contenu stable au re-jeu — "
    "0 divergence SHA) ; ULTRA régénéré ×2 idempotent (SHA 02bf6601…) ; KB gen-plan v3.39.0 + "
    "pin ECO_SKILLS 3.39.0 ; sweep citations 9 skills ; arborescence §2 recalibrée "
    "(GEN-PLAN v3.35.2→v3.39.0 — lag hérité résorbé) ; archive re-scellée v2.3 (corpus 9/9 + "
    "piliers 6/6). Précédent — ")


def main() -> int:
    # ---- 1. README corpus ----------------------------------------------------
    t = README_CORPUS.read_text(encoding="utf-8")
    if "Révision v2.1.19" in t:
        print("  [déjà] README corpus v2.1.19")
    else:
        t = sub(t, "> **Révision v2.1.18 (", REVISION_V219 + "**Révision v2.1.18 (",
                "README corpus révision v2.1.19")
        # en-tête Architecture : SHARED v1.7.27 → v1.7.34 (lag résorbé, cohérence chaîne)
        t = sub(t, "> **Architecture** : v2.2 — SHARED v1.7.27 — Contexte Système 3 niveaux",
                "> **Architecture** : v2.2 — SHARED v1.7.34 — Contexte Système 3 niveaux",
                "README corpus architecture SHARED")
        t = sub(t, "│   ├── PROMPT-MAITRE-GEN-PLAN-v3.35.2.md",
                "│   ├── PROMPT-MAITRE-GEN-PLAN-v3.39.0.md",
                "README corpus arborescence GEN-PLAN")
        README_CORPUS.write_text(t, encoding="utf-8")
        print("  [README corpus] révision v2.1.19 + architecture SHARED v1.7.34 + "
              "arborescence GEN-PLAN v3.39.0 (lag v3.35.2 résorbé)")

    # ---- 2. README @historique (sceaux §5) ------------------------------------
    t = README_HISTO.read_text(encoding="utf-8")
    if "PROMPT-MAITRE-GEN-PLAN-v3.38.0.md | 4c05a74e" in t:
        print("  [déjà] sceau v3.38.0 au README @historique")
    else:
        if not PM_ARCHIVE.exists():
            print("ABANDON : PM v3.38.0 archivé introuvable")
            return 2
        sha = hashlib.sha256(PM_ARCHIVE.read_bytes()).hexdigest()
        t = sub(t, "## 5. Index des fichiers sources archivés (49 PMs — sceau SHA-256)",
                "## 5. Index des fichiers sources archivés (50 PMs — sceau SHA-256)",
                "sceaux en-tête 50 PMs")
        t = sub(t,
                "| Fichier archivé | SHA-256 |\n|-----------------|---------|\n"
                "| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.25.0.md |",
                "| Fichier archivé | SHA-256 |\n|-----------------|---------|\n"
                "| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.38.0.md | " + sha + " |\n"
                "| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.25.0.md |",
                "sceau v3.38.0")
        # complément narratif après le complément v3.22.1
        t = sub(t,
                "SHA-256 scellé ci-dessous).",
                "SHA-256 scellé ci-dessous). Complément cascade Task 72 (2026-11-08, session "
                "web-ecef7f80 — Chantier R1 re-curation progressive disclosure gen-plan v3.39.0) : "
                "`PROMPT-MAITRE-GEN-PLAN-v3.38.0.md` archivé par `mv` byte-identité R4 (round-trip "
                "SHA-256 vérifié par scripts/task72-cascade.py ; sceau ci-dessous).",
                "complément Task 72")
        README_HISTO.write_text(t, encoding="utf-8")
        print(f"  [README @historique] §5 50 PMs + sceau v3.38.0 ({sha[:16]}…) + complément Task 72")

    print("CASCADE 2 terminée.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
