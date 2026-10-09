# PROMPT MAÎTRE — Pipeline d'installation de l'écosystème personnel

Version : 1.6.0
Date : 2026-10-09
Fusionne : INSTALL-ECOSYSTEME.md v1.0.0 (périmètre §A — supprimé, directive utilisateur « source d'installation unique »)
Répare : le bloc CONTEXTE SYSTÈME embarqué, corrompu depuis le sync b13-r7-c (table dupliquée cassée, résolu par git @1519bbe)
Dépend : CONTEXTE SYSTÈME (embarqué ci-dessous)
Complète : ce fichier est l'UNIQUE source d'installation de l'écosystème — périmètre (§A) + ordre d'exécution optimal (§2) + étendue d'installation COMPLET/MINIMALE (§2bis, v1.4.0) + références explicites des dernières versions des PMs et du socle indispensable (§2ter, v1.5.1) + génération automatique du PM à toute montée de version (§2quater, v1.6.0) + critères de passage (§3).
Référence : §2ter — instantané explicite des dernières versions des PMs sources (GEN-PLAN, CORRECT-WORK, CLONE-CHAT) et des fichiers indispensables (directive utilisateur 2026-10-09) ; rafraîchi à chaque révision — la dérivation dynamique « PM le plus récent » (KO-L003) demeure la mécanique de référence ; §2quater (v1.6.0) — génération mécanique du PM à toute montée de version (KO-L004 v1.1.0, `scripts/generer-pm-skill.py`).
Fonction héritée (SHARED §7) : ce pipeline applique la méthode prompt-engineering (méthode-mère : gen-plan, PM v3.7.0 §1.9) en tant que fonction héritée — chaque étape est un artefact de prompt (entrée, instruction, arbitre, sortie).

---
## ⚙️ CONTEXTE SYSTÈME (Extrait SHARED v1.6.4)
> **INSTRUCTION** : Ce bloc remplace la dépendance de lecture externe.

### Règle Zéro (§0)
L'écosystème Knowledge est un ensemble de 80 skills conçus pour un assistant IA.

### Variables d'installation (§1.1)
| Variable | Défaut | Description |
|----------|--------|-------------|
| `{{SKILLS_ROOT}}` | `skills/` | Racine |
| `{{KB_PATH}}` | `skills/KNOWLEDGE.md` | Registre KB |

### Conventions de nommage (§1.2)
- **Répertoires** : kebab-case
- **Fichiers** : kebab-case avec extension
- **Versions** : format semver

---

---

## §0 — Objet et règle zéro

Ce fichier est la **source de vérité unique de l'installation** — périmètre et ordre — pour installer l'écosystème Knowledge de façon optimale, reproductible et vérifiable, à partir du seul contenu du répertoire `@mon-ecosysteme/`. Il synthétise le pipeline complet en une référence unique et fusionne le contenu du fichier `INSTALL-ECOSYSTEME.md` v1.0.0 (périmètre, §A ci-dessous), supprimé le 2026-10-02 pour mettre fin à la double source d'installation (R4 anti-duplication).

Règle zéro (SHARED §0) : skills auto-contenus sous `{{SKILLS_ROOT}}`, registre KB (`{{KB_PATH}}`) comme source de vérité, cross-references bidirectionnelles, conventions de nommage SHARED §1.2. Aucune étape ne produit d'effet public avant le passage des arbitres (§4).

Variables (SHARED §1.1) : `{{SKILLS_ROOT}}` = `skills/` · `{{KB_PATH}}` = `skills/KNOWLEDGE.md` · `{{KB_ENABLED}}` = `true` · `{{PROFILE_DEFAULT}}` = `NORMAL`.

## §1 — Pourquoi cet ordre (principe de dépendance)

L'ordre dérive du graphe d'interactions cartographié (README §8, SHARED §3.1) :

1. **Rien ne s'interprète sans le socle** — chaque fichier spécifique ouvre par « Lire SHARED en premier » (§B) → SHARED est l'étape 1.
2. **Rien ne s'installe depuis un corpus non authentifié** — les formes installées sont assemblées DEPUIS les PMs ; si le corpus est corrompu, tout le reste l'est → intégrité en étape 2.
3. **L'archive garantit la byte-identité** — l'intégrité du corpus est vérifiée par le round-trip de `download/mon-ecosysteme_archive.zip` (véhicule d'intégrité v2.2 ; décisions d'architecture v2.0 et v2.2 : miroir local `skills/_prompts-maitres/` supprimé, puis canal de fichiers download/ supprimé — le corpus n'est publié que via l'archive) → étape 2.
4. **gen-plan avant les skills qu'il orchestre** — correct-work (Étape 1 : gen-plan obligatoire) et clone-chat (§2.6 : intégration optionnelle) s'enregistrent auprès d'un gen-plan présent → étape 4.
5. **correct-work et clone-chat après gen-plan** — l'ordre P4-b/P4-c respecte le précédent validé (worklog A2/A3) et la direction de dépendance dominante (gen-plan —invoque→ correct-work) → étapes 5-6.
6. **Le registre KB après les skills** — KNOWLEDGE.md décrit les skills installés ; une entrée sans skill installé est une référence morte → étape 7.
7. **L'outillage avant la certification** — les arbitres vérifient l'état installé, ils ne le précèdent pas → étape 8.
8. **Rien ne se publie sans certification** — archives et clones ne sont produits qu'après verdicts PASS (le canal de fichiers download/ est supprimé — décision d'architecture v2.2, déduplication Task 14 : le corpus n'est publié que via l'archive d'intégrité) → étapes 9-10.

## §2 — Le pipeline en 10 étapes (ordre d'exécution optimal)

| # | Étape | Source → Destination | Arbitre | Critère de passage |
|---|-------|----------------------|---------|--------------------|
| 0 | **Contexte** | Lire PROMPT-MAITRE-SHARED.md (§0-§7) | — | Conventions, variables, relations connues |
| 1 | **Corpus** | Vérifier `@mon-ecosysteme/` (corpus canonique, invariant `CORPUS_ATTENDU` du checker) | SHAs corpus vs archive scellée (check-ecosysteme-integrity.py) | N/N présents, byte-identité corpus OK |
| 2 | **Archive** | Round-trip `download/mon-ecosysteme_archive.zip` ↔ corpus (miroir supprimé, décision d'architecture v2.0 ; canal de fichiers download/ supprimé, décision v2.2) | check-ecosysteme-integrity.py §2 | corpus ⊆ archive byte-identique + extras homologues/ |
| 3 | **gen-plan** | PM gen-plan le plus récent §5 → `skills/gen-plan/` : SKILL.md + `references/` (extraction §9, fences incluses) + `evals/` | Checks §6 du PM | Lignes ±tolérance ; refs présentes ; JSON valide |
| 4 | **correct-work** | PM correct-work le plus récent §5 → `skills/correct-work/SKILL.md` (assemblage §4+§A+§1+§2+§3+§10) | Checks §6 du PM | ~200-400 L ; 3 modes ; 5 étapes |
| 5 | **clone-chat** | PM clone-chat le plus récent §5 → `skills/clone-chat/SKILL.md` (assemblage §4+§A+§1+§2+§3+§5) + `références/clone-template.md` (§9.1) | Checks §6 du PM | ~300-450 L ; 7+1 étapes ; template présent |
| 6 | **Registre KB** | §A.3 (ce fichier) → `skills/KNOWLEDGE.md` (14 entrées écosystème cibles) | Compte d'entrées + formats §2.2 SHARED | ≥ 14 entrées, versions = règle §A.3 |
| 7 | **Outillage** | Déployer `scripts/` : verify-cross.py, check-ecosysteme-integrity.py, certification-complete.py, arbitres dédiés | python -c import (syntaxe) | scripts exécutables |
| 8 | **Certification** | Exécuter dans l'ordre : (a) verify-cross.py → (b) correct-work Mode PROJET → (c) check-ecosysteme-integrity.py | Les 3 arbitres eux-mêmes | 0 FAIL ; 0 S1-S2 ; N/N byte-identique |
| 9 | **Publication** | Archive zip (round-trip byte-identique) + worklog — canal de fichiers download/ supprimé (décision v2.2 : aucun fichier du corpus ne doit exister en double dans `download/`, garde `scripts/task14-scan-doublons.py`) | Vérif round-trip byte-identique + scan doublons 0 | N/N round-trip OK ; 0 doublon download/ |
| 10 | **Clôture** | clone-chat (archivage session) + mise à jour KNOWLEDGE.md si nouveau skill | 8 checks S1-S8 clone-chat | Clone scellé, idempotent |

Note (correct-work CIBLE, 2026-09-06, S3 ; révisée session A9, 2026-09-06) : les skills sans prompt maître propre — `skills-inventory`, `skill-creator`, `agent-creator`, `fullstack-dev` — n'ont pas de forme installée locale : ils existent comme entrées du registre KB (étape 6) et sont mobilisés à l'exécution, pas à l'installation. `prompt-engineering` est désormais MATÉRIALISÉ (forme installée `prompt-engineering/` : SKILL.md + evals/evals.json + evals/trigger_evals.json + references/grille-evaluation-prompt.md ; recommandation clone 2026-09-06 §5.2 exécutée).

Note (recalibrage v1.1.0, 2026-10-02) : les comptes et versions d'époque (15 fichiers, 7 fichiers cœur, PM gen-plan v3.7.0, arbitres 60/60) sont remplacés par des invariants dynamiques (KO-L003) : l'invariant `CORPUS_ATTENDU` du checker fait foi pour la taille du corpus ; « PM le plus récent » se dérive du listing réel du corpus ; les critères numériques sont les verdicts des arbitres courants.

## §2bis — Étendue d'installation : profils COMPLET (défaut) et MINIMALE (v1.4.0, Task 23)

**Objet (directive propriétaire « gagner de la place sur le disque dur »)** : le profil MINIMALE n'installe que les éléments nécessaires au fonctionnement de `gen-plan`, `correct-work` et `skills-inventory` (et de leurs éléments liés), ainsi que des agents `PROMPT-ULTRA-MAITRE-ORCHESTRATION.md`, `PROMPT-MAITRE-SHARED.md` et `SYNC-CONTEXT.md`.

**Fermeture MINIMALE (définition normative)** — l'union de :
- les 3 skills fonctionnelles : `gen-plan/`, `correct-work/`, `skills-inventory/` (formes installées complètes : SKILL.md + `references/` + `evals/` + `scripts/`) ;
- leurs éléments liés, dérivés MÉCANIQUEMENT au moment de l'installation (jamais figés — KO-L003) : dépendances déclarées (frontmatter YAML `dependencies` + registre KB « Dépend de ») et affectations SHARED §7 — à date : `resource-monitor`, `prompt-engineering`, `context-engineering`, `loop-engineering`, `graph-engineering`, `harness-engineering`, `knowledge-observer`, `audit-provenance`, `skill-creator`, `agent-creator`, `script-creator`, `script-reviewer`, `script-mon-ecosysteme-infrastructure`, `skill-finder-cn` (fallback §1.16 gen-plan v3.21.0) ;
- les agents requis : `PROMPT-ULTRA-MAITRE-ORCHESTRATION.md`, `PROMPT-MAITRE-SHARED.md`, `SYNC-CONTEXT.md`, plus `PROMPT-MAITRE-INSTALL-ECOSYSTEME.md` (véhicule de la réinstallation D006) ;
- l'outillage et le registre : `scripts/` (arbitres, certification-complete.py, G-RES, ensure-installed.py, task23-install-minimale.py) et `skills/KNOWLEDGE.md` (source de vérité).

**Propriétés** : le profil COMPLET demeure le DÉFAUT (pipeline §2 inchangé) ; la fermeture du profil MINIMALE est calculée par `scripts/task23-install-minimale.py` qui matérialise `scripts/install-profile.json` (profil, fermeture, empreintes SHA-256, gain disque mesuré) ; les arbitres opèrent sur le périmètre déclaré par ce manifeste ; l'archive d'intégrité et le corpus canonique `@mon-ecosysteme/` restent TOUJOURS complets (véhicule d'intégrité v2.2) — l'élagage ne s'applique qu'à l'arbre installé, jamais au corpus source.

## §2ter — Références explicites des PMs les plus récents et du socle indispensable (instantané v1.6.0, 2026-10-09)

**Objet (directive utilisateur « faire appel à la dernière version des prompts maîtres »)** : ce tableau matérialise l'instantané explicite des PMs sources mobilisés aux étapes 3-5 pour installer `gen-plan`, `correct-work` et `clone-chat`, ainsi que les fichiers du corpus et de l'outillage indispensables à l'installation et au bon fonctionnement de l'écosystème. Il complète sans les remplacer les mécanismes dynamiques : la dérivation « PM le plus récent » (KO-L003, §3.2) demeure la mécanique de référence et la garde anti-rétrogradation R2 s'applique ; cet instantané est rafraîchi à chaque révision du présent fichier.

### PMs sources des étapes 3-5 (dernières versions au 2026-10-09)

| Famille | PM source explicite (dernière version du corpus) | Version skill cible | Étape |
|---------|--------------------------------------------------|---------------------|-------|
| gen-plan | `PROMPT-MAITRE-GEN-PLAN-v3.21.0.md` | gen-plan v3.21.0 | 3 |
| correct-work | `PROMPT-MAITRE-CORRECT-WORK-v2.7.0.md` | correct-work v2.7.0 | 4 |
| clone-chat | `PROMPT-MAITRE-CLONE-CHAT-v2.0.0.md` | clone-chat v2.0.0 | 5 |

### Fichiers de socle indispensables (corpus, archive, outillage, registre)

| Fichier | Rôle | Mobilisé à |
|---------|------|-----------|
| `PROMPT-MAITRE-SHARED.md` | Socle commun — Contexte Système, conventions, registre des relations | Étape 0 |
| `PROMPT-ULTRA-MAITRE-ORCHESTRATION.md` | Routeur d'orchestration à l'usage (généré idempotent) | Étape 0 / usage |
| `SYNC-CONTEXT.md` | Procédure de synchronisation du Contexte Système | Étape 0 / maintenance |
| `README.md` | Architecture et guide de référence (§9 installation, §13 canal R-1) | Étape 0 / documentation |
| `download/mon-ecosysteme_archive.zip` | Véhicule d'intégrité v2.2 — unique voie de diffusion du corpus | Étapes 1-2, 9 |
| `scripts/check-ecosysteme-integrity.py` | Arbitre intégrité — invariant `CORPUS_ATTENDU`, SHAs corpus ↔ archive | Étapes 1-2, 8(c) |
| `scripts/verify-cross.py` | Arbitre structure et cross-references | Étape 8(a) |
| `scripts/certification-complete.py` | Orchestrateur des arbitres | Étapes 7-8 |
| `scripts/task14-scan-doublons.py` | Garde anti-doublons `download/` (0 doublon attendu) | Étape 9 |
| `scripts/task21-f2-rebuild-archive.py` | Rescellage de l'archive d'intégrité (round-trip v2.2) | Étapes 2, 9 |
| `scripts/install-ecosystem.py` · `ensure-installed.py` · `task23-install-minimale.py` | Bootstrap, réinstallation garantie, profil MINIMALE | Étapes 3-7 |
| `skills/KNOWLEDGE.md` | Registre KB — source de vérité de l'état installé | Étape 6 |

**Versions historiques (jamais sources d'installation)** : les PMs antérieurs du corpus (`PROMPT-MAITRE-GEN-PLAN-v3.6.1` → `v3.19.0`, `PROMPT-MAITRE-CORRECT-WORK-v2.4.0` → `v2.6.0`) demeurent au titre de la byte-identité historique assumée (SYNC-CONTEXT, rétro-compatibilité R2) — les étapes 3-5 ne les mobilisent jamais (garde R2).

## §2quater — Génération automatique du PM à toute montée de version (v1.6.0, 2026-10-09)

**Directive KO-L004 v1.1.0 (gen-plan §1.15, matérialisation M4 — session web-b93f42fa)** : chaque fois qu'un skill des 3 familles (gen-plan, correct-work, clone-chat) monte en version, l'écosystème génère MÉCANIQUEMENT — avant toute certification — le prompt maître de la nouvelle version dans `@mon-ecosysteme/` sous le nom `PROMPT-MAITRE-<famille>-v<version>.md` (ex : `PROMPT-MAITRE-GEN-PLAN-v3.21.0.md` pour gen-plan v3.21.0). Aucun PM nouveau n'est rédigé à la main : la génération est l'affaire du script, l'agent ne complète que les deltas sémantiques.

**Mécanique** (`scripts/generer-pm-skill.py`, Python stdlib — `--check` et `--generate <famille|all> [--delta FILE] [--dry-run]`) :
- source de vérité : frontmatter `version:` de `skills/<famille>/SKILL.md` ; base : PM le plus récent du corpus (dérivation dynamique KO-L003) ;
- substitutions verrouillées : ABANDON SANS ÉCRITURE si un motif n'apparaît pas exactement n fois (méthode B1) ; garde anti-rétrogradation R2 (jamais de rétrogradation sous la forme installée) ;
- recalibrage croisé inclus : SHARED §6.1, PM-INSTALL §2ter/§A.3, historiques ; rapport de couverture SKILL.md↔PM (`scripts/generer-pm-report.json`) — le script ne masque jamais un écart (KO-L003) ; idempotent ×2 ;
- codes retour : 0 ok/no-op · 1 écart détecté (--check) · 2 ABANDON verrouillé · 3 usage invalide.

**Non-régression** : ce §2quater complète §2ter sans le remplacer (l'instantané explicite demeure rafraîchi à chaque révision) ; la dérivation dynamique KO-L003 (§3.2) demeure la mécanique de référence et la garde R2 s'applique ; l'ordre prescrit est : montée de version → génération PM (§2quater) → recalibrage des porteurs (KO-L004) → certification (étape 8 §3).

## §3 — Détail des points de contrôle critiques

### §3.1 Étape 1 — Intégrité du corpus
Comparer les SHAs SHA-256 des fichiers du corpus aux valeurs scellées dans l'archive de référence (méthode neutral-line, Annexe D du PDF source ; canal R-1 = README §13, référence historique). Toute divergence = STOP : restaurer depuis `download/mon-ecosysteme_archive.zip` ou le stockage versionné avant de reprendre au contrôle 1.

### §3.2 Étapes 3-5 — Assemblage des formes installées
Les SKILL.md sont ASSEMBLÉS depuis les PMs (jamais copiés à l'aveugle) : YAML frontmatter (§4 du PM) + règle zéro + spécifications (§1-§2) + relations (§3) + sections spécifiques. Les fichiers de référence sont extraits des blocs ```` ```markdown ```` du §9 avec fences incluses (round-trip déterministe, leçon A2) — l'extraction doit être insensible aux titres internes des blocs (logique de balance des fences).

**Dérivation « PM le plus récent » (v1.2.0, KO-L003)** : le PM source de chaque famille (gen-plan, correct-work, clone-chat) est le plus récent du corpus, dérivé du listing réel de `@mon-ecosysteme/` par tri semver des suffixes `-vX.Y.Z.md` — jamais d'un numéro figé. **Garde anti-rétrogradation (R2)** : si la version du PM dérivé est inférieure à celle du SKILL.md installé (`skills/<famille>/`, frontmatter = source de vérité), la forme installée est conservée inchangée — l'assemblage ne rétrograde jamais — et l'écart est journalisé au worklog ; l'entrée KB (étape 6) porte la version installée. Cas d'espèce au jour de la v1.2.0 : correct-work — corpus v2.5.1, installé v2.7.0 → l'étape 4 conservait v2.7.0. **Ce cas d'espèce est RÉSORBÉ depuis la v1.3.1 (Task 16, 2026-10-02)** : les PMs CORRECT-WORK v2.6.0/v2.7.0 sont matérialisés au corpus (reconstitution par diffs chirurgicaux méthode B1, provenance tracée au §7 de chaque PM) — le corpus porte désormais la forme certifiée v2.7.0 et la garde R2 demeure pour tout état futur.

### §3.3 Étape 8 — Arbitres et sévérité
L'ordre (a)→(b)→(c) est contraint : verify-cross valide la structure (rapide, déterministe), correct-work valide le raisonnement (coûteux, ne s'exécute que si la structure est saine), check-ecosysteme-integrity valide l'authenticité (corpus ↔ archive ↔ registre). Toute sévérité S1 (critique) ou S2 (majeure) à l'étape 8 = retour à l'étape correspondante du pipeline ; S3/S4 = journalisation au worklog + reprise.

### §3.4 Incidents (règle d'or n°1, PM gen-plan §1.8)
Tout blocage (fichier absent, wipe inter-sessions, outil perdu) = signal d'adaptation, jamais un arrêt : contournement conforme aux conventions, journalisation au worklog (cause, solution, coût #token), reprise à l'étape en échec. Le wipe inter-sessions est un cas documenté : ré-exécuter ce pipeline depuis l'étape 2 (le corpus `@mon-ecosysteme/` est la source de vérité restaurable).

## §4 — Interactions mobilisées par le pipeline (cartographie T2)

| Interaction | Mobilisée aux étapes | Nature |
|-------------|----------------------|--------|
| gen-plan —invoque→ correct-work | 3, 8(b) | E1 + hook E8 + contrôle par phase |
| gen-plan —utilise→ clone-chat | 3, 10 | E4, E15 (optionnel) |
| correct-work —utilise→ gen-plan | 4, 8(b) | Plan de vérification (obligatoire, dernière version) |
| correct-work —vérifie→ clone-chat | 5, 10 | Mode CIBLE (drifts) |
| clone-chat —enrichit→ KNOWLEDGE.md | 6, 10 | Descriptions §2 |
| skills-inventory —scanne→ KNOWLEDGE.md | 6 | Registre source |
| install-ecosystem —utilise→ infrastructure | 2-7 | Déploiement P6-P7 |
| gen-plan —délègue→ prompt-engineering | 0-10 | Optimisation fine des prompts |

## §5 — Relations

| Avec | Nature | Détails |
|------|--------|---------|
| PROMPT-MAITRE-SHARED.md | Socle | Conventions, variables, registre relations (§3.1), méthode prompt-engineering (§7) |
| (fusion v1.1.0) | Périmètre absorbé | INSTALL-ECOSYSTEME.md v1.0.0 supprimé 2026-10-02 — son périmètre est porté par le §A de ce fichier ; recréer un second installateur est interdit (R4) |
| PM gen-plan le plus récent | Spécification | Étape 3 (méthode-mère prompt-engineering, §1.9) |
| PM correct-work le plus récent | Spécification | Étape 4 + arbitre étape 8(b) |
| PM clone-chat le plus récent | Spécification | Étape 5 + clôture étape 10 |
| PROMPT-ULTRA-MAITRE-ORCHESTRATION.md | Route à l'usage (généré idempotent) | Point d'entrée d'orchestration globale — route chaque demande vers les PMs/skills sans dupliquer leur contenu (v1.0.0, 2026-10-02) ; ce fichier reste la source d'INSTALLATION, l'orchestrateur ne remplace aucun PM |
| README.md | Documentation | §9 architecture, §10 workflows, §12 verify-cross, §13 canal R-1 |

## §6 — Maintenance

- Toute évolution du périmètre (nouveau PM, nouveau skill) se traduit par : mise à jour de la table §2 + du §A + entrée KNOWLEDGE.md + cross-references bidirectionnelles (SHARED §3.2).
- L'ordre des étapes 3-5 suit le précédent P4-a/P4-b/P4-c ; il ne doit être modifié qu'avec un changement de contrat documenté (SHARED §3.2 règle 5).
- Ce fichier est l'UNIQUE source d'installation (documentaire et orchestration) : il ne détient pas la méthode prompt-engineering (fonction héritée, SHARED §7), ne remplace pas les §5 des PMs, et la recréation d'un fichier d'installation parallèle est interdite (R4 anti-duplication — leçon de la fusion v1.1.0).

## §7 — Historique

| Version | Date | Changements |
|---------|------|-------------|
| v1.6.0 | 2026-10-09 | Directive KO-L004 v1.1.0 (gen-plan §1.15, matérialisation M4 — session web-b93f42fa) : §2quater — génération automatique du PM à toute montée de version des 3 familles (`scripts/generer-pm-skill.py` : substitutions verrouillées méthode B1, garde R2, recalibrage croisé SHARED §6.1 + §2ter/§A.3 inclus, rapport de couverture SKILL.md↔PM, idempotent ×2 ; ex : PROMPT-MAITRE-GEN-PLAN-v3.21.0.md) ; §2ter instantané rafraîchi v1.6.0 ; §2bis référence §1.16 gen-plan v3.19.0 → v3.21.0 (recalibrage KO-L004 — occurrence réelle résorbée) ; recalibrage croisé KO-L004 : SHARED v1.6.7 (§6.1 matérialisation), check-ecosysteme-integrity.py ECO_SKILLS gen-plan 3.19.0 → 3.21.0, KNOWLEDGE.md entrée gen-plan v3.19.0 → v3.21.0, leçon L004 marqueur PATTERN v1.1.0 |
| v1.5.1 | 2026-10-09 | Règle d'or n°4 gen-plan (directive utilisateur « si tu dois utiliser un élément de mon dépôt alors clone-le à la place de lire son contenu sur mon dépôt », session web-b93f42fa) : §2ter — instantané rafraîchi gen-plan v3.20.0 → v3.21.0 (règle d'or n°4 : récupération du dépôt par clone git local, jamais lecture distante API/raw/web) ; §A.3 instantané courant v1.5.1 ; dérivation dynamique KO-L003 et garde R2 inchangées ; recalibrage croisé KO-L004 : SHARED v1.6.6 (§6.1 : gen-plan v3.21.0, PM-INSTALL v1.5.1) |
| v1.5.0 | 2026-10-09 | Directive utilisateur « faire appel à la dernière version des prompts maîtres » : §2ter — instantané explicite des PMs sources des étapes 3-5 (GEN-PLAN v3.20.0, CORRECT-WORK v2.7.0, CLONE-CHAT v2.0.0) et des fichiers de socle indispensables (SHARED, ULTRA-ORCHESTRATION, SYNC-CONTEXT, README, archive d'intégrité, arbitres, registre KB) ; dérivation dynamique KO-L003 et garde R2 conservées comme mécanique de référence ; instantané rafraîchi à chaque révision ; recalibrage croisé KO-L004 : SHARED v1.6.5 (§6.1 : gen-plan v3.20.0, PM-INSTALL v1.5.0) |
| v1.4.0 | 2026-10-03 | Directive Task 23 (gain de place disque) : §2bis profil d'installation MINIMALE — fermeture mécanique {gen-plan, correct-work, skills-inventory + liés KB/SHARED §7 + agents ULTRA/SHARED/SYNC-CONTEXT/INSTALL + outillage + KB} dérivée par `scripts/task23-install-minimale.py` (manifest `scripts/install-profile.json` : profil, fermeture, empreintes, gain mesuré) ; COMPLET demeure le défaut ; corpus `@mon-ecosysteme/` et archive d'intégrité intacts (l'élagage ne touche que l'arbre installé) ; recalibrage croisé KO-L004 : gen-plan v3.19.0 (§1.16 routage découverte + É1-INSTALL), ECO_SKILLS (gen-plan 3.19.0, skill-creator 1.1.0, version-management 1.1.0 — francisation Task 23) |
| v1.3.1 | 2026-10-02 | Résorption du cas d'espèce correct-work du §3.2 (suggestion (b), Task 16 — directive « appliquer (a) puis (b) pour résorber les écarts F1/F2/F4 », session web-8a7e5653) : PMs CORRECT-WORK v2.6.0/v2.7.0 matérialisés au corpus par diffs chirurgicaux depuis v2.5.1 (méthode B1 — script `scripts/materialise-pm-correct-work.py`, provenance de reconstitution tracée dans l'en-tête et le §7 de chaque PM, aucun faux lignage) ; CORPUS_ATTENDU 24 → 26, recalibrage croisé KO-L004 (SHARED v1.6.4 §6.1, SYNC-CONTEXT v1.4.1, orchestrateur ULTRA régénéré, archive rescellée round-trip 26/26) ; la garde R2 du §3.2 demeure pour tout état futur |
| v1.3.0 | 2026-10-02 | Directive utilisateur (déduplication « même nom, même contexte, idempotent ») : décision d'architecture v2.2 — le canal de fichiers download/ est supprimé, les 14 fichiers corpus répliqués dans download/ sont effacés (le corpus n'est publié que via l'archive d'intégrité, véhicule v2.2) ; étape 7 recalibrée (sync-download.py retiré → certification-complete.py) ; étape 9 recentrée archive + garde anti-doublons `scripts/task14-scan-doublons.py` (0 doublon attendu) ; recalibrage croisé KO-L004 : SHARED v1.6.3 (§6.1 + ligne harness), SYNC-CONTEXT v1.4.0 (une seule voie de diffusion), README v2.1.0, orchestrateur ULTRA régénéré, arbitres recalibrés (check 3 inversé, §7/§11d interactions), résorption des réserves trigger_evals (evals skill-creator + version-management équipés) |
| v1.2.0 | 2026-10-02 | Directive utilisateur (vérification préalable « continue mais avant vérifie… ») : généralisation de la dérivation dynamique « PM le plus récent » aux 3 familles — l'étape 5 et la relation §5 épinglaient clone-chat v2.0.0, incohérence avec la règle §A.3 (KO-L003) ; garde anti-rétrogradation R2 au §3.2 (cas correct-work : corpus v2.5.1 < installé v2.7.0 — la forme installée fait foi, jamais de rétrogradation, écart journalisé au worklog) ; recalibrage croisé KO-L004 : SHARED §6.1 (v1.6.2), orchestrateur régénéré (routage T1 clone-chat dynamisé), archive rescellée, canal download/ resynchronisé (dernière synchronisation avant sa suppression v1.3.0) |
| v1.1.1 | 2026-10-02 | Cross-ref §5 : PROMPT-ULTRA-MAITRE-ORCHESTRATION.md v1.0.0 (route à l'usage, généré idempotent) — complément de cohérence suite à vérification propriétaire « garder un prompt maître et le mettre à jour » : ce fichier EST le prompt maître d'installation conservé, mis à jour selon les demandes du jour (source unique, miroir supprimé, gen-plan obligatoire v2.7.0, périmètre §A absorbé) |
| v1.1.0 | 2026-10-02 | Fusion directive utilisateur : absorption du périmètre d'INSTALL-ECOSYSTEME.md v1.0.0 (supprimé) en §A — source d'installation unique ; réparation du bloc CONTEXTE SYSTÈME corrompu (table dupliquée cassée, contenu restauré depuis git @1519bbe) ; étape 2 « Miroir » révisée « Archive » (exécution décision d'architecture v2.0 : miroir skills/_prompts-maitres/ supprimé, round-trip archive v2.1 fait foi) ; invariants dynamiques recalibrés (KO-L003) : « PM le plus récent », CORPUS_ATTENDU, verdicts arbitres courants ; §A.3 versions dynamiques (anti-drift) ; criterion correct-work étape 1 : gen-plan obligatoire (couplage v2.7.0) |
| v1.0.0 | 2026-09-06 | Création (directive utilisateur) : pipeline 10 étapes issu de la cartographie des interactions ; principes de dépendance §1 ; critères de passage et arbitres §3 ; intégration règle d'or n°1 et canal R-1. Certification correct-work Mode CIBLE : PASS 31/31, 0 S1-S2, 1 S3 corrigée (note skills sans PM) |

## §A — Périmètre d'installation (absorbé d'INSTALL-ECOSYSTEME.md v1.0.0)

### §A.1 Périmètre général
26 fichiers répartis sur 4 zones (sommaire d'époque v1.0.0 conservé tel que documenté ; le détail zone-par-zone n'a jamais été développé dans le fichier source). Zones attestées par les référents : corpus prompts maîtres (`@mon-ecosysteme/`), formes installées (`skills/<skill>/`), registre KB (`skills/KNOWLEDGE.md`), outillage (`scripts/`).

### §A.2 Les 8 phases P0-P7
Note P4 : les SKILL.md + références des 4 skills sont créés en suivant le §5 de chaque prompt maître (ou via gen-plan). Le bootstrap install-ecosystem.py couvre P0-P3, P5-P7.

### §A.3 Registre KB cible (14 entrées)
Règle de version (recalibrage v1.1.0, anti-drift) : la version de chaque entrée est celle du PM le plus récent présent dans le corpus au moment de l'installation (dérivation dynamique — KO-L003) ; les versions figées d'époque ci-dessous (gen-plan v3.10.0, correct-work v2.5.1, prompt-engineering v1.0.1) sont des instantanés historiques et ne doivent pas être ré-installées telles quelles si le corpus porte un PM plus récent.

Instantané courant (v1.6.0, 2026-10-09) : gen-plan v3.21.0 · correct-work v2.7.0 · clone-chat v2.0.0 — cf. §2ter.

| Entrée KNOWLEDGE.md | Version d'époque |
|---------------------|------------------|
| gen-plan | v3.10.0 |
| correct-work | v2.5.1 |
| clone-chat | v2.0.0 |
| skills-inventory | v1.0.0 |
| skill-creator | v1.0.0 |
| agent-creator | v1.0.0 |
| script-mon-ecosysteme-infrastructure | v1.0.0 |
| install-ecosystem | v1.0.0 |
| prompt-engineering | v1.0.1 |
| verify-by-sha | v1.0.0 |
| context-engineering | v1.0.1 |
| loop-engineering | v1.0.1 |
| graph-engineering | v1.0.1 |
| harness-engineering | v1.0.1 |

Catégorie (attestée) : ecosystem — les 4 dernières matérialisations sont les skills des disciplines d'exécution (socle SHARED §7, session A12) : forme installée `<discipline>/` — SKILL.md + evals/evals.json + evals/trigger_evals.json, déclenchement automatique ; matérialisations agent `_disciplines/` retirées, SHA prouvés ; « Utilisé par » : gen-plan (couche disciplines), sessions d'ingénierie ; matérialisées 2026-09-07.
