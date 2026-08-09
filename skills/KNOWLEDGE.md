# Registre KB — Écosystème Knowledge

> **Date** : 2026-08-09
> **Version** : 2.0.0
> **Skills** : 77 (6 écosystème + 71 métier)
> **Relations** : 14 bidirectionnelles

---

## gen-plan v3.6.1

- **Category** : ecosystem
- **Description** : Planification de tâches. 4 modes, 15 étapes E1-E15, 3 profils ressource, tagging #token, lecture bloc par bloc.
- **Dépend de** : correct-work >= v2.4.0, clone-chat >= v2.0.0 (optionnel), skills-inventory >= v1.0.0
- **Utilisé par** : correct-work (Étape 1), autonomous-agent (tâches complexes)
- **Dernière calibration** : 2026-08-09
- **Statut** : stable

---

## correct-work v2.4.0

- **Category** : ecosystem
- **Description** : vérification et correction du travail. 3 modes (PROJET/CIBLE/DIRECT), 5 étapes, multi-cibles, découplage gen-plan, métriques de performance.
- **dépend de** : gen-plan >= v3.6.0 (optionnel), clone-chat >= v2.0.0, fullstack-dev >= v1.0.0
- **Utilisé par** : gen-plan (E1 validation plan + E8 hook), autonomous-agent (cohérence agent)
- **dernière calibration** : 2026-08-09
- **Statut** : stable

---

## clone-chat v2.0.0

- **Category** : ecosystem
- **Description** : Clonage de discussion en Markdown auto-suffisant. 7+1 étapes, 8 checks validation, 5 types de drift.
- **Dépend de** : correct-work >= v2.4.0 (validation croisée)
- **Utilisé par** : gen-plan (E4/E15 calibration + archivage, optionnel), correct-work (Mode CIBLE §3.5), autonomous-agent (État Long, optionnel)
- **Dernière calibration** : 2026-08-09
- **Statut** : stable

---

## skills-inventory v1.0.0

- **Category** : ecosystem
- **Description** : Scan et inventaire des skills disponibles. Consultation par tags, catégories, versions.
- **Dépend de** : aucun
- **Utilisé par** : gen-plan (E5 sélection skills), autonomous-agent (découverte agents)
- **Dernière calibration** : N/A
- **Statut** : stable

---

## skill-creator v1.0.0

- **Category** : ecosystem
- **Description** : Création et gestion de skills. Templates, évaluations, agents spécialisés.
- **Dépend de** : aucun
- **Utilisé par** : clone-chat (conventions structurelles)
- **Dernière calibration** : N/A
- **Statut** : stable

---

## autonomous-agent v1.0.0

- **Category** : ecosystem
- **Description** : Agent autonome avec mémoire interne à deux niveaux (État Court + État Long). 5 modules, 4 modes.
- **Dépend de** : gen-plan >= v3.6.0, clone-chat >= v2.0.0 (optionnel), correct-work >= v2.3.0
- **Utilisé par** : aucun
- **Dernière calibration** : N/A
- **Statut** : stable

---

## Relations inter-skills

| Skill A | Relation | Skill B | Nature | Détails |
|---------|----------|---------|--------|--------|
| gen-plan | invoque | correct-work | Étape 1 + E8 hook | Validation plan + hook vérification, >= v2.4.0 |
| gen-plan | utilise | clone-chat | Calibration + archivage | E4, E15, optionnel, >= v2.0.0 |
| gen-plan | consulte | skills-inventory | Sélection skills | E5, >= v1.0.0 |
| gen-plan | enrichit | KNOWLEDGE.md | Calibration | E15, mise à jour registre |
| correct-work | utilise | gen-plan | Plan de vérification | Étape 1, >= v3.6.0 |
| correct-work | vérifie | clone-chat | Mode CIBLE | §3.5 Context Drift, >= v2.0.0 |
| correct-work | vérifie | fullstack-dev | Projets web | Structure et dépendances |
| clone-chat | archivé par | gen-plan | Sessions longues | Optionnel, >= v3.6.1 |
| clone-chat | vérifié par | correct-work | Validation croisée | §3.5 drift, >= v2.4.0 |
| clone-chat | conventions par | skill-creator | Conventions structurelles | >= v1.0.0 |
| autonomous-agent | utilise | gen-plan | Planification | Tâches complexes, >= v3.6.0 |
| autonomous-agent | persist via | clone-chat | État Long | Inter-sessions, optionnel, >= v2.0.0 |
| autonomous-agent | vérifié par | correct-work | Validation | Cohérence agent, >= v2.4.0 |
| autonomous-agent | consulte | skills-inventory | Découverte agents | Sélection, >= v1.0.0 |