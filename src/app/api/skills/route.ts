import { NextResponse } from 'next/server'
import { getAllSkills, getSkillsStats, getSkillBySlug } from '@/lib/skills-reader'

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url)
    const slug = searchParams.get('slug')
    const category = searchParams.get('category')
    const search = searchParams.get('search')
    const lang = searchParams.get('lang')
    const stats = searchParams.get('stats')

    // Stats endpoint
    if (stats === 'true') {
      return NextResponse.json(getSkillsStats())
    }

    // Single skill detail
    if (slug) {
      const skill = getSkillBySlug(slug)
      if (!skill) {
        return NextResponse.json({ error: 'Skill not found' }, { status: 404 })
      }
      return NextResponse.json(skill)
    }

    // List with filters
    let skills = getAllSkills()

    if (category && category !== 'all') {
      skills = skills.filter(s => s.category === category)
    }

    if (lang && lang !== 'all') {
      skills = skills.filter(s => s.language === lang)
    }

    if (search) {
      const q = search.toLowerCase()
      skills = skills.filter(s =>
        s.name.toLowerCase().includes(q) ||
        s.description.toLowerCase().includes(q) ||
        s.tags.some(t => t.toLowerCase().includes(q))
      )
    }

    return NextResponse.json({
      total: skills.length,
      skills,
    })
  } catch (error) {
    console.error('Error reading skills:', error)
    return NextResponse.json({ error: 'Failed to read skills' }, { status: 500 })
  }
}
