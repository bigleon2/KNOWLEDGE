# Modèle « blue-tech » — modèle par défaut de l'écosystème

**Version 1.0.0** · Statut : **défaut** (registre `templates/registry.json`) · Standard : blue-tech v1 · Format : A4 portrait · Langue : fr

## 1. Objet

`blue-tech` est le modèle de document technique de l'écosystème KNOWLEDGE. Il encapsule le **design** (et non le contenu) du PDF `progressive-disclosure-optimise.pdf` : palette « tech sombre », structure couverture → sommaire → parties → fin, typographie Inter/JetBrains Mono, catalogue de 16 composants, jeu de 10 validations mécaniques. Il sert de base aux futures automatisations, générations de documents et workflows de l'écosystème.

- **Source du design** : analyse du PDF livré en session web-f68de5ac (98 sélecteurs CSS, palette exhaustive, échelle typo mesurée, ordre structurel réel).
- **Source de vérité** : `blue-tech.template.json` (ce dossier). Le README ne duplique pas les valeurs — il documente l'usage.

## 2. Architecture du template (8 blocs)

| Bloc | Rôle |
|------|------|
| `meta` | identité du modèle (nom, version, standard, source, formats) |
| `page` | géométrie A4, fond, grille, glows, spécification du pied de page tamponné |
| `design_tokens` | palette (16 couleurs nommées + rôles), bordures, fonds transparents, radii |
| `typography` | 2 familles + échelle (14 tokens : couverture 62px/900 → code 12.5px mono) |
| `components` | catalogue 16 composants : purpose, fields (champs), css_contract |
| `sections` | ordre canonique + règles de rupture (cover → toc → parts → ending) |
| `fields` | variables de gabarit `{{...}}` (document, sommaire, contenu, fin) |
| `validations` | 10 règles V1-V10 avec sévérité S1/S2 et méthode mécanique |
| `generation` | pipeline 5 étapes + dépendances (pagedjs, PyMuPDF, pypdf, Chromium) |

## 3. Usage (génération d'un document)

1. Lire `blue-tech.template.json` (source de vérité unique — ne jamais coder les tokens en dur ailleurs).
2. Instancier les `fields` (`{{document_title}}`, `{{sections}}`, …) dans le squelette de `sections.order` en respectant le `css_contract` de chaque composant.
3. Suivre `generation.pipeline` : validate → rendu Paged.js (2 passes si sommaire paginé) → tampon pieds → arbitres.
4. Toute dérive de design est un FAIL (règle FAIL-CLOSE gen-plan §1.17) : correction immédiate avant fermeture d'étape.

## 4. Champs et sections

- **Document** : titre, sous-titre, kicker, résumé, tags, méta de pied de couverture, date, version.
- **Sections** : chaque partie = intercalaire (`part-divider`) + sections `N.N` (`chapter-header` + corps). Composants disponibles : body-text, inline-code, codeblock, callout, stat-card, checklist, diagram, table, lexicon, qa-bubble, steps.
- **Fin** : page `ending` (marque, titre, texte, stats) — sans pied de page.

## 5. Validations (garde qualité)

V1 palette exclusive (aucun fond clair) · V2 polices déclarées · V3 @page A4 · V4 ordre des sections · V5 sommaire 1 page cohérent · V6 pieds tamponnés · V7 code sécable · V8 contrastes · V9 équilibre `<div>` · V10 QA PDF PASS. Exécution : `python3 scripts/blue_tech/validate_doc.py --doc <html> --template <json>` + `pdf_qa.py`.

## 6. Enregistrement

Le registre `templates/registry.json` porte `default: blue-tech`. Pour changer de modèle par défaut : modifier `registry.json` (statut `default` → `disponible` pour l'ancien, `default` pour le nouveau) et journaliser au worklog (R4/R5 — jamais d'écrasement silencieux).

## 7. Pipeline de génération (dépendances)

`pagedjs` (rendu paginé — symlink node_modules requis) · `PyMuPDF` (extraction sommaire/pieds) · `pypdf` + `reportlab` (tampon) · Chromium headless via `skills/pdf/scripts/html2pdf-next.js`. Arbritres du skill pdf : `poster_validate.py`, `pdf_qa.py`.
