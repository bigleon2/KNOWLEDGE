# Clone de discussion — session web-f492e049 (Task 112), 24ᵉ de la lignée

> Session : web-f492e049 · chat 17b8e0d9-d141-4dda-b86b-8b152e773f70 · canal zai-web. Généré le 2026-11-22 par clone-chat v2.0.2 (7+1 étapes). Directives du tour : traces `1a1fc6f31a7bf61d` (installation + gen-plan(step) tests $FACON2 10 skills + CW --bloc ×2 + clone-chat), `1a1fc7b1728869e9` (E13 : PROMPT-GATEWAY inconditionnel), `1a1fc8f117057cb1` (E13b : anti-boucle G1 — 1 redémarrage max), `1a200e89c5121855`/`1a201ad8840eb411` (E13c : analyse du dernier clone + continuation).

## §0 — Contexte Système (SHARED v1.7.43)

> Écosystème Knowledge : skills/ = racine | KB = skills/KNOWLEDGE.md | @mon-ecosysteme/ (9 corpus) | @historique/ (archive R4). Conventions kebab-case/semver/#token. Règle d'or n°6 : FRANÇAIS exclusif dès le premier mot. Référence canonique : « mon skill X » = forme installée skills/X/SKILL.md, jamais le PM du corpus. Versionnées : gen-plan v3.45.0 · correct-work v2.12.0 · clone-chat v2.0.2 · agent-prompt-engineering v1.2.0 · re-curation v1.2.4 · SHARED v1.7.43 · PM-INSTALL v1.10.0.

## §1 — Worklog chronologique (fenêtre du clone : suite 158)

| Suite | Date | Contenu (résumé exécutable) |
|---|---|---|
| 158 | 2026-11-21→22 | Task 112 — installation INSTALLE ×2 idempotent (56 SHA 0 divergence, certification 6/6) · PLAN G1-G14 D001-D014 (E7-DISP 6 points, E8 PASS) · G1 APE v1.0.1→v1.1.0→v1.2.0 PROMPT-GATEWAY INCONDITIONNEL (commits f7b97018 + bc45749b, phases A-B systématiques / C-D si COMPLEXE ≥2/5, triggers 13 cas, voie L 22 entrées, arbitre 55/55) · E13b anti-boucle D013 (compteur 0/1 consommé 0) · 9ᵉ recyclage sandbox arbre-amputé (70 dirs) → INSTALLE-REPARÉ (reset 2 807, 55 div, 56 SHA) · E13c G1b+D014 · G1b analyse 23ᵉ clone → download/analyse-dernier-clone.md (7 sections, recoupements mesurés) · G2-G8 : 10 syncs evals versions + re-curation v1.2.3→v1.2.4 (§6 Relations, cascade KO-L004 KB+pins ×2, PATCH) + diagnostic T1 dynamisé (casse + équivalences, KO-L003) + préservation merge t4/t5/t6 · 10ᵉ recyclage en chaîne → rétablissement idem · G9 CW --bloc 1re passe PASS 6/6 blocs · G10-G12 tests écosystème 3× NO-GO documentés (poids < 30 Kio · couche agents saine · signaux résorbés + blast radius CRITIQUE protecteur APE 31 backward) · G13 CW --bloc 2e passe PASS 6/6, 13/14 verified |

## §2 — Artefacts de la fenêtre (Étape 2)

| Artefact | Nature | Détail |
|---|---|---|
| `download/plan-2026-11-21-optimisation-ecosysteme.md` | LIVRABLE | plan 15 groupes (G1, G1b, G2-G14), answer key D001-D014 (13 verified, D010 vérifié au scellage du présent clone), extensions E13/E13b/E13c |
| `download/analyse-dernier-clone.md` | LIVRABLE | analyse approfondie du 23ᵉ clone (G1b, D014) — identification, structure, lignée, 6 décisions, 6 pendances recoupées, 5 leçons, 6 implications |
| `skills/agent-prompt-engineering/` | MODIFIÉ v1.2.0 | PROMPT-GATEWAY inconditionnel : description + §A + §1.6 + references/prompt-gateway.md + evals 7 + triggers 13 + voie L |
| `skills/re-curation/` | MODIFIÉ v1.2.4 | §6 Relations (arêtes KB) + journal + cascade (KB, pins ECO_SKILLS ×2 arbres) + evals sync |
| 10 × `evals/evals.json` | SYNC | versions alignées frontmatter (memory 1.2.1, context 1.2.1, fleet/graph/refactoring-eng/refactoring-test 1.1.1, refactor-guard 1.8.1, agent-creator 2.3.0, autonomous-agent 1.2.1) |
| `scripts/optimisation-skills-rapport.json` | LIVRABLE | 12 skills T1-T6 consignés (préservation merge) |
| `scripts/cw-groupe-g1…g8-rapport.md` ×9 | LIVRABLES | CW(groupe, CIBLE) — tous PASS |
| `scripts/cw-projet-bloc1-rapport.md` + `cw-projet-bloc2-rapport.md` | LIVRABLES | CW --bloc 1re/2e passes — VERDICT GLOBAL PASS ×2 |
| `scripts/tests-ecosysteme-g10-g12.json` | LIVRABLE | 3 décisions NO-GO avec preuves |
| `scripts/g1-redemarrages.json` | ÉTAT | compteur anti-boucle 0/1 (0 consommé) |
| `scripts/t112-*.py` ×13 | OUTILLAGE | e13b/e13c, g1-cloture, g2, groupe (générique), g6, g9, g10-g12, g13, reconsignation, diagnostic dynamisé |
| origin/main | PENDANCE | 9 commits locaux SANS PUSH (f7b97018→CLOSE) — PAT non fourni, E15 inchangée 37 |

## §3 — Décisions, bugs, conventions (Étape 3)

**Décisions d'exécution Task 112** : le déclenchement PROMPT-GATEWAY est INCONDITIONNEL (D012 — phases A-B systématiques sur tout prompt, C-D si COMPLEXE ≥2/5) ; anti-boucle G1 = 1 redémarrage MAX (D013, 0 consommé, généralisé à tous les groupes) ; D004 dynamisée (KO-L003 : inconditionnalité → triviaux à déclenchement vrai, négatifs = périmètres autres skills) ; syncs evals = résorptions stale R2 montantes (pas des montées de version → pas de cascade, sauf re-curation v1.2.4 PATCH avec cascade KB+pins) ; 3× NO-GO fondés sur mesures (poids, .agent, blast radius).

**Bugs (tous résorbés en séance)** : (1) D013 scalaire yaml non fermé (défaut E13b — backslash sans guillemet fermant → ParserError ; réparé E13c) ; (2) diagnostic T1 faux positifs (casse littérale → IGNORECASE ; re-curation sans §1/§2 littéraux → équivalences documentées) ; (3) re-diagnostic écrasant les consignations t4/t5/t6 → préservation merge ; (4) regex statuts answer key non bornée (traversée inter-entrées) → regex bornée (?:(?!- id:).) ; (5) 9ᵉ + 10ᵉ recyclages sandbox (formes arbre-amputé 70 dirs) → rétablissements bootstrap INSTALLE-REPARÉ (2 807 fichiers reset, certification 6/6, écritures du tour survécues).

**Conventions (avec règle)** : KO-L009 maintenu (0 PAT fourni ce tour : 0 manipulation, 0 exposition, E15 inchangée 37) ; voie canonique respectée pour TOUTE modification (dépôt → commit AVANT bootstrap → bootstrap, jamais d'édition directe hôte — 8 commits propres G1-G8) ; statuts answer key subordonnés aux verdicts mécaniques (KO-L003 — bascules bornées) ; scellage clone = scan 0 secret.

## §3.5 — Context Drift (Étape 3.5)

| Drift | Type | Avant → Après | Réf. |
|---|---|---|---|
| 10 skills cibles | OPTIMISATION | versions evals divergentes (10/12) + re-curation sans § Relations → 12/12 sains T1-T6 (syncs + §6 + v1.2.4) | G2-G8 |
| agent-prompt-engineering | MONTÉE ×2 | v1.0.1 passif → v1.2.0 PROMPT-GATEWAY inconditionnel (auto-déclenchement à CHAQUE prompt) | G1+E13 |
| Answer key | EXTENSION | 11 décisions → 14 (D012 inconditionnel, D013 anti-boucle, D014 analyse clone) — 13 verified + D010 au scellage | E13/E13b/E13c |
| Sandbox | RÉCIDIVE ×2 | 9ᵉ + 10ᵉ épisodes arbre-amputé → rétablis INSTALLE-REPARÉ (bootstrap AVANT E1 validé en conditions réelles ×2) | suite 158 |
| Pendance PUSH | RÉACTIVÉE | 0 unpushed (Task 111) → 9 commits locaux (PAT requis — push immédiat dès PAT frais, leçon 98/101) | G14 clôture |

## §4 — Spécifications techniques (Étape 4 — fichiers prioritaires)

Séquence héritière recommandée :
1. `download/clone-chat-session-web-f492e049-20261122-task112.md` (présent clone) + `download/plan-2026-11-21-optimisation-ecosysteme.md` (le plan fait foi — 14/14 décisions verified au scellage) + `download/analyse-dernier-clone.md`.
2. Bootstrap canonique : `scripts/bootstrap-ecosysteme.py` à exécuter AVANT E1 à la reprise (garde É1, préflight anti-dérive — 10 récidives consécutives : la garde est OBLIGATOIRE).
3. Si un PAT frais est fourni : push immédiat des 9 commits locaux (leçon Task 98/101) — KO-L009 mémoire de commande, sortie masquée, scan 0 jeton complet.
4. Rappels propriétaire : (a) RÉVOCATION ancien PAT Task 107 [CRITIQUE] ; (b) décision cron 531684 (5ᵉ vérification : 0 job, 5ᵉ dispositif perdu).
5. PROMPT-GATEWAY actif : tout prompt propriétaire → phases A-B systématiques (C-D si COMPLEXE ≥2/5).

## §5 — Auto-clonage (Étape 5)

Le mécanisme de croissance : chaque tour CLOSE génère son clone (lignée Task 72→112, 24ᵉ) — les sections §1-§3 sont ENRICHIES par le clone du tour, les sections §0/§4-§5 sont RÉGÉNÉRÉES (état courant). clone-chat référencé (skill v2.0.2, déclencheurs §A). La session héritière reprend : lire le présent clone + worklog.md (suite 158) + le plan Task 112 (fait foi) — puis exécuter le bootstrap canonique AVANT E1 ; si un PAT frais est fourni, éteindre la pendance PUSH (9 commits) ; rappeler au propriétaire la révocation PAT (CRITIQUE) et la décision cron.

## Validation (Étape 6 — 8 checks)

| # | Check | Statut |
|---|---|---|
| S1 | Auto-suffisance (aucun « voir fichier X », lisible par un assistant neuf) | PASS |
| S2 | Complétude worklog (table §1 = fenêtre suite 158, ≥1 ligne) | PASS |
| S3 | Complétude skills (chaque système créé/modifié décrit §2 avec version et relations) | PASS |
| S4 | Complétude décisions (décisions avec contexte+conséquence, conventions avec règle) | PASS |
| S5 | Complétude bugs (5 bugs résorbés en séance, qualifiés avec correctif) | PASS |
| S6 | Complétude drifts (5 drifts typés, avant/après explicites) | PASS |
| S7 | Exécutabilité (§4 séquence héritière claire) | PASS |
| S8 | Auto-clonage (§5 croissance + clone-chat référencé + enrichi/régénéré) | PASS |

**Scellage : 8/8 PASS · 0 secret** (KO-L009 — 0 PAT fourni ni manipulé ce tour, E15 inchangée 37, scan 0 jeton `github_pat_[A-Za-z0-9_]{50,}` sur le clone).

(Étape 7 — Sauvegarde : présent fichier `download/clone-chat-session-web-f492e049-20261122-task112.md` + miroir dépôt + worklog suite 158.)
