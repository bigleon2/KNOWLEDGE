---
name: jd-resume-tailor
description: À partir d'une offre (JD) et d'un CV existant, réaliser « décomposition de l'offre + réécriture ciblée du CV ». Décomposer l'offre pour en extraire compétences dures, soft skills et points bonus ; analyser les écarts avec le CV ; produire une version du CV réécrite pour ce poste, mettant en avant l'expérience pertinente, comblant les trous de mots-clés, et préservant le parcours réel du candidat sans rien inventer. Quand l'utilisateur dit « adapte mon CV pour ce poste / cette entreprise », « compare avec cette offre », « je veux postuler à ce poste, comment modifier », « optimise ce CV pour l'entreprise X », « fais-moi une version ciblée », ou fournit à la fois le texte de l'offre + le fichier du CV, ce skill doit se déclencher. **Ne pas utiliser ce skill pour « écrire un CV de zéro »** — c'est l'affaire de resume-builder.
---

## §0 — Contexte Système (SHARED v1.7.13)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# JD ⇄ Resume Tailor (décomposition de l'offre + réécriture ciblée du CV)

Le périmètre de ce skill est très resserré : **traiter uniquement le cas « offre existante + CV existant, produire la version au meilleur taux de réussite »**.

Ce qu'il ne fait pas :
- écrire un CV neuf (voir `resume-builder`)
- trouver une orientation / recommander des postes (voir `job-intent-tracker`)
- produire des questions d'entretien (voir `interview-prep`)

---

## Quand se déclencher

Signaux forts :
- L'utilisateur donne un lien d'offre / le texte de l'offre + un CV → **déclenchement obligatoire**
- « adapte mon CV pour ce poste »
- « compare avec cette offre »
- « je veux postuler au poste Y de l'entreprise X, regarde mon CV »
- « fais-moi une version ciblée »

Signaux faibles (confirmer d'abord) :
- Offre seule sans CV → demander « pouvez-vous m'envoyer votre CV ? Sinon, je peux d'abord vous en composer un de zéro (resume-builder) »
- CV seul avec « modifie mon CV » → demander « pour quelle offre ? Sans offre, on passe par l'optimisation générale de resume-builder »

---

## Workflow

### Étape 1 : analyser l'offre

L'entrée peut être :
- du texte brut (collé par l'utilisateur)
- un lien (**ne pas** fetcher automatiquement ; inviter l'utilisateur à coller le texte de l'offre ; s'il autorise le fetch, utiliser web_fetch)
- une capture d'écran (OCR / reconnaissance visuelle, avec validation de l'extraction par l'utilisateur)
- un fichier doc/pdf

Appeler le script :

```bash
python scripts/parse_jd.py --jd-file <jd.txt> --out jd_parsed.json
```

Le script extrait de l'offre :
- **compétences dures must-have** (celles qui suivent les marqueurs forts — 必须 « obligatoire », 要求 « exigé », « au moins X ans » etc. — tels que détectés par le script dans les offres)
- **compétences dures nice-to-have** (marqueurs faibles — 加分 « un plus », 优先 « apprécié » etc.)
- **signaux de soft skills** (communication / entraînement / transverse / résistance à la pression etc.)
- **verbes de responsabilité + objet** (« responsable de X » / « construire Y » / « faire aboutir Z »)
- **exigences particulières** (déplacements / diplôme / certifications / langues / ville)

Présenter le résultat à l'utilisateur pour **validation / correction de l'extraction** (aucun must-have clé ne doit manquer).

### Étape 2 : analyser le CV

Entrée : le fichier de CV téléversé (.pdf / .docx / .md / .txt).

Appeler le skill correspondant :
- pdf → skill pdf
- docx → skill docx

Extraire : informations de base, formation, pour chaque expérience pro/projet (entreprise, poste, période, puces de responsabilités), liste de compétences.

### Étape 3 : analyse des écarts

Appeler :

```bash
python scripts/jd_gap.py --jd jd_parsed.json --resume resume.txt --out gap.md
```

Le script produit trois listes :

1. **Correspondances parfaites** (un must-have de l'offre avec preuve explicite dans le CV)
2. **Correspondances implicites** (l'offre demande X, le CV contient une expérience synonyme mais formulée autrement → possible de « le mentionner » en réécrivant)
3. **Vraies lacunes** (demandé par l'offre, totalement absent du CV)

Pour les vraies lacunes, deux cas :
- **Rattrapables** : le candidat a fait des choses similaires sans les avoir écrites → lui demander « avez-vous déjà fait X ? »
- **Non rattrapables** : le candidat ne l'a vraiment jamais fait → **ne rien inventer** ; suggérer de l'expliquer honnêtement dans la lettre de motivation ou le Summary en valorisant les compétences transférables

### Étape 4 : réécriture ciblée

Réécrire le CV selon les principes suivants :

**a. Réordonner les expériences** : placer en tête le travail/projet le plus pertinent pour l'offre (sans toucher à la vérité des dates, mais les projets peuvent être scindés en deux blocs « projets pertinents / autres projets »)

**b. Réécrire chaque puce** :
- Insérer naturellement les « verbes de responsabilité » de l'offre dans la puce (ex. l'offre dit « piloter la conception du système ___ » : dans le CV, transformer « participé à » en « piloté » — à condition que l'utilisateur l'ait réellement piloté)
- Conserver et mettre en avant les chiffres (« 1 million d'utilisateurs » est un atout, ne pas le cacher)
- Combler les mots-clés de l'offre (ex. l'offre dit « tests A/B » alors que le CV écrit « comparaisons en déploiement progressif » : reformuler en « tests A/B (comparaisons en déploiement progressif) »)

**c. Réécrire le Summary** : 2~3 lignes résumant pourquoi vous êtes le bon candidat pour CE poste, **en réponse directe aux must-have de l'offre**

**d. Ajuster la liste de compétences** : remonter les compétences citées par l'offre (à condition de les maîtriser réellement)

**e. Les faits intouchables** :
- noms d'entreprises, intitulés de postes, dates, diplômes — inchangés au mot près
- échelle des projets, volumes d'utilisateurs, chiffres de revenus — rien à inventer, seulement à faire confirmer et préciser par l'utilisateur

### Étape 5 : auto-contrôle + rapport

Produire trois livrables :
1. `resume_tailored_<entreprise>_<poste>.md` (le CV réécrit)
2. `gap_analysis.md` (le rapport d'analyse des écarts)
3. Dans le chat, une comparaison du taux de réussite ATS : « avant X % → après Y % »

En annexe : rappeler honnêtement à l'utilisateur **quelles puces ont été réécrites par inférence à partir des informations existantes**, pour relecture avant envoi.

---

## Anti-patterns (à ne pas faire)

- ❌ Inventer des expériences (« ajouter un projet que vous n'avez pas vécu » — interdit absolu, même à la demande de l'utilisateur)
- ❌ Coller des paragraphes entiers de l'offre dans le CV (les RH le repèrent immédiatement, et l'anti-triche ATS le signale)
- ❌ Le bourrage de mots-clés (une longue traîne de compétences en fin de CV pour gonfler le score, visible au premier coup d'œil)
- ❌ Transformer « participé à » en « piloté » sans avoir interrogé l'utilisateur sur son rôle réel → vérifier d'abord
- ❌ Modifier en cachette sans montrer les écarts à l'utilisateur → il perdrait la « compréhension » de son propre CV

## Collaboration avec les autres skills

- Après la réécriture, si l'utilisateur dit « prépare-moi l'entretien de cette entreprise » → passer à `interview-prep` en transmettant l'offre + le CV réécrit
- Si l'utilisateur dit « je veux savoir à quels postes similaires postuler » → passer à `job-intent-tracker`
- Si l'utilisateur dit « mon CV est vraiment faible, peut-on tout refaire » → passer à `resume-builder`
