# PLAN D'ACTIONS W2 — discussion 28b4adb7 « Interprétation des pourcentages Winamax » — re-généré via gen-plan v3.23.1

> **Version du plan** : W2 | **Généré le** : 2026-10-16 | **Mode** : M1 (Planification) → exécution suite immédiate (clause mode NULL)
> **Provenance** : re-génération conforme à la **règle d'or n°2 §1.5** — écosystème réinstallé certifié (worklog local Task 1 : 3/3 arbitres verts) → plan d'actions de la discussion partagée `https://chat.z.ai/s/28b4adb7-2d2a-4122-b580-ee71ca4ae4aa` re-généré via gen-plan v3.23.1 installée ; objectif final inchangé, **R2 non-régression** : étapes T1-T2 terminées dans la discussion source sont conservées telles quelles (jamais réécriture destructrice).
> **Source de vérité** : rendu SPA headless de la discussion (agent-browser, capture `upload/discussion-28b4adb7-texte.txt`) — contenu reconstitué intégralement (demande, cahier des charges verrouillé, todos 7).
> **Auto-suffisance** : ce plan est auto-portant — tout tour peut reprendre sans contexte hérité (bloc REPRISE en fin de plan).
> **Cohérence** : ce plan W2 est référencé par le plan de session W1 (Tâche B) ; il en est le plan d'exécution opérationnel.

---

## E1 — Analyse de la demande (hook answer key)

| Objet | Contenu | Traçabilité |
|-------|---------|-------------|
| (a) Demande source | « poker Winamax : 3 pourcentages affichés au-dessus de l'avatar d'un adversaire — que représentent ces chiffres, comment les interpréter, peut-on les calculer, comment s'en servir pour calculer les cotes ? **Génére des fiches illustrées en version PDF, explicite et illustrée, donne-moi 5 exemples et 10 exercices illustrés de cas d'usage** » | discussion 28b4adb7, message 1 |
| (b) Cahier des charges verrouillé | Fiches approfondies **30+ pages** · niveau **intermédiaire** · **cash game + tournoi** · style **tech moderne (bleu nuit + cyan)** · **corrigés intégrés** · illustration par **HUD simulé en CSS** · **4 modules** : ranges, cotes & équité, calcul des stats, plan d'action | discussion 28b4adb7 — confirmation AskUserQuestion « cahier des charges verrouillé » |
| (c) Réponse factuelle verrouillée | Les 3 chiffres au-dessus de l'avatar = **VPIP** (% de mains jouées volontairement), **PFR** (% de relances pré-flop), **Agressivité (AF)** — 3 formats d'affichage possibles documentés ; concepts confirmés par recherche web (sources poker d'autorité) | todos T1 de la discussion (FAITE) |
| (d) Choix techniques verrouillés | Skill PDF plateforme, **Template 07 « Crystal Blue »** (couverture bleu nuit + accents cyan, corps clair même famille de teinte) ; convertisseur **html2pdf-next.js** (Paged.js, pages nommées `@page`, fond propagé chaque page, `preferCSSPageSize`) ; validation `poster_validate.py check-html` ; QA `pdf_qa.py` ; numérotation `pypdf` | todos T2 de la discussion (FAITE — tous fichiers référencés lus) |
| (e) Objectif final | Livrable PDF vectoriel complet dans `download/` (couverture + fiches 3 stats + 4 modules + 5 exemples + 10 exercices corrigés + HUD simulés), QA PASS, numérotation + métadonnées | directive maîtresse de la discussion |

Décisions vérifiables : capture texte `upload/discussion-28b4adb7-texte.txt` (D-W2-1 : cahier des charges ; D-W2-2 : 7 todos avec statuts ; D-W2-3 : template et convertisseur choisis).

## E2 — Inventaire des ressources

- **Contenu factuel** : VPIP/PFR/AF confirmés (T1 ✅) — définitions, interprétation, plages de référence, formats d'affichage Winamax.
- **Choix design** : Template 07 « Crystal Blue » du skill pdf (T2 ✅) — palette bleu nuit + cyan, typographie et brief creative-flow déjà analysés dans la discussion source.
- **Pipeline technique** : HTML complet → `poster_validate.py check-html` → `html2pdf-next.js` (Paged.js) → `pdf_qa.py` → numérotation pypdf + métadonnées → `download/`.
- **Illustrations** : HUD simulé en CSS (panneau 3 chiffres au-dessus d'un avatar), graphiques (plages VPIP/PFR, tableau AF, courbes d'équité).
- **Écosystème local certifié** : gen-plan v3.23.1 (méthode), correct-work v2.7.0 (hooks par phase), worklog partagé.
- **Réutilisation plateforme** : avant toute génération, vérifier les assets existants de `/home/z/my-project/download/` (règle de réutilisation des assets).

## E3 — Classification

**Type 1** (création de document — PDF) : livrable fiches PDF vectorielles illustrées ; aucun développement web (le HTML n'est qu'un étage du pipeline PDF). Déclencheur de skill : `pdf` (voie Creative — HTML/Blueprint → convertisseur Paged.js).

## E4 — Estimation #token

| Phase | Objet | Estimation |
|-------|-------|-----------|
| T1 | ✅ FAITE (discussion source) — vérification factuelle VPIP/PFR/AF | 0 (restant) |
| T2 | ✅ FAITE (discussion source) — lecture intégrale skill PDF + convertisseur | 0 (restant) |
| T3 | Outline détaillé du document (couverture, sommaire, fiches, modules, exemples, exercices) | ~1000 #token |
| T4 | Génération HTML complet (30+ pages : couverture + 3 fiches stats + 4 modules + 5 exemples + 10 exercices corrigés + HUD CSS) | ~12000 #token |
| T5 | Validation HTML (poster_validate.py check-html) + corrections | ~1500 #token |
| T6 | Conversion PDF vectoriel (html2pdf-next.js) + QA (pdf_qa.py) + corrections éventuelles | ~2000 #token |
| T7 | Numérotation pypdf + métadonnées + livraison download/ + worklog | ~1000 #token |
| Maintenance | worklog par tour | ~500 #token/tour |

## E5 — Sélection des skills

| Skill | Usage | Version plancher |
|-------|-------|-----------------|
| pdf (plateforme) | Génération fiches PDF — voie Creative (Template 07 Crystal Blue, html2pdf-next.js, poster_validate, pdf_qa) | courante |
| gen-plan | Méthode E1-E15, règles d'or, clause mode NULL | 3.23.1 |
| correct-work | Hooks par phase + E8 (vérification livrable final) | 2.7.0 |
| worklog partagé | Journalisation (règle d'or n°2 : régénérations journalisées) | convention SHARED §1.4 |
| resource-monitor (G-RES) | Collecte R-RES1 en continu — NORMAL | 1.0.0 |

## E6 — Profilage ressource

**NORMAL** — signaux de pression : aucun (disque OK, 0 timeout consécutif, budget < 80 %). **G-RES active** : collecte à l'ouverture/fermeture de chaque phase (R-RES1) ; adaptation en cascade au blocage (R-RES3) ; mise à jour optimisée du plan via gen-plan si structurel (R-RES4) ; objectif final intangible (R-RES5).

---

## E7 — LE PLAN (phases restantes)

> Philosophie : exécution série par défaut (§1.4 #4). Toute phase terminée → hook correct-work (§5.4). Idempotence R1-R6 sur chaque écriture. G-RES sur toutes les phases. **Le cahier des charges étant épinglé (audience + style + longueur explicites dans la discussion source), aucune re-clarification n'est requise — exécution directe.**

### T1-T2 — ✅ FAITES (discussion source 28b4adb7)

- T1 ✅ Vérification factuelle des 3 stats Winamax : **VPIP** (% mains jouées volontairement), **PFR** (% relances pré-flop), **Agressivité AF** — recherche web (VPIP/PFR sources d'autorité ; interface Winamax affiche « mains jouées / relances pré-flop / agressivité ») + connaissance client Winamax (3 formats d'affichage possibles documentés).
- T2 ✅ Lecture intégrale du skill PDF : brief creative-flow + fonts + typesetting + palette + cover + pagination + typographie + charts + cover-backgrounds + fill-engine + geometry ; Template 07 « Crystal Blue » identifié ; comportement convertisseur `html2pdf-next.js` analysé (Paged.js, pages nommées `@page`, fond propagé, `preferCSSPageSize`).

### T3 — Outline détaillé du document — ✅ FAITE (2026-10-16 : Outline 14 sections validé via outil dédié)

1. Charger le skill `pdf` plateforme et confirmer les gabarits (Template 07 « Crystal Blue »).
2. Construire l'outline : couverture (titre, sous-titre, visuel HUD) → sommaire → partie 1 : les 3 chiffres de l'avatar (VPIP, PFR, AF — définition, lecture, formats d'affichage) → partie 2 : module ranges → partie 3 : module cotes & équité → partie 4 : module calcul des stats (formules, exemples de calcul) → partie 5 : module plan d'action (tableaux de décision) → 5 exemples commentés avec HUD simulés → 10 exercices illustrés + corrigés intégrés → annexe : glossaire et plages de référence.
3. Chaque fiche stat : définition formelle + formule + tableau d'interprétation par plage + HUD simulé + cas cash game et tournoi.
4. Validation de l'outline avant génération (cohérence 30+ pages, répartition modules/exemples/exercices).

### T4 — Génération du HTML complet — ✅ FAITE (2026-10-16 : HTML Template 07 Crystal Blue, assemblé depuis scripts/pdf-parts/, ~800 lignes)

1. Vérifier les assets existants de `download/` (réutilisation, règle asset-reuse).
2. Générer le HTML complet stylé Template 07 « Crystal Blue » : couverture bleu nuit + cyan, corps clair ; HUD simulés en CSS (avatar + panneau 3 chiffres) ; tableaux d'interprétation ; formules ; graphiques.
3. Contenu conforme au cahier des charges : 30+ pages, niveau intermédiaire, cash game + tournoi, corrigés intégrés, 5 exemples, 10 exercices illustrés.
4. Respect des conventions typographiques du skill (fonts, overflow, pagination, geometry — fichiers déjà analysés en T2).

### T5 — Validation HTML — ✅ FAITE (2026-10-16 : poster_validate corrigé micro-polices + glows background ; couverture isolée cover_validate 0 collision)

1. Exécuter `poster_validate.py check-html` sur le HTML généré.
2. Corriger tout écart (débordements, polices non déclarées, structure de pages nommées) ; itérer jusqu'à PASS.

### T6 — Conversion PDF + QA — ✅ FAITE (2026-10-16 : html2pdf-next.js Paged.js, 32 pages après enrichissements, pdf_qa.py --no-tables PASS all checks)

1. Convertir via `html2pdf-next.js` (Paged.js, `preferCSSPageSize`, fond propagé chaque page) → PDF vectoriel.
2. Exécuter `pdf_qa.py` : contrôle pages, débordements, polices embarquées ; corriger et reconvertir si FAIL.

### T7 — Finalisation + livraison — ✅ FAITE (2026-10-16 : numérotation pypdf 1..31 couverture cachée, métadonnées, 0 U+FFFD, livrés download/fiches-winamax-hud-vpip-pfr-af.pdf + .html)

1. Numérotation des pages (pypdf) + métadonnées (titre, auteur, sujet).
2. Livraison dans `/home/z/my-project/download/` (nom descriptif) + worklog partagé (section dédiée) + rapport à l'utilisateur.
3. Hook E8 : correct-work(mode CIBLE) sur le livrable — verdict requis PASS (fichier non vide, ouverture OK, pagination conforme).

---

## E8 — Validation du plan

- **Cohérence cahier des charges** : chaque exigence verrouillée (30+ pages, intermédiaire, cash game + tournoi, bleu nuit + cyan, corrigés, HUD simulés, 4 modules, 5 exemples, 10 exercices) est mappée à une phase T3-T4 — tracée dans E1(b) et E7.
- **Non-régression R2** : T1-T2 conservées avec leurs conclusions (aucune re-exécution).
- **Hook correct-work par phase** : T4-T5 → vérification après génération/validations ; T7 → correct-work(mode CIBLE) final.
- **Critères de passage livrable** : `poster_validate` PASS, `pdf_qa` PASS, pypdf numérotation présente, fichier livré dans `download/`, worklog journalisé.

## Bloc REPRISE W2 (auto-suffisant)

Au prochain « continue » (ordre de priorité, clause mode NULL — sans portes de confirmation) :
1. **T3** — charger skill `pdf`, construire l'outline détaillé du document (point de reprise exact de la discussion source).
2. **T4** — générer le HTML complet (Template 07 Crystal Blue, HUD simulés, 30+ pages).
3. **T5-T6** — valider (`poster_validate.py check-html`) puis convertir + QA (`html2pdf-next.js`, `pdf_qa.py`).
4. **T7** — numérotation pypdf + métadonnées + livraison `download/` + worklog + correct-work final.
5. Reporter le statut dans le plan de session W1 (Tâche B) et le worklog partagé.
