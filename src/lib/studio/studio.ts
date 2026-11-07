/**
 * studio.ts — Studio v11 : compilateur DSL + application de presets + audit auto-évolutif.
 *
 * Extension React du studio v11 (architecture-mapping-studio-v11.md) : le DSL et
 * les presets restent la source de vérité partagée avec la toolchain Python
 * (tsi-toolkit/studio.py — miroir TS des mêmes sémantiques, R4).
 *
 *   DSL      : lignes « contrôle -> fonction [couche] », couches BASE/M1-M4
 *   Presets  : bloc/deck/paramètre (freeze-mode.json = preset de référence)
 *   Audit    : journal_autoévolutif — chaque action laisse une entrée horodatée
 *              (via l'API /api/projects/[id]/audit), jamais effacé, alimente
 *              l'itération suivante.
 */

import type { Mapping, ProjectData } from "@/lib/tsi/types"
import { detecterConflits } from "@/lib/tsi/edit"

export interface LigneDsl {
  controle: string
  fonction: string
  couche: string // BASE | M1..M4
}

/** Analyse le DSL (une ligne par mapping ; commentaires « # » ignorés). */
export function compilerDsl(dsl: string): { lignes: LigneDsl[]; erreurs: string[] } {
  const lignes: LigneDsl[] = []
  const erreurs: string[] = []
  for (const [i, l] of dsl.split("\n").entries()) {
    const ligne = l.trim()
    if (!ligne || ligne.startsWith("#")) continue
    const m = /^(\S+)\s*->\s*(.+?)(?:\s*\[(BASE|M[1-4])\])?$/.exec(ligne)
    if (!m) {
      erreurs.push(`ligne ${i + 1} : « ${ligne} » — attendu « contrôle -> fonction [couche] »`)
      continue
    }
    lignes.push({ controle: m[1], fonction: m[2].trim(), couche: m[3] ?? "BASE" })
  }
  return { lignes, erreurs }
}

/** Génère les mappings depuis les lignes DSL (numéros MIDI séquentiels anti-collision). */
export function mappingsDepuisDsl(lignes: LigneDsl[], base: ProjectData): Mapping[] {
  const pris = new Set(base.mappings.flatMap((m) => [m.midi?.numero, m.led?.numero].filter(Boolean) as number[]))
  let numero = 36
  const prochain = () => { while (pris.has(numero)) numero++; pris.add(numero); return numero }
  return lignes.map((l) => ({
    nom: `${l.fonction} — ${l.controle}${l.couche !== "BASE" ? ` [${l.couche}]` : ""}`,
    type: "IN" as const,
    groupe: "Deck A",
    controle: l.fonction,
    ...(l.couche !== "BASE" ? { modifier: { [l.couche]: 1 } } : {}),
    midi: { canal: 0, message: "NOTE" as const, numero: prochain(), mode: "Direct" as const },
  }))
}

export interface Preset {
  meta: { nom: string; description: string; version: string; appareil: string; traktor: string }
  device: ProjectData["device"]
  mappings: Mapping[]
}

/** Applique un preset : bloc/deck/paramètre (mapping complet ou sélection par groupe). */
export function appliquerPreset(base: ProjectData, preset: Preset, groupeCible?: string): Mapping[] {
  return preset.mappings.map((m) => ({
    ...m,
    groupe: groupeCible ?? m.groupe,
    nom: `${m.nom}${groupeCible && m.groupe !== groupeCible ? ` (${groupeCible})` : ""}`,
  }))
}

/** Compte-rendu d'audit d'une action (action, détail, mappings, conflits détectés). */
export function rendreAudit(
  action: string, detail: string, mappings: Mapping[],
): { action: string; detail: string; mappings: number; conflits: number } {
  return { action, detail, mappings: mappings.length, conflits: detecterConflits(mappings).length }
}
