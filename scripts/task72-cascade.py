#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.35)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).
"""

"""task72-cascade.py — Cascade KO-L004 de la montée gen-plan v3.39.0 (Task 72 G1/SG1.4).

Édite (substitutions verrouillées count==1, abandon sans écriture) :
  1. SWEEP 9 skills citant « gen-plan v3.38.0 » → v3.39.0 ;
  2. PIN ECO_SKILLS (check-ecosysteme-integrity.py) 3.38.0 → 3.39.0 + commentaire KO-L004 ;
  3. KB (skills/KNOWLEDGE.md) : en-tête entrée gen-plan v3.39.0 + description E7-DISP
     point 6 « fenêtre native » + « Dernière calibration » v3.39.0 (chaîne conservée) ;
  4. HISTORIQUES-PAR-SKILL (@historique/historiques-par-skill/gen-plan.md) : en-têtes
     (version vivante v3.39.0, 45 PMs archivés — lag v3.37.1 résorbé), compteur famille
     49 versions, ligne v3.39.0, ligne v3.38.0 « VERSION VIVANTE » → « supplantée »,
     liste fichiers archivés + v3.38.0 ;
  5. ARCHIVE PM v3.38.0 R4 : déplacement @mon-ecosysteme/ → @historique/prompts-maitres/
     gen-plan/ (SHA-256 consigné avant déplacement — preuve byte-identité).

Idempotent ×2 : re-jeu = no-op (déjà appliqué détecté). Le script n'invente rien.
"""
import hashlib
import sys
from pathlib import Path

RACINE = Path("/home/z/my-project")
SWEEP = [
    "harness-engineering", "loop-engineering", "fleet-engineering", "graph-engineering",
    "refactoring-engineering", "refactoring-test", "context-engineering",
    "memory-engineering", "spec-driven-development",
]
INTEGRITY = RACINE / "scripts" / "check-ecosysteme-integrity.py"
KB = RACINE / "skills" / "KNOWLEDGE.md"
HISTO = RACINE / "skills" / "@historique" / "historiques-par-skill" / "gen-plan.md"
CORPUS = RACINE / "skills" / "@mon-ecosysteme"
ARCHIVE = RACINE / "skills" / "@historique" / "prompts-maitres" / "gen-plan"
PM_OLD = "PROMPT-MAITRE-GEN-PLAN-v3.38.0.md"

LIGNE_V3390_HISTO = (
    "| v3.39.0 | 2026-11-08 | Task 72 G1 (session web-ecef7f80 — directives « Chantier R1 : "
    "re-curation progressive disclosure de gen-plan » [trace 1a1b79af6dcff4c5] + "
    "complémentaires 1a1b7b297b7b4975 [skill re-curation implémenté d'un script — plan Task 72 : "
    "protocole-test.py PRE/POST/--compare, tests AVANT re-curation] et 1a1b7fe1c7238e8d "
    "[fenêtre native AFFICHE-PLAN]) : **re-curation progressive disclosure R1** — 9 blocs "
    "déplacés R4 byte-identité vers references/ (journal-versions.md · regles-or.md [+ leçons "
    "KO] · disciplines-mobilisation.md · protocoles-detailles.md) + append contingences "
    "(grille-token.md) — résumés NOUVEAUX inline, zéro duplication ; **SKILL.md 104,0 → 29,95 "
    "Kio (−71,2 % #token ≈ 26 616 → 7 667, verdict CRITIQUE → INTERMÉDIAIRE)** ; contrats "
    "baseline golden master D001-D005 PASS (task72-baseline-verifier.py, re-vérifiés "
    "post-amendement SG1.3bis) ; **E7-DISP point 6 « fenêtre native »** : la fenêtre des "
    "étapes du plan s'affiche via le mécanisme natif de l'agent dédié à ce rôle (Z.ai : liste "
    "de tâches TodoWrite/TodoRead) au début de l'exécution du plan d'actions + mise à jour à "
    "chaque fin d'étape — canal supplémentaire (bloc chat, marqueur worklog PLAN-AFFICHE, "
    "garde check_plan_protocol.py P1-P5 inchangés) — intégral references/protocoles-detailles.md ; "
    "MINOR ; cascade KO-L004 : PM v3.39.0 (delta verrouillé scripts/delta-genplan-v3390.json — "
    "§1.8/§1.9/§1.12/§1.16 résumés compacts, intégraux §9.7-§9.10 in extenso, aucune "
    "duplication intra-PM), SHARED v1.7.34 / PM-INSTALL v1.9.10 recalibrés, PM v3.38.0 "
    "archivé R4, pin ECO_SKILLS 3.39.0, ULTRA régénéré, propagation §0, replay arbitres ×2 | "
    "Le plus lourd skill de l'écosystème devient INTERMÉDIAIRE : lecture ciblée = état par "
    "défaut, intégraux à la demande — **VERSION VIVANTE (corpus)** |")


def sub(texte: str, old: str, new: str, label: str) -> str:
    c = texte.count(old)
    if c != 1:
        print(f"ABANDON : {label} — motif trouvé {c} fois (attendu 1)")
        sys.exit(2)
    return texte.replace(old, new, 1)


def main() -> int:
    rapport = []

    # ---- 1. SWEEP 9 skills --------------------------------------------------
    n_sweep = 0
    for s in SWEEP:
        p = RACINE / "skills" / s / "SKILL.md"
        t = p.read_text(encoding="utf-8")
        c = t.count("gen-plan v3.38.0")
        if c == 0 and "gen-plan v3.39.0" in t:
            rapport.append(f"  [déjà] {s}/SKILL.md")
            continue
        if c < 1:
            print(f"ABANDON : sweep {s} — citation v3.38.0 introuvable")
            return 2
        p.write_text(t.replace("gen-plan v3.38.0", "gen-plan v3.39.0"), encoding="utf-8")
        n_sweep += c
        rapport.append(f"  [sweep] {s}/SKILL.md : {c} citation(s) → v3.39.0")

    # ---- 2. PIN ECO_SKILLS --------------------------------------------------
    t = INTEGRITY.read_text(encoding="utf-8")
    if '"gen-plan": "3.39.0"' in t:
        rapport.append("  [déjà] pin ECO_SKILLS 3.39.0")
    else:
        t = sub(t, '"gen-plan": "3.38.0",  # KO-L004 (session web-c30e6506',
                '"gen-plan": "3.39.0",  # KO-L004 (session web-ecef7f80 2026-11-08 — Task 72 G1 : '
                'v3.39.0 re-curation progressive disclosure R1 [9 blocs R4 vers references/, '
                'SKILL.md 104,0→29,95 Kio −71,2 %, CRITIQUE→INTERMÉDIAIRE] + directives '
                'complémentaires 1a1b7b297b7b4975 [skill re-curation par script] et '
                '1a1b7fe1c7238e8d [fenêtre native AFFICHE-PLAN E7-DISP point 6], cascade PM '
                'v3.39.0/SHARED v1.7.34/PM-INSTALL v1.9.10) ; précédent KO-L004 (session web-c30e6506',
                "pin ECO_SKILLS")
        INTEGRITY.write_text(t, encoding="utf-8")
        rapport.append("  [pin] ECO_SKILLS gen-plan 3.38.0 → 3.39.0 + commentaire KO-L004")

    # ---- 3. KB --------------------------------------------------------------
    t = KB.read_text(encoding="utf-8")
    if "## gen-plan v3.39.0" in t:
        rapport.append("  [déjà] KB en-tête v3.39.0")
    else:
        t = sub(t, "## gen-plan v3.38.0", "## gen-plan v3.39.0", "KB en-tête")
        t = sub(t,
                "chaîne 5 points + garde mécanique",
                "chaîne 5 points + point 6 « fenêtre native » (mécanisme natif de l'agent dédié "
                "à l'affichage des étapes — Z.ai : liste de tâches `TodoWrite`/`TodoRead` — "
                "affichée au début de l'exécution du plan d'actions, mise à jour à chaque fin "
                "d'étape ; directive 1a1b7fe1c7238e8d, v3.39.0) + garde mécanique",
                "KB description E7-DISP")
        t = sub(t,
                "- **Dernière calibration** : montée v3.38.0 (2026-11-08, Task 71 G3",
                "- **Dernière calibration** : montée v3.39.0 (2026-11-08, Task 72 G1 — directives "
                "« Chantier R1 : re-curation progressive disclosure de gen-plan » + "
                "complémentaires 1a1b7b297b7b4975 [skill re-curation implémenté d'un script : "
                "protocole-test.py PRE/POST/--compare, tests AVANT re-curation] et "
                "1a1b7fe1c7238e8d [fenêtre native AFFICHE-PLAN]) : **re-curation progressive "
                "disclosure R1** — 9 blocs déplacés R4 byte-identité vers references/ (journal-"
                "versions · regles-or [+ leçons KO] · disciplines-mobilisation · protocoles-"
                "detailles) + append contingences grille-token.md, résumés NOUVEAUX inline, "
                "zéro duplication ; SKILL.md 104,0 → 29,95 Kio (−71,2 % #token, CRITIQUE → "
                "INTERMÉDIAIRE) ; contrats baseline golden master D001-D005 PASS "
                "(task72-baseline-verifier.py, re-vérifiés post-amendement) ; E7-DISP point 6 "
                "« fenêtre native » (Z.ai : liste de tâches TodoWrite/TodoRead — début "
                "d'exécution + chaque fin d'étape, canal supplémentaire) ; cascade KO-L004 : PM "
                "v3.39.0 (delta verrouillé scripts/delta-genplan-v3390.json — intégraux "
                "§9.7-§9.10 in extenso, aucune duplication intra-PM), SHARED v1.7.34 / "
                "PM-INSTALL v1.9.10 recalibrés mécaniquement, PM v3.38.0 archivé R4, pin "
                "ECO_SKILLS 3.39.0, ULTRA régénéré, propagation §0, replay arbitres ; précédente "
                "montée v3.38.0 (2026-11-08, Task 71 G3",
                "KB dernière calibration")
        KB.write_text(t, encoding="utf-8")
        rapport.append("  [KB] en-tête v3.39.0 + description fenêtre native + calibration v3.39.0")

    # ---- 4. HISTORIQUES-PAR-SKILL -------------------------------------------
    t = HISTO.read_text(encoding="utf-8")
    if "**Version vivante (corpus)** : v3.39.0" in t:
        rapport.append("  [déjà] historiques-par-skill v3.39.0")
    else:
        t = sub(t,
                "> **Version vivante (corpus)** : v3.37.1 — "
                "`skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.37.1.md` (sa table §7 fait foi)",
                "> **Version vivante (corpus)** : v3.39.0 — "
                "`skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.39.0.md` (sa table §7 fait foi)",
                "histo version vivante")
        t = sub(t,
                "> **Versions archivées** : 40 PMs (v3.6.1 → v3.37.0) dans "
                "`prompts-maitres/gen-plan/`",
                "> **Versions archivées** : 45 PMs (v3.6.1 → v3.38.0) dans "
                "`prompts-maitres/gen-plan/`",
                "histo versions archivées")
        t = sub(t, "## Famille GEN-PLAN — 48 versions", "## Famille GEN-PLAN — 49 versions",
                "histo compteur famille")
        t = sub(t,
                "replay arbitres ×2 | Les deux leviers du goulot réel #token sont outillés : "
                "mesure du poids de chargement à E5 + verdicts figés ré-jouables sans ré-appel "
                "— **VERSION VIVANTE (corpus)** |",
                "replay arbitres ×2 | Les deux leviers du goulot réel #token sont outillés : "
                "mesure du poids de chargement à E5 + verdicts figés ré-jouables sans ré-appel "
                "— supplantée par v3.39.0 le 2026-11-08 (re-curation progressive disclosure R1 "
                "— Task 72 G1) |",
                "histo ligne v3.38.0")
        t = sub(t,
                "replay arbitres ×2 | Les deux leviers du goulot réel #token sont outillés : "
                "mesure du poids de chargement à E5 + verdicts figés ré-jouables sans ré-appel "
                "— supplantée par v3.39.0 le 2026-11-08 (re-curation progressive disclosure R1 "
                "— Task 72 G1) |",
                "replay arbitres ×2 | Les deux leviers du goulot réel #token sont outillés : "
                "mesure du poids de chargement à E5 + verdicts figés ré-jouables sans ré-appel "
                "— supplantée par v3.39.0 le 2026-11-08 (re-curation progressive disclosure R1 "
                "— Task 72 G1) |\n" + LIGNE_V3390_HISTO,
                "histo insertion ligne v3.39.0")
        t = sub(t,
                "v3.37.1, v3.37.2 (44 fichiers, SHA-256 au §5",
                "v3.37.1, v3.37.2, v3.38.0 (45 fichiers, SHA-256 au §5",
                "histo liste fichiers archivés")
        HISTO.write_text(t, encoding="utf-8")
        rapport.append("  [histo] en-têtes (lag v3.37.1 résorbé) + 49 versions + ligne v3.39.0 + "
                       "v3.38.0 supplantée + liste 45 fichiers")

    # ---- 5. ARCHIVE PM v3.38.0 R4 --------------------------------------------
    src = CORPUS / PM_OLD
    dst = ARCHIVE / PM_OLD
    if dst.exists():
        rapport.append(f"  [déjà] archive {PM_OLD}")
    elif not src.exists():
        print(f"ABANDON : {src} introuvable et archive absente")
        return 2
    else:
        donnees = src.read_bytes()
        sha = hashlib.sha256(donnees).hexdigest()
        dst.write_bytes(donnees)
        src.unlink()
        # round-trip : relecture byte-identique
        if hashlib.sha256(dst.read_bytes()).hexdigest() != sha:
            print("ABANDON : round-trip archive divergent")
            return 2
        rapport.append(f"  [archive] {PM_OLD} → @historique/prompts-maitres/gen-plan/ "
                       f"(SHA-256 {sha[:16]}…, round-trip byte-identique)")

    print("CASCADE KO-L004 v3.39.0 — éditions appliquées :")
    for l in rapport:
        print(l)
    print(f"sweep total : {n_sweep} citation(s) dans {len(SWEEP)} skills")
    return 0


if __name__ == "__main__":
    sys.exit(main())
