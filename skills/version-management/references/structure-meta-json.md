# 5. Structure de meta.json — version-management (bloc archivé R4)

> **Provenance** : skill `version-management` v1.3.0 · section « 5. Structure de meta.json » · déplacé R4 byte-identité vers `references/` le 2026-11-08 (Task 79 G2, re-curation — protocole re-curation v1.0.0, méthode moves-r4-pur arbitrée --compare) · **SHA-256 du bloc : d06c2214e34a6b463f24786e3739d4d9c09d46e915738d26da48ba5452c5027c**

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
