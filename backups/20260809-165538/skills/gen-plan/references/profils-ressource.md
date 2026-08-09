# Profils ressource — gen-plan v3.6.1

## NORMAL

**Contexte** : Ressources standards, sans contrainte.
**Déclenchement** : Par défaut.

**Règles** :
- 15 étapes exécutées
- Tous les skills disponibles
- Surveillance complète (E10-E12)
- Snippets complets et versionnés
- Graphiques et visuels autorisés

**Seuils** : #token sans plafond, E10+E11+E12 obligatoires.

---

## ECO

**Contexte** : Discussion courte ou tâche simple.

**Déclenchement** :
- Discussion < 5 sessions
- #token estimé < 3500
- Tâche simple (1 skill, 1 livrable)
- Demande explicite de l'utilisateur
- **1 signal de pression** détecté (§2.4.1 du SKILL.md)

**Règles** :
- Étapes réduites : E1-E9 puis E14-E15 (E10-E13 fusionnées)
- Snippets simplifiés (pas de versionnage)
- 1 checkpoint unique à E11
- Pas de matrice dynamique KB (statique seulement)
- Sous-tâches > 8000 #token exclues du plan (filtrage E4)

**Restrictions** :
- Pas de rapport de vérification détaillé
- Auto-calibration E15 simplifiée (ajustement seulement si > 35%)
- Pas de déclenchement clone-chat automatique

---

## VIEUX PC

**Contexte** : Environnement matériel limité.

**Déclenchement** :
- Demande explicite de l'utilisateur
- Environnement détecté comme limité
- **2+ signaux de pression** ou **1 signal critique** (§2.4.1 du SKILL.md)

**Règles ECO** : toutes les règles ECO s'appliquent (filtrage > 5000 #token).

**5 règles supplémentaires** :

1. **Dépendances séquentielles uniquement** — Pas de parallélisme. Chaque étape doit être terminée avant de commencer la suivante.
2. **Choix agent/skill justifié par le coût** — Toujours choisir l'agent ou le skill le moins cher qui suffit pour la tâche. Justifier le choix dans le plan.
3. **Budget ressource par phase** — Le budget #token est alloué par phase (E1-E8, E9-E14, E15), jamais global. Si une phase dépasse son budget, les étapes restantes sont reportées.
4. **Actions d'économie explicites** — Résumé de contexte avant chaque étape majeure, troncature des fichiers > 500 lignes, pas de relecture intégrale.
5. **Plan de contingence** — Si le profil se dégrade encore (3+ signaux critiques), basculer en mode survie : seules les étapes E1, E3, E7, E14 sont exécutées.

**Restrictions supplémentaires** :
- Pas de génération d'images
- Scripts < 100 lignes
- Préférer O(n) à O(n²)
- Pas de chargement de gros fichiers en mémoire
- Scripts Python légers uniquement (pas de bibliothèques lourdes)
- Pas de graphiques Matplotlib/Seaborn
- Pas de Playwright
- Préférer les sorties Markdown/texte

**Seuils** : #token plafond 2000, pas de graphiques.

---

## Règle de downgrade irréversible

Le profil ne remonte jamais automatiquement au cours d'une session :
- NORMAL → ECO : définitif pour la session
- ECO → VIEUX PC : définitif pour la session
- NORMAL → VIEUX PC : définitif pour la session

Le profil initial est NORMAL sauf détection de signaux de pression dès E2.
