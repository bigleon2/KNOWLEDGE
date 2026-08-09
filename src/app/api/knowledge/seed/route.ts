import { db } from '@/lib/db'
import { NextResponse } from 'next/server'

export async function POST() {
  try {
    // Check if already seeded
    const existing = await db.knowledgeEntry.count()
    if (existing > 0) {
      return NextResponse.json({ message: 'Already seeded', count: existing })
    }

    // Seed from memory-config-zai.md content
    const entries = [
      {
        title: 'Profil Utilisateur - François',
        content: 'Je suis François, DJ avec KONTROL S4 MK32 + TRAKTOR PRO 3.11, France.\nCompétences : Notions C/C++, Python intermédiaire, administration système.\nIntérêts : Conception de petits programmes, analyse de code, automatisation DJ.\nLangue : Toujours communiquer en français.',
        category: 'profile',
        tags: 'francoçois,dj,traktor,profil,utilisateur',
        priority: 'critical',
        source: 'imported',
        pinned: true,
      },
      {
        title: 'Écosystème d\'Orchestration',
        content: 'Écosystème de 12 agents spécialisés et 71 skills pour l\'orchestration de tâches complexes. Ce système permet une orchestration intelligente des tâches en sélectionnant automatiquement l\'agent et le skill optimaux pour chaque besoin.',
        category: 'agent',
        tags: 'orchestration,écosystème,agents,skills',
        priority: 'critical',
        source: 'imported',
        pinned: true,
      },
      {
        title: 'Agent tsi-expert',
        content: 'Expert fichiers TSI (TRAKTOR mappings XML MIDI). Spécialisé dans la création, modification et analyse des fichiers de mapping TSI pour TRAKTOR. Capacité à manipuler les mappings XML MIDI pour configurer les contrôleurs DJ.',
        category: 'agent',
        tags: 'tsi,traktor,mapping,xml,midi',
        priority: 'important',
        source: 'imported',
        pinned: false,
      },
      {
        title: 'Agent kontrol-s4-expert',
        content: 'Expert KONTROL S4 MK2 hardware (drivers, firmware, MIDI, Haptic Drive). Spécialisé dans le matériel Native Instruments, la configuration des pilotes, les mises à jour firmware, le protocole MIDI et la technologie Haptic Drive des jog wheels.',
        category: 'agent',
        tags: 'kontrol-s4,mk2,hardware,firmware,midi,haptic',
        priority: 'important',
        source: 'imported',
        pinned: false,
      },
      {
        title: 'Agent python-executor',
        content: 'Exécution scripts Python (<py script.py>). Agent dédié à l\'exécution de scripts Python pour l\'automatisation, le traitement de données, et les tâches système. Commande rapide via <py script.py>.',
        category: 'agent',
        tags: 'python,script,exécution,automatisation',
        priority: 'important',
        source: 'imported',
        pinned: false,
      },
      {
        title: 'Agent pdf-expert',
        content: 'Génération/extraction/manipulation PDF. Agent spécialisé dans la création de documents PDF, l\'extraction de contenu textuel, et la manipulation avancée de fichiers PDF (fusion, division, formulaires).',
        category: 'agent',
        tags: 'pdf,génération,extraction,documents',
        priority: 'important',
        source: 'imported',
        pinned: false,
      },
      {
        title: 'Agent image-analyst',
        content: 'Analyse images (VLM, OCR, computer vision). Capacité d\'analyse visuelle via Vision Language Model, reconnaissance optique de caractères, et traitement d\'images par vision par ordinateur.',
        category: 'agent',
        tags: 'image,vlm,ocr,vision,analyse',
        priority: 'important',
        source: 'imported',
        pinned: false,
      },
      {
        title: 'Agent auto-tagger',
        content: 'Tagging audio automatique (BPM, clé, genre, bibliothèque DJ). Agent spécialisé dans l\'analyse et le tagging automatique de fichiers audio : détection du BPM, identification de la clé musicale, classification par genre, et gestion de bibliothèque DJ.',
        category: 'agent',
        tags: 'audio,tagging,bpm,clé,genre,bibliothèque,dj',
        priority: 'important',
        source: 'imported',
        pinned: false,
      },
      {
        title: 'Agents Génériques',
        content: 'general-purpose : Agent polyvalent pour tâches diverses\nExplore : Agent rapide d\'exploration de codebase\nPlan : Agent architecte pour la conception de plans d\'implémentation\nfrontend-styling-expert : Expert CSS/styling/animations/UI-UX\nfull-stack-developer : Développeur fullstack Next.js 16\nppt-expert : Expert création de présentations',
        category: 'agent',
        tags: 'générique,polyvalent,exploration,plan,frontend,fullstack',
        priority: 'normal',
        source: 'imported',
        pinned: false,
      },
      {
        title: 'Protocole GEN-PLAN',
        content: 'Quand je dis "gen-plan:", "plan d\'actions", ou "orchestre" :\n1. Collecte des demandes (explicites + implicites)\n2. Lecture du projet (structure, dépendances)\n3. Identification nature (type, technologies, architecture)\n4. Objectifs (liste mesurable)\n5. Décomposition sous-tâches atomiques\n6. Dépendances (séquentielles/parallèles)\n7. Priorisation (critique > important > secondaire)\n8. Risques (fallbacks)\n9. Structuration plan formel\n10. Validation (checklist 6 critères)\n11. Mise à jour prompt-master (mode PROJET)',
        category: 'protocol',
        tags: 'gen-plan,orchestration,plan,actions,séquentiel',
        priority: 'critical',
        source: 'imported',
        pinned: true,
      },
      {
        title: 'Matrice de Décision Performance-Driven',
        content: 'Matrice de décision pour le choix optimal agent/skill :\n- Skill + Agent spécialisé = OPTIMAL\n- Skill seul = BON\n- Agent spécialisé seul = MODÉRÉ\n- general-purpose = DERNIER RECOURS\n\nCette matrice guide la sélection du meilleur agent pour chaque tâche, en privilégiant toujours la combinaison skill+agent spécialisé.',
        category: 'protocol',
        tags: 'matrice,décision,performance,agent,skill,optimisation',
        priority: 'critical',
        source: 'imported',
        pinned: true,
      },
      {
        title: 'Déclencheurs Prioritaires',
        content: 'Déclencheurs et leur agent associé :\n- "gen-plan:", "plan d\'actions" → Orchestration multi-agents\n- "crée un mapping TSI", "analyse mon .tsi" → Agent tsi-expert\n- "mon jog wheel ne répond plus", "configure les stems" → Agent kontrol-s4-expert\n- "<py script.py>", "crée un script Python" → Agent python-executor\n- "tag mes fichiers audio", "analyse BPM/clé" → Agent auto-tagger\n- "génère un PDF", "extrais le texte" → Agent pdf-expert\n- "analyse cette image", "extrais le texte" → Agent image-analyst',
        category: 'trigger',
        tags: 'déclencheur,commande,routage,agent,trigger',
        priority: 'critical',
        source: 'imported',
        pinned: false,
      },
      {
        title: 'Skills Prioritaires (71 au total)',
        content: 'Skills prioritaires pour l\'usage de François :\n- fullstack-dev (Next.js 16, TypeScript, Tailwind) : développement web complet\n- pdf, pdf-llm (génération/extraction PDF) : manipulation documents\n- VLM, image-understand (analyse images) : vision par ordinateur\n- charts (visualisation données) : graphiques et diagrammes\n- web-search, web-reader (recherche web) : recherche d\'information\n- skill-creator, skills-inventory (gestion skills) : administration skills\n- gen-plan, correct-work (orchestration) : coordination tâches',
        category: 'skill',
        tags: 'skills,prioritaires,fullstack,pdf,vlm,charts,web,orchestration',
        priority: 'important',
        source: 'imported',
        pinned: false,
      },
      {
        title: 'Règles d\'Or - Règle 1',
        content: 'Toujours lire le projet/système avant de planifier. Cette règle fondamentale garantit que toute planification ou action est basée sur une compréhension complète du contexte existant, évitant les erreurs d\'assomption et les actions inutiles ou redondantes.',
        category: 'rule',
        tags: 'règle,lecture,projet,contexte,planification',
        priority: 'critical',
        source: 'imported',
        pinned: false,
      },
      {
        title: 'Règles d\'Or - Règle 2',
        content: 'Sélectionner l\'agent optimal selon la performance. Utiliser la matrice de décision performance-driven pour choisir le meilleur agent pour chaque tâche, en privilégiant toujours la combinaison skill + agent spécialisé pour un résultat optimal.',
        category: 'rule',
        tags: 'règle,agent,optimal,performance,sélection',
        priority: 'critical',
        source: 'imported',
        pinned: false,
      },
      {
        title: 'Règles d\'Or - Règle 3',
        content: 'Exécuter en mode sériel par défaut (une tâche à la fois). L\'exécution séquentielle garantit la qualité et la traçabilité de chaque étape, permettant de vérifier les outputs avant de passer à la tâche suivante.',
        category: 'rule',
        tags: 'règle,sériel,séquentiel,exécution,tâche',
        priority: 'important',
        source: 'imported',
        pinned: false,
      },
      {
        title: 'Règles d\'Or - Règle 4',
        content: 'Vérifier les outputs avant de continuer. Chaque résultat produit doit être validé avant de passer à l\'étape suivante, garantissant la qualité et la cohérence de l\'ensemble du processus.',
        category: 'rule',
        tags: 'règle,vérification,output,qualité,validation',
        priority: 'important',
        source: 'imported',
        pinned: false,
      },
      {
        title: 'Règles d\'Or - Règle 5',
        content: 'Logger chaque phase dans worklog. La traçabilité est essentielle : chaque action, décision et résultat doit être consigné dans le worklog partagé pour permettre le suivi et la coordination entre agents.',
        category: 'rule',
        tags: 'règle,worklog,log,traçabilité,suivi',
        priority: 'important',
        source: 'imported',
        pinned: false,
      },
      {
        title: 'Règles d\'Or - Règle 6',
        content: 'Communiquer clairement en français. Toute communication avec François doit être en français, conformément à sa préférence linguistique exprimée dans son profil.',
        category: 'rule',
        tags: 'règle,français,communication,langue',
        priority: 'important',
        source: 'imported',
        pinned: false,
      },
      {
        title: 'Règles d\'Or - Règle 7',
        content: 'Utiliser les 12 agents spécialisés quand pertinent. L\'écosystème complet d\'agents spécialisés doit être exploité au maximum pour tirer parti de l\'expertise spécifique de chacun, plutôt que de se limiter aux agents génériques.',
        category: 'rule',
        tags: 'règle,agents,spécialisés,écosystème,expertise',
        priority: 'important',
        source: 'imported',
        pinned: false,
      },
    ]

    const created = await db.knowledgeEntry.createMany({ data: entries })

    return NextResponse.json({
      message: 'Seed completed successfully',
      count: created.count,
    })
  } catch (error) {
    console.error('Error seeding knowledge:', error)
    return NextResponse.json({ error: 'Failed to seed' }, { status: 500 })
  }
}
