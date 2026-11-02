import { NextResponse } from "next/server"
import fs from "node:fs/promises"
import path from "node:path"

/**
 * GET /api/presets — expose les presets du studio v11 par API
 * (architecture-mapping-studio-v11.md §Extension React : « exposant les mêmes
 * presets par API »). Source de vérité partagée : src/data/presets/*.json —
 * jumeaux du répertoire examples/ de la toolchain (R4, jamais régénérés à la main).
 */
export async function GET() {
  const dir = path.join(process.cwd(), "src", "data", "presets")
  const fichiers = await fs.readdir(dir).catch(() => [])
  const presets = await Promise.all(
    fichiers.filter((f) => f.endsWith(".json")).sort().map(async (f) => {
      const contenu = JSON.parse(await fs.readFile(path.join(dir, f), "utf-8"))
      return {
        fichier: f,
        nom: contenu.meta?.nom ?? f,
        description: contenu.meta?.description ?? "",
        version: contenu.meta?.version ?? "1.0.0",
        nbMappings: contenu.mappings?.length ?? 0,
      }
    }),
  )
  return NextResponse.json({ presets })
}
