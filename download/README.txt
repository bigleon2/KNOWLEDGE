===============================================================================
         PROMPTS MAÎTRES — Écosystème Knowledge
         Architecture en 3 fichiers + workflow
===============================================================================

Date      : 2026-08-09
Version   : 1.0.0
Vérif.    : 54/54 checks PASS (voir scripts/verify-cross.py)


===============================================================================
1. FICHIERS
===============================================================================

  PROMPT-MAITRE-SHARED.md              (~214 lignes)
    Socle commun de l'écosystème. Contient tout ce qui est partagé entre
    les skills : contexte, conventions, variables d'installation, registre
    KB, relations inter-skills, matrice agent x skill.

  PROMPT-MAITRE-GEN-PLAN-v3.6.0.md     (~766 lignes)
    Spécification complète du skill gen-plan v3.6.0. Contient la spec
    fonctionnelle (4 modes, 15 étapes E1-E15, normes N1-N3), la spec
    technique (stack, auto-calibration, profils, KB), le YAML frontmatter,
    les instructions d'installation, et le contenu in extenso des 4
    fichiers référence (étapes, grille #token, classification Type 1-4,
    profils ressource).

  PROMPT-MAITRE-CORRECT-WORK-v2.3.0.md  (~418 lignes)
    Spécification complète du skill correct-work v2.3.0. Contient la spec
    fonctionnelle (3 modes, 5 étapes, sévérité S1-S4), la spec technique
    (rapport, matrices statique/dynamique, logging), le YAML frontmatter,
    les instructions d'installation, l'historique des corrections clone-chat
    (3 rounds), et les checklists détaillées pour le SKILL.md.


===============================================================================
2. PRINCIPE D'ARCHITECTURE
===============================================================================

  SHARED est le "socle". Les deux autres fichiers sont les "spécifiques".

  Avant le refactoring (v1), chaque prompt maître dupliquait ~15-20% de
  contenu identique (contexte écosystème, conventions, variables, relations,
  matrice agent x skill). En cas de modification d'une info commune, il
  fallait la reporter dans chaque fichier.

  Après le refactoring (v2) :
  - L'info commune est centralisée dans SHARED (§0 à §6)
  - Les fichiers spécifiques contiennent uniquement la logique propre
    à leur skill et font référence à SHARED via des renvois (ex : "voir
    SHARED §1.2")
  - Toute mise à jour d'une info commune se fait UNE SEULE FOIS

  Réduction mesurée : -92 lignes (6.2%), mais surtout une maintenance
  simplifiée et un risque d'incohérence réduit.


===============================================================================
3. STRUCTURE DE CHAQUE FICHIER
===============================================================================

  SHARED.md
    §0 — Règle zéro (contexte écosystème, principes fondamentaux)
    §1 — Conventions écosystème
        §1.1 Variables d'installation ({{SKILLS_ROOT}}, {{KB_PATH}}, etc.)
        §1.2 Conventions de nommage (kebab-case, semver, tags)
        §1.3 Conventions YAML frontmatter (template minimum)
        §1.4 Format worklog (format partagé)
    §2 — Registre KB (KNOWLEDGE.md)
        §2.1 Rôle
        §2.2 Format d'une entrée (template)
        §2.3 Protocole de Découverte
    §3 — Registre des relations inter-skills
        §3.1 Tableau complet des relations
        §3.2 Règles de cross-references
    §4 — Matrice agent x skill (statique)
        §4.1 Matrice principale
        §4.2 Légende des droits
    §5 — Format du fichier SKILL.md (conventions structurelles)
    §6 — Prompt maîtres : architecture et workflow

  GEN-PLAN v3.6.0.md
    PRÉREQUIS (référence SHARED)
    §1 — Spécification fonctionnelle (4 modes, 15 étapes, N1-N3)
    §2 — Spécification technique (stack, auto-calibration, profils, KB)
    §3 — Relations (extrait SHARED §3.1)
    §4 — YAML frontmatter
    §5 — Instructions d'installation
    §6 — Vérification post-installation (9 checks)
    §7 — Historique des versions
    §8 — Notes de conception
    §9 — Contenu in extenso des 4 fichiers référence

  CORRECT-WORK v2.3.0.md
    PRÉREQUIS (référence SHARED)
    §1 — Spécification fonctionnelle (3 modes, 5 étapes, KB)
    §2 — Spécification technique (rapport, matrices, sévérité S1-S4)
    §3 — Relations (extrait SHARED §3.1)
    §4 — YAML frontmatter
    §5 — Instructions d'installation
    §6 — Vérification post-installation (16 checks)
    §7 — Historique des versions
    §8 — Historique des corrections clone-chat (3 rounds)
    §9 — Notes de conception
    §10 — Checklists pour le SKILL.md


===============================================================================
4. WORKFLOW D'UTILISATION
===============================================================================

  CAS A — Installer un skill depuis zéro
  --------------------------------------
  1. Lire PROMPT-MAITRE-SHARED.md en premier
  2. Lire le prompt maître du skill cible (gen-plan ou correct-work)
  3. Suivre les "Instructions d'installation" (§5 du fichier spécifique)
  4. Créer la structure de répertoires
  5. Créer le fichier SKILL.md en assemblant :
     - Le YAML frontmatter (§4)
     - La règle zéro (SHARED §0, adaptée en résumé)
     - La spec fonctionnelle et technique (§1-§2)
     - Les relations (§3 + SHARED §3)
     - Les sections spécifiques (checklists, grilles, etc.)
  6. Créer les fichiers de référence (si applicable, §9 in extenso)
  7. Exécuter les checks de vérification post-installation
  8. Mettre à jour KNOWLEDGE.md (SHARED §2.2 template)
  9. Mettre à jour les cross-references (SHARED §3.2)

  CAS B — Mettre à jour une info commune
  --------------------------------------
  1. Modifier l'info dans PROMPT-MAITRE-SHARED.md (une seule fois)
  2. Vérifier que les références dans les fichiers spécifiques pointent
     toujours vers la bonne section
  3. Relancer la vérification croisée si disponible

  CAS C — Ajouter un nouveau prompt maître (ex : clone-chat)
  -----------------------------------------------------------
  1. Créer PROMPT-MAITRE-CLONE-CHAT-vX.Y.Z.md
  2. Le faire dépendre de SHARED (préfixe PRÉREQUIS identique)
  3. Remplir les sections propres au skill
  4. Référencer SHARED pour tout ce qui est commun
  5. Ajouter les relations dans SHARED §3.1
  6. Mettre à jour la matrice SHARED §4.1 si nécessaire
  7. Lancer la vérification croisée

  CAS D — Vérifier la cohérence des 3 fichiers
  ---------------------------------------------
  1. Lancer le script : python3 scripts/verify-cross.py
  2. Vérifier que tous les checks sont PASS
  3. Corriger les FAILs éventuels


===============================================================================
5. RELATIONS DE DÉPENDANCE ENTRE FICHIERS
===============================================================================

  SHARED.md
    ├── lu par GEN-PLAN (références §0, §1.1, §1.2, §2.2, §2.3, §3, §3.1)
    └── lu par CORRECT-WORK (références §0, §1.1, §1.2, §1.4, §2.2, §2.3,
        §3, §3.1, §4, §4.1)

  GEN-PLAN v3.6.0
    ├── dépend de SHARED
    ├── référence correct-work >= v2.3.0 (à E1)
    ├── référence clone-chat >= v1.2.0 (E1-E7, E4, E15)
    └── référence skills-inventory >= v1.0.0 (E5)

  CORRECT-WORK v2.3.0
    ├── dépend de SHARED
    ├── référence gen-plan >= v3.6.0 (Étape 1)
    ├── référence clone-chat >= v1.2.0 (Mode CIBLE)
    └── référence fullstack-dev (projets web)


===============================================================================
6. NOTES
===============================================================================

  - Les numéros de version dans les noms de fichiers correspondent aux
    versions des skills, pas des prompts : gen-plan v3.6.0, correct-work
    v2.3.0.

  - SHARED n'a pas de numéro de version skill car ce n'est pas un skill,
    c'est un socle de référence commun.

  - Le contenu in extenso des fichiers référence de gen-plan (§9) est
    inclus dans le prompt maître pour permettre l'installation autonome
    sans avoir à consulter d'autres sources.

  - La vérification croisée (scripts/verify-cross.py) valide 5 axes :
    pas de duplication, références SHARED cohérentes, relations
    bidirectionnelles, aucune info perdue, tailles conformes.

===============================================================================