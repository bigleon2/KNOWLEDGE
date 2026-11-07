/**
 * midi.ts — Décodage des messages MIDI bruts (Web MIDI → UI).
 *
 * Correctif critique itération 3 (discussion b6170b8b) préservé : le décodage
 * narrow `msg.channel` AVANT toute utilisation — la variante `Other` n'a pas de
 * canal (garde `kind === "Other"` → pas d'accès membre inexistant).
 */

import type { DecodedMidiMessage } from "./types"

export function decodeMidi(data: Uint8Array): DecodedMidiMessage {
  const status = data[0] ?? 0
  const kind: DecodedMidiMessage["kind"] =
    status >= 0x90 && status <= 0x9f ? "NoteOn"
    : status >= 0x80 && status <= 0x8f ? "NoteOff"
    : status >= 0xb0 && status <= 0xbf ? "CC"
    : "Other"
  if (kind === "Other") {
    return { kind, channel: 0, label: `SysEx/autre (0x${status.toString(16).padStart(2, "0")})` }
  }
  const channel = status & 0x0f
  const data1 = data[1]
  const data2 = data[2]
  const type = kind === "CC" ? "CC" : "Note"
  const label = `Ch${String(channel).padStart(2, "0")}.${type}.${String(data1 ?? 0).padStart(3, "0")}` +
    (kind === "NoteOn" && data2 === 0 ? " (off)" : "")
  return { kind, channel, data1, data2, label }
}

/** Test LED : construit un message Note On à la vélocité 127 (sortie → contrôleur). */
export function ledTestMessage(numero: number, canal = 0): Uint8Array {
  return new Uint8Array([0x90 | canal, numero & 0x7f, 127])
}
