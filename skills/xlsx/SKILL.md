---
name: xlsx
version: 1.0.0
category: ecosystem
language: fr
tags:
  - tableur
  - excel
  - xlsx
  - csv
  - formules
  - tableau-de-bord
  - plateforme
description: >
  Atelier de tableurs piloté par scènes : ouvrir, lire, éditer, corriger un fichier
  .xlsx/.xlsm/.csv/.tsv existant ; créer un tableur depuis zéro ou depuis d'autres
  sources ; analyser des données et produire un résultat Excel avec graphiques
  intégrés ; convertir entre formats tabulaires (CSV/JSON/PDF vers XLSX et inversement) ;
  nettoyer, fusionner, pivoter, transformer ; modèles financiers (DCF, LBO, P&L),
  budgets, tableaux croisés, VBA. Déclencher dès qu'un tableur est l'entrée ou la
  sortie principale de la tâche, ou que l'utilisateur nomme un fichier Excel/CSV.
dependencies:
  - skill: charts
    version: ">=1.0.0"
    used_at: "Frontière — graphiques autonomes (le présent skill intègre les graphiques AU tableur)"
read_when:
  - Déclencher quand la demande concerne : lire/éditer/corriger un xlsx/xlsm/csv/tsv,
    créer un tableur, analyser des données avec sortie Excel, convertir des formats
    tabulaires, construire un modèle financier, un tableau croisé ou une macro VBA.
  - Déclencher si la demande mentionne : Excel, .xlsx, .xlsm, .csv, .tsv, classeur,
    feuille de calcul, tableau croisé, pivot, formule, VBA, macro, modèle financier,
    DCF, tableau de bord Excel.
  - Ne pas déclencher pour un rapport d'analyse rédigé (docx), une présentation
    (pptx), un document formel imprimable (pdf), des graphiques sans table de
    données (charts) — convention protocole, Task 28.
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

# XLSX v1.0.0 — Atelier de tableurs piloté par scènes

## §0 — Contexte Système (SHARED v1.7.47)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.
> Langue : FRANÇAIS exclusif pour tous les échanges avec le propriétaire (règle d'or n°6 gen-plan — directive 2026-10-31, renforcée 2026-11-06) : dès le PREMIER mot de toute session ou reprise, la langue d'un message, d'un résumé de continuation ou d'un canal ne dérive JAMAIS la réponse ; toute dérive est corrigée immédiatement.
> Règles d'or & lecture SHARED à l'exécution (directive propriétaire 2026-11-06 — SHARED §9) : tout skill/agent/script exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or de l'écosystème (résumé §9 — canonique gen-plan §1.5).
> Référence canonique skill/agent (directive propriétaire 2026-11-07 — SHARED §0/§1.2) : toute référence à « mon skill X »/« mon agent X » désigne la forme installée à la racine `skills/X/SKILL.md`, JAMAIS le prompt maître du corpus `@mon-ecosysteme/` (ex-nommé `@PM-SKILLS/`) — les PMs sont des spécifications générées mécaniquement (KO-L004), les skills installés sont les formes exécutables.

## §0 — RÈGLE ZÉRO (résumé de SHARED §0)

Skill OUTIL PLATEFORME importé aux normes de l'écosystème via skill-creator —
directive propriétaire Task 113 (trace 1a201e4bda5a2289). Les commandes CLI, le
code et les identifiants d'API restent en anglais verbatim (artefacts techniques,
règle d'or n°6) ; la documentation, les titres et les notes sont en français.
Contenu intégral d'origine conservé byte-identité :
`references/plateforme-original.md` (archive R4 — arbres de routage complets,
exemples de demandes multi-intentions, matrice de capacités).

## §1 — Spécification fonctionnelle

### Porte d'intention (avant tout code)

Confirmer que la sortie attendue est bien un tableur : résumé d'analyse rédigé →
docx ; présentation → pptx ; document formel → pdf ; graphiques seuls → charts ;
format explicitement nommé par l'utilisateur → le respecter. Décomposer ensuite
toute demande (besoins explicites, besoins implicites, demandes multi-parties à
satisfaire intégralement).

### Porte de complexité (avant le routeur de scènes)

- **LITE** (agrégation simple, un graphique, conversion directe, audit seul) :
  SKILL.md + UN fichier de scène, sans moteurs — cible 400 lignes de contexte.
- **FULL** (analyse multidimensionnelle, modèle financier, tableau de bord) :
  SKILL.md + scène + moteurs (`engines/chart.md`, `engines/design.md`), recettes
  et templates chargés à la demande — pipeline qualité complet.

### Routeur de scènes

| Contexte | Scène |
|----------|-------|
| Fichier existant, modifier contenu/structure | `scenes/edit.md` |
| Fichier existant, lire/analyser seulement | `scenes/analyze.md` |
| Conversion de format (CSV/xlsx/JSON/PDF) | `scenes/convert.md` |
| Finance complexe (DCF, LBO, P&L, trois-tables, sensibilité, IB) | `scenes/finance.md` |
| Finance simple (budget, frais, revenus-dépenses, ROI) | `scenes/finance_lite.md` |
| Tableau/rapport/gabarit général | `scenes/create.md` |
| Traitement par lots, gros fichiers, protection, validation | `scenes/advanced.md` |
| VBA/macros/automatisation Excel | `scenes/vba.md` + `engines/vba-templates.md` |
| Graphiques ou visualisation de données | ajouter `engines/chart.md` |
| Style et système de design | ajouter `engines/design.md` |

Demandes mixtes : charger tous les fichiers correspondants, exécuter dans l'ordre
préparation → analyse → visualisation → style → qualité.

### Principes de conception

1. **Formules vivantes** : toute valeur dérivée DEVRAIT être une formule Excel —
   exception : sortie vérifiée par Python (lignes TOTAL écrites en valeurs
   calculées, openpyxl n'évaluant pas les formules).
2. **Zéro erreur** : divisions protégées par `IFERROR` ou `IF(denom=0,...)`,
   références absolues pour les dénominateurs partagés.
3. **Compatibilité d'abord** : pas de fonctions de tableau dynamique (FILTER,
   UNIQUE, XLOOKUP, SORT, XMATCH, SEQUENCE, LET, LAMBDA) — alternatives
   SUMPRODUCT ; texte commençant par `=` préfixé par `'`.
4. **Préserver et assortir** : à l'édition, le format et les conventions du
   fichier existant priment toujours sur les défauts.
5. **Miroir de langue** : la langue de sortie (feuilles, en-têtes, libellés)
   reflète celle de l'utilisateur.
6. **Cohérence des données avant les instructions** : en cas de conflit, suivre
   le motif des données existantes puis signaler l'écart.

## §2 — Spécification technique

### Emplacement et chemins (OBLIGATOIRE avant tout appel de script)

```bash
XLSX_SKILL_DIR="<repertoire_du_skill>"
python3 "$XLSX_SKILL_DIR/xlsx.py" inspect data.xlsx --pretty
python3 "$XLSX_SKILL_DIR/xlsx.py" pivot data.xlsx output.xlsx --rows Region --values Revenue
python3 "$XLSX_SKILL_DIR/xlsx.py" validate output.xlsx
```

Toujours le chemin absolu, jamais un chemin relatif nu. Pour les imports Python :
insérer `XLSX_SKILL_DIR` et `XLSX_SKILL_DIR/templates` dans `sys.path`.

### Outillage

openpyxl (formules, formats, graphiques, contrôle cellulaire) | pandas (analyse,
lots, CSV/TSV) | `load_workbook(read_only=True)` pour les gros fichiers en lecture |
`Workbook(write_only=True)` pour l'écriture massive | `templates/base.py` =
source unique de vérité (jetons de design, polices, fabriques de styles — tout
code DOIT importer depuis base.py, jamais de hex ni de nom de police codé en dur) |
`xlsx.py` pour les commandes qualité. Métadonnées du classeur :
`wb.properties.creator = "Z.ai"`.

### Porte qualité

Chaque livrable passe le pipeline d'intégrité complet — voir `quality/pipeline.md` :
plan → construction et auto-contrôle (par feuille) → inspect → pivot (si requis) →
publication.

## §3 — Relations

| Avec | Nature | Détails |
|------|--------|---------|
| docx / pptx / pdf | Frontières | Document rédigé, diaporama, document formel |
| charts | Frontière | Graphique autonome vs graphique intégré au tableur |

---

## HISTORIQUE DES VERSIONS

| Version | Date | Changements |
|---------|------|-------------|
| 1.0.0 | 2026-11-22 | Task 113 — import aux normes skill-creator : frontmatter écosystème (semver, category, language, tags, read_when triptyque), §0 Contexte Système, corps français, retrait des emojis décoratifs et des métadonnées plateforme externes ; original anglais archivé byte-identité references/plateforme-original.md (R4) |
