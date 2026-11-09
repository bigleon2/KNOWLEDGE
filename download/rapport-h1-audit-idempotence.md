# Rapport H1 — audit de conformité idempotente (skills/agents/scripts)

**Session** : web-f90062ce (2026-10-24) · **Directive** : « audit de conformité idempotente des skills/agents/scripts + réécriture idempotente des non-conformes » (worklog H3, reste à faire).

**Norme (définie avant audit, jamais ajustée aux résultats)** : CONFORME = rejeu ×2 produit le même état final observable. Trois régimes : (1) **ÉTAT** (registres, KB, configs, .gitignore, corpus) → idempotence STRICTE byte-identique ; (2) **LIVRABLES** (rapports, artefacts générés) → zéro accumulation (écrasement en place ; l'horodatage de fraîcheur écrasé est un état mutable légitime) ; (3) **TEMPORAIRES** → auto-nettoyés.

## Périmètre et méthode

- **253** scripts Python (AST), **11** shell, **59** JS/TS (heuristiques), **219** SKILL.md, **2** agents — hors @historique (archives R2/R4 jamais rééditées) et download/.
- Analyseur statique volontairement STRICT (`scripts/task-h1-audit-idempotence.py`, persisté, idempotent) : toute écriture sans garde visible = NON CONFORME STATIQUE → revue manuelle systématique avant tout verdict (jamais de patch aveugle).
- Scan ciblé des marqueurs de vraie non-idempotence : append, horloge écrite, nom incrémental.

## Résultats consolidés

- LECTURE_SEULE : **334** — conformes par nature
- EFFETS_GARDES (statique) : **114** — conformes (gardes détectées : lecture/comparaison, exists, hash, dry-run)
- EFFETS_NON_GARDES (statique) : **94** → qualifiés ci-dessous

## Qualification des NON CONFORMES statiques

### Revus individuellement — 10 fichiers (1 corrigé, 9 requalifiés conformes)

- **scripts/install-ecosystem.py** → NON CONFORME AVÉRÉ → CORRIGÉ v2.0.1 — P2 append .gitignore : le bloc « Caches locaux écosystème » se dupliquait à chaque rejeu (accumulation d'ÉTAT). Garde ajoutée (lecture + skip si bloc présent). Preuve : scripts/task-h1-test-install-ecosystem.py — sandbox (import module + monkeypatch REPO_DIR, JAMAIS de rejeu sur cible réelle : la P2 purge download/), rejeu ×3 PASS byte-stable, test lui-même idempotent ×2.
- **scripts/refactoring-test-graph.py** → CONFORME (requalifié) — Rapport écrasé en place, zéro horloge → contenu déterministe (outil n°55, socle §2ter — vivant confirmé par références KB/SYNC-CONTEXT/PM gen-plan v3.25.0).
- **scripts/audit-provenance.py** → CONFORME (requalifié) — Zéro horloge ; fix orphelins convergent (2e passe : plus rien à retirer) ; rapport écrasé en place. Entrée KB vivante.
- **skills/alias-eco/scripts/alias-manager.py** → CONFORME (requalifié) — Garde anti-doublon stricte par clé normalisée + tri déterministe (SKILL.md §1.4.2) — garde algorithmique invisible à l'AST ; date « mis_a_jour » = fraîcheur écrasée en place. Registre @Alias vivant : rejeu = no-op fonctionnel.
- **skills/inter-scripts/scripts/is_client.py** → CONFORME (requalifié) — Requêtes one-shot en fichiers temporaires à nom unique (pid+time_ns), supprimés après usage — zéro accumulation.
- **mini-services/compile-yaml.py** → CONFORME (requalifié) — Compilation écrasée en place (open 'w'), « compiled_at » = fraîcheur ; vestige non référencé corpus/KB.
- **skills/aminer-daily-paper/scripts/common.py** → CONFORME (requalifié) — Rapports écrasés en place (write_text), timestamps = fraîcheur ; skill plateforme miroir.
- **skills/skill-creator/scripts/aggregate_benchmark.py** → CONFORME (requalifié) — output_json écrasé en place (open 'w'), timestamp = fraîcheur d'agrégat.
- **skills/skills-inventory/scripts/generate_skills_md.py** → CONFORME (requalifié) — skills.md écrasé en place ; les dates affichées dérivent du FS (fromtimestamp), pas d'une horloge d'état.
- **skills/quiz-html/scripts/build_quiz_html.py** → CONFORME (requalifié) — HTML livrable écrasé en place (write_text).

### ONE-SHOT / OUTIL DE SESSION HISTORIQUE — 17 fichiers : VERDICT LEÇON — non rejoués en production

- scripts/_archive/generate-knowledge-v3.py
- scripts/_archive/task17-rapport-baseline.py
- scripts/_archive/task21-p2b-kb-sync.py
- scripts/task-b2-port-refs-v3250.py
- scripts/task18-completion-pms.py
- scripts/task18-kb.py
- scripts/task18-pm-install-v180.py
- scripts/task18-shared-v178.py
- scripts/task20-registry-update.py
- scripts/task25ter-cascade.py
- scripts/task25ter-cascade2.py
- scripts/task39-test-vue-upload-v120.py
- scripts/task45c-generer-skills-photo.py
- scripts/task48-clone-checks.py
- scripts/task48-historique-photos.py
- scripts/task48-ip19-v010-projection.py
- scripts/task48-recalibrage-1944.py

### GÉNÉRATEUR DE LIVRABLES (miroirs plateforme) — 54 fichiers : PRÉSUMÉS CONFORMES — régime LIVRABLES

Échantillon revu 10/10 conforme ; liste complète dans le JSON qualifié.

- skills/TTS/tts.ts
- skills/agent-creator/references/agent-creator.agent
- skills/aminer-daily-paper/SKILL.md
- skills/autonomous-agent/references/autonomous-agent.agent
- skills/dessin-technique/scripts/capture_forme.py
- skills/dessin-technique/scripts/mesurer_filet.py
- skills/dessin-technique/scripts/mesurer_profondeur.py
- skills/dessin-technique/scripts/mise_a_echelle.py
- skills/docx/SKILL.md
- skills/docx/scripts/add_toc_placeholders.py
- … (+44 autres, cf. JSON)

### OUTIL DE SESSION HISTORIQUE (scripts racine) — 13 fichiers : VERDICT LEÇON — non référencés corpus/KB/socle

- scripts/create-pm-genplan-v3.11.0.py
- scripts/g1a-corrections-n55.py
- scripts/g1a-repair-dedup.py
- scripts/g1b-kb-n55.py
- scripts/g1c-genplan-shared-eco.py
- scripts/install-ecosystem-skills.py
- scripts/n60b-genplan-3170.py
- scripts/r1-evals-coverage.py
- scripts/r4-task-orchestrator.py
- scripts/r5-token-dashboard.py
- scripts/r7-agent-specialization.py
- scripts/r8-loop-guard.py
- scripts/repair-frontmatter-yaml.py

## Verdict final H1

- **1 non-conforme avéré corrigé** : install-ecosystem.py v2.0.0 → **v2.0.1** (garde idempotence append .gitignore, preuve sandbox rejeu ×3 byte-stable — le seul outil d'ÉTAT vivant défaillant du pipeline).
- **9 requalifiés conformes** (revue individuelle : déterminisme, dédup algorithmique, temporaires auto-nettoyés, fraîcheur écrasée en place).
- **84** classés par verdict catégoriel documenté (leçons one-shot / livrables présumés conformes sur échantillon).
- Outils VIVANTS du pipeline certifiés idempotents : eco_install_pipeline.py (EFFETS_GARDES, rejeu ×2 no-op prouvé en B4), scelleurs (gardes anti-perte), propagate-context (no-op rejeu ×2), arbitres, generer-pm (--check), task-eco-reinstall-sync0 (0 substitution au rejeu).
- Filet de reprise P2 (optionnel) : rejeu sandbox par lot des « PRÉSUMÉS CONFORMES » pour preuve formelle individuelle — l'analyseur persisté permet de rejouer l'audit à volonté.
