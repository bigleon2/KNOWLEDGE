---
name: dessin-technique
version: 1.3.0
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
  - "#trigo-euler"
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
  rejeté). Fonction voie géométrique déterministe (v1.3.0, F6) : nœud C++
  trigo-euler — 15 capacités mathématiques (trigonométrie, équations canoniques,
  dérivée/primitive/intégrale, séries de Fourier, théorème d'Euler [formule,
  rotation, projection isométrique, caractéristique], profil axial 2D de pièce
  de révolution avec aires/inerties/Guldin et cotes formatées françaises, modèle
  isométrique flat-shaded) — la géométrie est CALCULÉE (jamais devinée par le
  modèle d'image : proportions, cotes réelles et perspective exactes), appelable
  simultanément par plusieurs tâches (daemon socket NDJSON multi-clients,
  max_clients 8) depuis les scripts d'autres langages (registre inter-scripts).
dependencies:
  - skill: skill-creator
    version: ">=1.0.0"
    used_at: "conventions structurelles"
  - skill: image-generation
    version: ">=1.0.0"
    used_at: "génération du rendu de base (z-ai CLI/SDK)"
  - skill: inter-scripts
    version: ">=1.0.0"
    used_at: "registre du nœud trigo-euler + client is_client + orchestrateur (v1.3.0)"
read_when:
  - Déclencher quand la demande concerne : reproduire une image/pièce dans le style « dessin technique », générer un dessin technique coté, mesurer une pièce sur photo avec pièce de monnaie, mettre à l'échelle un dessin multi-pièces
  - Déclencher si la demande mentionne : dessin technique, style CAO, capture de forme, mise à l'échelle, cotes sur photo
  - Déclencher si la demande mentionne (v1.1.1) : filetage, pas de vis, visserie, tige filetée, désignation ISO, profondeur de trou, trou borgne
  - Déclencher si la demande mentionne (v1.3.0) : trigo-euler, calculs trigonométriques, équations canoniques, primitives, dérivées, intégrales, séries de Fourier, théorème d'Euler, angles d'Euler, projection isométrique, perspective, profil axial, pièce de révolution, aires, inerties, volume de Guldin, proportions exactes
  - Ne pas déclencher hors de ce périmètre (photos réalistes → image-generation/image-edit)
---

## §0 — Contexte Système (SHARED v1.7.33)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.
> Langue : FRANÇAIS exclusif pour tous les échanges avec le propriétaire (règle d'or n°6 gen-plan — directive 2026-10-31, renforcée 2026-11-06) : dès le PREMIER mot de toute session ou reprise, la langue d'un message, d'un résumé de continuation ou d'un canal ne dérive JAMAIS la réponse ; toute dérive est corrigée immédiatement.
> Règles d'or & lecture SHARED à l'exécution (directive propriétaire 2026-11-06 — SHARED §9) : tout skill/agent/script exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or de l'écosystème (résumé §9 — canonique gen-plan §1.5).
> Référence canonique skill/agent (directive propriétaire 2026-11-07 — SHARED §0/§1.2) : toute référence à « mon skill X »/« mon agent X » désigne la forme installée à la racine `skills/X/SKILL.md`, JAMAIS le prompt maître du corpus `@mon-ecosysteme/` (ex-nommé `@PM-SKILLS/`) — les PMs sont des spécifications générées mécaniquement (KO-L004), les skills installés sont les formes exécutables.

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
| T7 | nœud trigo-euler (v1.3.0, `--selftest`) | 15/15 capacités vérifiées à valeurs contrôlées (T01-T15, une par capacité) ; sortie byte-identique au re-jeu |
| T8 | daemon trigo-euler (v1.3.0, concurrence) | 4 clients × 25 requêtes = 100/100 ok via le daemon ; saturation 8+1 → « daemon sature » non-bloquant ; daemon.stop propre (socket supprimée) ; orchestrateur ×2 idempotent (sha16 identiques) |

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

## §1.8 F6 — voie géométrique déterministe (nœud C++ trigo-euler, v1.3.0)

**Douleur d'origine** (discussion « COOLING VOSS #2 », 2026-10-22) : le rendu
génératif z-ai est **stochastique** — proportions, cotes réelles, mise à
l'échelle et perspective non respectées (joint 5c : O-ring déplacé, hexagone
décentré, filets disproportionnés). Réponse : la géométrie est **calculée**
(trigonométrie, équations canoniques, théorème d'Euler), jamais devinée par
le modèle d'image.

- **Nœud** : `scripts/trigo-euler.cpp` (C++17, std uniquement, 0 dépendance)
  compilé en `scripts/trigo-euler` — commande EXACTE du registre :
  `g++ -O2 -std=c++17 -pthread -Wall trigo-euler.cpp -o trigo-euler`.
  Contrat : `skills/inter-scripts/scripts/registre.json` v1.0.0 (source de
  vérité) — interface JSON-NDJSON `{"op": …, "args": …}` ; modes one-shot
  (`--request F --out F`), stdin (NDJSON), daemon (socket UNIX
  `/tmp/trigo-euler.sock` + ready/pid files + max_clients 8 — au-delà :
  réponse non-bloquante « daemon sature ») ; déterminisme intégral (sorties
  %.10g, ordre d'insertion stable — idempotence R3).
- **Capacités** (inventaire mathématique intégral des 3 discussions d'origine —
  plan Task 58 §0-bis E13-5/6/7, mappage 15/15 sans calcul orphelin) :
  `trig.eval` (19 fonctions, degrés/radians), `trig.resoudre` (triangle
  rectangle SOH-CAH-TOA + Pythagore), `canonique.cercle` (circumcentre /
  moindres carrés Kåsa), `canonique.ellipse` (fit algébrique contrainte F=−1
  + valeurs propres 2×2 — centre, demi-axes, rotation, excentricité),
  `analyse.derivee` (différences centrées / Lagrange 3 points),
  `analyse.primitive` (polynôme formel / primitive définie),
  `analyse.integrale` (Gauss-Legendre 5 points composé — tolérance 1e-6 /
  Simpson sur points discrets), `fourier.serie` (coefficients par intégration
  Gauss composée) + `fourier.eval`, `euler.formule` (e^(iθ)), `euler.rotation`
  (matrices ZXZ/ZYZ/XYZ/ZYX + quaternion [w,x,y,z]), `euler.projection`
  (isométrie CAO azimut 45° / élévation 35,264° — ratio du petit axe d'un cap
  par **valeurs singulières** de la sous-application, vérification mécanique
  ≈ sin élévation : le ratio bbox d'une ellipse inclinée est FAUX),
  `euler.caracteristique` (angle/axe/quaternion depuis matrice, cas 0 et π),
  `piece.profil_2d` (profil axial de pièce de révolution : aires/inerties
  exactes de la section, volume Guldin-Pappus, contour fermé à **arêtes
  locales**, cotes **formatées françaises** Ø/mm — hexagone entre-pointes,
  gorges O-ring, chanfreins coniques, bores rapportés), `piece.modele_iso`
  (boîte / cylindre / révolution à facettes — palette DNA mesurée, painter
  **unifié faces+traits trié par profondeur**, faces émises seulement si
  normale vers la caméra [généralisation caps n′z > 0], arcs de cap en
  **moitié externe** par échantillonnage des secteurs visibles).
- **Auto-diagnostic** : `--selftest` = T7 (T01-T15, une par capacité, valeurs
  contrôlées — ex. Guldin exact sur cylindre, ratio cap ≈ sin 35,264°,
  ellipse 3/1,5/30° retrouvée à 1e-6).
- **Appels inter-langages** : `is_client.py` (canal auto — one-shot isolé,
  daemon paresseux si ≥ 2 tâches) ou orchestrateur multi-projets
  `orchestrer.py` (graph + fleet engineering) — skill inter-scripts v1.0.0.
- **Cas nominal** (session d'origine « VOSS COOLING », mission VOSS-C) : pièces
  de révolution filetées — raccords hydrauliques (joint 5c : cotes F1
  officielles 44,9 × 35,2 mm, filet G Ø 28,5 × 22,7, O-ring 22,7→23,9,
  hexagone entre-pointes 35,2 × 23,9→33,8, filet D M26×1,5 DKO VOSS, bores
  Ø 15,4/12,0/6,0 ; couples d'assemblage 40/120 N·m — cotation type « couple »).
- **Lignage honnête (R4)** : la v1.3.0 d'origine (2026-10-23, mission
  TRIGO-INTER-SCRIPTS, perdue au recyclage sandbox) est RECONSTRUITE (Task 58)
  avec ses enseignements de conception (valeurs singulières, Gauss 5 pts 1e-6,
  painter trié, caps n′z>0, arcs moitié externe, arêtes locales, polygone
  fermé O-ring, formatage français). La voie --geo Python d'origine
  (`geometry_from_cotes.py` + extension `generer_dessin.py --geo` + check T9)
  est PERDUE — suggestion de reconstruction ① de la session d'origine, hors
  contrat du registre (nœud C++).
- **Limites assumées** : `piece.*` couvre le profil extérieur (bores rapportés
  en cotes, pas soustraits des aires) ; `canonique.ellipse` = fit algébrique
  (biais connu sous bruit fort — points de contour propres requis) ; le rendu
  final (SVG/PNG) reste à la charge du script appelant — le nœud fournit les
  listes de rendu triées et les cotes formatées ; `--version` décrit le nœud.

## §2 — Spécification technique

- Stack : Python 3 (stdlib + PIL + numpy — autocorrélation, PCA, érosion binaire), z-ai CLI (génération), JSON ; **C++17** (nœud trigo-euler — std uniquement, 0 dépendance, compilation g++ verrouillée par le registre inter-scripts, std::thread + socket UNIX POSIX).
- Emplacements : `{{SKILLS_ROOT}}dessin-technique/` — SKILL.md, style-dna.json,
  scripts/{capture_forme.py, mise_a_echelle.py, generer_dessin.py,
  mesurer_filet.py, mesurer_profondeur.py, **trigo-euler.cpp + binaire
  trigo-euler**}, references/{pieces-centimes.md, filets-normaux.md},
  evals/evals.json, evals/trigger_evals.json.
- N3 (SHARED) : scripts Python par défaut — **exception déclarée** : le nœud
  C++ trigo-euler est le nœud inter-langages du registre inter-scripts v1.0.0
  (son existence, sa compilation et son interface y sont verrouillées).
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
  le documente (sortie `erreurs_estimees`) ; F6 — limites §1.8.

## §3 — Relations

| Avec | Nature | Détails |
|------|--------|---------|
| image-generation | utilise | rendu de base via z-ai (CLI `z-ai image`) |
| skill-creator | conventions | structure SKILL.md/evals, >= 1.0.0 |
| correct-work | vérifié par | Mode CIBLE sur le skill ; tests T1-T8 |
| inter-scripts | utilise | nœud trigo-euler déclaré au registre v1.0.0 (contrat verrouillé) ; appels via is_client.py / orchestrer.py |

## §4 — Conventions

Nommage kebab-case, version semver, tags `#token`, variables `{{VARIABLE}}`
(SHARED §1.2). Le DNA de style est un artefact versionné : toute modification
passe par re-mesure + `version_dna` + journalisation (R4).
