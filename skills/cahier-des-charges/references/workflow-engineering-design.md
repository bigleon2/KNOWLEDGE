# Workflow Engineering Design — pipeline 5 phases et V-cycle adaptatif

> Compatibilité : skill `cahier-des-charges` v2.0.1 → v2.0.2 (résorption réserve S3 — élargissement de la description ; contenu de cette référence inchangé, R2).


> Skill cahier-des-charges v2.0.0 — reference exécutable du cycle complet (M5 → M7).
> Posture : **Ingénieur Concepteur en System Engineering expert du domaine technique détecté**.
> Chaque phase a des entrées, une méthode, des sorties et un critère de passage — un passage sans
> critère satisfait est un passage en dette, jamais un passage silencieux (R3).

## §1 — Vue d'ensemble : les 5 phases

```text
P1 ANALYSE (M5)      → fiche-domaine-<projet>.md + calibration SE
P2 CDC (M1→M2→M3)    → cahier-des-charges-<projet>.md (+ .pdf) VALIDÉ
P3 CONCEPTION (M6)   → dossier-conception-<projet>.md
P4 TESTS FONCTIONNELS (M7) → batterie-tests-<projet>/tests_fonctionnels/ + verdicts
P5 TESTS MATÉRIELS (M7)    → batterie-tests-<projet>/tests_materiel/ + verdicts
                     → rapport-couverture-<projet>.md (matrice exigences ↔ tests)
```

Le V-cycle sous-jacent : les exigences (bras gauche, P2) se décomposent en sous-systèmes (P3)
puis s'assemblent ; les tests (bras droit, P4-P5) remontent la décomposition — test d'un
sous-système (TH-xx), test d'exigence intégrée (TF-xx) — jusqu'à la recette du système entier.
La matrice exigences ↔ conception ↔ tests EST le V-cycle rendu vérifiable.

**Phase à exécuter selon la demande** : CDC seul → P1 (allégée) + P2 ; cycle complet → P1→P5 ;
conception seule → P3 (CDC préalable requis) ; tests seuls → P4-P5 (CDC + conception requis).

## §2 — P1 ANALYSE (M5) : compiler, détecter, instruire, calibrer

1. **Compiler les informations du projet** — sources acceptées : lien partagé (extraction via
   web-reader), fichiers joints (lecture directe), discussion de cadrage, documents du dépôt.
   Consigner chaque source avec sa date. Les lacunes (information manquante pour cadrer) sont
   listées explicitement dans la fiche domaine — elles ne sont pas devinées.
2. **Détecter le domaine technique** — grille de détection `references/domaines-techniques.md` :
   signaux lexicaux du projet → domaine primaire (gouverne le vocabulaire, les normes, les
   méthodes) + domaines secondaires. La détection est automatique : ne pas bloquer sur une
   confirmation du propriétaire ; consigner les signaux et les doutes `[HYP-xx]`.
3. **Instruire le domaine par recherche web** — requêtes types par domaine dans
   `references/domaines-techniques.md` ; cibler : normes applicables, méthodes de conception du
   métier, état de l'art des solutions analogues, glossaire technique. Retenir 3 à 8 sources,
   chacune datée et citée. Une information web non vérifiée est marquée `[HYP-xx]`.
4. **Calibrer la rigueur SE** — grille §3 ci-dessous → profil mini/standard/complexe, AFFICHÉ
   dans le compte-rendu de phase (le propriétaire peut le corriger ; sa correction relance P1).
5. **Livrer** `download/fiche-domaine-<projet>.md` (structure §5).

**Critère de passage P1 → P2** : domaine primaire identifié avec ≥ 2 signaux convergents ;
≥ 3 sources web datées ; profil calibré et affiché ; lacunes listées.

## §3 — Grille de calibration (rigueur SE adaptative)

Scorer le projet sur les 6 critères (0, 1 ou 2 points chacun) — le total donne le profil.

| Critère | 0 point | 1 point | 2 points |
|---------|---------|---------|----------|
| Nombre de sous-systèmes attendus | ≤ 2 | 3-5 | ≥ 6 |
| Interfaces inter-sous-systèmes | ≤ 2 | 3-6 | ≥ 7 |
| Sécurité / réglementation (personne, bien, conformité) | néant | induite | critique/explicite |
| Exigences non-fonctionnelles chiffrées attendues | ≤ 3 | 4-10 | > 10 |
| Hétérogénéité technique (SW + HW + physique + humain) | une seule famille | deux familles | ≥ 3 familles |
| Recrudescence d'erreur tolérable (impact d'une défaillance) | anodine | dégradante | critique |

| Total | Profil | Conséquences sur le cycle |
|-------|--------|---------------------------|
| 0-3 | **mini** | Traçabilité simple (exigence → test) ; conception : 1 niveau (sous-systèmes + interfaces dans un tableau) ; tests : TF sur les exigences critiques + 1 TH représentatif |
| 4-7 | **standard** | Matrice exigences ↔ conception ↔ tests par lot ; conception : SS-xx détaillés + I-xx contractuelles ; tests : TF exhaustifs + TH par sous-système matériel |
| 8-12 | **complexe** | Matrice bidirectionnelle complète + revues de phase tracées ; conception : architecture à 2 niveaux + allocation chiffrée + analyse des risques formelle (FMEA allégée) ; tests : TF exhaustifs + TH par sous-système ET par interface + campagne de robustesse (bruit, tolérances) |

Le profil peut être FORCÉ par le propriétaire (ex : un projet simple à enjeux critiques → complexe).
Le profil forcé est consigné dans l'en-tête du CDC.

## §4 — P2 CDC (M1→M2→M3) : le contrat, enrichi du domaine

Le CDC suit la structure canonique 12 sections (§1.3 du SKILL.md) — l'enrichissement domaine se
fait EN PLACE, sans nouvelle structure :

- **Glossaire (§11)** : les termes métier du domaine détecté, avec unités SI.
- **Contraintes (§7)** : normes du domaine citées nommément (source datée de la fiche domaine).
- **ENF (§6)** : chiffrées à l'aune des pratiques du domaine (un seuil sans référentiel métier
  est marqué `[HYP-xx]`).
- **Annexe D** (template) : résumé de la fiche domaine (domaine, signaux, normes, sources).
- **Annexe T** (template) : stratégie de vérification annoncée (quels lots de tests prouveront quoi).

M3 VALIDER s'applique sans changement : grille 12 sections, critères exécutables, cohérence
interne. Statut VALIDÉ requis avant P3 (ou validation propriétaire explicite en BROUILLON).

## §5 — Fiche domaine (livrable P1) — structure imposée

```markdown
# Fiche domaine — <projet>
> Version X.Y.Z · Date AAAA-MM-JJ · Sources : <n sources datées>

## 1. Informations compilées du projet
<faits, chiffres, objectifs extraits des sources — chacun tracé à sa source>

## 2. Détection du domaine
| Domaine | Statut | Signaux lexicaux observés |
|---------|--------|---------------------------|
| <primaire> | PRIMAIRE | <≥ 2 signaux, cités du projet> |
| <secondaire> | SECONDAIRE | <signaux> |
> Doutes et alternatives écartées : [HYP-xx] …

## 3. Normes et méthodes du domaine (web daté)
| Référence | Ce qu'elle impose | Source (URL, date de consultation) |
|-----------|-------------------|-------------------------------------|

## 4. État de l'art des solutions analogues
<2-4 solutions existantes : ce qu'elles font, ce qu'elles impliquent en exigences>

## 5. Glossaire métier et unités
| Terme | Définition | Unité |
|-------|-----------|-------|

## 6. Calibration SE
Score 6 critères : <table §3 remplie> → profil <mini|standard|complexe> (+ forcé/non forcé)

## 7. Lacunes à combler par le propriétaire
<littérature manquante, décisions requises>
```

## §6 — P3 CONCEPTION (M6) : le dossier de conception — structure imposée

```markdown
# Dossier de conception — <projet>
> Version X.Y.Z · Date · CDC d'entrée : cahier-des-charges-<projet>.md vX (VALIDÉ) · Domaine : <d>

## 1. Architecture système
<vue d'ensemble en 2-4 paragraphes + diagramme mermaid (flowchart) des sous-systèmes et flux>

## 2. Sous-systèmes (SS-xx)
| ID | Sous-système | Rôle | Exigences allouées | Contraintes d'implémentation |
|----|--------------|------|--------------------|------------------------------|
| SS-01 | … | … | EF-01, EF-03, ENF-02 | <techno/env imposés ou choisis, justifiés §5> |

## 3. Interfaces (I-xx)
| ID | Entre | Nature | Contrat (format, cadence, tolérance, protocole) |
|----|-------|--------|--------------------------------------------------|
| I-01 | SS-01 ↔ SS-02 | <signal/flux/protocole> | <contrat vérifiable> |

## 4. Allocation des exigences
<matrice EF/ENF → SS (chaque exigence allouée à ≥ 1 sous-système ; toute exigence non allouée
est un trou de conception — la compléter ou remonter un amendement M4 du CDC)>

## 5. Choix techniques justifiés
| Décision | Options considérées | Option retenue | Justification (domaine, normes, coûts) |
|----------|--------------------|-----------------|----------------------------------------|

## 6. Risques de conception
| Risque | Sous-système | Impact | Parade (conception et/ou test TH/TF) |
|--------|--------------|--------|--------------------------------------|

## 7. Traçabilité exigences ↔ conception ↔ tests (profil standard/complexe)
<matrice par lot : EF/ENF → SS → TF/TH prévus (les IDs TF/TH se figent en P4-P5)>

## 8. Annexes (diagrammes détaillés, calculs dimensionnants)
<calculs au niveau du domaine : dimensionnement, bilans de puissance, budgets de latence…>
```

Règles de conception : chaque choix porte sa justification AU regard du domaine (pas de techno
« par défaut » non justifiée) ; les calculs dimensionnants sont faits, pas évoqués ; les
diagrammes sont en mermaid (dans le Markdown) ; cohérence obligatoire avec le CDC — un écart
constaté (exigence impossible, contradictoire, incomplète) remonte en amendement M4 AVANT d'être
contourné en silence.

## §7 — P4/P5 TESTS (M7) : batteries, exécution, couverture

1. **Scaffold** — `python3 {{SKILLS_ROOT}}cahier-des-charges/scripts/scaffold_tests.py --projet <slug>
   --out <download> [--exigences EF-01,EF-02,…] [--th N] [--profil mini|standard|complexe]` : crée
   `batterie-tests-<projet>/` (squelettes `tf_01_*.py`, `th_01_*.py`, `run_all.py`, `journal/`,
   `matrice-couverture.md` pré-remplie). Idempotent ×2 — re-scaffold sans changement = bytes
   identiques ; un fichier existant n'est JAMAIS écrasé (les tests implémentés sont conservés).
   Protocole STATUT : chaque squelette porte `STATUT = "NON_IMPLÉMENTÉ"` — `run_all.py` ne
   l'exécute pas tant que l'implémentation ne l'a pas passé à `"PRÊT"` (un squelette ne prouve
   rien, R3 ; code sortie run_all : 0 tout PASS · 1 ≥ 1 ECHEC · 2 ≥ 1 NON_IMPLÉMENTÉ · 3 vide).
2. **Implémenter** les squelettes : un TF-xx par exigence prioritaire (assertions sur les
   comportements exigés), un TH-xx par sous-système matériel — patrons physiques imposés de
   `references/simulation-materielle.md` (modèle discret, capteurs virtuels, actionneurs saturés,
   PID), déterministes (graine fixe), stdlib uniquement.
3. **Exécuter** `run_all.py` — verdict mécanique par test, journal JSON horodaté dans `journal/`.
4. **Corriger** les échecs : échec de test → correction du système conçu (dossier de conception
   amendé) ; échec révélant une exigence fausse/irréaliste → amendement M4 du CDC AVANT
   correction du test — jamais l'inverse (workflow inversé SDD).
5. **Rapporter** `download/rapport-couverture-<projet>.md` :
   - matrice exigences ↔ tests avec verdict (PASS/ÉCHEC/NON VÉRIFIABLE + raison) ;
   - couverture chiffrée : % d'exigences couvertes par ≥ 1 test PASS (cible : 100 % au profil
     standard/complexe, ≥ exigences critiques au profil mini) ;
   - recommandations (tests à ajouter, tolérances à durcir, hypothèses à lever).

**Critère de passage P4/P5 → fin** : tous les tests exécutables ont un verdict mécanique ;
aucune couverture alléguée ; les NON VÉRIFIABLES sont justifiés et assumés (R3).

## §8 — Boucle de retour (V-cycle vivant)

- Échec TH → parade de conception → re-exécution (idempotence : même graine, verdict reproductible).
- Exigence irréaliste → M4 amendement CDC (version bumpée) → allocation et tests mis à jour.
- Périmètre qui dérive en cours de route → hors périmètre : passer par M4, jamais d'absorption silencieuse.
- Tout re-passsage de phase reprend SEULEMENT les éléments impactés (traçabilité = carte d'impact).
