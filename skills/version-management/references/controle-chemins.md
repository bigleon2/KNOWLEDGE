# 1.2 Contrôle obligatoire des chemins (règle critique) — version-management (bloc archivé R4)

> **Provenance** : skill `version-management` v1.3.0 · section « 1.2 Contrôle obligatoire des chemins (règle critique) » · déplacé R4 byte-identité vers `references/` le 2026-11-08 (Task 79 G2, re-curation — protocole re-curation v1.0.0, méthode moves-r4-pur arbitrée --compare) · **SHA-256 du bloc : 088a88871dcdb0fc978b6ad006b230ef730527a982280ef27bfb005aac46105e**

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
