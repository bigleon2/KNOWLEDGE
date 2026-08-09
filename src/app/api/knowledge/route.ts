import { db } from '@/lib/db'
import { NextResponse } from 'next/server'

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url)
    const category = searchParams.get('category')
    const search = searchParams.get('search')
    const pinned = searchParams.get('pinned')

    const where: Record<string, unknown> = {}

    if (category && category !== 'all') {
      where.category = category
    }

    if (search) {
      where.OR = [
        { title: { contains: search } },
        { content: { contains: search } },
        { tags: { contains: search } },
      ]
    }

    if (pinned === 'true') {
      where.pinned = true
    }

    const entries = await db.knowledgeEntry.findMany({
      where,
      orderBy: [
        { pinned: 'desc' },
        { priority: 'asc' },
        { updatedAt: 'desc' },
      ],
    })

    return NextResponse.json(entries)
  } catch (error) {
    console.error('Error fetching knowledge entries:', error)
    return NextResponse.json({ error: 'Failed to fetch entries' }, { status: 500 })
  }
}

export async function POST(request: Request) {
  try {
    const body = await request.json()
    const { title, content, category, tags, priority, source, pinned } = body

    if (!title || !content || !category) {
      return NextResponse.json(
        { error: 'Title, content, and category are required' },
        { status: 400 }
      )
    }

    const entry = await db.knowledgeEntry.create({
      data: {
        title,
        content,
        category,
        tags: tags || '',
        priority: priority || 'normal',
        source: source || 'manual',
        pinned: pinned || false,
      },
    })

    return NextResponse.json(entry, { status: 201 })
  } catch (error) {
    console.error('Error creating knowledge entry:', error)
    return NextResponse.json({ error: 'Failed to create entry' }, { status: 500 })
  }
}

export async function PUT(request: Request) {
  try {
    const body = await request.json()
    const { id, title, content, category, tags, priority, source, pinned } = body

    if (!id) {
      return NextResponse.json({ error: 'ID is required' }, { status: 400 })
    }

    const entry = await db.knowledgeEntry.update({
      where: { id },
      data: {
        ...(title !== undefined && { title }),
        ...(content !== undefined && { content }),
        ...(category !== undefined && { category }),
        ...(tags !== undefined && { tags }),
        ...(priority !== undefined && { priority }),
        ...(source !== undefined && { source }),
        ...(pinned !== undefined && { pinned }),
      },
    })

    return NextResponse.json(entry)
  } catch (error) {
    console.error('Error updating knowledge entry:', error)
    return NextResponse.json({ error: 'Failed to update entry' }, { status: 500 })
  }
}

export async function DELETE(request: Request) {
  try {
    const { searchParams } = new URL(request.url)
    const id = searchParams.get('id')

    if (!id) {
      return NextResponse.json({ error: 'ID is required' }, { status: 400 })
    }

    await db.knowledgeEntry.delete({ where: { id } })
    return NextResponse.json({ success: true })
  } catch (error) {
    console.error('Error deleting knowledge entry:', error)
    return NextResponse.json({ error: 'Failed to delete entry' }, { status: 500 })
  }
}
