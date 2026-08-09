import fs from 'fs'
import path from 'path'

const SKILLS_ROOT = path.join(process.cwd(), 'skills')

// Ecosystem skill names (those with category: ecosystem or known by convention)
const ECOSYSTEM_SKILLS = new Set([
  'gen-plan',
  'correct-work',
  'clone-chat',
  'skills-inventory',
  'skill-creator',
  'autonomous-agent',
  'task-review',
])

export interface Skill {
  name: string
  slug: string
  version: string
  category: 'ecosystem' | 'metier'
  language: string
  description: string
  tags: string[]
  dependencies: string[]
  hasReferences: boolean
  hasScripts: boolean
  hasEvals: boolean
  fileCount: number
  totalSize: number
  contentPreview: string
}

export interface SkillDetail extends Skill {
  files: { path: string; size: number; type: 'skill' | 'script' | 'reference' | 'eval' | 'asset' | 'other' }[]
  fullDescription: string
}

function parseFrontmatter(content: string): Record<string, unknown> {
  const match = content.match(/^---\n([\s\S]*?)\n---/)
  if (!match) return {}
  try {
    // Simple YAML-like parser (not a full YAML parser, but handles our formats)
    const yaml = match[1]
    const result: Record<string, unknown> = {}
    let currentKey = ''
    let currentList: string[] = []
    let inList = false
    let currentObj: Record<string, unknown> | null = null
    let currentObjKey = ''
    let inObj = false

    const lines = yaml.split('\n')
    for (const line of lines) {
      // List item
      const listMatch = line.match(/^\s+-\s+(.+)/)
      if (listMatch) {
        if (inObj && currentObj) {
          // Inside an object, list items are values of the last key
          const val = listMatch[1].replace(/^['"]|['"]$/g, '').trim()
          currentList.push(val)
          currentObj[currentObjKey] = [...currentList]
        } else if (inList) {
          currentList.push(listMatch[1].replace(/^['"]|['"]$/g, '').trim())
          result[currentKey] = [...currentList]
        }
        continue
      }

      // Nested object key (e.g., "  author: Z.AI")
      const nestedMatch = line.match(/^\s+(\w[\w-]*):\s*(.*)/)
      if (nestedMatch && inObj && currentObj) {
        const key = nestedMatch[1]
        const val = nestedMatch[2].replace(/^['"]|['"]$/g, '').trim()
        if (val) {
          currentObj[key] = val
          currentList = []
          currentObjKey = key
          inList = false
        } else {
          currentList = []
          currentObjKey = key
          inList = true
        }
        continue
      }

      // Top-level key
      const keyMatch = line.match(/^(\w[\w-]*):\s*(.*)/)
      if (keyMatch) {
        // Save previous
        if (inObj && currentObj) {
          result[currentKey] = currentObj
        } else if (inList) {
          result[currentKey] = [...currentList]
        }

        currentKey = keyMatch[1]
        const val = keyMatch[2].replace(/^['"]|['"]$/g, '').trim()

        if (val === '' || val === '|' || val === '>') {
          // Could be a list or object below
          inList = true
          currentList = []
          inObj = true
          currentObj = {}
          currentObjKey = ''
        } else {
          result[currentKey] = val
          inList = false
          inObj = false
          currentObj = null
        }
        continue
      }
    }

    // Save last
    if (inObj && currentObj) {
      result[currentKey] = currentObj
    } else if (inList) {
      result[currentKey] = [...currentList]
    }

    return result
  } catch {
    return {}
  }
}

function extractDescription(content: string, frontmatter: Record<string, unknown>): { short: string; full: string } {
  // Try to get description from frontmatter first
  let desc = ''
  const fm = frontmatter
  if (typeof fm.description === 'string') {
    desc = fm.description
  }

  // If no frontmatter description, extract from body (first non-heading paragraph)
  if (!desc) {
    const body = content.replace(/^---[\s\S]*?---\n/, '')
    const lines = body.split('\n').filter(l => l.trim() && !l.startsWith('#'))
    desc = lines.slice(0, 3).join(' ').trim()
  }

  const full = desc
  const short = desc.length > 200 ? desc.slice(0, 200) + '...' : desc
  return { short, full }
}

function getFileType(filePath: string): 'skill' | 'script' | 'reference' | 'eval' | 'asset' | 'other' {
  const dir = path.dirname(filePath).split('/').pop() || ''
  const ext = path.extname(filePath)
  if (filePath.endsWith('SKILL.md')) return 'skill'
  if (dir === 'scripts' || dir === 'mini-services') return 'script'
  if (dir === 'references') return 'reference'
  if (dir === 'evals') return 'eval'
  if (dir === 'assets' || dir === 'data' || ['.png', '.jpg', '.svg', '.ico', '.csv'].includes(ext)) return 'asset'
  return 'other'
}

function walkDir(dir: string, base: string): { path: string; size: number }[] {
  const files: { path: string; size: number }[] = []
  try {
    const entries = fs.readdirSync(dir, { withFileTypes: true })
    for (const entry of entries) {
      const full = path.join(dir, entry.name)
      if (entry.name.startsWith('.') || entry.name === 'node_modules' || entry.name === '__pycache__') continue
      if (entry.isDirectory()) {
        files.push(...walkDir(full, base))
      } else {
        try {
          files.push({ path: path.relative(base, full), size: fs.statSync(full).size })
        } catch {
          // skip unreadable
        }
      }
    }
  } catch {
    // skip
  }
  return files
}

export function getAllSkills(): Skill[] {
  const dirs = fs.readdirSync(SKILLS_ROOT, { withFileTypes: true })
    .filter(d => d.isDirectory() && !d.name.startsWith('.') && d.name !== 'node_modules' && d.name !== '__pycache__')
    .map(d => d.name)
    .sort()

  return dirs.map(slug => {
    const skillPath = path.join(SKILLS_ROOT, slug, 'SKILL.md')
    const content = fs.existsSync(skillPath) ? fs.readFileSync(skillPath, 'utf-8') : ''
    const fm = parseFrontmatter(content)
    const { short, full } = extractDescription(content, fm)

    // Extract version from various formats
    let version = '—'
    const meta = fm.metadata as Record<string, unknown> | undefined
    if (typeof fm.version === 'string') version = fm.version
    else if (meta && typeof meta.version === 'string') version = meta.version
    else if (meta && typeof meta.version === 'number') version = String(meta.version)

    // Determine category
    let category: 'ecosystem' | 'metier' = ECOSYSTEM_SKILLS.has(slug) ? 'ecosystem' : 'metier'
    if (typeof fm.category === 'string') {
      if (fm.category === 'ecosystem' || fm.category === 'écosystème') category = 'ecosystem'
      else if (fm.category === 'metier' || fm.category === 'métier') category = 'metier'
    }

    // Language
    const language = typeof fm.language === 'string' ? fm.language : (short.match(/[\u4e00-\u9fff]/) ? 'zh' : 'en')

    // Tags
    let tags: string[] = []
    if (Array.isArray(fm.tags)) tags = fm.tags.filter((t): t is string => typeof t === 'string')
    if (typeof fm.tags === 'string') tags = fm.tags.split(',').map(t => t.trim()).filter(Boolean)

    // Dependencies
    let dependencies: string[] = []
    if (Array.isArray(fm.dependencies)) dependencies = fm.dependencies.filter((t): t is string => typeof t === 'string')
    if (typeof fm.dependencies === 'string') dependencies = fm.dependencies.split(',').map(t => t.trim()).filter(Boolean)

    // Directory analysis
    const skillDir = path.join(SKILLS_ROOT, slug)
    const files = walkDir(skillDir, SKILLS_ROOT)
    const fileCount = files.length
    const totalSize = files.reduce((s, f) => s + f.size, 0)
    const hasReferences = files.some(f => getFileType(f.path) === 'reference')
    const hasScripts = files.some(f => getFileType(f.path) === 'script')
    const hasEvals = files.some(f => getFileType(f.path) === 'eval')

    return {
      name: (typeof fm.name === 'string' ? fm.name : slug),
      slug,
      version,
      category,
      language,
      description: short,
      tags,
      dependencies,
      hasReferences,
      hasScripts,
      hasEvals,
      fileCount,
      totalSize,
      contentPreview: full,
    }
  })
}

export function getSkillBySlug(slug: string): SkillDetail | null {
  const skillDir = path.join(SKILLS_ROOT, slug)
  const skillPath = path.join(skillDir, 'SKILL.md')
  if (!fs.existsSync(skillPath)) return null

  const content = fs.readFileSync(skillPath, 'utf-8')
  const fm = parseFrontmatter(content)
  const { short, full } = extractDescription(content, fm)

  let version = '—'
  const meta = fm.metadata as Record<string, unknown> | undefined
  if (typeof fm.version === 'string') version = fm.version
  else if (meta && typeof meta.version === 'string') version = meta.version

  let category: 'ecosystem' | 'metier' = ECOSYSTEM_SKILLS.has(slug) ? 'ecosystem' : 'metier'
  if (typeof fm.category === 'string') {
    if (fm.category === 'ecosystem' || fm.category === 'écosystème') category = 'ecosystem'
    else category = 'metier'
  }

  const language = typeof fm.language === 'string' ? fm.language : (short.match(/[\u4e00-\u9fff]/) ? 'zh' : 'en')

  let tags: string[] = []
  if (Array.isArray(fm.tags)) tags = fm.tags.filter((t): t is string => typeof t === 'string')
  if (typeof fm.tags === 'string') tags = fm.tags.split(',').map(t => t.trim()).filter(Boolean)

  let dependencies: string[] = []
  if (Array.isArray(fm.dependencies)) dependencies = fm.dependencies.filter((t): t is string => typeof t === 'string')
  if (typeof fm.dependencies === 'string') dependencies = fm.dependencies.split(',').map(t => t.trim()).filter(Boolean)

  const files = walkDir(skillDir, SKILLS_ROOT).map(f => ({
    ...f,
    type: getFileType(f.path),
  }))
  const fileCount = files.length
  const totalSize = files.reduce((s, f) => s + f.size, 0)
  const hasReferences = files.some(f => f.type === 'reference')
  const hasScripts = files.some(f => f.type === 'script')
  const hasEvals = files.some(f => f.type === 'eval')

  return {
    name: (typeof fm.name === 'string' ? fm.name : slug),
    slug,
    version,
    category,
    language,
    description: short,
    tags,
    dependencies,
    hasReferences,
    hasScripts,
    hasEvals,
    fileCount,
    totalSize,
    contentPreview: full,
    fullDescription: full,
    files,
  }
}

export function getSkillsStats() {
  const skills = getAllSkills()
  const ecosystem = skills.filter(s => s.category === 'ecosystem')
  const metier = skills.filter(s => s.category === 'metier')

  const languages: Record<string, number> = {}
  skills.forEach(s => { languages[s.language] = (languages[s.language] || 0) + 1 })

  const totalFiles = skills.reduce((s, sk) => s + sk.fileCount, 0)
  const totalSize = skills.reduce((s, sk) => s + sk.totalSize, 0)
  const withRefs = skills.filter(s => s.hasReferences).length
  const withScripts = skills.filter(s => s.hasScripts).length
  const withEvals = skills.filter(s => s.hasEvals).length
  const withDeps = skills.filter(s => s.dependencies.length > 0).length
  const withTags = skills.filter(s => s.tags.length > 0).length

  // Build dependency graph
  const depGraph: Record<string, string[]> = {}
  skills.forEach(s => {
    if (s.dependencies.length > 0) depGraph[s.slug] = s.dependencies
  })

  return {
    total: skills.length,
    ecosystem: ecosystem.length,
    metier: metier.length,
    languages,
    totalFiles,
    totalSize,
    withReferences: withRefs,
    withScripts,
    withEvals,
    withDeps,
    withTags,
    dependencyGraph: depGraph,
  }
}

export function getRelations() {
  // Build relations from dependencies + known ecosystem relationships
  const skills = getAllSkills()
  const relations: { source: string; target: string; type: 'depends_on' | 'used_by' | 'related' }[] = []

  const slugMap: Record<string, string> = {}
  skills.forEach(s => { slugMap[s.slug] = s.name })

  // Dependency relations
  skills.forEach(s => {
    s.dependencies.forEach(dep => {
      // Normalize dep name to slug
      const depSlug = dep.toLowerCase().replace(/[\s_]+/g, '-')
      relations.push({ source: s.slug, target: depSlug, type: 'depends_on' })
      relations.push({ source: depSlug, target: s.slug, type: 'used_by' })
    })
  })

  // Known ecosystem relations (from KNOWLEDGE.md conventions)
  const knownRelations: [string, string][] = [
    ['gen-plan', 'correct-work'],
    ['gen-plan', 'clone-chat'],
    ['correct-work', 'gen-plan'],
    ['correct-work', 'clone-chat'],
    ['skills-inventory', 'autonomous-agent'],
    ['skill-creator', 'skills-inventory'],
    ['task-review', 'skill-creator'],
    ['autonomous-agent', 'gen-plan'],
    ['autonomous-agent', 'correct-work'],
  ]

  knownRelations.forEach(([a, b]) => {
    if (slugMap[a] && slugMap[b]) {
      const exists = relations.some(r =>
        (r.source === a && r.target === b) || (r.source === b && r.target === a)
      )
      if (!exists) {
        relations.push({ source: a, target: b, type: 'related' })
      }
    }
  })

  // Deduplicate
  const seen = new Set<string>()
  return relations.filter(r => {
    const key = [r.source, r.target, r.type].join('→')
    if (seen.has(key)) return false
    seen.add(key)
    return true
  })
}
