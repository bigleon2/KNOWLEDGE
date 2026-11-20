# Historique par skill — rea-analysis

> **Version** : 1.0.0 — **Date** : 2026-11-21 (Task ID 12, session web-93a4f011)
> **Version vivante** : v1.0.0 — `skills/rea-analysis/SKILL.md` (première version du skill)
> **Versions archivées** : aucune (création)

## Famille rea-analysis — 1 version (skill : rea-analysis)

**Particularité durable du skill** : analyse rétro-ingénierie d'artefacts SANS code source par le kit REA (fork bigleon2/REA_Reverse_All_Thing_Kit, miroir-épingle de morluto/rea v6.8.0 — CLI ~180 commandes + serveur MCP, moteurs Ghidra/Hopper/IDA/JADX/Kuna/Frida) — intégré selon le pattern ghorg-cmdr Task 51 (skill + script d'installation idempotent + KB + certification) ; périmètre strict : ANALYSE a posteriori (audit, inspection, Evidence), la reproduction d'applications restant la voie git clone + build (verdict Task 8).

| Version | Date | Améliorations implantées (source : §6 du skill vivant) | Avantage par rapport à la version précédente |
|---|---|---|---|
| v1.0.0 | 2026-11-21 | Task ID 12 (session web-93a4f011 — directive 1a1fa816474a35ad volet « intègre $FACON REA à mon écosystème (choisis comment : fais le meilleur choix entre skill, agent ou agent autonome) », exécuté sous la trace 1a1faad3d26c524d) : **CRÉATION — intégration $FACON par pattern ghorg-cmdr Task 51** — choix JUSTIFIÉ (matrice correct-work §6 : un CLI déterministe ~180 commandes n'exige ni boucle d'agent ni mémoire persistante → SKILL, forme installée règle d'or n°8 ; disciplines mobilisées spec-driven-development/harness-engineering/memory-engineering) ; livrés : SKILL.md (§A déclencheurs + §0 SHARED v1.7.43 + §1-§6) + scripts/rea-install.py (stdlib, idempotent ×2 — clone anonyme si absent / npm ci si node_modules absent / build:cached si dist absent / sonde CLI, rc 0/1/2, --pin épingle datée) + references/referentiel-kit-rea.md (identité, surface, moteurs, bornes D7, verdicts $FACON2 Task 8/9, protocole GO+KO-L009) + evals/trigger_evals.json (5 positifs + 3 vetos croisés) ; kit ré-acquis à l'installation : épingle 03a3fcbce (clone anonyme 18 s, npm ci 15 s, build 15 s — doctor ghidra healthy ×7, moteurs natifs absents documentés, divergence amont 0/2317 re-mesurée) ; cascade $FACON2 : KB + @historique + pin ECO_SKILLS + certification locale | **VERSION VIVANTE (première)** — le kit d'analyse rétro-ingénierie devient un citoyen de l'écosystème : installation idempotente, campagne bornée, état vérifiable au disque, orthogonalité ghorg-cmdr documentée |
