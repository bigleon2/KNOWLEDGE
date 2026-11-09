# 3.4 Sortie dans le flux de conversation (send_file) — version-management (bloc archivé R4)

> **Provenance** : skill `version-management` v1.3.0 · section « 3.4 Sortie dans le flux de conversation (send_file) » · déplacé R4 byte-identité vers `references/` le 2026-11-08 (Task 79 G2, re-curation — protocole re-curation v1.0.0, méthode moves-r4-pur arbitrée --compare) · **SHA-256 du bloc : 74cf8f157d02a6fc628d4abb15a1aa2d53d973e7e0843e39dbbd819e7ea9f7a2**

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
