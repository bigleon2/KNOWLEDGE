# Template canonique — Cahier des charges (12 sections)

> Compatibilité : skill `cahier-des-charges` v2.0.1 → v2.0.2 (résorption réserve S3 — élargissement de la description ; contenu de cette référence inchangé, R2).


> Skill cahier-des-charges v2.0.0 — template exécutable. À copier dans
> `download/cahier-des-charges-<projet>.md` puis à remplir section par section (M2).
> Les blocs `💡` sont des règles de rédaction : à lire, à appliquer, puis à SUPPRIMER du livrable.
> Les sections sans contenu réel sont marquées « à compléter en M1 » — jamais de texte creux (R3).
> Les annexes D (fiche domaine) et T (stratégie de vérification) s'activent en cycle Engineering
> Design complet (M5→M7) — en CDC seul (M1→M3), elles restent hors livrable.

---

# Cahier des charges — <Nom du projet>

> **Version** : 1.0.0 · **Statut** : BROUILLON → VALIDÉ → ÉVOLUÉ
> **Date** : AAAA-MM-JJ · **Rédigé par** : <agent/session> · **Validé par** : <propriétaire>
> **Domaine** : <primaire (+ secondaires) — détecté en M5, résumé en Annexe D> · **Profil SE** : <mini|standard|complexe — calibré en M5>
> **Sources** : <demande verbatim, discussion partagée, documents, décisions>

## 1. Contexte et problématique

<Situation actuelle, douleur constatée, opportunité. 2-4 paragraphes substantiels — le lecteur
qui ne connaît pas le projet doit comprendre POURQUOI il existe après cette section.>

💡 *Citer les faits et leurs sources. Marquer `[HYP-xx]` toute supposition non vérifiée avec sa
portée. Aucune solution ici — le contexte décrit le problème, pas la réponse.*

## 2. Objectifs et indicateurs de succès

| Objectif | Indicateur de succès | Cible mesurable |
|----------|---------------------|-----------------|
| O-1 : <objectif> | <ce qu'on mesure> | <seuil/valeur attendue> |

💡 *Un objectif sans indicateur mesurable est reformulé. 3 à 7 objectifs — au-delà, découper
le projet.*

## 3. Parties prenantes et rôles

| Partie | Rôle | Attendu / responsabilité |
|--------|------|--------------------------|
| <Propriétaire> | Demande et valide | <ce qu'il valide, ses critères> |
| <Utilisateurs> | Utilisent | <usage réel, volume, contraintes> |
| <Exécutants> | Réalisent | <périmètre d'exécution> |

## 4. Périmètre

**Inclus**
- <ce que le projet couvre — vérifiable>

**Exclus (explicite)**
- <ce que le projet ne fera PAS — écrit noir sur blanc>

💡 *Le périmètre exclu protège des dérives : toute demande hors périmètre en cours de projet
devient un amendement M4, jamais une absorption silencieuse.*

## 5. Exigences fonctionnelles (EF)

💡 *EF = ce que le système FAIT (fonction, comportement observable). Une exigence = un besoin
testable, pas de « et » logique. Chaque exigence porte sa source et son critère exécutable.*

| ID | Exigence | Source | Critère d'acceptation |
|----|----------|--------|----------------------|
| EF-01 | <capacité observable> | <demande/discussion/décision> | <check exécutable : commande, mesure, arbitre, seuil> |
| EF-02 | … | … | … |

## 6. Exigences non-fonctionnelles (ENF)

💡 *ENF = comment le système EST : performance, fiabilité, sécurité, maintenabilité,
utilisabilité, portabilité, conformité. Chiffrées (une ENF sans seuil est une intention).*

| ID | Exigence | Source | Critère d'acceptation |
|----|----------|--------|----------------------|
| ENF-01 | <qualité attribuable + seuil> | <source> | <mesure/seuil observable> |
| ENF-02 | … | … | … |

## 7. Contraintes

- **Techniques** : <imposées — techno, environnement, interopérabilité>
- **Réglementaires** : <lois, normes, conformité applicables>
- **Budgétaires** : <plafonds, coût cible>
- **Temporelles** : <échéances, fenêtres>

## 8. Livrables attendus

| Livrable | Nature / format | Critère de complétude |
|----------|----------------|----------------------|
| L-1 : <nom> | <document / code / application…> | <ce qui le rend complet — vérifiable> |

## 9. Jalons et planning indicatif

| Jalon | Contenu | Dépend de |
|-------|---------|-----------|
| J-1 : <nom> | <ce qui est livré> | <jalons préalables> |

💡 *Séquence et dépendances seulement — aucune date inventée ; les dates réelles viennent du
plan d'actions (gen-plan) ou du propriétaire.*

## 10. Critères d'acceptation

💡 *Recapitulatif mécanique — par lot si le projet s'exécute par groupes. Un critère
d'acceptation est une commande, une mesure ou un verdict d'arbitre ; à la réception d'un
livrable, le critère s'exécute et décide (correct-work mode CIBLE s'appuie sur cette table).*

| Lot / exigences | Critère | Vérification |
|-----------------|---------|--------------|
| EF-01…EF-xx | <check> | <commande / arbitre / mesure> |

## 11. Glossaire

| Terme | Définition |
|-------|------------|
| <terme du domaine> | <définition univoque> |

## 12. Annexes et sources

- **[S1]** <demande propriétaire — verbatim ou résumé fidèle, date>
- **[S2]** <discussion de cadrage — lien/chemin, date, points retenus>
- **[S3]** <documents, normes, décisions citées>

## Annexe D — Fiche domaine (résumé) — cycle Engineering Design (M5)

💡 *Résumé de `download/fiche-domaine-<projet>.md` — la fiche complète reste la source de vérité
du volet domaine et prévaut en cas d'écart. Activée en cycle complet (M5→M7) ; hors livrable en
CDC seul. Un domaine mixte déclare un PRIMAIRE (gouverne vocabulaire, normes, méthodes) et des
secondaires (règle 9). Toute norme citée ici est tracée à une source datée [Sx] — une norme sans
source est [HYP-xx] (règle 7).*

| Rubrique | Contenu |
|----------|---------|
| Domaine primaire | <domaine détecté — gouverne le vocabulaire, les normes, les méthodes> |
| Domaines secondaires | <domaines d'appoint — contraintes et glossaire additionnels> |
| Signaux de détection | <≥ 2 signaux lexicaux cités des sources du projet> |
| Normes citées | <normes du domaine — chacune tracée à sa source datée [Sx]> |
| Méthodes du métier | <méthodes de conception et de vérification retenues> |
| Doutes | [HYP-xx] <détection fragile, alternatives écartées> |

## Annexe T — Stratégie de vérification — cycle Engineering Design (M7)

💡 *Annonce contractuelle : quels lots de tests prouveront quoi. Les IDs TF-xx/TH-xx se figent
en P4-P5 (scaffold `scripts/scaffold_tests.py`). Au profil mini, une table simple exigence → test
suffit (règle 11). Chaque exigence est soit couverte par ≥ 1 test, soit déclarée NON VÉRIFIABLE
avec sa raison (règle 12) — jamais une couverture alléguée (R3).*

| Lot de tests | Prouve | Exigences visées | Nature |
|--------------|--------|------------------|--------|
| TF (fonctionnel) | <comportements exigés — assertions exécutables> | EF-…, ENF-… | assertions scriptées (`tests_fonctionnels/`) |
| TH (matériel simulé) | <sous-systèmes matériels — patrons `references/simulation-materielle.md`> | ENF-…, EF-… | simulation déterministe, graine fixe (`tests_materiel/`) |
| (non couvert) | — | EF/ENF-xx | NON VÉRIFIABLE : <raison assumée> |

---

## Amendements (M4 — à ne remplir que sur évolution)

| Date | Version | Section | Motif | Source |
|------|---------|---------|-------|--------|
| | | | | |

💡 *Règles M4 : jamais de modification silencieuse du corps — chaque évolution passe par une
ligne ici + bump de version (MAJOR = refonte du périmètre, MINOR = ajout/retrait d'exigences,
PATCH = correction éditoriale) + re-validation M3 des sections touchées. Un CDC existant fait
loi : l'évolution amende, elle ne réécrit pas (R2/R4).*
