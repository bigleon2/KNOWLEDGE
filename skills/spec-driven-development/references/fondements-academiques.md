# Fondements académiques et veille — spec-driven development (N34, r56 — n°54)

## 1. Sources vérifiées (preuves tmp/n31-recherche/ : cand-x2)

- **From Code to Contract in the Age of AI Coding Assistants** (arXiv, 30 janv. 2026) : le SDD inverse le flux traditionnel — la spécification devient la source de vérité, le code un artefact généré et vérifié contre elle.
- **A Spec-First Approach to AI-Native Engineering** (Microsoft Developer, 10 juin 2026) : l'équipe définit en amont guardrails, exigences, contraintes, critères d'acceptation — le SDD comme approche d'équipe, pas seulement d'outil.
- **GitHub Spec Kit** (outillage cité par les sources 2026) : chaîne spec → plan → tasks outillée ; la décomposition est une étape première-class.
- **What Is Spec-Driven Development? A Complete Guide** (augmentcode, 23 avr. 2026) : la spec comme contrat exécutable dont les agents dérivent le code, prévenant la dérive.
- **Spec-Driven Development in 2026: What It Is, the Tooling** (dev.to, 19 juin 2026) : spécification précise et exécutable = source de vérité ; code = artefact générable et vérifiable.

## 2. Signaux de veille

Consensus 2026 : la spec est le contrat, pas la documentation ; les critères d'acceptation doivent être mécaniquement exécutables ; l'outillage (Spec Kit et équivalents) outille la chaîne complète ; risque nommé par les sources : la spec-poussière (specs non tenues à jour) — d'où M5 RE-SPEC obligatoire.

## 3. Lecture professionnelle

Commencer par l'article arXiv (inversion théorique), puis le guide Microsoft (pratique d'équipe), puis Spec Kit (outillage) ; les guides 2026 servent de vérification de vocabulaire.

## 4. Interactions entre disciplines (n°54, r56)

(1) **sdd ↔ harness** — les critères d'acceptation SDD SONT des gardes-fous : ils s'exécutent à chaque boucle et à chaque round correct-work ; (2) **sdd ↔ loop** — la boucle externe génération-vérification exige un vérifier stable : la spec le fournit, sinon la boucle optimise du bruit ; (3) **sdd ↔ fleet** — micro-specs par sous-tâche (objectif, livrable, check) rendent la flotte auditable ; (4) **sdd ↔ context** — la spec est le plus fort réducteur d'incertitude du contexte : cadrer court et exigible vaut mieux qu'un historique long. Source transverse : arXiv janv. 2026 — « from code to contract » décrit exactement la pratique écosystème (plan = spec de session, answer key = journal d'amendements).
