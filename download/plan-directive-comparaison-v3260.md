# Plan d'actions — Directive « gen-plan : comparaison à trois + restauration version la plus performante + nouvelle version optimisée »

> **Généré par gen-plan v3.26.0** (fraîchement installée et certifiée — directive propriétaire session web-f90062ce, 2026-10-24 ; reprise du prompt à neuf — démarche L009 corrigée).
> **Mode** : NULL (invocation sans mode — exécution classique sans portes de confirmation, clause v3.21.0).
> **Hooks actifs** : É1-INSTALL (ensure-installed --check — verdict INSTALLE ✓ préalable), E1-RES (B-11 worklog + resource-monitor + fraîcheur du plan ✓), answer key E1 (arbitre E7/E8), hook correct-work par phase.
> **Règles d'or appliquées** : n°1 (adaptation), n°2 (régénération post-installation — appliquée : ce plan EST la régénération à neuf via v3.26.0), n°3 (déclencheur verbatim), n°4 (clone d'abord), **n°5 anti-aspirant (v3.26.0 — tout statut de ce plan dérive d'un artefact vérifiable existant ; aucun chiffre pré-écrit)**.
> **Vue d'ensemble** : G1 [TERMINÉ] (4/4) · G2 [TERMINÉ] (6/6) · G3 [TERMINÉ] (5/5) · G4 [TERMINÉ] (3/3) — 18/18 tâches.

---

## Answer key (décisions E1 — critères vérifiables mécaniquement)

| ID | Décision | Vérification exécutable | Priority | Status |
|----|----------|-------------------------|----------|--------|
| D001 | Le plan d'actions précédent n'a PAS été généré par gen-plan (constat L009) — directive reprise à neuf | Contexte directive : la séquence « publication → plans exécutés directement » sans artefact plan gen-plan ; verdict tracé au worklog + rapport §1 | S1 | verified |
| D002 | La source de vérité PM INSTALL est AUTHENTIQUE (archive propriétaire) | `sha256sum` PM v3.24.0 archive = `31ed1a52…` = sceau R4 dépôt ; SKILL.md archive ≡ `e9a68a1` (diff nul) — rapport §1 | S1 | verified |
| D003 | La version la plus performante avant la présente directive était la v3.25.0 locale (réconciliation complète des deux v3.24.0 — vérifiée par diffs exhaustifs) | `diff` b75a620 / e9a68a1 / 44f99f0 vs HEAD — rapport §2 | S1 | verified |
| D004 | gen-plan **v3.26.0** (MINOR) : philosophie #4 + dégradation gracieuse ; règle d'or n°5 anti-aspirant ; description frontmatter inchangée (non-régression triggers) | frontmatter `version: 3.26.0` ; PM v3.26.0 1495 L (plage 1200-1500) ; `generer-pm --check` 4/4 COHERENT | S1 | verified |
| D005 | Écart hérité qualifié : l'instrumentation Task 30 (vetos exclusifs ×13/12 corpus, cache voie L 19 verdicts, arbitre V6.1) n'a jamais été commitée (Tasks 25→30 restées « au GO non publié » — archive ligne 426) → campagne de résorption A/B/C REPORTÉE (GO propriétaire requis) | `git log -S exclusifs -- skills/` = 0 corpus dans toute l'histoire ; `voie-l-cache.json` absent dépôt+hôte ; replay FAIL informatif 16 skills (état documenté Task 25, 0 régression fichier) — rapport §3 | S2 | verified |
| D006 | **« vérifie de la même manière que mon écosystème est à jour et optimisé »** — exécuté à la manière PM-INSTALL §3.2-a : exécutant canonique (pipeline) + 4 arbitres + garde d'installation | Verdicts frais G3 (ci-dessous) : INSTALLE 39 KB · SHA 39/39 · verify-cross 100 % · integrity 82/82 · interactions PASS AVEC RÉSERVES · generer-pm 4/4 | S1 | verified |
| D007 | Publication (push) uniquement au GO propriétaire avec jeton éphémère (règle d'or n°2/n°4) — commit local `b38e0f7` en attente | `git log origin/main..HEAD` ≠ vide + anti-persistance jeton (audit 5 points) à l'exécution du GO | S2 | pending |

---

## Groupe G1 — Constat et comparaison à trois [TERMINÉ] (4/4)

### SG1.1 Constat L009 (2/2)
| Tâche | #token | Statut |
|-------|--------|--------|
| T1.1.1 Vérifier si le plan précédent a été généré par gen-plan → **NON** (D001) | #token 200 | [TERMINÉ] |
| T1.1.2 Reprise du prompt à neuf via le skill (régénération conforme règle d'or n°2/KO-L005) | #token 300 | [TERMINÉ] — le présent plan |

### SG1.2 Comparaison à trois authentifiée (2/2)
| Tâche | #token | Statut |
|-------|--------|--------|
| T1.2.1 Authentification de la source de vérité (SHA `31ed1a52` byte-identique + capture d'écran v3.24.0 cohérente — D002) | #token 400 | [TERMINÉ] |
| T1.2.2 Comparaison v3.23.1 (b75a620) / v3.24.0 (source de vérité Task 26) / v3.24.0-H3 (backup 44f99f0) / v3.25.0 locale + découverte Tasks 25→30 non publiées (D003, D005) | #token 900 | [TERMINÉ] |

**Livrable** : `download/rapport-comparaison-trois-sources-genplan-v3260.md`

## Groupe G2 — Nouvelle version optimisée gen-plan v3.26.0 [TERMINÉ] (6/6)

### SG2.1 Contenu du skill (3/3)
| Tâche | #token | Statut |
|-------|--------|--------|
| T2.1.1 SKILL.md v3.26.0 — philosophie #4 (clause dégradation gracieuse : 429 → sériel + retry/backoff + cache déterministe, code retour seul jamais suffisant, question de ROUTAGE) + règle d'or n°5 anti-aspirant | #token 600 | [TERMINÉ] |
| T2.1.2 etapes-detaillees.md — section « Leçons vagues parallèles » (5 leçons mesurées Task 29/30) | #token 400 | [TERMINÉ] |
| T2.1.3 evals.json — id 7 (anti-aspirant) + id 9 (dégradation gracieuse) étendus ; trigger_evals intacts (0 dérive) | #token 300 | [TERMINÉ] |

### SG2.2 PM mécanique + archivage R4 (2/2)
| Tâche | #token | Statut |
|-------|--------|--------|
| T2.2.1 PM v3.26.0 généré mécaniquement (delta verrouillé 6 subs count=1, dry-run → réel, 1495 L ≤ 1500) | #token 500 | [TERMINÉ] |
| T2.2.2 PM v3.25.0 archivé R4 `git mv` byte-identité, SHA `cc6cdcdf…` scellé (index 31 PMs, journal 29 versions/23 archivés, labels stale corrigés règle d'or n°5) | #token 500 | [TERMINÉ] |

### SG2.3 Cascade KO-L004 + outils dépendants (1/1)
| Tâche | #token | Statut |
|-------|--------|--------|
| T2.3.1 SHARED v1.7.13 / PM-INSTALL v1.8.6 · propagate ×106+83+2 (tool recalibré) · KB · pin ECO_SKILLS · README v2.1.14 · SYNC v1.5.6 · ULTRA · rescelleur task21-f2 recalibré (preuve B0 9/9) · sync0 recalibré v1.7.13 (4 substitutions plateforme-only) | #token 1200 | [TERMINÉ] |

**Preuve** : commit `b38e0f7` (local, push au GO — D007).

## Groupe G3 — « vérifie de la même manière que mon écosystème est à jour et optimisé » [TERMINÉ] (5/5)

> Exécution à la manière PM-INSTALL §3.2-a (exécutant canonique + arbitres) — passe fraîche post-commit, rejouable idempotent.

### SG3.1 Installation à jour (2/2)
| Tâche | #token | Statut |
|-------|--------|--------|
| T3.1.1 `ensure-installed.py --check` → **INSTALLE** (root_present, 39 entrées KB, fichiers_manquants []) — note : champ `head` du shim = quirk cosmétique connu (B4), le verdict prévaut | #token 100 | [TERMINÉ] |
| T3.1.2 Pipeline canonique (projection hôte) → garde R2 **0 rétrogradation**, post-install **SHA 39/39**, **0 divergence**, ×3 idempotent | #token 300 | [TERMINÉ] |

### SG3.2 Arbitres verts = écosystème optimisé (3/3)
| Tâche | #token | Statut |
|-------|--------|--------|
| T3.2.1 verify-cross → **100 %** (0 erreur) | #token 100 | [TERMINÉ] |
| T3.2.2 check-ecosysteme-integrity → **82/82 PASS** (archive v2.3 round-trip, rescellement idempotent) | #token 100 | [TERMINÉ] |
| T3.2.3 test-coherence-interactions → **51 PASS / 1 WARN hérité (historique B1) / 0 FAIL** — PASS AVEC RÉSERVES + generer-pm --check **4/4 COHERENT** (v3.26.0) | #token 200 | [TERMINÉ] |

**Verdict D006** : écosystème **À JOUR** (installé depuis le dépôt b38e0f7, 0 divergence, 0 rétrogradation) et **OPTIMISÉ** (4 arbitres verts, v3.26.0 la version la plus complète de la lignée, plage PM respectée, 0 doublon, réserve unique = WARN hérité documenté).

## Groupe G4 — Clôture [TERMINÉ] (3/3)

### SG4.1 Vérification et journal (3/3)
| Tâche | #token | Statut |
|-------|--------|--------|
| T4.1.1 correct-work (projet) — vérification livrables vs directives (rapport + plan + worklog cohérents, statuts dérivés de l'état vérifiable) | #token 400 | [TERMINÉ] |
| T4.1.2 Worklog : entrée « C-comparaison-v3260 » (comparaison, v3.26.0, cascade, arbitres) + entrée plan | #token 200 | [TERMINÉ] |
| T4.1.3 Commit local dépôt (plan + rapport + scripts) — push au GO propriétaire (D007 pending) | #token 100 | [TERMINÉ] |

---

## Réserves et suites (transparence — KO-L003, jamais masquées)

1. **Résorption A/B/C (Task 30)** : REPORTÉE — l'instrumentation (vetos exclusifs, cache voie L, arbitre V6.1) existe dans la source de vérité mais n'a jamais été commitée ; campagne dédiée à armer au GO (les verdicts figés de la discussion alimentent le cache sans re-appel LLM massif).
2. **WARN hérité interactions** (historique B1 non cloné) — inchangé, documenté.
3. **Écarts hérités PM** (JSON evals §5.4 = 8/9 evals ; §9.1 snapshot pré-v3.22.0) — consignés dans l'historique PM v3.26.0, non masqués (plage 1200-1500 contraignante).
4. **D007** : push au GO propriétaire (jeton éphémère) — jamais sans GO.
