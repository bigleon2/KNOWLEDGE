# @historique/photos/ — Archive des versions supplantées des PMs @photos

> Créé Task 48 (G3, session web-38713acd, 2026-10-21) — convention R4 : byte-identité
> prouvée contre les blobs git du dépôt (colonne « commit source ») ; les versions
> supplantées ne sont JAMAIS réinstallées (garde R2 KO-L003) et ne servent que de
> référence documentaire. Les PMs courants vivent dans `skills/@photos/`.

| Fichier archivé | Version | Commit source (byte-identité) | SHA-256 (16) | Rôle |
|---|---|---|---|---|
| `iphone17-photos-v2.0.md` | 2.0 | e62f354 | `6b2846fdda56d32a` | v2.0 — génération 17 (ARCHIVÉE au plan générationnel ; supplantée par v2.1 extension 1944 le 2026-10-21) |
| `iphone18-photos-v1.0.md` | 1.0 | e62f354 | `2887e9e3e8cbb5b0` | v1.0 — génération 18 CONFIRMÉE (supplantée par v1.1 extension 1944 le 2026-10-21) |
| `iphone19-photos-v0.9.0.md` | 0.9.0 | e62f354 | `fa5ad5ddf215e95e` | v0.9.0 — migration ANTICIPÉE (supplantée par v0.10.0 pixel binning le 2026-10-21) |
| `iphone19-photos-v0.10.0.md` | 0.10.0 | 29e2de1 | `bb9671fcc4b5fc51` | v0.10.0 — émulation pixel binning R19 (supplantée par v0.11.0 extension 1944 le 2026-10-21) |

Règle : toute évolution d'un PM @photos = bump versionné dans le fichier vivant
(changelog + note rétroactive §11 + auto-audit) + archivage de la version supplantée
ici (extraction git byte-identique + scellement SHA-256) + mise à jour de la table §2
du README @photos et du présent index.
