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
        title: 'Écosystème Knowledge',
        content: 'Écosystème de 78 skills (6 écosystème + 72 métier) avec registre KB central (skills/KNOWLEDGE.md), versions semver, cross-refs bidirectionnelles. Pipeline gen-plan v3.6.1 (15 étapes, 4 modes), correct-work v2.4.0 (5 étapes, 3 modes), clone-chat v2.0.0 (7+1 étapes). Verification automatisée : 81 checks (verify-cross 60 + verify-correct-work 16 + sync-download 5).',
        category: 'agent',
        tags: 'orchestration,écosystème,78-skills,knowledge,gen-plan,correct-work,clone-chat',
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
        title: 'Skills Écosystème (6 skills)',
        content: 'Skills de l\'écosystème Knowledge :\n- gen-plan v3.6.1 (15 étapes, 4 modes, 3 profils) : orchestration et planification\n- correct-work v2.4.0 (5 étapes, 3 modes, sévérité S1-S4) : vérification et correction\n- clone-chat v2.0.0 (7+1 étapes) : sauvegarde et clonage de sessions\n- autonomous-agent v1.0.0 (5 modules, pipeline A-H) : agents autonomes avec mémoire\n- skills-inventory : découverte et catalogue des skills disponibles\n- task-review : sauvegarde de tâches en skills réutilisables',
        category: 'skill',
        tags: 'skills,écosystème,gen-plan,correct-work,clone-chat,autonomous-agent,6-skills',
        priority: 'critical',
        source: 'imported',
        pinned: true,
      },
      {
        title: 'Skills Métier (72 skills)',
        content: '72 skills métier disponibles :\n- Dev : fullstack-dev, coding-agent, cpp-analysis\n- Documents : pdf, pdf-llm, docx, pptx, xlsx, charts\n- AI : LLM, VLM, TTS, ASR, image-generation, image-edit\n- Recherche : web-search, web-reader, literature-survey, research-explorer\n- Contenu : blog-writer, seo-content-writer, marketing-mode, content-strategy\n- Emploi : resume-builder, interview-prep, jd-resume-tailor, job-intent-tracker\n- Data : finance, stock-analysis-skill, aminer-*, gaokao-*\n- Autres : design, video-generation, audio-metadata, dream-interpreter, etc.',
        category: 'skill',
        tags: 'skills,métier,72-skills,fullstack,documents,ai,recherche,contenu',
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
        content: 'Utiliser les 78 skills de l\'écosystème Knowledge quand pertinent. Chaque skill est versionné semver, avec dépendances déclarées et cross-refs bidirectionnelles dans le registre KB (skills/KNOWLEDGE.md).',
        category: 'rule',
        tags: 'règle,skills,78-skills,écosystème,knowledge,KNOWLEDGE',
        priority: 'important',
        source: 'imported',
        pinned: false,
      },
      {
        title: 'Règles d\'Or - Règle 8',
        content: 'Vérifier l\'écosystème avec les scripts automatisés avant tout push : sync-download.py (5 checks), verify-cross.py (60 checks), verify-correct-work.py (16 checks). Le verdict doit être 81/81 PASS avant de considérer le travail comme terminé.',
        category: 'rule',
        tags: 'règle,vérification,81-checks,scripts,automatisé,quality-gate',
        priority: 'critical',
        source: 'imported',
        pinned: false,
      },
      {
        title: 'Outils d\'Intégration',
        content: 'Scripts de l\'écosystème :\n- scripts/git-deploy.sh : automatisation commit+push (4 modes : --status, --auto, --push-only, interactif)\n- scripts/sync-download.py : synchronisation _prompts-maitres/ ↔ download/\n- scripts/verify-cross.py : 60 checks de cohérence cross-fichiers\n- scripts/spell-check.py : vérification orthographique avec lexique dynamique\n- scripts/generate-clone-genplan.py : génération de clone-chat.zip\n- download/clone-chat.zip : archive complète de l\'écosystème (23 fichiers)',
        category: 'protocol',
        tags: 'outils,scripts,git-deploy,sync,verify,spell-check,clone-chat-zip',
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
