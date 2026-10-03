---
name: interview-prep
version: "1.0.0"
category: "Carrière & Emploi"
tags:
  - interview
  - prep
description: Aide l'utilisateur à préparer ses entretiens. À partir du JD cible, de l'entreprise et du poste visé, génère « questions d'entretien fréquentes + réponses de référence + banque de questions classée par entretien comportemental / technique / case », et produit un « manuel de préparation aux entretiens » imprimable. Quand l'utilisateur dit « aide-moi à préparer un entretien », « j'ai un entretien demain / après-demain », « questions d'entretien », « retours d'expérience d'entretien », « simulation d'entretien », « je passe un entretien pour le poste Y chez X », « aide-moi à préparer une histoire STAR », « comment répondre à cette question d'entretien », « présentation / raisons du départ / forces et faiblesses : comment répondre », ce skill doit être déclenché. Ne pas utiliser ce skill pour modifier un CV (voir jd-resume-tailor / resume-builder) ni pour recommander une orientation (voir job-intent-tracker).
language: fr

---

# Interview Prep (préparation aux entretiens)

Il fait 4 choses :

1. **Décortiquer le scénario d'entretien** : clarifier l'entreprise cible / le poste / le tour d'entretien (premier tour / deuxième tour / tour final / entretien RH)
2. **Générer la banque de questions** : puiser à la demande dans 4 banques de questions (comportemental, technique, case, spécifiques au poste)
3. **Générer des réponses de référence** : avec les cadres STAR / SCQA / MECE, en s'appuyant sur les faits du CV de l'utilisateur
4. **Produire le « manuel de préparation »** : un .md / .docx / .pdf imprimable, contenant les questions + pistes de réponse + liste d'autocontrôle

---

## Quand se déclencher

Signaux forts :
- « aide-moi à préparer un entretien / simulation d'entretien / entraînement d'entretien »
- « entretien demain / la semaine prochaine »
- mention d'une entreprise précise + d'un poste
- « questions d'entretien fréquentes / questions classiques »
- « comment répondre à la question ___ »
- « comment se présenter / comment justifier un départ / comment négocier le salaire attendu »

Signaux faibles (confirmer d'abord) :
- l'utilisateur dit seulement « je voudrais en savoir plus sur les entretiens » → demander quelle orientation / quel tour d'entretien

---

## Flux de travail

### Étape 1 : cerner le scénario d'entretien

Utiliser AskUserQuestion pour recueillir :
- Entreprise cible (nom précis / grande entreprise vs startup vs étrangère / type d'entreprise)
- Poste cible (précis jusqu'à l'orientation, p. ex. « PM growth » plutôt que « chef de produit »)
- Tour d'entretien (premier tour / deuxième tour / tour final / entretien RH / répétition complète)
- Urgence (demain / cette semaine / dans plus d'une semaine) — influence « largeur vs profondeur »
- Documents déjà disponibles (JD / CV / informations publiques sur l'entreprise / contexte connu des intervieweurs)

Si l'utilisateur a fourni le JD et le CV, **appeler d'abord le parse_jd.py de jd-resume-tailor** pour extraire les informations clés du poste et éviter une double analyse.

### Étape 2 : stratégie de sélection des questions

Décider de la structure de la banque de questions selon « tour + orientation + temps ». Lire les fichiers correspondants :

- Comportemental (demandé à chaque tour) → `references/behavioral.md`
- Technique (champ de bataille des postes techniques / data) → `references/technical.md`
- Case (conseil / stratégie / PM senior) → `references/case.md`
- RH (dernier kilomètre de tout poste) → `references/hr_round.md`
- Banques spécifiques au poste :
  - Produit / opérations / PM internet → `references/role_internet.md`
  - Technique / R&D / data → `references/role_tech.md`
  - Finance / conseil / business → `references/role_finance.md`

Volume de questions recommandé :
- **Entretien demain** : 5 à 8 questions par catégorie, focus sur les questions fréquentes
- **3 à 7 jours** : 10 à 15 questions par catégorie
- **> 1 semaine** : couverture complète + tours de simulation

### Étape 3 : générer les réponses de référence

**Principe clé : les réponses de référence doivent s'appuyer sur les expériences réelles du CV de l'utilisateur, pas être des réponses génériques.**

Appeler `scripts/star_story_builder.py` (s'il y a un CV) :

```bash
python scripts/star_story_builder.py --resume resume.md \
    --questions questions.json --out answers.md
```

Sinon, sans CV, utiliser le cadre de réponse générique (à lire dans references/answer_frameworks.md) comme modèle et laisser l'utilisateur compléter.

Format des réponses de référence :
```
【题目】___
【考察点】HR / 面试官想看你的什么能力
【回答框架】STAR / SCQA / MECE / 5W1H 之一
【建议长度】X 分钟（一般 1.5~3 分钟）
【参考回答 (基于你简历里的 ___ 经历)】
  S: 当时的背景 / 问题
  T: 你的任务 / 目标
  A: 你的具体动作（重点，要细节）
  R: 量化结果 + reflect
【可能的追问】1. ___ 2. ___ 3. ___
```

### Étape 4 : produire le « manuel de préparation »

Appeler le skill docx pour générer un `interview_prep_<entreprise>_<poste>.docx` complet, structuré ainsi :

```
封面：公司 + 岗位 + 面试日期 + 倒计时
1. 公司 / 岗位 速览（1 页）
2. 自我介绍（中 + 英两版，针对该岗位定制）
3. 行为面题库（X 题）+ 参考回答
4. 技术面 / Case 面 题库（X 题）+ 参考思路
5. 反向提问清单（你向面试官问什么）
6. 薪资谈判脚本
7. 面试当天 Checklist（路线 / 着装 / 物品 / 心态）
```

**Produire aussi une version .md allégée**, pratique pour que l'utilisateur révise dans le métro / en chemin.

### Étape 5 : simulation d'entretien (optionnel - seulement à la demande de l'utilisateur)

Si l'utilisateur dit « simule un entretien », passer en mode interactif :
- une question à la fois
- attendre la réponse de l'utilisateur (voix / texte)
- donner un feedback sur trois dimensions : contenu / structure / expression
- si l'utilisateur dit « change de question » ou « encore une plus dure », continuer

Pendant la simulation, **rester dans le personnage d'intervieweur** : ton d'un vrai intervieweur, relances, points de pression (sans devenir agressif, rester constructif).

---

## Anti-patterns (à ne pas faire)

- ❌ Fournir une liste « 50 questions génériques » pour se débarrasser du sujet → il faut personnaliser selon l'entreprise / le poste
- ❌ Des réponses de référence remplies de phrases creuses comme « j'ai d'excellentes capacités de communication » → il faut des histoires concrètes
- ❌ Ne pas faire pratiquer l'utilisateur et répondre à sa place du début à la fin → on perd la valeur de la simulation
- ❌ Inventer des expériences que l'utilisateur n'a pas pour les histoires STAR → cela se verra pendant l'entretien
- ❌ Des réponses RH trop « formatées » (mécaniques) → fournir « 3 versions de styles différents » à choisir

## Collaboration avec les autres skills

- L'utilisateur dit « mon CV n'est pas assez fort, améliore-le d'abord » → transférer vers `jd-resume-tailor` ou `resume-builder`
- L'utilisateur dit « j'hésite encore à postuler » → transférer vers `job-intent-tracker`
- Après l'entretien, l'utilisateur dit « je veux faire un débrief » → rester dans ce skill, entrer en « mode débrief d'entretien », questionner sur la performance, les points de blocage, les relances, et aider l'utilisateur à se préparer pour le tour suivant
