---
name: pdf
version: 1.0.0
category: ecosystem
language: fr
tags:
  - pdf
  - reportlab
  - latex
  - playwright
  - affiches
  - academique
  - plateforme
description: >
  Atelier professionnel PDF à quatre lignes de production : (1) Report — documents
  structurés via ReportLab (rapports, propositions, contrats, livres blancs) ;
  (2) Creative — design visuel via blueprint JSON puis design_engine.py et capture
  Playwright (affiches, infographies, invitations, tableaux de bord) ; (3) Academic
  — travaux savants via LaTeX/Tectonic (articles, thèses, documents à fort contenu
  mathématique) ; (4) Process — manipulation de PDF existants (extraire, fusionner,
  découper, remplir des formulaires, convertir). Routage automatique selon le type
  de document, avec sous-chemins CV ATS/créatif/académique. Déclencher dès qu'un
  PDF est l'entrée ou la sortie de la tâche.
dependencies:
  - skill: charts
    version: ">=1.0.0"
    used_at: "Diagrammes intégrés aux documents (Playwright+CSS vers PNG pour Report)"
read_when:
  - Déclencher quand la demande concerne : produire un PDF (rapport, affiche,
    article académique, CV), reprendre la mise en forme d'un PDF existant, ou
    manipuler un PDF (extraction, fusion, découpe, formulaires, conversion).
  - Déclencher si la demande mentionne : PDF, .pdf, ReportLab, LaTeX, Tectonic,
    affiche, infographie, livre blanc, formulaire PDF à remplir, fusionner/découper
    des PDF, convertir en PDF.
  - Ne pas déclencher pour les documents Word (docx), diaporamas (pptx), tableurs
    (xlsx) ni les graphiques autonomes (charts) — convention protocole, Task 28.
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

# PDF v1.0.0 — Atelier de production documentaire

## §0 — Contexte Système (SHARED v1.7.45)

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
`references/plateforme-original.md` (archive R4 — matrice de routage exhaustive,
mots-clés de détection par brief, règles détaillées).

## §1 — Spécification fonctionnelle

### Tri du poids de la tâche

- **Léger** (conversion de format, remplissage de formulaire, extraction de texte,
  fusion/découpe, certificat simple) : SKILL.md + `briefs/process.md` seul.
- **Standard** (rapport multi-pages, affiche, article académique, CV, reformatage —
  tout document avec décisions de design) : SKILL.md + `configs/fonts.md` + brief
  correspondant + TOUS les fichiers référencés par le brief.

### Contrôles pré-routage (AVANT l'appariement du brief)

1. **Détection d'emoji** : contenu utilisateur contenant des emoji décoratifs →
   forcer la ligne Creative (ReportLab rend les emoji en carrés, LaTeX les perd).
2. **Couverture CJK** : contenu chinois/japonais/coréen → sonder d'abord les
   polices disponibles (`ls /usr/share/fonts/truetype/chinese/` sous Linux) et
   enregistrer en conséquence ; Creative charge Noto Sans SC avec
   `font-display: swap` ; Academic utilise `ctex`.
3. **Taille non standard** (hors A4/Letter/A3) → préférer Creative (Playwright
   gère toute dimension).
4. **Sécurité des caractères** : avant toute écriture, traquer kana japonais et
   symboles rares susceptibles de corrompre l'encodage — remplacer par les
   équivalents chinois simples ; si le japonais doit être préservé, se limiter
   aux blocs CJK standard.

### Routage par brief

| Intention | Brief |
|-----------|-------|
| PDF existant : extraire/fusionner/découper/remplir/convertir/reformater | `briefs/process.md` |
| Rapport, proposition, livre blanc, contrat, analyse | `briefs/report.md` (ReportLab) |
| Affiche, invitation, infographie, tableau de bord, mise en page créative | `briefs/creative-fixed-canvas.md` (Playwright, canvas fixe) |
| Guide, manuel, catalogue, collection (texte dense + design) | `briefs/creative-flow.md` (Playwright, contenu fluide) |
| Article, thèse, mathématiques lourdes, IEEE/ACM, Beamer | `briefs/academic.md` (Tectonic) |
| CV ATS/entreprise | `briefs/resume.md` |
| CV créatif / académique | `briefs/creative-fixed-canvas.md` / `briefs/academic.md` (sous-sections) |
| Affiche (couche scène supplémentaire) | `briefs/poster.md` en sus du brief Creative canvas fixe |

Diagrammes complexes intégrés : selon le brief cible — Report → Playwright+CSS
vers PNG puis `Image()` ReportLab ; Creative → directement en HTML/CSS ; Academic
→ TikZ natif si simple (6 nœuds ou moins), sinon Playwright+CSS vers PNG puis
`\includegraphics`. Mots-clés de détection complets dans l'archive R4.

## §2 — Spécification technique

### Emplacement et chemins (OBLIGATOIRE avant tout appel de script)

```bash
PDF_SKILL_DIR="<repertoire_du_skill>"
# Scripts : $PDF_SKILL_DIR/scripts — imports Python : l'insérer dans sys.path
```

### Ligne Creative — principe directeur artistique

L'agent produit UNIQUEMENT des blueprints spatiaux JSON ; `convert.blueprint`
compile vers un PDF au pixel près (design_engine.py puis capture Playwright) —
jamais de HTML écrit à la main pour cette ligne.

### Arborescence

`briefs/` (workflows par ligne) | `configs/` (dont fonts.md) | `env_setup/` |
`references/` | `scripts/` | `typesetting/` | `templates/` (le cas échéant) —
détail par brief dans chacun d'eux.

## §3 — Relations

| Avec | Nature | Détails |
|------|--------|---------|
| docx / pptx / xlsx | Frontières | Word, diaporamas, tableurs |
| charts | Amont | Diagrammes intégrés au document |
| image-search | Amont | Illustrations par URLs OSS stables |

---

## HISTORIQUE DES VERSIONS

| Version | Date | Changements |
|---------|------|-------------|
| 1.0.0 | 2026-11-22 | Task 113 — import aux normes skill-creator : frontmatter écosystème (semver, category, language, tags, read_when triptyque), §0 Contexte Système, corps français, retrait des emojis décoratifs et des métadonnées plateforme externes ; original anglais archivé byte-identité references/plateforme-original.md (R4) |
