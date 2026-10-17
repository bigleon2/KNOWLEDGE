---
name: dessin-technique
version: 1.0.0
category: metier
language: fr
tags:
  - "#dessin-technique"
  - "#style-ca0"
  - "#capture-de-forme"
  - "#mise-a-lechelle"
  - "#image-generation"
description: >
  Reproduit n'importe quelle pièce ou scène dans le style « dessin technique »
  (isométrie CAO flat-shaded, cotation normalisée) à partir d'un DNA de style
  mesuré. Fonction capture de forme : reconnaît les formes d'une pièce
  photographiée et déduit ses cotes grâce à une pièce de centime posée à côté
  (référence d'échelle). Fonction mise à l'échelle : harmonise pièce par pièce
  les facteurs d'un dessin multi-pièces quand les cotes sont connues.
dependencies:
  - skill: skill-creator
    version: ">=1.0.0"
    used_at: "conventions structurelles"
  - skill: image-generation
    version: ">=1.0.0"
    used_at: "génération du rendu de base (z-ai CLI/SDK)"
read_when:
  - Déclencher quand la demande concerne : reproduire une image/pièce dans le style « dessin technique », générer un dessin technique coté, mesurer une pièce sur photo avec pièce de monnaie, mettre à l'échelle un dessin multi-pièces
  - Déclencher si la demande mentionne : dessin technique, style CAO, capture de forme, mise à l'échelle, cotes sur photo
  - Ne pas déclencher hors de ce périmètre (photos réalistes → image-generation/image-edit)
---

## §0 — Contexte Système (SHARED v1.7.7)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.

## §1 — Spécification fonctionnelle

### §1.1 DNA de style (source de vérité visuelle)

Le style est matérialisé dans `style-dna.json` — palette **mesurée** sur
l'image de référence `dessin technique.png` (fond #f8f8f8, faces dessus
lavande #d8d8f8, flancs gris #a8a8b0-#b8b8c0, traits/cotation #4b4b51),
isométrie CAO flat-shaded, cotation normalisée (lignes d'attache, flèches
pleines, Ø, mm, °). Le bloc `prompt_style_en` est injecté VERBATIM dans tout
prompt de génération (jamais paraphrasé — reproductibilité). Toute évolution
du style passe par une re-mesure de l'image de référence et un bump de
`version_dna` (traçabilité R4).

### §1.2 F1 — capture de forme

Photo d'une pièce (+ pièce de centime posée à côté, même plan) → spécification
de formes et cotes déduites.

- Entrée : `capture_forme.py <photo> [--coin 1c|2c|5c|10c|20c|50c|1e|2e] [--mode metal|sombre] [-o out.json]`
- Pipeline : segmentation (luminance + gradient, modes `metal` = pièce
  métallique texturée sur fond lisse clair, `sombre` = pièce sombre sur fond
  clair) → composantes connexes → détection de la pièce de monnaie
  (circularité ≥ 0,60, aspect 0,85-1,15, candidat le plus circulaire) →
  échelle px/mm = Ø_coin_px / Ø_coin_mm (table officielle
  `references/pieces-centimes.md`) → cotes de la pièce principale
  (bounding box mm) + trous internes (Ø mm).
- Sortie JSON : `{echelle_px_mm, coin:{denomination, diametre_mm, diametre_px, circularite}, piece:{largeur_mm, hauteur_mm, trous:[{diametre_mm}]}, erreurs_estimees}`.
- Tolérance contractuelle : erreur ≤ 5 % sur image conforme au protocole
  (§references) — vérifiée par `--selftest` (scène synthétique aux cotes connues).
- Garde : si aucune pièce de monnaie n'est détectée → ABANDON explicite avec
  cause (jamais d'échelle inventée) ; repli : `--diametre-mm X` si l'utilisateur
  fournit le Ø réel de l'objet de référence.

### §1.3 F2 — mise à l'échelle (pièce par pièce)

Cotes connues d'un dessin multi-pièces → facteurs d'échelle harmonisés.

- Entrée : `mise_a_echelle.py <spec.json> --cible-w W --cible-h H [--echelle-commune] [-o plan.json]`
- `spec.json` : `{"pieces":[{"id","dims_mm":{...},"poids":1.0}]}` — `poids` =
  part visuelle relative de la pièce dans le dessin (défaut 1/n).
- Pipeline : pour chaque pièce, `max_dim = max(dims_mm)` ; échelle propre
  `s_i = (part_i × surface_cible) / max_dim` ; mode `--echelle-commune` :
  `s = min(s_i)` (toutes les pièces à la même échelle — cas d'un dessin à
  l'échelle unique).
- Sortie JSON : par pièce `{id, echelle_px_mm, dims_px:{...}}` + contrôle de
  cohérence (ratios px/mm conservés à 1e-6 près).
- Tolérance contractuelle : vérifiée par `--selftest`.

### §1.4 F3 — génération dans le style dessin technique

- Entrée : `generer_dessin.py --spec scene.json --out img.png [--size 1344x768] [--check]`
- `scene.json` : `{"pieces":[{"id","forme":"description géométrique factuelle (primitives, proportions issues de F1/F2)"}], "scene":"disposition relative, assemblage", "annotations":[{"texte","x_px","y_px","type":"cote|couple|note"}]}`.
- Pipeline : prompt = `prompt_style_en` verbatim + description géométrique
  (SANS texte à rendre — le modèle d'image déforme le texte) → génération
  z-ai (`z-ai image` CLI) → **couche d'annotation PIL** (cotes, symboles Ø,
  couples en N·m) appliquée après rendu, suivant les conventions de cotation
  du DNA (couleur #4b4b51, flèches pleines, sans-serif fine) — le texte reste
  ainsi parfaitement lisible et contrôlé.
- `--check` : contrôle de conformité style du rendu (proportions palette vs
  DNA : fond clair dominant, faces grises présentes, lavande présente, traits
  sombres présents) → verdict JSON ; hors tolérance → régénération conseillée.

### §1.5 Tests contractuels

| Test | Objet | Critère |
|------|-------|---------|
| T1 | capture de forme (`--selftest`) | cotes déduites à ≤ 5 % des cotes connues |
| T2 | mise à l'échelle (`--selftest`) | ratios conservés, échelles cohérentes |
| T3 | conformité style (`--check`) | palette générée dans les tolérances DNA |
| T4 | idempotence | selftests ×2 → mêmes verdicts |

## §2 — Spécification technique

- Stack : Python 3 (stdlib + PIL + numpy), z-ai CLI (génération), JSON.
- Emplacements : `{{SKILLS_ROOT}}dessin-technique/` — SKILL.md, style-dna.json,
  scripts/{capture_forme.py, mise_a_echelle.py, generer_dessin.py},
  references/pieces-centimes.md, evals/evals.json.
- N3 (SHARED) : scripts Python uniquement.
- Limites assumées : la détection de la pièce de monnaie suppose une pièce
  circulaire visible et séparée de la pièce à mesurer ; les cotes internes
  complexes (profondeurs, filets) ne sont pas mesurables sur photo simple —
  la spécification le documente (sortie `erreurs_estimees`).

## §3 — Relations

| Avec | Nature | Détails |
|------|--------|---------|
| image-generation | utilise | rendu de base via z-ai (CLI `z-ai image`) |
| skill-creator | conventions | structure SKILL.md/evals, >= 1.0.0 |
| correct-work | vérifié par | Mode CIBLE sur le skill ; tests T1-T4 |

## §4 — Conventions

Nommage kebab-case, version semver, tags `#token`, variables `{{VARIABLE}}`
(SHARED §1.2). Le DNA de style est un artefact versionné : toute modification
passe par re-mesure + `version_dna` + journalisation (R4).
