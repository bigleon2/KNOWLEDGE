/**
 * edit.ts — Édition de masse des mappings (parité CMDR — discussion itérations 1-3).
 *
 * Opérations : dupliquer, copier/coller, interaction (Direct↔Toggle↔Increment),
 * cible (IN↔OUT), canal ±1. Toutes pures : (mappings) → mappings.
 */

import type { Mapping } from "./types"

const MAX_CANAL = 15

/** Duplique un mapping en incrémentant son numéro MIDI/LED (anti-collision). */
export function dupliquer(m: Mapping, tous: Mapping[]): Mapping {
  const numéros = new Set(tous.flatMap((x) => [x.midi?.numero, x.led?.numero].filter(Boolean)))
  let numero = (m.midi?.numero ?? m.led?.numero ?? 0) + 1
  while (numéros.has(numero)) numero++
  const suffixe = numero > 127 ? " bis" : ""
  return {
    ...m,
    nom: `${m.nom} (copie)`,
    midi: m.midi ? { ...m.midi, numero: numero > 127 ? m.midi.numero : numero } : undefined,
    led: m.led ? { ...m.led, numero: numero > 127 ? m.led.numero : numero } : undefined,
    ...(suffixe ? {} : {}),
  }
}

/** Cycle du mode d'interaction (Direct → Toggle → Increment → Direct). */
export function cyclerInteraction(m: Mapping): Mapping {
  if (!m.midi) return m
  const modes = ["Direct", "Toggle", "Increment"] as const
  const i = modes.indexOf(m.midi.mode)
  return { ...m, midi: { ...m.midi, mode: modes[(i + 1) % modes.length] } }
}

/** Bascule la cible IN ↔ OUT (le spec midi/led suit le sens). */
export function basculerCible(m: Mapping): Mapping {
  const type = m.type === "IN" ? "OUT" : "IN"
  if (type === "OUT" && m.midi) {
    return { ...m, type, led: { numero: m.midi.numero, on: 127, off: 0 }, midi: undefined }
  }
  if (type === "IN" && m.led) {
    return { ...m, type, midi: { canal: 0, message: "NOTE", numero: m.led.numero, mode: "Direct" }, led: undefined }
  }
  return { ...m, type }
}

/** Canal ±1 sur le spec MIDI (borde 0-15). */
export function decalerCanal(m: Mapping, delta: number): Mapping {
  if (!m.midi) return m
  const canal = Math.min(MAX_CANAL, Math.max(0, m.midi.canal + delta))
  return { ...m, midi: { ...m.midi, canal } }
}

/** Copie profonde d'une sélection (presse-papiers). */
export function copier(ms: Mapping[]): Mapping[] {
  return ms.map((m) => JSON.parse(JSON.stringify(m)) as Mapping)
}

/** Colle une sélection : noms désuffixés « — copie » pour éviter les collisions. */
export function coller(pressePapiers: Mapping[], cible: Mapping[]): Mapping[] {
  const noms = new Set(cible.map((m) => m.nom))
  return pressePapiers.map((m) => {
    let nom = m.nom
    while (noms.has(nom)) nom = `${nom} — copie`
    noms.add(nom)
    return { ...m, nom }
  })
}

/** Détecte les conflits d'allocation (même canal+message+numero+conditions de couche). */
export function detecterConflits(ms: Mapping[]): { a: string; b: string; cle: string }[] {
  const vus = new Map<string, string>()
  const conflits: { a: string; b: string; cle: string }[] = []
  for (const m of ms) {
    const spec = m.midi ?? (m.led ? ({ canal: 0, message: "NOTE", numero: m.led.numero, mode: "-" } as const) : null)
    if (!spec) continue
    const couche = Object.entries(m.modifier ?? {}).sort(([a], [b]) => a.localeCompare(b)).map(([k, v]) => `${k}=${v}`).join(",")
    const cle = `${m.type}|${(spec as { canal: number }).canal}|${(spec as { message: string }).message}|${(spec as { numero: number }).numero}|${couche}`
    const précédent = vus.get(cle)
    if (précédent) conflits.push({ a: précédent, b: m.nom, cle })
    else vus.set(cle, m.nom)
  }
  return conflits
}
