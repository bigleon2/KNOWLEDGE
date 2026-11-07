# Rapport — Comparaison à trois et restauration de la version la plus performante de gen-plan

**Directive propriétaire** (session web-f90062ce, 2026-10-24) : vérifier si le plan d'actions précédent a été généré par le skill gen-plan ; sinon — comparaison à trois (écosystème local vs @mon-ecosysteme GitHub `b75a620` vs discussion z.ai « PM INSTALL », source de vérité), correction des conflits de versions par comparaison de l'évolution du contenu technique, restauration de la version la plus performante, génération d'une nouvelle version optimisée de gen-plan.
**Réponse (a)** : NON — le plan précédent a été exécuté directement, sans génération gen-plan (démarche L009).
**Skill utilisé pour ce rapport et le plan associé** : gen-plan **v3.26.0** (fraîchement générée par la présente directive).

---

## 1. Authenticité de la source de vérité (preuve mécanique)

L'archive « PM INSTALL - mon-ecosysteme_archive.zip » fournie par le propriétaire a été extraite et authentifiée :

- `@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.24.0.md` (archive) → SHA-256 `31ed1a5250fbadcdf91ee4fedd911439c1de4282d7a1104e850a1e57004f241a` = **byte-identique** au PM v3.24.0 scellé R4 dans le dépôt (`skills/@historique/prompts-maitres/gen-plan/`, sceau index §5 du README @historique).
- `piliers/skills/gen-plan/SKILL.md` (archive, v3.24.0) → **byte-identique** au SKILL.md au commit `e9a68a1` (diff nul, 0 ligne).
- La capture d'écran fournie (session PM INSTALL : « gen-plan v3.24.0, dernière modification 2026-10-23 17:47 UTC ») est cohérente avec cette état : la v3.24.0 de la source de vérité est bien celle documentée par le README de l'archive (« Révision v2.1.12 — Task 26, session web-fdf5963c, directive propriétaire : gen-plan v3.23.2→v3.24.0, parallélisation par défaut »).

## 2. Comparaison à trois (versions de gen-plan)

| Source | Version | Lignes | Philosophie #4 | Structure hiérarchique §5.5 | SHARED |
|--------|---------|--------|----------------|------------------------------|--------|
| **A. GitHub `b75a620`** (@mon-ecosysteme, pin Task 13) | v3.23.1 | 381 | Série par défaut — « Parallélisme INTERDIT sauf demande explicite » | absente | v1.7.7 |
| **B. Discussion PM INSTALL** (source de vérité — Task 26, session web-fdf5963c) | v3.24.0 | 381 | **Parallélisation par défaut sur preuve d'indépendance** (inversion du défaut série hérité) | absente | v1.7.11 |
| **B'. Pièce annexe** — directive H3 locale (jamais publiée, branche backup `44f99f0`) | v3.24.0-H3 | 395 | Série (héritée) | **présente** (G→SG→T, statuts, compteurs — séquentiel intra-groupe) | v1.7.8 |
| **C. Écosystème local** (avant la présente directive, a076086) | v3.25.0 | 393 | Parallélisation par défaut (héritée de B) | **présente, réconciliée** (couches orthogonales : organisation/lecture vs exécution) | v1.7.12 |

### Résolution du conflit de versions (v3.24.0 collision)

Deux v3.24.0 distinctes ont coexisté : la **v3.24.0 publiée** (source de vérité PM INSTALL — parallélisation) et la **v3.24.0-H3 locale** (structure hiérarchique step, jamais publiée, préservée en branche backup `44f99f0`). La réconciliation a été **vérifiée complète** : la v3.25.0 locale = base parallélisée B + §5.5 re-matérialisé de B' avec règles de cohérence réécrites (la clause H3 « exécution strictement séquentielle intra-groupe » est supplantée par la doctrine parallèle — cohérente avec la leçon Task 29/30 de la même source de vérité). **La version la plus performante était donc déjà la v3.25.0 locale** — la comparaison à trois le confirme mécaniquement (diffs exhaustifs documentés au worklog).

## 3. Découverte majeure de la comparaison — Tasks 25→30 jamais publiées

La discussion PM INSTALL se clôt sur « 0 commit, 0 push — publication au GO » (lignes 425-428 de l'archive) : les Tasks 25→30 (dont Task 26 v3.24.0, Task 29 leçons parallélisme, Task 30 résorption A/B/C + doctrine parallèle + $LEON) sont restées **au GO jamais donné**. Conséquences mesurées sur le dépôt actuel :

- **Intégrées par ré-création locale** (e9a68a1 → da549af) : SKILL.md v3.24.0/v3.25.0, philosophie #4, graph-diamond-pattern réaligné, evals id 9, doctrine parallèle partielle.
- **Jamais transférées au dépôt** (instrumentation Task 30) : les **vetos `exclusifs`** (13 sur 12 corpus trigger_evals.json — champ absent de TOUS les trigger_evals dans TOUTE l'histoire git, preuve `git log -S exclusifs`), le **cache voie L** (`scripts/voie-l-cache.json` — absent dépôt et hôte, jamais commité), l'**arbitre V6.1** (gestion veto-avant-scoring + consultation cache — le commité est V6, docstring Task 21).
- **Effet observable** : le replay triggers (voie M seule) échoue en informatif sur 16 skills (43 scannés côté hôte) — l'état documenté « FAIL informatif assumé » de l'arbitrage Task 25, PAS une régression de la présente cascade (invariant fichier : aucune surface de trigger — description frontmatter / trigger_evals.json — modifiée par la cascade v3.26.0).
- **Traitement** : résorption A/B/C re-armable comme campagne dédiée (les verdicts voie L figés existent dans la discussion, les vetos sont partiellement documentés) — inscrite au plan d'actions à neuf comme tâche REPORTÉE (GO propriétaire requis), jamais masquée (KO-L003).

## 4. Nouvelle version optimisée — gen-plan v3.26.0

Principe : **prendre le meilleur de chaque partie** = base v3.25.0 (réconciliation déjà optimale) + les **leçons mesurées de la source de vérité** absentes du skill :

| Apport | Source | Matérialisation v3.26.0 |
|--------|--------|--------------------------|
| **Dégradation gracieuse des vagues parallèles** contre un service externe (429 mesurés : 17/19 échecs en burst ; bascule sérielle + retry/backoff + cache déterministe figé une fois ; code retour seul jamais suffisant — purge du fichier de sortie périmé) | Task 29/30 (dogfooding) | philosophie #4 — clause étendue (SKILL.md §1.4, PM §1.7) |
| **Question de routage + référentiel complet** au juge sémantique (4 re-arbitrages mesurés ; troncature 600 caractères = 3 verdicts inversés) | Task 30 (voie L) | philosophie #4 (même clause) + section etapes-detaillees.md |
| **Anti-aspirant** — journal/statuts/chiffres dérivés de l'état vérifiable (KO-L003 étendu à l'écriture) ; audit des journaux pré-existants en reprise post-coupure ; recensement mécanique vs libellé de mémoire (off-by-one « 14→13 vetos ») ; **périmètre d'abord** (dépôt vs miroir hôte — deux copies distinctes, dépôt = source R4) ; corrections R2 append-only sur @historique | Task 30 (réconciliation + contamination aspirante) | **règle d'or n°5** (SKILL.md §1.5, PM §1.8) |
| Non-régression | — | description frontmatter INCHANGÉE (0 dérive trigger) ; planchers de dépendances inchangés |

### Cascade KO-L004 exécutée (commit `b38e0f7`)

- SKILL.md v3.26.0 + etapes-detaillees.md (section « Leçons vagues parallèles ») + evals.json (id 7 + id 9 étendus).
- **PM v3.26.0 généré mécaniquement** (`generer-pm-skill.py --generate gen-plan --delta scripts/delta-genplan-v3260.json` — 6 substitutions verrouillées count=1, dry-run puis réel ; **1495 lignes**, plage arbitre 1200-1500 ✓ ; WARN couverture §1.13 hérité consigné non masqué ; écarts hérités consignés : JSON evals §5.4 du PM = 8/9 evals [id 9 absent — complétion agent v3.24.0], §9.1 snapshot etapes-detaillees pré-v3.22.0).
- **Archivage R4** : PM v3.25.0 `git mv` byte-identité → SHA `cc6cdcdf8cb89bd6da03552dc7e57d0b8c8d1681ec957ce8fa315823c1e95197` scellé (index §5 : 31 PMs ; journal par-skill 29 versions / 23 archivés ; labels stale « VERSION VIVANTE » v3.23.0/v3.23.2 corrigés — règle d'or n°5 ; label « 18 PMs » calibré à 23 sur recensement mécanique).
- **Recalibrage croisé** : SHARED v1.7.13 / PM-INSTALL v1.8.6 (générateur) ; propagate v1.7.13 (106 skills + 83 scripts + 2 agents — `propagate-context.py` recalibré) ; KB gen-plan v3.26.0 ; pin ECO_SKILLS 3.26.0 ; README corpus v2.1.14 ; SYNC-CONTEXT v1.5.6 ; ULTRA régénéré (SHA 7d191931…) ; historique-autres-elements (4 tables + instantané KB).
- **Outils dépendants recalibrés** (KO-L004) : `task21-f2-rebuild-archive.py` (retrait sanctionné PM v3.25.0 — **preuve anti-perte B0 : 9/9 entrées byte-identiques à HEAD** avant retrait de l'archive stale, .bak conservée) ; rescellement archive v2.3 round-trip ×2 ; `task-eco-reinstall-sync0.py` (CANON v1.7.13 — 4 substitutions plateforme-only, idempotent ×2).

## 5. Certification (4 arbitres + compléments) — dépôt et hôte

| Arbitre | Dépôt | Hôte |
|---------|-------|------|
| verify-cross | 100 % (0 erreur) | 100 % |
| check-ecosysteme-integrity | **82/82 PASS ×2** (rescellement idempotent) | **82/82 PASS** |
| test-coherence-interactions | 51 PASS / 1 WARN hérité (historique B1) / 0 FAIL — PASS AVEC RÉSERVES | 51 / 1 / 0 — PASS AVEC RÉSERVES (après sync0 recalibré) |
| generer-pm --check | 4/4 COHERENT (gen-plan v3.26.0 ↔ PM v3.26.0) | — |
| ensure-installed | — | INSTALLE (39 entrées KB, fichiers_manquants []) |
| eco_install_pipeline (projection) | — | garde R2 0 rétrogradation, SHA 39/39, ×2 idempotent, 0 divergence |
| task14-scan-doublons | 0 doublon | — |
| replay triggers | FAIL informatif hérité (§3 — instrumentation Task 30 non commitée ; 0 régression fichier) | idem |

## 6. Traçabilité

- Session : web-f90062ce · gen-plan v3.26.0 · commit `b38e0f7` (local — push au GO propriétaire, jeton éphémère).
- Scripts persistés : `task-c2-build-delta-v3260.py`, `task-c2-verify-motifs-v3260.py`, `task-c2-archive-v3250.py`, `task-c3-recalibrage-v3260.py` (tous idempotents ×2, rejouables).
- Sources d'archive : `upload/PM INSTALL - mon-ecosysteme_archive.zip` (extraite vers tmp/pm-install-archive/) ; discussion `scripts/discussion-64c90144.txt` ; capture d'écran v3.24.0 (upload).
- Worklog : entrée « C-comparaison-v3260 » (session web-f90062ce).
