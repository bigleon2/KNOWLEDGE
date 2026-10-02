# PROMPT ULTRA MAÎTRE — Orchestration de l'écosystème personnel

> **Version** : 1.0.0 (généré)
> **Généré par** : `scripts/gen-ultra-maitre.py` (idempotent — ne pas éditer à la main ; éditer le script puis régénérer)
> **Date de génération** : 2026-10-02
> **Rôle** : point d'entrée UNIQUE d'orchestration à l'usage — route chaque demande vers le bon prompt maître / skill, sans dupliquer leur contenu (R4)
> **Directive** : propriétaire 2026-10-02 (« prompt ultra maître ») — design retenu : orchestrateur léger dérivé dynamiquement du corpus (KO-L003), PAS de conversion des PMs existants en monolithes (R4 duplication / R2 corpus figé / KO-L004 drift)

---

## §0 — Règle Zéro et invariants vitaux

- Écosystème Knowledge : `{{SKILLS_ROOT}}`=skills/ | `{{KB_PATH}}`=skills/KNOWLEDGE.md | `{{KB_ENABLED}}`=true | `{{PROFILE_DEFAULT}}`=NORMAL
- **Règle Zéro (SHARED §0)** : skills auto-contenus, versionnés semver, registre KB source de vérité, cross-references bidirectionnelles.
- **Idempotence (R1-R6)** : vérifier présence avant insertion ; ne jamais rétrograder ; fusionner les frontmatters ; ne jamais dupliquer ; journaliser ; auto-adaptation sans duplication.
- **Arbitres dynamisés (KO-L003)** : tout invariant dérive de l'état courant — jamais d'état figé ; re-verdict honnête après correction.
- **Recalibrage croisé (KO-L004)** : toute montée de version recalibre arbitres, archive et CET orchestrateur (régénération = recalibrage).

## §1 — Routage demande → prompt maître / skill (table T1)

| Demande | Skill mobilisé | Prompt maître | Cadre |
|---------|----------------|---------------|-------|
| Planifier une tâche / un projet | gen-plan (dernière version) | PM gen-plan le plus récent | E1-E15, 4 modes |
| Vérifier / corriger un travail | correct-work v2.7.0 (gen-plan OBLIGATOIRE à l'Étape 1) | PM correct-work le plus récent | 5 étapes, 4 modes |
| Archiver une session / clone | clone-chat | PM clone-chat le plus récent | 7+1 étapes, 8 checks |
| Installer / réinstaller l'écosystème | PROMPT-MAITRE-INSTALL-ECOSYSTEME.md — SOURCE UNIQUE | ce fichier (§A + pipeline 10 étapes) | corpus -> registre -> arbitres |
| Synchroniser contexte / canaux | SYNC-CONTEXT.md + scripts de sync | — | 2 voies byte-identiques |
| Auditer la provenance | audit-provenance | — | L006, avant clone/install |
| Observer les leçons | knowledge-observer | — | journal lessons-learned, M1-M2 à E15 |

## §2 — Registre dynamique des prompts maîtres (dérivé du corpus réel)

État réel de `skills/@mon-ecosysteme/` : **25 fichiers canoniques + cet orchestrateur** (invariant `CORPUS_ATTENDU` du checker).

| Famille | PM le plus récent (source d'assemblage) | Versions historiques figées (R2) |
|---------|------------------------------------------|----------------------------------|
| GEN-PLAN | PROMPT-MAITRE-GEN-PLAN-v3.18.0.md (la plus récente) | 3.6.1, 3.7.0, 3.8.0, 3.8.1, 3.9.0, 3.10.0, 3.11.0, 3.12.0, 3.13.0, 3.16.0, 3.17.0, 3.17.1, 3.17.2 |
| CORRECT-WORK | PROMPT-MAITRE-CORRECT-WORK-v2.7.0.md (la plus récente) | 2.4.0, 2.5.0, 2.5.1, 2.6.0 |
| CLONE-CHAT | PROMPT-MAITRE-CLONE-CHAT-v2.0.0.md (la plus récente) | — |

Socle : `PROMPT-MAITRE-SHARED.md` v1.6.4 (lire en premier). Installateur : `PROMPT-MAITRE-INSTALL-ECOSYSTEME.md` v1.3.1 — **source d'installation UNIQUE** (fusion v1.1.0 : `INSTALL-ECOSYSTEME.md` supprimé, miroir `skills/_prompts-maitres/` supprimé, décision d'architecture v2.0 exécutée).

## §3 — Skills écosystème installés (versions réelles, frontmatter = source de vérité)

| Skill | Version |
|-------|---------|
| `gen-plan` | 3.18.0 |
| `correct-work` | 2.7.0 |
| `clone-chat` | 2.0.0 |
| `skills-inventory` | 1.0.0 |
| `skill-creator` | 1.0.0 |
| `agent-creator` | 2.0.0 |
| `script-creator` | 1.0.0 |
| `script-reviewer` | 1.0.0 |
| `audit-provenance` | 1.0.0 |
| `prompt-engineering` | 2.1.0 |
| `context-engineering` | 1.1.0 |
| `loop-engineering` | 1.0.1 |
| `graph-engineering` | 1.0.1 |
| `harness-engineering` | 1.0.1 |
| `knowledge-observer` | 1.0.0 |
| `script-mon-ecosysteme-infrastructure` | 1.1.0 |
| `audio-metadata` | 1.0.0 |
| `cpp-analysis` | 1.0.0 |
| `pdf-llm` | 1.0.0 |
| `resource-monitor` | 1.0.0 |
| `version-management` | 1.0.0 |
| `autonomous-agent` | 1.0.0 |
| `correct-py` | 1.0.0 |
| `fleet-engineering` | 1.0.0 |
| `memory-engineering` | 1.0.0 |
| `spec-driven-development` | 1.0.0 |

Registre KB : 26 entrées versionnées (`skills/KNOWLEDGE.md`). correct-work v2.7.0 exige gen-plan (dernière version installée) à son Étape 1 — couplage obligatoire.

## §4 — Points d'entrée et ordre de lecture

1. **Socle** : `PROMPT-MAITRE-SHARED.md` (v1.6.4) — toujours en premier.
2. **Installation** : `PROMPT-MAITRE-INSTALL-ECOSYSTEME.md` (v1.3.1) — périmètre §A + pipeline 10 étapes + critères §3.
3. **Planification** : PM gen-plan le plus récent — §A DÉCLENCHEURS (dont verbatim « intègre dans le plan d'actions » → E13).
4. **Vérification** : PM correct-work le plus récent + `skills/correct-work/scripts/verify-correct-work.py` (16 checks).
5. **Publication** : archive `download/mon-ecosysteme_archive.zip` (round-trip v2.2) — unique voie de diffusion du corpus (décision v2.2 : canal de fichiers download/ supprimé, garde `scripts/task14-scan-doublons.py`).

## §5 — Interactions clés (extrait graphe KB)

| Arête | Nature |
|-------|--------|
| gen-plan —invoque→ correct-work | E1 + hook E8 + contrôle par phase E9-E14 |
| correct-work —utilise→ gen-plan | Étape 1 OBLIGATOIRE (dernière version) |
| gen-plan —délègue→ prompt-engineering | optimisation fine des prompts (SHARED §3.1) |
| clone-chat —enrichit→ KNOWLEDGE.md | descriptions §2 |
| knowledge-observer —valide→ gen-plan | leçons §1.14/§1.15 (M1-M2 à E15) |
| install-ecosysteme —précondition→ audit-provenance | audit avant installation (L006) |

## §6 — Maintenance

- Toute évolution du corpus/skills : `python3 scripts/gen-ultra-maitre.py` PUIS recalibrage KO-L004 (checker, archive, garde anti-doublons) — la régénération de ce fichier fait partie du recalibrage.
- Ce fichier NE remplace AUCUN prompt maître : il ROUTE. Il ne détient ni méthode ni spécification (fonction héritée SHARED §7).
- Recréer un second installateur ou un second orchestrateur est interdit (R4).
