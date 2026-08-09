import { db } from '@/lib/db'
import { NextResponse } from 'next/server'

export async function POST() {
  try {
    const existing = await db.memoryConfig.count()
    if (existing > 0) {
      return NextResponse.json({ message: 'Already seeded', count: existing })
    }

    const configs = [
      // ── Profile ──
      { key: 'user.name', value: 'François', category: 'profile', description: "Nom de l'utilisateur" },
      { key: 'user.dj_setup', value: 'KONTROL S4 MK32 + TRAKTOR PRO 3.11', category: 'profile', description: 'Configuration DJ matérielle et logicielle' },
      { key: 'user.location', value: 'France', category: 'profile', description: "Localisation de l'utilisateur" },
      { key: 'user.skills_level', value: 'Notions C/C++, Python intermédiaire, administration système', category: 'profile', description: 'Niveau de compétences techniques' },
      { key: 'user.interests', value: 'Conception de petits programmes, analyse de code, automatisation DJ', category: 'profile', description: "Centres d'intérêt techniques" },
      { key: 'user.language', value: 'français', category: 'profile', description: 'Langue de communication préférée' },

      // ── Ecosystem ──
      { key: 'ecosystem.agents_count', value: '12', category: 'ecosystem', description: 'Nombre total d\'agents (6 spécialisés + 6 génériques)' },
      { key: 'ecosystem.skills_count', value: '71', category: 'ecosystem', description: 'Nombre total de skills installés' },
      { key: 'ecosystem.specialized_agents', value: 'tsi-expert, kontrol-s4-expert, python-executor, pdf-expert, image-analyst, auto-tagger', category: 'ecosystem', description: 'Agents spécialisés DJ/Système' },
      { key: 'ecosystem.generic_agents', value: 'general-purpose, Explore, Plan, frontend-styling-expert, full-stack-developer, ppt-expert', category: 'ecosystem', description: 'Agents génériques' },
      { key: 'ecosystem.ia_supported', value: 'z.ai, qwen, manus, copilot, chatgpt, perplexity, gemini, claude, codex', category: 'ecosystem', description: 'IA supportées par l\'écosystème' },

      // ── Gen-Plan ──
      { key: 'gen-plan.version', value: '1.0.0', category: 'gen-plan', description: 'Version du protocole gen-plan' },
      { key: 'gen-plan.steps_count', value: '11', category: 'gen-plan', description: "Nombre d'étapes séquentielles" },
      { key: 'gen-plan.triggers', value: 'gen-plan:, plan d\'actions, orchestre', category: 'gen-plan', description: 'Mots-clés déclencheurs du protocole' },
      { key: 'gen-plan.confirmation', value: 'Mémoire configurée pour François - DJ TRAKTOR - 12 agents - 71 skills - gen-plan v1.0.0', category: 'gen-plan', description: 'Phrase de confirmation de la mémoire' },
      { key: 'gen-plan.modes', value: 'DIRECT, PROJET, CIBLE', category: 'gen-plan', description: "Modes d'exécution du protocole" },

      // ── Decision Matrix ──
      { key: 'decision.optimal', value: 'Skill + Agent spécialisé', category: 'decision', description: 'Combinaison performance optimale' },
      { key: 'decision.good', value: 'Skill seul', category: 'decision', description: 'Combinaison performance bonne' },
      { key: 'decision.moderate', value: 'Agent spécialisé seul', category: 'decision', description: 'Combinaison performance modérée' },
      { key: 'decision.last_resort', value: 'general-purpose', category: 'decision', description: 'Dernier recours' },

      // ── Rules ──
      { key: 'rules.count', value: '7', category: 'rules', description: "Nombre de règles d'or" },
      { key: 'rules.execution_mode', value: 'sériel par défaut', category: 'rules', description: "Mode d'exécution par défaut" },
      { key: 'rules.logging', value: 'worklog.md', category: 'rules', description: 'Fichier de log des phases' },
      { key: 'rules.language', value: 'français', category: 'rules', description: 'Langue de communication obligatoire' },

      // ── App ──
      { key: 'app.version', value: '1.0.0', category: 'app', description: 'Version de l\'application KNOWLEDGE' },
      { key: 'app.db_type', value: 'SQLite', category: 'app', description: 'Type de base de données' },
      { key: 'app.last_sync', value: new Date().toISOString(), category: 'app', description: 'Dernière synchronisation des configs' },
    ]

    const created = await db.memoryConfig.createMany({ data: configs })

    return NextResponse.json({
      message: 'Config seed completed successfully',
      count: created.count,
    })
  } catch (error) {
    console.error('Error seeding config:', error)
    return NextResponse.json({ error: 'Failed to seed config' }, { status: 500 })
  }
}
