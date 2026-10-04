---
name: version-management
version: "1.2.0"
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

## §0 — Contexte Système (SHARED v1.6.4)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (exception)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.

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

**Tous les fichiers web_project doivent être enregistrés sous `mes-projets/{nom-projet}/`. Interdit de les enregistrer à la racine du workspace, sur le Desktop, dans un répertoire temporaire, ou de se contenter de coller le code.**

La pratique privilégiée est la **prévention** plutôt que le rattrapage : conformément à la « ⚠️ Règle absolue des chemins » en tête de fichier, créer le répertoire projet et écrire directement dedans avant le premier fichier. Les contrôles ci-dessous constituent le **dernier verrou** avant commit / `send_file` :

1. **Avant écriture** : créer les répertoires conformément à la règle absolue en tête et écrire directement au bon endroit
2. **Avant commit / send_file** : exécuter le script de verrou ci-dessous ; fichiers égarés détectés → **obligation de `mv` vers le répertoire projet d'abord**, puis revalidation avant de continuer
3. **Règle de génération du nom de projet** : générer automatiquement un nom de projet sémantique en français ou en anglais d'après l'intention de l'utilisateur et le thème du contenu (ex. `site-voyage-pekin`, `backoffice-clients-entreprise`)

```bash
# Verrou des chemins avant commit (à exécuter à la racine du workspace)
cd {racine-workspace}

# (a) le répertoire projet doit contenir au moins un fichier d'entrée (pas seulement index.html ; prototype.html etc. valent aussi)
ls "mes-projets/{nom-projet}/"*.html "mes-projets/{nom-projet}/"*.jsx \
   "mes-projets/{nom-projet}/"*.tsx "mes-projets/{nom-projet}/"*.vue 2>/dev/null | grep -q . \
  || { echo "ERROR: aucun fichier d'entrée dans mes-projets/{nom-projet}/, commit / send_file interdits"; }

# (b) aucun fichier d'entrée ne doit traîner à la racine du workspace ni ailleurs
find . -maxdepth 2 -not -path "./mes-projets/*" \
  \( -name '*.html' -o -name '*.jsx' -o -name '*.tsx' -o -name '*.vue' \) \
  | while read -r f; do
      echo "STRAY: $f → exécuter mv \"$f\" \"mes-projets/{nom-projet}/\" puis revalider"
    done
```

Tout ERROR / STRAY → **interdiction** de commit et de `send_file` ; corriger d'abord les chemins puis relancer le verrou.

### 1.3 Règles de structure des fichiers

**Principe central : le répertoire projet est auto-contenu ; tous les fichiers (code + ressources + produits d'export) sont suivis par Git.**

- **Mono-fichier vs multi-fichiers :** ni mono-fichier imposé (JS/CSS inlinés), ni multi-fichiers systématique. À juger selon la complexité du projet :
  - landing page simple, H5, page vitrine unique → mono-fichier `index.html` possible
  - styles/scripts à réutiliser, composants nombreux → multi-fichiers possible (ex. `index.html` + `style.css` + `main.js`)
- **Point de chute des uploads utilisateur :** `upload/` ; unique répertoire de ressources dans le projet : `mes-projets/{nom-projet}/assets/`
- Références en **chemin relatif** dans le code : `assets/{nom-fichier}` ; interdit de référencer des chemins `upload/` (à la prévisualisation, le back-end remplace les chemins relatifs par des liens OSS ; l'Agent n'a aucune adresse OSS à écrire à la main)
- Ressources nommées en anglais sémantique (ex. `hero-banner.png`), éviter le chinois et les espaces
- `assets/` **est suivi par Git** — le snapshot de chaque version embarque toutes les ressources du moment ; lors de la restauration d'une version historique, code et ressources reviennent ensemble, ce qui garantit la prévisualisation complète de toute version passée

#### Traitement des ressources (upload → assets, obligatoire)

**Interdit** d'écrire `assets/xxx` dans le HTML sans fichier correspondant sur disque (cause fréquente d'images cassées : chemin écrit sans copie depuis `upload/`).

1. Trouver le fichier source dans `upload/` (chemins des pièces jointes des messages, `find upload`, `ls -lt upload` pour les uploads les plus récents)
2. `mkdir -p mes-projets/{nom-projet}/assets`
3. `cp upload/{source} mes-projets/{nom-projet}/assets/{nom}` — `{nom}` **strictement identique** au `assets/{nom}` référencé dans le HTML (si le HTML est déjà écrit, copier/renommer selon le nom référencé)
4. Écrire/modifier ensuite les références HTML ; copier image par image
5. **Vérification avant commit** (présence de MISSING : commit / send_file interdits) :

```bash
cd mes-projets/{nom-projet}
grep -ohE 'assets/[a-zA-Z0-9_.-]+' index.html 2>/dev/null | sort -u | while read -r ref; do
  [ -f "$ref" ] || echo "MISSING: $ref"
done
```

6. Sans MISSING, créer la version selon §3 puis `send_file`

#### Origine des ressources (trois cas, mêmes règles de dépôt)

| Origine | Ordre typique | Action de l'Agent | Nouvelle version ? |
|------|----------|------------|------------|
| **Upload utilisateur** | HTML d'abord puis images / images d'abord puis HTML | `cp` de `upload/` vers `assets/`, référence cohérente avec le nom de fichier ; images envoyées après : nommer d'après les références HTML existantes | cp seul, code inchangé → ❌ ; références HTML modifiées → ✅ |
| **Recherche d'images par l'Agent** | l'utilisateur veut des illustrations, l'Agent les cherche en ligne | télécharger vers `assets/{nom}` (interdit d'écrire seulement une URL externe) ; puis écrire/modifier les références HTML | ✅ |
| **Génération d'images par l'Agent** | l'utilisateur veut des illustrations, l'Agent les génère | écrire dans `assets/{nom}` (interdit d'écrire `assets/xxx` sans dépôt sur disque) ; puis écrire le HTML | ✅ |

**Commun aux trois cas :** tout HTML contenant des références `assets/` impose la vérification ci-dessus avant commit ; fichier absent → déposer le fichier ou modifier la référence, commit avec MISSING interdit.
**HTML d'abord, sans image :** textes/styles de substitution admis, mais **ne pas** écrire un `assets/xxx` inexistant ; une fois l'image fournie par l'utilisateur ou complétée par l'Agent, écrire la référence réelle et faire le cp.

#### Conservation des images utilisateur entre les versions (important)

Pour les images déjà uploadées et référencées dans `assets/`, lorsque les éditions ultérieures par **langage naturel / commentaires / éditeur de paramètres** produisent une nouvelle version :

- L'utilisateur n'a **pas** demandé de retirer le module ni de changer l'image → **conserver obligatoirement** les fichiers `assets/` d'origine et les références `assets/...` du HTML ; ne pas supprimer, ne pas changer les chemins, ne pas demander de re-upload
- Modifications limitées au style, aux textes, à la mise en page etc. → ne toucher que les fichiers de code, sans toucher à `assets/` (sauf demande explicite de remplacement des ressources)
- `git add .` inclut automatiquement les fichiers `assets/` inchangés dans le snapshot de la nouvelle version (Git réutilise automatiquement les fichiers non modifiés, sans stockage dupliqué) ; aucun traitement manuel nécessaire

#### Règles de conservation des maquettes (style samples)

S'il existe une phase de maquettes avant la construction officielle (le modèle produit d'abord un HTML contenant plusieurs directions de design numérotées à faire choisir à l'utilisateur), le HTML de maquettes doit être déplacé sous `mes-projets/{nom-projet}/` et nommé `style-samples.html` ; si l'utilisateur n'est pas satisfait et demande de nouvelles directions, les tours suivants s'incrémentent en `style-samples-2.html`, `style-samples-3.html`, interdiction d'écraser une maquette existante. Interdit de nommer une maquette `index.html` ou tout autre nom de fichier d'entrée. Les maquettes sont émises via `send_file` pour la prévisualisation et le choix de l'utilisateur. `style-samples*.html` est déjà exclu par wildcard dans `.gitignore` : pas d'historique Git, pas de comptage dans la numérotation des versions du projet. Interdit de supprimer les fichiers/dossiers sources des maquettes avant leur dépôt dans le répertoire projet.

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

| Point d'entrée d'édition | Projet | Version |
|---------|------|------|
| Édition par commentaire (instruction écrite sur l'élément sélectionné dans la zone d'aperçu) | l'instruction MD contient le nom du projet | l'instruction MD contient le numéro de version (celui de l'aperçu) |
| Éditeur de paramètres (bouton d'édition de la zone d'aperçu) | l'instruction MD contient le nom du projet | l'instruction MD contient le numéro de version (celui de l'aperçu) |
| Langage naturel (saisie dans la boîte de dialogue) | voir les règles ci-dessous | voir les règles ci-dessous |
| Carte du flux de conversation « Éditer à partir de cette version » | projet correspondant à la carte | version correspondant à la carte (passe par le flux de fusion §4) |

**Défaut en langage naturel : éditer la dernière version du projet le plus récent.**

Détermination du projet : selon les priorités du §2 (nom désigné par l'utilisateur > contexte front-end > dernière opération > question posée).

Détermination de la version :

| Scénario | Traitement |
|------|----------|
| L'utilisateur désigne explicitement une version (ex. « à partir de V2, modifier le titre », ou boîte de saisie préremplie « Éditer à partir de la version V2 de « {nom-projet} » ») | suivre la version désignée → flux de fusion §4 |
| L'utilisateur désigne un projet sans désigner de version | dernière version de ce projet |
| Autres cas | par défaut : dernière version du projet le plus récent |

Pas de question supplémentaire. Toutes les versions sont restaurables ; une édition par mégarde d'une version non prévue se corrige par une restauration.

#### Règles de traitement des éditions par commentaire et par l'éditeur de paramètres

Après une édition par commentaire ou par l'éditeur de paramètres dans la zone d'aperçu (y compris l'aperçu d'une version historique), le front-end génère une instruction MD envoyée à l'Agent. L'instruction MD contient le **nom du projet** et le **numéro de version** ; l'Agent applique les règles suivantes :

1. Extraire le nom du projet de l'instruction MD → localiser `mes-projets/{nom-projet}/`
2. Extraire le numéro de version de l'instruction MD → obtenir `V{n}`
3. Lire le `latest_version` du `meta.json` du projet et déterminer la relation entre versions :
   - **Version désignée = dernière version** → éditer directement dans le workspace courant → créer une nouvelle version selon §3.3
   - **Version désignée ≠ dernière version (version historique)** → **obligation** d'exécuter le flux de fusion §4.4 (restaurer d'abord la version désignée avec `git checkout v{n} -- .`, puis appliquer l'édition, enfin un seul commit en nouvelle version). **Interdit de sauter l'étape de restauration** ; aussi minime que l'Agent estime l'écart entre la version courante et la version cible, il doit restaurer strictement avant de modifier.
4. Rechercher les correspondances par ancres dans tous les fichiers HTML du répertoire projet, localiser l'élément cible et appliquer la modification
5. Une fois terminé : créer la version avec les commandes git du §3.3 / §4.4 + mettre à jour `meta.json` + `send_file`

> **Le template MD est maintenu par le front-end.** Ce Skill ne définit pas le format MD précis ; il suffit qu'il contienne le nom du projet, le numéro de version, les ancres et les modifications pour être parsable par l'Agent.

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

Chaque nouvelle version générée impose un appel à `send_file`.

#### 3.4.1 Règle par défaut : projet à fichier d'entrée unique

| Paramètre | Valeur |
|------|-----|
| `ext` | toujours `web_project` |
| `title` | nom du projet, ex. `site-voyage-pekin` ; **ne pas** y inclure le numéro de version (le front-end le concatène via le champ `version`) ; en aucun cas le nom d'un fichier précis (index, main etc.) |
| `file_path` | chemin complet du fichier d'entrée principal du projet, ex. `/mes-projets/site-voyage-pekin/index.html` |
| `project_name` | identique au `project_name` de `meta.json` |
| `version` | numéro de la version en cours, ex. `V3` |

Exemple d'appel :
```json
{"title": "site-voyage-pekin", "ext": "web_project", "file_path": "/mes-projets/site-voyage-pekin/index.html", "project_name": "site-voyage-pekin", "version": "V3"}
```

#### 3.4.2 Projets multi-fichiers d'entrée (règle ajoutée)

Quand le projet contient **plusieurs fichiers d'entrée HTML indépendants** (ex. `index.html` + `light.html`, ou plusieurs pages) :

1. **Tous les fichiers d'entrée doivent être commités dans le même commit** (`git add .` les inclut naturellement tous)
2. **Stratégie send_file :**
   - S'il n'y a qu'**une entrée principale** (les autres étant auxiliaires), n'émettre par défaut que l'entrée principale
   - Si le Skill appelant exige explicitement l'émission de plusieurs fichiers (ex. double fichier prototype), suivre la demande de l'appelant
   - Aucun oubli toléré : tous les fichiers HTML doivent être suivis par git
3. **Interdit** d'appeler `ext=directory` sur le répertoire projet pour émettre un dossier

Exemple (`index.html` entrée principale, `light.html` variante ajoutée) :
```bash
# le même commit contient les deux fichiers
git add index.html light.html assets/
git commit -m "V4: ajout de la variante de thème light"
git tag v4
```

send_file n'émet que l'entrée principale :
```json
{"title": "site-voyage-pekin", "ext": "web_project", "file_path": "/mes-projets/site-voyage-pekin/index.html", "project_name": "site-voyage-pekin", "version": "V4"}
```

#### 3.4.3 Livraison prototype en double fichier (règle stable)

Quand le Skill appelant est `prototype.md` et que la version contient les deux fichiers de livraison (prototype interactif + document de flux) :

1. **Périmètre de la version (obligatoire)**
   La version doit inclure et commiter les deux fichiers HTML (en général `prototype.html` et `flow.html`) ; commiter un seul des deux est interdit.
2. **Sortie dans le flux de conversation (obligatoire)**
   Appeler `send_file` **deux fois** pour le même numéro de version, en émettant chacun des deux fichiers :
   - Premier appel : `prototype.html`
   - Second appel : `flow.html`
3. **Nommage suggéré des cartes**
   Indiquer le rôle du fichier dans `title` pour que l'utilisateur les distingue (title sans numéro de version) :
   - `{nom-projet}-prototype`
   - `{nom-projet}-flow`
4. **Interdictions**
   - Interdit d'empaqueter `prototype.html + flow.html` en un dossier pour une émission unique
   - Interdit de n'émettre qu'un seul des deux fichiers en prétendant avoir réalisé la double livraison prototype

Exemple (même version V4, deux appels successifs) :
```json
{"title":"backoffice-clients-entreprise-prototype","ext":"web_project","file_path":"/mes-projets/backoffice-clients-entreprise/prototype.html","project_name":"backoffice-clients-entreprise","version":"V4"}
{"title":"backoffice-clients-entreprise-flow","ext":"web_project","file_path":"/mes-projets/backoffice-clients-entreprise/flow.html","project_name":"backoffice-clients-entreprise","version":"V4"}
```

#### 3.4.4 Projets à export d'images fixes (cartes Xiaohongshu etc., règle ajoutée)

Pour les scénarios de cible de sortie `fixed-image` (cartes Xiaohongshu, images de couverture, images longues etc.), le flux typique est :

1. **Générer d'abord le HTML** (produit de la phase de conception) → l'enregistrer comme d'habitude sous `mes-projets/{nom-projet}/`
2. **Exécuter ensuite l'export** des images → enregistrer les produits d'export sous `mes-projets/{nom-projet}/export/`
3. **Gestion de versions :** le HTML et `export/` sont tous deux suivis par Git, dans le même commit
4. **Stratégie send_file (obligatoire) :**
   - **Premier appel :** émettre le fichier HTML (`ext: web_project`)
   - **Second appel :** émettre le produit d'export
     - Export d'une seule image : `ext: extension précise` (ex. `png`, `jpg`), `file_path: /mes-projets/{nom-projet}/export/xxx.png`
     - Export d'un dossier (plusieurs images) : `ext: directory`, `file_path: /mes-projets/{nom-projet}/export/`

**Règles clés :**
- Le HTML et les produits d'export **doivent se trouver dans le même répertoire projet**
- Les deux **doivent figurer dans la même version (commit)**
- Interdit de laisser des produits d'export dispersés hors du répertoire projet

Exemple (projet d'image longue Xiaohongshu, V2) :
```bash
# structure du répertoire projet
cd mes-projets/guide-voyage-xiaohongshu
git add .
git commit -m "V2: optimisation des couleurs de couverture et de la mise en page"
git tag v2
```

Appels send_file (deux appels successifs) :
```json
{"title":"guide-voyage-xiaohongshu","ext":"web_project","file_path":"/mes-projets/guide-voyage-xiaohongshu/index.html","project_name":"guide-voyage-xiaohongshu","version":"V2"}
{"title":"guide-voyage-xiaohongshu-export","ext":"directory","file_path":"/mes-projets/guide-voyage-xiaohongshu/export/"}
```

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

Un exemplaire par projet, il consigne l'état global du projet. Exclu via `.gitignore`, il n'entre pas dans l'historique des versions.

```json
{
  "project_name": "site-voyage-pekin",
  "latest_version": "v3",
  "is_published": false,
  "published_version": null,
  "domain": null,
  "versions": [
    {
      "id": "v1",
      "timestamp": "2026-05-01T14:30:00+08:00",
      "based_on": null,
      "summary": "accueil + liste des sites touristiques"
    },
    {
      "id": "v2",
      "timestamp": "2026-05-05T10:30:00+08:00",
      "based_on": null,
      "summary": "changement de style vers l'International"
    },
    {
      "id": "v3",
      "timestamp": "2026-05-06T14:30:00+08:00",
      "based_on": "v1",
      "summary": "à partir de V1 : refonte de la mise en page"
    }
  ]
}
```

| Champ | Type | Description |
|------|------|------|
| project_name | string | nom du projet, généré automatiquement par l'Agent, modifiable par l'utilisateur |
| latest_version | string | numéro de la dernière version courante (ex. "v5") |
| is_published / published_version / domain | phase 1 : par défaut false / null |
| versions[].id | string | numéro de version (ex. "v1") |
| versions[].timestamp | string | horodatage de création (ISO 8601 avec fuseau horaire) |
| versions[].based_on | string \| null | renseigné uniquement en cas de restauration ou d'édition à partir d'une version historique, pointe vers la version de base ; null pour une édition ordinaire |
| versions[].summary | string | résumé du changement en une phrase, généré automatiquement par l'Agent |

---

## 6. Aide-mémoire des opérations

| Action utilisateur | Opération exécutée |
|--------|--------|
| « Faire un site XX » | **créer d'abord** `mes-projets/{nom-projet}/` → générer les fichiers dans le répertoire → création §1 (git init + V1) → `send_file` |
| « Faire un prototype produit » | **créer d'abord** le répertoire projet → générer `prototype.html` + `flow.html` dans le répertoire → commit dans la même version (les deux fichiers suivis par Git) → deux `send_file` successifs selon §3.4.3 |
| « Agrandir un peu le titre » (sans contexte particulier) | éditer la dernière version du projet le plus récent → commandes de création de version §3.3 → `send_file` |
| « Ajouter un thème light au projet existant » | générer `light.html` → même commit que les fichiers existants → `send_file` émettant l'entrée principale |
| « À partir de V2, modifier le titre » / préremplissage « Éditer à partir de la version V2 de « {nom-projet} » » | flux de fusion §4 → `send_file` |
| Commentaire / édition de paramètres | extraire nom de projet + numéro de version de l'instruction MD → selon les règles de traitement du §3.1, passer par §3.3 ou §4.4 → `send_file` |
| Upload d'images par l'utilisateur (`upload/`) | `cp` → `assets/` → alignement sur le HTML → vérification §1 → si le code change : §3.3 |
| HTML d'abord, images ensuite | `cp` selon les noms référencés dans le HTML ; pas de commit si le code est inchangé, nouvelle version si les références changent |
| L'Agent cherche/génère des images pour remplir le site | télécharger ou écrire dans `assets/` → écrire les références → vérification §1 → §3.3 |
| Upload seulement, sans changement de code | écriture dans `assets/` seulement, pas de commit |
| Modification de style sans demande de changement d'image ni suppression de module | modifier le code, **conserver les références et fichiers assets** → §3.3 → `send_file` |
| « Restaurer vers V2 » | restauration standard §4 (code + assets reviennent ensemble) → `send_file` |
| Clic sur la carte « Éditer à partir de cette version » | l'utilisateur envoie le texte prérempli → fusion §4 → `send_file` |
| En langage naturel : « publier » / « dépublier » | orienter l'utilisateur vers le bouton de publication du front-end (non implémenté en phase 1) |
| « Rédige-moi une proposition » | ne déclenche pas la gestion de versions |
| Référence ambiguë | scanner `mes-projets/` → poser la question |
| Cartes Xiaohongshu / image de couverture | générer le HTML → enregistrer dans le projet → export vers `export/` → même commit → `send_file` du HTML + `send_file` de l'export |
| Phase de maquettes (« propose d'abord plusieurs directions ») | générer `style-samples.html` → enregistrer sous `mes-projets/{nom-projet}/` → émission via `send_file` → attendre le choix de direction de l'utilisateur → pas de commit, pas de comptage de version |

---

## 7. Annexe : prévisualisation et chemins (référence Agent)

- **Dans le workspace :** le HTML utilise des chemins relatifs comme `assets/xxx.png` ; dans les projets multi-fichiers, `link` / `script` référencent en chemins relatifs les fichiers de code du même répertoire ou de sous-répertoires
- **À la prévisualisation utilisateur :** le back-end résout les chemins absolus sur la machine cloud et les remplace par des liens OSS ; l'Agent **ne doit pas** écrire d'URL OSS dans le code source
- **Périmètre de suivi Git :** fichiers de code + ressources `assets/` + produits `export/` entrent tous dans Git ; `meta.json` et `style-samples*.html` sont exclus par `.gitignore`
- **Limitations connues :** prévisualisation JS/CSS des projets multi-fichiers et aperçu des versions historiques incohérent avec la dernière version — voir §0.1, non corrigé dans cette phase

---

## Baseline A2 — statut de mesure
> **Baseline A2 (Task 21 P3/F3, 2026-10-03)** : MESURÉE 2 voies (voie mécanique SHARED §7 v2 + voie L 3 runs réels) — score baseline 3/8 (nulls : 2) ; détail par cas : `scripts/baseline-a2-all-report.json` ; cas structurels consignés au registre KB (décision Task 21) ; re-mesure idempotente `--skip-done` armée pour les nulls 429 restants.
