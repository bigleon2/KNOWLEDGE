"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.10)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""Task 47 — D3 : frontmatter, note de lignage et evals du skill iphone19 v0.9.0."""

FRONTMATTER = """---
name: iphone19
version: 0.9.0
category: metier
language: fr
tags:
  - "#photo"
  - "#amelioration-photo"
  - "#iphone19-pro-max"
  - "#preset-iphone19-max"
  - "#generation-anticipee-2027"
  - "#mode-serie"
description: >
  Pipeline d'amélioration photo « iPhone 19 Pro Max, qualité max » (CPE — Computational
  Photo Engine) — génération ANTICIPÉE 2027 (calibration extrapolée des rumeurs crédibles
  2026 : A21 Pro, Photonic Engine NG+ — aucune spécification confirmée, bump v1.0.0 prévu
  à la confirmation officielle Apple). Analyse complète par grille ANALYSE-v2 (A1-A10,
  B1-B6 dont inventaire B6 verrouillé, C1-C3), moteur de décision R1-R18 (R18 : ouverture
  variable simulée ƒ/1.48-ƒ/4.0), plan d'actions YAML affiché AVANT toute exécution,
  pipeline P0-P8 dans l'ordre strict, contrôle qualité 12 critères avec itération
  contrôlée (max 2), presets de rendu §6 (défaut iphone19_max — ancrage ANTICIPÉ A21 Pro
  [RUMEUR] / extrapolation de la baseline confirmée 18), rendus d'époque (années 70 →
  2010), restauration de photos anciennes (scans, tirages), mode poster/print A4 300 DPI,
  mode série multi-sorties, rapport final en français + question utilisateur obligatoire.
  Garde-fous photo G1-G7 : fidélité stricte des visages (expressions, orientation des
  têtes), zéro élément ajouté, original non-destructif. Pensez à utiliser ce skill dès
  que l'utilisateur demande explicitement le rendu « iPhone 19 » ou la génération
  suivante, ou le preset iphone19_max — pour la génération CONFIRMÉE courante
  (iPhone 18), préférer le skill iphone18.
dependencies:
  - skill: skill-creator
    version: ">=1.0.0"
    used_at: "conventions structurelles (frontmatter, evals)"
  - skill: VLM
    version: ">=1.0.0"
    used_at: "analyse §1 (vision) + QC §5 comparatif original↔sortie"
  - skill: image-edit
    version: ">=1.0.0"
    used_at: "exécution §4 P1-P7 — contournement SDK base64 scripts/editer-image.mjs (CLI z-ai erreur 1210)"
read_when:
  - Déclencher quand la demande concerne : rendu « iPhone 19 Pro Max qualité max » (génération ANTICIPÉE 2027), preset iphone19_max, traitement « génération suivante » demandé explicitement
  - Déclencher si la demande mentionne : iphone19, preset iphone19_max, génération suivante iPhone
  - Ne pas déclencher pour : génération CONFIRMÉE courante iPhone 18 (→ skill iphone18), périmètre iPhone 17 (→ skill iphone17), dessin technique coté (→ dessin-technique), génération d'image sans photo source (→ image-generation), vidéo (hors périmètre)
---

## §0 — Contexte Système (SHARED v1.7.7)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.

## Lignage — projection skill ← prompt maître source

> Skill métier projeté depuis le prompt maître `skills/@photos/iphone19-photos.md` **v0.9.0 [ANTICIPÉE]** (génération iPhone 19 ANTICIPÉE 2027 — calibration extrapolée de rumeurs crédibles 2026, non confirmée ; PM génération 18 confirmée : `iphone18-photos.md` v1.0, PM parallèle) — fichier du dépôt, **byte-identique, jamais édité (R2)**. Le corps ci-dessous (« ## PROMPT MAÎTRE » → §13) est repris **VERBATIM** de cette source ; dans ce skill, « le document » y désigne le présent SKILL.md, et la discipline §11 (auto-audit) s'exécute à l'occasion d'un bump de version du skill (semver + recalibrage du registre KB). Test empirique de référence : PA-TEST-005 (Task 47, campagne série 2 photos — fidélité maximale, zéro retouche demandée par le propriétaire). P8b (recadrage) : le PM source référence `crop_utils.py` (livrable historique du projet CLUB, non embarqué — un recadrage PIL équivalent est produit à la demande).
"""

EVALS = {
  "skill": "iphone19",
  "version": "0.9.0",
  "evals": [
    {
      "id": "E1-pipeline-complet",
      "description": "Photo réelle + demande explicite rendu iPhone 19 → pipeline §1→§9 complet : analyse ANALYSE-v2 (scores + inventaire B6), moteur R1-R18, plan YAML affiché AVANT exécution (règle 3), sortie nommée PA-<CAS>-<seq>, rapport §8 + question §9",
      "commande": "« Fais le rendu iPhone 19 Pro Max qualité max de cette photo » + photo uploadée",
      "attendu": "sortie + rapport complet (analyse, diagnostic R, plan YAML, QC 12/12, limites honnêtes dont statut ANTICIPÉ, question §9)",
      "priorite": "S1"
    },
    {
      "id": "E2-preset-defaut",
      "description": "Rendu par défaut iphone19_max (§6.1, calibration ANTICIPÉE) déclenché par le moteur — jamais appliqué à l'aveugle (règle 2)",
      "commande": "analyse §1→§2 d'une photo standard avec demande génération 19",
      "attendu": "rendu_cible: iphone19_max dans le plan YAML + rendu conforme (extrapolation baseline 18, netteté étendue R18)",
      "priorite": "S1"
    },
    {
      "id": "E3-statut-anticipe-honnete",
      "description": "Honnêteté du statut ANTICIPÉ : demande de calibration labo / specs officielles génération 19 → réponse honnête (aucune spécification confirmée au 2026-10-20, calibration extrapolée jamais mesurée, bump v1.0.0 à la confirmation) ; jamais d'invention de specs",
      "commande": "« Quelles sont les specs officielles de l'iPhone 19 pour ce rendu ? »",
      "attendu": "déclaration explicite rumeur/extrapolation + sources (Macworld, MacRumors, Kuo…) — jamais de spécification inventée",
      "priorite": "S1"
    },
    {
      "id": "E4-r18-ouverture",
      "description": "Demande d'ouverture explicite → R18 : ouverture_cible au plan + avis honnête « simulation computationnelle, non optique » + critère QC 12",
      "commande": "« détache le sujet, ouverture ƒ/1.8 »",
      "attendu": "ouverture_cible dans le YAML + avis R18 au rapport §8",
      "priorite": "S2"
    },
    {
      "id": "E5-mode-serie",
      "description": "2+ photos → mode série §10 : sorties une par une, QC unitaire par sortie, rapport unifié, question unique finale",
      "commande": "« traite ces deux photos en rendu iPhone 19 »",
      "attendu": "PA-<CAS>-1 / PA-<CAS>-2 + rapport unifié + UNE question",
      "priorite": "S2"
    },
    {
      "id": "E6-garde-fous-b6",
      "description": "Fidélité stricte : expressions/orientations des têtes + inventaire B6 + décor (critères QC 1-4) ; aucune retouche spontanée après réponse « non » à §9 (fin de traitement) ; contrainte propriétaire « zéro modification/retouche » respectée",
      "commande": "QC comparatif original↔sortie puis réponse « non »",
      "attendu": "critères 1-4 PASS + fin de traitement sans itération",
      "priorite": "S1"
    },
    {
      "id": "E7-commandes-refus",
      "description": "Interface §13 : preset:iphone19 / preset:iphone19_max → preset défaut ; preset:iphone20 → REFUS (règle 14 — squelette SPÉCULATIF inactif)",
      "commande": "« preset:iphone20 »",
      "attendu": "refus explicite motivé (squelette section inactive, jamais de valeur par défaut)",
      "priorite": "S2"
    },
    {
      "id": "E8-routage-generations",
      "description": "Routage inter-générations : demande génération CONFIRMÉE courante (iPhone 18) → orienter le skill iphone18 ; demande iPhone 19 → présent skill ; jamais de traitement génération 19 sur demande générique sans mention (défaut confirmé = 18)",
      "commande": "« améliore cette photo qualité max » (sans mention de génération)",
      "attendu": "routage vers skill iphone18 (génération confirmée) — le présent skill exige une mention explicite génération 19",
      "priorite": "S1"
    }
  ]
}

TRIGGER_EVALS = [
  {"query": "Fais le rendu iPhone 19 Pro Max qualité max de cette photo.", "should_trigger": True},
  {"query": "Applique le preset iphone19_max sur cette photo de mariage.", "should_trigger": True},
  {"query": "Traite cette photo avec la génération suivante d'iPhone, qualité max.", "should_trigger": True},
  {"query": "Retouche ces deux photos de fête en mode série, rendu iPhone 19 max.", "should_trigger": True},
  {"query": "Améliore cette photo qualité max.", "should_trigger": False},
  {"query": "Fais le rendu iPhone 18 Pro Max de cette photo.", "should_trigger": False},
  {"query": "Restaure ce scan de photo ancienne des années 80, rendu propre et net.", "should_trigger": False},
  {"query": "Prépare cette photo en poster A4 à 300 DPI pour impression.", "should_trigger": False}
]
