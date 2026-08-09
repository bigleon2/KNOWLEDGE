# Détail des 15 étapes gen-plan

## E1 — Analyse de la demande

**Objectif** : Décortiquer la demande utilisateur pour en extraire les livrables, contraintes et critères de succès.

**Inputs** :
- Message ou demande brute de l'utilisateur
- Contexte de session (worklog, artefacts précédents)
- KNOWLEDGE.md (si disponible via KB)

**Outputs** :
- Liste des livrables identifiés
- Liste des contraintes (techniques, temporelles, ressources)
- Critères de succès explicites
- Questions clarificatoires (si ambiguïté)

**Critères de validation** :
- [ ] Au moins 1 livrable identifié
- [ ] Les contraintes sont explicites
- [ ] Le type de tâche est identifiable

**Exemple** :
> Demande : « Crée un rapport d'analyse des ventes du Q3 »
> Livrables : rapport.docx, graphiques PNG
> Contraintes : données Q3, format professionnel

---

## E2 — Inventaire des ressources

**Objectif** : Faire le bilan de tout ce qui est disponible pour accomplir la tâche.

**Inputs** :
- Sortie de E1 (livrables, contraintes)
- `{{SKILLS_ROOT}}` (liste des skills installés)
- `{{KB_PATH}}` (registre KB)
- Fichiers existants dans le projet

**Méthode — Lecture bloc par bloc** :
Pour chaque fichier > 500 lignes à inventorier :
1. Lire le premier bloc (200 lignes max)
2. Produire une synthèse intermédiaire (objectif, structure, sections clés)
3. Lire le bloc suivant (200 lignes max) en utilisant la synthèse comme contexte
4. Répéter jusqu'à la fin du fichier
5. Synthèse finale consolidée
Les fichiers ≤ 500 lignes sont lus en une seule fois.

**Outputs** :
- Liste des skills disponibles et pertinents
- Liste des fichiers/sources de données existants
- Synthèses intermédiaires des fichiers volumineux
- Gaps identifiés (ressources manquantes)

**Critères de validation** :
- [ ] Skills pertinents identifiés
- [ ] Gaps clairement listés
- [ ] Pas de ressource critique manquante sans contournement
- [ ] Fichiers > 500L lus par blocs avec synthèse intermédiaire

---

## E3 — Classification du type de tâche

**Objectif** : Router la tâche vers le bon type de traitement (Type 1-4).

**Inputs** :
- Sortie de E1 (livrables)
- Sortie de E2 (ressources)
- Grille de classification (voir classification-types.md)

**Outputs** :
- Type assigné (1, 2, 3 ou 4)
- Skill principal à invoquer
- Skills secondaires éventuels
- Mode par défaut (M1-M4)

**Critères de validation** :
- [ ] Exactement 1 type assigné
- [ ] Skill principal identifié
- [ ] Pas de conflit type/skill

---

## E4 — Estimation #token

**Objectif** : Calculer le budget token de la tâche.

**Inputs** :
- Type de tâche (E3)
- Complexité estimée (simple/moyenne/complexe)
- Profil ressource cible (E6, si connu)
- Grille #token (voir grille-token.md)

**Outputs** :
- Estimation #token totale
- Estimation par étape
- Tag #token pour chaque skill utilisé

**Critères de validation** :
- [ ] Estimation dans la plage du profil
- [ ] Tags #token présents sur chaque élément du plan

---

## E5 — Sélection des skills

**Objectif** : Identifier les skills pertinents pour la tâche.

**Inputs** :
- Type de tâche (E3)
- Ressources disponibles (E2)
- skills-inventory (scan)
- KNOWLEDGE.md (KB)

**Outputs** :
- Liste ordonnée des skills à utiliser
- Version minimale requise pour chaque skill
- Nature de l'utilisation de chaque skill

**Critères de validation** :
- [ ] Chaque skill cité existe dans le registre ou l'inventaire
- [ ] Versions minimales cohérentes
- [ ] Pas de doublon

---

## E6 — Profilage ressource

**Objectif** : Choisir le profil de ressource adapté.

**Inputs** :
- Estimation #token (E4)
- Complexité de la tâche
- Contraintes matérielles (si connues)
- Grille des profils (voir profils-ressource.md)

**Outputs** :
- Profil assigné (NORMAL/ECO/VIEUX PC)
- Justification du choix
- Restrictions activées (si profil réduit)

**Critères de validation** :
- [ ] 1 profil assigné
- [ ] Justification cohérente avec les inputs

---

## E7 — Création du plan

**Objectif** : Assembler le plan d'exécution structuré.

**Inputs** :
- Livrables (E1), Skills (E5), Profil (E6), #token (E4)

**Outputs** :
- Plan structuré : étapes, dépendances, checkpoints, #token par étape
- TODO list ordonnée
- Identification des étapes parallélisables

**Critères de validation** :
- [ ] Toutes les étapes E9-E14 couvertes
- [ ] Dépendances explicites
- [ ] Au moins 1 checkpoint
- [ ] #token total cohérent avec E4

---

## E8 — Validation du plan

**Objectif** : Vérifier cohérence, complétude et faisabilité.

**Inputs** :
- Plan brut (E7), Contraintes (E1)

**Outputs** :
- Plan validé (ou révisé)
- Liste des risques et plans de contournement

**Critères de validation** :
- [ ] Cohérence interne (pas de contradiction)
- [ ] Complétude (tous les livrables couverts)
- [ ] Faisabilité (ressources suffisantes)
- [ ] Pas de cycle dans les dépendances

---

## E9 — Lancement de l'exécution

**Objectif** : Démarrer l'exécution selon le plan validé.

**Inputs** : Plan validé (E8), Contexte session

**Méthode — Lecture bloc par bloc** :
Si les fichiers sources de l'étape E9 sont > 500 lignes, appliquer la méthode de lecture par blocs (voir E2) avant de démarrer l'exécution.

**Outputs** : Première étape lancée, Entrée worklog initialisée

**Critères** : [ ] Exécution démarrée, [ ] Worklog initialisé, [ ] Fichiers volumineux synthétisés par blocs

---

## E10 — Suivi d'étape

**Objectif** : Monitorer chaque étape en cours.

**Inputs** : Plan en cours (E8), État réel

**Méthode — Lecture bloc par bloc** :
Lors du suivi d'étapes manipulant des fichiers > 500 lignes, vérifier la cohérence bloc par bloc (ne pas relire le fichier intégralement, utiliser les synthèses produites à E2/E9).

**Outputs** : Entrée worklog par étape, #token réel, Écarts éventuels

**Critères** : [ ] Chaque étape terminée loggée, [ ] #token réel mesuré, [ ] Fichiers volumineux traités par synthèse de blocs

---

## E11 — Checkpoint intermédiaire

**Objectif** : Vérification à mi-parcours.

**Inputs** : Avancement (E10), Plan initial (E8)

**Outputs** : Bilan mi-parcours, Ajustements mineurs, Décision (continuer/ajuster/arrêter)

**Critères** : [ ] Checkpoint à ~50%, [ ] Décision documentée

---

## E12 — Détection d'écart

**Objectif** : Comparer réel vs estimé.

**Inputs** : #token estimé (E4), #token réel (E10)

**Outputs** : Tableau des écarts, Alertes si > 20%

**Critères** : [ ] Écarts calculés, [ ] Alertes si seuil dépassé

---

## E13 — Ajustement

**Objectif** : Modifier le plan en cas de dérive.

**Inputs** : Écarts (E12), Plan en cours (E8)

**Outputs** : Plan révisé (si nécessaire), Justification, Nouvelle estimation

**Critères** : [ ] Modifications justifiées, [ ] Plan révisé cohérent

---

## E14 — Finalisation

**Objectif** : Achèvement des étapes restantes.

**Inputs** : Plan (révisé ou non), État d'avancement

**Outputs** : Toutes les étapes terminées, Livrables finaux, Worklog complet

**Critères** : [ ] Tous les livrables produits, [ ] Worklog à jour

---

## E15 — Bilan et auto-calibration

**Objectif** : Retour d'expérience et mise à jour des grilles.

**Inputs** : Plan initial (E8), Worklog complet, #token estimé vs réel

**Outputs** :
- Bilan de la session
- Mise à jour grille #token (si écart > 20%)
- Enrichissement KNOWLEDGE.md (si `{{KB_ENABLED}}`)
- Déclenchement éventuel de clone-chat

**Critères** : [ ] Bilan produit, [ ] Calibration mise à jour si nécessaire, [ ] KNOWLEDGE.md enrichi si pertinent

---

## Portées étendues (E8, E14, E15)

Les étapes E8, E14 et E15 incluent des portées héritées des versions antérieures du protocole :

**E8 — Validation du plan** inclut aussi les vérifications de qualité pré-intégration :
- [ ] Chaque fichier candidat à l'intégration est classifié : Skill / Écosystème / Utilitaire
- [ ] Les fichiers Skill ont un YAML frontmatter valide (name, description, > 200 chars)
- [ ] Les scripts Python compilent (pas de syntax error, imports valides)
- [ ] Les fichiers Markdown sont structurés (titres, sections cohérentes, pas de contenu tronqué)
- [ ] Les fichiers de configuration (JSON/YAML) sont valides
- [ ] Les références croisées entre fichiers sont valides

**E8 — Hook correct-work** (si correct-work >= v2.4.0 est disponible) :
- [ ] Après validation du plan, lancer `correct-work(cibles, mode=CIBLE)` sur les livrables produits
- [ ] Si correct-work retourne FAIL, l'exécution est mise en pause jusqu'à correction
- [ ] Si correct-work retourne PASS AVEC RÉSERVES, les réserves sont loggées et l'exécution continue
- [ ] Si correct-work retourne PASS, l'exécution passe directement à E9

**E14 — Finalisation** inclut l'intégration écosystème :
- [ ] Les fichiers Skill sont placés dans `{{SKILLS_ROOT}}<nom>/SKILL.md`
- [ ] Les fichiers de référence vont dans `{{SKILLS_ROOT}}<nom>/references/`
- [ ] Aucun skill existant n'est écrasé sans confirmation utilisateur
- [ ] Le YAML frontmatter est conforme (SHARED §1.3)
- [ ] L'inventaire des skills est mis à jour si nécessaire

**E15 — Bilan** inclut l'auto-réapplication :
- [ ] Si le SKILL.md de gen-plan a été modifié pendant l'exécution, les tâches restantes sont réévaluées
- [ ] Les tâches affectées sont marquées `[REEVALUER]` avec la raison et les sections impactées
- [ ] Chaque réévaluation est documentée dans le worklog
