/**
 * types.ts — Types du mapping TSI (format canonique écosystème — tsi-toolkit/nixml.py).
 *
 * LEON TSI EDITEUR v11 — Task 40 (Extension React du studio v11).
 * Source de vérité du format : tsi-toolkit (R4 — jamais dupliquer la sémantique,
 * miroir typé du format NIXML canonique validé par l'arbitre tsi-validator bi-racine).
 */

export type MessageType = "NOTE" | "CC"
export type MappingMode = "Direct" | "Toggle" | "Increment"
export type MappingType = "IN" | "OUT"

export interface MidiSpec {
  canal: number
  message: MessageType
  numero: number
  mode: MappingMode
}

export interface LedSpec {
  numero: number
  on: number
  off: number
  /** canon arbitre E6 : toujours "Output" pour un LED de mapping OUT */
  mode?: "Output"
}

export interface ModifierSpec {
  /** M1..M8 → 0/1 */
  [mod: string]: number
}

export interface Mapping {
  nom: string
  type: MappingType
  groupe: string
  /** Nom exact de la commande Traktor (catalogue scellé) */
  controle: string
  modifier?: ModifierSpec
  midi?: MidiSpec
  led?: LedSpec
}

export interface DeviceSpec {
  name: string
  type: string
  in_port: string
  out_port: string
  deck_target: string
}

export interface ProjectData {
  device: DeviceSpec
  mappings: Mapping[]
}

export interface CatalogueCommande {
  id: number
  nom: string
  categorie: string
  provenance: "toolkit-djtt-reel" | "discussion-cmdr"
  cmdrId?: number
}

export interface Catalogue {
  meta: { titre: string; sources: string[]; convention: string }
  comptes: { commandes: number; categories: number }
  categories: Record<string, number[]>
  commandes: Record<string, { nom: string; categorie: string; provenance: string; cmdrId?: number }>
}

export interface ControlChip {
  nom: string
  cc: number
  type: "fader" | "bouton"
}

export interface S4Controls {
  meta: { titre: string; sources: string[] }
  comptes: { in: number; out: number }
  in: Record<string, string[]>
  out: Record<string, string[]>
  tableCC: Record<string, ControlChip[]>
  controlesUsine: Record<string, { cids: number[]; notes: string }>
  modeMidi: { combinaison: string; source: string }
}

/** Message MIDI décodé (couche Web MIDI → UI). */
export interface DecodedMidiMessage {
  kind: "NoteOn" | "NoteOff" | "CC" | "Other"
  channel: number
  data1?: number
  data2?: number
  label: string
}

export interface AuditEntry {
  id: string
  action: string
  detail: string
  mappings: number
  conflits: number
  createdAt: string
}
