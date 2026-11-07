import { NextRequest, NextResponse } from "next/server"
import { db } from "@/lib/db"

type Params = { params: Promise<{ id: string }> }

export async function GET(_req: NextRequest, { params }: Params) {
  const { id } = await params
  const projet = await db.project.findUnique({ where: { id }, include: { audits: { orderBy: { createdAt: "desc" }, take: 50 } } })
  if (!projet) return NextResponse.json({ error: "projet introuvable" }, { status: 404 })
  return NextResponse.json({ projet })
}

export async function PATCH(req: NextRequest, { params }: Params) {
  const { id } = await params
  const body = await req.json().catch(() => null)
  if (!body || typeof body.data !== "string") {
    return NextResponse.json({ error: "corps attendu : { data: \"<JSON string>\" }" }, { status: 400 })
  }
  try {
    JSON.parse(body.data)
  } catch {
    return NextResponse.json({ error: "data n'est pas un JSON valide" }, { status: 400 })
  }
  const projet = await db.project.update({ where: { id }, data: { data: body.data } })
  return NextResponse.json({ projet })
}

export async function DELETE(_req: NextRequest, { params }: Params) {
  const { id } = await params
  await db.project.delete({ where: { id } })
  return NextResponse.json({ ok: true })
}
