---
name: jd-resume-tailor
version: "1.0.0"
category: "Carrière & Emploi"
tags:
  - jd
  - resume
  - tailor
description: À partir d'une fiche de poste (JD) et d'un CV existant, effectue « décryptage du JD + réécriture ciblée du CV ». Extrait du JD les compétences techniques dures, les compétences douces et les atouts bonus ; compare avec le CV pour une analyse d'écarts ; produit un CV réécrit pour ce poste précis, valorisant les expériences pertinentes, comblant les manques de mots-clés, tout en préservant les expériences réelles du candidat sans rien inventer. Quand l'utilisateur dit « adapte mon CV à ce poste / à cette entreprise », « aide-moi à comparer avec ce JD », « je veux postuler à cette offre, vois comment modifier mon CV », « optimise ce CV pour l'entreprise X », « fais-moi une version ciblée du CV », ou fournit simultanément un texte de JD + un fichier de CV, ce skill doit être déclenché. **Ne pas utiliser ce skill pour « écrire un CV de zéro »** — c'est le rôle de resume-builder.
language: fr

read_when:
  - Déclencher quand la demande concerne : à partir d'une fiche de poste (JD) et d'un CV existant, effectue « décryptage du JD + réécriture ciblée du CV…
  - Déclencher si la demande mentionne : poste, ciblée, compétences
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

# JD ⇄ Resume Tailor (décryptage du JD + réécriture ciblée du CV)

Le périmètre de ce skill est étroit : **il ne résout que « on a déjà un JD + un CV, il faut produire la version au taux de réussite le plus élevé »**.

Ce qu'il ne fait pas :
- Écrire un nouveau CV (voir `resume-builder`)
- Trouver une orientation / recommander des postes (voir `job-intent-tracker`)
- Créer des questions d'entretien (voir `interview-prep`)

---

## Quand se déclencher

Signaux forts :
- l'utilisateur fournit un lien JD / un texte JD + un CV → **déclenchement obligatoire**
- « adapte mon CV à ce poste »
- « compare avec ce JD »
- « je veux postuler au poste Y de l'entreprise X, examine mon CV »
- « fais une version ciblée »

Signaux faibles (confirmer d'abord) :
- JD fourni mais pas de CV → demander « peux-tu m'envoyer ton CV ? Sinon, je peux d'abord t'aider à en créer un de zéro (resume-builder) »
- CV fourni avec juste « améliore mon CV » → demander « par rapport à quel JD ? Sans JD, passe par resume-builder pour une optimisation générique »

---

## Flux de travail

### Étape 1 : analyser le JD

L'entrée peut être :
- du texte brut (collé par l'utilisateur)
- un lien (**ne pas** faire de fetch automatique, rappeler à l'utilisateur de copier le texte du JD ; si l'utilisateur autorise le fetch, utiliser web_fetch)
- une capture d'écran (utiliser l'OCR / la reconnaissance visuelle, faire confirmer le résultat d'extraction à l'utilisateur)
- un fichier doc/pdf

Appeler le script :

```bash
python scripts/parse_jd.py --jd-file <jd.txt> --out jd_parsed.json
```

Le script extrait du JD :
- **les compétences dures must-have** (les compétences qui suivent les mots de signal fort comme « indispensable » / « requis » / « au moins X ans »)
- **les compétences dures nice-to-have** (les signaux faibles comme « un plus » / « apprécié » / « les candidats familiers seront privilégiés »)
- **les signaux de compétences douces** (communication / drive / transversal / résistance au stress, etc.)
- **les verbes de responsabilité + objets** (« responsable de X » / « mettre en place Y » / « porter Z »)
- **les exigences particulières** (déplacements / diplôme / certifications / langues / ville)

Présenter le résultat à l'utilisateur pour qu'il **confirme / corrige l'exactitude de l'extraction** (les must-have clés ne doivent pas être manqués).

### Étape 2 : analyser le CV

Entrée : fichier de CV téléversé par l'utilisateur (.pdf / .docx / .md / .txt).

Appeler le skill correspondant pour l'analyse :
- pdf → skill pdf
- docx → skill docx

Extraire : informations de base, formation, chaque expérience professionnelle / projet (entreprise, poste, période, puces de responsabilités), liste de compétences.

### Étape 3 : analyse d'écarts (gap)

Appeler :

```bash
python scripts/jd_gap.py --jd jd_parsed.json --resume resume.txt --out gap.md
```

Le script produit trois listes :

1. **Correspondance parfaite** (le must-have du JD a une preuve claire dans le CV)
2. **Correspondance implicite** (le JD demande X, le CV contient une expérience proche de X, mais formulée différemment → réécrivable en « le mentionnant »)
3. **Véritable manque** (exigé par le JD mais totalement absent du CV)

Pour les « véritables manques », distinguer deux cas :
- **Rattrapable** : le CV décrit en réalité des choses similaires, simplement non formulées → demander à l'utilisateur « as-tu déjà fait X ? »
- **Non rattrapable** : l'utilisateur ne l'a vraiment pas fait → **ne rien inventer**, conseiller à l'utilisateur de le reconnaître honnêtement dans la cover letter ou le summary et de mettre en avant ses compétences transférables

### Étape 4 : réécriture ciblée

Réécrire le CV selon les principes suivants :

**a. Réordonner les expériences** : placer en tête les expériences professionnelles / projets les plus pertinents avec le JD (sans altérer la réalité des dates, mais on peut scinder les projets en deux blocs « projets pertinents / autres projets »)

**b. Réécrire chaque puce** :
- insérer naturellement les « verbes de responsabilité » du JD dans les puces (si le JD dit « piloter la conception du système ___ », remplacer dans le CV « participer » par « piloter » — à condition que l'utilisateur ait réellement piloté)
- conserver et amplifier les chiffres (« 1 million d'utilisateurs » est un atout, ne pas le cacher)
- compléter les mots-clés du JD (si le JD dit « tests A/B » et que le CV écrit « comparaison en déploiement graduel », écrire « tests A/B (déploiement graduel) »)

**c. Réécrire le Summary** : résumer en 2 à 3 lignes pourquoi vous êtes le bon candidat pour ce poste, **en réponse directe aux must-have du JD**

**d. Ajuster la liste de compétences** : faire remonter en tête les compétences mentionnées dans le JD (à condition de vraiment les maîtriser)

**e. Les faits intangibles** :
- nom de l'entreprise, intitulé du poste, dates de début et fin, formation — pas un mot changé
- taille des projets, nombre d'utilisateurs, chiffres de revenus — interdiction d'inventer, ne faire remplir que ce que l'utilisateur confirme

### Étape 5 : autocontrôle + rapport

Produire trois fichiers :
1. `resume_tailored_<entreprise>_<poste>.md` (le CV réécrit)
2. `gap_analysis.md` (rapport d'analyse d'écarts)
3. Dans le chat, une comparaison du taux de correspondance ATS : « avant X % → après Y % »

Ajouter : rappeler honnêtement à l'utilisateur **quelles puces ont été réécrites par déduction à partir des informations existantes**, pour qu'il vérifie avant de postuler.

---

## Anti-patterns (à ne pas faire)

- ❌ Inventer des expériences (« ajoute un projet que tu n'as jamais fait » — absolument interdit, même à la demande de l'utilisateur)
- ❌ Coller des paragraphes entiers du JD directement dans le CV (repéré très vite par les RH, et l'anti-fraude ATS le signale)
- ❌ Bourrage de mots-clés (entasser une longue liste de compétences à la fin pour gonfler le taux, les RH le voient immédiatement)
- ❌ Remplacer « participer » par « piloter » sans avoir demandé le rôle réel de l'utilisateur → vérifier d'abord
- ❌ Ne pas montrer l'analyse d'écarts à l'utilisateur et modifier en silence → l'utilisateur perd la « compréhension » de son CV

## Collaboration avec les autres skills

- Après modification, l'utilisateur dit « aide-moi à préparer l'entretien de cette entreprise » → transférer vers `interview-prep` en transmettant le JD + le CV réécrit
- L'utilisateur dit « je voudrais savoir à quels autres postes similaires postuler » → transférer vers `job-intent-tracker`
- L'utilisateur dit « mon CV n'est vraiment pas bon, peut-on tout refaire » → transférer vers `resume-builder`
