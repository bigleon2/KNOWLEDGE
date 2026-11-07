"use client"

/**
 * page.tsx — Orchestrateur LEON TSI EDITEUR v11 (Extension React du studio v11).
 *
 * Parité CMDR + discussion itérations 1-3 : projets, tableau des mappings,
 * mass-edit (dupliquer/copier/coller/interaction/cible/canal ±1), dialogue
 * d'ajout pré-remplissable, Ctrl+L, vérification byte-exacte, export .tsi,
 * panneau MIDI, presets studio v11 (source de vérité partagée toolchain),
 * éditeur DSL, journal d'audit auto-évolutif.
 */

import { useCallback, useEffect, useMemo, useRef, useState } from "react"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Checkbox } from "@/components/ui/checkbox"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { toast } from "sonner"
import {
  ArrowRight, Check, Upload, ClipboardCopy, ClipboardPaste, Download, FilePlus,
  Layers, Music4, Plus, Repeat, ScrollText as AuditIcon, SlidersHorizontal, Trash2, Volume2,
} from "lucide-react"
import { ControllerView } from "@/components/leon/controller-view"
import { AddMappingDialog, type Prefill } from "@/components/leon/add-mapping-dialog"
import { MidiPanel } from "@/components/leon/midi-panel"
import { midi } from "@/lib/midi/midi-access"
import { midiLabel } from "@/lib/tsi/format"
import { parseTsi } from "@/lib/tsi/binary"
import { basculerCible, cyclerInteraction, coller, copier, decalerCanal, detecterConflits, dupliquer } from "@/lib/tsi/edit"
import { compilerDsl, mappingsDepuisDsl, type Preset } from "@/lib/studio/studio"
import type { AuditEntry, Mapping, ProjectData } from "@/lib/tsi/types"

interface Projet {
  id: string
  name: string
  data: string
  updatedAt: string
}

interface PresetApi { fichier: string; nom: string; description: string; version: string; nbMappings: number }

const DATA_VIERGE: ProjectData = {
  device: {
    name: "Traktor Kontrol S4 MK2", type: "MIDI",
    in_port: "Traktor Kontrol S4 MK2 In", out_port: "Traktor Kontrol S4 MK2 Out", deck_target: "Focus",
  },
  mappings: [],
}

export default function Home() {
  const [projets, setProjets] = useState<Projet[]>([])
  const [actif, setActif] = useState<Projet | null>(null)
  const [data, setData] = useState<ProjectData>(DATA_VIERGE)
  const [selection, setSelection] = useState<Set<number>>(new Set())
  const [pressePapiers, setPressePapiers] = useState<Mapping[]>([])
  const [dialogOuvert, setDialogOuvert] = useState(false)
  const [prefill, setPrefill] = useState<Prefill | null>(null)
  const [presets, setPresets] = useState<PresetApi[]>([])
  const [audit, setAudit] = useState<AuditEntry[]>([])
  const [dsl, setDsl] = useState("# contrôle -> fonction [couche]\nplay -> Play/Pause\nsync -> Sync [M1=1]\nloop_in -> Loop Set [M2=1]")
  const [enEdition, setEnEdition] = useState<number | null>(null)
  const editionRef = useRef<HTMLInputElement>(null)

  // --- chargements ---
  const chargerProjets = useCallback(async () => {
    const r = await fetch("/api/projects")
    const j = await r.json()
    setProjets(j.projets ?? [])
    return (j.projets ?? []) as Projet[]
  }, [])
  const chargerAudit = useCallback(async (id: string) => {
    const r = await fetch(`/api/projects/${id}/audit`)
    const j = await r.json()
    setAudit(j.audits ?? [])
  }, [])
  useEffect(() => {
    chargerProjets().then((ps) => { if (ps[0]) ouvrir(ps[0]) })
    fetch("/api/presets").then((r) => r.json()).then((j) => setPresets(j.presets ?? []))
  }, [])

  const ouvrir = (p: Projet) => {
    setActif(p)
    try { setData(JSON.parse(p.data)) } catch { setData(DATA_VIERGE) }
    setSelection(new Set())
    chargerAudit(p.id)
  }

  const persiste = useCallback(async (nouveau: ProjectData, action: string, detail: string) => {
    if (!actif) return
    await fetch(`/api/projects/${actif.id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ data: JSON.stringify(nouveau) }),
    })
    await fetch(`/api/projects/${actif.id}/audit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action, detail }),
    })
    setData(nouveau)
    chargerAudit(actif.id)
    chargerProjets()
  }, [actif, chargerAudit, chargerProjets])

  // --- mappings ---
  const ajouterMapping = (m: Mapping, noteProvisoire?: boolean) => {
    const nouveau = { ...data, mappings: [...data.mappings, m] }
    const conflits = detecterConflits(nouveau.mappings)
    persiste(nouveau, "ajout", `${m.nom} (${m.type}${m.midi ? ` ${midiLabel(m.midi)}` : ""})`)
    if (noteProvisoire) toast(`Mapping ajouté : ${m.nom}`, { description: `note provisoire ${m.midi ? midiLabel(m.midi) : ""} — capturez la vraie note (Learn ou Ctrl+L)` })
    else toast(`Mapping ajouté : ${m.nom}`, conflits.length ? { description: `${conflits.length} conflit(s) signalé(s) par l'audit` } : undefined)
  }

  const majMappings = (ms: Mapping[], action: string, detail: string) => {
    persiste({ ...data, mappings: ms }, action, detail)
  }

  const opsSelection = () => {
    const idx = [...selection]
    const applique = (f: (m: Mapping) => Mapping, action: string) => {
      const ms = data.mappings.map((m, i) => (selection.has(i) ? f(m) : m))
      majMappings(ms, action, `${idx.length} mapping(s)`)
      toast(`${action} — ${idx.length} mapping(s)`)
    }
    return {
      dupliquer: () => {
        const nouveaux: Mapping[] = []
        const ms = [...data.mappings]
        for (const i of idx) nouveaux.push(dupliquer(data.mappings[i], ms))
        majMappings([...ms, ...nouveaux], "duplication", `${idx.length} mapping(s)`)
      },
      copier: () => { setPressePapiers(copier(idx.map((i) => data.mappings[i]))); toast(`Copié : ${idx.length}`) },
      coller: () => {
        const ajout = coller(pressePapiers, data.mappings)
        majMappings([...data.mappings, ...ajout], "collage", `${ajout.length} mapping(s)`)
      },
      interaction: () => applique(cyclerInteraction, "interaction"),
      cible: () => applique(basculerCible, "cible"),
      canalPlus: () => applique((m) => decalerCanal(m, 1), "canal +1"),
      canalMoins: () => applique((m) => decalerCanal(m, -1), "canal -1"),
      supprimer: () => {
        const ms = data.mappings.filter((_, i) => !selection.has(i))
        majMappings(ms, "suppression", `${idx.length} mapping(s)`)
        setSelection(new Set())
      },
    }
  }

  // --- contrôleur : chips → dialogue pré-rempli ---
  const onQuickCommand = (p: Prefill) => {
    setPrefill(p)
    setDialogOuvert(true)
  }

  // --- Ctrl+L (parité CMDR) : Learn sur le mapping en édition ---
  useEffect(() => {
    const h = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "l" && enEdition !== null) {
        e.preventDefault()
        midi.attendreProchainMessage((msg) => {
          const note = `Ch${String(msg.channel).padStart(2, "0")}.${msg.kind === "CC" ? "CC" : "NOTE"}.${String(msg.data1 ?? 0).padStart(3, "0")}`
          setData((d) => {
            const ms = d.mappings.map((m, i) =>
              i === enEdition ? { ...m, midi: { ...(m.midi ?? { canal: 0, message: "NOTE" as const, numero: 0, mode: "Direct" as const }), ...(() => { const [canal, , numero] = [Number(String(msg.channel).padStart(2, "0")), 0, msg.data1 ?? 0]; return { canal, numero } })() } } : m,
            )
            return { ...d, mappings: ms }
          })
          toast(`Ctrl+L : note capturée ${note}`)
        })
        toast("Ctrl+L : jouez le contrôle…")
      }
    }
    window.addEventListener("keydown", h)
    return () => window.removeEventListener("keydown", h)
  }, [enEdition])

  // --- studio v11 ---
  const appliquerPreset = async (p: PresetApi) => {
    const presetJson = (await import(`@/data/presets/${p.fichier.replace(/\.json$/, "")}.json`))
      .default as unknown as Preset
    const mappings = presetJson.mappings.map((m) => ({ ...m }))
    const nouveau = { ...data, mappings: [...data.mappings, ...mappings] }
    await persiste(nouveau, `preset ${p.nom}`, `${mappings.length} mapping(s) appliqués (source de vérité partagée toolchain)`)
    toast(`Preset appliqué : ${p.nom} (+${mappings.length})`)
  }

  const compilerEtAppliquer = () => {
    const { lignes, erreurs } = compilerDsl(dsl)
    if (erreurs.length) { toast.error(`DSL : ${erreurs[0]}`); return }
    const mappings = mappingsDepuisDsl(lignes, data)
    const nouveau = { ...data, mappings: [...data.mappings, ...mappings] }
    persiste(nouveau, "DSL", `${lignes.length} ligne(s) compilée(s)`)
    toast(`DSL : ${lignes.length} mapping(s) générés`)
  }

  const importerTsi = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0]
    if (!f || !actif) return
    const texte = await f.text()
    try {
      const dataImport = parseTsi(texte)
      await persiste(dataImport, "import", `${f.name} — ${dataImport.mappings.length} mapping(s)`)
      toast.success(`Importé : ${f.name} (${dataImport.mappings.length} mappings)`)
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Import impossible", {
        description: "Les .tsi réels Traktor (blob DIOM) s'inspectent via le pont écosystème tsi-toolkit (R4).",
      })
    }
    e.target.value = ""
  }

  const verifier = async () => {
    if (!actif) return
    const r = await fetch(`/api/projects/${actif.id}/verify`, { method: "POST" })
    const j = await r.json()
    if (j.verdict === "BYTE-EXACT") toast.success(`Vérification : ${j.verdict} (${j.mappings} mappings, ${j.taille} octets)`)
    else toast.error(`Vérification : ${j.verdict} — ${j.detail}`)
  }

  const nouveauProjet = async () => {
    const nom = prompt("Nom du projet :", `Mapping S4 MK2 ${new Date().toISOString().slice(0, 10)}`)
    if (!nom) return
    const r = await fetch("/api/projects", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ name: nom }) })
    const j = await r.json()
    await chargerProjets()
    ouvrir(j.projet)
    toast(`Projet créé : ${nom}`)
  }

  const conflits = useMemo(() => detecterConflits(data.mappings), [data])

  return (
    <div className="flex min-h-screen flex-col bg-background">
      <header className="border-b px-4 py-3">
        <div className="mx-auto flex max-w-7xl flex-wrap items-center gap-3">
          <Music4 className="size-5 text-primary" />
          <div>
            <h1 className="text-lg font-semibold leading-tight">LEON TSI EDITEUR <span className="text-muted-foreground">v11</span></h1>
            <p className="text-xs text-muted-foreground">Éditeur de mapping MIDI (TSI) — Traktor Kontrol S4 MK2 · Extension React du studio v11</p>
          </div>
          <div className="ml-auto flex items-center gap-2">
            <Select value={actif?.id ?? ""} onValueChange={(id) => { const p = projets.find((x) => x.id === id); if (p) ouvrir(p) }}>
              <SelectTrigger className="h-8 w-52 text-xs"><SelectValue placeholder="Projet…" /></SelectTrigger>
              <SelectContent>{projets.map((p) => <SelectItem key={p.id} value={p.id}>{p.name}</SelectItem>)}</SelectContent>
            </Select>
            <Button size="sm" variant="outline" onClick={nouveauProjet}><FilePlus className="mr-1 size-3.5" />Projet</Button>
          </div>
        </div>
      </header>

      <main className="mx-auto w-full max-w-7xl flex-1 space-y-4 px-4 py-4">
        <div className="grid gap-4 lg:grid-cols-3">
          <div className="lg:col-span-2 space-y-4">
            <ControllerView onQuickCommand={onQuickCommand} />
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="flex flex-wrap items-center gap-2 text-base">
                  <SlidersHorizontal className="size-4" /> Mappings
                  <Badge variant="outline">{data.mappings.length}</Badge>
                  {conflits.length > 0 && <Badge variant="destructive">{conflits.length} conflit(s)</Badge>}
                  <div className="ml-auto flex flex-wrap gap-1.5">
                    <Button size="sm" onClick={() => { setPrefill(null); setDialogOuvert(true) }}><Plus className="mr-1 size-3.5" />Mapping</Button>
                    {(() => { const ops = opsSelection(); return (
                      <>
                        <Button size="sm" variant="outline" disabled={!selection.size} onClick={ops.dupliquer}><Repeat className="mr-1 size-3.5" />Dupliquer</Button>
                        <Button size="sm" variant="outline" disabled={!selection.size} onClick={ops.copier}><ClipboardCopy className="size-3.5" /></Button>
                        <Button size="sm" variant="outline" disabled={!pressePapiers.length} onClick={ops.coller}><ClipboardPaste className="size-3.5" /></Button>
                        <Button size="sm" variant="outline" disabled={!selection.size} onClick={ops.interaction}>Interaction</Button>
                        <Button size="sm" variant="outline" disabled={!selection.size} onClick={ops.cible}>Cible</Button>
                        <Button size="sm" variant="outline" disabled={!selection.size} onClick={ops.canalPlus}>Canal +1</Button>
                        <Button size="sm" variant="outline" disabled={!selection.size} onClick={ops.canalMoins}>−1</Button>
                        <Button size="sm" variant="outline" disabled={!selection.size} onClick={ops.supprimer}><Trash2 className="size-3.5" /></Button>
                      </>
                    ) })()}
                    <Button size="sm" variant="outline" onClick={verifier}><Check className="mr-1 size-3.5" />Vérifier</Button>
                    <Button size="sm" variant="outline" disabled={!actif} asChild>
                      <a href={actif ? `/api/projects/${actif.id}/export` : "#"}><Download className="mr-1 size-3.5" />Exporter .tsi</a>
                    </Button>
                    <label className="inline-flex h-8 cursor-pointer items-center rounded-md border px-2.5 text-xs hover:bg-muted">
                      <Upload className="mr-1 size-3.5" />Importer .tsi
                      <input type="file" accept=".tsi,.xml" className="hidden" onChange={importerTsi} />
                    </label>
                  </div>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="max-h-80 overflow-y-auto rounded-md border">
                  <table className="w-full text-xs">
                    <thead className="sticky top-0 bg-muted/60 text-left text-muted-foreground">
                      <tr>
                        <th className="w-8 px-2 py-1.5" />
                        <th className="px-2 py-1.5">Sens</th>
                        <th className="px-2 py-1.5">Commande</th>
                        <th className="px-2 py-1.5">Groupe</th>
                        <th className="px-2 py-1.5">Note / LED</th>
                        <th className="px-2 py-1.5">Mode</th>
                        <th className="px-2 py-1.5">Couche</th>
                      </tr>
                    </thead>
                    <tbody>
                      {data.mappings.length === 0 && (
                        <tr><td colSpan={7} className="px-2 py-6 text-center text-muted-foreground">
                          Aucun mapping — cliquez un chip de la vue contrôleur, « + Mapping », ou appliquez un preset du studio v11.
                        </td></tr>
                      )}
                      {data.mappings.map((m, i) => {
                        const couche = m.modifier ? Object.entries(m.modifier).map(([k, v]) => `${k}=${v}`).join(",") : "BASE"
                        return (
                          <tr key={i} className={`border-t ${selection.has(i) ? "bg-primary/5" : ""}`}>
                            <td className="px-2 py-1.5">
                              <Checkbox checked={selection.has(i)}
                                onCheckedChange={(c) => setSelection((s) => { const n = new Set(s); if (c) n.add(i); else n.delete(i); return n })} />
                            </td>
                            <td className="px-2 py-1.5"><Badge variant={m.type === "IN" ? "default" : "secondary"}>{m.type}</Badge></td>
                            <td className="px-2 py-1.5" title={m.nom}>{m.controle}</td>
                            <td className="px-2 py-1.5 text-muted-foreground">{m.groupe}</td>
                            <td className="px-2 py-1.5 font-mono">
                              <Input ref={i === enEdition ? editionRef : undefined}
                                className="h-6 w-28 font-mono text-xs"
                                defaultValue={m.midi ? midiLabel(m.midi) : m.led ? `LED ${m.led.numero}` : "—"}
                                onFocus={() => setEnEdition(i)}
                                onBlur={() => setEnEdition(null)}
                                onChange={(e) => {
                                  const val = e.target.value
                                  if (/^Ch\d+\.(NOTE|CC)\.\d+$/.test(val)) {
                                    try {
                                      const [ch, msg, num] = val.split(".")
                                      setData((d) => ({ ...d, mappings: d.mappings.map((mm, j) =>
                                        j === i && mm.midi ? { ...mm, midi: { ...mm.midi, canal: Number(ch.slice(2)), message: msg as "NOTE" | "CC", numero: Number(num) } } : mm) }))
                                    } catch { /* saisie partielle */ }
                                  }
                                }}
                              />
                            </td>
                            <td className="px-2 py-1.5 text-muted-foreground">{m.midi?.mode ?? m.led ? m.midi?.mode ?? "LED on/off" : "—"}</td>
                            <td className="px-2 py-1.5 text-muted-foreground">{couche}</td>
                          </tr>
                        )
                      })}
                    </tbody>
                  </table>
                </div>
                <p className="mt-2 text-[11px] text-muted-foreground">
                  Sélectionnez une ligne puis Ctrl+L pour capturer la note au contrôleur (parité CMDR). Sauvegarde explicite via l&apos;édition de ligne (persistée par frappe).
                </p>
              </CardContent>
            </Card>
          </div>

          <div className="space-y-4">
            <MidiPanel />
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="flex items-center gap-2 text-base"><Layers className="size-4" /> Studio v11 — Presets &amp; DSL</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="space-y-1.5">
                  {presets.map((p) => (
                    <div key={p.fichier} className="flex items-center gap-2 rounded-md border p-2">
                      <div className="min-w-0 flex-1">
                        <p className="truncate text-xs font-medium">{p.nom}</p>
                        <p className="truncate text-[11px] text-muted-foreground">{p.description}</p>
                      </div>
                      <Badge variant="outline" className="text-[10px]">{p.nbMappings}</Badge>
                      <Button size="sm" onClick={() => appliquerPreset(p)}>Appliquer</Button>
                    </div>
                  ))}
                </div>
                <div className="space-y-1.5">
                  <p className="text-xs font-medium">Éditeur DSL (source de vérité partagée toolchain)</p>
                  <textarea
                    className="h-24 w-full rounded-md border bg-muted/40 p-2 font-mono text-[11px]"
                    value={dsl} onChange={(e) => setDsl(e.target.value)}
                    spellCheck={false}
                  />
                  <Button size="sm" className="w-full" onClick={compilerEtAppliquer}>
                    <ArrowRight className="mr-1 size-3.5" />Compiler &amp; générer
                  </Button>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="flex items-center gap-2 text-base">
                  <AuditIcon className="size-4" /> Audit auto-évolutif
                  <Badge variant="outline" className="text-[10px]">{audit.length}</Badge>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="max-h-52 space-y-1 overflow-y-auto text-[11px] text-muted-foreground">
                  {audit.length === 0 && <p>Aucune entrée — chaque action (preset, DSL, mass-edit) alimente le journal.</p>}
                  {audit.map((a) => (
                    <div key={a.id} className="rounded border px-2 py-1">
                      <span className="font-medium text-foreground">{a.action}</span> — {a.detail}
                      <span className="ml-1 opacity-70">({a.mappings} m. / {a.conflits} c. — {new Date(a.createdAt).toLocaleTimeString("fr-FR")})</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>

      <footer className="border-t px-4 py-3 text-center text-[11px] text-muted-foreground">
        LEON TSI EDITEUR v11 — catalogue scellé {`455`} commandes · {`125`} entrées / {`220`} sorties usines · format canonique validé par l&apos;arbitre tsi-validator (R4 toolchain)
      </footer>

      <AddMappingDialog
        key={`dlg-${JSON.stringify(prefill)}-${dialogOuvert}`}
        open={dialogOuvert}
        prefill={prefill}
        onClose={() => { setDialogOuvert(false); setPrefill(null) }}
        onSubmit={ajouterMapping}
        mappingsExistants={data.mappings}
      />
    </div>
  )
}
