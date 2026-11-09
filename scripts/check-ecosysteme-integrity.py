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

"""Intégrité de l'écosystème Knowledge installé dans ce projet.

Recalibré Architecture v2.0 (corrige-ecosysteme, session B8) ; re-calibré B13-r5
(gen-plan v3.16.0, knowledge-observer 13e entrée, corpus 19 fichiers) ;
re-calibré B13-r6 (N25 : script-creator + script-reviewer au registre — ECO_SKILLS 15,
check 5, archive homologues v2.1 ; N27 : audit-provenance — ECO_SKILLS 16 ;
N28 : gen-plan v3.17.0 — PM v3.17.0 assemblé 1362 L, corpus 20 fichiers) ;
re-calibré 2026-10-02 (montée gen-plan v3.17.1 — propagation renommage
prompt-engineering : PM v3.17.1 assemblé, corpus 22 fichiers, SYNC_MAP 12) ;
re-calibré 2026-10-02 (fusion installateurs PM-INSTALL v1.1.0 — directive
source d'installation unique : INSTALL-ECOSYSTEME.md supprimé, miroir
skills/_prompts-maitres/ supprimé (exécution décision d'architecture v2.0),
corpus 21 fichiers, SYNC_MAP 11) ; le miroir
skills/_prompts-maitres/ est SUPPRIMÉ par décision d'architecture (KB §Décisions)
— sa vérification est remplacée par le round-trip de l'archive
download/mon-ecosysteme_archive.zip (véhicule d'intégrité v2.0) ;
re-calibré 2026-10-02 (montée gen-plan v3.17.2 — déclencheur verbatim
« intègre dans le plan d'actions » + correction E1 → PM-INSTALL v1.1.0 :
PM v3.17.2 assemblé, corpus 22 fichiers, SYNC_MAP 12) ;
re-calibré 2026-10-02 (directive « prompt ultra maître » — orchestrateur léger
généré idempotent : PROMPT-ULTRA-MAITRE-ORCHESTRATION.md ajouté au corpus via
scripts/gen-ultra-maitre.py — dérivation dynamique KO-L003, idempotence ×2
prouvée, corpus 23 fichiers, SYNC_MAP 13) ;
re-calibré 2026-10-02 (Task 14, déduplication — décision d'architecture v2.2 :
canal de fichiers download/ SUPPRIMÉ, les 14 fichiers corpus répliqués dans
download/ sont effacés, sync-download.py retiré — le check 3 devient la garde
anti-doublons : AUCUN fichier du corpus ne doit exister en copie dans download/
(l'archive d'intégrité v2.2 est l'unique voie de diffusion) ; corpus 24 fichiers
avec le clone -f, garde calibrée sur le listing réel du corpus) ;
re-calibré 2026-10-02 (Task 16, suggestions (a)/(b) — résorption F1/F2/F4 :
ECO_SKILLS 21 → 26 (5 skills famille inscrits au registre KB), CORPUS_ATTENDU
24 → 26 (PMs CORRECT-WORK v2.6.0/v2.7.0 matérialisés au corpus, méthode B1,
provenance tracée), check 5 « 26 entrées KB versionnées » ; reconstitué Task 17
session suivante — couche Task 16 récupérée via l'archive certifiée de la
discussion partagée, round-trip 26/26 byte-identique).

Vérifications (pipeline PM-INSTALL étapes 1-2, 8 — périmètre v1.3.0) :
  1. SHA-256 des fichiers du corpus canonique skills/@mon-ecosysteme/
  2. Round-trip byte-identité archive download/mon-ecosysteme_archive.zip ↔ corpus + piliers (v2.3)
  3. Garde anti-doublons download/ (décision v2.2 — 0 fichier du corpus en copie)
  4. Structure des 26 skills écosystème installés (21 + 5 skills famille Task 16)
  5. Cohérence versions SKILL.md ↔ registre KNOWLEDGE.md (26 entrées versionnées
     + section « Décisions d'architecture »)

Usage :
    python3 scripts/check-ecosysteme-integrity.py            # vérification + manifeste
    python3 scripts/check-ecosysteme-integrity.py --check    # vérification seule
"""

import hashlib
import json
import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS = os.path.join(BASE_DIR, "skills", "@mon-ecosysteme")
ARCHIVE = os.path.join(BASE_DIR, "download", "mon-ecosysteme_archive.zip")
DOWNLOAD = os.path.join(BASE_DIR, "download")
SKILLS = os.path.join(BASE_DIR, "skills")
KB = os.path.join(SKILLS, "KNOWLEDGE.md")
MANIFEST = os.path.join(BASE_DIR, "scripts", "ecosysteme-integrity.json")

ECO_SKILLS = {
    "gen-plan": "3.41.0",  # KO-L004 (session web-ecef7f80 2026-11-08 — Task 78/79 G1 : v3.41.0 règle de sondage borné ; précédent Task 77 G2 : v3.40.0 protocole d'émission parallèle ; précédent Task 72 G1 : v3.39.0 re-curation progressive disclosure R1 [9 blocs R4 vers references/, SKILL.md 104,0→29,95 Kio −71,2 %, CRITIQUE→INTERMÉDIAIRE] + directives complémentaires 1a1b7b297b7b4975 [skill re-curation par script] et 1a1b7fe1c7238e8d [fenêtre native AFFICHE-PLAN E7-DISP point 6], cascade PM v3.39.0/SHARED v1.7.34/PM-INSTALL v1.9.10) ; précédent KO-L004 (session web-c30e6506 2026-11-07 — v3.37.0 : déclencheur verbatim « met à jour » [re-génération $FACON d'un NOUVEAU plan d'actions $FACON2 consolidé — voie distincte de « intègre dans le plan d'actions » = extension E13 en place] + glossaire alias-eco INLINE $FACON/$FACON2 au §A [auto-contenu — la lecture du SKILL.md n'exige plus alias-eco], cascade PM v3.37.0/SHARED v1.7.30/PM-INSTALL v1.9.6) ; précédent KO-L004 (Task 56 G1, session web-c30e6506 2026-11-06 — garde É1-INSTALL étendue : contrôle dynamique SKILL.md de toutes les entrées KB + auto-réparation miroir local KNOWLEDGE-repo, verdict INSTALLE-REPARÉ, cascade PM v3.35.2/SHARED v1.7.25/PM-INSTALL v1.9.3) ; précédent KO-L004 (directive langue française 2026-11-06, session web-c30e6506 — renforcement règle d'or n°6 : français dès le PREMIER mot de toute session/reprise/continuation, §0 SHARED v1.7.24 propagation 116 skills + 150 scripts + 4 agents, cascade PM v3.35.1/PM-INSTALL v1.9.2) ; précédent KO-L004 (Task 52 règle d'or n°9 post-coupure, session web-c30e6506 2026-11-05 — vérification automatique installation écosystème, cascade PM v3.35.0/SHARED v1.7.23/PM-INSTALL v1.9.1) ; précédent KO-L004 (Task 49 règle d'or n°8, session web-c30e6506 2026-11-04 — PM INSTALL installe les skills, jamais les PMs, cascade PM v3.34.0/SHARED v1.7.22/PM-INSTALL v1.8.16) ; précédent KO-L004 (Task 47-b précision sémantique n°7, session web-6058b3ba 2026-11-04 — « ce que tu as oublié » = les éléments post-coupure partiellement reconstitués, cascade PM v3.33.1/SHARED v1.7.20/PM-INSTALL v1.8.14) ; précédent KO-L004 (Task 47, session web-6058b3ba 2026-11-04 — règle d'or n°7 mémoire complète de la discussion, cascade générateur PM v3.33.0/SHARED v1.7.19/PM-INSTALL v1.8.13) ; KO-L004 (session web-6058b3ba, 2026-11-02 — v3.32.0 parallélisation par défaut des tâches ET commandes + resorption divergence PM stale §1.7 #4, cascade PM v3.32.0) ; KO-L004 (session web-4f989063, 2026-11-01 — v3.31.0 complétion disciplines C1-C4, cascade PM v3.31.0) ; KO-L004 (session web-4f989063, 2026-10-31 — installation PATTERN KO-L009 §1.5, cascade générateur PM v3.30.0) ; KO-L004 (session web-4f989063, 2026-10-31 — règle d'or n°6 langue française, cascade générateur PM v3.29.0/SHARED v1.7.15/PM-INSTALL v1.8.9) ; KO-L004 (session web-eb6c8580, Task 7 2026-10-30 — directive propriétaire : recommandation E15 Task 6) : v3.28.1→v3.28.2 contingence « récupération externe bloquée ×3-4 » au §4 SKILL + grille-token.md (row 14) ; précédent (2026-10-30 — résorption réserves héritées P3-P7) : v3.26.0→v3.28.1 (v3.27.0 fusion lignée canonique+fork E7-DISP, web-dd290b0d ; v3.28.0 §A déclencheurs ; v3.28.1 recalibration E15 #token) ; précédent (web-f90062ce, 2026-10-24) : leçons vérité source PM INSTALL (dégradation gracieuse philosophie #4 + règle d'or n°5 anti-aspirant) ; précédent SG7.4 Task B2 : re-matérialisation structure hiérarchique ; précédent Task 26 : parallélisation par défaut
    "re-curation": "1.2.2",  # KO-L003 (2026-11-09, web-ecef7f80 — Task 82 G3, correctif sur preuves réelles knowledge-observer : tolérance des références INTER-SKILL dans pointeurs_valides [lookbehind — seuls les pointeurs LOCAUX exigent l'existence locale] ; selftest 14→15 cas 15/15 ×2 ; PATCH description inchangée — révélateur : conversion agent autonome v1.1.0 G2 a exposé le cas inter-skill jamais couvert) ; précédent KO-L003 (2026-11-09, web-ecef7f80 — Task 81 G2, correctif sur preuves réelles iphone19 : idempotence des verdicts POST [re-jeu sur baseline ancrée = non-régression ; réduction stricte au 1er POST] ; selftest 14/14 ×2 ; PATCH description inchangée) ; précédent KO-L004 (2026-11-09, web-ecef7f80 — Task 80 directive 1a1bcb98c022bfe9 : suite de tests v1.2.0 intégrée à protocole-test.py — F1 fonctionnels [selftests réels exécutés, timeout 60 s, rc+durée] · F2 performance [durées mesurées, perf_stable ×1,5+0,5 s] · F3 interactions [sortantes/entrantes semver, KB, ECO_SKILLS, PM si famille, agents, empreinte sha256] ; verdicts PRE/POST étendus [GO exige F1 PASS + F3 SAINES ; POST 5 dimensions] ; selftest 13/13 ×2 ; deux faux positifs résorbés sur preuves réelles [evals format liste ; NON-VERSIONNÉ plateforme] ; description ADDITIVE, non-régression triggers) ; précédent pendance Task 79 0b1712b (2026-11-09) : harnais v3 — correctif comparateur §0 [borne bloc socle + dates de directives normalisées], selftest 7/7 ×2 ; précédent Task 72 G4 (2026-11-08, web-ecef7f80) : création — skill IMPLÉMENTÉ du script protocole-test.py (directive complémentaire 1a1b7b297b7b4975 : tests AVANT re-curation [PRE GO/NO-GO], maintien de l'optimisation [POST cohérent/fonctionnel/optimisé], --compare méthodes R4)
    "knowledge-observer": "1.1.0",  # KO-L004 (Task 82 G2, session web-ecef7f80 2026-11-09 — conversion cibles-to-agent P1 : agent autonome tandem, knowledge-observer.agent créé [format .agent : mémoire 2 niveaux + pipeline A-H + sécurité], SKILL.md v1.1.0 §1.6 ajouts purs) ; précédent 1.0.0 (N20 2026-09-19 matérialisation Task Observer)
    "ghorg-cmdr": "1.1.0",  # Task 51 (D3 — skill famille intégration ghorg/cmdr, session web-c30e6506 2026-11-04 ; reconstruction post-coupure n°3 Task 53)
    "correct-work": "2.11.0",  # KO-L004 (Task 60 G4, session web-c30e6506 2026-11-07 — D605 : v2.9.0→v2.11.0 double apport — contrat §1.5bis correctifs mode STEP ré-intégré [v2.10.0 perdue au recyclage, reconstituée plan-task59 D591] + matrice best-of §12 ; plancher gen-plan élevé >=3.22.0 ; arbitre recalibré checks 11/15) ; précédent KO-L004 (Task 48, session web-6058b3ba 2026-11-04 : v2.9.0 mode --bloc)
    "clone-chat": "2.0.2",
    "skills-inventory": "1.1.0",
    "skill-creator": "1.1.0",
    "agent-creator": "2.3.0",  # Task 22 (2026-10-23) : DÉRIVE CRITIQUE résorbée — SKILL.md re-écrit comme VRAIE fabrique d'agents (workflow F1-F5), .agent ré-écrit (capacites A2A), read_when réparé
    "script-creator": "1.1.0",
    "script-reviewer": "1.0.0",
    "audit-provenance": "1.1.0",
    "prompt-engineering": "2.3.1",
    "context-engineering": "1.2.1",
    "loop-engineering": "1.2.1",
    "graph-engineering": "1.1.1",
    "harness-engineering": "1.2.1",
    "script-mon-ecosysteme-infrastructure": "1.1.0",
    "audio-metadata": "1.1.0",
    "cpp-analysis": "1.1.0",
    "pdf-llm": "1.0.0",
    "resource-monitor": "1.1.1",
    "version-management": "1.3.0",  # re-curation Task 79 G2 (2026-11-08) : 46,1→25,2 Kio, 7 blocs R4 references/ — version inchangée (contrats intacts)
    "skill-finder-cn": "1.0.0",  # Task 23 : fallback §1.16 inscrit au registre
    # Skills famille (Task 16, suggestion (a) — inscription au registre, résorption F1)
    "autonomous-agent": "1.2.1",
    "correct-py": "1.1.0",
    "fleet-engineering": "1.1.1",  # KO-L004 (session web-b4d7dd19, 2026-10-11) : read_when + dependencies gen-plan — bump PATCH cascade n°54
    "memory-engineering": "1.2.1",  # KO-L004 (session web-b4d7dd19, 2026-10-11) : read_when + dependencies gen-plan — bump PATCH cascade n°54 (Task 18 : Description Optimization conservée)
    "spec-driven-development": "1.1.1",
    "refactoring-engineering": "1.1.1",  # n°55 — Task 9 (2026-10-12) : Description Optimization A2 (dérive voie M résorbée, re-mesure 7/7) ; Task 8 : seule discipline de refactoring, outil refactoring-test ; Task 12 : recalibrage doc (§5 baseline MESURÉE 7/7, plancher ref-test >=1.0.1)
    "refactor-guard": "1.8.1",
    "alias-eco": "1.3.0",  # KO-L004 Task 25bis/25ter (2026-10-23) : Description Optimization v1.1.0 + grammaire B --trigger v1.2.0 ; créé Task 18 (registre d'alias $<ALIAS> — délégation correct-work mode PROJET),  # Task 8 (fusion discussion 468a4c26) : garde-fous de refactoring — lignée externe v1.7.0, base hôte v1.2.0 portée,  # Task 32 (2026-11-01) : MINOR v1.3.0 — alias $FACON2 + exemples d'usage par commande (SKILL.md §2.4)
    "cahier-des-charges": "2.0.2",  # KO-L004 (session web-eb6c8580, 2026-10-30 — résorption réserve S3, tâche 5) : v2.0.1→v2.0.2 (élargissement description en M4 — rejeu voie M 12/12, cas [9] voie-m) ; précédent (même session, P3-P7) : v1.0.0→v2.0.1 (v2.0.0 web-dd290b0d 2026-10-25 : extension cycle System Engineering complet ; v2.0.1 : reconnaissance discipline Engineering Design — tags discipline/engineering, description au canon, synchronisation différée R3 résorbée) ; précédent (SG7.4 Task B2, web-f90062ce, 2026-10-24) : entrée KB restaurée — forme publiée e9a68a1 sans entrée KB (trou de synchronisation analyse B2 résorbé) ; créé v1.0.0 directive propriétaire 2026-10-23
    "agent-prompt-engineering": "1.0.1",  # KO-L004 (SG7.4 Task B2, session web-f90062ce, 2026-10-24) : entrée KB créée — forme au dépôt depuis e9a68a1 sans entrée KB (trou de synchronisation analyse B2 résorbé) ; matérialisé 2026-09-06
    "fullstack-dev": "1.0.0",  # Task 8 (fusion discussion 468a4c26 Task 27 externe) : inscrit au registre — précédent vue-upload
    "refactoring-test": "1.1.1",  # Task 8 (session web-b4d7dd19, 2026-10-12) : OUTIL de la discipline n°55 (non discipline — correction directive propriétaire) ; Task 12 : §5 baseline MESURÉE 7/7
    "vue-upload": "1.5.0",  # KO-L004 (Task 8, session web-eb6c8580, 2026-10-31 — directive « crée $facon ces trois skills », D018-1) : v1.4.0→v1.5.0 hygiène des versions (versions, push archivage automatique download/archive/, section repliée) ; précédent (Task 7 G0, 2026-10-30) : v1.3.0→v1.4.0 épinglage livrable courant + journal des téléchargements ; précédent (web-b93f42fa, 2026-10-09) : KB=registre fait foi — occurrence L004 résorbée, arbitre dynamisé
    "livraison-garantie": "1.1.0",  # Option A (2026-10-31, session web-4f989063 — directive propriétaire « continue en effectuant l'option «A» ») : bump v1.1.0 MINOR — marqueur veto-exclusif canon Task 30 « portail → vue-upload » sur le cas négatif du corpus trigger_evals (recommandation D006 plan-task3 ; rejeu 105/105, non-resorbe 0) ; Task 8 (session web-eb6c8580, 2026-10-31 — directive « crée $facon ces trois skills », D018-2) : création via skill-creator — orchestrateur de livraison en boucle fermée (épinglage avant fenêtre, surveillance journal, verdicts CONFIRME/PARTIEL/AUCUN) ; dépendance vue-upload >= 1.5.0 (douleur prouvée du 2026-10-25 : livraison manuelle en 4 tours)
    "dessin-technique": "1.3.0",  # Task 58 (session web-c30e6506, 2026-11-07) : bump v1.3.0 — nœud C++ trigo-euler reconstruit (contrat registre inter-scripts v1.0.0, selftest 15/15 ×2, preuves daemon PASS 8/8 ×2) ; précédent : v1.1.1 Task 12 (2026-10-18, ACF latitude + garde anti-fallacieux + trou-ness) ; v1.1.0 Task 10 (F4 filetage + F5 profondeur) ; v1.0.0 création VOSS-C 2026-10-13
    "iphone18": "1.1.0",  # Task 48 (session web-38713acd) : bump v1.1.0 extension 1944 (chemin argentique N&B années 1930-1950) ; création v1.0.0 Task 45 (R18 ouverture variable, PA-TEST-001 QC 12/12)
    "iphone19": "0.12.0",  # KO-L004 (2026-11-09, web-ecef7f80 — Task 81 directive 1a1bcf4fecbf5f29 « règle fidélité » : bump v0.12.0 — règle absolue 15 [ne jamais inventer et rester fidèle à l'image d'origine : visage, vêtement, arrière-plan, etc. — sauf demande explicite de modifications] + critère QC 14, ajouts purs [règles absolues 1-14 · R1-R19 · G1-G7 · QC 1-13 intacts] ; PM @photos v0.12.0 + archive v0.11.0 scellée @historique/photos/ + projection VERBATIM + description ADDITIVE) ; précédent Task 48 (session web-38713acd) : bump v0.11.0 extension 1944 (chemin argentique N&B années 1930-1950) ; v0.10.0 pixel binning R19 (frandroid 27/03/2026) ; création v0.9.0 Task 47 (migration ANTICIPÉE)
    "iphone17": "1.1.0",  # Task 48 (session web-38713acd) : bump v1.1.0 extension 1944 (chemin argentique N&B années 1930-1950) ; création v1.0.0 Task 45 (R1-R17 d'époque, PM v2.0 scellé @historique/photos/)  # Task 12 (2026-10-18) : bump PATCH v1.1.1 — corrections findings Task 11 (ACF par latitude + garde anti-fallacieux + trou-ness) ; Task 10 : bump v1.1.0 — F4 filetage + F5 profondeur, evals T5/T6 (recalibrage KO-L004 ; création Task 8 2026-10-17, réinscription post-wipes)
    "traduction-zh-fr": "1.3.1",  # KO-L004 (recalibrage croisé, session web-4f989063 2026-11-01, directive installation écosystème) : entrée KB créée v1.0.0 (3965f6b) puis bumpée v1.1.0 (8fa153a) et v1.2.0 (eb4be64) sans recalibrage de l'arbitre — dérive résorbée (41e entrée versionnée) ; v1.2.0 = glossaire FR + TMX 1.4b + axes --src/--dest (E13 n°5) ; v1.3.1 = recalibrage triggers F-2 (correct-work Task 28, GO 2026-11-01)
    "tsi-architect": "1.2.1",  # KO-L004 (Task 67 G4, session web-c30e6506 2026-11-07 — résorption F-67-2 directive bloc n°3 : dependencies += tsi-validator/multi-shift-architect/midi-doc-expert [relations §4 déclarées, alignement frontmatter↔KB]) ; Task 46 (session web-6058b3ba 2026-11-04 — reconstitution §3bis catalogue & MIDI Controls + pattern délégation par deck, DJTT = exemple)  # Task 31 (inscription au dépôt, directive GO (a) trace 1a1975c9a4c7fa31, session web-4f989063 2026-11-01) : skill hôte-seul inscrit — lignage honnête Task 27, 44e entrée versionnée ; Task 33 (GO initial P2 MK3→MK2, trace 1a197aaf0eb6557d, session web-4f989063 2026-11-02) : recalibrage croisé v1.1.0 (conversion périmètre MK2, copie host→repo byte-identique)
    "tsi-validator": "1.3.1",  # KO-L004 (Task 67 G4, session web-c30e6506 2026-11-07 — résorption F-67-2 directive bloc n°3 : dependencies += tsi-architect/midi-doc-expert/multi-shift-architect) ; Task 55 (session web-c30e6506 2026-11-06 — GO exécution plan STEP, suggestions F1/F2 rapport Task 51 §6.7, décision propriétaire Task 54 item 6) : v1.2.0→v1.3.0 F1 verdict PRÉFÉRENCES (exit 2, JSON PREFERENCES) + F2 multi-devices E3 (itération DEVI, stats.devices, erreurs qualifiées « device i : »), exit codes 0/1/2/3 ; Task 31 (même directive) : arbitre mécanique tandem TSI, 45e entrée ; Task 33 : recalibrage croisé v1.1.0 (conversion MK2 + constat interopérabilité E1 NIXML consigné, format réel couvert par analyse-doc-s4mk2) ; Task 34 suite (directive GO trace 1a198688435d6bf1, session web-4f989063 2026-11-02) : évolution BI-RACINE NISYSTEM+NIXML v1.1.0→v1.2.0 (pendante Task 33 n°1 résorbée, preuves mécaniques ×4) ; Task 36 (reprise E1-RES post-compression, 2026-11-02) : recalibrage KO-L004 de l'arbitre (5 FAIL intégralement qualifiés évolutions légitimes, 0 régression)
    "midi-doc-expert": "1.2.1",  # KO-L004 (Task 67 G4, session web-c30e6506 2026-11-07 — résorption F-67-2 directive bloc n°3 : dependencies += tsi-architect/tsi-validator) ; installation profil local 2026-11-04 (session web-6058b3ba — Task 45 : §5 rédigé par mode + §2 bridge MIDI Controls 2 étages IDs 850-873, forme installée fait foi — R2, PM-INSTALL §3.2, précédent fcd377e) ; Task 31 (même directive) : génération documentation MIDI, 46e entrée ; Task 33 : recalibrage croisé v1.1.0 (conversion MK2)
    "orchestrateur-tsi": "1.1.2",  # KO-L004 (Task 67 G4, session web-c30e6506 2026-11-07 — résorption F-67-2 directive bloc n°3 : dependencies += 5 membres famille TSI [relations §3 « Orchestré » déclarées]) ; Task 32 (directive propriétaire trace 1a1977ef5718a28d, session web-4f989063 2026-11-01) : orchestrateur domaine TSI/Traktor (méta maître, tandem skill+agent), 47e entrée ; Task 33 : recalibrage croisé v1.1.0 (agent renommé agent-TSI.agent, nouveau membre analyse-doc-s4mk2, conversion MK2) ; Task 57 : v1.1.1 §2.2bis sémantique verdicts & agrégation pire-des-membres (résorption S4 correct-work --bloc Task 55)
    "multi-shift-architect": "1.1.0",  # Task 33 (GO initial P4 — cascade KB/pins/cascade/self-healing, trace 1a197aaf0eb6557d, session web-4f989063 2026-11-02) : skill hôte-seul inscrit — lignage honnête, 48e entrée versionnée (méthode des couches SHIFT, règle E7, conversion MK2)
    "analyse-doc-s4mk2": "1.3.2",  # Task 66 (F-65-1 implémenté : calibration ZIP interne non muet — analyser-zip-mk2 v1.2.1 + run_all v1.2.1 + SKILL.md v1.3.2, batterie $FACON2 16/16 ×2 idempotent sur l'échantillon re-téléversé avec ZIP imbriqué)  # Task 61 G3 (F-V2-1 résorbé : fix TF-00 tests/run_all.py tuple->lambda, branche « ZIP introuvable » rendait TypeError au lieu du verdict propre — échantillon DJTT perdu du disque a révélé la branche jamais exercée, v1.3.1)  # KO-L004 (Task 46, session web-6058b3ba 2026-11-04 — reconstitution §4bis blob DeviceIO, v1.3.0 d origine perdue au recyclage, R2 forme installée fait foi)  # Task 33 (GO initial + directives « avant gen-plan » : skill famille TSI + tests $FACON2 + orchestration agent-TSI, trace 1a197aaf0eb6557d, session web-4f989063 2026-11-02) : création Task 33, inscription dépôt byte-identique, 49e entrée versionnée (batterie $FACON2 11/11, table P1b 22/22) ; Task 34 (GO traces 1a198688435d6bf1→1a198840319c3ec5) : v1.1.0 adaptatif aux types (règle d'or, PDF stdlib, signatures magiques) ; Task 35 (directives propriétaire traces 1a1989725d74c901 + 1a1989862dd46e61) : v1.2.0 cohérence croisée TSI↔non-TSI ; Task 36 (reprise E1-RES post-compression, 2026-11-02) : recalibrage KO-L004 de l'arbitre (évolutions légitimes qualifiées)
    # Task 55 (2026-11-06, session web-c30e6506 — GO exécution plan STEP ; observation P3
    # Task 52, décision propriétaire Task 54 item 7) : inscription des 4 skills restés
    # hors registre — 52 entrées versionnées.
    "inter-scripts": "1.0.0",  # création 2026-10-23 (mission TRIGO-INTER-SCRIPTS, Task ID 10, session web-da654199) ; dépôt depuis e9a68a1 ; arêtes bidirectionnelles graph-engineering/fleet-engineering/dessin-technique/script-creator inscrites Task 55
    "resume-youtube": "1.1.0",  # création 2026-10-04 (Task 26 via gen-plan v3.19.0, commit 48f71c4) ; v1.1.0 anti-hallucination G1-G5 (exigence propriétaire)
    "web-reader": "1.0.0",  # skill plateforme z-ai-web-dev-sdk (license MIT) — dépôt depuis 78f8b2c (2026-08-09)
    "web-search": "1.0.0",  # skill plateforme z-ai-web-dev-sdk (license MIT) — dépôt depuis 78f8b2c (2026-08-09)
    # Task 60 G3-SG2 (2026-11-07, session web-c30e6506 — porte propriétaire D604
    # VALIDÉE : « je valide ta proposition, tu peux l'exécuter $FACON pour me
    # générer $FACON un écosystème $FACON2 ») : création — portabilité universelle
    # (PM éphémères auto-portants depuis les SKILL.md vivants, usage IA externe ;
    # couche ADDITIVE, corpus intact — KO-L004 continue pour les 4 familles).
    "pm-skill": "1.0.2",  # KO-L004 (Task 67 G4, session web-c30e6506 2026-11-07 — résorption F-67-2 directive bloc n°3 : dependencies += vue-upload [livraison PM éphémère, direction sémantique corrigée]) ; Task 61 G3 (F2 résorbé : dependencies += correct-work — certification post-intégration, v1.0.1)
}
# Convention KB_ONLY_VERSION levée (corrige-ecosysteme G-bis) : skill-creator
# porte désormais sa version dans le frontmatter (v1.0.0) comme les autres.
KB_ONLY_VERSION = set()
METIER_SKILLS = []  # P-H (2026-10-02) : les ex-métier sont versionnés et au registre — check 4bis vidé
# Recalibrage F5 (Task 8, session web-43f5b4bd, 2026-10-17) : archive v2.3 étendue aux
# piliers — l'archive embarque, sous le préfixe piliers/, les 6 fichiers critiques du
# profil (2 SKILL.md familles PM, registre KB, orchestrateur de certification, arbitre
# d'intégrité, réinstallateur) afin que la restauration autonome couvre suppression ET
# corruption sur ce périmètre ; le round-trip vérifie leur byte-identité (compatibilité
# ascendante : une archive v2.2 sans entrées piliers/ reste conforme, n_pil_ko = 0).
PILIERS_ARCHIVE = {
    "piliers/skills/gen-plan/SKILL.md": os.path.join(SKILLS, "gen-plan", "SKILL.md"),
    "piliers/skills/correct-work/SKILL.md": os.path.join(SKILLS, "correct-work", "SKILL.md"),
    "piliers/skills/KNOWLEDGE.md": KB,
    "piliers/scripts/certification-complete.py": os.path.join(BASE_DIR, "scripts", "certification-complete.py"),
    "piliers/scripts/check-ecosysteme-integrity.py": os.path.join(BASE_DIR, "scripts", "check-ecosysteme-integrity.py"),
    "piliers/scripts/install-ecosysteme-local.sh": os.path.join(BASE_DIR, "scripts", "install-ecosysteme-local.sh"),
}
# [N14-c] SYNC_MAP — HISTORIQUE : bloc supprimé Task 14 (décision v2.2, déduplication) —
# le canal de fichiers download/ n'existe plus ; le check 3 applique la garde
# anti-doublons sur le listing RÉEL du corpus (dérivation dynamique — KO-L003).
# CORPUS_ATTENDU — invariant canonique du corpus (dérivation L003) [N28]
# Recalibrage L004 (Task 56) : 20 → 21 — ajout clone -f (directive utilisateur
# « push le clone dans @mon-ecosysteme/ » ; miroir + archive alignés).
# Recalibrage L004 (Task 16, suggestion (b)) : 24 → 26 — PMs CORRECT-WORK
# v2.6.0/v2.7.0 matérialisés au corpus (méthode B1, provenance tracée).
# Recalibrage L004 (session web-b93f42fa, 2026-10-09) : 26 → 28 — corpus réel certifié
# (28 fichiers à HEAD 3eebe65 ; PMs GEN-PLAN v3.19.0/v3.20.0 recréés,
# KB Tasks 39-40) — arbitre dynamisé, jamais la réalité (KO-L003).
# Recalibrage Task 15 (session web-b93f42fa, 2026-10-10) : 28 → 27 — suppression
# propriétaire d72226a (clone-discussion-2026-09-27-…-b13-r7-f.md, UI web) —
# corpus réel certifié 27 fichiers, re-scellement archive aligné (F2 retrait
# sanctionné D002, plan-task15-decisions-restantes.md).
# Recalibrage Task 16 (session web-b93f42fa, 2026-10-11) : 27 → 8 — déduplication
# des PMs (directive propriétaire « ne garder que la dernière version ») : 19 PMs
# historiques déplacés git mv vers skills/@historique/prompts-maitres/ (byte-identité
# SHA-256 scellée contre blobs b36f177, dossier @historique/) — corpus = 3 PMs
# sources (GEN-PLAN v3.21.0, CORRECT-WORK v2.7.0, CLONE-CHAT v2.0.0) + socle
# (SHARED, INSTALL, ULTRA, README, SYNC-CONTEXT), re-scellement archive aligné (F2).
# Recalibrage Task 9 (session web-b4d7dd19, 2026-10-12) : 8 → 9 — PM REFACTOR-GUARD
# v1.7.0 au corpus (décision D009 — 4e famille, bootstrap canonique).
CORPUS_ATTENDU = 9

results = []


def check(name, passed, detail=""):
    results.append((name, bool(passed), detail))
    print(f"  [{'PASS' if passed else 'FAIL'}] {name}{(' — ' + detail) if detail else ''}")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    write_manifest = "--check" not in sys.argv
    manifest = {"corpus": {}, "archive": {}, "download": {}, "skills": {}}

    print("=== 1. Corpus canonique @mon-ecosysteme (SHA-256) ===")
    corpus_files = sorted(os.listdir(CORPUS)) if os.path.isdir(CORPUS) else []
    check(f"{CORPUS_ATTENDU} fichiers présents (Architecture v2.0 — N27, recalibré Task 16 b36f177: dédup PMs → @historique)", len(corpus_files) == CORPUS_ATTENDU,
          f"{len(corpus_files)} fichiers")
    for fname in corpus_files:
        digest = sha256(os.path.join(CORPUS, fname))
        manifest["corpus"][fname] = digest

    print("\n=== 2. Archive round-trip (véhicule d'intégrité v2.3 — corpus + piliers) ===")
    ok, n_ident, n_homologues, n_pil, n_pil_ko = os.path.isfile(ARCHIVE), 0, 0, 0, 0
    if ok:
        import zipfile
        with zipfile.ZipFile(ARCHIVE) as z:
            znames = [n for n in z.namelist() if not n.endswith("/")]
            for n in znames:
                if n in PILIERS_ARCHIVE:
                    # F5 (Task 8, 2026-10-17) : piliers scellés — byte-identité exigée
                    cp = PILIERS_ARCHIVE[n]
                    if os.path.isfile(cp) and hashlib.sha256(z.read(n)).hexdigest() == sha256(cp):
                        manifest["archive"][n] = sha256(cp)
                        n_pil += 1
                    else:
                        n_pil_ko += 1
                    continue
                rel = n.split("@mon-ecosysteme/")[-1] if "@mon-ecosysteme/" in n else n
                cp = os.path.join(CORPUS, rel)
                if os.path.isfile(cp) and hashlib.sha256(z.read(n)).hexdigest() == sha256(cp):
                    manifest["archive"][rel] = sha256(cp)
                    n_ident += 1
                elif rel.startswith("homologues/"):
                    n_homologues += 1
            # v2.1 (N26, recalibrage L004) : corpus ⊆ archive byte-identique +
            # extras uniquement sous homologues/ (famille créateur/relecture).
            # v2.3 (F5, Task 8) : + piliers scellés vérifiés byte-identiques.
            extras = [n for n in znames
                      if n not in PILIERS_ARCHIVE
                      and (n.split("@mon-ecosysteme/")[-1]
                           if "@mon-ecosysteme/" in n else n) not in corpus_files]
            ok = (n_ident == len(corpus_files)
                  and n_pil_ko == 0
                  and all(e.startswith("homologues/") for e in extras)
                  and n_ident + n_pil + n_pil_ko + len(extras) == len(znames))
    check("Archive byte-identique au corpus + piliers (v2.3)", ok,
          f"corpus {n_ident}/{len(corpus_files)} · piliers {n_pil}/{len(PILIERS_ARCHIVE)} ({n_pil_ko} divergents) · {n_homologues} homologues")

    print("\n=== 3. Garde anti-doublons download/ (décision v2.2) ===")
    n_dup = 0
    for fname in sorted(corpus_files):
        d = os.path.join(DOWNLOAD, fname)
        if os.path.isfile(d):
            # Calibration Task 18 (2026-10-23, KO-L003) : détection par CONTENU —
            # un homonyme de contenu différent (ex. README.md du canal plateforme
            # hôte) n'est PAS une copie du corpus ; seule la copie byte-identique
            # (ou quasi) est un doublon sanctionné (décision v2.2).
            if sha256(d) == sha256(os.path.join(CORPUS, fname)):
                n_dup += 1
                check(f"doublon {fname}", False,
                      "copie du corpus dans download/ — à supprimer (déduplication v2.2)")
            else:
                print(f"  [NOTE] {fname} : homonyme de contenu différent dans download/ (canal partagé) — non compté")
    if n_dup == 0:
        check(f"download/ sans doublon du corpus ({len(corpus_files)} fichiers corpus absents)", True)
    if os.path.isfile(ARCHIVE):
        manifest["download"]["mon-ecosysteme_archive.zip"] = sha256(ARCHIVE)

    print("\n=== 4. Skills écosystème installés ===")
    for skill, expected_ver in ECO_SKILLS.items():
        sp = os.path.join(SKILLS, skill, "SKILL.md")
        if not os.path.isfile(sp):
            check(f"{skill}", False, "SKILL.md manquant")
            continue
        with open(sp, encoding="utf-8") as f:
            content = f.read()
        m = re.search(r"^version:\s*[\"']?([\d.]+)", content, re.MULTILINE)
        ver = m.group(1) if m else None
        manifest["skills"][skill] = {"version": ver or "KB", "sha256": sha256(sp)}
        check(f"{skill} v{ver}", ver == expected_ver, f"attendu v{expected_ver}")

    print("\n=== 4bis. Skills métier installés ===")
    for skill in METIER_SKILLS:
        sp = os.path.join(SKILLS, skill, "SKILL.md")
        check(f"{skill}", os.path.isfile(sp))

    print("\n=== 5. Cohérence registre KNOWLEDGE.md ===")
    if os.path.isfile(KB):
        with open(KB, encoding="utf-8") as f:
            kb = f.read()
        entries = re.findall(r"^## ([\w-]+) v([\d.]+)", kb, re.MULTILINE)
        has_decisions = "## Décisions d'architecture" in kb
        # Dynamisé KO-L004 (Task 23) : l'attendu = len(ECO_SKILLS), jamais un chiffre figé
        check(f"{len(ECO_SKILLS)} entrées KB versionnées + Décisions d'architecture",
              len(entries) == len(ECO_SKILLS) and has_decisions,
              f"{len(entries)} entrées versionnées (attendu {len(ECO_SKILLS)}), Décisions={'oui' if has_decisions else 'non'}")
        for skill, expected_ver in ECO_SKILLS.items():
            match = [e for e in entries if e[0] == skill]
            check(f"KB {skill}", bool(match) and match[0][1] == expected_ver,
                  f"KB={match[0][1] if match else 'absent'} / attendu={expected_ver}")
    else:
        check("Registre KB", False, "KNOWLEDGE.md manquant")

    n_pass = sum(1 for _, p, _ in results if p)
    n_fail = len(results) - n_pass
    print(f"\n=== RESUME : {n_pass}/{len(results)} PASS, {n_fail} FAIL ===")

    if write_manifest and n_fail == 0:
        with open(MANIFEST, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False, sort_keys=True)
        print(f"Manifeste écrit : {MANIFEST}")
    elif write_manifest:
        print("Manifeste NON écrit (échecs détectés)")

    sys.exit(1 if n_fail else 0)


if __name__ == "__main__":
    main()
