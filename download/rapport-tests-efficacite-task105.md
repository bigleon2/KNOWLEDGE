# Rapport Task 105 — Tests d'efficacité du système d'installation → stratégie d'optimisation

**Horodatage : 2026-11-19** · Directive propriétaire trace `1a1efb513dfbc805` (item A, gen-plan mode step) : « génère $FACON et fais des tests $FACON2 sur le système d'installation de mon écosystème dans l'objectif d'optimiser son efficacité, trouve $FACON la meilleure stratégie pour faire cela. » · Harnais : `scripts/task105-campagne-efficacite.py` (stdlib, self-test 6/6, protocole `download/protocole-tests-efficacite-task105.json`) · Rapports machine : `download/rapport-efficacite-task105-{machine,flux,garanties,bootstrap-consolide,synthese}.json`.

## 1. Méthode — la meilleure stratégie pour TESTER le système d'installation

Trois axes complémentaires, orchestration R4 des arbitres existants (le harnais mesure, ne duplique aucune logique de verdict, n'écrit aucune correction) :

- **Axe A — Efficacité machine** : 7 composants chronométrés médiane ×3 (perf_counter, conventions Task 95), comparés à la baseline Task 70.
- **Axe B — Efficacité du flux de bout en bout** : le goulot réel identifié par l'étude Task 70 n'est PAS l'entré-sortie mais le **budget #token** — le coût d'un bootstrap se compte donc en **tours agent** et **octets de sortie**, pas en millisecondes. Trois voies d'entrée mesurées apples-to-apples.
- **Axe C — Garanties non négociables** : toute optimisation est invalide si elle casse l'idempotence, la lecture seule du dry-run, la garde R2 ou les arbitres (zéro-régression refactor-guard).

## 2. Résultats — Axe A (efficacité machine) : verdict FAIL honnête (défaut F1 découvert, pas un échec de mesure)

| Composant | Médiane | Verdict |
|---|---|---|
| c1 pipeline `--dry-run` (lecture seule) | 45,8 ms | PASS |
| c2 pipeline complet (sync + seal v2.3 + manifeste + post-install 55 SHA) | 226,6 ms | PASS |
| c3 scelleur archive v2.3 | 71,0 ms | PASS |
| c4 manifeste intégrité (114 checks) | 44,4 ms | PASS |
| c5 chaîne certification complète (6 arbitres) | 377,3 ms | PASS |
| c6 garde É1-INSTALL `--check` | 62,0 ms | PASS |
| c7 auto-install D727 | 335,0 ms | **FAIL — défaut F1 (§5)** |

**Lecture** : coût machine TOTAL médian **1 162 ms** pour l'ensemble du système — hypothèse H1 confirmée : le coût machine est négligeable à l'échelle d'une session. Le pipeline complet passe de 140 ms (Task 70, 53 entrées, ancien véhicule de rescellement) à **226,6 ms (+61,9 %)** : aggravation intégralement expliquée par le passage à 55 entrées KB, au scelleur v2.3 (corpus + piliers, mission F1 Task 100) et à l'étape 2bis de régénération du manifeste — un surcoût de sûreté, pas une régression. **Conclusion Axe A : il n'existe RIEN à optimiser côté machine qui soit perceptible** (accélérer 1,16 s est sans objet dans une session dominée par les tours LLM).

## 3. Résultats — Axe B (efficacité du flux) : le levier réel, mesuré — verdict PASS

| Voie d'entrée du bootstrap | Tours agent | Commandes | Durée | Octets émis | Verdict consolidé | Garanties |
|---|---|---|---|---|---|---|
| **V1 — manuelle canonique** (séquence G0 réelle : état · préflight git · dry-run · install · certification · É1) | **6** | 10 | 2,21 s | 15 958 | non (aucune vue unique) | complètes |
| **V2 — auto-install D727** (existant) | 1 | 1 | 0,34 s | 402 | oui — **ECHEC (défaut F1)** | partielles (sans préflight git ni certification) |
| **V3 — prototype consolidé** (`--bootstrap-consolide`, preuve de mesure Task 105) | **1** | 1 | 0,75 s | 389 | **oui — INSTALLE** | **complètes** |

**Gains V3 vs V1 : −83,3 % de tours agent, −97,6 % d'octets émis, SANS AUCUNE perte de garantie** (préflight git dépôt + dry-run + installation canonique + certification 6 arbitres + garde É1, verdict unique compact). Hypothèse H2 confirmée par la mesure : à 6 tours par bootstrap et des recyclages sandbox systématiques (4ᵉ consécutif — suites 147-150), la consolidation est le SEUL levier d'efficacité réel du système d'installation. Donnée réelle complémentaire (cas dérive, G0 de ce tour) : les 6 tours ont inclus la réparation d'une dérive de 2 741 fichiers — même séquence, la voie consolidé traite ce cas par ses étapes internes sans multiplier les tours.

## 4. Résultats — Axe C (garanties) : PASS 4/4

| Test | Attendu | Obtenu |
|---|---|---|
| g1 idempotence ×2 du prototype | verdicts normalisés byte-identiques (R6) | **identiques** (champs volatils horodatage/durées/verdict_compact exclus — le contenu sémantique etapes+verdict_global est comparé) |
| g2 dry-run 0 mutation | rc=0 et 0 fichier modifié dans les zones cibles | **rc=0, 0 fichier modifié** (preuve mtime sur skills/ + scripts/ + archive + manifeste) |
| g3 garde R2 | 0 rétrogradation — host ≤ repo partout | **0 rétrogradation** |
| g4 arbitres post-campagne | certification ALL PASS 6/6 | **rc=0 — 6/6** (verify-cross 165/165 ×2 · vcw 16/16 · integrity 114/114 · interactions 55/55 STRICT · tool-routing 6/6) |

Hypothèse H3 confirmée : la consolidation est prouvablement sans régression.

## 5. Défauts découverts par la campagne (consignés, NON corrigés — application sous GO)

- **F1 (S2 — découverte majeure)** : `auto-install-ecosysteme.py` (voie 1-commande EXISTANTE, D727) est **non fonctionnel** : la copie dépôt de `ensure-installed.py` crashe (`subprocess` avec `cwd=ROOT/"KNOWLEDGE-repo"` inexistant quand ROOT est le dépôt lui-même — le contrôle « head miroir » O-68-1 Task 69 a introduit le bug) → contrôle initial passé pour ERREUR → pipeline exécuté à tort → verdict ECHEC. Cassé depuis Task 69, **inaperçu car le bootstrap canonique est manuel** — preuve vivante que la consolidation existante n'était plus vérifiée. Correctif proposé (chirurgical, 3 lignes) : dans `etat()`, n'appeler le miroir que si `(ROOT / "KNOWLEDGE-repo" / ".git").exists()`, sinon pointer le head sur ROOT lui-même quand ROOT est déjà le dépôt.
- **F2 (résolu en cours de campagne)** : le harnais ne capturait pas les sorties des composants (l'anomalie c1 de la 1ʳᵉ passe a été impossible à diagnostiquer a posteriori) — corrigé : champ `sortie_run1` ajouté, re-jeu complet.
- **F3 (anomalie transitoire, non reproduite)** : à la 1ʳᵉ passe, c1 (dry-run) a rendu rc=2 ×3 sur un hôte pourtant synchronisé ; 2ᵉ passe : rc=0 ×3. Cause exacte non déterminée (sortie non capturée à l'époque — cf. F2) ; hypothèse la plus probable : divergence hôte transitoire réparée par les runs d'installation de la campagne elle-même. Consigné honnêtement, à surveiller au prochain bootstrap.
- **F4 (convention, résolu)** : la garde N1 de `check-tool-routing` exige la docstring dans les 600 premiers octets — le bloc CONTEXTE SYSTÈME en tête de script la repoussait à l'octet 886 → FAIL 6/6 de la certification en cours de campagne. Convention rétablie : **docstring d'abord, bloc CONTEXTE ensuite** (précédent task104-genere-fiche.py, passé 6/6) — appliqué au harnais, certification revenue à 6/6.

## 6. Stratégie d'optimisation hiérarchisée (réponse à « trouve la meilleure stratégie »)

La feuille de route d'application (GO propriétaire à chaque étape) est détaillée au §8 ; la hiérarchie :

- **S1 — Faire de la voie consolidée l'entrée canonique unique du bootstrap** (gains mesurés : −83,3 % tours, −97,6 % octets par session, garanties intactes §4). Application : promotion du prototype V3 (pattern du harnais Task 105) en point d'entrée documenté du PM-INSTALL §3.2 — **sous GO propriétaire** (R2/zéro-régression : le pipeline et les arbitres existants ne sont PAS modifiés, seule l'entrée change). C'est LA recommandation : le seul goulot réel est le nombre de tours agent.
- **S2 — Corriger le défaut F1** (auto-install D727 + copie dépôt d'ensure-installed) pour rendre à l'écosystème son véhicule de self-healing 1-commande historique — utile même si S1 est adopté (redondance de voie d'entrée). Correctif 3 lignes proposé §5-F1, sous GO.
- **S3 — Inscrire la convention « docstring d'abord »** pour tout nouveau script (F4) dans les conventions script-creator/correct-py — évite le FAIL N1 silencieux sur la couche.
- **S4 (cosmétique)** : rafraîchir l'étiquette de baseline (Task 70 : 140 ms/53 entrées) dans les futurs rapports de performance pour éviter les deltas trompeurs (+61,9 % mesuré ici est un surcoût de sûreté assumé, pas une dérive).

## 7. Contre-recommandations (réitérées par la mesure — étude Task 70)

Aucune réécriture structurelle : ni OOP intégrale, ni noyau compilé unique, ni réingénierie du pipeline — le coût machine total est de 1,16 s et le goulot réel est le budget #token. Toute optimisation qui ajoute des lectures de contexte (agents supplémentaires, couches d'abstraction) dégrade l'efficacité réelle.

## 8. Feuille de route (GO propriétaire requis à chaque étape)

1. **GO-1** : promotion de la voie consolidée en entrée canonique (S1) — livrable : mise à jour PM-INSTALL §3.2 + point d'entrée unique, campagne de non-régression re-jouée.
2. **GO-2** : correctif F1 (S2) + test de non-régression dédié (la voie V2 doit rendre INSTALLE sur état sain).
3. **GO-3** (optionnel) : convention S3 ajoutée aux canons script-creator/correct-py.
4. Surveiller F3 au prochain bootstrap (si récidive : capture immédiate — le harnais sait désormais le faire).
