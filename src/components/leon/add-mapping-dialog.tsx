"use client"

/**
 * add-mapping-dialog.tsx — Dialogue d'ajout/édition d'un mapping.
 *
 * `prefill` (3 champs : note / zone / commandId — discussion itération 3) :
 * un chip de module pré-remplit la commande, un chip physique pré-remplit la
 * note CC, Learn capture la note réelle du contrôleur.
 */

import { useMemo, useState } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from "@/components/ui/command"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { Radio, Search } from "lucide-react"
import { categoriesAvecTaille, rechercherCommandes } from "@/lib/tsi/catalog"
import { midi } from "@/lib/midi/midi-access"
import type { Mapping, MappingType } from "@/lib/tsi/types"
import { midiDeLabel, midiLabel } from "@/lib/tsi/format"

export interface Prefill {
  note?: string // « Ch00.CC.006 »
  zone?: string
  commandId?: number
}

interface Props {
  open: boolean
  prefill?: Prefill | null
  onClose: () => void
  onSubmit: (m: Mapping, noteProvisoire?: boolean) => void
  mappingsExistants: Mapping[]
}

export function AddMappingDialog({ open, prefill, onClose, onSubmit, mappingsExistants }: Props) {
  // Pré-remplissage au montage (la clé du parent remonte ce composant par prefill)
  const commandeInitiale = prefill?.commandId
    ? (() => { const c = rechercherCommandes("").find((x) => x.id === prefill.commandId)
               return c ? { id: c.id, nom: c.nom, categorie: c.categorie } : null })()
    : null
  const [commande, setCommande] = useState<{ id: number; nom: string; categorie: string } | null>(commandeInitiale)
  const [type, setType] = useState<MappingType>("IN")
  const [note, setNote] = useState(prefill?.note ?? "")
  const [zone, setZone] = useState(prefill?.zone ?? "Deck A")
  const [pickerOuvert, setPickerOuvert] = useState(false)
  const [recherche, setRecherche] = useState("")
  const [ecoute, setEcoute] = useState(false)

  // Le pré-remplissage est appliqué au MONTAGE via la clé de remontage du parent
  // (key={JSON.stringify(prefill)}) — aucun setState en effet (react-hooks/set-state-in-effect).

  const résultats = useMemo(() => rechercherCommandes(recherche).slice(0, 60), [recherche])
  const catégories = useMemo(() => categoriesAvecTaille(), [])

  const apprendre = () => {
    setEcoute(true)
    midi.attendreProchainMessage((msg) => {
      setNote(`Ch${String(msg.channel).padStart(2, "0")}.${msg.kind === "CC" ? "CC" : "NOTE"}.${String(msg.data1 ?? 0).padStart(3, "0")}`)
      setEcoute(false)
    })
  }

  const valider = () => {
    if (!commande) return
    // note absente → prochaine note libre (anti-collision, générateur conservateur),
    // signalée à l'utilisateur — jamais d'impasse silencieuse (correctif Task 40)
    const pris = new Set(mappingsExistants.flatMap((x) => [x.midi?.numero, x.led?.numero].filter((n): n is number => n !== undefined)))
    let numeroAuto = 36
    while (pris.has(numeroAuto)) numeroAuto++
    let midiSpec: Mapping["midi"] | undefined
    let ledSpec: Mapping["led"] | undefined
    if (note) {
      const spec = midiDeLabel(note)
      midiSpec = spec
      ledSpec = { numero: spec.numero, on: 127, off: 0 }
    } else if (type === "IN") {
      midiSpec = { canal: 0, message: "NOTE", numero: numeroAuto, mode: "Direct" }
    } else {
      ledSpec = { numero: numeroAuto, on: 127, off: 0 }
    }
    const m: Mapping = type === "IN"
      ? { nom: `${commande.nom} — ${zone}`, type: "IN", groupe: zone, controle: commande.nom,
          ...(midiSpec ? { midi: midiSpec } : {}) }
      : { nom: `${commande.nom} — ${zone}`, type: "OUT", groupe: zone, controle: commande.nom,
          ...(ledSpec ? { led: ledSpec } : {}) }
    onSubmit(m, !note)
    setCommande(null); setNote(""); setEcoute(false)
    onClose()
  }

  return (
    <Dialog open={open} onOpenChange={(o) => { if (!o) onClose() }}>
      <DialogContent className="max-w-lg">
        <DialogHeader>
          <DialogTitle>Nouveau mapping {prefill?.zone ? `· ${prefill.zone}` : ""}</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <div className="space-y-1.5">
            <Label>Commande Traktor (catalogue scellé — {rechercherCommandes("").length})</Label>
            <Popover open={pickerOuvert} onOpenChange={setPickerOuvert}>
              <PopoverTrigger asChild>
                <Button variant="outline" role="combobox" className="w-full justify-between font-normal">
                  {commande ? commande.nom : "Choisir une commande…"}
                  <Search className="ml-2 size-4 shrink-0 opacity-50" />
                </Button>
              </PopoverTrigger>
              <PopoverContent className="w-[22rem] p-0" align="start">
                <Command>
                  <CommandInput value={recherche} onValueChange={setRecherche} placeholder="Rechercher (nom, catégorie)…" />
                  <CommandList className="max-h-72">
                    <CommandEmpty>Aucune commande trouvée.</CommandEmpty>
                    {catégories.map((cat) => {
                      const items = résultats.filter((r) => r.categorie === cat.nom)
                      if (!items.length) return null
                      return (
                        <CommandGroup key={cat.nom} heading={`${cat.nom} (${cat.n})`}>
                          {items.map((r) => (
                            <CommandItem key={r.id} value={`${r.nom} ${r.categorie}`}
                              onSelect={() => { setCommande({ id: r.id, nom: r.nom, categorie: r.categorie }); setPickerOuvert(false) }}>
                              <span className="flex-1">{r.nom}</span>
                              {r.provenance === "discussion-cmdr" && <Badge variant="outline" className="ml-2 text-[10px]">CMDR {r.cmdrId}</Badge>}
                            </CommandItem>
                          ))}
                        </CommandGroup>
                      )
                    })}
                  </CommandList>
                </Command>
              </PopoverContent>
            </Popover>
            {commande && <p className="text-xs text-muted-foreground">Catégorie : {commande.categorie}</p>}
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div className="space-y-1.5">
              <Label>Sens</Label>
              <div className="flex gap-2">
                {(["IN", "OUT"] as MappingType[]).map((t) => (
                  <Button key={t} size="sm" variant={type === t ? "default" : "outline"} onClick={() => setType(t)}>{t}</Button>
                ))}
              </div>
            </div>
            <div className="space-y-1.5">
              <Label>Zone / groupe</Label>
              <Input value={zone} onChange={(e) => setZone(e.target.value)} />
            </div>
          </div>
          <div className="space-y-1.5">
            <Label>Note / CC {type === "IN" ? "(appuyez sur le contrôleur ou saisissez Ch00.CC.013)" : "(sortie LED)"}</Label>
            <div className="flex gap-2">
              <Input placeholder="Ch00.CC.013" value={note} onChange={(e) => setNote(e.target.value)} />
              <Button variant={ecoute ? "secondary" : "outline"} size="sm" onClick={apprendre} disabled={midi.etat !== "ouvert"}>
                <Radio className="mr-1 size-4" />{ecoute ? "Écoute…" : "Learn"}
              </Button>
            </div>
            {ecoute && <p className="text-xs text-muted-foreground">Jouez un contrôle sur le S4 MK2 — SHIFT + PREVIEW pour le mode MIDI (manuel NI §6.10.2).</p>}
          </div>
          <div className="flex justify-end gap-2 pt-1">
            <Button variant="ghost" onClick={onClose}>Annuler</Button>
            <Button onClick={valider} disabled={!commande}>Ajouter</Button>
          </div>
          <p className="text-xs text-muted-foreground">
            {mappingsExistants.length} mapping(s) dans ce projet — les collisions canal/message/numéro sont signalées par l&apos;audit du studio.
          </p>
        </div>
      </DialogContent>
    </Dialog>
  )
}

export { midiLabel }
