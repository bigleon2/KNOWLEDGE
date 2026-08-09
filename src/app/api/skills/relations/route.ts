import { NextResponse } from 'next/server'
import { getRelations, getAllSkills } from '@/lib/skills-reader'

export async function GET() {
  try {
    const skills = getAllSkills()
    const relations = getRelations()
    const nodes = skills.map(s => ({
      id: s.slug,
      name: s.name,
      category: s.category,
      version: s.version,
      language: s.language,
      tags: s.tags,
      dependencies: s.dependencies,
    }))

    return NextResponse.json({ nodes, edges: relations })
  } catch (error) {
    console.error('Error reading relations:', error)
    return NextResponse.json({ error: 'Failed to read relations' }, { status: 500 })
  }
}
