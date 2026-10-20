---
name: dessin-technique
version: 1.1.1
category: metier
language: fr
tags:
  - "#dessin-technique"
  - "#style-ca0"
  - "#capture-de-forme"
  - "#mise-a-lechelle"
  - "#image-generation"
  - "#filetage"
  - "#profondeur"
description: >
  Reproduit n'importe quelle pièce ou scène dans le style « dessin technique »
  (isométrie CAO flat-shaded, cotation normalisée) à partir d'un DNA de style
  mesuré. Fonction capture de forme : reconnaît les formes d'une pièce
  photographiée et déduit ses cotes grâce à une pièce de centime posée à côté
  (référence d'échelle). Fonction mise à l'échelle : harmonise pièce par pièce
  les facteurs d'un dessin multi-pièces quand les cotes sont connues. Fonction
  mesure de filetage (v1.1.1) : pas, Ø majeur et désignation ISO 261 d'une tige
  filetée photographiée de profil — ACF par latitude puis moyennée, invariante
  en phase entre stries (robuste à l'hélice réelle), garde anti-fallacieux hors
  table ISO. Fonction mesure de profondeur (v1.1.1) : profondeur d'un trou borgne
  circulaire à fond visible (ellipticité de l'ouverture + décalage du fond,
  projection orthographique ; validation trou-ness — un relief d'objet plat est
  rejeté).
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
  - Déclencher si la demande mentionne (v1.1.1) : filetage, pas de vis, visserie, tige filetée, désignation ISO, profondeur de trou, trou borgne
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
| T5 | mesure de filetage (v1.1.1, `--selftest`) | pas et Ø majeur ≤ 5 %, désignation ISO correcte — 4 cas : stries droites, hélice verticale déphasée, tige lisse → ABANDON, pas hors table ISO à signature forte → rapporté sans abandon |
| T6 | mesure de profondeur (v1.1.1, `--selftest`) | profondeur ≤ 8 %, Ø ≤ 5 %, inclinaison ±3° ; validation trou-ness active |

### §1.6 F4 — mesure de filetage (v1.1.1)

Tige/vis filetée photographiée **de profil** (+ pièce de centime pour l'échelle)
→ pas du filet, Ø majeur, désignation ISO 261.

- Entrée : `mesurer_filet.py <photo> --coin DENOM [--zone x0,y0,x1,y1]
  [--axe horizontal|vertical] [--diametre-mm X] [-o out.json]` — `--selftest` = T5.
- Pipeline : échelle monnaie (primitives F1 importées — discrimination
  pièce/tige par **remplissage de bbox** : cercle vu de face ≈ 0,785, objet plein
  de profil ≈ 1,0, indépendant des tailles relatives ; jamais d'upscale —
  l'interpolation polluerait les masques) → zone (défaut : bbox tige rognée
  10 % **le long de l'axe** — les extrémités d'une tige verticale sont en
  haut/bas) → **traces par latitude** (une trace par ligne/colonne objet) →
  détendance par trace → **ACF par latitude puis moyennée** (invariante en
  phase entre stries : l'hélice réelle décale les crêtes d'une latitude à
  l'autre et ANNULE le pic de l'ACF du profil moyenné — défaut v1.1.0 confirmé
  sur photo réelle ; la voie v1.1.0 reste rapportée en métrique secondaire
  `pic_profil_moyenne` pour tracer l'annihilation) → pic dominant (seuil 0,25,
  interpolation parabolique) → **pas** ; **Ø majeur** = extension perpendiculaire
  du masque ; **désignation** : table ISO 261 (`references/filets-normaux.md` —
  miroir de la table intégrée), critères Ø ±5 % ET pas ±max(10 %, 0,15 mm) →
  candidats triés + meilleur.
- Sortie JSON : `{echelle_px_mm, reference_echelle, filet:{pas_mm, pas_px_analyse,
  pic_autocorrelation, pic_profil_moyenne, lag_profil_moyenne_px, nb_latitudes,
  diametre_majeur_mm, hors_table_iso}, designation_candidats[], meilleur,
  erreurs_estimees}`.
- Tolérances : T5 — pas ≤ 5 %, Ø ≤ 5 % (synthétique) ; photo réelle : pas ±10 %.
- Gardes : aucune périodicité (pic < 0,25 ou profil constant) → ABANDON ;
  **anti-fallacieux (v1.1.1)** : pas hors table ISO avec pic < 0,45 → ABANDON
  explicite (un pas hors ISO n'est rapporté qu'à signature forte — éradique le
  pas fallacieux mesuré sur photo réelle en v1.1.0).
- Résolution : à ANALYSE_MAX (760 px) un filet fin sur photo pleine définition
  peut être sous-échantillonné (pas < 5 px analyse) → ABANDON honnête ; la voie
  est alors un **crop géométrie-préservé** (pièce + filetage seuls) pour ramener
  l'analyse en haute résolution (jamais d'upscale).
- Échelle : le bord de la pièce de référence rogné/ombré biaise px/mm de ±2-4 %
  (l'ombre gonfle la bbox) — préférer une pièce nette sur fond clair,
  contre-vérifier avec `--diametre-mm`.

### §1.7 F5 — mesure de profondeur (v1.1.1)

Trou borgne **circulaire** à fond visible (+ pièce de centime) → profondeur,
Ø d'ouverture, inclinaison de vue.

- Entrée : `mesurer_profondeur.py <photo> --coin DENOM --trou x0,y0,x1,y1
  [--diametre-mm X] [-o out.json]` — `--selftest` = T6.
- Pipeline (projection orthographique, d ≪ distance caméra) : échelle monnaie →
  masque intérieur (seuil adaptatif p5/p95 de la zone) → PCA des pixels →
  ellipse d'ouverture (2a, 2b) → inclinaison φ = acos(b/a) → fond visible
  (plus clair que la paroi ; érosion 4-connexe du masque — tue les anneaux
d'interpolation — compensation 1 bord) → extension du fond le long de l'axe
  mineur = 2b − δ → **profondeur = δ / (px_mm · sin φ)** ; **Ø bord = 2a / px_mm**.
- **Validation trou-ness (v1.1.1)** : le masque « fond » doit porter la
  signature d'un vrai fond — (1) dominante connexe ≥ 60 % (un fond réel est
  d'un seul tenant) ; (2) encastré : ne déborde pas du bord proche de
  l'ouverture (≤ 3 px) ; (3) contact far : la lèvre lointaine partage son
  contour entre ouverture et fond (écart ≤ max(4 px, 0,2·δ) — l'axe mineur PCA
  est orienté déterministiquement vers le fond, son signe étant arbitraire) ;
  sinon ABANDON explicite « signature de trou absente » — un relief d'objet
  plat (ex. frappe de monnaie) est rejeté au lieu de produire une profondeur
  fallacieuse (défaut v1.1.0 confirmé sur photo réelle).
- Sortie JSON : `{echelle_px_mm, reference_echelle, trou:{diametre_bord_mm,
  inclinaison_deg, profondeur_mm, profondeur_note, delta_px, b_sur_a,
  trou_ness:{dominante_pct, debord_proche_px, contact_far_px}}, erreurs_estimees}`.
- Tolérances : T6 — profondeur ≤ 8 %, Ø ≤ 5 %, φ ±3° (synthétique) ; photo
  réelle : profondeur ±15 %.
- Gardes : vue trop verticale (b/a > 0,97) → ABANDON (profondeur non séparable
  de l'ellipticité) ; fond non visible/non éclairé → ABANDON ; δ ≤ 1 px →
  profondeur 0 (trou traversant ou fond au ras, noté) ; trou-ness (1)/(2)/(3)
  non satisfaite → ABANDON.

## §2 — Spécification technique

- Stack : Python 3 (stdlib + PIL + numpy — autocorrélation, PCA, érosion binaire), z-ai CLI (génération), JSON.
- Emplacements : `{{SKILLS_ROOT}}dessin-technique/` — SKILL.md, style-dna.json,
  scripts/{capture_forme.py, mise_a_echelle.py, generer_dessin.py,
  mesurer_filet.py, mesurer_profondeur.py},
  references/{pieces-centimes.md, filets-normaux.md}, evals/evals.json,
  evals/trigger_evals.json.
- N3 (SHARED) : scripts Python uniquement.
- Limites assumées : F1/F2 — la détection de la pièce de monnaie suppose une pièce
  circulaire visible et séparée de la pièce à mesurer ; F4 — vue de profil
  requise, seuls le pas et le Ø majeur sont mesurables (le profil du filet :
  angle, relief, n'est pas mesurable sur photo simple) ; le pas est extrait par
  ACF par latitude (l'ACF du profil moyenné annule l'hélice réelle — pic
  secondaire rapporté pour traçabilité) ; un filet sous-échantillonné à
  ANALYSE_MAX → ABANDON + voie crop géométrie-préservé ; l'échelle peut être
  biaisée de ±2-4 % si le bord de la pièce de référence est rogné/ombré ; F5 —
  trou circulaire à fond visible et éclairé, projection orthographique (±8 %
  synthétique / ±15 % photo), la validation trou-ness exige un fond dominant
  encastré en contact du bord lointain — un relief d'objet plat est rejeté, trou
  elliptique ou fond occulté hors périmètre ; les autres cotes internes
  complexes ne sont pas mesurables sur photo simple — la spécification
  le documente (sortie `erreurs_estimees`).

## §3 — Relations

| Avec | Nature | Détails |
|------|--------|---------|
| image-generation | utilise | rendu de base via z-ai (CLI `z-ai image`) |
| skill-creator | conventions | structure SKILL.md/evals, >= 1.0.0 |
| correct-work | vérifié par | Mode CIBLE sur le skill ; tests T1-T6 |

## §4 — Conventions

Nommage kebab-case, version semver, tags `#token`, variables `{{VARIABLE}}`
(SHARED §1.2). Le DNA de style est un artefact versionné : toute modification
passe par re-mesure + `version_dna` + journalisation (R4).
