---
name: add-template-pdf
version: 1.0.1
category: ecosystem
language: fr
tags:
  - pdf
  - template
  - registre
  - generation
  - ecosysteme
description: >
  Ajoute des templates PDF aux skills PDF de l'écosystème. Déclencheur verbatim
  propriétaire : « add-template-pdf (<nom du template>) » — l'argument <nom du
  template> (kebab-case) désigne le modèle à créer puis installer. Routage des
  cibles (choix propriétaire délégué, justifié §2) : les templates sont installés
  au skill `pdf` (seul générateur PDF de l'écosystème — 4 lignes de production
  Report/Creative/Academic/Process) et inscrits au registre écosystème
  `templates/registry.json` (source de vérité des modèles, `default: blue-tech`).
  Exclusions justifiées : `pdf-llm` (extraction — aucun gabarit de mise en page),
  `mise-en-page` (couche DA décisionnelle — consomme les templates, n'en stocke
  pas), `pptx`/`docx`/`charts` (hors PDF). Mécanique idempotente : re-exécution
  = NO-OP prouvé ; gardes anti-nom-invalide et anti-doublon ; le modèle
  « default » du registre n'est jamais réassigné sans l'option explicite
  `--default`. Exécutant canonique : `scripts/add_template_pdf.py`
  (--name <nom> [--palette slate] [--dry-run] [--json] [--selftest]).
dependencies:
  - skill: pdf
    version: ">=1.0.0"
---

## §0 — Contexte Système (SHARED v1.7.46)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.
> Langue : FRANÇAIS exclusif pour tous les échanges avec le propriétaire (règle d'or n°6 gen-plan — directive 2026-10-31, renforcée 2026-11-06) : dès le PREMIER mot de toute session ou reprise, la langue d'un message, d'un résumé de continuation ou d'un canal ne dérive JAMAIS la réponse ; toute dérive est corrigée immédiatement.
> Règles d'or & lecture SHARED à l'exécution (directive propriétaire 2026-11-06 — SHARED §9) : tout skill/agent/script exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or de l'écosystème (résumé §9 — canonique gen-plan §1.5).
> Référence canonique skill/agent (directive propriétaire 2026-11-07 — SHARED §0/§1.2) : toute référence à « mon skill X »/« mon agent X » désigne la forme installée à la racine `skills/X/SKILL.md`, JAMAIS le prompt maître du corpus `@mon-ecosysteme/` (ex-nommé `@PM-SKILLS/`) — les PMs sont des spécifications générées mécaniquement (KO-L004), les skills installés sont les formes exécutables.

# add-template-pdf — ajout de templates PDF aux skills PDF

## §1 — Objet et déclencheurs

Ce skill matérialise la demande du propriétaire : **« génère un skill "add-template-pdf" qui ajoutera des template PDF à mes skills PDF lorsque j'écrirai "add-template-pdf (<nom du template>)" »** (trace 1a218db7095e21f9, 2026-11-26).

Déclencheurs verbatim (déclenchement automatique) :
- `add-template-pdf (<nom du template>)` — forme canonique avec argument ;
- `add-template-pdf <nom du template>` — parenthèses optionnelles ;
- « ajoute le template PDF <nom> » / « ajoute un template PDF nommé <nom> ».

L'argument `<nom du template>` est un identifiant **kebab-case** (`^[a-z][a-z0-9-]{2,30}$`) : il désigne le modèle à créer (squelette standard) ou réinstaller s'il existe déjà au registre (ex. `blue-tech`).

## §2 — Routage des cibles (choix justifié)

| Cible | Rôle | Décision |
|-------|------|----------|
| `skills/pdf/` | SEUL skill de génération PDF (Report/Creative/Academic/Process) | **Installation** : `skills/pdf/templates/<nom>/` |
| `templates/registry.json` (écosystème) | Source de vérité des modèles — `default` sert de gabarit par défaut aux générations | **Inscription** : entrée `status: "standard"` |
| `pdf-llm` | Extraction/OCR — aucun gabarit de mise en page | Exclu |
| `mise-en-page` | Couche DA décisionnelle transverse — consomme les templates | Exclu |
| `pptx`, `docx`, `charts` | Formats non-PDF | Exclus |

Le modèle `default` du registre est **jamais** réassigné sans l'option explicite `--default` (garde anti-écrasement — le défaut courant est `blue-tech`, Task 79).

## §3 — Protocole d'ajout en 6 temps (exécutant canonique `scripts/add_template_pdf.py`)

1. **Créer** le squelette du template : `<nom>/<nom>.template.json` (structure standard **9 blocs** conforme au format `blue-tech` : `meta`, `page`, `design_tokens`, `typography`, `components`, `sections`, `fields`, `validations`, `generation`) + `README.md` documentaire. Palette paramétrable (`--palette slate` par défaut — A4 portrait sombre ; ou `--palette-json <fichier>`).
2. **Installer** au skill pdf : copie byte-identique vers `skills/pdf/templates/<nom>/` (profil ET dépôt — parité hôte↔dépôt).
3. **Inscrire** au registre `templates/registry.json` (dépôt — source de vérité) : entrée horodatée (name, version 1.0.0, status `standard`, path, documentation, page_format, created, validations, components). Idempotent : entrée déjà présente et identique → NO-OP.
4. **Valider** : contrôles mécaniques intégrés (JSON parseable 9/9 blocs, semver, nom conforme, registre re-parsé cohérent, `default` inchangé, parité SHA dépôt↔profil).
5. **Documenter** : README du template (objet, palette, composants, validations, usage).
6. **Consigner** : worklog de session (template ajouté, registre mis à jour) + KB si première installation du skill.

Gardes : nom invalide → refus rc=2 avec diagnostic ; doublon divergent sans `--force` → refus rc=1 ; `--dry-run` = rapport complet sans aucune écriture ; `--json` = rapport machine.

## §4 — Structure standard du template (9 blocs)

`meta` (identité) · `page` (A4 210×297 mm, fond, marges) · `design_tokens` (palette nommée + rôles) · `typography` (2 familles + échelle) · `components` (catalogue : purpose, fields, css_contract) · `sections` (ordre canonique cover → toc → parts → ending) · `fields` (variables `{{...}}`) · `validations` (règles V1-Vn, sévérité, méthode) · `generation` (pipeline 5 étapes : validate → rendu → tampon → arbitres → inspection).

Palette par défaut `slate` (A4 sombre cohérente avec le standard de l'écosystème) : fond `#111827`, surface `#1f2937`, accent `#38bdf8`, accent secondaire `#a5b4fc`, texte `#f8fafc`, muted `#94a3b8` — polices Inter (300-900) + JetBrains Mono.

## §5 — Relations

| Avec | Nature |
|------|--------|
| `pdf` | Cible d'installation (templates consommés par les 4 lignes de production) |
| `templates/registry.json` | Registre écosystème inscrit (source de vérité Task 79) |
| `blue-tech` | Standard de format des templates (9 blocs) — réinstallable par ce skill |
| `mise-en-page` | Consommatrice DA des templates installés (pas de stockage) |
| `skill-creator` | Conventions de génération du skill lui-même |

## §A — Usage mécanique

```bash
python3 skills/add-template-pdf/scripts/add_template_pdf.py --name slate           # création + installation + inscription
python3 skills/add-template-pdf/scripts/add_template_pdf.py --name slate           # re-exécution = NO-OP (idempotent)
python3 skills/add-template-pdf/scripts/add_template_pdf.py --name blue-tech       # réinstallation depuis le registre
python3 skills/add-template-pdf/scripts/add_template_pdf.py --name demo --dry-run  # rapport sans écriture
python3 skills/add-template-pdf/scripts/add_template_pdf.py --selftest             # tests internes
```
