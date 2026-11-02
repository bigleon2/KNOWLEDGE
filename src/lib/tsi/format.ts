/**
 * format.ts — Aides de formatage MIDI/TSI (conventions de la discussion itération 1-3).
 *
 * learn → « Ch01.CC.013 » · numéro sur 3 chiffres · groupement des sorties LED.
 */

import type { MidiSpec, S4Controls, ControlChip } from "./types"

const pad2 = (n: number): string => String(n).padStart(2, "0")
const pad3 = (n: number): string => String(n).padStart(3, "0")

/** MidiSpec → étiquette lisible « Ch00.CC.006 ». */
export function midiLabel(m: MidiSpec): string {
  return `Ch${pad2(m.canal)}.${m.message}.${pad3(m.numero)}`  // convention discussion : Ch00.CC.013
}

/** Analyse « Ch00.CC.006 » → MidiSpec (mode conservé). */
export function midiDeLabel(label: string, mode: MidiSpec["mode"] = "Direct"): MidiSpec {
  const m = /^Ch(\d+)\.(NOTE|CC)\.(\d+)$/.exec(label.trim())
  if (!m) throw new Error(`Étiquette MIDI non reconnue : ${label}`)
  return { canal: Number(m[1]), message: m[2] as MidiSpec["message"], numero: Number(m[3]), mode }
}

/** Regroupe les 220 sorties usine par préfixe de deck (A./B./C./D./Global). */
export function groupOutControls(controls: S4Controls): { groupe: string; noms: string[] }[] {
  const groupes: Record<string, string[]> = {}
  for (const [deck, noms] of Object.entries(controls.out)) {
    const cle = deck.includes(".") ? deck : "Global"
    groupes[cle] = (groupes[cle] ?? []).concat(noms)
  }
  return Object.entries(groupes)
    .map(([groupe, noms]) => ({ groupe, noms }))
    .sort((a, b) => a.groupe.localeCompare(b.groupe))
}

/** Zones physiques du S4 MK2 (table CC scellée) aplaties avec leur zone d'origine. */
export function zonesPhysiques(controls: S4Controls): { zone: string; chips: ControlChip[] }[] {
  return Object.entries(controls.tableCC).map(([zone, chips]) => ({ zone, chips }))
}
