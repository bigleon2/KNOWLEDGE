"use client"

/**
 * midi-access.ts — Couche Web MIDI temps réel (singleton).
 *
 * LEON TSI EDITEUR v11 — correctif critique itération 3 (discussion b6170b8b)
 * PRÉSERVÉ PAR CONSTRUCTION : le gestionnaire interne du port s'appelle
 * `handlePortMessage` et l'API publique d'abonnement s'appelle `onMessage` —
 * DEUX méthodes distinctes (à l'origine, la méthode publique `onMessage`
 * dupliquée ÉCRASAIT le gestionnaire de port : aucun message entrant n'était
 * décodé avec un S4 MK2 réel — Learn bloqué « Écoute… », moniteur muet ;
 * indétectable à ESLint/SWC, visible à tsc).
 *
 * Dégradation G5 : sans Web MIDI (Firefox/Safari ou contexte non sécurisé),
 * le service rend un état « indisponible » honnête — jamais de crash.
 */

import { decodeMidi } from "@/lib/tsi/midi"
import type { DecodedMidiMessage } from "@/lib/tsi/types"

export type EtatMidi = "indisponible" | "fermé" | "demande" | "ouvert"

export interface MidiPortInfo {
  id: string
  nom: string
  fabricant: string
  etat: string
}

type Listener = (msg: DecodedMidiMessage) => void

class MidiService {
  private static _instance: MidiService | null = null
  static instance(): MidiService {
    MidiService._instance ??= new MidiService()
    return MidiService._instance
  }

  private acces: MIDIAccess | null = null
  private listeners: Set<Listener> = new Set()
  private handlersPorts: Set<(e: MIDIMessageEvent) => void> = new Set()
  etat: EtatMidi = "fermé"
  ports: { entrees: MidiPortInfo[]; sorties: MidiPortInfo[] } = { entrees: [], sorties: [] }
  s4mk2Detecte = false
  dernierMessage: DecodedMidiMessage | null = null
  learnActif = false
  private onLearnCapture: ((msg: DecodedMidiMessage) => void) | null = null

  /** Autorise l'accès MIDI (garde : API absente → état honnête, pas de crash). */
  async autoriser(): Promise<EtatMidi> {
    if (typeof navigator === "undefined" || !("requestMIDIAccess" in navigator)) {
      this.etat = "indisponible"
      return this.etat
    }
    this.etat = "demande"
    try {
      this.acces = await navigator.requestMIDIAccess()
    } catch {
      this.etat = "fermé"
      return this.etat
    }
    this.brancher()
    return this.etat
  }

  /**
   * Gestionnaire interne du port — RENOMMÉ `handlePortMessage` (correctif
   * critique) : jamais exposé publiquement, jamais écrasé par l'API d'abonnement.
   */
  private handlePortMessage = (e: MIDIMessageEvent): void => {
    if (!e.data) return // narrowing : e.data est Uint8Array | null (garde TS2339/TS2769)
    const msg = decodeMidi(new Uint8Array(e.data))
    this.dernierMessage = msg
    for (const l of this.listeners) l(msg)
    if (this.learnActif && msg.kind !== "Other") {
      const cb = this.onLearnCapture
      this.learnActif = false
      this.onLearnCapture = null
      cb?.(msg)
    }
  }

  private brancher(): void {
    if (!this.acces) return
    const majPorts = () => {
      const entrees: MidiPortInfo[] = []
      const sorties: MidiPortInfo[] = []
      this.acces!.inputs.forEach((p) => entrees.push({ id: p.id, nom: p.name ?? "", fabricant: p.manufacturer ?? "", etat: p.state }))
      this.acces!.outputs.forEach((p) => sorties.push({ id: p.id, nom: p.name ?? "", fabricant: p.manufacturer ?? "", etat: p.state }))
      this.ports = { entrees, sorties }
      this.s4mk2Detecte =
        [...entrees, ...sorties].some((p) => /s4 mk2|kontrol s4/i.test(p.nom)) ||
        entrees.some((p) => /kontrol s4/i.test(p.nom))
    }
    majPorts()
    // brancher le routage entrant sur CHAQUE port d'entrée (attachInputs)
    const attacher = () => {
      this.acces!.inputs.forEach((p) => {
        // un seul handler par port (déduplication)
        p.onmidimessage = (e: MIDIMessageEvent) => this.handlePortMessage(e)
      })
    }
    attacher()
    this.acces.onstatechange = () => { majPorts(); attacher() }
    this.etat = "ouvert"
  }

  /** API publique d'abonnement (distincte du gestionnaire interne — TS2393 jamais réintroduit). */
  onMessage(listener: Listener): () => void {
    this.listeners.add(listener)
    return () => this.listeners.delete(listener)
  }

  /** Mode Learn : capture le prochain message significant et le rend au callback. */
  attendreProchainMessage(cb: (msg: DecodedMidiMessage) => void): void {
    this.onLearnCapture = cb
    this.learnActif = true
  }

  annulerLearn(): void {
    this.learnActif = false
    this.onLearnCapture = null
  }

  /** Test LED : envoie Note On 127 vers la sortie choisie (numéro ≤ 127). */
  testerLed(numero: number, indexSortie = 0): boolean {
    if (!this.acces) return false
    const sorties: MIDIOutput[] = []
    this.acces.outputs.forEach((p) => sorties.push(p))
    const cible = sorties[indexSortie]
    if (!cible) return false
    cible.send(new Uint8Array([0x90, numero & 0x7f, 127]))
    cible.send(new Uint8Array([0x80, numero & 0x7f, 0]), window.performance.now() + 150)
    return true
  }

  portEntreeNom(): string {
    return this.ports.entrees[0]?.nom ?? "—"
  }
}

export const midi = MidiService.instance()
