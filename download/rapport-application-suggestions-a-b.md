# Rapport d'application des suggestions (a)/(b) — résorption des écarts F1/F2/F4

> **Session** : web-8a7e5653 · Task 16 · 2026-10-02
> **Méthode** : gen-plan v3.18.0 (pipeline E1-E15, profil NORMAL, exécution séquentielle) · Directive : « appliquer (a) puis (b) pour résorber les écarts F1/F2/F4 » (suggestions Task 15 / P2)
> **Périmètre** : suggestion (a) — inscription des 5 skills famille au registre KB ; suggestion (b) — matérialisation des PMs CORRECT-WORK v2.6.0/v2.7.0 au corpus. La suggestion (c) (baselines A2 disciplines n°54) demeure EN ATTENTE au prochain QUOTA_OK (gate KO-L001 — hors périmètre de la directive).

---

## 1. État initial et objectifs

La session Task 15 avait cartographié les interactions gen-plan ↔ correct-work (87 arêtes, 5 couches) et identifié 7 constats, dont trois actionnables : **F1** (skills famille installés hors registre KB — invisibles au Protocole de Découverte), **F2** (corpus CORRECT-WORK en retard : PM v2.5.1 < installé v2.7.0) et **F4** (détention des disciplines n°54 par gen-plan non matérialisée au registre). Les suggestions (a) et (b) de cette même session étaient conçues pour les résorber ; la présente Task 16 les exécute séquentiellement, avec recalibrage croisé KO-L004 des arbitres et rescellement de l'archive d'intégrité (unique voie de diffusion du corpus, décision v2.2).

## 2. Suggestion (a) — inscription des 5 skills famille (résorbe F1 + F4)

Le registre `skills/KNOWLEDGE.md` passe de **21 à 26 entrées versionnées**. Les cinq nouvelles entrées — `autonomous-agent` v1.0.0, `correct-py` v1.0.0, `fleet-engineering` v1.0.0, `memory-engineering` v1.0.0, `spec-driven-development` v1.0.0 — sont dérivées de leurs SKILL.md réels (descriptions, dépendances YAML, relations §3). Les relations non versionnées (consultation skills-inventory, convergence script-reviewer, fonctions héritées inter-disciplines) sont reléguées en champ Note afin de ne pas créer d'arêtes sans contrat (SHARED §3.2 règle 5).

Les réciproques « Utilisé par » sont complétées sur six entrées existantes : `gen-plan` (+ autonomous-agent), `correct-work` (+ autonomous-agent, + correct-py — escalade mode CIBLE), `clone-chat` (+ autonomous-agent), `skill-creator` (+ correct-py), `script-creator` (+ correct-py, post-traitement GF-6) et `knowledge-observer` (+ correct-py, leçons L003/L005). L'entrée `gen-plan` inscrit en outre les trois disciplines n°54 dans son « Dépend de » (détention §1.9, intégration v3.15.0, **sans plancher versionné** — le pattern assumé des 4 disciplines d'exécution), ce qui matérialise la détention fleet/spec/memory et clôt l'asymétrie F4. L'arbitre `check-ecosysteme-integrity.py` est recalibré (ECO_SKILLS 21 → 26, check 5 « 26 entrées ») et `test-coherence-interactions.py` étend son ensemble BY_DESIGN_AUTOTRIGGER aux 3 disciplines n°54 (déclenchement automatique SHARED §7 — même design documenté que context/loop/graph/harness).

**Résultat mesuré** : le constat F1 disparaît du rapport d'analyse mécanique (5/5 skills famille inscrits), F4 disparaît (discipline listée + entrée KB), la réciprocité passe de 66 OK à **78 OK / 0 ABSENTE**, et l'arbitre d'interactions reste à 0 FAIL avec un unique avertissement hérité (frontière fullstack-dev, D013). Le Protocole de Découverte (gen-plan E5, correct-work scan KB) voit désormais 100 % des skills écosystème installés.

## 3. Suggestion (b) — matérialisation des PMs CORRECT-WORK v2.6.0/v2.7.0 (résorbe F2)

Les deux PMs manquants sont reconstitués par la **méthode B1** (diffs chirurgicaux depuis v2.5.1), matérialisée dans le script persistant `scripts/materialise-pm-correct-work.py` : base byte-lue de PM v2.5.1 (643 lignes), chaîne de 24 remplacements exacts pour v2.6.0 puis 22 pour v2.7.0, chaque motif devant apparaître exactement une fois (garde bruyante sinon). Le contenu des changements est tracé par des sources vérifiables : le SKILL.md v2.7.0 installé certifié (marqueurs « v2.6.0, phase N20 », §1.5 « changement de contrat v2.7.0, directive propriétaire 2026-10-02 : fin du mode autonome »), la décision KB N20 et `references/verification-protocol.md` (v2.6.0 : 4e mode AVEUGLE + hook 2nd opinion agent-driven + protocole embarqué au §5.6 ; v2.7.0 : couplage gen-plan obligatoire, résolution dynamique frontmatter → KB, ARRÊT EXPLICITE).

L'honnêteté de la reconstitution est garantie par une **provenance explicite** dans l'en-tête et le §7 de chaque PM (aucun faux lignage — même pattern que `verification-protocol.md` reconstitué B13-r5) : les détails de forme non traçables post-wipe sont assumés et listés (estimations de taille, plage du check 2, §5.4 de v2.6.0 conservé à 8 cas trigger_evals, §5.4 de v2.7.0 aligné sur les 7 cas de la forme installée certifiée dépôt 42c2a41). Le §4 YAML du PM v2.7.0 est byte-aligné sur le frontmatter installé (contrat d'assemblage PM → skill), et les diffs totaux sont bornés aux changements documentés (116 lignes v2.5.1→v2.6.0, 60 lignes v2.6.0→v2.7.0, vérifiés ligne à ligne).

Le recalibrage croisé KO-L004 accompagne la matérialisation : **CORPUS_ATTENDU 24 → 26** (check-ecosysteme-integrity), **SHARED v1.6.4** (§6.1 : PM CORRECT-WORK porté à v2.7.0, référence PM-INSTALL à v1.3.1), **PM-INSTALL v1.3.1** (§3.2 : le cas d'espèce R2 correct-work — corpus v2.5.1 < installé v2.7.0 — est RÉSORBÉ, la garde R2 demeurant pour tout état futur), **SYNC-CONTEXT v1.4.1** (état du corpus porté à 26 fichiers, statut des blocs CONTEXTE SYSTÈME hérités documenté), **orchestrateur ULTRA régénéré** (CORRECT-WORK v2.7.0 « la plus récente », historiques 2.4.0 → 2.6.0, 26 skills, 26 entrées KB), **archive d'intégrité rescellée** (`scripts/task16-resceller-archive.py`, round-trip **26/26 byte-identiques**) et **manifeste SHA-256 rescellé**.

## 4. Certification (gen-plan:correct-work(projet))

| Arbitre | Résultat | Verdict |
|---|---|---|
| verify-cross.py (axes 1-6) | 78/78 (26 skills × 3 checks) | ALL PASS |
| verify-cross.py --mode correct-work | 78/78 | ALL PASS |
| verify-correct-work.py | 16/16 | ALL PASS |
| check-ecosysteme-integrity.py | 56/56 (corpus 26, round-trip 26/26, KB 26) | ALL PASS |
| test-coherence-interactions.py | 51/52 (1 avertissement hérité D013) | PASS AVEC RÉSERVES |

**VERDICT CONSOLIDÉ : CERTIFICATION COMPLÈTE — PASS AVEC RÉSERVES (5/5 arbitres verts, 0 échec)**, strictement comparable à la baseline Task 15 (la seule réserve est l'avertissement structurel fullstack-dev documenté D013, hérité). Vérifications complémentaires : re-analyse d'interactions (`analyse-interactions-gc.py`) — **F1, F2 et F4 totalement résorbés**, ne subsistent que F3/F5 (S4, documentés, aucune action requise) ; test d'installation (`test-installation-ecosysteme.py`) — **40/40 PASS STRICT**, garde R2 correct-work désormais à l'équilibre (installé v2.7.0 = PM corpus v2.7.0) ; idempotence prouvée sur trois plans (rapport d'installation SHA identique ×2, générateur ULTRA no-op au re-jeu, matérialisation des PMs byte-identique au re-jeu) ; garde anti-doublons à 0.

## 5. Bilan

Les trois écarts ciblés par la directive sont résorbés : le registre KB redevient vrai pour 100 % des skills écosystème installés (Règle Zéro), le graphe de relations reste intégralement bidirectionnel (78 OK / 0 ABSENTE), et l'unique voie de diffusion du corpus porte désormais la forme documentaire certifiée correct-work v2.7.0 avec une lignée complète depuis v2.4.0. Les formes installées sont restées byte-inchangées (certifiées dépôt 42c2a41 — aucune réinstallation ni rétrogradation R2) ; toutes les modifications sont additives et documentées au worklog (Task 16), à la décision d'architecture KB et aux historiques des fichiers de gouvernance. La couche Task 16 n'est PAS publiée (push non demandé — protocole Task 7) ; la suggestion (c) reste armée pour le prochain QUOTA_OK.
