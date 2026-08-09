#!/usr/bin/env python3
"""
Intégration massive du contenu manquant dans la base KNOWLEDGE.
Chaque entrée est testée (validée) avant insertion.
Protocole gen-plan Étape 11 : Test et Correction Pré-Intégration.
"""

import json
import urllib.request
import sys
import time

API_BASE = "http://localhost:3000/api/knowledge"

# ═══════════════════════════════════════════════════════
# VALIDATEURS (Étape 11 — Test avant intégration)
# ═══════════════════════════════════════════════════════

def validate_entry(entry):
    """Valide une entrée avant insertion. Retourne (valide, erreurs)."""
    errors = []
    
    # Titre : obligatoire, min 5 chars
    if not entry.get("title") or len(entry["title"].strip()) < 5:
        errors.append("Titre manquant ou trop court (< 5 chars)")
    
    # Contenu : obligatoire, min 50 chars
    if not entry.get("content") or len(entry["content"].strip()) < 50:
        errors.append(f"Contenu manquant ou trop court ({len(entry.get('content',''))} chars, min 50)")
    
    # Catégorie : obligatoire, parmi les valeurs autorisées
    valid_categories = ["profile", "agent", "skill", "protocol", "trigger", "rule", "other"]
    if entry.get("category") not in valid_categories:
        errors.append(f"Catégorie invalide: {entry.get('category')}")
    
    # Priorité : obligatoire
    valid_priorities = ["critical", "important", "normal", "secondary"]
    if entry.get("priority") not in valid_priorities:
        errors.append(f"Priorité invalide: {entry.get('priority')}")
    
    # Tags : obligatoire, au moins 1 tag
    if not entry.get("tags") or len(entry["tags"].strip()) < 2:
        errors.append("Tags manquants")
    
    # Pas de placeholders non résolus
    for field in ["title", "content"]:
        val = entry.get(field, "")
        for marker in ["[TODO]", "[PLACEHOLDER]", "[À COMPLÉTER]", "..."]:
            if marker in val:
                errors.append(f"Placeholder non résolu '{marker}' dans {field}")
    
    # Pas de contenu tronqué (finit par un mot coupé)
    content = entry.get("content", "").strip()
    if content and content[-1:] not in [".", "!", "?", ":", "'", ")", "]"]:
        if not content.endswith("...") and len(content) > 100:
            errors.append(f"Contenu possiblement tronqué (finit par '{content[-20:]}')")
    
    return len(errors) == 0, errors


def test_api_post(entry):
    """Teste l'insertion d'une entrée via l'API. Retourne (succès, réponse)."""
    try:
        data = json.dumps(entry).encode("utf-8")
        req = urllib.request.Request(
            API_BASE,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        resp = urllib.request.urlopen(req, timeout=10)
        result = json.load(resp)
        return True, result
    except Exception as e:
        return False, str(e)


def verify_entry_after_insert(expected, actual):
    """Vérifie qu'une entrée insérée correspond à ce qui était attendu."""
    errors = []
    if actual.get("title") != expected["title"]:
        errors.append(f"Titre mismatch: {actual.get('title')} != {expected['title']}")
    if actual.get("category") != expected["category"]:
        errors.append(f"Catégorie mismatch")
    if actual.get("priority") != expected["priority"]:
        errors.append(f"Priorité mismatch")
    if actual.get("content") != expected["content"]:
        errors.append(f"Contenu mismatch (longueurs: {len(actual.get('content',''))} vs {len(expected['content'])})")
    return len(errors) == 0, errors


# ═══════════════════════════════════════════════════════
# ENTRÉES À INTÉGRER (contenu validé depuis les fichiers)
# ═══════════════════════════════════════════════════════

ENTRIES = [
    # ─── SKILL gen-plan (détaillé) ─────────────────────
    {
        "title": "Skill gen-plan — Protocole Détaillé",
        "content": """Skill d'orchestration et de planification structurée pour tâches complexes multi-étapes. Version v1.0.0.

DÉCLENCHEURS :
- "gen-plan:" suivi d'une description de tâche
- "plan d'actions" — demande explicite de planification
- "orchestre" — orchestration multi-agents
- Toute demande impliquant plusieurs étapes séquentielles avec des livrables

3 MODES D'EXÉCUTION :
- DIRECT : L'utilisateur écrit "gen-plan:" — génère plan + orchestration optionnelle
- PROJET : Appelé par correct-work(projet) — analyse complète + plan + gestion prompt-master
- CIBLE : Appelé par correct-work(cible) — analyse ciblée des fichiers pertinents uniquement

PHILOSOPHIE (5 principes) :
1. Lire avant de planifier — un plan sans connaissance du projet est générique et probablement erroné
2. Sélection performance-driven — le choix skill/agent est dicté par le gain de performance
3. Les skills peuvent lancer des agents spécialisés — modèle à 2 couches : Skill (protocole) → Agent (exécution)
4. Exécution sérielle par défaut — une tâche à la fois, sauf demande explicite de parallélisation
5. Progression visible — l'utilisateur sait toujours où on en est

PROTOCOLE 11 ÉTAPES DÉTAILLÉES :
Étape 1 — Collecte des demandes : relire toute la conversation, identifier demandes explicites et implicites, lister sans ambiguïté
Étape 2 — Lecture du projet : traverser tous les fichiers (structure, source, schéma BDD, dépendances, config, docs, assets)
Étape 3 — Identification nature : type projet, technologies, architecture, complexité
Étape 4 — Objectifs : lister tous les objectifs mesurables, supprimer doublons
Étape 5 — Décomposition : sous-tâches atomiques avec ordre logique, adaptées au type projet
Étape 6 — Dépendances : séquentielles, parallèles, conditionnelles ; vérifier absence de cycles
Étape 7 — Priorisation : Critique (échec invalide tout) > Importante (impact qualité) > Secondaire (améliore)
Étape 8 — Risques : complexité technique, ambiguïté, dépendances externes, plans fallback
Étape 9 — Structuration : plan formel avec en-tête, étapes ordonnées avec IDs, carte dépendances, matrice risques
Étape 10 — Validation : checklist 6 critères (couverture, étapes manquantes, ordre logique, adaptation projet, critères validation, risques couverts)
Étape 11 — Mise à jour prompt-master : uniquement en mode PROJET si modifications effectuées

GESTION D'ERREURS :
Si une phase échoue : 1) Logger dans worklog, 2) Annoncer à l'utilisateur, 3) Demander retry/agent différent/skip, 4) Ne jamais continuer silencieusement, 5) Considérer un autre skill ou agent

RELATIONS AVEC AUTRES SKILLS :
- correct-work appelle gen-plan à son Étape 1
- gen-plan scanne skills-inventory à l'Étape 5
- gen-plan délègue à skill-creator pour création/amélioration de skills
- gen-plan délègue à fullstack-dev, pptx, charts, pdf, docx, xlsx, web-search, web-reader, image-generation, image-edit, ASR, TTS, VLM, LLM, video-understand, pdf-llm.

Ce skill constitue le cœur du système d'orchestration et doit être chargé prioritairement pour toute tâche complexe.""",
        "category": "skill",
        "tags": "gen-plan,orchestration,plan,séquentiel,multi-agents,protocole,détaillé",
        "priority": "critical",
        "source": "imported",
        "pinned": True,
    },
    {
        "title": "Skill gen-plan — Mappings Agents/Skills (17 paires)",
        "content": """Table de référence pour la sélection performance-driven des agents et skills.
Chaque paire est classée par type de performance : Skill+Agent (optimal), Skill seul (bon), Agent seul (modéré).

MAPPINGS SKILL + AGENT SPÉCIALISÉ (Performance OPTIMALE) :
1. fullstack-dev → full-stack-developer : développement web Next.js 16. Skill fournit conventions + quality gates ; agent construit l'app
2. pptx → ppt-expert : présentations slides HTML. Skill fournit layout/format ; agent génère les slides

MAPPINGS SKILL + AGENT GÉNÉRIQUE (Performance BONNE) :
3. pdf → general-purpose : génération PDF. Skill fournit templates + layout rules
4. docx → general-purpose : documents Word. Skill fournit formatting + styles
5. xlsx → general-purpose : tableurs Excel. Skill fournit data structures + chart rules
6. charts → general-purpose : graphiques/visualisations. Skill fournit chart type routing + styling
7. web-search → general-purpose : recherche web. Skill fournit search protocol + result formatting
8. web-reader → general-purpose : extraction contenu web. Skill fournit extraction + parsing protocol
9. image-generation → general-purpose : création images IA. Skill fournit prompt engineering + sizing
10. image-edit → general-purpose : modification images IA. Skill fournit edit protocol + formats
11. ASR → general-purpose : speech-to-text. Skill fournit audio handling + transcription
12. TTS → general-purpose : text-to-speech. Skill fournit voice selection + audio format
13. VLM → general-purpose : analyse images. Skill fournit multimodal interaction
14. LLM → general-purpose : chat IA. Skill fournit conversation management + context
15. video-understand → general-purpose : analyse vidéo. Skill fournit frame analysis protocol
16. pdf-llm → general-purpose : extraction PDF. Skill fournit extraction modes (qwen/glm/multi)
17. skill-creator → general-purpose : création/amélioration skills. Skill fournit eval + optimization loop

AGENTS SEULS (sans skill, Performance MODÉRÉE) :
- Explore : recherche rapide dans codebase (fichiers, grep, patterns)
- Plan : architecture et stratégie (raisonnement architecte logiciel)
- frontend-styling-expert : CSS, responsive, animations, UI/UX
- general-purpose : dernier recours si aucun skill ni agent spécialisé ne correspond

RÈGLE CLÉ : L'agent parent DOIT charger le skill pertinent avant de déléguer à un sous-agent. Les sous-agents n'ont PAS accès au contexte de conversation ni aux instructions du skill.""",
        "category": "skill",
        "tags": "gen-plan,mapping,agents,skills,sélection,performance,optimisation,routage",
        "priority": "critical",
        "source": "imported",
        "pinned": True,
    },
    {
        "title": "Skill gen-plan — Modèle Délégation 2 Couches",
        "content": """Le modèle de délégation à 2 couches est le principe fondamental de l'orchestration gen-plan.

COUCHE 1 — SKILL (Protocole + Connaissance domaine) :
Le skill fournit le "COMMENT" : protocole détaillé, templates, critères qualité, conventions, points de vérification. Il est l'accélérateur qui donne à l'agent des connaissances spécifiques au domaine.

COUCHE 2 — AGENT SPÉCIALISÉ (Exécution + Outils) :
L'agent fournit le "QUI" : capacités spécialisées, outils, vitesse d'exécution, expertise technique. Il exécute la tâche avec les directives du skill.

PROCESSUS DE DÉLÉGATION :
1. L'agent parent identifie une sous-tâche
2. Il scanne l'écosystème de skills → un skill correspond-il ?
3. Si OUI → charger le skill
4. Le skill bénéficie-t-il d'un agent spécialisé en interne ?
5. Si OUI → Skill + Agent Spécialisé (PERFORMANCE OPTIMALE)
6. Si NON → Skill seul via agent général (BONNE PERFORMANCE)
7. Si pas de skill → Agent spécialisé seul (MODÉRÉ)
8. Si rien → general-purpose (DERNIER RECOURS)

EXEMPLE CONCRET — Développement web Next.js :
- Sans modèle 2 couches : general-purpose code une app → résultat générique, lent
- Avec skill seul : fullstack-dev chargé dans general-purpose → conventions + quality gates → meilleur
- Avec 2 couches : fullstack-dev chargé puis délégué à full-stack-developer → OPTIMAL (protocole + expertise)

POINT CLÉ : Un skill n'est pas un remplacement pour un agent — c'est un ACCÉLÉRATEUR. Charger un skill donne à l'agent des connaissances spécifiques au domaine, des templates et des protocoles qualité. L'agent exécute plus vite et mieux avec le skill chargé que sans lui.""",
        "category": "skill",
        "tags": "gen-plan,délégation,2-couches,skill,agent,protocole,orchestration",
        "priority": "critical",
        "source": "imported",
        "pinned": True,
    },

    # ─── SKILL correct-work ────────────────────────────
    {
        "title": "Skill correct-work — Protocole de Vérification",
        "content": """Skill de vérification du travail réalisé. Alias : verify-work. Version v1.0.0.

DÉCLENCHEURS :
- "vérifie ton travail", "vérifie tes résultats", "vérifie ton code"
- "correct_work", "verify_work"

3 MODES D'APPEL :
- PROJET : correct_work(projet) — vérification complète avec gestion du prompt-maître. Première analyse = intégralité du projet ; appels suivants = lecture du prompt-maître existant uniquement
- CIBLE : correct_work(cible) — vérification ciblée sur un livrable spécifique, sans gestion du prompt-maître
- DIRECT : correct_work() — vérification rapide sans analyse approfondie

PROTOCOLE 5 ÉTAPES SÉQUENTIELLES :

ÉTAPE 1 — Plan d'actions (appel à gen-plan) :
Appelle le skill gen-plan pour générer un plan de vérification adapté au projet. Le plan sert de base pour les étapes 2 à 5. Le plan DOIT être spécifiquement adapté au type de projet vérifié (web, Python, PDF, script, etc.).

ÉTAPE 2 — Erreurs et omissions :
1. Relire les spécifications initiales et vérifier chaque exigence satisfaite
2. Vérifier les données factuelles (noms, chemins, versions, tailles, counts)
3. Vérifier la cohérence linguistique (pas de mélange de langues incohérent)
4. Vérifier les fichiers de sortie (existent, lisibles, non vides)
5. Vérifier les dépendances (imports, chemins, références croisées)
6. Adapter la vérification au type de projet
7. Corriger chaque erreur ou omission identifiée

ÉTAPE 3 — Structure du code et conflits :
1. Imports circulaires
2. Conflits de noms (fonctions/classes/variables en double)
3. Variables non initialisées ou utilisées avant définition
4. Chemins en dur non portables
5. Gestion des erreurs (cas d'erreur traités ou échec silencieux ?)
6. Doublons de code à factoriser
7. Convention de nommage cohérente
8. Conflits logiques et conditions contradictoires — utiliser un TABLEAU DE KARNAUGH pour simplifier, détecter les contradictions, vérifier la couverture complète
9. Corriger chaque problème identifié

ÉTAPE 4 — Vérification des interactions :
Adaptée au type de projet (fullstack, frontend, backend, document, script) :
1. API frontend-backend : endpoints existent, params correspondent, réponses parsées, codes erreur gérés
2. Props inter-composants : types corrects, callbacks bons args, pas de props manquantes
3. State management : store expose données nécessaires, actions au bon moment, pas de state mort
4. Flux de données bout en bout : tracer scénario complet clic→API→store→render
5. Communications entre services : ports/URLs, XTransformPort, WebSockets, timeouts
6. Références croisées entre livrables (documents)
7. Corriger chaque problème d'interaction

ÉTAPE 5 — Cohérence des raisonnements et résultats :
1. Cohérence logique (pas de saut, pas de contradiction)
2. Cohérence numérique (chiffres, pourcentages, tailles)
3. Cohérence temporelle (dates, versions, chronologies)
4. Résultat attendu vs résultat obtenu
5. Cohérence entre fichiers livrables
6. Corriger toute incohérence

DÉPENDANCE : Ce skill dépend de gen-plan pour son Étape 1. Si gen-plan n'est pas disponible, l'Étape 1 doit être réalisée manuellement.""",
        "category": "skill",
        "tags": "correct-work,vérification,qualité,validation,5-étapes,karnaugh,verify-work",
        "priority": "critical",
        "source": "imported",
        "pinned": True,
    },

    # ─── SKILL cpp-analysis ────────────────────────────
    {
        "title": "Skill cpp-analysis — Analyse Code C/C++",
        "content": """Skill d'analyse de code C/C++ pour détection de bugs, optimisation et documentation. Version v1.0.0.

DÉCLENCHEURS : "analyse code C++", "détecte bugs C/C++", "optimise performance C++", "génération documentation C++", "analyse complexité"

5 CAPACITÉS PRINCIPALES :

1. DÉTECTION DE BUGS :
- Fuites de mémoire (memory leaks)
- Buffer overflows
- Null pointer dereferences
- Race conditions (multithreading)
- Undefined behavior
- Violations de règles (MISRA, CERT)

2. OPTIMISATION DE PERFORMANCE :
- Analyse de complexité algorithmique O(n)
- Détection de code inefficace
- Suggestions d'optimisation
- Profiling et benchmarking
- Optimisation mémoire

3. ANALYSE DE QUALITÉ :
- Métriques de code (lignes, complexité, couverture)
- Détection de code dupliqué
- Analyse de dépendances
- Respect des standards (ISO C/C++)

4. GÉNÉRATION DE DOCUMENTATION :
- Documentation automatique (Doxygen)
- Génération de diagrammes
- Documentation d'API
- Commentaires inline

5. REFACTORING :
- Suggestions de refactoring
- Modernisation de code (C++11 vers C++20)
- Amélioration de lisibilité
- Réduction de complexité

OUTILS D'ANALYSE :
- Statique : cppcheck (bugs/sécurité), clang-tidy (linting/refactoring), flawfinder (vulnérabilités), rats (audit sécurité)
- Dynamique : valgrind (fuites mémoire), gprof (profiling), gcov (couverture)
- Documentation : doxygen (génération docs), graphviz (diagrammes dépendances)

INTÉGRATION AVEC AUTRES SKILLS :
- coding-agent : workflow de développement C/C++
- python-executor : exécution de scripts d'analyse Python
- pdf-expert : génération de rapports d'analyse PDF

CAS D'USAGE : "Analyse ce code C++ et trouve les bugs", "Optimise les performances", "Génère la documentation Doxygen", "Détecte les fuites mémoire", "Analyse la complexité".""",
        "category": "skill",
        "tags": "cpp-analysis,c++,analyse,bugs,optimisation,documentation,refactoring,valgrind,cppcheck",
        "priority": "important",
        "source": "imported",
        "pinned": False,
    },

    # ─── MATRICE AGENTS DÉTAILLÉE ──────────────────────
    {
        "title": "Matrice Agents — Capacités Détaillées",
        "content": """Référence détaillée des 6 types d'agents disponibles avec leurs capacités, outils, limites et boost de performance.

1. general-purpose :
- Outils : Tous (Read, Write, Edit, Bash, Grep, Glob, LS, Task)
- Meilleur pour : Recherche multi-étapes, opérations fichiers complexes, tâches multi-domaines
- Limites : Pas de connaissance domaine spécialisée ; plus lent que les spécialistes
- Boost performance : SIGNIFICATIF quand un skill est chargé (le skill fournit le protocole domaine)
- Utiliser quand : La tâche couvre plusieurs domaines ou nécessite un raisonnement flexible

2. Explore :
- Outils : Tous
- Meilleur pour : Exploration rapide de codebase, recherche par patterns fichiers, recherche par mots-clés
- Vitesse : Rapide (conçu pour les recherches fichiers/code)
- Niveaux de profondeur : "quick", "medium", "very thorough"
- Boost performance : Aucun nécessaire — déjà optimal pour les tâches de recherche
- Utiliser quand : Trouver des fichiers, chercher du code, comprendre la structure d'un projet

3. Plan :
- Outils : Tous
- Meilleur pour : Décisions d'architecture, stratégie d'implémentation, identification fichiers critiques
- Boost performance : Aucun nécessaire — déjà optimal pour les tâches de planification
- Utiliser quand : Concevoir des plans d'implémentation avant de coder

4. frontend-styling-expert :
- Outils : Tous
- Meilleur pour : CSS, frameworks styling, responsive design, UI/UX, animations, layout systems
- Boost performance : Aucun nécessaire — déjà spécialisé pour les tâches visuelles
- Utiliser quand : Aspects visuels/présentationnels du développement web

5. full-stack-developer :
- Outils : Tous, construit des apps Next.js production-ready
- Meilleur pour : Sites web complets, dashboards, applications web, interfaces temps réel
- Stack : Next.js 16, TypeScript, Tailwind CSS 4, shadcn/ui, Prisma ORM
- Boost performance : SIGNIFICATIF quand le skill fullstack-dev est chargé (conventions + quality gates)
- Utiliser quand : Pages web interactives, systèmes de gestion, apps Next.js

6. ppt-expert :
- Outils : Tous
- Meilleur pour : Présentations slides professionnelles en fichiers HTML standalone
- Boost performance : SIGNIFICATIF quand le skill pptx est chargé (layout + format rules)
- Utiliser quand : Création de PPT/decks de slides

PRINCIPE DE SÉLECTION PERFORMANCE-DRIVEN :
Les skills sont des accélérateurs, pas des remplacements. Charger un skill dans n'importe quel agent donne à cet agent des connaissances domaine-spécifiques, des templates et des protocoles qualité. Le chemin d'exécution optimal est toujours : Skill (protocole) + Agent Spécialisé (exécution).""",
        "category": "agent",
        "tags": "agents,matrice,capacités,outils,performance,sélection,détaillé",
        "priority": "critical",
        "source": "imported",
        "pinned": True,
    },
    {
        "title": "Arbre de Décision — Sélection Agent/Skill",
        "content": """Arbre de décision pour la sélection performance-driven d'agents et de skills.
À utiliser pour chaque sous-tâche dans le cadre du protocole gen-plan.

PROCESSUS DE DÉCISION :

ÉTAPE 1 : Existe-t-il un SKILL correspondant dans l'écosystème ?
├─ OUI → Charger le Skill
│   └─ Le skill bénéficie-t-il d'un agent spécialisé en interne ?
│       ├─ OUI → Skill + Agent Spécialisé (PERFORMANCE OPTIMALE)
│       │   Exemple : fullstack-dev chargé, puis délégué à full-stack-developer
│       └─ NON → Skill seul via general-purpose (BONNE PERFORMANCE)
│           Exemple : web-search utilisé via general-purpose
└─ NON → Continuer à la sélection d'agent

ÉTAPE 2 : Quel agent SPÉCIALISÉ correspond le mieux (pas de skill disponible) ?
- Est-ce une app web Next.js avec UI interactive ?
  └─ OUI → full-stack-developer
  └─ NON → Est-ce un PPT/deck de slides ?
      └─ OUI → ppt-expert
      └─ NON → Est-ce purement visuel/styling (CSS, responsive, animation) ?
          └─ OUI → frontend-styling-expert
          └─ NON → Est-ce de l'architecture/planification uniquement (pas de sortie code) ?
              └─ OUI → Plan
              └─ NON → Est-ce une recherche rapide fichiers/code ?
                  └─ OUI → Explore
                  └─ NON → general-purpose (DERNIER RECOURS)

CLÉ : La performance est le moteur de décision à CHAQUE branche.

CHECKLIST D'ÉVALUATION PAR SOUS-TÂCHE :
| Question | Si OUI | Si NON |
|---|---|---|
| Skill correspondant existe ? | Charger → évaluer besoin agent | Passer à recherche agent |
| Skill + agent spécialisé > skill seul ? | Déléguer à agent spécialisé | Utiliser skill directement |
| Agent spécialisé > general-purpose ? | Utiliser agent spécialisé | Utiliser general-purpose |

Cet arbre de décision doit être appliqué systématiquement pour chaque sous-tâche d'un plan gen-plan.""",
        "category": "protocol",
        "tags": "arbre,décision,sélection,agent,skill,performance,routage,workflow",
        "priority": "critical",
        "source": "imported",
        "pinned": True,
    },

    # ─── INVENTAIRE 69 SKILLS ──────────────────────────
    {
        "title": "Inventaire Skills — 69 Skills en 12 Catégories",
        "content": """Inventaire complet des 69 skills installés, répartis en 12 catégories. Source : /home/z/my-project/skills/

CATÉGORIE 1 — MÉTA (Skills & Plans) : 6 skills
- gen-plan v1.0.0 : planification et orchestration multi-étapes
- correct-work v1.0.0 : vérification du travail réalisé (alias verify-work)
- skill-creator : création, modification et amélioration de skills
- skills-inventory : scan et rapport d'inventaire des skills
- task-review : sauvegarde de tâches comme skills réutilisables
- auto-target-tracker : suivi automatique de progression d'objectifs

CATÉGORIE 2 — DÉVELOPPEMENT : 3 skills
- fullstack-dev : développement web complet Next.js 16, TypeScript, Tailwind
- cpp-analysis v1.0.0 : analyse code C/C++, détection bugs, optimisation, documentation
- coding-agent : workflow développement propre (planification, implémentation, vérification, tests)

CATÉGORIE 3 — DOCUMENTS & CONTENU : 5 skills
- pdf : création, édition et analyse de documents PDF (4 pipelines : Report, Creative, Academic, Process)
- pdf-llm : extraction PDF vers Markdown + JSON structuré RAG-ready (modes qwen/glm/multi/pipeline)
- docx : création, édition et analyse de documents Word (.docx)
- xlsx : manipulation de fichiers Excel/tableurs (.xlsx, .xlsm, .csv, .tsv)
- pptx : création, édition et analyse de présentations (.pptx)

CATÉGORIE 4 — IA & MEDIA : 12 skills
- VLM : analyse et compréhension d'images via Vision Language Model
- LLM : chat et complétions via modèles de langage
- TTS : synthèse vocale (texte vers audio)
- ASR : reconnaissance vocale (audio vers texte)
- image-generation : création d'images par IA
- image-edit : modification d'images par IA
- image-search : recherche d'images sur le web
- video-understand : analyse et compréhension de vidéos
- agent-browser : automatisation de navigateur headless
- web-search : recherche web en temps réel
- web-reader : extraction de contenu de pages web

CATÉGORIE 5 — WEB & RECHERCHE : 6 skills
Skills de recherche web, extraction de contenu, navigation automatisée

CATÉGORIE 6 — VISUALISATION & DESIGN : 5 skills
- charts : création de graphiques, diagrammes, visualisations de données

CATÉGORIE 7 À 12 — Autres catégories : 32 skills
Contenu & Marketing (6), Finance & Recherche (7), Carrière & Emploi (4), Éducation (8), Lifestyle & Bien-être (5), Autres (2)

NOTE IMPORTANTE : L'inventaire source indique 69 skills. La plateforme z.ai actuelle en compte 71 (2 skills additionnels : task-review et skills-inventory ajoutés ultérieurement).""",
        "category": "skill",
        "tags": "inventaire,69-skills,12-catégories,écosystème,référence,complet",
        "priority": "critical",
        "source": "imported",
        "pinned": True,
    },

    # ─── PROMPTS MAÎTRES ──────────────────────────────
    {
        "title": "Prompt Maître — Mode Ingénieur Système",
        "content": """Prompt maître pour le mode INGÉNIEUR SYSTÈME. Version 1.0.0-system. IA cible : z.ai.

RÔLE PRINCIPAL :
Tu es l'ingénieur système de François. Ton rôle est d'orchestrer, administrer, automatiser et diagnostiquer.

COMPÉTENCES PRIORITAIRES :
1. Orchestration multi-agents (protocole gen-plan)
2. Hardware DJ : KONTROL S4 MK2/MK3, TRAKTOR PRO 3.11, fichiers TSI
3. Administration système : scripts bash, cron, services, monitoring
4. Automatisation : pipelines, workflows, intégrations
5. Diagnostic : troubleshooting hardware/software, logs, performance

AGENTS SPÉCIALISÉS PRIORITAIRES (6) :
1. tsi-expert — Expert fichiers TSI (mappings MIDI TRAKTOR). Analyse/modification mappings, détection conflits, validation XML, création presets
2. kontrol-s4-expert — Expert KONTROL S4 MK2. Specs MIDI, Haptic Drive, stems decks, troubleshooting drivers/firmware, optimisation latency ASIO
3. python-executor — Exécution scripts Python système. Automatisation, gestion fichiers, batch processing, intégration API système
4. pdf-expert — Génération rapports système. Rapports diagnostic, documentation technique, logs formatés
5. image-analyst — Analyse visuelle système. OCR screenshots d'erreurs, analyse captures, EXIF données
6. auto-tagger — Tagging audio bibliothèque DJ. Analyse BPM/clé/genre, organisation collection TRAKTOR, détection doublons

SCÉNARIOS D'USAGE SYSTÈME :
- Diagnostic hardware DJ : kontrol-s4-expert → vérification MIDI → tsi-expert → script test → rapport PDF
- Création mapping TSI : kontrol-s4-expert (specs MIDI) → tsi-expert (création) → validation XML → script test
- Automatisation système : python-executor (script backup) → gestion erreurs → kontrol-s4-expert (fichiers config) → documentation PDF

DÉCLENCHEURS SYSTÈME :
- "gen-plan:", "plan d'actions" → Orchestration
- "mon jog wheel ne répond plus" → Diagnostic hardware
- "crée un mapping TSI" → Fichiers TSI
- "backup config TRAKTOR" → Automatisation
- "analyse logs" → Diagnostic système

Ce prompt maître est la configuration de base pour toute session système sur z.ai.""",
        "category": "protocol",
        "tags": "prompt-maître,système,ingénieur,zai,hardware,dj,diagnostic,automatisation",
        "priority": "critical",
        "source": "imported",
        "pinned": True,
    },
    {
        "title": "Prompt Maître — Mode Codage",
        "content": """Prompt maître pour le mode CODAGE. Version 1.0.0-code. IA cible : qwen.

RÔLE PRINCIPAL :
Tu es le développeur de François. Ton rôle est de concevoir, coder, tester et déboguer des programmes.

COMPÉTENCES PRIORITAIRES :
1. Développement Python : scripts, automatisation, data processing
2. Développement C/C++ : programmes système, performance
3. Applications web : Next.js 16, TypeScript, Tailwind CSS 4
4. APIs et bases de données : REST, Prisma ORM, SQLite
5. Scripts audio : librosa, mutagen, pydub (pour DJ)

AGENTS SPÉCIALISÉS DÉVELOPPEMENT (6) :
1. python-executor — Expert Python (création + exécution). Bibliothèques : librosa, mutagen, pydub, pandas, numpy. Virtual environments, pip, debugging. Intégration audio (analyse BPM, clés, tagging)
2. full-stack-developer — Expert Next.js 16. TypeScript, Tailwind CSS 4, shadcn/ui, Prisma ORM, SQLite. Applications web complètes, dashboards, API routes
3. pdf-expert — Génération rapports code. Documentation technique, rapports de tests, conversion code vers PDF
4. image-analyst — Analyse visuelle pour dev. OCR screenshots d'erreurs, analyse captures UI, détection bugs visuels
5. auto-tagger — Scripts analyse audio. Analyse BPM/clé/genre avec librosa, essentia. Tagging automatique, détection doublons (acoustid, chromaprint)
6. coding-agent — Workflow développement propre. Planification, implémentation, vérification, tests. Clean code, best practices

RÈGLE ADDITIONNELLE MODE CODE : Écrire du code propre et documenté (règle d'or #7 spécifique au mode codage)

DÉCLENCHEURS CODAGE :
- "<py script.py>" → Exécution script Python
- "crée un script Python" → Développement Python
- "programme C++" → Développement C/C++
- "app web Next.js" → Développement web
- "API REST" → Backend development
- "debug ce code" → Débogage

Ce prompt maître est la configuration de base pour toute session codage sur qwen.""",
        "category": "protocol",
        "tags": "prompt-maître,codage,développement,qwen,python,c++,nextjs,api",
        "priority": "critical",
        "source": "imported",
        "pinned": True,
    },
    {
        "title": "Prompt Maître — Écosystème DJ Complet",
        "content": """Prompt maître universel pour l'écosystème DJ/Python/PDF/Image/Audio. Version 1.0.0. Checksum : Écosystème 69 skills + 12 agents + protocole gen-plan v1.0.0.

INSTRUCTIONS D'AUTO-INTÉGRATION (à destination de l'IA réceptrice) :
1. Charger ce prompt en mémoire permanente pour toute la durée de la session
2. Reconnaître les déclencheurs : gen-plan:, plan d'actions, orchestre, <py script.py>, crée un mapping TSI, mon jog wheel ne répond plus, tag mes fichiers audio, génère un PDF, analyse cette image
3. Appliquer le protocole d'orchestration (11 étapes séquentielles)
4. Sélectionner l'agent optimal selon la matrice de décision performance-driven
5. Exécuter en mode sériel (une tâche à la fois)
6. Mettre à jour le worklog après chaque phase
7. Communiquer en français avec l'utilisateur (François)

PHILOSOPHIE DE L'ÉCOSYSTÈME :
Principe fondamental : Performance-driven selection. Le choix entre skill, agent spécialisé ou agent général est dicté par le gain de performance, pas par une hiérarchie rigide.

MODÈLE À DEUX COUCHES :
Skill (protocole + connaissance domaine) → Agent Spécialisé (exécution + outils)
Le skill fournit le "comment" (protocole, templates, critères qualité)
L'agent fournit le "qui" (capacités spécialisées, outils, vitesse)

EXÉCUTION SÉRIELLE PAR DÉFAUT :
Toutes les tâches s'exécutent UNE À LA UNE dans l'ordre défini. Pas de parallélisation sauf demande explicite de l'utilisateur et sous-tâches provablement indépendantes. Quality gate entre chaque phase : vérifier les outputs avant de continuer. Corrections en vol possibles si la sortie d'une phase change l'état du projet.

9 IA SUPPORTÉES : z.ai, qwen, manus, copilot, chatgpt, perplexity, gemini, claude, codex.

Ce prompt maître universel est le plus complet et sert de base pour toutes les IAs.""",
        "category": "protocol",
        "tags": "prompt-maître,écosystème,dj,universel,auto-intégration,performance-driven",
        "priority": "critical",
        "source": "imported",
        "pinned": True,
    },

    # ─── CONFIG MÉMOIRE MULTI-IA ──────────────────────
    {
        "title": "Config Mémoire — Comparatif 9 IAs",
        "content": """Comparatif des capacités de mémoire permanente des 9 IAs supportées par l'écosystème.

| IA | Mémoire Permanente | Project Knowledge | Recommandation |
|---|---|---|---|
| z.ai | Oui | Oui | Utiliser Project Knowledge (Settings → Projects → Knowledge) |
| qwen | Oui | Non | Utiliser Mémoire (Settings → Personalization → Memory) |
| manus | Oui | Oui | Utiliser Project Knowledge (Projects → Knowledge Base) |
| copilot | Oui | Non | Utiliser Mémoire (Settings → Personalization → Memory) |
| chatgpt | Oui | Oui (GPTs) | Créer un GPT personnalisé (chat.openai.com/gpts → Create) |
| perplexity | Limitée | Non | Utiliser Collections (Library → Collections) |
| gemini | Oui | Oui (Gems) | Créer un Gem personnalisé (Gemini → Gems) |
| claude | Oui | Oui (Projects) | Utiliser Project Knowledge (Projects → Project Knowledge) |
| codex | Oui | Non | Utiliser Mémoire (Settings → Memory) |

ACTIONS POUR CHAQUE IA :
1. Activer la mémoire (si disponible)
2. Créer un Project/Gem/GPT (si disponible)
3. Ajouter le prompt maître comme knowledge/context
4. Dire à l'IA : "Mémorise ceci : [résumé du prompt maître]"

RÉSUMÉ DU PROMPT MAÎTRE À MÉMORISER :
Je suis François, DJ avec KONTROL S4 MK32 + TRAKTOR 3.11, France. J'ai un écosystème de 12 agents spécialisés et 69/71 skills. Agents DJ : tsi-expert, kontrol-s4-expert, python-executor, pdf-expert, image-analyst, auto-tagger. Agents génériques : general-purpose, Explore, Plan, frontend-styling-expert, full-stack-developer, ppt-expert. Protocole gen-plan : 11 étapes séquentielles pour orchestration. Matrice performance-driven : Skill + Agent > Skill seul > Agent seul > General. Déclencheurs : gen-plan:, plan d'actions, <py script.py>, crée un mapping TSI, tag mes fichiers audio. Communication : Toujours en français.""",
        "category": "other",
        "tags": "mémoire,config,ia,multi-ia,comparatif,zai,qwen,chatgpt,claude,gemini",
        "priority": "important",
        "source": "imported",
        "pinned": False,
    },

    # ─── CONFIG QWEN ───────────────────────────────────
    {
        "title": "Config Mémoire — Qwen (Développement)",
        "content": """Configuration mémoire spécifique pour Qwen (Alibaba) orientée développement.

IA : qwen (Alibaba Qwen)
Rôle : Développement Python, C/C++, Next.js, APIs, scripts audio
URL : https://chat.qwen.ai/
Config : Settings → Personalization → Memory

AGENTS SPÉCIALISÉS DÉVELOPPEMENT (différences vs config système) :
- python-executor : accent sur bibliothèques développement (librosa, mutagen, pydub, pandas, numpy)
- full-stack-developer : accent sur stack web complète (TypeScript, Tailwind, shadcn/ui, Prisma)
- coding-agent : workflow développement propre (planification, implémentation, vérification, tests, clean code)

DÉCLENCHEURS SPÉCIFIQUES MODE CODAGE :
- "<py script.py>" → Agent python-executor
- "programme C++", "développement C/C++" → Agent coding-agent
- "app web Next.js", "dashboard" → Agent full-stack-developer
- "API REST", "backend" → Agent full-stack-developer
- "debug ce code", "optimise ce script" → Agent python-executor
- "tag mes fichiers audio" → Agent auto-tagger
- "génère un PDF", "documentation technique" → Agent pdf-expert

RÈGLE ADDITIONNELLE : Toujours écrire du code propre et documenté (règle d'or #8 spécifique au mode codage)

VALIDATION :
Après configuration, tester avec :
- "gen-plan:" → qwen doit appliquer les 11 étapes
- "<py script.py>" → qwen doit créer un script Python
- "programme C++" → qwen doit utiliser l'agent coding-agent.

Cette configuration est optimisée pour le développement logiciel.""",
        "category": "other",
        "tags": "mémoire,qwen,développement,config,codage,python,c++,nextjs",
        "priority": "important",
        "source": "imported",
        "pinned": False,
    },

    # ─── LAUNCHER ──────────────────────────────────────
    {
        "title": "Launcher Multi-Contexte IA v3.0.0",
        "content": """Lanceur multi-contexte IA avec auto-détection. Script Python : /home/z/my-project/launcher.py

FONCTIONNALITÉS :
- Lancement automatique d'une session IA avec le prompt maître adapté au contexte
- Auto-détection du contexte (système ou codage)
- Support de 9 IAs : z.ai, qwen, manus, copilot, chatgpt, perplexity, gemini, claude, codex
- Copie automatique du prompt maître dans le presse-papier
- Ouverture du navigateur vers l'IA sélectionnée
- Historique des sessions et statistiques d'utilisation
- Configuration persistante des IA par défaut par contexte

2 CONTEXTES :
- system : Ingénieur système (z.ai par défaut). Administration, orchestration, hardware DJ, TSI, automatisation
- code : Développement (qwen par défaut). Python, C/C++, Next.js, APIs, scripts audio

COMMANDES PRINCIPALES :
python3 launcher.py                    # Auto-détection contexte + IA
python3 launcher.py system             # Contexte système, IA auto
python3 launcher.py code               # Contexte codage, IA auto
python3 launcher.py system qwen        # Système sur qwen
python3 launcher.py code chatgpt       # Codage sur ChatGPT
python3 launcher.py --config           # Configure les IA par défaut
python3 launcher.py --list             # Liste contextes et IA

ALIAS SHELL (via setup-aliases.sh) :
ai        → Auto-détection
sys       → Système sur z.ai
code      → Codage sur qwen
sys-zai   → Système sur z.ai
sys-qwen  → Système sur qwen
code-qwen → Codage sur qwen
ai-config → Configurer IA par défaut
ai-list   → Lister contextes et IA

FICHIERS ASSOCIÉS :
- launcher.py : script principal
- setup-aliases.sh : installation alias shell
- prompt-maitre-system.md : prompt maître système
- prompt-maitre-code.md : prompt maître codage
- Configuration : ~/.config/ai-launcher/config.json

Le launcher est l'outil central pour démarrer rapidement une session IA avec le contexte adapté.""",
        "category": "other",
        "tags": "launcher,ia,multi-contexte,auto-détection,shell,alias,zai,qwen",
        "priority": "important",
        "source": "imported",
        "pinned": False,
    },

    # ─── SCÉNARIOS D'USAGE DJ ──────────────────────────
    {
        "title": "Scénarios DJ — Cas d'Usage Détaillés",
        "content": """Scénarios d'usage concrets de l'écosystème pour les tâches DJ.

SCÉNARIO 1 — Analyse Collection Vinyles :
Demande : "Analyse ma collection de vinyles, détecte BPM et clés, génère rapport PDF"
Plan :
1. auto-tagger → Scan répertoire, analyse BPM avec librosa/essentia
2. auto-tagger → Détection clé musicale (Camelot wheel)
3. image-analyst → Analyse pochettes (optionnel, OCR, classification)
4. pdf-expert → Génération rapport PDF structuré

SCÉNARIO 2 — Création Mapping TSI :
Demande : "Crée-moi un mapping TSI pour mes hot cues sur le deck A"
Plan :
1. kontrol-s4-expert → Identification specs MIDI KONTROL S4 MK2
2. tsi-expert → Analyse structure TSI existante
3. tsi-expert → Création mapping hot cues (XML MIDI)
4. tsi-expert → Validation XML, détection conflits
5. python-executor → Script test du mapping

SCÉNARIO 3 — Script Python Analyse Audio :
Demande : "<py analyze_bpm.py> Analyse BPM de tous mes MP3"
Plan :
1. python-executor → Création script avec librosa
2. python-executor → Installation dépendances (pip install librosa)
3. python-executor → Exécution script avec gestion erreurs
4. python-executor → Validation résultats
5. pdf-expert → Génération rapport PDF des BPM

SCÉNARIO 4 — Diagnostic Hardware DJ :
Demande : "Mon jog wheel droit ne répond plus"
Plan :
1. kontrol-s4-expert → Diagnostic hardware (drivers, firmware, USB)
2. kontrol-s4-expert → Vérification config MIDI
3. tsi-expert → Analyse mapping TSI (conflits ?)
4. python-executor → Script test MIDI (envoi/retour)
5. pdf-expert → Rapport diagnostic

SCÉNARIO 5 — Automatisation Backup TRAKTOR :
Demande : "Crée un script qui backup ma config TRAKTOR chaque nuit"
Plan :
1. python-executor → Création script backup avec cron
2. python-executor → Gestion erreurs, logs rotation
3. kontrol-s4-expert → Identification fichiers config TRAKTOR
4. pdf-expert → Documentation du script

SCÉNARIO 6 — Script Renommage Fichiers Audio :
Demande : "Crée un script qui renomme mes fichiers audio selon format Artiste - Titre (BPM)"
Plan :
1. python-executor → Création script avec mutagen
2. python-executor → Lecture métadonnées audio (ID3 tags)
3. python-executor → Renommage fichiers avec rollback si erreur
4. pdf-expert → Rapport des fichiers renommés

Ces scénarios illustrent l'utilisation concrète de l'écosystème pour les tâches DJ les plus courantes.""",
        "category": "trigger",
        "tags": "scénarios,dj,usage,traktor,tsi,bpm,audio,backup,diagnostic,mapping",
        "priority": "important",
        "source": "imported",
        "pinned": False,
    },

    # ─── AGENT CODING-AGENT (manquant) ─────────────────
    {
        "title": "Agent coding-agent — Workflow Développement",
        "content": """Agent spécialisé pour le workflow de développement propre et structuré. Disponible uniquement en mode Codage (IA cible : qwen).

CAPACITÉS :
- Planification : analyse des besoins, architecture technique, choix technologiques
- Implémentation : écriture de code propre, respect des conventions, design patterns
- Vérification : tests unitaires, tests d'intégration, revue de code
- Documentation : commentaires inline, documentation API, README

DOMAINES D'EXPERTISE :
- Développement C/C++ : programmes système, performance, optimisation
- Développement Python : scripts, automatisation, data processing
- Applications web : Next.js 16, TypeScript, API REST
- Scripts audio : librosa, mutagen, pydub

PRINCIPES CLEAN CODE :
- Noms de variables/fonctions explicites
- Fonctions courtes et mono-responsabilité
- Commentaires pour le "pourquoi", pas le "quoi"
- Gestion d'erreurs explicite (pas de try/catch silencieux)
- Tests pour les chemins critiques

DÉCLENCHEURS :
- "programme C++" → développement C/C++ avec workflow propre
- "développement C/C++" → architecture + implémentation + tests
- Tâches nécessitant un code de qualité production

INTÉGRATION AVEC AUTRES AGENTS :
- python-executor : pour l'exécution de scripts créés par coding-agent
- pdf-expert : pour la documentation technique
- auto-tagger : pour les scripts d'analyse audio

Cet agent est disponible uniquement en mode Codage et se distingue de python-executor par son focus sur la qualité du code.""",
        "category": "agent",
        "tags": "coding-agent,développement,c++,python,workflow,clean-code,tests,qualité",
        "priority": "important",
        "source": "imported",
        "pinned": False,
    },

    # ─── SCRIPTS UTILITAIRES ───────────────────────────
    {
        "title": "Scripts Utilitaires — Écosystème",
        "content": """Scripts utilitaires de l'écosystème pour l'automatisation et la maintenance.

1. launcher.py (v3.0.0) :
Lanceur multi-contexte IA avec auto-détection. Supporte 9 IAs et 2 contextes (système/codage). Copie automatiquement le prompt maître adapté dans le presse-papier et ouvre le navigateur vers l'IA sélectionnée. Historique des sessions et config persistante.

2. setup-aliases.sh :
Installation d'alias shell pour un accès rapide aux commandes du launcher. Alias principaux : ai, sys, code, sys-zai, sys-qwen, code-qwen, ai-config, ai-list. À sourcer dans ~/.bashrc après installation.

3. analyze_logs.py :
Script Python d'analyse de logs système. Analyse les fichiers de log pour détecter des patterns d'erreurs, des anomalies de performance, et des problèmes récurrents. Utile pour le diagnostic système en mode ingénieur.

4. configure-memory-zai.sh :
Script shell pour configurer automatiquement la mémoire de z.ai. Automatise le processus de copie du prompt maître dans la configuration mémoire de z.ai.

5. configure-memory-qwen.sh :
Script shell pour configurer automatiquement la mémoire de Qwen. Similaire à configure-memory-zai.sh mais adapté à l'interface Qwen.

6. install-memory.sh / install-memory-config.sh :
Scripts d'installation pour déployer les fichiers de configuration mémoire dans les répertoires appropriés. Automatisent la copie des fichiers prompt-maître, context, et config mémoire.

EMPLACEMENT : /home/z/my-project/upload/gen-plan-ecosysteme/
UTILISATION : bash <script>.sh ou python3 <script>.py

Ces scripts facilitent le déploiement et la maintenance quotidienne de l'écosystème.""",
        "category": "other",
        "tags": "scripts,utilitaires,launcher,aliases,logs,installation,automatisation,shell",
        "priority": "normal",
        "source": "imported",
        "pinned": False,
    },
]


# ═══════════════════════════════════════════════════════
# BOUCLE D'INTÉGRATION AVEC TESTS
# ═══════════════════════════════════════════════════════

def main():
    print(f"\n{'='*60}")
    print(f"INTÉGRATION KNOWLEDGE — {len(ENTRIES)} entrées à tester et intégrer")
    print(f"{'='*60}\n")
    
    success_count = 0
    fail_count = 0
    skip_count = 0
    results = []
    
    for i, entry in enumerate(ENTRIES, 1):
        title = entry["title"]
        print(f"\n[{i}/{len(ENTRIES)}] 📋 {title}")
        
        # ══ TEST 1 : Validation du contenu ══
        valid, errors = validate_entry(entry)
        if not valid:
            print(f"  ❌ VALIDATION ÉCHOUÉE :")
            for err in errors:
                print(f"     - {err}")
            fail_count += 1
            results.append({"title": title, "status": "VALIDATION_FAIL", "errors": errors})
            continue
        
        print(f"  ✅ Validation OK (contenu: {len(entry['content'])} chars)")
        
        # ══ TEST 2 : Vérifier doublon (même titre) ══
        try:
            check_resp = urllib.request.urlopen(f"{API_BASE}?search={urllib.parse.quote(title[:30])}", timeout=5)
            existing = json.load(check_resp)
            duplicates = [e for e in existing if e["title"] == title]
            if duplicates:
                print(f"  ⚠️  DOUBLON détecté — entrée '{title}' existe déjà (id: {duplicates[0]['id']})")
                skip_count += 1
                results.append({"title": title, "status": "DUPLICATE_SKIP", "id": duplicates[0]['id']})
                continue
        except Exception as e:
            print(f"  ⚠️  Vérification doublon impossible: {e}")
        
        # ══ TEST 3 : Insertion via API ══
        ok, resp = test_api_post(entry)
        if not ok:
            print(f"  ❌ INSERTION ÉCHOUÉE : {resp}")
            fail_count += 1
            results.append({"title": title, "status": "INSERT_FAIL", "error": str(resp)})
            continue
        
        # ══ TEST 4 : Vérification post-insertion ══
        ok_verify, verify_errors = verify_entry_after_insert(entry, resp)
        if not ok_verify:
            print(f"  ⚠️  VÉRIFICATION POST-INSERTION :")
            for err in verify_errors:
                print(f"     - {err}")
            # On ne supprime pas, mais on signale
            results.append({"title": title, "status": "INSERTED_WITH_WARNINGS", "id": resp.get("id"), "warnings": verify_errors})
        else:
            print(f"  ✅ Inséré et vérifié (id: {resp.get('id')})")
            results.append({"title": title, "status": "OK", "id": resp.get("id")})
        
        success_count += 1
        
        # Petit délai pour ne pas surcharger
        time.sleep(0.1)
    
    # ══════════════════════════════════════════════════
    # BILAN FINAL
    # ══════════════════════════════════════════════════
    print(f"\n{'='*60}")
    print(f"BILAN D'INTÉGRATION")
    print(f"{'='*60}")
    print(f"  ✅ Succès :  {success_count}")
    print(f"  ⚠️  Doublons : {skip_count}")
    print(f"  ❌ Échecs :   {fail_count}")
    print(f"  📊 Total :    {len(ENTRIES)}")
    
    if fail_count > 0:
        print(f"\n❌ ENTRÉES EN ÉCHEC :")
        for r in results:
            if r["status"] in ["VALIDATION_FAIL", "INSERT_FAIL"]:
                print(f"  - {r['title']}: {r['status']}")
                if 'errors' in r:
                    for e in r['errors']:
                        print(f"    → {e}")
                if 'error' in r:
                    print(f"    → {r['error']}")
    
    print(f"\n✅ ENTRÉES INTÉGRÉES :")
    for r in results:
        if r["status"] in ["OK", "INSERTED_WITH_WARNINGS"]:
            print(f"  - {r['title']} (id: {r.get('id','?')})")
    
    if skip_count > 0:
        print(f"\n⚠️  DOUBLONS IGNORÉS :")
        for r in results:
            if r["status"] == "DUPLICATE_SKIP":
                print(f"  - {r['title']}")
    
    return fail_count == 0


if __name__ == "__main__":
    import urllib.parse
    success = main()
    sys.exit(0 if success else 1)
