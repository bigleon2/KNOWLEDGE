---
name: resume-builder
description: >-
  Génère de zéro ou optimise en profondeur un CV en chinois, avec export multi-formats docx /
  pdf / markdown. Réécrit les expériences selon la méthode STAR, vérifie la couverture de
  mots-clés ATS et choisit le gabarit selon le secteur (produit internet / technique /
  finance / général). Se déclenche obligatoirement quand l'utilisateur dit « 帮我写简历 /
  优化简历 / 简历不会写 / 我的简历太弱了 / 简历看起来不专业 / 简历改一改 / 给我做个简历模板 /
  简历导出 / 简历加点关键词 » (écris/optimise mon CV, mon CV est trop faible, pas pro,
  change-le, fais-moi un gabarit, exporte, ajoute des mots-clés), ou dépose un CV
  .pdf/.docx puis dit « 看看怎么改 » (vois comment le modifier). Se déclenche aussi pour la
  seule question « 我的简历有什么问题 » (qu'est-ce qui ne va pas dans mon CV ?).
---

## §0 — Contexte Système (SHARED v1.7.14)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# Resume Builder (génération et optimisation de CV)

Ce skill fait trois choses :

1. **Génération structurée** : produit à partir du parcours de l'utilisateur un CV conforme aux codes du marché de l'emploi chinois
2. **Réécriture STAR** : transforme les phrases faibles du type « j'ai participé à X » en « grâce à X, obtenu Y, avec pour résultat Z »
3. **Optimisation mots-clés ATS + export multi-gabarits** : garantit que le CV passe les filtres automatiques, avec export docx/pdf/md

Hors périmètre : la réécriture ciblée sur une offre (JD) — c'est l'affaire de jd-resume-tailor (« adapter mon CV à telle offre » se traite là-bas)

---

## Quand se déclencher

- « 帮我写一份简历 » (écris-moi un CV)
- « 我的简历太弱了 / 没有亮点 / 看起来不专业 » (mon CV est trop faible / sans relief / pas pro)
- « 把这段经历用 STAR 改一下 » (réécris cette expérience en STAR)
- « 简历里关键词够不够 » (mes mots-clés suffisent-ils ?)
- « 导出 PDF / docx 简历 » (exporte le CV en PDF/docx)
- L'utilisateur dépose un CV sans préciser « adapter à telle offre » → déclencher CE skill ; s'il dit « adapter à la société X / au poste X » → appeler jd-resume-tailor

---

## Flux de travail

### Étape 1 : Établir l'état actuel du CV

Si l'utilisateur **a un fichier CV** (.pdf / .docx / .md / .txt) :
- pdf : parser via le skill pdf
- docx : parser via le skill docx
- Extraire : informations personnelles, formation, expériences professionnelles, projets, compétences, divers

Si l'utilisateur **n'a pas de CV** :
- Collecter les informations via AskUserQuestion (liste de questions dans `references/intake_questions.md`)
- 3-4 questions par tour, en plusieurs tours, pour ne pas décourager

### Étape 2 : Choisir le gabarit

Lire `references/templates/` pour décider de la structure :

- Produit internet / operations / PM → `templates/internet.md`
- Technique / R&D / data → `templates/tech.md`
- Finance / conseil / école de commerce → `templates/finance.md`
- Général / intersectoriel → `templates/general.md`

Si l'utilisateur n'a pas précisé d'orientation, utiliser le gabarit général mais **poser la question** : « Vers quel secteur comptes-tu postuler ensuite ? Je peux utiliser une mise en page mieux adaptée. »

### Étape 3 : Réécrire chaque expérience en STAR

Lire `references/star_rewrite_guide.md` et appliquer la réécriture STAR à chaque expérience professionnelle / projet.

**STAR n'est pas un quadriptyque rigide** : l'essentiel est que chaque puce contienne :
- **Un signal de contexte** (une phrase qui situe l'ampleur du problème ou la situation)
- **Une action** (ce que tu as concrètement fait, avec un verbe)
- **Un résultat** (chiffre / pourcentage / classement / échelle)

Si les informations fournies **ne contiennent aucun chiffre**, relancer activement : « Quel était l'ordre de grandeur des utilisateurs de ce projet ? » « De combien l'optimisation a-t-elle amélioré les choses ? Si tu ne te souviens pas exactement, un ordre de grandeur suffit. »

### Étape 4 : Contrôle des mots-clés ATS

Appeler le script :

```bash
python scripts/ats_check.py --resume <resume.md> \
    --industry internet \
    [--jd <jd.txt>]
```

Le script :
1. Extrait les mots-clés du CV
2. Les compare au lexique sectoriel (issu de job-intent-tracker ou du `references/keywords/` du skill)
3. Produit deux listes « couvert / à ajouter »
4. Donne un score de compatibilité ATS (uniformité des polices, tableaux, symboles spéciaux, images, etc.)

**Règles strictes de compatibilité ATS** :
- Pas de tableau Word pour les expériences (beaucoup d'ATS échouent à les parser)
- Ne pas mettre les dates dans des images décoratives
- Pas de mise en page à deux colonnes (certains ATS lisent colonne par colonne et brouillent l'ordre)
- Pas d'icônes / emoji dans les titres
- Polices : Songti / Source Han Serif / Arial / Helvetica exclusivement

### Étape 5 : Export multi-formats

Lire `references/export_guide.md` et choisir selon le besoin :

**Export docx** (le plus universel, les RH chinoises préfèrent le docx) :
- Appeler le skill docx
- Utiliser `assets/resume_template.docx` comme gabarit (s'il existe)

**Export pdf** (version finale de candidature) :
- Flux recommandé : docx d'abord → conversion pdf via Word/LibreOffice
- La génération pdf directe avec reportlab rend mal : déconseillé
- Appeler le skill pdf pour le post-traitement (chiffrement / nettoyage des métadonnées)

**Export markdown** (sauvegarde + GitHub) :
- Écrire simplement le fichier .md

**Comportement par défaut** : sauf demande contraire, produire docx + md en parallèle.

### Étape 6 : Auto-contrôle & retours

Après la sortie, faire un auto-contrôle (affiché dans la conversation, sans fichier dédié) :

```
✓ Longueur : < 1 page (jeune diplômé) / ≤ 2 pages (expérimenté)
✓ Coordonnées complètes (téléphone + e-mail, option GitHub/portfolio)
✓ Chaque expérience a un résultat quantifié
✓ Couverture de mots-clés (vs lexique <industry>) : __%
✓ Compatibilité ATS : __/10
⚠ À confirmer avec l'utilisateur : <informations encore manquantes>
```

---

## Anti-patterns (à ne pas faire)

- ❌ Inventer des chiffres pour l'utilisateur (écrire « +30 % » sans que l'utilisateur l'ait dit) — s'appuyer uniquement sur ses informations ; en cas d'inconnue, marquer `[待补充：具体数字]` (à compléter : chiffre exact)
- ❌ Empiler les adjectifs (« excellente capacité de communication », « consciencieux et responsable », « ambitieux ») — supprimer
- ❌ Plus de 5 puces par expérience — trop dense, la RH passe outre
- ❌ « Auto-évaluation » interminable — passé de mode en Chine : 1-2 lignes de résumé suffisent
- ❌ Même nombre de puces pour toutes les entreprises — détailler l'important, résumer le secondaire
- ❌ Présenter « connaître / savoir utiliser » comme une compétence — reformuler en « réalisé Y avec X »

## Collaboration avec les autres skills

- L'utilisateur enchaîne sur « adapte pour cette société » → transférer à `jd-resume-tailor`
- L'utilisateur enchaîne sur « je prépare un entretien » → transférer à `interview-prep`
- L'utilisateur modifie son CV sans orientation claire → demander d'abord « vers quel secteur comptes-tu postuler ? » ; au besoin, transférer à `job-intent-tracker`
