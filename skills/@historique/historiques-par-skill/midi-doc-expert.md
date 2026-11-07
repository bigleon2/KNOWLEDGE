# Historique par skill — midi-doc-expert

> **Version** : 1.0.0 — **Date** : 2026-11-01 (Task 31, session web-4f989063 — directive propriétaire GO (a) trace 1a1975c9a4c7fa31 : inscription au dépôt)
> **Version vivante (corpus)** : v1.2.0 — `skills/midi-doc-expert/SKILL.md` (sa spécification fait foi)
> **Versions archivées** : 0 (aucune version antérieure au dépôt — le skill est né v1.0.0)
> **Provenance** : skill créé hors dépôt (sessions Traktor S4 MK3, installation hôte-seule) — inscrit au dépôt 2026-11-01 par copie host→repo BYTE-IDENTIQUE (lignage honnête, doctrine Task 27 : aucune revendication rétroactive, aucune réécriture)

## Famille MIDI-DOC-EXPERT — 3 versions (skill : midi-doc-expert)

**Rôle** : Skill de génération de documentation technique MIDI (tableaux de référence, états LED, annexes) — générateur déterministe generer-doc-midi.py (Markdown + JSON).

| Version | Date | Améliorations implantées | Avantage par rapport à la version précédente |
|---------|------|--------------------------|----------------------------------------------|
| v1.0.0 | 2026-11-01 | Version initiale (inscrite au dépôt Task 31) : SKILL.md + evals (evals.json + trigger_evals.json 6 cas — vetos croisés tandem Task 30) + bloc §0 SHARED v1.7.17 ; périmètres croisés encodés : validation = tsi-validator, documentation = midi-doc-expert, conception = tsi-architect | — (point de départ) |
| v1.1.0 | 2026-11-02 | Task 33 (GO initial P2, trace 1a197aaf0eb6557d) : conversion périmètre MK3→MK2, persona enrichi du cahier des charges, §0 re-normalisé | périmètre aligné sur le contrôleur réel du propriétaire |
| v1.2.0 | 2026-11-04 | Task 45 (session web-6058b3ba) : §5 rédigé par mode (Increment/Decrement = encodeur ; Toggle = commutation ; Direct = valeur absolue) ; §2 détection du bridge MIDI Controls (2 étages, IDs 850-873, looprituals 1-4 gauche / 5-8 droite) ; attribution Interaktiv Audio CC BY 4.0 ; JSON `generateur: v1.2.0` ; evals + gabarit + generer-doc-midi.py recalibrés | documentation du preset « MIDI Controls bridge » (Task 45) — modes et bridge expliqués mécaniquement |

Révisions documentaires de la famille (sans changement de version du skill) : Task 30 (2026-11-01, directive GO trace 1a197552459ad8f5) — recalibrage triggers (vetos croisés V6.1 sur les cas négatifs en dérive, replay hôte PASS 483/483) ; Task 31 (2026-11-01, directive GO trace 1a1975c9a4c7fa31) — inscription au dépôt + entrée KB + pin ECO_SKILLS. ; Task 33 (2026-11-02, GO initial P2/P5, trace 1a197aaf0eb6557d) — conversion périmètre MK2 + Task 33 cascade KB (byte-identité, entrée KB recalibrée) ; Task 45 (2026-11-04, session web-6058b3ba — installation profil local) — cascade KO-L004 complète (pin ECO_SKILLS 1.2.0, entrée KB v1.2.0, archive v2.3 rescellée round-trip).
Fichiers archivés de la famille : néant (0 fichier).
