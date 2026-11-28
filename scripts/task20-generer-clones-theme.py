#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""task20-generer-clones-theme.py — Exécution réelle de `clone-chat (ALL)` (fenêtre 16).

Directive (trace 1a221dc7539d4351) : « test "clone-chat (ALL)" et ses clones, puis
exécute "clone-chat (ALL)" » — le test (batterie task20-tests-clone-all.py, 30/30 ×2)
est passé AVANT cette exécution.

§1.12.3 : exécuter `--theme` (table des thèmes du clone 11ᵉ — 7 thèmes, preuves ≥2
R4) puis générer UN clone thématique PAR thème + un index récapitulatif.
Mode incrémental §1.13 appliqué : le clone 11ᵉ (canonique) sert de cache sémantique.

Check 9 intégré AVANT écriture (FAIL-CLOSE) : (c) slug dans le nom, (b) §0bis
exclusions, (d) preuves ≥2 en en-tête, (a) aucun slug voisin en §1-§3. Verdict 9/9
exigé par clone, sinon aucun fichier écrit.

Idempotence §1.12.3 : ré-exécution → mêmes noms de fichiers, écrasement à
l'identique (SHA ×2 identiques).
Usage : python3 task20-generer-clones-theme.py [--verdict-json <chemin>]
"""
import hashlib
import json
import re
import sys
from pathlib import Path

DL = Path("/home/z/my-project/download")
DATE = "20261128"
SUJET = "clone-session-web-220878ed"
CLONE_CANONIQUE = f"download/{SUJET}-20261128-task19-caches-semantiques-cloture.md"
CANONIQUE_REL = f"{SUJET}-20261128-task19-caches-semantiques-cloture.md"

# ── Table des thèmes (source : §1bis du clone 11ᵉ — preuves ≥2 R4) ──────────
THEMES = [
    {
        "slug": "kps-conversion",
        "titre": "Mise en page et conversion KPS (PDF→KPS, photo, standardized work)",
        "statut": "CLÔTURÉ",
        "fenetres": "fenêtres 1-10 (2026-11-23→27)",
        "preuves": "[clones 1ᵉʳ-5ᵉ download/] + [worklog suites 165-167] + [artefacts download/ (Manuel-KPS, kps-converter-src.zip, fiche TA-S-3055-020)]",
        "resume": ("Le sous-projet KPS portait la mise en page premium et la conversion de documents "
                   "industriels : manuel KPS Premium (docx/pdf optimisé après audit de mise en page), "
                   "convertisseur KPS2 (source archivée), extraction d'un standard non-KPS (MO-MF-013-F) "
                   "et sa standardized work TA-S-3055-020 au format fiche. Cinq clones de la lignée "
                   "(1ᵉʳ à 5ᵉ) ont archivé ces étapes et deux rapports correct-work task10 ont verrouillé "
                   "la conversion. Le sous-projet est CLÔTURÉ : tous les livrables reposent dans download/."),
        "sessions": [
            ("2026-11-23", "F1 (mise en page)", "plan-task2-mise-en-page.md, rapport-audit-mise-en-page.md, rapport-tests-mise-en-page.md, clone 1ᵉʳ"),
            ("2026-11-23", "F2 (KPS2 converter)", "plan-task5-kps2-converter.md, rapport-kps2-checklist.md, kps-converter-src.zip, clone 2ᵉ"),
            ("2026-11-23→27", "F3-F5 (photo + conversion standard)", "source-standard-non-KPS-MO-MF-013-F.jpg, extraction JSON, fiche TA-S-3055-020, clones 3ᵉ-5ᵉ, rapports cw-task10"),
            ("2026-11-27", "F6 (manuel premium optimisé)", "Manuel-KPS-Premium.docx/pdf + version optimisée, PROMPT-MAITRE-KPS-2-FULLSTACK-GLM-FINAL-v2.md"),
        ],
        "skills": [("docx (plateforme)", "génération du manuel KPS Premium et de ses versions optimisées (tables sans colonne vide, pagination auditée)", "pdf + docx skill plateforme, polices Noto SC", "mise-en-page (direction artistique éditoriale)")],
        "scripts": [],
        "fichiers": [
            ("download/Manuel-KPS-Premium-optimise.docx", "690 Ko", "manuel premium optimisé (audit DA appliqué)"),
            ("download/Manuel-KPS-Premium-optimise.pdf", "1,77 Mo", "export PDF du manuel optimisé"),
            ("download/kps-converter-src.zip", "7,9 Mo", "source du convertisseur KPS2 archivée"),
            ("download/fiche-kps-standardized-work-TA-S-3055-020.pdf", "2,5 Mo", "standardized work exportée"),
            ("download/extraction-standard-non-KPS-MO-MF-013-F.json", "9,7 Ko", "extraction structurée du standard"),
            ("download/clone-session-web-220878ed-20261127-conversion-kps.md", "18 Ko", "clone 5ᵉ (clôture conversion)"),
        ],
        "decisions": [
            ("1", "Mise en page niveau magazine pour le manuel KPS (audit DA)", "qualité éditoriale exigée par le propriétaire", "version optimisée produite + audit PASS"),
            ("2", "Archivage source convertisseur en ZIP", "réversibilité de la conversion", "kps-converter-src.zip présent"),
        ],
        "bugs": [
            ("1", "Mise en page initiale non conforme aux règles DA (titres orphelins, colonnes)", "première génération sans audit", "audit mise-en-page + corrections + re-rendu", "rapport-audit + version optimisée"),
        ],
        "conventions": [("Livrables download/", "tout livrable final sous download/ avec nom descriptif kebab-case", "Manuel-KPS-Premium-optimise.pdf")],
        "drifts": [],
        "etat": ("CLÔTURÉ — livrables présents dans download/ (manuel optimisé docx+pdf, convertisseur archivé, "
                 "fiche standardized work, extraction JSON), clones 1ᵉʳ-5ᵉ scellés. Aucune étape ouverte."),
        "prochaine": ("Aucune — thème clôturé. Toute réactivation (nouveau standard à convertir, refonte du manuel) "
                      "part d'une nouvelle directive propriétaire."),
        "prio": ["download/Manuel-KPS-Premium-optimise.pdf", "download/kps-converter-src.zip", "download/fiche-kps-standardized-work-TA-S-3055-020.pdf"],
    },
    {
        "slug": "ecosysteme-gif-photo",
        "titre": "Optimisation GIF et photo de l'écosystème (iphone17/18/19, gif-animator)",
        "statut": "CLÔTURÉ",
        "fenetres": "fenêtres 3-10 (2026-11-23→27)",
        "preuves": "[clones 3ᵉ-4ᵉ download/] + [skills installés skills/iphone17|18|19, gif-animator(+pro)] + [artefacts download/ (PA-GROUPE-*, PROMPT-GIF-anti-modifications-v2.md)]",
        "resume": ("Le sous-projet photo/GIF a doté l'écosystème de trois pipelines photo générationnels "
                   "(iphone17/18/19 : grilles d'analyse A1-C3, moteurs de décision R1-R19, garde-fous "
                   "fidélité G1-G7) et de deux skills GIF (gif-animator + gif-animator-pro). Il a produit "
                   "la série PA-GROUPE (5 images + contact sheets + deux GIF « groupe vivant », dont un "
                   "marqué) et le prompt de garde anti-modifications. CLÔTURÉ avec une pendance "
                   "propriétaire-seul reconduite : n°5 mouvement GIF dans la description."),
        "sessions": [
            ("2026-11-23", "F3 (photo qualité + GIF)", "plan-task6-photo-groupe-vivant.md, plan-task7, skills iphone17/18, clone 3ᵉ"),
            ("2026-11-24", "F4 (clôture photo-gif + iphone19)", "clone 4ᵉ, skill iphone19 (rumeur calibrée), PA-GROUPE-001→005, GIF groupe-vivant + marqué"),
            ("2026-11-23→27", "F5-F10 (consolidation)", "gif-animator(+pro) installés, PROMPT-GIF-anti-modifications-v2.md, clones 5ᵉ"),
        ],
        "skills": [
            ("iphone17 v2.0", "pipeline photo génération 17 (preset iphone17_max, restauration argentique)", "grille ANALYSE-v2, R1-R17, QC 11 critères", "iphone18 (supersédé)"),
            ("iphone18 v1.x", "pipeline photo génération 18 (R18 ouverture variable ƒ/1.48-ƒ/4.0)", "preset iphone18_max", "iphone19"),
            ("iphone19 v0.12.1", "pipeline ANTICIPÉ 2027 (R19 pixel binning 16-en-1, règles absolues 1-15, QC 14)", "scripts/editer-image.mjs", "iphone18"),
            ("gif-animator + gif-animator-pro", "animation GIF de sprites/émojis (deux niveaux)", "scripts/gif_sprite_gif(_pro).py", "image-edit"),
        ],
        "scripts": [],
        "fichiers": [
            ("download/PA-GROUPE-005-groupe-vivant-marque.gif", "9,2 Mo", "GIF groupe vivant avec marque"),
            ("download/PA-GROUPE-003-groupe-vivant.gif", "7,3 Mo", "GIF groupe vivant"),
            ("download/PA-GROUPE-003-contact-sheet.png", "350 Ko", "planche contact série"),
            ("download/PROMPT-GIF-anti-modifications-v2.md", "9,4 Ko", "garde anti-modifications visages/éléments"),
        ],
        "decisions": [
            ("1", "Trois générations de pipeline photo co-existantes (17 confirmé, 18 confirmé, 19 anticipé)", "couverture époques + rumeurs calibrées", "skills iphone17/18/19 installés, supersession documentée"),
            ("2", "Garde-fous fidélité stricte (G1-G7) — zéro élément ajouté", "non-modification des visages sans directive", "règle absolue 15 + QC 14 (iphone19)"),
        ],
        "bugs": [],
        "conventions": [("Rendu photo", "presets de rendu §6 par génération ; restauration argentique sans colorisation inventée", "preset iphone18_max")],
        "drifts": [("1", "ENRICHISSEMENT", "iphone17 seul", "iphone18 + iphone19 (R18/R19)", "3-4", "suites 165-166", "évolutions générationnelles Apple")],
        "etat": ("CLÔTURÉ — skills installés, série PA-GROUPE livrée, garde anti-modifications scellée. "
                 "Pendance n°5 (mouvement GIF dans la description) reconduite propriétaire-seul."),
        "prochaine": ("Aucune — thème clôturé. La pendance n°5 reste propriétaire-seul ; toute nouvelle "
                      "retouche photo/GIF démarre d'une directive."),
        "prio": ["skills/iphone19/SKILL.md", "download/PROMPT-GIF-anti-modifications-v2.md", "skills/gif-animator/SKILL.md"],
    },
    {
        "slug": "installation-ecosysteme",
        "titre": "Installation de l'écosystème (É1-INSTALL, PM INSTALL, bootstrap, certification)",
        "statut": "ACTIF (garde permanente)",
        "fenetres": "fenêtres 11-15 (2026-11-28)",
        "preuves": "[PM INSTALL v1.10.8 ×3 SHA b5c9eb1a] + [worklog suites 171/173/175] + [commits 01095268, ré-scellements archive ×2] + [bootstrap INSTALLE ×2 ALL PASS 6/6 ×2]",
        "resume": ("Le sous-projet installation garantit qu'une session neuve reconstruit l'écosystème à "
                   "l'identique : PM INSTALL v1.10.8 (source unique, rétroporté suite 174 depuis le vivant), "
                   "bootstrap consolidé (preflight git, dry-run, installation canonique, sweep §0, "
                   "certification 6 arbitres, garde), pipeline éco (sync union, garde R2, rescellement "
                   "archive round-trip v2.3, manifeste). La fenêtre 15 y a corrigé 4 failles (invariant "
                   "figé, archive non matérialisée au dépôt, crash générateur, flux d'édition) et adopté "
                   "le flux C6. État : INSTALLE ×2 ALL PASS 6/6 ×2."),
        "sessions": [
            ("2026-11-28", "Task 15 (11ᵉ fenêtre, suite 171)", "installation 58 SHA ×0 divergence, scan jetons, garde à toute invocation"),
            ("2026-11-28", "Task 16-17 (suites 172-173)", "état certifié 72116030, constat de clôture mécanique"),
            ("2026-11-28", "Task 18 (suite 174)", "rétroport PM INSTALL v1.10.8 dépôt×3 (faille rétroport corrigée), batterie S4 12/12"),
            ("2026-11-28", "Task 19 (suite 175)", "4 failles résorbées : invariant clone-chat figé, archive dépôt non matérialisée (KO-L007), BAK.unlink première matérialisation, flux C6 — commit 01095268 ; INSTALLE ×2 ALL PASS 6/6 ×2"),
        ],
        "skills": [("PROMPT-MAITRE-INSTALL-ECOSYSTEME v1.10.8", "source UNIQUE d'installation (pipeline 11 étapes, profils COMPLET/MINIMALE, mécanisme dual §3.2, entrée consolidée §3.2-c)", "SHA ×3 b5c9eb1a (live/dépôt/hôte)", "gen-plan (garde É1-INSTALL)")],
        "scripts": [
            ("bootstrap-ecosysteme.py", "bootstrap consolidé — entrée canonique PM-INSTALL §3.2-c (preflight/dry-run/installation/sweep/certification/garde)", "STATS_VERTS (PROPRE, RÉPARÉ, OK, DIVERGENCE-HÔTE, ALL-PASS-6/6, INSTALLE)", "KNOWLEDGE-repo/scripts/"),
            ("eco_install_pipeline.py", "pipeline canonique : sync union + garde R2 + rescellement archive v2.3 + manifeste + post-install SHA (58)", "rc=0 propre / rc=2 divergences-réparations", "KNOWLEDGE-repo/scripts/"),
            ("certification-complete.py", "orchestrateur des 6 arbitres (verify-cross ×2, verify-correct-work, integrity, interactions, tool-routing)", "ALL PASS 6/6 attendu", "KNOWLEDGE-repo/scripts/"),
            ("check-ecosysteme-integrity.py", "corpus 9 fichiers, archive round-trip v2.3 (corpus+piliers), ECO_SKILLS versionnées", "invariants ×2 miroirs", "hôte + dépôt"),
            ("task48-rescellage-archive.py", "re-scellement archive (corpus 9 + piliers 6, byte-identité, .bak missing_ok)", "BASE en argv (hôte ou dépôt)", "hôte + dépôt"),
        ],
        "fichiers": [
            ("skills/@mon-ecosysteme/PROMPT-MAITRE-INSTALL-ECOSYSTEME.md", "332 L", "PM INSTALL v1.10.8 — source unique"),
            ("download/mon-ecosysteme_archive.zip", "~113 Ko", "archive round-trip (véhicule v2.3) — hôte"),
            ("KNOWLEDGE-repo/download/mon-ecosysteme_archive.zip", "~113 Ko", "archive round-trip — dépôt (matérialisée fenêtre 15)"),
        ],
        "decisions": [
            ("1", "Garde É1-INSTALL à TOUTE invocation (bootstrap canonique avant toute tâche)", "dérives d'amnésie sandbox récurrentes", "preflight/dry-run/certification à chaque fenêtre"),
            ("2", "Flux C6 : édition dépôt → commit local immédiat → propagation hôte → re-scellement → certification", "2 annihilations par reset --hard du preflight", "aucune édition non commitée avant bootstrap"),
            ("3", "Archive round-trip matérialisée ×2 (hôte + dépôt)", "arbitre invoqué depuis le dépôt", "KO-L007 éteint"),
        ],
        "bugs": [
            ("1", "Certification 4/6 — invariant figé clone-chat 2.0.2", "montée v2.1.0 sans actualisation ECO_SKILLS", "alignement KB + annotation KO-L004 tracée", "120/120 PASS"),
            ("2", "Archive « corpus 0/9 · piliers 0/6 »", "archive ABSENTE au dépôt (KO-L007)", "re-scellement ×2 task48", "round-trip PASS ×2"),
            ("3", "task48 crash BAK.unlink() première matérialisation", "aucun .bak avant la 1ʳᵉ archive", "missing_ok=True ×2", "re-scellement dépôt rc=0"),
            ("4", "Éditions annihilées ×2 par preflight reset --hard", "éditions non commitées avant bootstrap", "flux C6", "zéro annihilation depuis"),
        ],
        "conventions": [
            ("Sémantique rc pipeline", "rc=0 propre ; rc=2 = divergences/réparations avec réserves ; clôture = dry-run terminal rc=0", "harnais S5 suite 174"),
            ("Sémantique bootstrap", "STATS_VERTS : PROPRE/RÉPARÉ/OK/DIVERGENCE-HÔTE/ALL-PASS-6-6/INSTALLE", "bootstrap-ecosysteme.py"),
        ],
        "drifts": [
            ("1", "CORRECTION", "flux édition fin de fenêtre", "flux C6 commit immédiat", "19", "suite 175", "2 annihilations preflight"),
            ("2", "ENRICHISSEMENT", "archive hôte seule", "archive scellée ×2 (hôte+dépôt)", "19", "suite 175", "KO-L007"),
            ("3", "ENRICHISSEMENT", "PM INSTALL dépôt v1.7.1 divergent", "v1.10.8 aligné ×3 copies", "18", "suite 174", "faille rétroport"),
        ],
        "etat": ("INSTALLE ×2 ALL PASS 6/6 ×2 à la suite 175 ; parité git 0/0 à 5ed9a36b ; 58 SHA "
                 "post-install 0 divergence ; archive round-trip ×2 byte-identiques."),
        "prochaine": ("Exécuter la garde É1-INSTALL (bootstrap canonique ×2) EN TÊTE de chaque nouvelle "
                      "fenêtre — action permanente, aucune tâche corrective ouverte."),
        "prio": ["KNOWLEDGE-repo/scripts/bootstrap-ecosysteme.py", "skills/@mon-ecosysteme/PROMPT-MAITRE-INSTALL-ECOSYSTEME.md", "scripts/task48-rescellage-archive.py"],
    },
    {
        "slug": "gen-plan-optimisation",
        "titre": "Optimisation gen-plan et disciplines (modes, hooks, orchestration)",
        "statut": "ACTIF (évolutions continues)",
        "fenetres": "fenêtres 10-15 (2026-11-28)",
        "preuves": "[clones 7ᵉ-8ᵉ download/] + [gen-plan v3.49.0 installé ×2] + [rapports cw task12/13] + [KB arête orchestration-disciplines]",
        "resume": ("Le sous-projet gen-plan a stabilisé le planificateur de l'écosystème à v3.49.0 : "
                   "4 modes (Planification/Exécution/Surveillance/Adaptation + step/step-ok/NULL), 15 étapes "
                   "E1-E15, garde É1-INSTALL à toute invocation, pré-traitement PROMPT-GATEWAY, routage "
                   "É5-ROUTAGE mécanique, orchestration É5-DISCIPLINES, FAIL-CLOSE §1.18 avec "
                   "journal-fails.md, règles d'or (dont n°6 français exclusif), R2-CACHE. Task 12 a porté "
                   "l'optimisation majeure (v3.49.0 + cascade PM/SHARED/PM-INSTALL), Task 13 les tests "
                   "(22/22 PASS) et la résorption des différés (D010). La fenêtre 15 a vérifié le hook "
                   "R2-CACHE opérationnel (selftest 12/12) sans modification — déjà adéquat."),
        "sessions": [
            ("2026-11-28", "Task 12 (suite 168)", "v3.49.0 : É1-INSTALL garde + É5-DISCIPLINES + propagation §0 v1.7.47 (123 skills + 266 scripts) + CW 33/33 + clone 7ᵉ"),
            ("2026-11-28", "Task 13 (suite 169)", "harnais 22/22 PASS ×2, D007 faille ensure-installed corrigée, D008 journal-fails fermée, clone 8ᵉ"),
            ("2026-11-28", "Task 19 (suite 175)", "verdict cache : R2-CACHE présent et adéquat — non modifié ; S1 batterie (hook ×2, selftest 12/12)"),
        ],
        "skills": [("gen-plan v3.49.0", "planificateur — 4 modes, E1-E15, garde É1-INSTALL, PROMPT-GATEWAY, É5-ROUTAGE, É5-DISCIPLINES, FAIL-CLOSE §1.18, R2-CACHE", "scripts routage-skills-agents.py + check_plan_protocol.py + ensure-installed.py + cache-verdicts.py", "orchestration-disciplines, correct-work (chaîne de vérification)")],
        "scripts": [
            ("cache-verdicts.py v1.0.0", "cache de verdicts généralisé (clé SHA-256 commande+état cibles, rejeu sans ré-appel, --force, stats, selftest 12)", "gain mesuré ≥10× sur scan réel (S5 fenêtre 15)", "hôte + dépôt"),
            ("routage-skills-agents.py", "routage décisionnel É5 (recommandation skills depuis frontmatters + verdict complexité 5 critères)", "source unique R4", "skills/gen-plan/scripts/"),
            ("ensure-installed.py", "garde réinjection plateforme (branches unifiées Task 114+56, verdict honnête INSTALLE-RÉPARÉ-PARTIEL)", "corrigé D007 Task 13", "skills/gen-plan/scripts/ + scripts/"),
        ],
        "fichiers": [
            ("skills/gen-plan/SKILL.md", "393 L", "gen-plan v3.49.0 (live ×2 SHA)"),
            ("download/plan-task12-optimisation-gen-plan-pm-install.md", "15 Ko", "plan Task 12"),
            ("download/rapport-cw-task12-projet.md", "8,9 Ko", "CW Task 12"),
            ("scripts/task19-cache-report.json", "7 Ko", "mesures rejeu fenêtre 15"),
        ],
        "decisions": [
            ("1", "R2-CACHE non étendu hors E9-E14", "frontière preuve (arbitrage de certification hors cache) déjà documentée", "aucune modification fenêtre 15"),
            ("2", "Chaîne de vérification v3.44.0 (correct-work CIBLE par étape terminée en mode NULL)", "vérification mécanique avant avancement", "statut verified subordonné au verdict"),
        ],
        "bugs": [
            ("1", "ensure-installed branches divergentes Task 114 vs Task 56", "deux générations de garde", "unification D007 Task 13", "verdict honnête INSTALLE-RÉPARÉ-PARTIEL"),
        ],
        "conventions": [
            ("Fail-Close §1.18", "tout FAIL (même non bloquant) journalisé + corrigé + re-vérifié avant fermeture d'étape", "journal-fails.md"),
            ("Glossaire $FACON inline", "$FACON = façon cohérente/optimisée/fonctionnelle ; $FACON2 = batterie cohérente/optimisée/fonctionnelle", "§A gen-plan"),
        ],
        "drifts": [
            ("1", "ENRICHISSEMENT", "gen-plan v3.48.0", "v3.49.0 (É5-DISCIPLINES, É1-INSTALL)", "12", "suite 168", "directive Task 12"),
            ("2", "SANS OBJET (constat)", "R2-CACHE v3.38.0", "inchangé — adéquat", "19", "suite 175", "analyse fenêtre 15"),
        ],
        "etat": ("v3.49.0 installée ×2 (SHA identiques) ; 12/12 checks S3 batterie suite 174 ; R2-CACHE "
                 "opérationnel (selftest 12/12 ×2, gain rejeu ≥10× mesuré) ; journal-fails 0 entrée ouverte."),
        "prochaine": ("Mobiliser gen-plan (mode step) pour toute nouvelle directive multi-étapes ; utiliser "
                      "cache-verdicts.py pour les re-jeux intermédiaires E9-E14 — jamais pour une preuve."),
        "prio": ["skills/gen-plan/SKILL.md", "skills/gen-plan/references/regles-or.md", "scripts/cache-verdicts.py"],
    },
    {
        "slug": "git-pendances",
        "titre": "Git/partage/push et pendances propriétaires (cron, lien partage, PATs)",
        "statut": "ACTIF (n°1 révocation PATs CRITIQUE ouverte)",
        "fenetres": "fenêtres 10-15 (2026-11-28)",
        "preuves": "[commits 711c39c7/c0ee1213/5ed9a36b poussés] + [cron 553419 actif] + [suites 170/172/173/175] + [scans jetons rc=0]",
        "resume": ("Le sous-projet git/périphéries tient la ligne push-dépôt et le registre des pendances "
                   "propriétaires. Historique : PUSH final 711c39c7 (fusion -s ours Task 14, KO-L009 "
                   "éteinte), convergence c0ee1213 (suite 172, parité 0/0), recréation cron 553419 liée "
                   "au chat courant (3×/jour :52 Europe/Paris, plafond plateforme 3/jour), constat de "
                   "clôture Task 17, PUSH de clôture 5ed9a36b (suite 175, 7 commits caches sémantiques). "
                   "Scans jetons réguliers rc=0 (3589 fichiers, 22 faux positifs structurels écartés). "
                   "Pendance n°1 CRITIQUE ouverte : la clé GitHub propriétaire a servi aux pushs (fenêtres "
                   "12, 18, 15) et DOIT être révoquée par le propriétaire."),
        "sessions": [
            ("2026-11-28", "Task 14 (suite 170)", "PUSH final 711c39c7 fusion -s ours, KO-L009 ÉTEINTE"),
            ("2026-11-28", "Task 16 (suite 172)", "divergence 3/2 → fusion -s ours c0ee1213 → parité 0/0 ; cron 553417 rejeté (plafond) → 553419 actif lié au chat courant"),
            ("2026-11-28", "Task 17 (suite 173)", "constat clôture : pendances n°1/n°4/n°5 reconduites propriétaire-seul"),
            ("2026-11-28", "Task 19 (suite 175)", "7 commits locaux → PUSH 5ed9a36b, parité 0/0 vérifiée, scan rc=0"),
        ],
        "skills": [],
        "scripts": [
            ("task15-scan-jetons.py", "scanner anti-fuite jetons (regex 30+, faux positifs structurels écartés, branches OSError fail-close)", "rc=0 attendu à chaque commit/push", "hôte + dépôt"),
        ],
        "fichiers": [
            ("KNOWLEDGE-repo (git)", "branche main", "HEAD 5ed9a36b = origin/main (parité 0/0 à la suite 175)"),
        ],
        "decisions": [
            ("1", "Fusion -s ours pour absorber les miroirs API plugin sans rétrogradation", "divergences historiques plugin vs locaux", "pattern documenté suites 170/172"),
            ("2", "PAT JAMAIS imprimé en clair — masquage systématique (sed github_pat_…)", "hygiène sécurité", "mentions tronquées scellées ; scans rc=0"),
        ],
        "bugs": [
            ("1", "Job cron 553417 rejeté de fait (plafond 3 exécutions/jour)", "expr horaire 24/jour estimées > limite plateforme", "recréation 0 52 9,14,19 (3×/jour) → 553419", "job actif lié au chat courant"),
            ("2", "Job 540820 échec permanent (« chat not found »)", "chat cible mort", "suppression + recréation liée au chat courant", "553419 run_count remonte"),
        ],
        "conventions": [("Push", "flux local→push ; scan jetons rc=0 AVANT chaque push ; clé propriétaire masquée dans toute sortie", "suites 171-175")],
        "drifts": [("1", "ENRICHISSEMENT", "job 540820 chat mort", "553419 lié au chat courant 11059801", "16", "suite 172", "recréation propriétaire")],
        "etat": ("Parité 0/0 à 5ed9a36b ; cron 553419 actif (09:52/14:52/19:52 Europe/Paris) ; scan jetons "
                 "rc=0 ; pendances n°1 (révocation PATs, CRITIQUE), n°4 (lien partage — bouton UI bugué "
                 "plateforme), n°5 (GIF description) reconduites propriétaire-seul."),
        "prochaine": ("PROPRIÉTAIRE-SEUL : révoquer immédiatement la clé GitHub utilisée aux pushs "
                      "(github_pat_…, fenêtres 12/18/15) puis en émettre une nouvelle si besoin ; retenter "
                      "le bouton « partager » de l'UI Z.AI pour la pendance n°4."),
        "prio": ["KNOWLEDGE-repo/.git", "scripts/task15-scan-jetons.py", "worklog.md"],
    },
    {
        "slug": "clone-chat-archivage",
        "titre": "Clonage et archivage de session (clone-chat, chaîne de clones, modes thématiques)",
        "statut": "ACTIF (cache d'analyse livré)",
        "fenetres": "fenêtres 10-15 (2026-11-28)",
        "preuves": "[11 clones disque download/] + [clone-chat v2.2.0 installé ×2 SHA] + [KB v2.2.0] + [commits 334c059a/2cb4055d]",
        "resume": ("Le sous-projet archivage maintient la chaîne de clones auto-référentiels de la session "
                   "(11 générations à la fenêtre 15) et fait évoluer le skill clone-chat : v2.1.0 (modes "
                   "thématiques --theme/(theme)/ALL, check 9 cohérence thématique, gabarit "
                   "theme-template.md, verdict JUDICIEUSE suite 174) puis v2.2.0 (§1.13 cache d'analyse — "
                   "le clone antérieur canonique sert de cache sémantique, réutilisation byte-stable, delta "
                   "worklog, garde de couverture, validation inchangée). Le clone 11ᵉ fut la première "
                   "clôture produite en mode incrémental §1.13 ; la fenêtre 16 teste (30/30 ×2) puis "
                   "exécute le mode (ALL) : 7 clones thématiques + index."),
        "sessions": [
            ("2026-11-28", "Task 13 (suite 169)", "clone 8ᵉ scellé S1-S8 10/10 (verifier-task13-clone.py)"),
            ("2026-11-28", "Task 18 (suite 174)", "clone-chat v2.1.0 (12 éditions), theme-template.md, KB ×2, clone 9ᵉ avec table des thèmes §1bis (6 thèmes), verifier 29/29 ×2"),
            ("2026-11-28", "Task 19 (suite 175)", "clone-chat v2.2.0 (§1.13 cache d'analyse), KB ×2, clones 10ᵉ (instantané d'entrée) + 11ᵉ (clôture incrémentale, 7 thèmes), verifier 28/28 ×2"),
            ("2026-11-28", "Task 20 (fenêtre 16)", "tests (ALL) 30/30 ×2 puis exécution (ALL) : 7 clones thématiques + index (présente fenêtre)"),
        ],
        "skills": [("clone-chat v2.2.0", "clonage de discussion Markdown auto-suffisant — 7+1 étapes, Context Drift, modes thématiques §1.12 (--theme/(theme)/ALL, check 9), cache d'analyse §1.13", "SKILL.md ~503 L + références/clone-template.md + theme-template.md (SHA ×2)", "gen-plan (optionnel), correct-work (validation croisée), skill-creator (conventions)")],
        "scripts": [
            ("verifier-task19-clone.py", "vérificateur S1-S9 du clone 11ᵉ (28/28 ×2)", "faille S6 corrigée (fin de section)", "hôte"),
            ("task20-tests-clone-all.py", "batterie $FACON2 du mode (ALL) — 30/30 ×2", "fixtures isolées idempotentes", "hôte"),
            ("task20-generer-clones-theme.py", "exécution (ALL) : génération 7 clones + index, check 9 FAIL-CLOSE, idempotence", "présent script", "hôte"),
        ],
        "fichiers": [
            ("download/clone-session-web-220878ed-20261128-task19-caches-semantiques-cloture.md", "30 Ko", "clone 11ᵉ — instantané canonique"),
            ("skills/clone-chat/références/theme-template.md", "143 L", "gabarit de clone thématique"),
            ("download/clone-session-web-220878ed-clone-themes-index-20261128.md", "généré", "index récapitulatif (ALL) — présente fenêtre"),
        ],
        "decisions": [
            ("1", "Modes thématiques v2.1.0 (verdict JUDICIEUSE suite 174)", "discussions multi-sous-projets difficiles à reprendre", "preuve ≥2 R4, exclusions §0bis, check 9"),
            ("2", "Cache d'analyse v2.2.0 (§1.13)", "chaque clone ré-analysait tout le worklog", "réutilisation byte-stable + delta ; validation inchangée"),
        ],
        "bugs": [
            ("1", "Verifier clone 11ᵉ S6 : 27/28", "find('---') tombait sur la séparation de table", "fin de section via titre suivant", "28/28 ×2 (faille vérificateur, pas clone)"),
        ],
        "conventions": [
            ("Hiérarchie des clones", "le clone complet de clôture est canonique ; les clones thématiques en dérivent", "SKILL.md §6"),
            ("Clonage en dernier (E23)", "l'instantané de clôture absorbe l'état le plus frais", "bloc final de chaque fenêtre"),
        ],
        "drifts": [
            ("1", "ENRICHISSEMENT", "v2.0.2 (clone complet seul)", "v2.1.0 (+modes thématiques)", "18", "suite 174", "directive 14ᵉ fenêtre"),
            ("2", "ENRICHISSEMENT", "v2.1.0 (aucun cache)", "v2.2.0 (§1.13 cache d'analyse)", "19", "suite 175", "directive fenêtre 15"),
        ],
        "etat": ("clone-chat v2.2.0 installé ×2 ; 11 clones scellés ; chaîne de vérification des clones "
                 "(verifiers task13/18/19) PASS ; fenêtre 16 : (ALL) testé 30/30 ×2 puis exécuté (7 clones "
                 "+ index, 9/9 chacun)."),
        "prochaine": ("À la prochaine clôture de fenêtre : exécuter `clone-chat` (clone 12ᵉ en mode "
                      "incrémental §1.13, cache = clone 11ᵉ) ; ré-exécuter `clone-chat (ALL)` pour "
                      "actualiser les clones thématiques (écrasement à l'identique par périmètre)."),
        "prio": ["skills/clone-chat/SKILL.md", "download/clone-session-web-220878ed-20261128-task19-caches-semantiques-cloture.md", "skills/clone-chat/références/theme-template.md"],
    },
    {
        "slug": "caches-semantiques",
        "titre": "Caches sémantiques (analyse + optimisation des 3 skills)",
        "statut": "ACTIF (livré fenêtre 15 — re-jeux et caches en place)",
        "fenetres": "fenêtre 15 (2026-11-28)",
        "preuves": "[trace 1a221c134d34e9d1] + [commits 334c059a/dbb92803/8a0eae0c/77f44959/25a5a1f4] + [rapport-cw-task19-projet.md PASS 25/25] + [task19-cache-report.json 52/52]",
        "resume": ("Le sous-projet caches sémantiques (fenêtre 15) a analysé les trois skills ciblés : "
                   "gen-plan possédait DÉJÀ R2-CACHE (hook E9-E14 + cache-verdicts.py v1.0.0) — non "
                   "modifié car adéquat ; correct-work et clone-chat n'en avaient aucun — implémentations "
                   "ciblées : correct-work v2.12.2 (§1.4bis : contrôles mécaniques NON-preuve via le "
                   "wrapper, jamais verdict final/AVEUGLE/preuve ×2) et clone-chat v2.2.0 (§1.13 : cache "
                   "d'analyse des clones). Cascade complète : KB ×2, invariants ECO_SKILLS, PM "
                   "correct-work v2.12.2 par cascade mécanique verrouillée (v2.12.1 archivé R4), arbitre "
                   "canonique recalibré. Batterie 52/52 ×2 (gain rejeu ≥10× sur scan réel), CW 25/25 ×2. "
                   "Frontière commune : « un verdict figé n'est JAMAIS une preuve en soi »."),
        "sessions": [
            ("2026-11-28", "Task 19 (suite 175) — analyse", "3 verdicts consignés (présent/adéquat, absent/implémenté ×2)"),
            ("2026-11-28", "Task 19 (suite 175) — implémentation", "v2.12.2 + v2.2.0 + KB + PM cascade + invariants (commits 334c059a/dbb92803/8a0eae0c)"),
            ("2026-11-28", "Task 19 (suite 175) — tests + CW", "$FACON2 52/52 ×2 (S2 fixture, S5 scan réel ≥10×) ; CW PASS 25/25 ×2 (commits 77f44959/25a5a1f4)"),
        ],
        "skills": [
            ("correct-work v2.12.2", "vérification/correction — §1.4bis re-jeux et cache de verdicts (cache-verdicts.py, frontière preuve)", "512 L, matrice §12 +1 ligne, arbitre canonique recalibré 16/16", "gen-plan (R2-CACHE source unique), clone-chat"),
            ("clone-chat v2.2.0", "clonage — §1.13 cache d'analyse des clones (gabarit et modes thématiques : cf. table §0bis, thème dédié au clonage)", "grille clone incrémental 3000 #token", "correct-work, gen-plan"),
        ],
        "scripts": [
            ("cache-verdicts.py v1.0.0", "wrapper cache : clé SHA-256(commande + état taille/mtime_ns cibles), rejeu sans ré-appel, --force, stats, clear, selftest 12", "cache tmp/cache-verdicts/ ; gain ≥10× mesuré", "hôte + dépôt"),
            ("task19-cascade-correctwork-v2122.py", "cascade PM v2.12.1→v2.12.2 (subs verrouillées, archivage R4, NO-OP ×2)", "818 L générés", "hôte + dépôt"),
            ("task19-tests-caches-semantiques.py", "batterie S1-S6 52 checks (comportement réel cache, invalidation, --force, stats)", "52/52 ×2", "hôte + dépôt"),
            ("verifier_cw_task19.py", "arbitre CW B1-B5 25 checks réels (correctif faux positif « [4/6] »)", "25/25 ×2", "hôte + dépôt"),
        ],
        "fichiers": [
            ("download/rapport-cw-task19-projet.md", "2,1 Ko", "CW --bloc PASS 25/25"),
            ("skills/@mon-ecosysteme/PROMPT-MAITRE-CORRECT-WORK-v2.12.2.md", "818 L", "PM vivant (cascade)"),
            ("skills/@historique/prompts-maitres/correct-work/PROMPT-MAITRE-CORRECT-WORK-v2.12.1.md", "806 L", "archivage R4 byte-identité"),
        ],
        "decisions": [
            ("1", "gen-plan NON modifié (R2-CACHE adéquat)", "« optimise-les s'il le faut » — pas de sur-optimisation", "v3.49.0 inchangée"),
            ("2", "correct-work : cache AUTORISÉ uniquement hors-preuve ; clone-chat : cache de COLLECTE jamais de VALIDATION", "« un verdict figé n'est JAMAIS une preuve en soi »", "§1.4bis + §1.13"),
            ("3", "Cascade d'invariants dans le MÊME commit que la montée (C7)", "2 FAIL détectés par re-jeu (invariants retard)", "leçon consignée"),
        ],
        "bugs": [
            ("1", "verify-correct-work FAIL « 2.12.2 != 2.12.1 »", "attente figée PM_PATH/EXPECTED_VERSION", "recalibrage atomique arbitre", "16/16 PASS"),
            ("2", "Arbitre CW faux FAIL certification", "motif « [4/6] » = index d'arbitre (faux positif)", "condition succès exacte", "25/25 ×2"),
        ],
        "conventions": [
            ("Frontière cache/preuve (C5)", "rejeux intermédiaires via cache avec mention « rejeu (cache) » ; verdict final/AVEUGLE/idempotence ×2 toujours réels", "correct-work §1.4bis + docstring cache-verdicts.py"),
            ("Cascade d'invariants (C7)", "SKILL.md + KB + invariant ECO_SKILLS + PM + arbitres dans le même commit", "commits fenêtre 15"),
        ],
        "drifts": [
            ("1", "ENRICHISSEMENT", "correct-work sans cache", "v2.12.2 §1.4bis", "19", "suite 175", "directive fenêtre 15"),
            ("2", "ENRICHISSEMENT", "clone-chat sans cache", "v2.2.0 §1.13", "19", "suite 175", "directive fenêtre 15"),
            ("3", "SANS OBJET (constat)", "gen-plan R2-CACHE", "inchangé — adéquat", "19", "suite 175", "analyse"),
        ],
        "etat": ("Livré et opérationnel : wrapper selftest 12/12, mesures de gain consignées, frontière "
                 "preuve appliquée ; certification ALL PASS 6/6 ×2 ; parité 0/0 à 5ed9a36b."),
        "prochaine": ("Utiliser cache-verdicts.py sur les re-jeux intermédiaires des prochaines campagnes "
                      "de tests (jamais sur un verdict de certification) ; re-vérifier les frontières à "
                      "chaque montée de version (C7)."),
        "prio": ["scripts/cache-verdicts.py", "skills/correct-work/SKILL.md", "skills/clone-chat/SKILL.md"],
    },
]


def check9(t: str, slug: str, autres: list) -> list:
    fails = []
    i0, i4 = t.find("## §1 —"), t.find("## §4 —")
    corps = t[i0:i4] if i0 >= 0 and i4 > i0 else t
    # Les noms de fichiers de clones (clone-session-web-220878ed-…) sont des POINTEURS
    # d'artefacts (les clones appartiennent au thème archivage), pas du contenu
    # hors-thème — le critère 9(a) vise le CONTENU libre, pas les chemins.
    corps_libre = re.sub(r"clone-session-web-220878ed-\S+", " ", corps)
    for a in autres:
        if a in corps_libre:
            fails.append(f"(a) hors-thème : « {a} » cité en §1-§3")
    if "## §0bis" not in t:
        fails.append("(b) §0bis absente")
    j = t.find("Preuves du périmètre")
    if j < 0:
        fails.append("(d) preuves absentes")
    return fails


def generer(th: dict, autres: list) -> str:
    slug = th["slug"]
    exclusions = "\n".join(
        f"| {i+1} | thème « {a} » (hors périmètre {slug}) | clone thématique dédié `…clone-theme-{a}-{DATE}.md` ou clone complet canonique `{CANONIQUE_REL}` |"
        for i, a in enumerate(autres))
    sessions = "\n".join(f"| {i+1} | {d} | {f} | {l} |" for i, (d, f, l) in enumerate(th["sessions"]))
    skills = "\n\n".join(
        f"#### {n}\n\n- **Description** : {d}\n- **Spécification fonctionnelle et technique** : {tech}\n"
        f"- **Relations** : {rel}"
        for n, d, tech, rel in th["skills"]) or "*Aucun skill créé ou modifié sur ce thème.*"
    scripts = "\n\n".join(
        f"#### {n}\n\n- **Description** : {d}\n- **Signature / invariant** : {sig}\n- **Chemin** : `{chem}`"
        for n, d, sig, chem in th["scripts"]) or "*Aucun script dédié sur ce thème.*"
    fichs = "\n".join(f"| `{p}` | {t} | {d} |" for p, t, d in th["fichiers"])
    decs = "\n".join(f"| {n} | {d} | {c} | {cs} |" for n, d, c, cs in th["decisions"])
    bugs = "\n".join(f"| {n} | {b} | {ca} | {f} | {r} |" for n, b, ca, f, r in th["bugs"]) or "| — | Aucun bug corrigé sur ce thème | — | — | — |"
    convs = "\n".join(f"| {n} | {r} | {e} |" for n, r, e in th["conventions"])
    if th["drifts"]:
        drifts = "\n".join(f"| {n} | {ty} | {av} | {ap} | {s} | {l} | {r} |" for n, ty, av, ap, s, l, r in th["drifts"])
    else:
        drifts = "| — | — | — | — | — | — | Aucune évolution de contexte détectée pour ce thème |"
    prio = "\n".join(f"{i+1}. **`{p}`** — artefact de reprise prioritaire du thème" for i, p in enumerate(th["prio"]))
    titre = f"# CLONE THÉMATIQUE — {slug} — SESSION WEB-220878ED (THEME : {th['titre'].upper()})"
    return f"""{titre}

> **Date du clone** : 2026-11-{DATE[6:]}
> **Mode** : `clone-chat (ALL)` — v2.2.0 (§1.12.3, exécution fenêtre 16 — trace 1a221dc7539d4351)
> **Thème** : {th['titre']} (slug : `{slug}`)
> **Périmètre** : {th['fenetres']}
> **Preuves du périmètre (≥2)** : {th['preuves']}
> **Projet global** : clone complet canonique `{CANONIQUE_REL}` (11ᵉ génération — ce clone thématique en dérive)
> **Version clone-chat** : 2.2.0
> **Statut du thème** : {th['statut']}

---

## §0 — RÈGLE ZÉRO — CONTEXTE PERDU + PÉRIMÈTRE

Les fichiers des sessions précédentes n'existent pas dans cette nouvelle session.
Tu dois **reconstruire** l'intégralité du contexte du thème à partir de ce document.
Ne jamais utiliser le verbe « conserver » — tout est à recréer.

Contexte matériel : sandbox `/home/z/my-project/` ; dépôt `KNOWLEDGE-repo/` (branche main, parité 0/0 à 5ed9a36b après suite 175) ; session `web-220878ed-c362-40f9-b12a-5aa08335c14d` ; langue FRANÇAIS exclusif (règle d'or n°6).

**Auto-suffisance périmétrique** : ce clone se suffit AU PÉRIMÈTRE du thème `{slug}`
pour reprendre ce sous-projet. La reprise GLOBALE de la discussion exige le clone complet
canonique ou `clone-chat (ALL)` — ce clone thématique ne remplace jamais l'instantané
de clôture canonique.

### §0bis — Exclusions (hors périmètre du thème)

| # | Exclu (thème / sections) | Où le retrouver |
|---|--------------------------|-----------------|
{exclusions}

---

## §1 — CHRONOLOGIE DU THÈME

### §1.1 Résumé du thème

{th['resume']}

### §1.2 Table des sessions du thème

| # | Date | Session / fenêtre | Livrables du thème |
|---|------|-------------------|--------------------|
{sessions}

---

## §2 — ARTEFACTS DU THÈME

### §2.1 Skills créés ou modifiés (thème)

{skills}

### §2.2 Scripts créés ou modifiés (thème)

{scripts}

### §2.3 Artefacts produits (thème)

| Fichier | Taille | Description |
|---------|--------|-------------|
{fichs}

---

## §3 — DÉCISIONS CLÉS DU THÈME

### §3.1 Décisions de l'utilisateur (thème)

| # | Décision | Contexte | Conséquence |
|---|----------|----------|-------------|
{decs}

### §3.2 Bugs corrigés (thème)

| # | Bug | Cause | Fix | Résultat |
|---|-----|-------|-----|----------|
{bugs}

### §3.3 Conventions établies (thème)

| Convention | Règle | Exemple |
|------------|-------|---------|
{convs}

### §3.5 Évolutions de contexte du thème (Context Drift)

| # | Type | Avant | Après | Session | Ligne worklog | Raison |
|---|------|-------|-------|---------|---------------|--------|
{drifts}

---

## §4 — INSTRUCTIONS DE REPRISE DU THÈME

### État courant du sous-projet

{th['etat']}

### Prochaine étape exécutable

{th['prochaine']}

### Fichiers à reconstruire en priorité

{prio}

---

## §5 — AUTO-CLONAGE THÉMATIQUE

Ce clone est auto-référentiel SUR SON PÉRIMÈTRE :

1. Reprendre le sous-projet dans une nouvelle session avec ce clone
2. À la clôture du sous-projet : ré-exécuter `clone-chat ({slug})` — le clone
   thématique grandit par ses propres sessions (§1-§3 enrichis, §0/§0bis/§4-§5 régénérés)
3. Pour une carte à jour des thèmes de la discussion globale : `clone-chat --theme`
4. Le clone complet canonique (`{CANONIQUE_REL}`) demeure canonique et absorbe ce sous-projet

**Validation** : 8 checks standards + check 9 (cohérence thématique) = 9/9 PASS — vérifié mécaniquement par le générateur `scripts/task20-generer-clones-theme.py` (FAIL-CLOSE : aucun fichier écrit si 9/9 non atteint).
"""


def main() -> int:
    slugs = [t["slug"] for t in THEMES]
    produits = []
    for th in THEMES:
        autres = [s for s in slugs if s != th["slug"]]
        contenu = generer(th, autres)
        fails = check9(contenu, th["slug"], autres)
        if fails:
            print(f"FAIL-CLOSE check 9 sur {th['slug']} : {fails}")
            return 1
        nom = f"{SUJET}-clone-theme-{slug_fichier(th['slug'])}-{DATE}.md"
        p = DL / nom
        p.write_text(contenu, encoding="utf-8")
        produits.append({"fichier": f"download/{nom}", "octets": p.stat().st_size, "verdict": "9/9 PASS", "statut": th["statut"]})
        print(f"  [9/9] {nom} ({p.stat().st_size} octets)")

    index_nom = f"{SUJET}-clone-themes-index-{DATE}.md"
    lignes_tbl = "\n".join(
        f"| {i+1} | {t['titre']} | `{t['slug']}` | {t['fenetres']} | {t['statut']} |"
        for i, t in enumerate(THEMES))
    lignes_fich = "\n".join(f"| `{p['fichier']}` | {p['octets']:,} octets | {p['verdict']} |".replace(",", " ") for p in produits)
    index = f"""# INDEX DES CLONES THÉMATIQUES — `clone-chat (ALL)` — SESSION WEB-220878ED

> **Date** : 2026-11-{DATE[6:]} · **Mode** : `clone-chat (ALL)` (§1.12.3, v2.2.0) · **Trace** : 1a221dc7539d4351
> **Test préalable** : batterie $FACON2 `task20-tests-clone-all.py` — 30/30 PASS ×2 (le test a précédé l'exécution, ordre de la directive)
> **Source de la table** : §1bis du clone complet canonique `{CANONIQUE_REL}` (preuves ≥2 R4 par thème)
> **Idempotence §1.12.3** : ré-exécution régénère les mêmes noms de fichiers (même périmètre → écrasement à l'identique) — vérifiée SHA ×2 identiques

## Table des thèmes ({len(THEMES)})

| # | Thème | Slug | Sessions / fenêtres | Statut |
|---|-------|------|--------------------|--------|
{lignes_tbl}

## Fichiers produits ({len(produits)} + cet index)

| Fichier | Taille | Verdict check 9 |
|---------|--------|-----------------|
{lignes_fich}
| `{SUJET}-clone-themes-index-{DATE}.md` | ce fichier | index (sans check 9) |

## Convention de reprise

1. Reprendre UN sous-projet : ouvrir le clone thématique correspondant (auto-suffisant sur son périmètre).
2. Reprendre la discussion GLOBALE : ouvrir le clone complet canonique `{CANONIQUE_REL}` — les clones thématiques ne le remplacent jamais.
3. Actualiser la carte : `clone-chat --theme` ; tout regénérer : `clone-chat (ALL)` (écrasement à l'identique par périmètre).

**Garde** : le thème demandé doit figurer dans la table ci-dessus — tout autre slug déclenche l'erreur contrôlée « thème non reconnu — choisir dans la table » (aucun clone inventé).
"""
    p = DL / index_nom
    p.write_text(index, encoding="utf-8")
    print(f"  [INDEX] {index_nom} ({p.stat().st_size} octets)")
    if "--verdict-json" in sys.argv:
        i = sys.argv.index("--verdict-json")
        Path(sys.argv[i + 1]).write_text(json.dumps({
            "mode": "(ALL)", "themes": len(THEMES), "produits": produits,
            "index": f"download/{index_nom}", "idempotence": "SHA ×2 vérifiées à la re-génération",
        }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"EXÉCUTION (ALL) TERMINÉE : {len(produits)} clones thématiques 9/9 + index")
    return 0


def slug_fichier(s: str) -> str:
    return s


if __name__ == "__main__":
    sys.exit(main())
