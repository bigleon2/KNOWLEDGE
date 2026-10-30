```markdown
# Grille de calibration #token — gen-plan v3.7.0

## Grille par agent/skill

| Agent/Skill | #token sortie (min) | #token sortie (max) | Coeff. complexité |
|-------------|--------------------|--------------------|------------------|
| Planification E1-E2 | 800 | 1500 | 1.0x |
| Classification E3 | 200 | 500 | 1.0x |
| Estimation E4 | 300 | 800 | 1.0x |
| Sélection E5 | 500 | 1200 | 1.2x |
| Profilage E6 | 200 | 400 | 1.0x |
| Création plan E7 | 1000 | 2500 | 1.5x |
| Validation E8 | 500 | 1500 | 1.0x |
| Exécution simple (1 skill) | 2000 | 5000 | 1.0x |
| Exécution moyenne (2-3 skills) | 5000 | 10000 | 1.3x |
| Exécution complexe (4+ skills) | 10000 | 20000 | 1.5x |
| Surveillance E10-E12 | 500 | 1500 | 1.0x |
| Auto-calibration E15 | 800 | 2000 | 1.0x |

## Grille par type de tâche (usage clone-chat)

| Mode | Longueur discussion | #token estimé | Profil min. |
|------|---------------------|---------------|-------------|
| clone-court | < 5 sessions | 2000-3500 | ECO |
| clone-moyen | 5-15 sessions | 3500-5500 | NORMAL |
| clone-long | > 15 sessions | 5500-9000 | NORMAL |

> Note (historique v1.2.0) : estimation +10% pour couvrir l'Étape 3.5 Context Drift et l'intégration gen-plan.

## Coefficients d'ajustement

| Facteur | Coefficient | Condition |
|---------|-------------|-----------|
| Complexité faible | 0.8x | Tâche routinière, template existant |
| Complexité standard | 1.0x | Cas nominal |
| Complexité élevée | 1.3x | Multi-skills, dépendances croisées |
| Complexité critique | 1.5x | Projet nouveau, aucune référence |
| Profil ECO | 0.7x | Réduction surveillance, snippets simplifiés |
| Profil VIEUX PC | 0.5x | Scripts légers, pas de graphiques |
| **Profil frais local** | **3-4x** (v3.28.1) | Première exécution sur profil restauré/réinstallé — coût de découverte du corpus (lectures multi-fichiers, PMs longs, KB, outillage) non couvert par les grilles calibrées sur environnement établi |
| **Appels API en masse** | **2-3x** (v3.28.1) | Phases avec appels LLM/API répétés — rate-limit 429, retries, backoff 12-48 s + pause anti-rafale 45 s ; guidance : ThreadPoolExecutor 2-4 workers, throttle 1-2 s/appel, journal d'état idempotent, tri par taille croissante |
| **Récupération externe bloquée** | **3-4x** (v3.28.2) | Contenu externe adversarial (WAF CDN 405, SPA non rendue en headless, rate-limit API web) — multi-tours de contournement règle d'or n°1 avant la voie gagnante (escalade : WebFetch → curl → agent-browser [double-open] → z-ai function `page_reader`), puis lecture intégrale du contenu récupéré ; la campagne de récupération porte son budget propre AVANT l'étape qui la requiert (preuve : Task 6 E15 — 2 liens chat.z.ai, 10+ tours d'adaptation, ~60 k de texte ; recommandation E15 consignée au worklog, sollicitée par le propriétaire) |

## Historique de calibration

| Exécution | Date | Type tâche | #token estimé | #token réel | Écart | Action |
|-----------|------|-----------|---------------|-------------|-------|--------|
| 1 | 2026-07-18 | Planification 66 skills | 4500 | 5200 | +15.6% | Aucune (0-20%) |
| 2 | 2026-07-18 | Test E2E gen-plan | 3000 | 3600 | +20.0% | Aucune (seuil) |
| 3 | 2026-07-29 | clone-chat v1.1.0 | 4000 | 5200 | +30.0% | Ajustement grille |
| 4 | 2026-07-29 | clone-chat v1.2.0 (historique) | 4400 | 4600 | +4.5% | Aucune (0-20%) |
| 5 | 2026-08-29 | correct-work PROJET écosystème | 12000 | ~11000 | -8.3% | Aucune (0-20%) |
| 6 | 2026-08-29 | Frontmatters + clone-chat 08-29 | 10000 | ~9500 | -5.0% | Aucune (0-20%) |
| 7 | 2026-08-29 | QA clone GML + spell-check | 11000 | ~9800 | -10.9% | Aucune (0-20%) |
| 8 | 2026-08-30 | ZIP v1.1.0 + réconciliation | 9000 | ~8800 | -2.2% | Aucune (0-20%) |
| 9 | 2026-08-30 | correct-work PROJET + archéologie versions + lignée clones | 9500 | ~9800 | +3.2% | Aucune (0-20%) |
| 10 | 2026-08-30 | correct-work PROJET + alignement gen-plan v3.7.0 au sein de correct-work | 9000 | ~9200 | +2.2% | Aucune (0-20%) |
| 11 | 2026-08-30 | Propagation knowledge-repo (Tasks 8-9, commit c79fdb6) | 4500 | ~4700 | +4.4% | Aucune (0-20%) |
| 12 | 2026-10-25 | Audit écosystème complet (profil frais local — session web-eb6c8580, Tasks 1-5) | 12200 | ~52000 | ×3-4 (326 %) | **Recalibration complète** : + coefficient profil frais local ×3-4 (row v3.28.1) |
| 13 | 2026-10-26 | Directive 10 tâches P0-P2 (session web-eb6c8580 — 233 fichiers API en masse, rate-limit 429) | 78000 | ~120000 (partiel) | ×1,5-1,7 (grille déjà recalibrée ×3-4 au plan) | Contingence API en masse ×2-3 + guidance parallélisation ajoutées (row v3.28.1) |
| 14 | 2026-10-30 | Task 6 publication GO + trio TSI + re-mesure voie L (session web-eb6c8580 — récupération externe adversariale : 2 liens chat.z.ai, WAF CDN 405 + SPA non rendue) | 17000 | ~60000-70000 (ressenti, non instrumenté) | ×3,5-4 (> 35 %) | **Contingence « récupération externe bloquée ×3-4 » ajoutée** (row v3.28.2 — recommandation E15 Task 6 consignée au worklog, sollicitée par le propriétaire le 2026-10-30) |
```