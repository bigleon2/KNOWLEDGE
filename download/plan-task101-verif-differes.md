# Plan Task 101 — Vérification mécanique des différés consignés à corriger

> gen-plan mode step (v3.43.0) · Directive propriétaire trace `1a1dfbe7d6565fa5` : « vérifie $FACON qu'il n'y a plus de différés consignés à corriger et s'il en reste alors corrige $FACON »

## Contexte

Le dernier point d'état (Task 99, suite 144) consignait 4 items de pendance. Task 100 (GO trace `1a1dfb31d58350d5`) a éteint F1. La présente mission établit un verdict MÉCANIQUE ($FACON) sur l'ensemble des différés consignés, puis corrige les résidus correctables.

## Zones de vérification

- **Zone VIVANTE** : worklog (3 dernières suites) · dernier plan (plan-task100) · derniers rapports (rapport-cw-task99-bloc).
- **Zone HISTORIQUE (scellée — non éditable, R6)** : clones-chat, plans/rapports antérieurs → mentions = enregistrements datés, non items ouverts.
- **Zone CODE** : scripts/*.py et skills/*/SKILL.md — marqueurs TODO/FIXME/à corriger = candidats OPEN réels.

## Groupes

- **G1** État dépôt + reconnaissance zones (fait en amont — parité 2303 lignes, HEAD `dd6afc7d`).
- **G2** Scanner mécanique `scripts/task101-scan-differes.py` (stdlib, selftest embarqué, rapport JSON déterministe sans horloge) : marqueurs [Pp]endance / différé / [FUTURE] / à corriger / reste à faire / EN ATTENTE / TODO / FIXME / mission dédiée / reporté → classification OPEN / RÉSORBÉ / PROPRIÉTAIRE / AUTO / PROPOSITION / HISTORIQUE.
- **G3** Adjudication des candidats OPEN + corrections $FACON si résidus correctables.
- **G4** Arbitres re-jeu (si modifications) + worklog suite 146 + parité hôte↔dépôt + COMMIT local SANS PUSH (0 PAT fourni ce tour — 0 exposition, recalibrage E15).
- **G5** Rapport final au chat (français, règle d'or n°6).

## Answer key (vérifiables mécaniquement)

- **D001** : scanner selftest PASS (cas synthétiques OPEN/RÉSORBÉ/PROPRIÉTAIRE/AUTO/HISTORIQUE).
- **D002** : rapport JSON `download/task101-differes-report.json` déterministe (sans horloge), rc=0.
- **D003** : verdict global explicite : soit « 0 différé correctable restant », soit liste des corrections appliquées avec preuves.
- **D004** : si corrections → arbitres ALL PASS avant commit ; sinon arbitres non requis (0 fichier modifié).
- **D005** : worklog suite 146, parité hôte↔dépôt vérifiée md5.
- **D006** : commit local « Task 101 CLOSE », 0 exposition (no push sans PAT frais).

## Routage

[gen-plan] · couche scripts/ + .md · KO-L009 (aucun jeton fourni ni utilisé) · règle d'or n°6 (sorties françaises).
