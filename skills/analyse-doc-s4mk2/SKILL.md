---
name: analyse-doc-s4mk2
version: 1.3.0
category: ecosystem
language: fr
tags:
  - tsi
  - famille-tsi
  - agent-tsi
  - s4-mk2
  - djtt
  - analyse
  - documents-illustres
  - vue-partielle
  - vue-complete
  - referentiel-g2
  - pdf
  - adaptatif-types
  - coherence-croisee
description: >-
  Skill d'analyse des mappings TSI existants ET de TOUS les fichiers liés qui
  leurs sont associés (Kontrol S4 MK2) — pipeline 7 étapes sur un ZIP ou un
  dossier : inventaire exhaustif Y COMPRIS les sous-dossiers (l'échantillon
  de référence DJTT v2.1.0 porte Extra/), classification des TSI (mapping
  DeviceIO.Config.Controller vs préférences-FX vs préférences-layouts),
  analyse du mapping au format réel DIOM (référentiel G2, erratum Task 33 :
  CMAD embarqué, 163 noms DCBM, 393 commandes), résumé des TSI compagnons
  (FX Settings : mode 4 unités FX ; Layouts : decks C/D Remix), ROUTEUR
  ADAPTATIF aux types pour les non-TSI (v1.1.0 : PDF analysés en profondeur
  — texte via CMap ToUnicode bfchar/bfrange direct+tableau et codespacerange,
  pages, polices, mots-clés mapping ; illustrés JPG/PNG ; textes txt/md ;
  inconnus par signature magique — aucun muet), documents illustrés (vue
  complète QuickGuide, vues partielles) et vérification mécanique de la table
  de correspondance visuels↔contrôles (P1b, 22 noms) ; COHÉRENCE CROISÉE
  (v1.2.0 : les données extraites des non-TSI sont vérifiées contre les TSI
  sources de vérité — mentions numérotées hotcue/fx/deck/slot/slice/mod
  confrontées à l'univers S4 MK2 et aux noms/conditions du mapping, écarts
  HORS_UNIVERS/NON_CÂBLÉE = FAIL, SUPPORTÉE/INDETERMINABLE = honnêteté,
  couverture lexicale, illustrés via P1b) ; verdict PASS/FAIL + rapport JSON
  + batterie $FACON2 16/16. Échantillon secondaire : DREW
  (1 TSI + 3 PDF + 2 PNG). Membre de la famille TSI, ORCHESTRÉ PAR agent-TSI.
dependencies: []
read_when:
  - Déclencher quand la demande concerne : analyser un ZIP/dossier de mapping TSI avec TOUS ses fichiers liés (PDF, images, textes, sous-dossiers), relier des captures d'éléments du S4 MK2 à la vue d'ensemble (QuickGuide), classifier les TSI d'un pack (mapping/préférences), extraire les comptes d'un mapping réel (format DIOM), extraire le texte des PDF compagnons (liste d'assignation, description du fonctionnement), analyser les sous-dossiers d'un pack.
  - Déclencher si la demande mentionne : analyse-doc-s4mk2, documents illustrés, vue partielle, vue complète, QuickGuide, Manual, Freeze Mode Help, sous-dossiers du ZIP, DJTT, DREW, FX Settings, Layouts, PDF compagnon, Assignment List, Mapping Speech, adaptatif, types de fichiers, correspondance visuels↔contrôles, comptes G2, cohérence croisée, source de vérité, mentions numérotées, HORS_UNIVERS, NON_CÂBLÉE, attestations.
  - Ne pas déclencher pour concevoir une architecture (tsi-architect), valider la structure d'un TSI synthétique E1-E8 (tsi-validator), les couches SHIFT d'une architecture (multi-shift-architect), ni la documentation d'un mapping (midi-doc-expert).
---

## §0 — Contexte Système (SHARED v1.7.24)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.
> Langue : FRANÇAIS exclusif pour tous les échanges avec le propriétaire (règle d'or n°6 gen-plan — directive 2026-10-31, renforcée 2026-11-06) : dès le PREMIER mot de toute session ou reprise, la langue d'un message, d'un résumé de continuation ou d'un canal ne dérive JAMAIS la réponse ; toute dérive est corrigée immédiatement.

# analyse-doc-s4mk2 — Analyse des mappings TSI réels, de leurs documents et cohérence croisée

## §1 — Mission

Analyser MÉCANIQUEMENT les mappings TSI **existants** (format réel Traktor, blob DIOM) **et TOUS les fichiers qui leurs sont liés** — captures des éléments du S4 MK2, vue d'ensemble, PDF compagnons et tout type envoyé dans le même dossier, les **sous-dossiers** ou le même ZIP — afin de produire : un inventaire exhaustif, une classification des TSI (mapping contre préférences), les comptes du mapping contre le référentiel G2, l'analyse du contenu des fichiers non-TSI (**adaptation automatique aux types** : PDF → texte/pages/polices/mots-clés ; JPG/PNG → dimensions/rôle ; txt/md → texte ; inconnu → signature magique), la **cohérence croisée TSI ↔ non-TSI** (les données extraites des documents sont vérifiées contre les TSI, **sources de vérité** : mentions numérotées contre l'univers S4 MK2 et les noms/conditions du mapping — un document qui promet « Hotcue 9 » ou « FX 5 » non câblé produit un ÉCART FORT), la **relation vues partielles ↔ vue complète** (photo d'élément → zone du QuickGuide → contrôles TSI exacts → fonction de mapping), et un verdict exploitable machine-à-machine (`PASS`/`FAIL`, exit code, JSON). Le skill ne modifie jamais l'échantillon analysé (lecture seule, rejets propres sans traceback) et ne laisse **aucun fichier muet** (tout non-TSI est analysé, au minimum par signature).

**Orchestration** : membre de la famille TSI, **orchestré par `agent-TSI`** (matrice de routage : « analyser un mapping existant + ses documents illustrés » → ce skill). Hors orchestration, mobilisable directement en CLI (§3). Le skill assume la même discipline que les arbitres de la famille : jamais de verdict sans preuve mécanique, jamais d'interprétation non documentée (les hypothèses sont qualifiées comme telles — cf. §6).

## §2 — Pipeline (7 étapes)

| Étape | Action | Garde |
| --- | --- | --- |
| E1 | **Inventaire exhaustif** (ZIP ou dossier : tous membres, tailles, dossiers Y COMPRIS sous-dossiers) | 8 membres attendus sur l'échantillon de référence (6 fichiers + 2 dossiers) |
| E2 | **Classification** de chaque `.tsi` : `MAPPING` (Entry `DeviceIO.Config.Controller`) / `PRÉFÉRENCES-FX` (`Audio.FX.Selection`, `Status.4 FX Units`) / `PRÉFÉRENCES-LAYOUTS` (`Gui.Layouts2`, `Status.Select Layout`) / `PRÉFÉRENCES-GÉNÉRIQUES` / `ILLISIBLE` | 1/1/1 attendu sur la référence ; rejet propre des préférences par le moteur |
| E3 | **Analyse du mapping** (moteur `analyser_tsi_mk2.py`) : comptes + conformité référentiel G2 (10/10) + baseline stricte | erratum Task 33 intégré : 4960 lisibles / 666 illisibles / 393 commandes / 163 noms |
| E4 | **Résumé des compagnons** (Entries, clés structurantes) | FX Settings 96 Entry, Layouts 39 Entry attendus |
| E5 | **Fichiers liés non-TSI, ROUTEUR ADAPTATIF** (`ROUTEUR` ext→analyseur) : PDF → module `analyser-pdf-mk2.py` (texte via CMap ToUnicode bfchar/bfrange direct+tableau, codespacerange 1/2 octets, fallback cp1252 ; pages, polices, mots-clés mapping, métadonnées) ; jpg/png → dimensions (SOF/IHDR) + rôle ; txt/md → texte (utf-8/cp1252) ; **inconnu → signature magique stdlib** (jamais muet) | 3 illustrés attendus sur la référence (4000×2500, 858×892, 2149×2753) ; DREW : 3 PDF TEXTE_EXTRAIT (5507/5125/6589 car) + 2 PNG, 0 muet |
| E6 | **Correspondance visuels↔contrôles** (table P1b de `references/correspondance-visuels.md`) : présence et nb cid exacts des noms de contrôles des vues partielles dans les 163 noms définis | 22/22 attendus ; verdict `PASS` ssi (a) 1 mapping analysé, (b) G2 conforme si référence, (c) P1b sans écart, (d) aucun TSI illisible, (e) aucun PDF rejeté, (f) aucun écart de cohérence fort (E7) |
| E7 | **Cohérence croisée TSI (source de vérité) ↔ non-TSI** (`coherence-non-tsi-mk2.py`) : mentions numérotées du texte extrait (hotcue/fx/deck/slot/slice/mod/knob/button, collations de colonnes tolérées `M8M8`/`Knob 1FX`) vérifiées — HORS_UNIVERS (au-delà du référentiel matériel : decks A-D, FX 1-4, hotcues 1-8, slots 1-4, slices 1-8, mods M1-M8, knobs/boutons 1-3) et NON_CÂBLÉE (dans l'univers, absent des noms/conditions d'un TSI lisible) = ÉCARTS FORTS → FAIL ; SUPPORTÉE (présent des noms DCBM/conditions DCDT) ; INDETERMINABLE (CMAD illisibles > 20 % — honnêteté, jamais un FAIL) ; couverture lexicale des tokens (pivot réutilisé du module PDF) ; illustrés via table P1b si elle est sans écart | DREW : verdict COHÉRENT, 12 attestations SUPPORTÉES / 5 INDETERMINABLES (mods M4-M8), 0 écart ; TF-10 : fantôme « Hotcue 9 FX 5 Deck H Slice 12 » → 4 HORS_UNIVERS → FAIL |

## §3 — Usage

```bash
# Pipeline complet sur un ZIP (inventaire, classification, mapping, compagnons, illustrés, P1b)
python3 skills/analyse-doc-s4mk2/scripts/analyser-zip-mk2.py "<zip-ou-dossier>" --json rapport.json

# Moteur seul sur un .tsi de mapping (comptes + conformité G2 + self-test)
python3 skills/analyse-doc-s4mk2/scripts/analyser_tsi_mk2.py <fichier.tsi> --json rapport.json
python3 skills/analyse-doc-s4mk2/scripts/analyser_tsi_mk2.py <fichier.tsi> --self-test

# Module PDF seul (texte, pages, polices, mots-clés mapping) — v1.1.0
python3 skills/analyse-doc-s4mk2/scripts/analyser-pdf-mk2.py <fichier.pdf> --json rapport.json

# Module cohérence croisée seul : self-test mécanique embarqué — v1.2.0
python3 skills/analyse-doc-s4mk2/scripts/coherence-non-tsi-mk2.py --self-test

# Batterie de tests $FACON2 (cohérent, optimisé et fonctionnel) : TF-01..10 + TR-01..06
python3 skills/analyse-doc-s4mk2/tests/run_all.py [--zip CHEMIN] [--dir CHEMIN_DOSSIER] [--pdf-dir CHEMIN_DREW]
```

Exit codes : `0` PASS / `1` écart ou FAIL / `2` usage ou cible absente. Les rapports JSON sont byte-stables (idempotence ×2 vérifiée par TR-03).

## §4 — Échantillons et batterie

- **Référence (golden)** : `DJTT Kontrol S4 MK2 Custom Mapping v2.1.0` (ZIP du propriétaire) : 6 fichiers + 2 dossiers — mapping 1 810 459 o (conforme G2 10/10), `Extra/FX Settings.tsi` 7 517 o (96 Entry), `Extra/Layouts.tsi` 5 923 o (39 Entry), QuickGuide 4000×2500, Freeze Help 858×892, Manual 2149×2753 (978 634 o).
- **Échantillon secondaire (v1.1.0)** : `Kontrol S4 [DREW's MAPPING] - FX4(JogWheel) + Mode Freeze + Etc` (ZIP du propriétaire) : 1 TSI mapping tiers (device `Traktor.Kontrol S4.User`, 2360 DCBM) + **3 PDF compagnons** (`Drew's Assignment List.pdf` = liste d'assignations, titre « Button Map », OpenOffice Calc 2018 ; `Mapping Speech.pdf` = description narratif du fonctionnement ; `Mapping Speech-fr.pdf` = traduction française, PDFium 2026) + 2 PNG (description 1135×658, vue Traktor 3 1031×670). Hors référence G2 : le verdict FAIL y est mécaniquement correct (comptes comparés à la référence DJTT) ; la batterie y teste l'ADAPTATION (couverture 5/5 non-TSI, 0 muet), pas la conformité G2.
- Batterie `$FACON2` (`tests/run_all.py`) : **16 tests** — TF-01 inventaire, TF-02 classification, TF-03 comptes G2, TF-04 baseline stricte (4960/666/49), TF-05 table P1b (22 noms, cid exacts), TF-06 illustrés (dimensions+rôles), TF-07 PDF compagnons (3 PDF DREW : texte, mots, mots-clés), TF-08 adaptation automatique aux types (couverture 5/5, 0 muet), TF-09 cohérence croisée positive (DREW : 12 SUPPORTÉES / 5 INDETERMINABLES, 0 écart), TF-10 détection d'écart injecté (PDF fantôme → 4 HORS_UNIVERS → FAIL), TR-01 rejet préférences (rc=1 sans traceback), TR-02 blob corrompu (rejet contrôlé), TR-03 idempotence ×2 byte-stable, TR-04 cible absente (rc=2), TR-05 self-test moteur, TR-06 PDF : signature absente → rc=1 / sans texte → statut honnête. Journal JSON individuel par test (`tests/journal/`) + `synthese.json`. Échantillon introuvable = **FAIL explicite** (le skill ne ment jamais).
- Résultat de référence : **BATTERIE PASS (16/16)** ; module PDF idempotent ×2 byte-stable ; self-test cohérence 20/20.

## §4bis — Format réel Traktor 3.x : blob DeviceIO (v1.3.0, Task 44 — reconstitué Task 46)

- **Découverte** : les mappings Traktor 3.x ne sont PAS dans une section XML `<ControllerManager>` : ils vivent dans le **blob base64 `DeviceIO.Config.Controller`** (sections DEVS/DEVI/DDIF/DDIV/DDPT/DCMA/DCDT/CMAD/DCBM, chaînes UTF-16). Mesures sur 2 TSI réels : settings personnel du propriétaire (blob décodé 2 940 882 o — DCDT 3105, CMAD 11 596, DCBM 11 586, DEVI 9 : `Kontol S4 mk2 SEMITONE (default)`, `$Kontrol S4 _ Mon Mapping (Aout 2024)`, `DJTT Kontrol S4 MK2 Custom Mapping v2.1.0 (stewe update)`, `S4 MK2 MOTS Aout 2026` + Traktor.Kontrol S4MK2 Default/User) vs DJTT v2.1.0 (1 352 130 o — DCDT 345, CMAD 5 626, DCBM 5 627, DEVI 1).
- **Outils du chaînon** (`tsi-toolkit/scripts/`) : `task44-decoder-deviceio.py` (décodage stdlib, idempotent ×2), `task44-enricher-catalogues.py` (+`catalogue_interaktiv` : 524 commandes Interaktiv **CC BY 4.0**), `task44-valider-mapping-catalogue.py` (valide les commandes d'un .tsi contre le catalogue enrichi 393 DJTT + 524 Interaktiv, suggère les noms officiels — ex « Slice 1 » → « Slice Trigger 1 » id 810 — gère TSI 3.x blob ET format toolkit). Résultats réels : DJTT 429/440 · DREW 172/172 · freeze-e2e PASS_AVEC_RESERVES.
- **Versions embarquées** : 2.9.0 (R1257) / 3.0.3 / 3.2.1 9 / 3.11.1 17.
- **Lignage honnête (Task 46, 2026-11-04)** : la v1.3.0 d'origine (hôte-seule, session web-6058b3ba) a été perdue au recyclage sandbox ; la présente section est reconstituée depuis le rapport Task 44 §4 (contenu identique, formulation resserrée).

## §5 — Relations (famille TSI)

| Avec | Nature |
| --- | --- |
| `agent-TSI` | **Orchestration** : membre routé de la matrice (« analyser un mapping existant + documents illustrés » → ce skill) ; verdicts consommés par l'agrégation de l'agent |
| `tsi-validator` | Complémentarité de formats : le validateur couvre les TSI synthétiques écosystème (`NISYSTEM`) ; ce skill couvre les TSI réels (`NIXML`, blob DIOM) — écart E1 consigné dans la doc approfondie §7, évolution du validateur proposée (non appliquée) |
| `tsi-architect` | En amont : les comptes réels (163 noms, 345 conditions, top commandes `_(Mod)`) calibrent les conceptions |
| `multi-shift-architect` | En lecture : les 9 couches logiques du mapping réel (BASE, Shifts, Super FX, JogFX, Freeze, Echo Mods, Flux, Panic, Hotcue 5-8) alimentent l'analyse de couverture — lien CMAI↔condition non décodé (§6) |
| `midi-doc-expert` | En aval : les comptes et la table P1b nourrissent la documentation illustrée d'un mapping validé |
| `gen-plan` / `correct-work` | Verdicts machine mobilisables par les hooks de phase (analyse d'artefacts TSI réels dans un projet) |

**Règle d'or — recherche écosystème préalable (v1.1.0, consignée)** : avant d'écrire le module PDF, recherche mécanique dans l'écosystème (CLAUDE.md Règle 3) — registre KB (`KNOWLEDGE-repo/skills/KNOWLEDGE.md`), `153 scripts` (`grep FlateDecode|PyMuPDF|pdftotext` = **0 résultat**), skills plateforme `pdf` (ReportLab/Playwright/LaTeX — chaîne de PRODUCTION de documents, pas un analyseur stdlib) et `pdf-llm` (modes qwen/glm + pipeline post-PyMuPDF — dépendances SDK non embarquables dans un arbitre), `inter-scripts` (communication multi-langages, pas un analyseur). **Décision** : module stdlib propre `analyser-pdf-mk2.py` (contrainte famille TSI : stdlib, lecture seule, rejets propres, exit codes) — sémantique alignée sur le skill pdf plateforme, sortie JSON consommable par un canal one-shot `inter-scripts`.

**Provenance** : moteur issu de `scripts/zip-tsi/analyse-djtt-mk2.py` v1.1.0 (session Task 33, GO trace 1a197aaf0eb6557d) — self-test PASS ; table P1b ancrée sur les crops vérifiés (`crop-fx1-quickguide.png`, `crop-vignettes-manual.png`) et le doc approfondi `download/analyse-djtt-s4mk2-v2.1.0-approfondie.md` ; v1.1.0 (GO traces 1a198688435d6bf1 + 1a198840319c3ec5, session web-4f989063 2026-11-02) : routeur adaptatif + module PDF (échantillon DREW) ; v1.2.0 (traces 1a1989725d74c901 + 1a1989862dd46e61, même session) : cohérence croisée TSI↔non-TSI (module `coherence-non-tsi-mk2.py`, étape E7, univers S4 MK2 ancré, seuil CMAD 20 %, équation FX par decks consignée) — batterie TF-09/TF-10.

## §6 — Limites assumées (jamais masquées)

1. Lien CMAI ↔ condition **non décodé** : le candidat « index de condition » du payload CMAD (@44/@48) est une hypothèse qualifiée ; l'analyse multi-shift s'appuie sur les sources textuelles du pack (Manual, Freeze Help) et non sur une attribution mécanique par assignation.
2. Les 666 CMAD illisibles (11,83 %) : payloads de 120 o sans champ nom (erratum Task 33, reproductible) — les comptes G2 publiés 394/4970 contenaient un artefact non reproductible du décodeur perdu.
3. La reconnaissance des photos d'éléments non listées dans la table P1b reste **assistée** (libellés sérigraphiés → préfixe DCBM → vérification mécanique) : le skill vérifie, il ne devine pas.
4. `Status.Effect 4 Select` absent du FX Settings.tsi : constat brut, interprétation refusée.
5. **PDF (v1.1.0)** : PDF scannés (image) → `AUCUN_TEXTE_EXTRAIT` (consigné, statut honnête, pas de FAIL) ; PDF 1.5+ avec ObjStm → objets compressés non résolus (les 3 PDF DREW sont sans ObjStm) ; polices sans ToUnicode décodées cp1252 (approximation documentée) ; bfrange tableau + ordre du flux « dernier gagne » (sémantique lecteurs) ; espaces insécables U+00A0 possibles dans le texte extrait (code 0x01 des CMap PDFium).
6. **Types inconnus (v1.1.0)** : analysés par signature magique + taille seulement (pas de décodage) — statut « analysé sommairement » ; l'extension du routeur (`ROUTEUR`/`SIGNATURES`) est la voie canonique pour ajouter une profondeur d'analyse.
7. **Hors référence G2** : un mapping tiers (ex. DREW) est comparé à la référence DJTT — verdict FAIL mécaniquement correct (ce n'est pas l'échantillon de référence), les comptes réels restent intégralement rapportés.
8. **Cohérence croisée (v1.2.0)** : vérification LEXICALE et de PLAGE, pas sémantique — un document peut décrire un contrôle avec d'autres mots que les noms du TSI (les mentions non couvertes sont consignées NON_COUVERTE, jamais un FAIL) ; support des *commandes* indémontrable quand les CMAD sont majoritairement illisibles (DREW : 90,08 % → INDETERMINABLE consigné) ; pivot du vocabulaire en ANGLAIS uniquement — le Speech-fr est attesté sur les mentions numérotées seulement ; support des unités FX au-delà du max vu régit par l'équation « N ≤ max(unités vues) × nb de decks » (hypothèse de câblage par deck, consignée en sortie) ; mentions numérotées à la suite d'un chiffre collé (« 2024M8 ») potentiellement attestées à tort (risque résiduel consigné) ; illustrés sans OCR → cohérence via la table P1b seulement (une table en écart = non vérifiable, consigné).
