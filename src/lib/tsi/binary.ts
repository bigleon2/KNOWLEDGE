/**
 * binary.ts — Sérialisation/analyse TSI du format canonique écosystème (NIXML/NISYSTEM).
 *
 * LEON TSI EDITEUR v11 — miroir TS de tsi-toolkit/nixml.py (R4) : mêmes éléments,
 * mêmes attributs, mêmes conventions. Round-trip byte-exact exigé (le bouton
 * « Vérifier » de l'app s'appuie sur serializeTsi(parseTsi(x)) === x).
 *
 * Convention de remplacement (discussion itération 1-2) : remplacements par
 * `regex.test` préalable + `replace` — jamais de concaténation non vérifiée.
 */

import type { Mapping, MidiSpec, LedSpec, ModifierSpec, ProjectData } from "./types"

const échapperXml = (s: string): string =>
  s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;")

const attrs = (o: Record<string, string | number>): string =>
  Object.entries(o).map(([k, v]) => ` ${k}="${échapperXml(String(v))}"`).join("")

/** Projet → document TSI canonique (NISYSTEM — validé par l'arbitre tsi-validator bi-racine,
 * conforme au golden sample skills/tsi-validator/samples/echantillon-valide.tsi). */
export function serializeTsi(data: ProjectData): string {
  const lignes: string[] = []
  lignes.push('<?xml version="1.0" encoding="UTF-8"?>')
  lignes.push('<!--')
  lignes.push('  Export LEON TSI EDITEUR v11 — format canonique NISYSTEM (arbitre tsi-validator, R4 toolchain)')
  lignes.push('-->')
  lignes.push('<NISYSTEM VERSION="1">')
  lignes.push(`  <DEVICE${attrs({
    NAME: data.device.name, TYPE: data.device.type, IN_PORT: data.device.in_port,
    OUT_PORT: data.device.out_port, DECK_TARGET: data.device.deck_target,
  })}>`)
  lignes.push(`    <MAPPINGS COUNT="${data.mappings.length}">`)
  for (const m of data.mappings) {
    lignes.push(`      <MAPPING${attrs({ NAME: m.nom, TYPE: m.type, GROUP: m.groupe, CONTROL: m.controle })}>`)
    if (m.modifier) {
      lignes.push(`        <MODIFIER${attrs(m.modifier as Record<string, number>)}\/>`)
    }
    if (m.midi) {
      lignes.push(`        <MIDI${attrs({
        CHANNEL: m.midi.canal, MESSAGE: m.midi.message, NUMBER: m.midi.numero, MODE: m.midi.mode,
      })}\/>`)
    }
    if (m.led) {
      // canon arbitre E6 : LED dans un MAPPING TYPE=OUT avec MODE="Output" (golden sample)
      lignes.push(`        <LED${attrs({ NUMBER: m.led.numero, ON: m.led.on, OFF: m.led.off, MODE: "Output" })}\/>`)
    }
    lignes.push(`      </MAPPING>`)
  }
  lignes.push(`    </MAPPINGS>`)
  lignes.push(`  </DEVICE>`)
  lignes.push('</NISYSTEM>')
  return lignes.join("\n") + "\n"
}

const ATTR_RE = /([A-Z0-9_]+)="([^"]*)"/g  // A-Z0-9_ : les modifiers M1-M8 portent un chiffre (bug attrapé par verify Task 40)

function lireAttrs(bloc: string): Record<string, string> {
  const out: Record<string, string> = {}
  for (const m of bloc.matchAll(ATTR_RE)) out[m[1]] = m[2]
  return out
}

const décoderXml = (s: string): string =>
  s.replace(/&quot;/g, '"').replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&amp;/g, "&")

/**
 * Document TSI canonique → ProjectData. Lance une erreur explicite sur les formats
 * réels Traktor (blob DIOM) — inspection réservée au pont écosystème (R4).
 */
export function parseTsi(texte: string): ProjectData {
  if (/<TraktorSettings/.test(texte)) {
    throw new Error(
      "Format réel Traktor (TraktorSettings/blob DIOM) — l'inspection passe par le pont " +
      "écosystème tsi-toolkit (R4) ; l'app édite le format canonique.",
    )
  }
  if (!/<NISYSTEM|<NIXML/.test(texte)) throw new Error("Racine inconnue — fichier TSI non reconnu (rejet propre)")
  const devMatch = texte.match(/<DEVICE([^>]*)>/)  // conteneur canonique NISYSTEM (non auto-fermant)
  const a = devMatch ? lireAttrs(devMatch[1]) : {}
  const device = {
    name: décoderXml(a.NAME ?? "Traktor Kontrol S4 MK2"),
    type: a.TYPE ?? "MIDI",
    in_port: décoderXml(a.IN_PORT ?? "Traktor Kontrol S4 MK2 In"),
    out_port: décoderXml(a.OUT_PORT ?? "Traktor Kontrol S4 MK2 Out"),
    deck_target: a.DECK_TARGET ?? "Focus",
  }
  const mappings: Mapping[] = []
  const blocs = texte.match(/<MAPPING\s[^>]*>[\s\S]*?<\/MAPPING>/g) ?? []
  for (const bloc of blocs) {
    const head = bloc.match(/<MAPPING\s([^>]*)>/)![1]
    const h = lireAttrs(head)
    const modBloc = bloc.match(/<MODIFIER([^>]*)\/>/)
    const midiBloc = bloc.match(/<MIDI([^>]*)\/>/)
    const ledBloc = bloc.match(/<LED([^>]*)\/>/)
    const modifier: ModifierSpec | undefined = modBloc
      ? Object.fromEntries(Object.entries(lireAttrs(modBloc[1])).map(([k, v]) => [k, Number(v)]))
      : undefined
    const midi: MidiSpec | undefined = midiBloc
      ? (() => { const m = lireAttrs(midiBloc[1]); return {
          canal: Number(m.CHANNEL), message: m.MESSAGE as MidiSpec["message"],
          numero: Number(m.NUMBER), mode: m.MODE as MidiSpec["mode"] } })()
      : undefined
    const led: LedSpec | undefined = ledBloc
      ? (() => { const l = lireAttrs(ledBloc[1]); return {
          numero: Number(l.NUMBER), on: Number(l.ON), off: Number(l.OFF) } })()
      : undefined
    mappings.push({
      nom: décoderXml(h.NAME ?? ""), type: (h.TYPE as Mapping["type"]) ?? "IN",
      groupe: décoderXml(h.GROUP ?? ""), controle: décoderXml(h.CONTROL ?? ""),
      ...(modifier ? { modifier } : {}), ...(midi ? { midi } : {}), ...(led ? { led } : {}),
    })
  }
  return { device, mappings }
}

/** Vérification byte-exacte : serializeTsi(parseTsi(t)) === t. */
export function verifierRoundTrip(texte: string): { ok: boolean; detail: string } {
  try {
    const rediffusé = serializeTsi(parseTsi(texte))
    const ok = rediffusé === texte
    return { ok, detail: ok ? "byte-exact" : "re-sérialisation divergente" }
  } catch (e) {
    return { ok: false, detail: e instanceof Error ? e.message : String(e) }
  }
}
