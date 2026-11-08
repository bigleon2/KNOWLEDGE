# 8. Résorption structurelle — neutralisation résiliente (Task 69) — version-management (bloc archivé R4)

> **Provenance** : skill `version-management` v1.3.0 · section « 8. Résorption structurelle — neutralisation résiliente (Task 69) » · déplacé R4 byte-identité vers `references/` le 2026-11-08 (Task 79 G2, re-curation — protocole re-curation v1.0.0, méthode moves-r4-pur arbitrée --compare) · **SHA-256 du bloc : f95dc63abd7c5fb0c8ee73de899105f0430c47b5129c4f11e347b1396a58a288**

## 8. Résorption structurelle — neutralisation résiliente (Task 69)

> **Diagnostic consolidé (Task 69, directive n°8 item 1 — 32 incidents documentés)** : la
> disparition de ce skill survient ENTRE LES TOURS, par un processus EXTERNE au projet (ni
> cron ni process local) ; le dépôt git hôte reçoit des commits automatiques à messages UUID
> (snapshots plateforme) aux frontières de tours ; corrélation temporelle exacte entre
> interruptions utilisateur et disparitions (clarification propriétaire : « je te t'arrête
> souvent pour affiner mes requêtes »). **La prévention est impossible → la résorption est
> une NEUTRALISATION RÉSILIENTE à 4 composantes** :
>
> | Composante | Mécanisme | État |
> |---|---|---|
> | (a) Watchdog battements de cœur | `scripts/vm-watchdog.py` — détecte SON PROPRE temps d'arrêt (écart heartbeat > seuil 180 s = fenêtre de disparition potentielle) ; modes `--once` / `--daemon` / `--selftest` (harnais 8 tests en répertoire temporaire) / `--init` ; réparation déterministe via la garde | **v1.3.0 — nouveau** |
> | (b) Journal forensique horodaté | `tmp/vm-watchdog/journal-forensique.jsonl` — événements INIT / INCIDENT_DOCUMENTE (backfill qualifié des 32 incidents) / DEMARRAGE / ECART / DISPARITION_DETECTEE / REPARATION / RETABLIE / VERIF_OK / ARRET ; heads hôte + miroir consignés à chaque événement (corrélation mécanique avec les interruptions) | **v1.3.0 — nouveau** |
> | (c) Garde à l'invocation | `skills/gen-plan/scripts/ensure-installed.py` (hook É1-INSTALL, Task 56) — INSTALLE-REPARÉ rc=0 depuis le miroir local ; AUCUN doublon (R4 jamais dupliquer) | préexistante, intégrée |
> | (d) Persistance disque | miroir `KNOWLEDGE-repo` (règle d'or n°5 — le disque fait foi) | préexistante, intégrée |
>
> **Usage** : `python3 skills/version-management/scripts/vm-watchdog.py --once` (un cycle) ·
> `--daemon` (heartbeat permanent, défaut 30 s) · `--init` (initialise le journal — no-op
> idempotent si présent) · `--selftest` (8 tests mécaniques sans effet sur l'écosystème).
> Toute réparation déclenchée par le watchdog doit être suivie d'une re-certification
> arbitre (`check-ecosysteme-integrity.py` — 110/110 attendu).

---
