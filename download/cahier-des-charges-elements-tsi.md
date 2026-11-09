# Cahier des charges — Éléments TSI des discussions QWEN (génération/optimisation $facon)

> **Version** : 1.0.0 · **Statut** : BROUILLON
> **Date** : 2026-11-02 · **Rédigé par** : session web-6058b3ba (gen-plan Task 39 / G2, skill cahier-des-charges M1+M2) · **Validé par** : en attente propriétaire (M3 interne exécuté — périmètre dérivé intégralement de directives explicites)
> **Sources** : directive propriétaire verbatim (mission Task 39) · rapport G1 `download/rapport-dedoublonnage-qwen.md` (inventaire E1-E9, 10 lignées QWEN) · analyse DJTT `download/analyse-djtt-s4mk2-v2.1.0-approfondie.md` · Google Drive mapping TSI (base de connaissance).

## 1. Contexte et problématique

Le propriétaire a mené, entre mars et octobre 2026, **10 lignées de discussions** (principalement avec QWEN, une avec Z.ai — L10) consacrées à la création d'outils et d'agents pour le mapping TSI du contrôleur **Traktor Kontrol S4 MK2** sous **Traktor Pro 3.11**. Ces discussions ont produit de nombreux éléments — générateurs de TSI (v7.7.9, 1 297 lignes), éditeur modulaire S4 MK2 v7 (parser NIXML, Karnaugh, virtual MIDI), système Multi_SHIFT/Méga Couche (modifiers M1-M4, Pseudo-TSI CSV), Ultra Prompt Maître `tsi-agent.md` (TSI_Engine, zip-tsi), bibliothèque multi-IA (`@Optimiser_Script_Python` + 6 plateformes), vision « Mapping Studio v11 » (React + DSL + presets), et un socle de connaissance CMDR (Traktor Commands, enums).

En parallèle, l'écosystème KNOWLEDGE a développé une **couche méthodologique TSI mature et validée** : la famille orchestreur-tsi / tsi-architect / tsi-validator / multi-shift-architect / midi-doc-expert / analyse-doc-s4mk2 (batterie 16/16 PASS, Tasks 33-36), adossée au mapping réel DJTT v2.1.0 (référence mécanique : NIXML, DCBM 5 626, 345 conditions, 9 couches multi-shift). **Mais les outils exécutables créés dans les discussions n'ont jamais été consolidés dans l'écosystème** : ils sont dispersés en fragments de code dans des exports de chat, redondants entre eux (trois générateurs, deux validateurs, quatre convertisseurs), parfois incohérents avec le format réel (DJCONFIG vs NIXML), et sans tests ni idempotence vérifiable.

La douleur : le propriétaire dispose d'un savoir-faire d'outillage TSI riche mais **non matérialisé, non vérifié et non intégré** — chaque besoin de génération de mapping repart de fragments de discussion. L'opportunité : générer $facon (cohérent, optimisé, fonctionnel) ces éléments en les **convergeant** avec la famille TSI existante et le référentiel DJTT, avec la base de connaissance Google Drive (manuels Traktor 3.9 Mapping FR/EN, S4 MK2 FR, Controller Editor) pour affiner la précision.

## 2. Objectifs et indicateurs de succès

| Objectif | Indicateur de succès | Cible mesurable |
|----------|---------------------|-----------------|
| O-1 : Matérialiser l'outil central TSI (convergence E2+E3+E8) | Toolchain Python modulaire opérationnelle | Tous les modules s'exécutent (CLI) ; suite de tests **PASS** ; idempotence ×2 byte-stable |
| O-2 : Générer des TSI réellement importables | TSI généré conforme au format réel | Fichier de test généré **PASS** à l'analyseur réel du format NIXML (analyse-doc-s4mk2 arbitre) ; structure alignée sur la référence DJTT |
| O-3 : Pas de collision anti-conflits | Détection Karnaugh/collisions opérationnelle | Injection d'un conflit volontaire → détecté (test négatif) ; mapping sain → 0 faux positif |
| O-4 : Générer l'Ultra Prompt Maître portable (E4) | `tsi-agent.md` + `zip-tsi` produit | Prompt maître idempotent (marqueurs [NOUVEAU]/[MISE_A_JOUR]/[INCHANGE]) ; zip-tsi reconstruit par script ×2 identique |
| O-5 : Générer la bibliothèque multi-IA (E6) | Bibliothèque @processus + 6 plateformes | Chaque plateforme a son prompt ; source de vérité unique (core) ; re-génération ×2 identique |
| O-6 : Vérifier optimisés les éléments existants (E1, E9, E5-méthode) | Audit croisé + verdicts | Tableau élément-par-élément avec verdict (OPTIMISÉ / corrigé + arbitres re-PASS) ; batteries existantes re-jouées **PASS** |
| O-7 : Toute la chaîne validée mécaniquement | Verdicts arbitres | correct-work(groupe) PASS par groupe ; correct-work(projet) PASS ×2 (G4, G6) ; tests fonctionnels rapport PASS |

## 3. Parties prenantes et rôles

| Partie | Rôle | Attendu / responsabilité |
|--------|------|--------------------------|
| Propriétaire | Demande et valide | Valide le présent CDC (M3), reçoit les livrables dans `download/`, intègre GitHub (KO-L009 : push = propriétaire), fournit le re-partage de la discussion `b6170b8b` si souhaité |
| Session Z.ai (exécutant) | Réalise | Génère/optimise les éléments selon ce CDC, exécute les tests, consigne worklog et rapports |
| Famille TSI (écosystème) | Cadre et arbitres | tsi-validator (PASS/FAIL des TSI), analyse-doc-s4mk2 (format réel), multi-shift-architect (couverture couches), orchestreur-tsi (routage) |
| correct-work | Vérification | Verdicts CIBLE par groupe, PROJET aux jalons G4/G6 |

## 4. Périmètre

**Inclus**
- Convergence E2+E3+E8 en **une toolchain TSI unique** (engine NIXML lecture/écriture, base de commandes Traktor 3.11/CMDR + MIDI S4 MK2, générateur par presets JSON, import Pseudo-TSI CSV, validateur branché sur l'existant, Karnaugh anti-conflits, CLI, convertisseurs TSI↔JSON, export DL/CSV) ;
- Génération **E4** : `tsi-agent.md` (Ultra Prompt Maître idempotent, optimisé exécution Z.ai/GLM) + script de construction de `zip-tsi.zip` ;
- Génération **E6** : bibliothèque multi-IA `@processus` (5 processus historiques + core + 6 plateformes QWEN/CLAUDE/CHATGPT/COPILOT/PERPLEXITY/GEMINI) ancrée sur les skills écosystème existants (correct-py, script-creator) ;
- Génération **E7 $facon outillée** : module « studio » de la toolchain (presets, DSL minimal, `audit_log.md` auto-évolutif, export documentation) + documentation d'architecture v11 — l'interface React complète reste une extension documentée, pas un livrable (voir Exclus) ;
- Vérification d'optimisation **E1** (midi-doc-expert : persona + chaîne doc + dictionnaire TRAKTOR 3.11 + mode GENERAL) et **E9** (famille TSI : batteries re-jouées) ;
- Recherches web ciblées + extraction Google Drive pour affiner la précision (spécifications MIDI S4 MK2, commandes Traktor 3.11, interop CMDR).

**Exclus (explicite)**
- Application React complète du Mapping Studio v11 (l'usage visé — créer des mappings — est couvert par le module studio CLI ; une UI web relèverait du skill fullstack-dev sur demande dédiée — extension documentée, pas silencieuse) ;
- Modification des PDF/documents sources du propriétaire (originaux `upload/` intouchables) ;
- Push/commit GitHub (KO-L009 point 5) ;
- Ré-analyse complète du ZIP DJTT (R4 — l'analyse approfondie existante fait foi) ;
- Réactivation du matériel MIDI physique (aucun contrôleur branché au sandbox — les tests « virtual MIDI » se limitent à la simulation logique) ;
- Génération de nouveaux mappings musicaux complets pour usage DJ (l'objectif est l'OUTILLAGE ; un mapping de démonstration suffit aux tests).

## 5. Exigences fonctionnelles (EF)

| ID | Exigence | Source | Critère d'acceptation |
|----|----------|--------|----------------------|
| EF-01 | La toolchain lit un fichier .tsi au **format réel NIXML** (racine + device + mappings) et en produit une représentation structurée (JSON) | L4 (parser NIXML) + DJTT §7 | `python3 -m tsi_toolkit inspect <DJTT.tsi>` sort un JSON comptant DEVI=1 et le même nombre de mappings que l'arbitre (±0) |
| EF-02 | La toolchain **génère** un .tsi valide depuis un preset JSON (device, mappings, conditions, LED) | L2/L4 (générateurs) | Le TSI généré passe `valider-tsi.py` (verdict PASS) et l'inspection EF-01 roundtrip (générer→lire = identique) |
| EF-03 | La toolchain importe un **Pseudo-TSI CSV** (format des discussions, séparateur `;`) et le convertit en preset interne puis en .tsi | L8 (csv_to_tsi_converter) | Un CSV d'essai de 23 lignes (celui de L8) → .tsi généré ; 23 mappings retrouvés à l'inspection |
| EF-04 | La toolchain **détecte les conflits** d'allocation MIDI (même canal/note/CC utilisé deux fois sans condition distincte) et de modifiers (incohérences d'états) | L4 (Karnaugh) + E5 | Test positif : conflit injecté → signalé ; test négatif : mapping DJTT réel → 0 conflit déclaré |
| EF-05 | La toolchain vérifie la **couverture multi-couches** (chaque contrôle × chaque couche, aucune couche morte) en s'appuyant sur la méthode du skill multi-shift-architect | L6/L7/L8 + E5 | Matrice de couverture générée ; test avec couche morte volontaire → détectée |
| EF-06 | La toolchain exporte un TSI vers **JSON** (et inversement) sans perte | L4 (tsi_to_json) | Roundtrip JSON→TSI→JSON byte-identique (ou sémantiquement identique : mêmes comptes et valeurs) |
| EF-07 | La toolchain expose une **CLI** cohérente (`inspect`, `generate`, `validate`, `convert`, `coverage`, `presets`) avec aide en français | L2 (tsi-cli) | `--help` par sous-commande ; exécution de bout en bout d'un scénario documenté sans erreur |
| EF-08 | La base de **commandes Traktor 3.11 + valeurs MIDI S4 MK2** est embarquée en données structurées (JSON) et documentée | L3 (Traktor Commands) + Drive | `data/commandes-traktor.json` charge en < 1 s ; ≥ 200 commandes [HYP-01 : périmètre calibré sur le référentiel DCBM DJTT + manuels Drive] |
| EF-09 | `tsi-agent.md` (E4) est un Ultra Prompt Maître **idempotent** qui régénère l'écosystème TSI (toolchain + famille) avec marqueurs `[NOUVEAU]/[MISE_A_JOUR]/[INCHANGE]` et consigne la source de vérité `zip-tsi.zip` | L10 | Présence des 3 marqueurs ; un état existant → sorties majoritairement `[INCHANGE]` (2ᵉ exécution) |
| EF-10 | Le script `construire-zip-tsi.py` construit `zip-tsi.zip` (toolchain + manifestes + exemples) de façon **déterministe** | L10 (generate_zip_tsi.py) | Construction ×2 → sha256 identiques |
| EF-11 | La bibliothèque multi-IA (E6) fournit le core `@processus` (5 processus dont `@Optimiser_Script_Python`) + 1 déclinaison par plateforme (6), générées depuis une source unique | L2 | `tools/generate_prompts.py` ×2 → sorties identiques ; 6 plateformes présentes ; core unique sans duplication |
| EF-12 | La bibliothèque multi-IA **réutilise** les compétences écosystème (correct-py pour l'optimisation Python) plutôt que de les dupliquer | R4 écosystème | Le core cite correct-py comme exécutant ; aucun code d'arbitre dupliqué |
| EF-13 | Le module « studio » (E7) applique des **presets** (bloc/deck/paramètre), compile un **DSL minimal** (lignes `contrôle -> fonction [couche]`) et produit un `audit_log.md` des écarts/ajustements | L9 | Scénario documenté : preset appliqué → TSI généré (EF-02) + audit_log.md créé avec ≥ 1 entrée réelle |
| EF-14 | L'audit d'optimisation E1 confirme ou corrige midi-doc-expert sur 3 points des discussions : dictionnaire TRAKTOR 3.11, mode GENERAL (au-delà du Freeze), chaîne PDF illustrée | L1 | Rapport d'audit : 3 points vérifiés avec statut (COUVERT/correctif appliqué/écart documenté) |
| EF-15 | L'audit E9 re-joue les batteries existantes de la famille TSI (non-régression confirmée après les livrables) | E9 + Tasks 34-36 | Batterie $FACON2 16/16 PASS re-exécutée après G3 ; verdict consigné |

## 6. Exigences non-fonctionnelles (ENF)

| ID | Exigence | Source | Critère d'acceptation |
|----|----------|--------|----------------------|
| ENF-01 | Python **stdlib uniquement** pour toute la toolchain et les scripts (zéro dépendance pip) | N3 écosystème | `grep -rE "^[[:space:]]*import (?!json|csv|xml|argparse|…)"` → 0 import tiers ; scripts s'exécutent sur Python 3.10+ |
| ENF-02 | **Idempotence ×2** : chaque générateur re-joué produit un résultat byte-identique (R6) | R1-R6 | sha256 des sorties identiques entre 2 exécutions (EF-10, EF-11 + TSI générés) |
| ENF-03 | **Performance** : inspect/generate sur le DJTT réel (1,8 Mo) < 10 s ; validate < 5 s | $facon | Mesure `time` consignée au rapport de tests |
| ENF-04 | **Traçabilité écosystème** : livrables en français, chemins kebab-case, worklog alimenté, scripts persistés `scripts/` | Conventions §5 gen-plan | Contrôle correct-work(groupe) par lot |
| ENF-05 | **Non-régression famille TSI** : aucune modification des skills existants sans cascade KO-L004 complète si version | R2 + KO-L004 | Si version bumpée : arbitres replay PASS ×2 ; sinon : skills byte-identiques |
| ENF-06 | **Sécurité** : aucun identifiant/secret dans les livrables ; originaux jamais modifiés | KO-L009 | Scan des livrables : 0 secret ; `upload/` intègre |
| ENF-07 | **Portabilité** : toolchain utilisable hors écosystème (zip-tsi autonome) tout en restant intégrée (KB, references) | L10 (portabilité Z.ai) | zip-tsi contient README d'exécution autonome ; écosystème : entrée KB + references croisées |

## 7. Contraintes

- **Techniques** : Python 3.10+ stdlib (ENF-01) ; format TSI Traktor Pro 3.11 (NIXML réel — référence DJTT, PAS le format DJCONFIG des discussions L8) ; contrôleur cible S4 MK2 (mode MIDI CC/Note) ; KB et PM de l'écosystème = conventions obligatoires.
- **Réglementaires** : dépôt privé personnel — aucune donnée personnelle dans les livrables ; licences : les éléments dérivés des discussions QWEN appartiennent au propriétaire ; le dépôt externe CMDR (GPL) sert de **référence de lecture** uniquement — aucun code copié (écriture originale).
- **Budgétaires** : budget #token du plan Task 39 (≈ 72 000, surveillance resource-monitor continue) ; aucune ressource payante externe.
- **Temporelles** : chaîne Task 39 (G2→G7) — aucune échéance externe ; la fenêtre sandbox impose de clôturer avant épuisement du contexte (ordres de priorité : LOTS B > C > D > E > audits A si pression).

## 8. Livrables attendus

| Livrable | Nature / format | Critère de complétude |
|----------|----------------|----------------------|
| L-1 : le présent CDC | Markdown 12 sections | M3 validé (grille complète, critères exécutables) |
| L-2 : rapport G1 (dédoublonnage/références) | Markdown | **DÉJÀ LIVRÉ** (G1) |
| L-3 : toolchain `tsi-toolkit/` | Python stdlib + tests + README + données commandes | EF-01→EF-08, ENF-01→ENF-03 ; suite tests PASS |
| L-4 : `tsi-agent.md` + `construire-zip-tsi.py` + `zip-tsi.zip` | Prompt maître + script + archive | EF-09, EF-10 |
| L-5 : bibliothèque multi-IA `bibliotheque-skills-ia/` | Core + 6 plateformes + générateur | EF-11, EF-12 |
| L-6 : module studio + doc architecture v11 | Module toolchain + Markdown | EF-13 |
| L-7 : rapport d'audit éléments existants (E1/E9/E5) | Markdown + verdicts arbitres | EF-14, EF-15 |
| L-8 : rapport de tests fonctionnels | Markdown, verdicts PASS/FAIL exécutables | D010 (batterie G5) |
| L-9 : rapport final de couverture | Markdown, tableau E1-E9 | D009 |
| L-10 : clone-chat de clôture | Markdown auto-suffisant | D012 |

## 9. Jalons et planning indicatif

| Jalon | Contenu | Dépend de |
|-------|---------|-----------|
| J-1 : CDC validé (M3) | L-1 | G1 (inventaire) |
| J-2 : base de connaissance prête | Recherches web + extraits Drive (T3.1.1, T3.1.2) | J-1 |
| J-3 : toolchain générée + tests unitaires verts | L-3 (+module studio L-6) | J-2 |
| J-4 : tsi-agent + zip-tsi + bibliothèque multi-IA | L-4, L-5 | J-3 (contenu à empaqueter) |
| J-5 : audits éléments existants | L-7 | J-3 (toolchain comme instrument de vérification) |
| J-6 : correct-work(projet) #1 | Verdict G4 | J-3→J-5 |
| J-7 : tests fonctionnels robustes + optimisations | L-8 (G5) | J-6 |
| J-8 : correct-work(projet) #2 | Verdict G6 | J-7 |
| J-9 : rapport final + clone-chat | L-9, L-10 (G7) | J-8 |

## 10. Critères d'acceptation

| Lot / exigences | Critère | Vérification |
|-----------------|---------|--------------|
| Lot B — toolchain (EF-01, EF-02, EF-03, EF-04, EF-05, EF-06, EF-07, EF-08 ; ENF-01, ENF-02, ENF-03) | Suite de tests + scénario DJTT réel | `python3 -m unittest` (ou équivalent stdlib) → PASS ; inspect/generate/validate sur `work/djtt/…v2.1.0.tsi` → sorties conformes ; temps < seuils ENF-03 |
| Lot C — tsi-agent/zip-tsi (EF-09, EF-10) | Idempotence marqueurs + archive | Re-exécution simulée → [INCHANGE] dominant ; sha256 zip ×2 identiques |
| Lot D — bibliothèque multi-IA (EF-11, EF-12) | Génération déterministe + ancrage | `generate_prompts.py` ×2 identiques ; core cite correct-py |
| Lot E — studio (EF-13) | Scénario preset→TSI→audit | Scénario documenté exécuté PASS |
| Lot A — audits (EF-14, EF-15) | 3 points E1 + batteries E9 | Rapport L-7 : statuts tranchés ; batterie 16/16 PASS re-jouée |
| Transverse (ENF-04…ENF-07) | Conventions + sécurité + non-régression | correct-work(groupe) par lot ; scan secrets ; diff skills byte-identiques (ou cascade KO-L004 documentée) |

## 11. Glossaire

| Terme | Définition |
|-------|------------|
| TSI | Fichier de mapping Traktor (XML natif Traktor Pro 3.11, format réel dit **NIXML** — cf. racine du mapping DJTT) |
| NIXML | Format réel des .tsi DJTT (≠ DJCONFIG utilisé dans les discussions L8, ≠ NISYSTEM théorique du validateur historique) |
| DIOM / DCBM / CMAD | Structures binaires embarquées dans les .tsi réels (payload base64) — DCBM = trame des définitions de commandes (5 626 entrées DJTT) |
| Pseudo-TSI CSV | Tableau maître des assignations (séparateur `;`) antérieur à l'implémentation — cahier des charges du mapping |
| Multi_SHIFT / Méga Couche | Système de couches d'activation par modifiers M1-M4 (binaire natif, limite 4) — couches Normal/Hyper/Méga |
| Karnaugh | Méthode de vérification des états de modifiers (tableaux) anti-conflits |
| Preset | Configuration JSON réutilisable (bloc/deck/paramètre) servant d'entrée au générateur |
| DSL | Langage minimal `contrôle -> fonction [couche]` du module studio |
| $facon | Alias propriétaire : « de façon cohérente, optimisée et fonctionnelle » |
| KO-L009 | Règle écosystème : jamais d'exposition de secret ; push = propriétaire |

## 12. Annexes et sources

- **[S1]** Directive propriétaire verbatim — mission Task 39 (2026-11-02) : « génère-moi $facon un cahier des charges… dans l'objectif de générer $facon tous les éléments… (si certains font déjà partis de mon écosystème, vérifie qu'ils sont optimisés)… recherches web ciblées… GOOGLE DRIVE… base de connaissance ».
- **[S2]** Rapport G1 `download/rapport-dedoublonnage-qwen.md` — 10 lignées, inventaire E1-E9, références croisées, journal discussion b6170b8b [BLOQUÉ].
- **[S3]** `download/analyse-djtt-s4mk2-v2.1.0-approfondie.md` (référence mécanique DJTT) ; skills famille TSI v2.x (batterie 16/16) ; `skills/@mon-ecosysteme/` (SHARED v1.7.18, gen-plan v3.32.0, correct-work v2.8.0) ; Google Drive « mapping TSI » : TRAKTOR_PRO_3.9_Manual_English_Mapping (Total).pdf, TRAKTOR_PRO_3.9_Manual_francais_Mapping (Total) fr.pdf, traktor_kontrol_s4_mk2_manual_french.pdf, Controller Editor Manual French.pdf, TRAKTOR_PRO_3_Manual_English_2023_09.pdf ; dépôt externe cmdr-editor/cmdr (TsiLib/Enums — lecture de référence) ; manuels NI (S4 MK2 EN, setup FR, Controller Editor 2017).
- **[HYP-01]** Périmètre de la base de commandes (≥ 200) calibré sur le référentiel DCBM du mapping DJTT + manuels Drive — affiné en G3 après extraction réelle.
- **[HYP-02]** Les éléments des discussions non listés au §4 (présentation PDF, diagrammes ponctuels, packages ZIP historiques) sont couverts par les livrables L-3→L-6 qui les consolident — table de couverture complète au rapport final (L-9).

---

## Amendements (M4 — à ne remplir que sur évolution)

| Date | Version | Section | Motif | Source |
|------|---------|---------|-------|--------|
