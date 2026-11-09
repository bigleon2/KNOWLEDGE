# Analyse re-curation Task 82 — cibles-recursion (skills/agents/agents autonomes) + cibles-recursion-no-skill (autres éléments)

> **Livrable G5 — Task 82** (directive trace `1a1be717bb0fbdb1`, items 6-7) · Horodatage : 2026-11-09T04:45:00Z
> Méthode : inventaire mécanique G1 (`scripts/task82-inventaire.py` — 71 skills mesurés : poids, sections, references/, scripts, usage worklog réel) + protocole re-curation v1.2.2 (seuils : LOURD ≥ 30 Kio, blocs extractibles ≥ 1,5 Kio HISTORIQUES/RÉFÉRENCE/DORMANTS, vivants) + file KB consignée (« version-management RE-CURÉ −45,4 % → iphone19 RE-CURÉ −27,3 % → **iphone18 (prochaine)** → skill-creator [noyau] → web-reader → cahier-des-charges → iphone17 ; pdf/pptx = plateforme ») · règle d'or n°5 : poids et vivance MESURÉS.

## §1 — LISTE « cibles-recursion » (skills/agents/agents autonomes — triée par priorité)

| Priorité | Cible | Mesure | Justification |
|----------|-------|--------|---------------|
| **P1** | **iphone18** | 41 395 o (**40,4 Kio LOURD**, seuil 30) · **0 references/** · 39 sections · 1 script · usage 5 · PM source `@photos/iphone18-photos.md` 36 023 o | **Tête de file KB explicite** (consignée Task 81 G2 : « iphone18 prochaine ») — même famille que iphone19 (curé Task 81 : 54,3→39,5 Kio, −27,3 %) : le pattern d'extraction (blocs changelogs/origines/notes/livrables/preset/squelette) est PROUVÉ, scriptable et la preuve R4-INTÈGRE est calibrée (blocs ↔ PM source byte-identité) |
| **P2** | **skill-creator** | 41 323 o (40,4 Kio LOURD) · 1 reference · 9 scripts · 35 sections · usage 9 | 2ᵉ plus gros skill écosystème non-curé — file KB (« skill-creator [noyau] », consignée Task 72 G3) — noyau créateur de skills, candidat aux blocs dormants (schémas, conventions, archives d'evals) |
| **P3** | **iphone17** | 35 013 o (34,2 Kio LOURD) · 0 references/ · 39 sections · usage 4 | 3ᵉ membre de la famille photo (génération 17, époque) — même structure P1, file KB après skill-creator |
| **P4** | **cahier-des-charges** | 31 583 o (30,8 Kio LOURD, juste au-dessus du seuil) · 4 references/ existantes · 14 sections · usage faible worklog mais skill pivot M1-M7 | File KB consignée (« cahier-des-charges ») — les 4 references/ existantes proument la extractibilité ; le cœur opérationnel M1-M7 doit demeurer inline (écart C4 possible à consigner, précédent iphone19) |

### Évalués et NON ciblés (motifs mesurés)

| Élément | Mesure | Verdict |
|---------|--------|---------|
| gen-plan | 30 697 o INTERMÉDIAIRE — **curé Task 72** (104,0→29,95 Kio, −71,2 %, 9 blocs R4 → 15 references/) | NON — déjà re-curé, sous seuil ; re-cible seulement au re-ancrage d'une version majeure |
| correct-work | 29 331 o — sous seuil 30 Kio · 60 sections denses (contrats) | NON — sous seuil, arbite de confiance |
| iphone19 | 40 431 o — **curé Task 81** (−27,3 %, 6 blocs R4, POST MAINTIEN, écart C4 consigné cœur opérationnel) | NON — re-curé, verdict MAINTIEN vivant |
| version-management | 25 783 o — **curé Task 79** (−45,4 %, 7 references/) | NON — re-curé, sous seuil |
| pdf (58 056) · pptx (38 746) · web-reader (32 085) · LLM (21 913) · TTS (20 054) · video-understand (24 867) · image-edit (24 774) · web-search (26 355) · charts (21 980) · xlsx · docx · VLM/ASR/image-*/fullstack-dev/skill-finder-cn/gif-* | 19,9-58,1 Kio | NON — **plateforme** (décision propriétaire pdf/pptx : structurées `references/`+`scenes/`+`engines/` natives, non-vivantes monolithiquement — le SKILL.md n'est pas chargé avec ses references) |
| refactor-guard (22 799) · dessin-technique (22 265) · analyse-doc-s4mk2 (19 951) · re-curation (19 450) · vue-upload (19 246) · clone-chat (18 477) · orchestrateur-tsi (15 203) · pm-skill (14 325) · alias-eco (12 120) · inter-scripts (10 663) · tsi-validator (9 711) · knowledge-observer v1.1.0 (7 400, converti G2) · disciplines n°50-55 (13-19 Kio) | tous < 30 Kio | NON — sous seuil LOURD |
| agents .agent (tsi-architect 4 869 · orchestrateur-tsi 6 851 · agent-TSI 7 348) + knowledge-observer.agent (5 302) | ≤ 7,3 Kio | NON — légers, mémoire de travail |
| autonomous-agent.agent + agent-creator.agent (gabarits references/) | gabarits | NON — documentation de format, pas des exécutants |

## §2 — LISTE « cibles-recursion-no-skill » (éléments vivants hors skills — triée par priorité)

**Verdict : LISTE VIDE — aucun élément hors skills ne requiert une re-curation progressive disclosure ; motifs mesurés par élément :**

| Élément | Mesure | Verdict motivé |
|---------|--------|----------------|
| `PROMPT-MAITRE-GEN-PLAN-v3.41.0.md` | **222 074 o** (plus gros artefact vivant) | NON — **artefact DÉRIVÉ** : projection auto-portante du skill gen-plan (SHARED §6.2 : les references/ du SKILL sont EMBARQUÉES dans le PM car les IAs externes n'ont pas accès à l'arbre — le poids est la conséquence de l'auto-portance, pas de la dormance) ; corpus --check **4/4 COHERENT** (le recalibrage KO-L004 suit le skill : régénérer le PM à la main casserait la parité de génération) — sa « cure » passe par gen-plan (déjà curé) + la régénération, pas par une extraction |
| `PROMPT-MAITRE-SHARED.md` | 52 913 o | NON — socle à **lecture ciblée par sections** (§0 + sections dédiées §3/§4/§7 + règles d'or §9 — directive 2026-11-06) : la divulgation progressive est OPÉRÉE par le contrat de lecture, pas par le découpage ; sous contrôle à 52,9 Kio (point de vigilance consigné si > ~80 Kio) |
| `PROMPT-MAITRE-INSTALL-ECOSYSTEME.md` (52 032) · PM CORRECT-WORK (51 621) · PM CLONE-CHAT (34 882) · PM REFACTOR-GUARD (27 108) | corpus 4/4 | NON — projections dérivées des skills (KO-L004 — même motif que PM GEN-PLAN) ; leurs poids suivent les skills respectifs |
| `@photos/iphone19-photos.md` (48 903) · `iphone18-photos.md` (36 023) · `iphone17-photos.md` (29 310) | sources v1.1-v0.12 | NON — **SOURCES R2 intégrales par conception** : le PM source fait foi pour les preuves R4-INTÈGRE de la re-curation des skills photo (Task 81 : « PM source intégral — R2 byte-identique, intact par la re-curation ») ; extraire des blocs d'une SOURCE casserait la ligne métier (SKILL = projection du PM, jamais l'inverse) |
| `README.md` @mon-ecosysteme | 26 668 o | NON — sous seuil, doc de corpus |
| `SYNC-CONTEXT.md` | 20 936 o | NON — sous seuil ; réécrit à CHAQUE resync (churn maximal : toute extraction serait périmée à la passe suivante — contre-productif par nature) |
| `PROMPT-ULTRA-MAITRE-ORCHESTRATION.md` | ~8 000 o | NON — orchestrateur LÉGER par conception (routage = divulgation progressive structurelle ; recalibrage = régénération idempotente, opérée G2) |
| KB `KNOWLEDGE.md` | 214 926 o | NON — **registre à entrées `## <skill> v<semver>`** : la divulgation progressive est STRUCTURELLE (consultation par entrée, jamais chargée monolithiquement — règle Zéro : « registre KB source de vérité ») ; le re-découper détruirait le protocole de découverte (SHARED §2.3) |
| `worklog.md` | 543 201 o | NON — journal append-only R5 (lecture par QUEUE — suites horodatées ; jamais chargé intégralement par contrat) |
| `@historique/historiques-par-skill/*.md` (gen-plan.md 48 644 en tête) + `@historique/prompts-maitres/**` (≈40 PMs archivés) + `@historique/photos/**` | archives | NON — **archives R4/R2 par conception** (cold storage byte-identité, `git mv` jamais édité) : les re-curater contredit leur fonction de conservation |
| `@Bibliotheque-skills-Multi-IA/**` (6 prompts plateforme + tools) | statique | NON — projections dérivées (tools/generate_prompts.py) |
| `@GHORG-ecosysteme/**` · `@Alias/aliases.json` · evals/** · scripts/** (protocole-test.py 50 Kio etc.) | config/registres/code | NON — exécutés ou ciblés par nature, jamais chargés monolithiquement (le code n'est pas un artefact de divulgation) |

## §3 — Exécution (item 7 de la directive : « par ordre de priorité »)

- **P1 iphone18 exécutée en G6** (fenêtre de contexte de la présente passe) — protocole P0→P7 complet, harnais **v1.2.2** (P0 --pre GO obligatoire avant toute extraction).
- **P2 skill-creator · P3 iphone17 · P4 cahier-des-charges : EN FILE** (honnêteté R5 — la file KB reste l'ordonnateur ; la fenêtre de contexte de la session borne le nombre de campagnes P0-P7 complètes exécutables SANS dégrader la qualité des preuves ; chaque campagne = P0-P7 + cascade + miroir, ≈ 1 groupe de travail).
- Les listes vides (§2) ne déclenchent AUCUNE action (motifs documentés ci-dessus — la directive est satisfaite par l'analyse : « savoir si… » → non, sauf la file skills ci-dessus).
