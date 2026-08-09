import { db } from '@/lib/db'
import { NextResponse } from 'next/server'

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url)
    const category = searchParams.get('category')
    const key = searchParams.get('key')

    if (key) {
      const entry = await db.memoryConfig.findUnique({ where: { key } })
      if (!entry) {
        return NextResponse.json({ error: 'Config not found' }, { status: 404 })
      }
      return NextResponse.json(entry)
    }

    const where: Record<string, unknown> = {}
    if (category) {
      where.category = category
    }

    const entries = await db.memoryConfig.findMany({
      where,
      orderBy: [{ category: 'asc' }, { key: 'asc' }],
    })

    return NextResponse.json(entries)
  } catch (error) {
    console.error('Error fetching config:', error)
    return NextResponse.json({ error: 'Failed to fetch config' }, { status: 500 })
  }
}

export async function POST(request: Request) {
  try {
    const body = await request.json()
    const { key, value, category, description } = body

    if (!key || !value) {
      return NextResponse.json({ error: 'Key and value are required' }, { status: 400 })
    }

    const entry = await db.memoryConfig.create({
      data: {
        key,
        value,
        category: category || 'config',
        description: description || '',
      },
    })

    return NextResponse.json(entry, { status: 201 })
  } catch (error: unknown) {
    if (String(error).includes('Unique constraint')) {
      return NextResponse.json({ error: 'Key already exists. Use PUT to update.' }, { status: 409 })
    }
    console.error('Error creating config:', error)
    return NextResponse.json({ error: 'Failed to create config' }, { status: 500 })
  }
}

export async function PUT(request: Request) {
  try {
    const body = await request.json()
    const { key, value, category, description } = body

    if (!key) {
      return NextResponse.json({ error: 'Key is required' }, { status: 400 })
    }

    const entry = await db.memoryConfig.update({
      where: { key },
      data: {
        ...(value !== undefined && { value }),
        ...(category !== undefined && { category }),
        ...(description !== undefined && { description }),
      },
    })

    return NextResponse.json(entry)
  } catch (error: unknown) {
    if (String(error).includes('Record to update not found')) {
      return NextResponse.json({ error: 'Config key not found' }, { status: 404 })
    }
    console.error('Error updating config:', error)
    return NextResponse.json({ error: 'Failed to update config' }, { status: 500 })
  }
}

export async function DELETE(request: Request) {
  try {
    const { searchParams } = new URL(request.url)
    const key = searchParams.get('key')

    if (!key) {
      return NextResponse.json({ error: 'Key is required' }, { status: 400 })
    }

    await db.memoryConfig.delete({ where: { key } })
    return NextResponse.json({ success: true })
  } catch (error) {
    console.error('Error deleting config:', error)
    return NextResponse.json({ error: 'Failed to delete config' }, { status: 500 })
  }
}
