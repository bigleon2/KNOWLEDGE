---
name: job-intent-tracker
version: "1.0.0"
category: "Carrière & Emploi"
tags:
  - job
  - intent
  - tracker
description: Aide l'utilisateur à clarifier ses intentions de recherche d'emploi, génère un portrait des postes cibles et tient à jour une « table de suivi des candidatures » structurée. Quand l'utilisateur dit « je veux changer de travail / je ne sais pas à quel poste postuler / aide-moi à voir quel poste me convient / aide-moi à gérer mes candidatures / j'ai postulé à plusieurs endroits mais je perds le fil / je veux un OKR de recherche d'emploi / range ma recherche d'emploi », ou téléverse un CV sans demander de modification, ce skill doit être déclenché proactivement. Ce skill s'adresse aussi aux stagiaires, jeunes diplômés et candidats en reconversion qui, au démarrage de leur recherche, veulent faire trois choses : « auto-diagnostic + portrait cible + gestion des candidatures ».
language: fr

read_when:
  - Déclencher quand la demande concerne : aide l'utilisateur à clarifier ses intentions de recherche d'emploi, génère un portrait des postes cibles et t…
  - Déclencher si la demande mentionne : recherche, aide, emploi
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

# Job Intent Tracker (intentions d'emploi + suivi des postes)

Ce skill résout trois problèmes centraux du « démarrage de la recherche d'emploi » :

1. **À quels postes puis-je postuler ?** — extraire des signaux du profil de l'utilisateur et en déduire 2 à 3 orientations cibles
2. **À quoi ressemble le poste cible ?** — générer pour chaque orientation un « portrait de poste / Target Profile »
3. **Où ai-je postulé, et où j'en suis ?** — tenir une table de suivi structurée (table Excel / Markdown)

Ne pas utiliser ce skill comme un outil de « réécriture de CV » ou de « génération de questions d'entretien » — c'est le rôle de resume-builder / jd-resume-tailor / interview-prep. Ce skill ne s'occupe que de l'« orientation » et de la « gestion ».

---

## Quand déclencher ce skill

Signaux forts (à utiliser en principe) :
- « je veux changer de travail / démissionner / trouver le prochain poste »
- « aide-moi à voir quel poste me convient »
- « aide-moi à gérer mes candidatures / suis les entreprises où j'ai postulé »
- « j'ai X ans d'expérience en Y, où aller ensuite »
- « j'ai postulé à plein d'endroits mais j'ai perdu le fil »

Signaux faibles (confirmer avant d'utiliser) :
- l'utilisateur envoie juste un CV sans dire pourquoi → demander d'abord « tu veux clarifier ton orientation, améliorer ton CV, ou préparer un entretien ? »
- l'utilisateur dit « je cherche un travail » mais reste flou → demander d'abord « as-tu déjà une orientation en tête ? Ou veux-tu que je t'aide à la déterminer ? »

---

## Flux de travail

Suivre cet ordre, sans sauter d'étape :

### Étape 1 : auto-diagnostic (Background Intake)

Utiliser AskUserQuestion (ou poser directement les questions si l'outil est absent) pour recueillir les informations suivantes. **Ne pas tout demander d'un coup : procéder en 2 à 3 tours de 2 à 3 questions**, sinon l'utilisateur se fera « sonder » et décrochera.

Premier tour (obligatoire) :
- poste actuel / plus récent, type d'entreprise, ancienneté
- 3 à 5 compétences clés (mots-clés suffisent)
- secteur / orientation cible (si l'utilisateur en a) — pas grave si non, passer à l'étape 2

Deuxième tour (selon le cas) :
- fourchette de salaire attendue (passer si l'utilisateur ne veut pas en parler)
- préférence de ville / acceptation du remote
- exclusions (« pas de vente / pas d'heures supplémentaires / pas de déplacements », etc.)

Troisième tour (signaux profonds, seulement si les deux premiers tours ne suffisent pas à dresser le portrait) :
- les 1 à 2 projets dont il est le plus fier
- ce qu'il n'aime le plus pas faire
- sa vision à 5 ans

Si l'utilisateur a téléversé un CV en .pdf / .docx, **appeler d'abord le skill pdf ou docx pour extraire le texte**, puis en tirer les informations ci-dessus, pour éviter à l'utilisateur de ressaisir.

### Étape 2 : recommander des orientations professionnelles

À partir des informations de l'étape 1, générer 2 à 3 orientations candidates. Chaque orientation doit préciser :

```
方向 N：<岗位名>（如：互联网产品经理 / 数据分析师 / 量化研究员）
- 匹配度：高 / 中 / 低（高=核心技能直接命中；中=需补 1~2 个关键技能；低=需要转岗叙事）
- 匹配理由：基于用户的 ___ 经验和 ___ 技能
- 缺口：用户还需要补 ___ 才能成为强候选人
- 典型雇主：<3~5 个具体公司或公司类型>
- 薪资带（仅供参考）：__k - __k（注明"市场行情，仅供参考，建议用户自行通过职级查询"）
```

**Important : ne pas recommander uniquement des orientations « sûres ».** Si les compétences de l'utilisateur le permettent, proposer au moins une orientation « accessible en s'étirant », et étiqueter honnêtement les manques.

### Étape 3 : générer le portrait de poste (Target Profile)

Pour les 1 à 2 orientations **finalement choisies** par l'utilisateur (le laisser choisir), générer un portrait détaillé. Le modèle se trouve dans `references/target_profile_template.md`, à lire avant de remplir.

Le portrait doit contenir : description type des responsabilités, exigences de compétences must-have / nice-to-have, déroulé d'entretien attendu, liste d'entreprises de référence (par palier).

Lire la banque de mots-clés sectorielle pour décider des must-have / nice-to-have :
- Produit / opérations / PM internet → `references/keywords_internet.md`
- Technique / R&D / data → `references/keywords_tech.md`
- Finance / conseil / business → `references/keywords_finance.md`
- Général / tous secteurs → `references/keywords_general.md`

### Étape 4 : créer la table de suivi des candidatures

Appeler `scripts/init_tracker.py` pour générer la table de suivi initiale. Le script supporte deux formats :

```bash
python scripts/init_tracker.py --format xlsx --output /path/to/tracker.xlsx
# ou
python scripts/init_tracker.py --format md --output /path/to/tracker.md
```

Format recommandé par défaut : xlsx (l'utilisateur peut trier, ajouter une mise en forme conditionnelle). Si l'utilisateur demande explicitement du léger, utiliser md.

Structure des colonnes de la table (déjà préréglée dans le script, à ne pas modifier) :
entreprise, poste, source (chasseur / site officiel / cooptation / site d'emploi), lien JD, date de candidature, étape actuelle (soumise / test écrit / premier entretien / deuxième entretien / entretien RH / Offer / Reject / sans nouvelles), prochaine action, Deadline, fourchette de salaire, référent, remarques

### Étape 5 : faire un « tableau de bord de recherche d'emploi » avec un Artifact (optionnel mais recommandé)

Si l'environnement courant dispose de l'outil `mcp__cowork__create_artifact`, proposer proactivement : « veux-tu que je transforme cette table de suivi en un tableau de bord consultable chaque jour ? »

Si l'utilisateur accepte, créer un artifact HTML rendu à partir des données de la table :
- KPI en haut : nombre total de candidatures / entrées en entretien / Offers / à relancer
- Table au centre : vue Kanban groupée par « étape actuelle »
- Rappels en bas : entreprises sans nouvelle depuis 3 jours, tâches proches de leur deadline

---

## Style de sortie

- **Structuré, actionnable** ; ne pas rester dans le vague avec des phrases comme « poste plus de candidatures »
- Pour tout ce qui touche au salaire ou au jugement sectoriel, **étiqueter explicitement « référence de marché, sans engagement »**
- En recommandant des orientations, ne pas flatter (ne pas pousser tous les utilisateurs vers « les postes IA bien payés »), évaluer honnêtement l'adéquation
- Si l'utilisateur refuse une orientation, ne pas insister : demander pourquoi puis ajuster

---

## Collaboration avec les autres skills

- L'utilisateur a choisi une orientation et dit « alors améliore mon CV » → appeler `resume-builder` en transmettant le portrait de poste
- L'utilisateur dit « adapte-le au JD de cette entreprise » → appeler `jd-resume-tailor`
- L'utilisateur dit « aide-moi à préparer l'entretien » → appeler `interview-prep` en transmettant le portrait de poste

Produire une phrase de transition du type « j'ai enregistré ton portrait de poste dans ___, tu peux maintenant me demander d'améliorer ton CV avec resume-builder », pour que l'agent enchaîne dans les tâches en plusieurs étapes.

---

## Anti-patterns (à ne pas faire)

- ❌ Démarrer avec 8 questions d'affilée
- ❌ Ne pas demander les préférences de l'utilisateur et pousser 5 orientations d'un coup
- ❌ Ne pas fournir de table de suivi et seulement déblatérer dans le chat
- ❌ Proposer « opérations / produit / chef de projet » à tous les profils littéraires
- ❌ Voir « IA / grands modèles » et pousser bêtement des postes LLM sans évaluer l'adéquation réelle des compétences
