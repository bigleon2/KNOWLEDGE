import { NextRequest, NextResponse } from "next/server"
import { db } from "@/lib/db"
import { serializeTsi, verifierRoundTrip } from "@/lib/tsi/binary"

type Params = { params: Promise<{ id: string }> }

/**
 * Vérification byte-exacte (G1 de la discussion) : re-sérialise le mapping
 * stocké et le compare à ce qu'un export produirait — le verdict honnête
 * « byte-exact si aucune modification » attendu par le CDC Task 39 (EF-04).
 */
export async function POST(_req: NextRequest, { params }: Params) {
  const { id } = await params
  const projet = await db.project.findUnique({ where: { id } })
  if (!projet) return NextResponse.json({ error: "projet introuvable" }, { status: 404 })
  const data = JSON.parse(projet.data)
  const tsi = serializeTsi(data)
  const rt = verifierRoundTrip(tsi)
  return NextResponse.json({
    verdict: rt.ok ? "BYTE-EXACT" : "DIVERGENT",
    detail: rt.detail,
    taille: tsi.length,
    mappings: data.mappings?.length ?? 0,
  })
}
