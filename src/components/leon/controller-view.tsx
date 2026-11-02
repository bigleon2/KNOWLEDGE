"use client"

/**
 * controller-view.tsx — Vue contrôleur S4 MK2 : 3 vues thématiques
 * (discussion itération 3) : (a) Contrôles (In) — zones physiques avec chips CC
 * documentés (plein) et chips Learn (tiretés) ; (b) Modes & Modules — 8 modules
 * sourcés, chips commandes cliquables → mapping pré-rempli, chips physiques →
 * CC pré-rempli, doc sourcée par module, recherche, Learn par module ;
 * (c) Retours LED — 220 sorties usine groupées.
 */

import { useMemo, useState } from "react"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Bluetooth, Eye, Keyboard, Layers, Search } from "lucide-react"
import { MODULES, chipsModule, commandesModule, s4Controls, toutesCommandes } from "@/lib/tsi/catalog"
import { groupOutControls } from "@/lib/tsi/format"
import type { Prefill } from "./add-mapping-dialog"

type Vue = "in" | "modules" | "led"

interface Props {
  onQuickCommand: (prefill: Prefill) => void
}

export function ControllerView({ onQuickCommand }: Props) {
  const [vue, setVue] = useState<Vue>("in")
  const [recherche, setRecherche] = useState("")
  const [learnModule, setLearnModule] = useState<string | null>(null)

  const zones = useMemo(
    () => Object.entries(s4Controls.tableCC).map(([zone, chips]) => ({ zone, chips })),
    [],
  )
  const sorties = useMemo(() => groupOutControls(s4Controls), [])
  const filtre = (s: string) => !recherche || s.toLowerCase().includes(recherche.toLowerCase())

  return (
    <Card>
      <CardHeader className="pb-2">
        <CardTitle className="flex flex-wrap items-center gap-2 text-base">
          <Keyboard className="size-4" /> Vue Contrôleur S4 MK2
          <div className="ml-auto flex gap-1">
            <Button size="sm" variant={vue === "in" ? "default" : "ghost"} onClick={() => setVue("in")}>
              Contrôles (In · {s4Controls.comptes.in})
            </Button>
            <Button size="sm" variant={vue === "modules" ? "default" : "ghost"} onClick={() => setVue("modules")}>
              Modes &amp; Modules ({MODULES.length})
            </Button>
            <Button size="sm" variant={vue === "led" ? "default" : "ghost"} onClick={() => setVue("led")}>
              <Eye className="mr-1 size-3.5" /> Retours LED ({s4Controls.comptes.out})
            </Button>
          </div>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        <div className="flex items-center gap-2">
          <Search className="size-3.5 text-muted-foreground" />
          <Input
            className="h-7 max-w-64 text-xs"
            placeholder={vue === "modules" ? "ableton, sequencer, loop rec…" : "hotcue, flux, gain…"}
            value={recherche} onChange={(e) => setRecherche(e.target.value)}
          />
        </div>

        {vue === "in" && (
          <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
            {zones.map(({ zone, chips }) => {
              const visibles = chips.filter((c) => filtre(c.nom))
              if (!visibles.length) return null
              return (
                <div key={zone} className="rounded-md border p-3">
                  <p className="mb-2 text-xs font-medium text-muted-foreground">{zone}</p>
                  <div className="flex flex-wrap gap-1.5">
                    {visibles.map((c) => (
                      <button key={c.nom}
                        className={`rounded-full px-2 py-0.5 text-xs transition-colors hover:bg-primary hover:text-primary-foreground ${
                          c.type === "fader"
                            ? "border border-dashed border-muted-foreground/40 text-foreground"
                            : "bg-primary/10 text-primary"
                        }`}
                        title={`${zone} — CC ${String(c.cc).padStart(3, "0")} (${c.type})`}
                        onClick={() => onQuickCommand({ note: `Ch00.CC.${String(c.cc).padStart(3, "0")}`, zone })}>
                        {c.nom}
                      </button>
                    ))}
                  </div>
                </div>
              )
            })}
          </div>
        )}

        {vue === "modules" && (
          <div className="grid gap-3 md:grid-cols-2">
            {MODULES.map((mod) => {
              const cmds = commandesModule(mod).filter((c) => filtre(c.nom) || filtre(mod.titre)).slice(0, 26)
              const chips = chipsModule(mod).slice(0, 8)
              if (!filtre(mod.titre) && !cmds.length) return null
              return (
                <div key={mod.cle} className="rounded-md border p-3">
                  <div className="mb-1 flex items-center gap-2">
                    <Layers className="size-3.5 text-primary" />
                    <p className="text-sm font-medium">{mod.titre}</p>
                    <Badge variant="outline" className="ml-auto text-[10px]">{cmds.length} cmd</Badge>
                    <Button
                      size="sm" variant={learnModule === mod.cle ? "secondary" : "ghost"}
                      className="h-6 px-2 text-[11px]"
                      title="Learn par module — capture une note puis l'associe à ce module"
                      onClick={() => setLearnModule(learnModule === mod.cle ? null : mod.cle)}>
                      <Bluetooth className="mr-1 size-3" />{learnModule === mod.cle ? "Écoute…" : "Learn"}
                    </Button>
                  </div>
                  <p className="mb-2 text-[11px] leading-snug text-muted-foreground">{mod.doc}</p>
                  <div className="flex flex-wrap gap-1">
                    {cmds.map((c) => (
                      <button key={c.id}
                        className="rounded-full bg-primary/10 px-2 py-0.5 text-xs text-primary hover:bg-primary hover:text-primary-foreground"
                        title={c.cmdrId ? `${c.nom} — id catalogue ${c.cmdrId}` : c.nom}
                        onClick={() => onQuickCommand({ commandId: c.id, zone: mod.titre })}>
                        {c.nom.length > 30 ? `${c.nom.slice(0, 28)}…` : c.nom}
                      </button>
                    ))}
                    {chips.map((c) => (
                      <button key={c.nom}
                        className="rounded-full border border-dashed border-muted-foreground/40 px-2 py-0.5 text-xs hover:bg-primary hover:text-primary-foreground"
                        title={`Chip physique — CC ${String(c.cc).padStart(3, "0")}`}
                        onClick={() => onQuickCommand({ note: `Ch00.CC.${String(c.cc).padStart(3, "0")}`, zone: mod.titre })}>
                        {c.nom}
                      </button>
                    ))}
                  </div>
                </div>
              )
            })}
            {!recherche && (
              <p className="text-[11px] text-muted-foreground md:col-span-2">
                Appartenance des modules dérivée mécaniquement du catalogue scellé ({toutesCommandes().length} commandes) —
                chips pleins = commande pré-remplie, tiretés = CC physique pré-rempli.
              </p>
            )}
          </div>
        )}

        {vue === "led" && (
          <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
            {sorties.map(({ groupe, noms }) => {
              const visibles = noms.filter(filtre)
              if (!visibles.length) return null
              return (
                <div key={groupe} className="rounded-md border p-3">
                  <p className="mb-2 text-xs font-medium text-muted-foreground">
                    {groupe} <Badge variant="outline" className="text-[10px]">{visibles.length}</Badge>
                  </p>
                  <div className="max-h-40 overflow-y-auto text-xs">
                    {visibles.map((n) => (
                      <button key={n} className="block w-full truncate rounded px-1 py-0.5 text-left hover:bg-primary/10"
                        title={`${n} — sortie usine OUT`}
                        onClick={() => onQuickCommand({ zone: groupe })}>
                        {n}
                      </button>
                    ))}
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </CardContent>
    </Card>
  )
}
