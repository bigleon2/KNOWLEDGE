# Rapport correct-work (projet) — Task 107

**Mode** : PROJET (§10.1 correct-work v2.11.0 — couplage gen-plan v3.43.0 installé, Étape 1 = plan `download/plan-task107-go1-entree-canonical-go2-correctif-f1-cw-clone.md`)
**Directive vérifiée** : trace `1a1efebf27dcbafd` « PUSH [clé du tour] · GO-1 · GO-2 · correct-work · clone-chat · continue. »
**Horodatage** : 2026-11-19

## Pré-vérification

- Prompt maître / directive : disponible et lisible (message propriétaire du tour, chaîne d'items ordonnée) ✓
- Versions mobilisées : gen-plan v3.43.0 (installé, KB) · correct-work v2.11.0 · clone-chat v2.0.2 · PM-INSTALL v1.10.0 (édité ce tour, GO-1) · SHARED v1.7.40 ✓
- Livrables attendus (liste) : (1) pendance PUSH éteinte ; (2) `scripts/bootstrap-ecosysteme.py` + PM-INSTALL §3.2-c v1.10.0 + SHARED §6.1 v1.7.40 + ULTRA régénéré (GO-1) ; (3) campagne de non-régression re-jouée ; (4) correctif F1 + test dédié V2 INSTALLE (GO-2) ; (5) présent rapport CW ; (6) clone-chat 20ᵉ ; (7) worklog suite 153 + commit + PUSH final.

## Phase 1 — Plan (via gen-plan, OBLIGATOIRE)

Plan créé AVANT exécution (`download/plan-task107-go1-entree-canonical-go2-correctif-f1-cw-clone.md`, answer key D001-D009 schéma criterion/verification/source/priority/status, 9 décisions) ✓ · plan des correctifs Étapes 2-5 mode STEP : le plan intègre la séquence de vérification par décision ✓ · sections à vérifier identifiées (G0-G5) ✓ · estimation #token : profil NORMAL (G-RES 7,6 Go, aucune pression) ✓.

## Phase 2 — Erreurs et omissions (délégation alias-eco v2.8.0)

Registre `@historique/@Alias/aliases.json` consulté : 4 entrées, `$FACON`/`$FACON2` déjà inscrits (occurrences historiques Task 105/106) — la directive du tour ne contient AUCUNE nouvelle phrase récurrente (chaque item apparaît une fois) → registre inchangé, no-op honnête ✓.
Comparaison directive ↔ livrables, item par item :

| Item directive | Livrable | Statut |
|---|---|---|
| PUSH (clé du tour) | `aa855a2f..0473e8f4` rc=0, ls-remote anonyme : origin/main = HEAD, 0 unpushed | ✓ rendu |
| GO-1 | bootstrap-ecosysteme.py (selftest 5/5, N1) + PM-INSTALL v1.10.0 (§3.2-c/§2ter/§A.3/§7/en-tête) + SHARED v1.7.40 (§6.1/Révision) + ULTRA régénéré + propagation §0 (120 skills + 213 scripts + 4 agents) + campagne non-régression (bootstrap INSTALLE-REPARÉ→INSTALLE rc=0 · idempotence ×2 byte-identique · garanties 4/4 · certification 6/6) | ✓ rendu |
| GO-2 | correctif F1 11+/3− lignes (garde existence miroir, head = ROOT si dépôt) + test dédié V2 `INSTALLE` rc=0 (contrôle initial ET final) + harnais flux V2 fonctionnel=true | ✓ rendu |
| correct-work | le présent rapport | ✓ rendu |
| clone-chat | livrable G4 (voir §Clone) | ✓ rendu |
| continue | point d'état final (cron, PAT, PMs §0 L2, G-RES) au worklog 153 et au récapitulatif | ✓ rendu |

Omissions : AUCUNE — les 6 items de la directive sont couverts. Erreurs factuelles : AUCUNE détectée dans les livrables (versions, chemins, numéros de commits vérifiés à la relecture).

## Phase 3 — Structure et conflits

Conventions : kebab-case (`bootstrap-ecosysteme.py`, `rapport-nonregression-task107-*.json`) ✓ · semver (PM-INSTALL v1.10.0 mineur — nouvelle clause mécanique, précédent v1.8.0 mécanisme dual ; SHARED v1.7.40 patch — recalibrage référence, précédent v1.7.39) ✓ · docstring d'abord (S3/F4, N1 < 600 octets — tool-routing PASS 7/7, le nouveau script est le 7ᵉ scanné) ✓ · aucune modification du pipeline/arbitres/harnais (R2/zéro-régression — `git diff` borné : nouveau fichier + corpus + 11 lignes ensure-installed) ✓.
Cross-references : PM-INSTALL §3.2-c ↔ §2ter ↔ §7 cohérents ; SHARED §6.1 ligne PM-INSTALL = v1.10.0 = version réelle (fichier) ✓ ; ULTRA install_v dérivée dynamiquement (v1.10.0 constaté) ✓ ; aucun doublon download↔skills (task14-scan-doublons 0 — vérifié en G5) ✓. Conflits entre sections : AUCUN.

## Phase 4 — Interactions

Dépendances inter-skills : gen-plan v3.43.0 ≥ plancher correct-work v3.22.0 ✓ · clone-chat v2.0.2 ≥ v2.0.0 ✓ · versions minimales respectées partout (verify-cross 165/165 ×2) ✓. Interfaces : bootstrap-ecosysteme.py consomme les exécutants canoniques PAR SOUS-PROCESSUS (pipeline, certification-complete, ensure-installed — chemins absolus dérivés de BASE, précédent auto-install-ecosysteme.py) — aucune interface modifiée ✓. Interactions certifiées : test-coherence-interactions PASS STRICT (55/55) ✓ · check-tool-routing PASS (7/7) ✓ · certification ALL PASS (6/6) ×3 runs ce tour (bootstrap 3, 6 + final) ✓.

## Phase 5 — Cohérence des raisonnements

- Ordre d'exécution = ordre de la directive (PUSH → GO-1 → GO-2 → CW → clone → continue) ✓ — GO-2 après la campagne GO-1 conformément à la feuille de route Task 105 §8.
- Décision D-version (PM-INSTALL v1.10.0 mineur vs v1.9.17 patch) : cohérente avec le précédent v1.8.0 (nouveau mécanisme d'entrée = changement de contrat de la §3.2, pas un simple recalibrage) ✓.
- Décision pas-de-bump gen-plan (correctif F1 = restauration du comportement documenté §1.16, pas de changement de spécification) : cohérente avec l'absence de modification de SKILL.md et la certification verify-cross/integrity vertes ✓.
- Décision propagation §0 v1.7.40 (120+213+4) : précédent Task 95 (120+211+4) — mécanisme canonique propagate-context v2.1.1, dérivation dynamique ✓.
- Décision revert des 5 scripts injectés (vs retenir l'injection) : les 5 états d'origine sont certifiés (Tasks 98/101/102/104/106) ; l'injection portait un gabarit périmé v1.7.39 ET cassait 2 compilations (`from __future__`) — le revert est le seul choix conforme R2 ; le défaut injecteur est consigné (F3) pour correctif futur sous GO ✓.
- Décision voie opérationnelle rescellement (mise à l'écart explicite de l'archive entrante vs modification du scelleur) : le GO-1 interdit de modifier les exécutants (R2) ; la mise à l'écart préserve la sémantique anti-perte (aucune perte silencieuse : action explicite de l'opérateur, restauration .bak native en cas d'échec d'auto-vérification, contenu corpus historisé git) ✓.
- Alignement décisions/actions : chaque décision de l'answer key correspond à une action exécutée et réciproquement ✓.

## Findings

| # | Sévérité | Constat | Traitement |
|---|---|---|---|
| F1 | S4 (récurrente, escalade maintenue) | 5ᵉ récidive de recyclage sandbox : version-management hôte absent au dry-run run-1 + micro-dérive 2 fichiers entre commit GO-2 et bootstrap run-6 | réparé automatiquement par l'entrée canonique (installation sync / préflight reset --hard LOCAL) — le comportement est EXACTEMENT le cas d'usage mesuré Task 105 |
| F2 | S3 | Garde anti-perte du scelleur v2.3 bloque la 1ʳᵉ évolution de corpus légitime depuis Task 100 (aucune distinction dérive/légitime) | voie opérationnelle appliquée et documentée (mise à l'écart explicite) ; correctif structurel (drapeau d'évolution contrôlé ou comparaison git) proposé sous GO futur |
| F3 | S3 | Branche « injection fraîche » de propagate-context.py porte un gabarit littéral périmé (v1.7.39) et casse les scripts `from __future__` — la dynamisation v2.1.1 ne couvre que la branche remplacement (classe F-70-2) | 5 scripts protégés par revert ; correctif (dynamiser CONTEXT_HEADER_L3 + insertion après la docstring d'en-tête) proposé sous GO futur |
| F4 | S4 | Certifications FAIL transitoires aux runs 1-2 du bootstrap (interactions : 55 en-têtes §0 stale v1.7.39 ≠ v1.7.40) | inhérent au premier bump SHARED sous scelleur v2.3 : la propagation §0 doit précéder la certification — séquence documentée, tout vert dès le run 3 |
| F5 | S4 | `rapport-efficacite-task105-{garanties,flux,bootstrap-consolide}.json` côté hôte écrasés par les re-jeux task107 | conforme au dessein (rapports machine régénérables) — les originaux du dépôt demeurent intacts (R4), copies re-jeu sous noms `rapport-nonregression-task107-*.json` |

## Verdict

**PASS** — 6/6 items de la directive rendus, answer key D001-D009 re-jouée 9/9 verified (voir plan), 5 findings classés et traités (0 S1/S2), garanties intactes (certification 6/6 ×3, É1 rc=0, R2 0 rétrogradation, idempotence ×2 byte-identique, dry-run 0 mutation 4/4).
