---
name: resume-builder
version: "1.0.0"
category: "Carrière & Emploi"
tags:
  - resume
  - builder
description: Génère à partir de zéro ou optimise en profondeur un CV, puis l'exporte en plusieurs formats (docx / pdf / markdown). Réécrit les expériences avec la méthode STAR, vérifie la couverture en mots-clés ATS, choisit le template selon le secteur (internet produit / tech / finance / général). Déclenchez ce skill dès que l'utilisateur dit « aide-moi à rédiger un CV / optimiser mon CV / je ne sais pas écrire un CV / mon CV est trop faible / mon CV manque de professionnalisme / corrige mon CV / fais-moi un template de CV / exporte mon CV / ajoute des mots-clés à mon CV », ou qu'il téléverse un CV .pdf/.docx en demandant « vois comment l'améliorer ». Même si l'utilisateur se contente de demander « quels sont les défauts de mon CV », déclenchez-le.
language: fr

read_when:
  - Déclencher quand la demande concerne : génère à partir de zéro ou optimise en profondeur un CV, puis l'exporte en plusieurs formats (docx / pdf / mar…
  - Déclencher si la demande mentionne : exporte, docx, mots
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

## §0 — Contexte Système (SHARED v1.6.8)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# Resume Builder (génération et optimisation de CV)

Ce skill fait trois choses :

1. **Génération structurée** : produit à partir des expériences de l'utilisateur un CV conforme aux standards du marché de l'emploi
2. **Réécriture STAR** : transforme des phrases faibles du type « j'ai participé à X » en « via X, réalisé Y, avec le résultat Z »
3. **Optimisation des mots-clés ATS + export multi-templates** : garantit que le CV passe les filtres automatiques, avec export docx/pdf/md

Ne fait pas : la réécriture orientée fiche de poste (c'est l'affaire de jd-resume-tailor ; faites-y les demandes « adapter le CV à telle fiche de poste »)

---

## Quand se déclenche

- « aide-moi à rédiger un CV »
- « mon CV est trop faible / sans points forts / manque de professionnalisme »
- « réécris cette expérience avec la méthode STAR »
- « est-ce qu'il y a assez de mots-clés dans mon CV »
- « exporter le CV en PDF / docx »
- L'utilisateur téléverse un CV sans préciser « adapter à une fiche de poste » → déclenchez ce skill ; s'il dit « adapter pour l'entreprise X / le poste X » → appelez jd-resume-tailor

---

## Workflow

### Étape 1 : établir l'état actuel du CV

Si l'utilisateur **a un fichier de CV** (.pdf / .docx / .md / .txt) :
- le pdf est parsé via le skill pdf
- le docx est parsé via le skill docx
- extrayez : informations de base, formation, expérience professionnelle, projets, compétences, divers

Si l'utilisateur **n'a pas de CV** :
- collectez les informations avec AskUserQuestion (voir la liste de questions dans `references/intake_questions.md`)
- posez 3 à 4 questions à la fois, collectez en plusieurs rounds pour ne pas décourager

### Étape 2 : choisir le template

Lisez `references/templates/` pour décider de la structure :

- Internet produit / opérations / PM → `templates/internet.md`
- Tech / développement / data → `templates/tech.md`
- Finance / conseil / commerce → `templates/finance.md`
- Général / tous secteurs → `templates/general.md`

Si l'utilisateur n'a pas précisé d'orientation, utilisez le template général, mais **posez la question** : « Vers quel type de poste comptes-tu candidater ensuite ? Je peux utiliser une mise en page mieux adaptée à cette direction. »

### Étape 3 : réécrire chaque expérience avec STAR

Lisez `references/star_rewrite_guide.md` et appliquez la réécriture STAR à chaque expérience professionnelle / de projet.

**STAR n'est pas une structure rigide en quatre paragraphes**, c'est l'assurance que chaque puce contient :
- **un signal de contexte** (une phrase sur l'ampleur du problème ou de la situation)
- **une action** (ce que tu as concrètement fait, avec des verbes)
- **un résultat** (chiffres / pourcentages / classement / échelle)

Si les informations fournies par l'utilisateur **ne contiennent aucun chiffre**, relancez activement : « quelle est environ la taille de la base d'utilisateurs de ce projet ? », « cette optimisation a apporté à peu près combien ? Une estimation d'ordre de grandeur suffit si tu ne te rappelles plus. »

### Étape 4 : vérification des mots-clés ATS

Appelez le script :

```bash
python scripts/ats_check.py --resume <resume.md> \
    --industry internet \
    [--jd <jd.txt>]
```

Le script va :
1. extraire les mots-clés du CV
2. les comparer à la base de mots-clés sectorielle (provenant de job-intent-tracker ou du `references/keywords/` de ce skill)
3. sortir deux listes : « déjà couvert / suggéré en complément »
4. attribuer un score de compatibilité ATS (unicité de la police, usage de tableaux, symboles spéciaux, images, etc.)

**Règles strictes de compatibilité ATS** :
- ne mettez pas les expériences dans un tableau Word (beaucoup d'ATS ne savent pas les parser)
- ne placez pas les dates dans une image décorative
- pas de mise en page à deux colonnes (certains ATS lisent par colonne et mélangent l'ordre)
- pas d'icônes / emojis dans les titres
- police au choix parmi SimSun / Source Han Serif / Arial / Helvetica

### Étape 5 : export multi-formats

Lisez `references/export_guide.md` et choisissez selon le besoin de l'utilisateur :

**Export docx** (le plus universel ; les recruteurs le demandent en priorité) :
- appelez le skill docx
- utilisez `assets/resume_template.docx` comme template (si présent)

**Export pdf** (version finale d'envoi) :
- flux recommandé : d'abord docx → puis conversion pdf via word/libreoffice
- la génération directe en pdf via reportlab donne un rendu médiocre, non recommandé
- appelez le skill pdf pour le post-traitement (chiffrement / nettoyage des métadonnées)

**Export markdown** (sauvegarde + GitHub) :
- écrivez simplement le fichier .md

**Comportement par défaut** : sauf indication de l'utilisateur, produisez à la fois les versions docx + md.

### Étape 6 : auto-vérification & retour

Après la sortie, faites une auto-vérification (à afficher dans la conversation, sans fichier séparé) :

```
✓ 长度：< 1 页（应届）/ ≤ 2 页（社招）
✓ 联系方式齐全（手机 + 邮箱，可选 GitHub/作品集）
✓ 每段经历都有量化结果
✓ 关键词覆盖率（vs <industry> 行业库）：__%
✓ ATS 友好度：__/10
⚠ 待用户确认：<还需要补的信息>
```

---

## Anti-patterns (à ne pas faire)

- ❌ Inventer des chiffres pour l'utilisateur (dire « +30 % » alors qu'il n'a jamais rien dit) — il faut s'appuyer uniquement sur les informations fournies ; à défaut, marquez `[à compléter : chiffre précis]`
- ❌ Empiler les adjectifs (« excellente capacité de communication », « consciencieux et rigoureux », « très motivé ») — supprimez
- ❌ Plus de 5 puces pour une seule expérience — trop dense, le recruteur saute
- ❌ Une longue « auto-évaluation » — ce n'est plus la mode ; un résumé de 1 à 2 lignes suffit
- ❌ Le même nombre de puces pour toutes les entreprises — plus pour les importantes, moins pour les secondaires
- ❌ Décrire ses capacités avec « connaît / a des notions / sait utiliser » — reformulez en « réalisé Y avec X »

## Coopération avec les autres skills

- L'utilisateur enchaîne avec « adapte-le pour cette entreprise » → basculez vers `jd-resume-tailor`
- L'utilisateur enchaîne avec « prépare l'entretien » → basculez vers `interview-prep`
- L'utilisateur veut retoucher son CV sans direction définie → demandez d'abord « vers quel type de poste vises-tu ? », et si besoin basculez vers `job-intent-tracker`
