---
nom: job-intent-tracker
source: skills/job-intent-tracker/SKILL.md
sha256_source: db0adbcdeeac
genere: 2026-10-29 (phase P2 — directive 10 tâches, tâche 2)
usage: AUTONOME hors écosystème (dossier « Prompt Maitre » — non lu par l'orchestration)
---

> ⚠️ **MARQUEUR D'EXCLUSION (garde D010)** — CE DOSSIER N'EST PAS LU PAR L'ORCHESTRATION. Les dossiers « Prompt Maitre » sont des prompts autonomes à usage HORS écosystème : ils ne sont pas indexés au registre KB, ne sont mobilisés par aucun arbitre, et ne remplacent jamais la forme installée `skills/<skill>/` (source de vérité).

# Prompt Maître autonome — job-intent-tracker (version non déclarée)

## Comment utiliser ce prompt (hors écosystème)

Ce document encapsule la compétence sous forme autonome : copiez-le intégralement
dans un assistant IA (ou ouvrez-le en référence directe) — aucune installation,
aucun registre, aucune dépendance à l'écosystème Knowledge d'origine n'est requise.
Les variables de l'écosystème d'origine ont été résolues en valeurs littérales ;
si des ressources `references/` accompagnent ce dossier, elles sont jointes au même
emplacement et le prompt y renvoie par leur chemin relatif. La version d'origine
(source de vérité) vit dans `skills/job-intent-tracker/SKILL.md` du dépôt KNOWLEDGE.

---

## Le prompt

---
name: job-intent-tracker
description: Aider l'utilisateur à clarifier ses intentions de recherche d'emploi, générer des profils de postes cibles et tenir un « tableau de suivi de candidatures » structuré. Quand l'utilisateur dit « je veux changer de travail / je ne sais pas quoi viser / regarde quels postes me conviennent / aide-moi à suivre mes candidatures / j'ai postulé à plein d'endroits mais je ne retiens plus où j'en suis / je veux un OKR de recherche / clarifie mon orientation », ou dépose un CV sans demander de réécriture, ce skill doit se déclencher activement. Il convient aussi aux stagiaires, jeunes diplômés et candidats en reconversion au moment du lancement de leur recherche, pour les trois volets « auto-inventaire + profil cible + gestion des candidatures ».
---

## §0 — Contexte Système (SHARED v1.7.14)

> Écosystème Knowledge : `skills/`=skills/ | `skills/KNOWLEDGE.md`=skills/KNOWLEDGE.md | `true`=true | `NORMAL`=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# Job Intent Tracker (intentions de recherche + suivi des candidatures)

Ce skill répond aux trois questions clés de la phase de lancement d'une recherche :

1. **Quels postes me conviennent ?** — extraire les signaux du parcours de l'utilisateur pour déduire 2~3 orientations cibles
2. **À quoi ressemble le poste visé ?** — générer pour chaque orientation un « profil de poste / Target Profile »
3. **Où j'en suis de mes candidatures ?** — tenir un tableau de suivi structuré (Excel / table Markdown)

Ne pas détourner ce skill en « réécriture de CV » ou « générateur de questions d'entretien » — c'est l'affaire de resume-builder / jd-resume-tailor / interview-prep. Ce skill ne traite que « l'orientation » et « la gestion ».

---

## Quand ce skill se déclenche

Signaux forts (usage quasiment obligatoire) :
- « je veux changer de travail / je veux bouger / je cherche mon prochain poste »
- « regarde quels postes me conviennent »
- « aide-moi à suivre mes candidatures / suis les entreprises où j'ai postulé »
- « j'ai X ans d'expérience en Y, quelle est la prochaine étape »
- « j'ai postulé à plein d'endroits et j'ai perdu le fil »

Signaux faibles (confirmer avant) :
- L'utilisateur dépose juste un CV sans préciser l'objectif → demander « tu veux clarifier ton orientation, retravailler le CV, ou préparer des entretiens ? »
- « je veux retrouver un travail » très vague → demander « as-tu déjà une orientation en tête, ou veux-tu que je t'aide à en déterminer une ? »

---

## Workflow

Suivre cet ordre, sans sauter d'étape :

### Étape 1 : auto-inventaire (Background Intake)

Collecter les informations suivantes avec AskUserQuestion (ou en questionnant directement à défaut). **Ne pas tout demander d'un coup : 2~3 salves de 2~3 questions**, sinon l'utilisateur décroche face au questionnaire.

Première salve (indispensable) :
- poste, type d'entreprise et ancienneté du poste actuel / dernier poste
- 3~5 compétences clés (des mots-clés suffisent)
- secteur / orientation cibles (si l'utilisateur en a) — sinon, peu importe, passer à l'étape 2

Deuxième salve (selon le cas) :
- fourchette de rémunération souhaitée (passer si l'utilisateur préfère ne pas dire)
- préférences de ville / acceptation du remote
- exclusions (« pas de commercial / pas d'heures sup / pas de déplacements » etc.)

Troisième salve (signaux de profondeur, seulement si les deux premières salves ne suffisent pas à bâtir le profil) :
- 1~2 projets dont il est le plus fier
- ce qu'il déteste le plus faire
- où il se voit dans 5 ans

Si l'utilisateur a téléversé un CV .pdf / .docx, **appeler d'abord le skill pdf ou docx pour extraire le texte**, puis en tirer les informations ci-dessus — éviter de lui faire retaper.

### Étape 2 : recommander des orientations

À partir de l'étape 1, produire 2~3 orientations candidates. Chacune doit exposer clairement :

```
Orientation N : <intitulé du poste> (ex. : product manager internet / data analyst / chercheur quantitatif)
- Adéquation : haute / moyenne / basse (haute = compétences clés directement en jeu ; moyenne = 1~2 compétences clés à acquérir ; basse = récit de reconversion nécessaire)
- Justification de l'adéquation : au vu de l'expérience ___ et de la compétence ___ de l'utilisateur
- Manque : ce que l'utilisateur doit encore acquérir pour devenir un candidat fort
- Employeurs types : <3~5 entreprises ou types d'entreprises précis>
- Fourchette de rémunération (indicative) : __k - __k (préciser « tendance de marché, à titre indicatif ; inviter l'utilisateur à vérifier selon le niveau et la ville »)
```

**Important : ne pas ne recommander que des orientations « sûres ».** Si les compétences le permettent, donner au moins une orientation « atteignable en se stretchant un peu », avec un étiquetage honnête des manques.

### Étape 3 : générer le profil de poste (Target Profile)

Pour les 1~2 orientations **finalement retenues** (laisser l'utilisateur choisir activement), générer le profil détaillé. Le gabarit est dans `references/target_profile_template.md` — lire ce fichier avant de le remplir.

Le profil doit contenir : description type des responsabilités, must-have / nice-to-have, attentes sur le processus de recrutement, liste des entreprises de référence (par paliers).

Lire la bibliothèque de mots-clés sectoriels pour arbitrer must-have / nice-to-have :
- produit internet / opérations / PM → `references/keywords_internet.md`
- technique / R&D / data → `references/keywords_tech.md`
- finance / conseil / commerce → `references/keywords_finance.md`
- généraliste / intersectoriel → `references/keywords_general.md`

### Étape 4 : créer le tableau de suivi des candidatures

Appeler `scripts/init_tracker.py` pour générer le tableau initial. Deux formats :

```bash
python scripts/init_tracker.py --format xlsx --output /path/to/tracker.xlsx
# ou
python scripts/init_tracker.py --format md --output /path/to/tracker.md
```

xlsx recommandé par défaut (l'utilisateur peut trier, ajouter des mises en forme conditionnelles). Si l'utilisateur veut du léger, prendre md.

Structure des colonnes du tableau (pré-réglée dans le script, ne pas modifier) :
entreprise, poste, source (chasseur/site officiel/recommandation/plateforme), lien de l'offre, date de candidature, étape en cours (candidature/test écrit/entretien 1/entretien 2/RH/offre/refus/silence), prochaine action, échéance, fourchette de rémunération, parrain interne, notes

### Étape 5 : un « tableau de bord emploi » en Artifact (optionnel mais recommandé)

Si l'environnement propose l'outil `mcp__cowork__create_artifact`, proposer activement : « veux-tu que je transforme ce tableau en un tableau de bord que tu peux ouvrir chaque jour ? »

Si l'utilisateur accepte, créer un artifact HTML rendu depuis les données du tableau :
- KPI en haut : total des candidatures / passages en entretien / offres / relances en attente
- Table au milieu : vue Kanban groupée par « étape en cours »
- Rappels en bas : entreprises sans nouvelles depuis 3 jours, tâches dont l'échéance approche

---

## Style de sortie

- **Structuré, actionnable**, pas de généralités du type « tu devrais postuler davantage »
- Pour toute mention de rémunération ou de jugement sectoriel, **étiqueter explicitement « référence de marché, non contractuel »**
- Ne pas être flatteur dans les recommandations (ne pas pousser tout le monde vers « les postes IA très payants »), évaluer l'adéquation avec honnêteté
- Si l'utilisateur refuse une orientation, ne pas insister : comprendre pourquoi puis ajuster

---

## Collaboration avec les autres skills

- Orientation retenue puis « retravaille mon CV » → appeler `resume-builder` en transmettant le profil de poste
- « Adapte pour l'offre de cette entreprise » → appeler `jd-resume-tailor`
- « Prépare-moi pour l'entretien » → appeler `interview-prep` en transmettant le profil de poste

Formuler des phrases de transition du type « j'ai enregistré ton profil de poste dans ___, prochaine étape possible : me demander de retravailler le CV avec resume-builder », pour que l'agent enchaîne dans les tâches multi-étapes.

---

## Anti-patterns (à ne pas faire)

- ❌ Poser 8 questions d'emblée
- ❌ Recommander 5 orientations sans demander les préférences
- ❌ Parler sans fournir le tableau de suivi
- ❌ Fourguer « opérations / produit / chef de projet » à tout profil littéraire
- ❌ Pousser sans réfléchir vers les postes LLM dès qu'on voit « IA / grand modèle », sans évaluer l'adéquation réelle des compétences


---

## Ressources locales du dossier

Ressources jointes (usage autonome — lire au besoin pendant l'application du prompt) :
- `references/keywords_finance.md`
- `references/keywords_general.md`
- `references/keywords_internet.md`
- `references/keywords_tech.md`
- `references/target_profile_template.md`
