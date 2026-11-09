# Plan Task 1 — Installation de l'écosystème personnel + certification + plan d'actions audit (couplage correct-work §1.5)

> **Session** : web-eb6c8580 · 2026-10-25 · **Directive propriétaire** : « installe mon écosystème personnel en tant que mon écosystème personnel sur mon profil local grâce à mon fichier PROMPT-MAITRE-INSTALL-ECOSYSTEME.md (dépôt @ b75a620) et, lorsque l'installation sera terminée, prend en compte mon skill gen-plan fraîchement installé pour générer le plan d'actions de la tâche : "fais un audit complet de mon écosystème (inclus dedans un test pour comprendre le bug GEN-PLAN oublie de générer les plans d'actions depuis v3.24.0)" »
> **Hook E1-RES** : lecture préalable worklog (session vierge — profil local neuf) · garde É1-INSTALL exécutée en préemption (gen-plan §1.16) : ensure-installed.py --check → rc=0, verdict INSTALLE, 33 entrées KB · fraîcheur plan ✓ (première directive → plan neuf)
> **Type (E3)** : Type 2 — installation/vérification écosystème (correct-work §10.6 « Écosystème skills ») · **Profil (E6)** : NORMAL (aucun signal de pression — resource-monitor OK)
> **gen-plan** : v3.23.1 fraîchement installée (frontmatter = source de vérité) — couplage correct-work §1.5 Étape 1 : le présent plan EST le plan de vérification exigé par le Mode PROJET (jamais de plan autonome)

## Answer Key (E1 — hook obligatoire)

| ID | Décision | Vérification exécutable | Source | Priorité | Statut |
|----|----------|------------------------|--------|----------|--------|
| D001 | Source d'installation UNIQUE = dépôt GitHub bigleon2/KNOWLEDGE @ b75a62066791a8cce8c1ec5d1dbe7d976bae4244 (règle d'or n°4 : récupération par téléchargement intégral de l'arborescence — jamais lecture distante API/raw pour l'installation matérielle) | commit b75a620 vérifié (tarball 45 Mo, extraction .staging/) | directive propriétaire + PM-INSTALL §1 | S1 | PASS |
| D002 | Pipeline = PROMPT-MAITRE-INSTALL-ECOSYSTEME.md **v1.7.1** (11 étapes), profil **COMPLET** (défaut — toutes les entrées du registre KB, 4 familles D009 incluses) | PM lu intégralement (249 L) : §2 table 11 étapes, §2bis, §2ter, §A | PM-INSTALL §2 | S1 | PASS |
| D003 | Racine d'installation = `/home/z/my-project` (profil local) — `{{SKILLS_ROOT}}=skills/`, chemins relatifs portables (convention L008) ; arbitres dérivés de `__file__` | ensure-installed.py --check → root_present=true, rc=0 | SHARED §1.1 | S1 | PASS |
| D004 | Formes installées = état certifié du dépôt, **version-matched aux PMs les plus récents du corpus** (gen-plan v3.23.1, correct-work v2.7.0, clone-chat v2.0.1, refactor-guard v1.7.0) — assemblage §3.2, garde R2 : aucune rétrogradation | check-ecosysteme-integrity.py : 33/33 skills aux versions attendues | PM-INSTALL §3.2 | S1 | PASS |
| D005 | Incident archive (règle d'or n°1 §3.4) : `download/mon-ecosysteme_archive.zip` gitignorée (absente du dépôt) → rescellage **v2.3** via task-f5-seal-archive-v23.py (portable L008) : 9 corpus + 6 piliers = 15 entrées, round-trip byte-identité vérifié | sortie scelleur : « Archive v2.3 scellée » + check intégrité check 2 PASS | .gitignore `*.zip` + §2ter | S2 | PASS |
| D006 | Incident doublon : placeholder plateforme `download/README.md` en collision nominale avec le fichier corpus `README.md` (garde anti-doublons v2.2) → suppression du placeholder (l'état canonique de l'auteur n'a pas de README dans download/) | check-ecosysteme-integrity.py check 3 : 70/70 PASS | décision v2.2 Task 14 | S3 | PASS |
| D007 | Skills plateforme alias-eco & cahier-des-charges (état ultérieur : en-têtes §0 SHARED v1.7.10/v1.7.8) absents du dépôt b75a620 → marqueurs §0 alignés sur v1.7.7 (extrait Contexte Système byte-identique au corpus installé) — correction S3 journalisée ; finding conservé pour l'audit (divergence de lignée post-b75a620) | test-coherence-interactions.py check 11c : plus aucun STALE | arbitre Task 21 P4 | S3 | PASS |
| D008 | Rapports download/ de l'auteur NON importés (livrables de session, pas composants d'écosystème) ; rapport correct-work Mode PROJET de CETTE session généré à E13 ; skills plateforme hors ECO_SKILLS conservés en l'état (hors périmètre certifiable) ; worklog local neuf ; scaffolding web-app (src/, prisma/, .github/) non installé | diff arborescence vs dépôt : périmètre = corpus + @historique + 33 ECO + scripts + archive | verify-cross.py (commentaire périmètre) | S3 | PASS |
| D009 | Le bug rapporté « GEN-PLAN oublie de générer les plans d'actions depuis v3.24.0 » : à l'état b75a620, gen-plan = v3.23.1 (aucune v3.24.0 au corpus ni à l'installé) → le test du bug relève du plan d'actions AUDIT (Phase 2), qui devra simuler la montée v3.24.0 (génération mécanique §2quater) et vérifier la préservation de la machinerie de génération de plans (E9-E14, déclencheur E13, §9 extraction) | listing corpus : PROMPT-MAITRE-GEN-PLAN-v3.23.1.md = plus récent (dérivation KO-L003) | PM-INSTALL §2ter + §2quater | S2 | PASS |

## Étapes (E1-E15) — #token

| Étape | Action | #token | Statut |
|-------|--------|--------|--------|
| E1 | Analyse directive + answer key ci-dessus + hook E1-RES + garde É1-INSTALL (préemption §1.16) | 500 | ✓ terminé |
| E2 | Inventaire : lecture PM-INSTALL v1.7.1 + SHARED v1.7.7 (§0-§8) + arbitres (intégrité, verify-cross, certification, routage, interactions) + structure du dépôt | 900 | ✓ terminé |
| E3 | Classification Type 2 (installation/vérification écosystème) | 100 | ✓ terminé |
| E4 | Estimation #token : totale ~28 000 (installation ~22 000 consommés + audit ~6 000 restants) | 100 | ✓ terminé |
| E5 | Skills : gen-plan v3.23.1 (planification — présent plan), correct-work v2.7.0 (Mode PROJET E9-E14), skills-inventory (registre — protocole de découverte), clone-chat v2.0.1 (E15 archivage), resource-monitor (E1-RES ✓), knowledge-observer (E15) ; conventions skill-creator (SKILL.md), format agent-creator §6.1 (worklog), conventions script-creator (scripts), INFRA-1..3 script-mon-ecosysteme-infrastructure (déploiement artefacts) — routage N2 check-tool-routing | 300 | ✓ terminé |
| E6 | Profil NORMAL (aucun signal de pression) | 50 | ✓ terminé |
| E7 | Création du présent plan (via gen-plan v3.23.1 — couplage §1.5) | 400 | ✓ terminé |
| E8 | Validation du plan : answer-key-checker + verify-cross (99/99) + verify-correct-work (16/16) + check-ecosysteme-integrity (70/70) + test-coherence-interactions + check-tool-routing — verdict PASS requis | 600 | en cours |
| E9 | Certification étape 9 : (a) verify-cross ✓ 99/99 · (b) correct-work Mode PROJET (le présent plan = Étape 1 ; Étapes 2-5 ci-dessous) · (c) check-ecosysteme-integrity ✓ 70/70 — arbitres 5-6 re-passés après corrections D006/D007 | 800 | en cours |
| E10 | correct-work Étapes 2-3 (Mode PROJET) : erreurs/omissions (D001-D009 factuelles) + structure/conflits (conventions kebab-case, cross-refs bidirectionnelles, frontmatter complet) | 700 | en cours |
| E11 | correct-work Étape 4 : interactions (deps YAML : correct-work >=2.4.0 satisfait par v2.7.0, clone-chat >=2.0.0 par v2.0.1, skills-inventory >=1.0.0 par v1.1.0, knowledge-observer/resource-monitor >=1.0.0 ; couplage gen-plan↔correct-work, KB 33 entrées, matrice SHARED §3.1) | 400 | en cours |
| E12 | correct-work Étape 5 : cohérence des raisonnements (ordre des 11 étapes respecté, incidents §3.4 contournés-journalisés, décisions D001-D009 alignées actions/état) | 400 | en cours |
| E13 | Rapport `download/rapport-correct-work-projet-installation-2026-10-25.md` + worklog + certification-complete.py (consolidation 6 arbitres) + task14-scan-doublons.py (0 doublon attendu) | 600 | à venir |
| E14 | Publication étape 10 : archive v2.3 round-trip ✓ (déjà scellée E9) + scan doublons 0 + manifeste ecosysteme-integrity.json ✓ | 200 | à venir |
| E15 | Phase 2 — **plan d'actions de l'AUDIT** via gen-plan v3.23.1 (règle d'or n°2 : plan régénéré via le gen-plan fraîchement installé) : audit complet de l'écosystème incluant le test du bug « GEN-PLAN oublie de générer les plans d'actions depuis v3.24.0 » (D009) ; puis clôture : archivage session clone-chat (étape 11) + knowledge-observer M1-M2 | 6000 | à venir |

## Hooks phase E9-E14

PASS CIBLE après chaque phase (correct-work §5.4 gen-plan — hook par phase) ; E8 = vérification du plan (présent document) ; E15 knowledge-observer modes M1-M2 + clôture clone-chat (étape 11 PM-INSTALL : le clone scelle la session complète, installation + audit).

## Routage N2 (traçabilité d'usage — check-tool-routing Task 22 D006)

- skill → **skill-creator** (conventions structurelles des 33 SKILL.md installés — frontmatter complet)
- agent/PM → **agent-creator** (format §6.1 du worklog ; PMs du corpus @mon-ecosysteme/)
- script → **script-creator** (conventions des scripts de l'outillage scripts/ — docstring N3, stdlib)
- registre KB → **skills-inventory** (protocole de découverte ; registre skills/KNOWLEDGE.md 33 entrées)
- infrastructure → **script-mon-ecosysteme-infrastructure** (INFRA-1..3 : déploiement des artefacts de l'écosystème)
