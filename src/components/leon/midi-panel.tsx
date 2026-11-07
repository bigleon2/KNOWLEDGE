"use client"

/**
 * midi-panel.tsx — Panneau « Contrôleur MIDI » : autorisation, ports, badge S4 MK2,
 * moniteur temps réel, état Learn (couche midi-access — correctif handlePortMessage
 * préservé : le moniteur affiche réellement les messages entrants).
 */

import { useEffect, useRef, useState } from "react"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Radio } from "lucide-react"
import { midi } from "@/lib/midi/midi-access"
import type { DecodedMidiMessage } from "@/lib/tsi/types"

export function MidiPanel() {
  const [etat, setEtat] = useState(midi.etat)
  const [ports, setPorts] = useState(midi.ports)
  const [s4, setS4] = useState(midi.s4mk2Detecte)
  const [journal, setJournal] = useState<DecodedMidiMessage[]>([])
  const dernierRef = useRef<HTMLSpanElement>(null)

  useEffect(() => {
    const off = midi.onMessage((msg) => {
      setJournal((j) => [msg, ...j].slice(0, 12))
    })
    const tick = setInterval(() => {
      setEtat(midi.etat); setPorts(midi.ports); setS4(midi.s4mk2Detecte)
    }, 800)
    return () => { off(); clearInterval(tick) }
  }, [])

  const autoriser = async () => {
    const e = await midi.autoriser()
    setEtat(e); setPorts(midi.ports); setS4(midi.s4mk2Detecte)
  }

  return (
    <Card>
      <CardHeader className="pb-2">
        <CardTitle className="flex items-center gap-2 text-base">
          <Radio className="size-4" /> Contrôleur MIDI
          {s4 && <Badge className="bg-emerald-600">S4 MK2 détecté</Badge>}
          {etat === "indisponible" && <Badge variant="destructive">Web MIDI indisponible (G5)</Badge>}
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {etat === "ouvert" ? (
          <>
            <p className="text-xs text-muted-foreground">
              Entrées : {ports.entrees.map((p) => p.nom || p.id).join(", ") || "—"} · Sorties : {ports.sorties.map((p) => p.nom || p.id).join(", ") || "—"}
            </p>
            <div className="flex items-center gap-2">
              <Radio className="size-3.5 text-muted-foreground" />
              <span className="text-xs text-muted-foreground">Moniteur —</span>
              <span ref={dernierRef} className="font-mono text-xs">{journal[0]?.label ?? "—"}</span>
            </div>
            <div className="max-h-28 overflow-y-auto text-xs text-muted-foreground">
              {journal.slice(1).map((j, i) => (
                <div key={i} className="font-mono">{j.label}</div>
              ))}
            </div>
            <p className="text-[11px] text-muted-foreground">
              Mode MIDI : SHIFT + PREVIEW sur le contrôleur (écrans Loop « ON » — manuel NI §6.10.2).
            </p>
          </>
        ) : (
          <div className="space-y-2">
            <p className="text-xs text-muted-foreground">
              {etat === "indisponible"
                ? "Ce navigateur n'expose pas Web MIDI — l'éditeur reste utilisable (saisie manuelle des notes)."
                : "Autorisez l'accès MIDI pour la capture Learn et le moniteur (Chrome/Edge/Opera, contexte sécurisé)."}
            </p>
            {etat !== "indisponible" && (
              <Button size="sm" onClick={autoriser} disabled={etat === "demande"}>
                {etat === "demande" ? "Autorisation…" : "Autoriser l'accès MIDI"}
              </Button>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  )
}
