# Clone de discussion — session web-f492e049 (Task 112, tour G15-G19), 25ᵉ de la lignée

> Session : web-f492e049 · chat 17b8e0d9-d141-4dda-b86b-8b152e773f70 · canal zai-web · trace directive 1a201cc4330be619. Généré le 2026-11-22 par clone-chat v2.0.2 (7+1 étapes). Fenêtre du clone : réexpédition directive avec PAT fourni (PUSH) + 2 analyses nouvelles (ensure-installed.py, déclenchement agent-prompt-engineering × gen-plan) + tests + CW --bloc + clone. Chaîne mode step SANS validation propriétaire (anti-boucle D013 respectée : 0 redémarrage ce tour).

## §0 — Contexte Système (SHARED v1.7.44)

> Écosystème Knowledge : skills/ = racine | KB = skills/KNOWLEDGE.md (56 entrées) | @mon-ecosysteme/ (9 corpus) | @historique/ (archive R4, rescellement v2.2 round-trip vérifié). Conventions kebab-case/semver/#token. Règle d'or n°6 : FRANÇAIS exclusif dès le premier mot. Référence canonique : « mon skill X » = forme installée skills/X/SKILL.md, jamais le PM du corpus. Versionnées : gen-plan v3.46.0 · correct-work v2.12.0 · clone-chat v2.0.2 · agent-prompt-engineering v1.2.0 · re-curation v1.2.4 · SHARED v1.7.44 · PM-INSTALL v1.10.4 · pin ECO_SKILLS 56 entrées ×2 arbres. Certification : bootstrap ALL-PASS-6/6 · integrity 116/116 ×2 · cohérence interactions PASS STRICT.

## §1 — Worklog chronologique (fenêtre du clone : suite du tour)

| Suite | Date | Contenu (résumé exécutable) |
|---|---|---|
| 159 | 2026-11-22 | PUSH initial aaac4fa1→8af48df0 (9 commits Task 112 G1-G14 éteints — PAT propriétaire consommé via variable d'environnement éphémère, jamais persistée) · G15 analyse ensure-installed.py (commit aaac4fa ≡ état local — 238 L) : couverture = 17/17 exigences KB couvertes par garde étendue Task 56 MAIS agent-browser (requis hors-KB, contingences E5) invisible → faux positif INSTALLE prouvé (T1) + promesse Phase A jamais tenue → patch garde SKILLS_REQUIS_GENPLAN + réparation miroir + certification-complete.py après clone (best-effort timeout 600 s) · tests T1-T8 8/8 PASS (0,033 s) · G16 constat 0 référence APE au SKILL.md gen-plan (divergence KB↔SKILL.md — relation « §3 du skill » inexacte) → montée v3.45.0→v3.46.0 : §1.16 hook É1-PROMPT-GATEWAY (après É1-INSTALL, AVANT analyse E1) + §3 + YAML deps + description + KB 4 champs · cascade KO-L004 COMPLÈTE : delta verrouillé + PM v3.46.0 généré mécaniquement (SHARED v1.7.44/PM-INSTALL recalibrés) + PM v3.45.0 dédup @historique R4 + journal R4 + pin ×2 3.46.0 + evals sync 3.10.0→3.46.0 (4ᵉ cas motif stale) + cascade transverse 103 en-têtes §0 v1.7.40/43→v1.7.44 + 9 citations vives + agent-creator + rescellement archive v2.2 · arbitres 11a/11c dynamisés KO-L003 (transitions « 3.10.0→3.46.0 » = historique légitime) · bootstrap ALL-PASS-6/6 · G17 idempotence ×2 arbitres 4/4 PASS · G18 CW --bloc 3ᵉ passe VERDICT GLOBAL PASS · livrable download/rapport-g15-g16-analyses.md |

## §2 — Artefacts de la fenêtre (Étape 2)

| Artefact | Nature | Détail |
|---|---|---|
| `skills/gen-plan/scripts/ensure-installed.py` | MODIFIÉ (G15) | garde requi hors-KB (SKILLS_REQUIS_GENPLAN figé documenté) + promesse Phase A tenue ; champ diagnostic requis_genplan_manquants |
| `skills/gen-plan/` v3.46.0 | MONTÉE (G16) | §1.16 hook É1-PROMPT-GATEWAY + §3 ligne APE + YAML dependency >= 1.2.0 + description ; evals sync 3.46.0 ; PM v3.46.0 corpus ; journal v3.45.0 migrée R4 |
| `scripts/delta-genplan-v3460.json` | NOUVEAU | delta verrouillé (history + subs[]) |
| `scripts/check-ecosysteme-integrity.py` ×2 arbres | MODIFIÉ | pin gen-plan 3.46.0 (KO-L004) |
| 103 × SKILL.md | RECALIBRÉS | en-têtes §0 SHARED v1.7.44 (cascade transverse) |
| 9 × SKILL.md disciplines + agent-creator | RECALIBRÉS | citations vives gen-plan v3.46.0 |
| `scripts/test-coherence-interactions.py` | DYNAMISÉ | checks 11a/11c : tolérance transitions documentées (KO-L003) |
| `scripts/t112-g15-tests-ensure.py` + rapport | OUTILLAGE | T1-T8 avant/après (preuve original aaac4fa) |
| `scripts/t112-g16-genplan-v3460.py` | OUTILLAGE | montée idempotente cascade complète |
| `scripts/t112-g17-idempotence.py` + rapport | OUTILLAGE | re-jeux ×2 arbitres 4/4 PASS |
| `download/rapport-g15-g16-analyses.md` | LIVRABLE | réponses Q1 (couverture installation) + Q2 (déclenchement APE) + perfs |
| `scripts/cw-groupe-g16-rapport.md` | LIVRABLE | CW(groupe G16, CIBLE) PASS |
| `download/clone-chat-session-web-f492e049-20261122-task112-tour-g15-g19.md` | LIVRABLE | présent clone 25ᵉ + miroir dépôt |
| origin/main | ÉTAT | aaac4fa1→8af48df0 poussé en tête de tour ; commits G15-G19 poussés en clôture (PAT fourni) |

## §3 — Décisions, bugs, conventions (Étape 3)

**Décisions d'exécution du tour** : PUSH en tête de tour (directive liste PUSH ×2 — premier push = sauvegarde de l'état Task 112 avant les travaux ; second = publication) ; PAT propriétaire consommé UNIQUEMENT via variable d'environnement éphémère de la commande push (jamais persistée fichier, jamais réimprimée) ; SKILLS_REQUIS_GENPLAN figé et documenté (KO-L003 : le figé est vérifiable) extensible aux futurs requis hors-KB ; É1-PROMPT-GATEway = filet de sécurité (si le PROMPT-GATEWAY a déjà traité le prompt, passage direct journalisé) ; cascades arbitres dynamisées KO-L003 (jamais ajuster la réalité : la transition « 3.10.0→3.46.0 » est un historique légitime).

**Bugs (tous résorbés en séance)** : (1) faux positif arbitre 11a « mention stale 3.10.0 » sur la mention journal de sync → dynamisation (regex transition A→B) ; (2) idem check 11c ; (3) cascade transverse incomplete côté générateur (103 en-têtes §0 v1.7.40/43 non rafraîchis par --refresh-ctx NO-OP) → recalibrage global mécanique dérivé du PM SHARED courant ; (4) heredoc Python tuple (replace argument 2 tuple) → édition Edit directe ; (5) verdict_ok fenêtre tail 120 car. ratant « INSTALLE » en tête de JSON → head+tail ; (6) T1 test G15 : verdict attendu ABSENT-DERIVE erroné (le comportement RÉEL du bug = INSTALLE à tort) → test réécrit pour prouver le faux positif.

**Conventions (avec règle)** : règle d'or n°4 respectée (dépôt → commit AVANT bootstrap — 7 commits propres ce tour : G15 patch, G16 ×5, rescellement, manifeste, recalibrage transverse) ; KO-L009 adapté (PAT fourni ce tour : consommation éphémère unique, scan 0 jeton sur le clone) ; scellage clone = scan 0 secret ; anti-boucle D013 généralisée respectée (0 redémarrage).

## §3.5 — Context Drift (Étape 3.5)

| Drift | Type | Avant → Après | Réf. |
|---|---|---|---|
| gen-plan | MONTÉE | v3.45.0 (0 référence APE) → v3.46.0 (É1-PROMPT-GATEway avant E1 + §3 + YAML) | G16 |
| ensure-installed.py | EXTENSION | garde KB seule (agent-browser invisible, faux positif prouvé) → garde KB ∪ requis hors-KB + Phase A tenue | G15 |
| en-têtes §0 | STALE résorbé | SHARED v1.7.40/43 (103 fichiers) → v1.7.44 uniforme | G16 |
| evals gen-plan | STALE résorbé | 3.10.0 figé depuis matérialisation → 3.46.0 sync | G16 |
| Pendance PUSH | ÉTEINTE | 9 commits locaux → poussés aaac4fa1→8af48df0 + commits du tour | PUSH |
| Chaines d'ouverture | CLARIFIÉE | PROMPT-GATEway implicite → explicite : APE (inconditionnel) → É1-INSTALL → É1-PROMPT-GATEway → E1 | G16 |

## §4 — Spécifications techniques (Étape 4 — fichiers prioritaires)

Séquence héritière recommandée :
1. `download/clone-chat-session-web-f492e049-20261122-task112-tour-g15-g19.md` (présent clone) + clone 24ᵉ (contexte Task 112 complet) + plan Task 112 (14/14 verified, fait foi).
2. Bootstrap canonique : `scripts/bootstrap-ecosysteme.py` AVANT E1 à la reprise (garde É1 — 10 récidives consécutives documentées : la garde est OBLIGATOIRE).
3. gen-plan v3.46.0 : la chaîne d'ouverture = PROMPT-GATEway (APE inconditionnel) → É1-INSTALL (--check) → É1-PROMPT-GATEway → E1 — ne jamais sauter le pré-traitement des demandes complexes.
4. ensure-installed.py : tout nouveau requis gen-plan hors-KB → ajouter à SKILLS_REQUIS_GENPLAN (référence §3/§1.16) ou inscrire au registre KB.
5. Rappels propriétaire : (a) RÉVOCATION du PAT utilisé (transmis en clair dans la conversation — régénérer après la session) [CRITIQUE] ; (b) RÉVOCATION ancien PAT Task 107 ; (c) décision cron 531684 (0 job, 5ᵉ vérification).

## §5 — Auto-clonage (Étape 5)

Le mécanisme de croissance : chaque tour CLOSE génère son clone (lignée Task 72→112, 25ᵉ) — les sections §1-§3 sont ENRICHIES par le clone du tour, les sections §0/§4-§5 sont RÉGÉNÉRÉES (état courant). clone-chat référencé (skill v2.0.2, déclencheurs §A). La session héritière reprend : lire le présent clone + le clone 24ᵉ + worklog.md (suite 159) — puis exécuter le bootstrap canonique AVANT E1 ; rappeler la révocation PAT au propriétaire (CRITIQUE — deux tokens concernés) et la décision cron.

## Validation (Étape 6 — 8 checks)

| # | Check | Statut |
|---|---|---|
| S1 | Auto-suffisance (aucun « voir fichier X », lisible par un assistant neuf) | PASS |
| S2 | Complétude worklog (table §1 = fenêtre suite 159, ≥1 ligne) | PASS |
| S3 | Complétude skills (chaque système créé/modifié décrit §2 avec version et relations) | PASS |
| S4 | Complétude décisions (décisions avec contexte+conséquence, conventions avec règle) | PASS |
| S5 | Complétude bugs (6 bugs résorbés en séance, qualifiés avec correctif) | PASS |
| S6 | Complétude drifts (6 drifts typés, avant/après explicites) | PASS |
| S7 | Exécutabilité (§4 séquence héritière claire) | PASS |
| S8 | Auto-clonage (§5 croissance + clone-chat référencé + enrichi/régénéré) | PASS |

**Scellage : 8/8 PASS · 0 secret** (KO-L009 — PAT consommé via variable d'environnement éphémère uniquement, jamais inscrit au clone ni aux rapports ; scan 0 jeton `github_pat_[A-Za-z0-9_]{50,}` sur le clone).

(Étape 7 — Sauvegarde : présent fichier `download/clone-chat-session-web-f492e049-20261122-task112-tour-g15-g19.md` + miroir dépôt + worklog suite 159.)
