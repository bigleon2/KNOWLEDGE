---
name: version-management
version: 1.3.0
category: metier
language: fr
tags:
  - version-management
  - front-end
  - project-lifecycle
description: Skill autonome générique de gestion de versions (version management) couvrant tout le cycle de vie des projets front-end. Dès que la tâche **risque** d'écrire un fichier d'entrée .html/.jsx/.tsx/.vue — typiquement toute demande de **création de page web ou d'interface** — page, site, formulaire, landing page, tableau de bord / dashboard, visualisation de données rendue en page —, il faut lire et suivre ce Skill **avant** d'écrire le premier fichier (pour déterminer le chemin de dépôt et le répertoire projet), et non en rattrapage après production ; à utiliser même si l'utilisateur ne mentionne ni « projet » ni « version ». Répond aussi aux opérations de versions et de projets demandées par l'utilisateur — consultation de l'historique, montée de version / incrément semver, mise à jour, restauration, rétrogradation, retour à une version antérieure, release, changelog, changement de projet, revenir à / reprendre / basculer vers le dernier projet ou un projet précédent, etc.
read_when:
  - Déclencher quand la demande concerne : skill autonome générique de gestion de versions (version management) couvrant tout le cycle de vie des projets…
  - Déclencher si la demande mentionne : projet, version, page
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

## §0 — Contexte Système (SHARED v1.7.36)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.
> Langue : FRANÇAIS exclusif pour tous les échanges avec le propriétaire (règle d'or n°6 gen-plan — directive 2026-10-31, renforcée 2026-11-06) : dès le PREMIER mot de toute session ou reprise, la langue d'un message, d'un résumé de continuation ou d'un canal ne dérive JAMAIS la réponse ; toute dérive est corrigée immédiatement.
> Règles d'or & lecture SHARED à l'exécution (directive propriétaire 2026-11-06 — SHARED §9) : tout skill/agent/script exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or de l'écosystème (résumé §9 — canonique gen-plan §1.5).
> Référence canonique skill/agent (directive propriétaire 2026-11-07 — SHARED §0/§1.2) : toute référence à « mon skill X »/« mon agent X » désigne la forme installée à la racine `skills/X/SKILL.md`, JAMAIS le prompt maître du corpus `@mon-ecosysteme/` (ex-nommé `@PM-SKILLS/`) — les PMs sont des spécifications générées mécaniquement (KO-L004), les skills installés sont les formes exécutables.

# Gestion de versions

> **Mode d'exécution :** la gestion de versions est **entièrement réalisée par ce Skill + `send_file`** ; ni le front-end ni le back-end ne maintiennent Git ni un journal de versions. L'Agent exécute git et les opérations fichiers dans le répertoire projet de la machine cloud. Les commandes git ci-dessous sont des commandes exécutables complètes ; une fois encapsulées en tools, seuls les paragraphes d'instructions seront remplacés — **la logique de décision et l'ordre du processus restent inchangés**.

> **Règle de communication avec l'utilisateur :** les détails techniques de la gestion de versions (commandes git, mise à jour de `meta.json`, calcul des numéros de version, etc.) relèvent du processus d'exécution interne ; il est interdit de les montrer ou de les mentionner à l'utilisateur dans la conversation. L'utilisateur ne doit voir que : le résultat généré + la carte de version émise par `send_file`. Pour communiquer une information de version, dire uniquement « enregistré sous V{n} », sans expliquer les opérations sous-jacentes.

---

## ⚠️ Règle absolue des chemins (priorité maximale, à exécuter avant d'écrire tout fichier)

**Ce Skill doit intervenir avant l'écriture du premier fichier d'entrée, pas en rattrapage après production.** Dès la première écriture sur disque d'un fichier d'entrée (`.html` / `.jsx` / `.tsx` / `.vue`), le chemin cible doit se situer dans `mes-projets/{nom-projet}/`.

### Chemin de référence

« mes-projets » **se trouve fixé à la racine du workspace**, en correspondance un à un avec l'écriture `file_path` de `send_file` : `/mes-projets/{nom-projet}/...`. Avant toute opération `mkdir` / `cd` / écriture de fichier, il faut d'abord revenir à la racine du workspace (ou utiliser un chemin complet calculé depuis la racine) ; **interdit** d'utiliser le chemin relatif `mes-projets/...` sans avoir confirmé `pwd` — c'est la cause fréquente d'un dossier « mes-projets » créé au mauvais endroit.

### Ordre fixe avant écriture des fichiers (non permutable)

```bash
# 1. Déterminer le nom du projet (règles de génération : voir §1.2)
# 2. Revenir à la racine du workspace, créer le répertoire projet
cd {racine-workspace}
mkdir -p "mes-projets/{nom-projet}/assets"
# 3. Entrer dans le répertoire projet ; tous les fichiers sont ensuite créés [directement] dans ce répertoire
cd "mes-projets/{nom-projet}"
# 4. Écrire index.html / prototype.html etc. (fichiers d'entrée et fichiers de code)
# 5. Enchaîner ensuite le flux git / meta.json / send_file du §1
```

### Liste des violations (chacun des cas ci-dessous est une erreur de processus, même déplacé après coup)

- Écrire d'abord les fichiers à la racine du workspace, dans `~/Desktop`, `/tmp` ou n'importe quel répertoire courant, puis les déplacer dans le répertoire projet
- Coller le code uniquement dans la conversation, sans écriture sur disque
- Exécuter des commandes d'écriture de fichiers hors du répertoire projet

### Auto-contrôle avant écriture (dernier verrou)

Avant toute commande d'écriture de fichier, se poser la question : **« Le chemin cible que je m'apprête à écrire se trouve-t-il dans `mes-projets/{nom-projet}/` ? »** Si la réponse est non → stop, exécuter d'abord l'ordre fixe ci-dessus pour créer les répertoires, puis écrire les fichiers.

---


## 0. Articulation avec le Design Skill (lecture obligatoire)

Ce Skill coopère **en parallèle** avec le Design Skill (les deux sont portés simultanément par le même Design Agent) : le Design Skill assure la production de conception, ce Skill assure le dépôt sur disque et la gestion de versions. Cette section décrit leur collaboration dans le scénario de livraison HTML.

> **Le déclenchement ne dépend pas du Design Skill.** Ce Skill se déclenche par type de fichier : dès qu'on produit **ou modifie** un fichier d'entrée (.html / .jsx / .tsx / .vue), il faut passer par ce Skill, que la tâche ait ou non emprunté le routage du Design Skill — y compris les cas de modification directe du texte/couleur d'un HTML existant sans aucun flux de conception (on saute alors quality-gate et on enchaîne directement : vérification des ressources → git → meta.json → send_file).

### Ordre de déclenchement (en coordination avec le Design Skill)

```text
Routage Design Skill → skill de scénario (portfolio / deck / prototype etc.)
→ [avant d'écrire les fichiers] créer d'abord mes-projets/{nom-projet}/ selon la « Règle absolue des chemins » en tête de ce Skill
→ production .html / .jsx / .tsx / .vue → fichiers [écrits directement] dans mes-projets/{nom-projet}/ (pas de déplacement après coup)
→ quality-gate.md validé
→ ce Skill (vérification des ressources → git → meta.json → send_file)
```

**Interdit** de commit ou `send_file` une production issue du Design Skill tant que la quality gate n'est pas validée.
**Interdit** au Design Skill de considérer un projet web HTML comme livré sans que ce Skill soit allé au bout (coller seulement le code, ne rien écrire sur disque, ne rien écrire dans `mes-projets/` ne comptent pas comme livraison).

### Design Skill en charge / ce Skill en charge

| Dimension | Design Skill | Ce Skill |
|------|--------------|----------|
| Scénario, style, mise en page, langue des textes | ✅ | — |
| quality-gate, commentaires Design Compliance | ✅ | — |
| Répertoire projet, dépôt des assets, versions git | — | ✅ |
| `meta.json`, cartes de version `send_file` | — | ✅ |
| Communication vers l'utilisateur | description du résultat de conception | uniquement « enregistré sous V{n} » |

### Suggestions de résumé de commit

`git commit -m` et le `summary` de `meta.json` peuvent mentionner le scénario, pour faciliter l'identification par l'utilisateur, par exemple :

- `V2: refonte du hero de la page d'accueil (portfolio)`
- `V3: à partir de V1 : passage au style International (landing-page)`

### Point d'entrée de lecture

La description de l'articulation côté Design figure dans : `SKILL.md` § Version Management Handoff. Les mécanismes de dépôt sur disque, git, `meta.json`, `send_file` etc. sont régis par ce Skill (le design ne fait que transférer, sans redéfinir).

---

## 0.1 État de la prévisualisation (limitations connues, maintien en l'état)

| Phénomène | Cause | Traitement actuel |
|------|------|----------|
| Projets HTML multi-fichiers (multi-pages, plusieurs html) : impossible de naviguer entre les pages | la prévisualisation passe par des liens OSS ; seuls les HTML et les images ont été traités cette fois, le paquet complet n'est pas encore uploadé sur OSS et les chemins relatifs référencés par les autres html ne peuvent pas être chargés par le front-end | **non traité pour l'instant**, maintenu en l'état |
| Dans certains scénarios, l'aperçu d'une version historique peut encore montrer la dernière version | la prévisualisation scanne à la volée les chemins du workspace puis régénère l'OSS, sans isolation par tag | **non traité pour l'instant**, maintenu en l'état |
| HTML mono-fichier avec `.js``.css``assets/` (images) : généralement prévisualisable | le back-end remplace les chemins relatifs des ressources dans le HTML par des liens OSS | normal |

**À savoir pour l'Agent :** ces limitations n'affectent ni le commit de versions ni l'émission `send_file` ; ne pas basculer vers l'inlining de toutes les ressources ni forcer la mise en mono-fichier à cause d'un échec de prévisualisation.

---

## 1. Création du projet

### 1.1 Règles de décision

Si la production contient des fichiers front-end de l'un de ces types : `.html`, `.jsx`, `.tsx`, `.vue` → **obligation** de créer/mettre à jour le projet et de suivre le flux de versions (indépendamment du Skill appelant emprunté à ce moment-là).
Si la production est une image, un doc, un ppt, du JSON, une design spec, du texte pur etc. → fichier ordinaire, pas de création de projet.

**Erreurs de jugement fréquentes (interdites) :** penser que le routage vers un scénario appelant autorise « seulement coller le code » ou « écrire sur le Desktop » ; dès qu'on écrit un fichier d'entrée HTML/front-end, on livre comme un projet.

### 1.2 Contrôle obligatoire des chemins (règle critique)

> **Intégral archivé R4** : `references/controle-chemins.md` (2,2 Kio — SHA-256 088a88871dcdb0fc…) — tous les fichiers sous `mes-projets/{nom-projet}/` — prévention d'abord, contrôle avant commit, répertoire projet auto-contenu obligatoire. Chargé à la demande (lecture ciblée E5-POIDS — jamais par défaut).

### 1.3 Règles de structure des fichiers

> **Intégral archivé R4** : `references/regles-structure-fichiers.md` (5,7 Kio — SHA-256 f31e059e63371a80…) — répertoire projet auto-contenu — mono-fichier vs multi-fichiers selon le type de projet (landing, H5, vitrine, application). Chargé à la demande (lecture ciblée E5-POIDS — jamais par défaut).

### 1.4 Flux de création

À la première production d'un fichier d'entrée pour l'utilisateur (**les étapes 1 à 3 doivent survenir avant l'écriture de tout fichier de code**, voir la « ⚠️ Règle absolue des chemins » en tête) :

1. Générer le nom du projet d'après l'intention de l'utilisateur
2. Revenir à la racine du workspace ; si « mes-projets » n'existe pas : `mkdir -p mes-projets/`
3. Créer le répertoire projet et assets : `mkdir -p mes-projets/{nom-projet}/assets`, puis `cd` dedans, **tous les fichiers s'écrivent directement dans ce répertoire**
4. Copier d'abord les images utilisateur de `upload/` vers `assets/`, puis écrire le HTML ; interdit d'écrire seulement un chemin `assets/` sans dépôt sur disque
5. Initialisation Git et premier commit :

```bash
cd mes-projets/{nom-projet}
git init
echo -e "meta.json\nstyle-samples*.html" > .gitignore
git add .
git commit -m "V1: {resume-en-une-phrase}"
git tag v1
# ↑ tout ce qui précède doit être exécuté intégralement, puis créer meta.json, et enfin appeler send_file pour émettre V1
```

6. Créer `meta.json` (structure : voir §5)
7. Appeler `send_file` pour émettre cette version (voir §3.4), `title` = nom du projet (ex. `site-voyage-pekin`)

### 1.5 Structure du répertoire projet

```
upload/                  ← point de chute des uploads utilisateur (hors Git du projet)

mes-projets/
└── {nom-projet}/
    ├── .git/
    ├── .gitignore       ← exclut meta.json et style-samples*.html
    ├── meta.json        ← métadonnées de versions (hors Git)
    ├── style-samples*.html ← maquettes de directions de design, plusieurs directions numérotées au choix de l'utilisateur (hors Git, optionnel, multi-tours)
    ├── index.html       ← entrée principale (suivie par Git, chemin variable selon le projet)
    ├── ...              ← autres fichiers de code (suivis par Git)
    ├── assets/          ← fichiers de ressources (suivis par Git, tracés avec les snapshots de version)
    └── export/          ← produits d'export (suivis par Git, pour les projets à images fixes)
```

---

## 2. Gestion multi-projets

### 2.1 Identification du projet courant

Par ordre de priorité :

1. Nom de projet explicitement mentionné dans le langage naturel de l'utilisateur
2. Projet correspondant au tab courant transmis par le front-end (sert uniquement à identifier le projet, ne décide pas de la version à éditer)
3. Projet manipulé le plus récemment dans la session courante
4. Si rien ne permet de trancher → scanner les sous-répertoires de `mes-projets/`, lire le `meta.json` de chaque projet, lister les projets et poser la question

### 2.2 Changement de projet

Lire le `meta.json` du projet cible et l'annoncer à l'utilisateur : « Projet rejoint : {nom-projet}, version courante V{n} »

### 2.3 Tâches hors projet

Les tâches qui ne produisent pas de fichier d'entrée ne déclenchent aucune opération de projet ni de version.

---

## 3. Gestion des versions

### 3.1 Points d'entrée d'édition et détermination de la version

> **Intégral archivé R4** : `references/points-entree-edition.md` (3,4 Kio — SHA-256 4e6435236ca92f2f…) — table des points d'entrée d'édition (commentaire, carte, restauration) et détermination de la version de base du projet. Chargé à la demande (lecture ciblée E5-POIDS — jamais par défaut).

### 3.2 Moments de création de version

| Scénario déclencheur | Nouvelle version ? | Remarque |
|--------|-------------|------|
| Première production | ✅ V1 | création du projet |
| Édition en langage naturel | ✅ | incrément du numéro de version |
| Édition par commentaire | ✅ | incrément du numéro de version |
| Sauvegarde via l'éditeur de paramètres | ✅ | changer un texte, des paramètres de style ou remplacer une image compte comme nouvelle version |
| Restauration de version | ✅ | voir §4 |
| Édition à partir d'une version historique | ✅ | fusion §4, produit une seule version |
| L'utilisateur n'uploade que des ressources, sans changement de code | ❌ | écriture dans `assets/` seulement, pas de commit |
| Upload utilisateur et références du code mises à jour par l'Agent | ✅ | commit + `send_file` obligatoires |
| Ajout d'un fichier d'entrée dans le même projet (ex. ajout de `light.html`) | ✅ | le nouveau fichier est commité avec les fichiers existants comme nouvelle version |
| Production de maquettes `style-samples*.html` | ❌ | hors Git, hors numérotation de version, seulement émises via `send_file` pour le choix de l'utilisateur |

### 3.3 Commandes Git de création de version

Une fois les modifications terminées, exécuter dans le répertoire projet :

```bash
cd mes-projets/{nom-projet}
LATEST_TAG=$(git tag --sort=-v:refname | head -n 1)
NEXT_NUM=$((${LATEST_TAG#v} + 1))
NEXT_TAG="v${NEXT_NUM}"
git add .
git commit -m "V${NEXT_NUM}: {resume-en-une-phrase}"
git tag $NEXT_TAG
# ↑ tout ce qui précède doit être exécuté intégralement, puis mettre à jour meta.json, et enfin appeler send_file pour émettre la nouvelle version
```

### 3.4 Sortie dans le flux de conversation (send_file)

> **Intégral archivé R4** : `references/sortie-flux-send-file.md` (5,5 Kio — SHA-256 74cf8f157d02a6fc…) — règle send_file : chaque version générée impose un appel — paramètres par défaut et variantes mono/multi-fichiers (§3.4.1 et suivantes). Chargé à la demande (lecture ciblée E5-POIDS — jamais par défaut).

### 3.5 Cartes du flux de conversation et « Éditer à partir de cette version »

- **Versions historiques et dernière version** s'affichent de façon identique en haut de la zone d'aperçu (l'UI précise est implémentée par le front-end) ; l'Agent ne distingue pas deux protocoles d'aperçu
- **Chaque** carte de version produite par `send_file` dans le flux de conversation comporte un bouton « Éditer à partir de cette version » (implémenté par le front-end)
- Après le clic de l'utilisateur, la boîte de saisie est préremplie avec : **« Éditer à partir de la version V{n} de « {nom-projet} » »** (ex. `Éditer à partir de la version V2 de « site-voyage-pekin »` ; numéro de version en `V` majuscule + chiffres, cohérent avec `send_file.version`)
- À la réception de ce format par l'Agent → traiter selon le **flux de fusion** du §4 (dans le texte, `V{n}` devient `TARGET_TAG=v{n}`)
- Les cartes **dernière version et versions historiques** affichent toutes ce bouton ; barre supérieure de la zone d'aperçu au style identique (implémentée par le front-end, aucune action supplémentaire de l'Agent)

> **Remarque :** pas de capacité « liste des versions » dédiée ; l'utilisateur désigne la version via les cartes historiques du flux de conversation ou en langage naturel.

---

## 4. Restauration de version

### 4.1 Périmètre de restauration

La restauration est celle de **l'état complet du répertoire projet** (fichiers de code + ressources `assets/` + produits `export/`). `git checkout` restaure l'arbre de travail complet de la version cible, ce qui garantit que la version restaurée soit prévisualisable intégralement.

### 4.2 Points d'entrée de restauration

Pas de bouton front-end « Restaurer » dédié. La restauration se déclenche par les moyens suivants :

| Point d'entrée | Description |
|------|------|
| Langage naturel « restaurer vers V2 » | l'Agent exécute directement la restauration standard du §4.3 |
| Langage naturel « à partir de V2, changer le style » | l'Agent exécute le flux de fusion §4.4 (restauration + édition = une version) |
| Bouton « Éditer à partir de cette version » d'une carte du flux de conversation | boîte de saisie préremplie « Éditer à partir de la version V{n} de « {nom-projet} » » → envoi par l'utilisateur → traitement par l'Agent selon le flux de fusion §4.4 |
| Commentaire / édition de paramètres (dans l'aperçu d'une version historique) | l'instruction MD contient un numéro de version historique → traitement par l'Agent selon le flux de fusion §4.4 |

### 4.3 Restauration standard (restauration seule, sans édition)

Restaurer = checkout + commit d'une nouvelle version + send_file : les trois étapes sont indispensables. Un simple checkout ne compte pas comme restauration achevée.
Commandes à exécuter :

```bash
cd mes-projets/{nom-projet}
TARGET_TAG="v{version-cible}"
LATEST_TAG=$(git tag --sort=-v:refname | head -n 1)
NEXT_NUM=$((${LATEST_TAG#v} + 1))
NEXT_TAG="v${NEXT_NUM}"
git checkout $TARGET_TAG -- .
git add .
git commit -m "V${NEXT_NUM}: restauration vers V{version-cible}"
git tag $NEXT_TAG
# ↑ tout ce qui précède doit être exécuté intégralement, puis mettre à jour meta.json, et enfin appeler send_file pour émettre la nouvelle version
```

**Compréhension de l'état après restauration :** la référence est l'ensemble des fichiers du workspace (code + `assets/` + `export/`) + `meta.json` ; ne pas dépendre d'un service de versions back-end ni d'une relecture de la conversation passée.

Après restauration, l'Agent confirme à l'utilisateur :
- le nom du projet courant et le nouveau numéro de version
- les fichiers/pages inclus
- les différences par rapport à l'état précédant la restauration (ex. « ne contient pas le module de recommandations gourmandes, ajouté dans la V3 »)
- l'appel à `send_file` émettant l'entrée principale de la nouvelle version (paramètres identiques au §3.4).

La numérotation des versions est toujours croissante (restauration de V4 vers V2 → produit V5). Les versions existantes sont conservées.

### 4.4 Flux fusionné restauration + édition (une seule version produite)

S'applique à : l'utilisateur demande d'éditer à partir d'une version historique (y compris « Éditer à partir de la version V{n} de « {nom-projet} » »).

**Règle de numérotation :** quelle que soit la version historique de base, le nouveau numéro de version **doit** être l'incrément purement numérique de la dernière version courante +1 (ex. V8 courant → nouvelle version V9). **Interdit** d'utiliser des numéros de version avec suffixe (ex. `V4-light`, `V4-dark`, `V2-new` etc.), interdit de nommer avec la version de base en préfixe. **Interdit** d'écraser, déplacer ou supprimer le tag d'une version existante — les versions existantes sont conservées pour toujours, les nouvelles versions ne peuvent qu'être ajoutées.

Commandes à exécuter :
```bash
cd mes-projets/{nom-projet}
TARGET_TAG="v{version-cible}"
git checkout $TARGET_TAG -- .
# ↓ exécuter sur cette base l'édition demandée par l'utilisateur (modification du contenu des fichiers), sans commit intermédiaire
LATEST_TAG=$(git tag --sort=-v:refname | head -n 1)
NEXT_NUM=$((${LATEST_TAG#v} + 1))
NEXT_TAG="v${NEXT_NUM}"
git add .
git commit -m "V${NEXT_NUM}: à partir de V{version-cible} : {resume-des-modifications}"
git tag $NEXT_TAG
# ↑ tout ce qui précède doit être exécuté intégralement, puis mettre à jour meta.json, et enfin appeler send_file pour émettre la nouvelle version
```

---

## 5. Structure de meta.json

> **Intégral archivé R4** : `references/structure-meta-json.md` (1,6 Kio — SHA-256 d06c2214e34a6b46…) — exemplaire unique par projet, exclu du dépôt git (.gitignore) — schéma complet des champs de l'état global du projet. Chargé à la demande (lecture ciblée E5-POIDS — jamais par défaut).

## 6. Aide-mémoire des opérations

> **Intégral archivé R4** : `references/aide-memoire-operations.md` (3,0 Kio — SHA-256 4883fbee1cdac522…) — table « Action utilisateur → Opération exécutée » pour tous les cas (création, édition, restauration, multi-projets). Chargé à la demande (lecture ciblée E5-POIDS — jamais par défaut).

## 7. Annexe : prévisualisation et chemins (référence Agent)

- **Dans le workspace :** le HTML utilise des chemins relatifs comme `assets/xxx.png` ; dans les projets multi-fichiers, `link` / `script` référencent en chemins relatifs les fichiers de code du même répertoire ou de sous-répertoires
- **À la prévisualisation utilisateur :** le back-end résout les chemins absolus sur la machine cloud et les remplace par des liens OSS ; l'Agent **ne doit pas** écrire d'URL OSS dans le code source
- **Périmètre de suivi Git :** fichiers de code + ressources `assets/` + produits `export/` entrent tous dans Git ; `meta.json` et `style-samples*.html` sont exclus par `.gitignore`
- **Limitations connues :** prévisualisation JS/CSS des projets multi-fichiers et aperçu des versions historiques incohérent avec la dernière version — voir §0.1, non corrigé dans cette phase

---

## 8. Résorption structurelle — neutralisation résiliente (Task 69)

> **Intégral archivé R4** : `references/resorption-structurelle.md` (2,2 Kio — SHA-256 f95dc63abd7c5fb0…) — diagnostic consolidé Task 69 (32 incidents : disparition entre les tours par processus externe) et mécanisme de neutralisation résiliente. Chargé à la demande (lecture ciblée E5-POIDS — jamais par défaut).

## Baseline A2 — statut de mesure
> **Baseline A2 (Task 21 P3/F3, 2026-10-03)** : MESURÉE 2 voies (voie mécanique SHARED §7 v2 + voie L 3 runs réels) — score baseline 3/8 (nulls : 2) ; détail par cas : `scripts/baseline-a2-all-report.json` ; cas structurels consignés au registre KB (décision Task 21) ; re-mesure idempotente `--skip-done` armée pour les nulls 429 restants.
