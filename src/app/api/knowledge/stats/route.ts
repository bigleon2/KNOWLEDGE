import { db } from '@/lib/db'
import { NextResponse } from 'next/server'

export async function GET() {
  try {
    const total = await db.knowledgeEntry.count()
    const pinned = await db.knowledgeEntry.count({ where: { pinned: true } })

    const categories = await db.knowledgeEntry.groupBy({
      by: ['category'],
      _count: { category: true },
    })

    const priorities = await db.knowledgeEntry.groupBy({
      by: ['priority'],
      _count: { priority: true },
    })

    const categoryStats = categories.reduce((acc, c) => {
      acc[c.category] = c._count.category
      return acc
    }, {} as Record<string, number>)

    const priorityStats = priorities.reduce((acc, p) => {
      acc[p.priority] = p._count.priority
      return acc
    }, {} as Record<string, number>)

    return NextResponse.json({
      total,
      pinned,
      categories: categoryStats,
      priorities: priorityStats,
    })
  } catch (error) {
    console.error('Error fetching stats:', error)
    return NextResponse.json({ error: 'Failed to fetch stats' }, { status: 500 })
  }
}
