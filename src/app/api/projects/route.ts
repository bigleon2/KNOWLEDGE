import { NextRequest, NextResponse } from "next/server"
import { db } from "@/lib/db"

export async function GET() {
  const projets = await db.project.findMany({ orderBy: { updatedAt: "desc" } })
  return NextResponse.json({ projets })
}

export async function POST(req: NextRequest) {
  const body = await req.json().catch(() => null)
  if (!body || typeof body.name !== "string" || !body.name.trim()) {
    return NextResponse.json({ error: "name requis" }, { status: 400 })
  }
  const data = JSON.stringify(
    body.data ?? {
      device: {
        name: "Traktor Kontrol S4 MK2", type: "MIDI",
        in_port: "Traktor Kontrol S4 MK2 In", out_port: "Traktor Kontrol S4 MK2 Out",
        deck_target: "Focus",
      },
      mappings: [],
    },
  )
  const projet = await db.project.create({ data: { name: body.name.trim(), data } })
  return NextResponse.json({ projet }, { status: 201 })
}
