# 6. Aide-mémoire des opérations — version-management (bloc archivé R4)

> **Provenance** : skill `version-management` v1.3.0 · section « 6. Aide-mémoire des opérations » · déplacé R4 byte-identité vers `references/` le 2026-11-08 (Task 79 G2, re-curation — protocole re-curation v1.0.0, méthode moves-r4-pur arbitrée --compare) · **SHA-256 du bloc : 4883fbee1cdac52205f65a4d81d33475977b392bc6752542cf49be294a3a38d2**

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
