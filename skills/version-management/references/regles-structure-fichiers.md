# 1.3 Règles de structure des fichiers — version-management (bloc archivé R4)

> **Provenance** : skill `version-management` v1.3.0 · section « 1.3 Règles de structure des fichiers » · déplacé R4 byte-identité vers `references/` le 2026-11-08 (Task 79 G2, re-curation — protocole re-curation v1.0.0, méthode moves-r4-pur arbitrée --compare) · **SHA-256 du bloc : f31e059e63371a80473116277e563211641dd82a1807676197a7ef17e5e475c1**

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
