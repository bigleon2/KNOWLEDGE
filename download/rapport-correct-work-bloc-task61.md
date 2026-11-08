# Rapport correct-work — Task 61 · Vérification bloc par bloc du périmètre créé/modifié hier et aujourd'hui (2026-11-06 → 2026-11-07)

## Métadonnées
- **Date** : 2026-11-07
- **Mode** : PROJET (option « bloc par bloc » `--bloc`, §1.7 — déclencheur directive propriétaire 11ᵉ, item 2)
- **Version correct-work** : 2.11.0
- **Cible** : périmètre P1-P7 (multi-cibles — éléments de l'écosystème créés ou modifiés dans cette discussion hier et aujourd'hui, dérivés du disque, règle d'or n°5)
- **Plan de vérification** : `download/plan-task61-correct-work-bloc-tests-facon2-optimisations.md` (gen-plan v3.35.2 — dernière version installée, couplage obligatoire §1.5, G2)

## Étape 1 — Plan d'actions
Plan de vérification = le plan Task 61 (groupe G2), généré via gen-plan v3.35.2 réinstallé ce jour (règle d'or n°2). Ordre de vérification : B1→B7 (P1-P7 du plan). Estimation #token G2 : ~18 k. Couplage §1.5bis : tout lot de correctifs issu du présent rapport sera planifié mode STEP (intégré au G4 du plan Task 61).

## Blocs vérifiés (Étapes 2-5 appliquées à chaque bloc)

### B1 — pm-skill v1.0.0 (P1, créé Task 60 G3-SG2)

**É2 — Erreurs et omissions** : version 1.0.0 (frontmatter) ✅ ; fichiers présents : SKILL.md + evals/evals.json + evals/trigger_evals.json (JSON valides) ✅ ; `scripts/generer-pm-ephemere.py` présent ✅ ; PM éphémères témoins générés (`download/PM-ephemere-correct-work-v2.11.0.md` 513 L, `download/PM-ephemere-pm-skill-v1.0.0.md` 120 L — commit 768bb3a) ✅ ; entrée KB `## pm-skill v1.0.0` présente ✅. Exigences Task 60 D604 (extraction SKILL.md → PM éphémère auto-portant, sans SKILL.md, usage IA externe) : satisfaites (auto-portance contrôlée en G3-T3.1.2).
**É3 — Structure** : kebab-case ✅ ; frontmatter complet ✅ ; pas de doublon détecté ✅.
**É4 — Interactions** : 2 asymétries KB détectées par l'arbitre coherence — (a) pm-skill → gen-plan : gen-plan ne liste pas pm-skill dans « Utilisé par » ; (b) correct-work ← pm-skill : pm-skill ne déclare pas correct-work en « Dépend de ». Qualification **S4** (suggestion de bidirectionnalité — aucune altération de comportement ; verify-cross 159/159 PASS, les 8 checks KB correct-work PASS) → correction planifiée G4 (D006 — candidat n° 1).
**É5 — Cohérence** : v1.0.0 = KB = PM éphémère témoin ✅ ; lignage Task 60 documenté (bbff275) ✅.
**Findings** : 2 × S4 → **Verdict B1 : PASS**

### B2 — correct-work v2.9.0→v2.11.0 (P2, optimisé Task 60 G4)

**É2** : version 2.11.0 (frontmatter) ✅ ; §1.5bis correctifs mode STEP ré-intégré (contrat D591 reconstitué, lignage honnête de la perte v2.10.0 documenté) ✅ ; matrice best-of §12 présente (v1.0.0→v2.11.0, 11 lignes, chaque avantage durable présent ou supplanté documenté) ✅ ; plancher gen-plan >= v3.22.0 respecté (v3.35.2 installée) ✅.
**É3** : structure §1-§12 conforme ; 499 L (plage 200-400 L du PM-INSTALL historique dépassée mais héritée des montées successives — non-régression R2, S4 cosmétique non compté) ; pas de doublon.
**É4** : arbitre `verify-correct-work.py` **16/16 PASS** ✅ ; PM corpus `PROMPT-MAITRE-CORRECT-WORK-v2.11.0.md` présent ✅ ; `scripts/delta-correctwork-v2110.json` valide ✅ ; @historique correct-work.md présent ✅ ; entrée KB v2.11.0 ✅ ; dépendances (gen-plan >= 3.22.0, clone-chat >= 2.0.0, alias-eco >= 1.0.0) toutes satisfaites ✅.
**É5** : v2.11.0 = KB = PM = delta (chaîne KO-L004 conforme, integrity 110/110) ✅ ; chronologie Task 60 G4 (5544734) cohérente ✅.
**Findings** : 0 → **Verdict B2 : PASS**

### B3 — dessin-technique v1.3.0 + nœud C++ trigo-euler (P3, Task 58 G2)

**É2** : version 1.3.0 (frontmatter) ✅ ; scripts présents : capture_forme.py, generer_dessin.py, mesurer_filet.py, mesurer_profondeur.py, mise_a_echelle.py, **trigo-euler.cpp** + binaire compilé `trigo-euler` ✅ ; evals 8 tests (T1-capture-forme → T8-trigo-euler-daemon, JSON valide) ✅ ; preuves mécaniques `tmp/mission-task58/trigo-node/` (journaux run1/run2, profils joint 5c, mini-plan) ✅ ; entrée KB v1.3.0 ✅.
**É3** : structure §1.1-§1.8 conforme (§1.8 F6 nœud C++ ajouté v1.3.0) ; T7/T8 présents dans evals ✅ ; ligne historique v1.3.0 (3 occurrences dans @historique/historiques-par-skill/dessin-technique.md) ✅.
**É4** : relation dessin-technique → inter-scripts déclarée (le nœud C++ est inscrit au registre inter-scripts) — asymétrie héritée S4 (inter-scripts ne liste pas dessin-technique dans « Utilisé par » — HORS périmètre du jour pour la partie réciproque, consigné G4 opportunité) ; registre `skills/inter-scripts/scripts/registre.json` référence le contrat 15 capacités + echo + daemon.stop (vérifié Task 58, re-testé en G3-T3.3.2).
**É5** : v1.3.0 = KB = historique ✅ ; cotes F1 officielles 44,9 × 35,2 mm tracées (profil joint 5c) ✅ ; chronologie Task 58 (00f9ca6) cohérente ✅.
**Findings** : 0 S1-S4 propre au bloc (1 asymétrie héritée réciproque classée B7) → **Verdict B3 : PASS**

### B4 — Corpus socle (P4 : SHARED v1.7.26→v1.7.28, PM-INSTALL v1.9.4, ULTRA, propagation §0, archive v2.3)

**É2** : SHARED v1.7.28 ✅ ; PM-INSTALL **v1.9.4** ✅ ; ULTRA présent (dé-figé Task 60 G4) ✅ ; propagation §0 du commit 768bb3a : **70 fichiers `skills/*/SKILL.md` modifiés (comptage exact `--name-only`)** ✅ — vérification croisée : 118 SKILL.md étiquetés « Contexte Système (SHARED » au dépôt, 53 à l'hôte (déploiement partiel conforme : l'hôte porte les 53 entrées KB + skills plateforme pré-installés, ensure-installed 0 défaut) ; archive v2.3 : **round-trip corpus 9/9 byte-identiques** (préfixe `@mon-ecosysteme/`) ✅ ; manifeste `scripts/ecosysteme-integrity.json` présent (9 536 octets) ✅.
**É3** : 9 fichiers corpus conformes (4 PMs familles + SHARED + INSTALL + ULTRA + README + SYNC-CONTEXT) ✅ ; conventions @préfixe ✅.
**É4** : SHARED §6.1 référence les 4 PMs familles aux versions vivantes (GEN-PLAN v3.35.2, CORRECT-WORK v2.11.0, CLONE-CHAT v2.0.2, REFACTOR-GUARD v1.8.1 — KO-L004 conforme, integrity 110/110) ✅.
**É5** : chronologie v1.7.26→v1.7.28 (Task 60 G4 → Task 58 G2 suite) tracée dans l'en-tête SHARED ✅. Note de méthode (enseignement, pas un finding) : 3 alertes de collecte initiales (round-trip « 0/9 », evals « 3 », propagation « 69 ») étaient des artifacts de test agent (préfixe d'archive omis, mauvaise clé JSON, chemins tronqués par `--stat`) — résolues par re-test avec le bon outil ; aucune faille du livrable.
**Findings** : 0 → **Verdict B4 : PASS**

### B5 — Système d'installation (P5 : auto-install-ecosysteme.py, eco_install_pipeline.py, ensure-installed.py, install-ecosysteme-local.sh)

**É2** : les 4 exécutants présents aux chemins canoniques ✅ ; PIN `b75a62066791a8cce8c1ec5d1dbe7d976bae4244` conforme (descendant-tolérant : clone a5ae36f accepté — merge-base vérifié) ✅ ; shim racine `scripts/ensure-installed.py` délègue au maître intégré `skills/gen-plan/scripts/ensure-installed.py` ✅.
**É3** : garde anti-persistance jeton (règle d'or n°4) : aucun jeton dans `.git/config` (remote en URL publique) ✅.
**É4** : garde étendue Task 56 (auto-réparation INSTALLE-REPARÉ — 2 occurrences du verdict dans ensure-installed.py) ✅ ; chaîne auto-install → ensure-installed --check + eco_install_pipeline (PIPELINE pointeur) ✅.
**É5** : preuve vivante du jour : réinstallation REINSTALLE (59 défauts → 0, rc=0) puis **no-op ×3** (INSTALLE, actions [], 0,08 s — G1-T1.2.1/T1.2.2) ; F3 post-install du pipeline : 0 divergence SHA (prouvé par contrôle final INSTALLE) ✅.
**Findings** : 0 → **Verdict B5 : PASS**

### B6 — version-management v1.2.0 (P6, garde Task 56)

**É2** : version 1.2.0 (frontmatter) ✅ ; entrée KB `## version-management v1.2.0` présente ✅ ; restauré ce jour par la réinstallation (19ᵉ disparition absorbée par la garde — cause racine volatilité snapshots documentée Task 56) ✅.
**É4** : couvert par la garde étendue ensure-installed (SKILL.md de TOUTES les entrées KB — dérivation dynamique) ✅ ; test complet disparition-simulée → G3-T3.4.1.
**É5** : 1.2.0 = KB ✅.
**Findings** : 0 → **Verdict B6 : PASS**

### B7 — Écosystème global (P7 : registre KB, @historique, arbitres)

**É2** : 53 entrées KB versionnées (54 en-têtes `##` — 53 entrées + 1 section) ✅ ; @historique complet (historiques-par-skill, @Alias/aliases.json valide, sceaux, orphelins, photos) ✅ ; manifeste integrity ✅.
**É4** : arbitres du jour — verify-cross **159/159 PASS (100 %)** · check-ecosysteme-integrity **110/110 PASS, 0 FAIL** · coherence **54 PASS / 27 WARN / 0 FAIL** · answer-key-checker **16 PASS** ✅.
**É5** : cohérence des raisonnements — la dette d'asymétries KB (WARN coherence) est **en diminution** (29 → 27 entre Task 58 CLOSE et ce jour, PASS 53 → 54) ; les 27 WARN sont des asymétries héritées de bidirectionnalité KB (S3/S4 — aucune introduite par le périmètre du jour, 2 seulement le touchent via pm-skill, classées B1) ; verdict de l'arbitre : PASS AVEC RÉSERVES (0 FAIL).
**Findings** : 25 asymétries héritées S3/S4 (dette documentée, hors périmètre direct de la directive — opportunité G4) → **Verdict B7 : PASS AVEC RÉSERVES** (aligné sur le verdict de l'arbitre coherence)

## Étape 2 — Erreurs et omissions (synthèse transversale)

| # | Sévérité | Description | Emplacement | Correction proposée |
|---|----------|-------------|-------------|---------------------|
| F1 | S4 | Asymétrie KB : gen-plan ne liste pas pm-skill dans « Utilisé par » | skills/KNOWLEDGE.md (entrée gen-plan) | G4-D006 : ajouter la réciproque (bidirectionnalité SHARED §3.2) |
| F2 | S4 | Asymétrie KB : pm-skill ne déclare pas correct-work en « Dépend de » | skills/pm-skill/SKILL.md + KB | G4-D006 : déclarer la dépendance (si usage réel confirmé) |
| F3 | S4 | Asymétries KB héritées ×25 (dette préexistante, en diminution) | skills/KNOWLEDGE.md (entrées diverses) | Opportunité G4 (hors périmètre directive — consignation) |

Aucune erreur factuelle, omission d'exigence, ou incohérence linguistique détectée sur le périmètre P1-P7 (données factuelles vérifiées bloc par bloc contre le disque).

## Étape 3 — Structure et conflits

| # | Type | Description | Fichiers concernés | Résolution |
|---|------|-------------|-------------------|------------|
| — | — | Aucun conflit structurel détecté : frontmatters valides, conventions kebab-case/semver respectées, archive byte-identique 9/9, aucun doublon corpus (garde D010) | — | — |

## Étape 4 — Interactions

| # | Skill A | Skill B | Type d'interaction | Statut |
|---|--------|--------|-------------------|--------|
| 1 | correct-work | gen-plan | Invocation E1 obligatoire (plancher >= 3.22.0) | OK (v3.35.2) |
| 2 | pm-skill | gen-plan / correct-work | Références nouvelles (Task 60) | ASYMÉTRIE S4 ×2 (F1/F2 — G4) |
| 3 | dessin-technique | inter-scripts | Nœud C++ au registre | OK (contrat 15+2 ops) |
| 4 | Système installation | gen-plan (ensure-installed) | Garde E1-INSTALL | OK (no-op ×3 prouvé) |
| 5 | Tous (KB) | Registre | Bidirectionnalité | 159/159 verify-cross PASS ; 25 asymétries héritées WARN |

## Étape 5 — Cohérence des raisonnements

| # | Point vérifié | Résultat | Détail |
|---|---------------|----------|--------|
| 1 | Chaîne des versions SKILL.md = KB = PM (4 familles + périmètre) | OK | integrity 110/110 (contrôle mécanique croisé) |
| 2 | Chronologie des commits (bbff275 → a5ae36f) vs livrables | OK | chaque livrable cité existe au chemin annoncé |
| 3 | Chiffres des messages de commit vs disque | OK | 70 SKILL.md (comptage exact), 16/16, 110/110, 159/159, 9/9 round-trip |
| 4 | Répartition hôte/dépôt (53 vs 118 étiquettes §0) | OK | déploiement partiel conforme (53 entrées KB = fermeture du profil, ensure-installed 0 défaut) |
| 5 | Dette coherence | EN DIMINUTION | 29→27 WARN, 53→54 PASS, 0 FAIL stable |

## Table « Blocs vérifiés » (agrégation --bloc, §10.1bis)

| Bloc | Périmètre | Étapes couvertes | Findings | Verdict |
|------|-----------|------------------|----------|---------|
| B1 | pm-skill v1.0.0 | É2-É5 | 2 × S4 (asymétries — G4) | **PASS** |
| B2 | correct-work v2.11.0 | É2-É5 | 0 | **PASS** |
| B3 | dessin-technique v1.3.0 + trigo-euler | É2-É5 | 0 | **PASS** |
| B4 | Corpus socle (SHARED v1.7.28, PM-INSTALL v1.9.4, ULTRA, archive) | É2-É5 | 0 | **PASS** |
| B5 | Système d'installation (4 exécutants, PIN b75a620) | É2-É5 | 0 | **PASS** |
| B6 | version-management v1.2.0 (garde) | É2-É5 | 0 | **PASS** |
| B7 | Écosystème global (KB, @historique, arbitres) | É2-É5 | 25 × S3/S4 héritées (dette ↓) | **PASS AVEC RÉSERVES** |

## Résumé
- **Problèmes trouvés** : 27 (2 S4 périmètre du jour + 25 S3/S4 hérités, dette en diminution)
- **Corrections appliquées** : 0 immédiate (S4 — non bloquants ; lot planifié G4 mode STEP, §1.5bis)
- **Corrections planifiées (G4-D006)** : F1 + F2 (bidirectionnalité pm-skill) + opportunité F3
- **Problèmes restants** : 25 hérités (hors périmètre directive, tracés)
- **Verdict global = pire des verdicts de blocs (§1.4) : PASS AVEC RÉSERVES** — 0 S1, 0 S2, réserves = 25 asymétries KB héritées S3/S4 (arbitre coherence 54/27/0, dette en diminution, aucune introduite par le périmètre du jour)

**Suite** : G3 (tests $FACON2 fonctionnels ×2 + performances) puis G4 (corrections F1/F2 + optimisations, lot planifié mode STEP via le plan Task 61).
