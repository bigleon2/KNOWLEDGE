# Plan Task 12 — Re-matérialisation S2-α/β + réconciliation 28/29 + correct-work PROJET

## Métadonnées
- **Date** : 2026-10-10 (session web-b93f42fa, canal sain — mesures byte-level uniquement, leçon Task 11)
- **Directive propriétaire** : « re-valider S2-α/β (cale + 5 lignes SKILL.md — jamais matérialisées) ; réconcilier la tension 28 compétences contre 29 entrées KB ; exécute correct-work ; exécute gen-plan:correct-work(projet) »
- **gen-plan** : v3.21.0 (frontmatter installé — source de vérité, contrat §1.5 correct-work)
- **correct-work** : v2.7.0, mode PROJET (couplage Étape 1 OBLIGATOIRE — §1.5)
- **Profil** : NORMAL (hook E1-RES : worklog lu, G-RES niveau 0, fraîcheur plan OK — plan nouveau)
- **Estimation #token** : ~14 000 (exécution complexe 4+ skills — grille §4)
- **Règle d'or n°2** : 0 commit, 0 push — HEAD 3eebe65, travail en arbre local uniquement

## E1 — Livrables + critères de succès
1. **S2-α** : cale racine `scripts/verify-correct-work.py` → délégation au canonique `skills/correct-work/scripts/verify-correct-work.py` + refus EXPLICITE des modes non délégués (résorption finding S3 SO Task 10 — jamais d'avalage silencieux). Succès : sha256(stdout shim) == sha256(stdout canonique) ×2 runs ; 16/16 PASS.
2. **S2-β** : 5 lignes `skills/correct-work/SKILL.md` — §10.1 L275/L276 éditées, 1 garde ARRÊT EXPLICITE insérée, L279 #token éditée, §2.6 L194 `Agent: correct-work v2.7.0`. Succès : grep « ou autonome » = 0, « v2.4.0 » = 0, 436 lignes, vcw 16/16.
3. **S2-ε (réconciliation 28/29)** : compteur `kb_entrees` de `skills/gen-plan/scripts/ensure-installed.py` → regex stricte `^## [a-z0-9-]+ v<semver>$` (KO-L003 : dynamiser l'instrument, JAMAIS ajuster la réalité — la KB reste source de vérité à 28 entrées ; la section « Décisions d'architecture » n'est pas une entrée). Succès : --check kb_entrees=28, verdict INSTALLE rc0, ×2 canaux (canonique + shim racine) ×2 runs.
4. **correct-work PROJET** (Étapes 1-5) → verdict + rapport + worklog Task 12.

## E2 — Ressources (mesuré)
Clone HEAD 3eebe65 (dirty 59) ; canonique vcw 307 L (md5 ac48d004) vs racine v1.0.0 99 L (md5 b2b6a39f — double divergent vivant) ; KB 28 entrées skill + 1 section Décisions = 29 headers ; verify-registry-sync 28/28 sync, ghosts 0, 67 GAP plateforme par conception ; G-RES niveau 0. Aucun gap bloquant.

## E3 — Type 2 (ingénierie écosystème — protocole + scripts ; rapport .md secondaire)

## E5 — Skills mobilisés
gen-plan (plan) · correct-work v2.7.0 PROJET · resource-monitor (G-RES fait) · arbitres : verify-correct-work, check-ecosysteme-integrity, test-coherence-interactions, verify-cross, generer-pm-skill, verify-registry-sync, ensure-installed · leçons KO-L003/L007 appliquées en continu.

## E7 — Séquence (série par défaut — philosophie #4)
| Phase | Contenu | #token |
|---|---|---|
| A | S2-α matérialisation + validation ×2 canaux | 2 000 |
| B | S2-β 5 lignes SKILL.md + validation (grep 0 + vcw 16/16) | 1 500 |
| C | S2-ε compteur + validation ×2 idempotence (28/28) | 1 500 |
| D | correct-work PROJET Étapes 2-5 → verdict | 4 000 |
| E | R2 arbitres vs baseline Task 11 (+ AVEUGLE si divergence persistante É5) | 3 000 |
| F | Rapport download/ + worklog Task 12 + synthèse | 2 000 |

## Answer key (hook E1 — décisions D001-D006)
| ID | Décision | Vérification exécutable | Source | Priorité | Statut |
|---|---|---|---|---|---|
| D001 | Cale = délégation + refus explicite rc 64 | sha256(stdout shim)==sha256(stdout canonique) ×2 ; rc 64 sur arg `<rapport.md>` | directive S2-α + finding S3 SO Task 10 | S2 | pending |
| D002 | 5 lignes SKILL.md exactement (4 édits + 1 insertion) | grep « ou autonome »=0 ; « v2.4.0 »=0 ; wc -l=436 ; vcw 16/16 | directive S2-β | S2 | pending |
| D003 | Compteur regex strict (KO-L003) | --check kb_entrees=28, ×2 canaux, ×2 runs | mesure verify-registry-sync 28/28 | S2 | pending |
| D004 | PM master §10.1/§2.6 staleness = FINDING, pas de fix | grep PM : lignes d'origine intactes | périmètre directive (« SKILL.md ») + KO-L004 (régén PM = directive dédiée) | S3 | pending |
| D005 | AVEUGLE seulement si divergence persistante à l'É5 | hook §1.3 correct-work | SKILL.md §1.3 | S2 | pending |
| D006 | 0 commit / 0 push ; HEAD inchangé 3eebe65 | git rev-parse avant/après | règle d'or n°2 | S1 | pending |

## E8 — Validation du plan
answer-key-checker.py exécuté (verdict consigné) ; fallback honnête (règle d'or n°1, journalisé) si l'arbitre est inopérant dans la layout courante : validation manuelle des critères D001-D006.

## R2 — Baselines Task 11 (non-régression)
vcw 16/16 · integrity 60/60 · coherence 48/3/0 · verify-cross 83/84 (C006 héritée, non bloquante) · generer-pm 3/3 · registry-sync 28 sync / ghosts 0 · hook --check rc0 INSTALLE
