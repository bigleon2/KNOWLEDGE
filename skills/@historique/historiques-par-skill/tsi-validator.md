# Historique par skill — tsi-validator

> **Version** : 1.0.0 — **Date** : 2026-11-01 (Task 31, session web-4f989063 — directive propriétaire GO (a) trace 1a1975c9a4c7fa31 : inscription au dépôt)
> **Version vivante (corpus)** : v1.2.0 — `skills/tsi-validator/SKILL.md` (sa spécification fait foi)
> **Versions archivées** : 0 (aucune version antérieure au dépôt — le skill est né v1.0.0)
> **Provenance** : skill créé hors dépôt (sessions Traktor S4 MK3, installation hôte-seule) — inscrit au dépôt 2026-11-01 par copie host→repo BYTE-IDENTIQUE (lignage honnête, doctrine Task 27 : aucune revendication rétroactive, aucune réécriture)

## Famille TSI-VALIDATOR — 3 versions (skill : tsi-validator)

**Rôle** : Skill-arbitre de validation mécanique des mappings TSI — 8 contrôles E1-E8, verdict PASS/FAIL JSON, bras scripts/valider-tsi.py + golden samples.

| Version | Date | Améliorations implantées | Avantage par rapport à la version précédente |
|---------|------|--------------------------|----------------------------------------------|
| v1.0.0 | 2026-11-01 | Version initiale (inscrite au dépôt Task 31) : SKILL.md + evals (evals.json + trigger_evals.json 6 cas — vetos croisés tandem Task 30) + bloc §0 SHARED v1.7.17 ; périmètres croisés encodés : validation = tsi-validator, documentation = midi-doc-expert, conception = tsi-architect | — (point de départ) |
| v1.1.0 | 2026-11-02 | Task 33 (GO initial P2, trace 1a197aaf0eb6557d) : conversion périmètre MK2 (golden corroboré DJTT v2.1.0) ; constat interopérabilité E1 consigné (NISYSTEM vs NIXML réel — évolution bi-racine proposée sur GO), format réel couvert par analyse-doc-s4mk2 | périmètre aligné + écart de format documenté sans masquage |
| v1.2.0 | 2026-11-02 | Task 34 (GO traces 1a198688435d6bf1→1a198840319c3ec5, session web-4f989063) : évolution BI-RACINE E1 — pendante Task 33 n°1 résorbée : NISYSTEM (déclaratif, non-régression golden) + NIXML (réel Traktor : blob DIOM embarqué, magique, hiérarchie DEVS→…→DCBM, comptes E2, device E3 ; E4-E8 binaire délégués au moteur analyse-doc-s4mk2 — R4) ; self-test étendu (fixtures NIXML à la volée) | les TSI réels Traktor (DJTT v2.1.0, DREW) passent désormais le garde E1 directement : PASS [réel NIXML] |
| v1.3.1 | 2026-11-07 | Task 67 G4 (résorption F-67-2 — directive bloc n°3, 25 WARN coherence) : frontmatter dependencies += tsi-architect >= v1.2.0 (tandem — garde obligatoire avant toute livraison de mapping conçu), midi-doc-expert >= v1.2.0 (documentation aval — mapping à verdict PASS), multi-shift-architect >= v1.1.0 (règle E7 matérialise l'invariant de transitions complètes, I-3) ; alignement frontmatter ↔ KB ; PATCH addition pure | Les relations tandem/aval/E7 du validateur sont déclarées structurellement des deux côtés — le graphe KB de la famille TSI est bidirectionnel — **VERSION VIVANTE (skill installé)** |

Révisions documentaires de la famille (sans changement de version du skill) : Task 30 (2026-11-01, directive GO trace 1a197552459ad8f5) — recalibrage triggers (vetos croisés V6.1 sur les cas négatifs en dérive, replay hôte PASS 483/483) ; Task 31 (2026-11-01, directive GO trace 1a1975c9a4c7fa31) — inscription au dépôt + entrée KB + pin ECO_SKILLS. ; Task 33 (2026-11-02, GO initial P2/P5, trace 1a197aaf0eb6557d) — conversion périmètre MK2 + Task 33 cascade KB (byte-identité, entrée KB recalibrée).
Fichiers archivés de la famille : néant (0 fichier).
