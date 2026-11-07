import { NextRequest, NextResponse } from "next/server"
import { db } from "@/lib/db"
import { rendreAudit } from "@/lib/studio/studio"

type Params = { params: Promise<{ id: string }> }

/**
 * Journal d'audit auto-évolutif du studio v11 — GET : lecture (50 dernières
 * entrées) ; POST : consigne une action (action, detail, mappings, conflits
 * recalculés mécaniquement côté serveur — le client ne déclare pas les
 * conflits, le serveur les vérifie).
 */
export async function GET(_req: NextRequest, { params }: Params) {
  const { id } = await params
  const audits = await db.auditLog.findMany({ where: { projectId: id }, orderBy: { createdAt: "desc" }, take: 50 })
  return NextResponse.json({ audits })
}

export async function POST(req: NextRequest, { params }: Params) {
  const { id } = await params
  const body = await req.json().catch(() => null)
  if (!body || typeof body.action !== "string") {
    return NextResponse.json({ error: "action requis" }, { status: 400 })
  }
  const projet = await db.project.findUnique({ where: { id } })
  if (!projet) return NextResponse.json({ error: "projet introuvable" }, { status: 404 })
  const data = JSON.parse(projet.data)
  const audit = rendreAudit(String(body.action), String(body.detail ?? ""), data.mappings ?? [])
  const entrée = await db.auditLog.create({ data: { projectId: id, ...audit } })
  return NextResponse.json({ entrée }, { status: 201 })
}
