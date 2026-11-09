# Historique par skill — dessin-technique

> **Version** : 1.0.0 — **Date** : 2026-10-18 (Task 10, session web-da654199 — directive propriétaire « bump v1.1.0 … puis teste cette nouvelle version »)
> **Version vivante (corpus)** : v1.3.0 — `skills/dessin-technique/SKILL.md` (bump MINOR Task 58, 2026-11-07 — nœud C++ trigo-euler)
> **Versions archivées** : 0 fichiers déplacés — v1.0.0 vit dans l'historique git du dépôt KNOWLEDGE (commits `b944a27` → `26de6c1`, 2026-10-17) ; sceau SHA-256 du SKILL.md v1.0.0 ci-dessous (R2 : consultatif, jamais source d'installation KO-L003)
> **Provenance** : journal créé à la première montée de version du skill (convention historiques-par-skill, README §2/§3 — Task 17-B)

## Famille DESSIN-TECHNIQUE — 4 versions (skill : dessin-technique)

**Particularité durable du skill** : unique skill métier de l'écosystème — style
« dessin technique » (isométrie CAO flat-shaded, DNA mesuré), mesure dimensionnelle
sur photo avec pièce de centime comme référence d'échelle, génération cotée
(rendu z-ai + annotations PIL en seconde passe).

| Version | Date | Améliorations implantées | Avantage par rapport à la version précédente |
|---------|------|--------------------------|----------------------------------------------|
| v1.3.0 | 2026-11-07 | **VERSION VIVANTE (corpus)** — Task 58 (différé « plancher dessin-technique >=1.3.0 ») : F6 voie géométrique déterministe — nœud C++ **trigo-euler** RECONSTRUIT selon le contrat registre inter-scripts v1.0.0 (la v1.3.0 d'origine, 2026-10-23 mission TRIGO-INTER-SCRIPTS Task ID 10, PERDUE au recyclage sandbox — lignage honnête, enseignements de conception conservés) : 15 capacités + echo + daemon.stop, C++17 std uniquement 0 dépendance, mini-JSON maison ordonné, interface JSON-NDJSON, modes one-shot/stdin/daemon (socket UNIX /tmp/trigo-euler.sock + ready/pid, max_clients 8, saturation non-bloquante « daemon sature »), déterminisme intégral (%.10g, ordre d'insertion stable) ; enseignements d'origine intégrés : ratio ellipse par **valeurs singulières**, Gauss-Legendre 5 pts (1e-6), painter **unifié faces+traits trié par profondeur**, caps n′z>0, arcs **moitié externe**, silhouette par **arêtes locales**, polygone fermé O-ring, **formatage français** des cotes (Ø/mm/N·m) ; SKILL.md §1.8 F6 + T7/T8 + §2 stack C++ + dépendance inter-scripts ; preuves tmp/mission-task58/trigo-node/ (selftest 15/15 ×2 byte-identique, 15 op via is_client, daemon concurrence 100/100 à ~0,1-0,7 ms, saturation 8+1, daemon.stop propre, orchestrateur ×2 sha16 identiques, cas vivant joint 5c 44,9 × 35,2 — harnais PASS 8/8 ×2 re-jeu identique) ; affinage par les 3 discussions d'origine (plan Task 58 §0-bis E13-5/6/7 — inventaire mathématique intégral mappé 15/15 sans calcul orphelin) ; cascade KO-L004 5 touches (SKILL.md, evals T7/T8, KB, pin ECO_SKILLS, historiques) | Le plancher inter-scripts >=1.3.0 est satisfait : le nœud inter-langages du registre est matérialisé (source + binaire + preuves) — la voie géométrique déterministe est de nouveau outillée : cotes réelles mesurées (F1/F4/F5) → calculs exacts (trigonométrie, canonique, analyse, Fourier, Euler) → rendu déterministe, contre le rendu génératif stochastique qui ne respectait ni proportions, ni cotes, ni perspective (douleur d'origine joint 5c) |
| v1.0.0 | 2026-10-13 | Version initiale (mission VOSS-C) : DNA de style mesuré sur l'image de référence (style-dna.json, palette 5 tons, prompt_style_en verbatim) ; F1 capture de forme (segmentation + détection monnaie circulaire hors bbox, échelle px/mm via diamètres officiels euro, trous par cavités relatives) ; F2 mise à l'échelle pièce par pièce (poids + mode commune) ; F3 génération (prompt DNA verbatim → z-ai → postpro flat 5 tons → annotations PIL) ; 3 scripts + references/pieces-centimes.md + evals T1-T4 ; correct-work CIBLE PASS 11/11 ; réinscrit au registre KB le 2026-10-17 (Task 8, commit b944a27) et ancré au socle d'installation (e185698) | — (point de départ) |
| v1.1.1 | 2026-10-18 | Task 12 (directive « (2) bump v1.1.1 » — application des 4 findings Task 11 confirmés par exécution sur photo réelle) : F4 — ACF par latitude puis moyennée (traces par latitude → détendance par trace → ACF normalisée par trace → moyenne des ACF — invariante en phase entre stries : l'hélice réelle décale les crêtes entre latitudes et annulait le pic de l'ACF du profil moyenné v1.1.0 — pic 0,20 dilué contre 0,482 par latitude, contrôle opérateur 3 méthodes) ; ancienne voie conservée en métrique secondaire (pic_profil_moyenne — traçabilité annihilation) ; garde anti-fallacieux (0 candidat ISO ET pic < 0,45 → ABANDON — éradique le pas fallacieux 0,72 mm/pic 0,363 de la Task 11) ; biais bord de pièce documenté (±2-4 % si bord rogné/ombré). F5 — validation trou-ness (dominante connexe ≥ 60 % du fond + encastrement bord proche ≤ 3 px + contact bord lointain ≤ max(4 px, 0,2·δ) — la lèvre far partage son contour entre ouverture et fond) → ABANDON « signature de trou absente » — éradique la mesure fallacieuse 5,35 mm sur le relief frappé d'une pièce plate. Selftest T5 étendu à 4 cas (droites / hélice verticale déphasée / lisse ABANDON / hors-table-forte rapportée sans abandon) ; test décisif sur la photo réelle Task 11 : pas vrai 1,0 mm M8x1 mesuré par le SKILL (éradique la contre-vérification opérateur hors-skill), image tournée concordante, P1 ABANDON trou-ness | Rends autonome le skill sur les défauts que le test photo réel a révélés : le pas se mesure désormais sur la photo qui échouait en v1.1.0 (plus besoin de contre-vérification opérateur), et les objets plats texturés ne produisent plus de profondeur fallacieuse —PATCH sans nouvelle fonction (F1-F5 inchangés en périmètre) |
| v1.1.0 | 2026-10-18 | Task 10 : F4 mesure de filetage (mesurer_filet.py : pas par autocorrélation du profil détendu — moyenne glissante normalisée aux bords — pic dominant + interpolation parabolique ; Ø majeur ; désignation ISO 261, table references/filets-normaux.md ; discrimination pièce/tige par remplissage de bbox ; jamais d'upscale) ; F5 mesure de profondeur (mesurer_profondeur.py : trou borgne circulaire à fond visible — ellipse d'ouverture par PCA, φ = acos(b/a), fond plus clair isolé par érosion 4-connexe + compensation 1 bord, profondeur = δ/(px_mm·sin φ)) ; evals T5/T6 (S1) + trigger_evals 6→8 ; read_when/description/tags étendus ; gardes ABANDON explicites (périodicité absente, vue trop verticale b/a > 0,97, fond non visible) ; tests : T5/T6 PASS ×2 idempotents, vivants M12×1,75 / M26×1,5 (DKO VOSS) / Ø20-p12-φ35 PASS, non-régression T1-T4 + F1/F2/F3 vérifiée (SHA v1.0.0 des 5 fichiers intacts) | Lève une partie de la limite documentée « profondeurs/filets non mesurables » (SKILL.md §2 v1.0.0) de façon contractuelle et testable ; les vis/rondelles deviennent mesurables (pas, Ø, profondeur) sans instrumentation |

Sceau d'identité v1.0.0 (R2/R4 — consultatif, l'original vit en git dépôt) :
`SKILL.md` SHA-256 = `cc06940cf4f005fc0db9733ea78162143ff457dbb6abbab245149ec710b3f9a7`
`(capture_forme.py` = `c570d98f1a8465c4…`, `mise_a_echelle.py` = `94d7c3f23b7ea382…`,
`generer_dessin.py` = `fd0f6f16c043242c…`, `style-dna.json` = `f58741ab5fb04434…`,
`pieces-centimes.md` = `c833bae5175f8aee…` — fichier complet tmp/mission-dessin-technique/sha-avant.txt).

Révisions documentaires de la famille (sans changement de version) : Task 9
2026-10-18 (test de bout en bout v1.0.0 : 9/9 PASS — T1-T4, F1/F2/F3 vivants,
déclencheurs 6/6, arbitres 100 % ; artefact dessin-technique-test-bride.png).

Sceaux d'identité v1.1.0 (R2/R4 — consultatifs, capturés AVANT le bump v1.1.1,
l'original vit en git dépôt, commit `7e67c7e`) :
`SKILL.md` SHA-256 = `07eab6fb0f058572ae1a9061d72a926dcd5927e0a36c52b40b2d7abdeb8353d8`
(`mesurer_filet.py` = `0eebac31c2e4cb36…`, `mesurer_profondeur.py` = `fe47c38e6bcc804f…` —
fichier complet tmp/mission-dessin-technique/sha-avant-v111.txt).

Sceaux d'identité v1.1.1 (R2/R4 — consultatifs, capturés AVANT le bump v1.3.0,
l'original vit en git dépôt, commit `a988f51` — état certifié Task 60) :
`SKILL.md` SHA-256 = `6751d98b0ead7bbd4bc621a5defcf0658a64c223db5eaddc5cf106925ee4729d`
(`capture_forme.py` = `523664e70852d29e…`, `mise_a_echelle.py` = `558eed4d741e8390…`,
`generer_dessin.py` = `0f77f53172fcecb6…`, `mesurer_filet.py` = `1beb4f109c57fe6f…`,
`mesurer_profondeur.py` = `1105ea4609ff76ca…`, `evals.json` = `6c784ad130c5a4e6…` —
en-têtes contexte système propagés depuis les sceaux v1.0.0, scripts
fonctionnellement inchangés depuis v1.1.1 ; les sceaux diffèrent des v1.0.0/v1.1.0
uniquement par la propagation des en-têtes §0, mécanisme écosystème).
