# Prompt Engineering Kit (PEK) v4.1 — Méthode de raisonnement adaptative

> **Rôle dans gen-plan** : matérialisation opérationnelle de la philosophie §1.4.6 (« CoT + Chaining avec auto-correction »). La sélection du mode de raisonnement s'effectue à E3 (complexité) et se combine avec le profil ressource (§2.4). Les blocs adaptatifs A-J structurent les livrables de sortie selon le Type 1-4.
> **Provenance** : PEK v4.1-META-PROMPT-EDITED (upload 2026-09-10, édition 2025-07-13) — intégrée par assemblage (§3.2 PM-INSTALL) ; modules d'implémentation web éliminés. Sources secondaires : V4.0-Consolidated (méta-prompt auto-suffisant), kits v3.0.0/v3.0.1 (blocs A-J).

---

## §1 — Les 3 modes d'exécution

| Mode | Pipeline | Complexité cible | Équivalent gen-plan |
|------|----------|------------------|---------------------|
| **CoT** (défaut) | 7 étapes séquentielles | moyenne à complexe | Profil NORMAL — plan complet E1-E15 |
| **Chaining** | 4 étapes pipeline | simple, linéaire | Profil ECO — étapes réduites, 1 checkpoint |
| **Hybride** (auto) | Bascule dynamique | détectée à l'étape 1 | Règle §2.4 signaux de pression → ECO/VIEUX PC |

**Règle de bascule (mode Hybride)** : complexité `simple` → Chaining ; complexité `moyen`/`complexe` → CoT. La complexité est déterminée à la première étape (Compréhension) — jamais recalculée en cours d'exécution (cohérent avec §1.4.8 : downgrade irréversible).

---

## §2 — Pipeline CoT (7 étapes)

| # | Étape | Durée indicative | Livrable |
|---|-------|------------------|----------|
| 1 | **Compréhension** | 5-10 min | Résumé exécutif : type de projet, objectif en une phrase, contraintes majeures, niveau de complexité |
| 2 | **Décomposition** | 5 min | Carte des composants + dépendances + patterns + sélection des blocs A-J |
| 3 | **Extraction** | 10-15 min | Liste exhaustive : objectifs, règles absolues, étapes, format de sortie, style, stack |
| 4 | **Structuration** | 10 min | Plan de mapping éléments → architecture du livrable (blocs sélectionnés) |
| 5 | **Génération** | 20-30 min | Livrable complet, blocs générés dans l'ordre |
| 6 | **Validation** | 10 min | Score qualité (§6) + rapport de validation |
| 7 | **Amélioration** | 5 min | 3 points d'amélioration concrets + cas limites non couverts + tests additionnels |

**Contrainte C1** : séquence stricte 1→7, aucun saut, aucune fusion d'étapes. Revenir en arrière est autorisé (cohérent avec E12-E13 détection d'écart → ajustement).

---

## §3 — Pipeline Chaining (4 étapes)

| # | Étape | Livrable |
|---|-------|----------|
| 1 | **Préparation** | Inventaire structuré des composants, métadonnées, patterns, blocs pertinents |
| 2 | **Traitement** | Contenu détaillé de chaque bloc (versions intermédiaires) |
| 3 | **Vérification** | Auto-évaluation (cohérence, complétude, exemples 4+ domaines) + corrections appliquées |
| 4 | **Optimisation** | Livrable final en 3 versions : Pro (annoté), Clean (prêt à l'emploi), Compacte (synthèse) |

---

## §4 — Blocs de sortie adaptatifs (A-J)

La structure de sortie n'est **pas figée** : elle s'adapte au livrable produit.

### Hiérarchie de priorité

- **Niveau 1 (obligatoires)** : `A` Résumé exécutif (toujours premier) · `H` Recommandations (toujours dernier)
- **Niveau 2 (fortement recommandés)** : `C` Prompt/Instructions · `E` Contraintes & règles · `G` Guide d'utilisation
- **Niveau 3 (contextuels)** : `B` Architecture · `D` Données & schemas · `F` Résultats & outputs · `I` Tests & validation · `J` Glossaire & références

### Correspondance Type de tâche (E3) → blocs

| Type gen-plan | Blocs recommandés |
|---------------|-------------------|
| Type 1 (documents) | A + C + D + E + G + H + J |
| Type 2 (visualisation) | A + C + D + F + G + H |
| Type 3 (développement web) | A + B + C + D + E + G + H + I |
| Type 4 (traitement données) | A + B + D + E + F + G + H + I |
| Méta-outil / écosystème | A + B + C + D + E + F + G + H + I + J |

### Règles de composition

1. Bloc `A` toujours en premier, bloc `H` toujours en dernier.
2. Ordre des blocs contextuels libre (enchaînement le plus logique).
3. Chaque bloc autonome — compréhensible sans lire les autres.
4. Cohérence inter-blocs — aucune contradiction ni redondance (hook correct-work E9-E14).
5. Nombre total recommandé : **5 à 9 blocs** selon la complexité.

---

## §5 — Les 9 règles critiques

| # | Règle | Priorité | Autorisé / Interdit |
|---|-------|----------|---------------------|
| 1 | **Préservation de l'original** | CRITICAL | Structurer, clarifier, organiser / inventer, modifier les décisions, dénaturer |
| 2 | **Complétude des livrables** | CRITICAL | Contenu minimal avec `[À COMPLÉTER]` / omettre un livrable, vide silencieux |
| 3 | **Cohérence des références** | CRITICAL | Chemins relatifs, liens valides / référencer l'inexistant, chemins absolus, liens brisés |
| 4 | **Respect des schemas** | CRITICAL | Valider la conformité, signaler les écarts / output non conforme, champs ignorés |
| 5 | **Application du pipeline** | CRITICAL | Prendre le temps, revenir en arrière / sauter ou mélanger les étapes |
| 6 | **Qualité des exemples** | CRITICAL | Cas limites, 4+ domaines / exemples génériques, mono-domaine, doublons |
| 7 | **Automatisation et versionnage** | CRITICAL | Outils automatisés, traçage VERSION / générer manuellement si script existe |
| 8 | **Détection de contenu trompeur** | HIGH | Vérifier les allégations / greenwashing, fausses promesses, statistiques inventées |
| 9 | **Boucle de feedback itérative** | HIGH | Intégrer les métriques A/B / ignorer les données quantitatives disponibles |

Les règles 1-7 héritent des contraintes absolues V4.0 ; les règles 8-9 sont les ajouts v4.1.

---

## §6 — Contrôle qualité (12 checks, scoring 25 pts)

**Structure du score** : Complétude 10 pts · Cohérence 8 pts · Qualité 7 pts. **Seuil minimum : 22/25 (88%)** — cohérent avec les verdicts correct-work (S1-S4) et l'arbitre verify-cross.

| # | Check | Axe |
|---|-------|-----|
| 1 | Tous les livrables présents et non vides | Complétude |
| 2 | Références croisées valides | Complétude |
| 3 | Livrable directement utilisable (zéro placeholder non signalé) | Complétude |
| 4 | Exemples pertinents, 4+ domaines variés | Cohérence |
| 5 | Structure de sortie adaptée au type de tâche | Cohérence |
| 6 | Format d'entrée correctement pris en compte | Cohérence |
| 7 | Version tracée (registre KB / VERSION) | Complétude |
| 8 | Pas de contenu trompeur détecté | Qualité |
| 9 | Mécanismes de feedback prévus | Qualité |
| 10 | Variables et placeholders définis | Qualité |
| 11 | Cas d'erreur couverts | Cohérence |
| 12 | Instructions claires et non ambigües | Qualité |

**Verdicts** : 25/25 PARFAIT · 22-24 EXCELLENT · 20-21 ACCEPTABLE · <20 À REPRENDRE. Score < 22 → corriger puis re-valider (boucle E12-E13).

### Cas limites (edge cases)

| Cas | Conduite |
|-----|----------|
| Données manquantes | Signaler les champs requis, proposer les formats, NE PAS générer |
| Contexte incomplet | Livrable partiel avec `[À COMPLÉTER]`, aucun contenu inventé |
| Contraintes contradictoires | Identifier chaque contradiction, proposer une résolution |
| Auto-référence | Détecter la circularité → rapport d'auto-analyse, pas de génération imbriquée |
| Génération circulaire | Détecter et interrompre, recommander correction directe |
| Input corrompu | Signaler l'erreur, proposer alternative de format |

---

## §7 — Mapping gen-plan ↔ PEK

| gen-plan (E1-E15) | Étape PEK correspondante |
|--------------------|--------------------------|
| E1 Analyse de la demande | 1 Compréhension (objectif, contraintes, complexité) |
| E2 Inventaire des ressources | 1 Compréhension (fin) — signaux de pression = données manquantes |
| E3 Classification Type 1-4 | 1 Compréhension — type de projet + sélection mode (CoT/Chaining/Hybride) |
| E4 Estimation #token | (spécifique gen-plan — grille §4, coeffs mode PEK applicables) |
| E5 Sélection des skills | 2 Décomposition (blocs A-J) |
| E6 Profilage ressource | 1 Compréhension — calibre le mode d'exécution (cf. §1) |
| E7 Création du plan | 4 Structuration (mapping éléments → blocs) |
| E8 Validation du plan | 6 Validation (pré-validation du plan, hook correct-work) |
| E9-E14 Exécution + hooks | 5 Génération (blocs) + 6 Validation par phase (mode CIBLE) |
| E15 Bilan et auto-calibration | 7 Amélioration (3 points concrets + calibration grille) |

**Règle d'usage** : le PEK ne remplace PAS les 15 étapes — il fournit le **mode de raisonnement** (§1) et la **structure de sortie** (§4) mobilisés par les étapes. Les livrables des plans génèrent leurs blocs selon le Type ; la validation par phase applique les 12 checks ; le score 22/25 s'ajoute aux critères correct-work.

---

## §8 — Provenance et historique

| Version | Nature | Apport |
|---------|--------|--------|
| v1.0 | Kit standalone (structure XML) | Structure modulaire initiale |
| v2.0 | Templates complets | Modules 00-07 |
| v3.0 | Fusion XML + Markdown | 8 modules prompts, build assemblé |
| v3.1 | Universel multi-format | Blocs A-J adaptatifs, 10 tests, structure adaptative |
| v4.0 | Consolidé auto-suffisant | 7 contraintes CRITICAL, edge cases, scoring 25 pts, quickstart zéro placeholder |
| v4.1 | Interface web + 3 modes | Modes CoT/Chaining/Hybride, règles 8-9, 12 checks, buildSystemPrompt() |

**Note d'intégration** : la présente référence est la forme « méthode pure » du PEK v4.1 édité — les modules d'implémentation web (stack Next.js 16, interface 5 onglets, Prisma/SQLite, pipeline temps réel, z-ai-web-dev-sdk, buildSystemPrompt) ont été écartés lors de l'assemblage : ils relèvent d'une matérialisation applicative, pas de la méthode mobilisable par gen-plan (skill prompt pur, auto-contenu, zéro dépendance d'infrastructure — §0 règle zéro). L'implémentation de référence reste documentée dans l'archive source (upload/pek-v4.1.zip).
