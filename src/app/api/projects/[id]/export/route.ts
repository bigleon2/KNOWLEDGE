import { NextRequest, NextResponse } from "next/server"
import { db } from "@/lib/db"
import { serializeTsi } from "@/lib/tsi/binary"

type Params = { params: Promise<{ id: string }> }

/** Export du mapping en .tsi canonique (téléchargement — importable dans Traktor). */
export async function GET(_req: NextRequest, { params }: Params) {
  const { id } = await params
  const projet = await db.project.findUnique({ where: { id } })
  if (!projet) return NextResponse.json({ error: "projet introuvable" }, { status: 404 })
  const tsi = serializeTsi(JSON.parse(projet.data))
  const nomFichier = `${projet.name.replace(/[^\w-]+/g, "_")}.tsi`
  return new NextResponse(tsi, {
    headers: {
      "Content-Type": "application/xml; charset=utf-8",
      "Content-Disposition": `attachment; filename="${nomFichier}"`,
    },
  })
}
