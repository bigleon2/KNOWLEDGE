# Grille de calibration #token — gen-plan v3.6.1

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

## Historique de calibration

| Exécution | Date | Type tâche | #token estimé | #token réel | Écart | Action |
|-----------|------|-----------|---------------|-------------|-------|--------|
| 1 | 2026-07-18 | Planification 66 skills | 4500 | 5200 | +15.6% | Aucune (0-20%) |
| 2 | 2026-07-18 | Test E2E gen-plan | 3000 | 3600 | +20.0% | Aucune (seuil) |
| 3 | 2026-07-29 | clone-chat v1.1.0 | 4000 | 5200 | +30.0% | Ajustement grille |
| 4 | 2026-07-29 | clone-chat v1.2.0 (historique) | 4400 | 4600 | +4.5% | Aucune (0-20%) |
