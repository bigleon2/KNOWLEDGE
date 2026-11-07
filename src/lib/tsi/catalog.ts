/**
 * catalog.ts — Accès au catalogue scellé (455 commandes — fusion toolkit réel DJTT +
 * familles documentées de la discussion) et aux contrôles S4 MK2 (125 in / 220 out).
 *
 * Génération mécanique : scripts/task40-generer-catalogue-app.py (zéro valeur
 * inventée — sources scellées uniquement, provenance par entrée).
 */

import catalogueBrut from "@/data/commands.json"
import controlsBrut from "@/data/s4mk2-controls.json"
import type { Catalogue, CatalogueCommande, S4Controls } from "./types"

export const catalogue = catalogueBrut as unknown as Catalogue
export const s4Controls = controlsBrut as unknown as S4Controls

/** Commande résolue avec id numérique stable. */
export type CommandeEtendue = CatalogueCommande

/** Toutes les commandes (ordre d'id stable). */
export function toutesCommandes(): CommandeEtendue[] {
  return Object.entries(catalogue.commandes)
    .map(([idStr, c]) => ({
      id: Number(idStr), nom: c.nom, categorie: c.categorie,
      provenance: c.provenance as CatalogueCommande["provenance"],
      ...(c.cmdrId !== undefined ? { cmdrId: c.cmdrId } : {}),
    }))
    .sort((a, b) => a.id - b.id)
}

/** Recherche insensible à la casse sur le nom + catégorie. */
export function rechercherCommandes(q: string): CommandeEtendue[] {
  const aiguille = q.trim().toLowerCase()
  if (!aiguille) return toutesCommandes()
  return toutesCommandes().filter(
    (c) => c.nom.toLowerCase().includes(aiguille) || c.categorie.toLowerCase().includes(aiguille),
  )
}

/** Catégories triées avec leurs tailles. */
export function categoriesAvecTaille(): { nom: string; n: number }[] {
  return Object.entries(catalogue.categories)
    .map(([nom, ids]) => ({ nom, n: ids.length }))
    .sort((a, b) => b.n - a.n || a.nom.localeCompare(b.nom))
}

/**
 * Les 8 modules « Modes & Modules » (discussion itération 3) — appartenance
 * dérivée mécaniquement du catalogue scellé par motifs de noms (aucun id codé
 * en dur, la source de vérité fait foi) + documentation sourcée par module.
 */
export interface ModuleDoc {
  cle: ModuleKey
  titre: string
  doc: string
  motif: RegExp
}

export type ModuleKey =
  | "flux" | "remix" | "sequencer" | "looprec" | "audiorec" | "advanced" | "live" | "ableton"

export const MODULES: ModuleDoc[] = [
  { cle: "flux", titre: "Flux", doc: "Flux Mode/reverse — §5.2.4 manuel NI ; 2 chips usine (cid 30).", motif: /flux/i },
  { cle: "remix", titre: "Remix Deck & Sampler", doc: "26+ commandes Remix/Samples + Submix — §6.3.9 manuel NI ; 8 slots usine (cid 9-12).", motif: /remix|sample|submix/i },
  { cle: "sequencer", titre: "Step Sequencer", doc: "20 commandes (734-756 discussion) : Sequencer On, Swing, Pattern Length, Enable Step 1-16.", motif: /sequencer/i },
  { cle: "looprec", titre: "Loop Recorder", doc: "§6.6 + §12.5 manuel NI : REC overdub au beat, SIZE, UNDO punch in/out, PLAY, DRY/WET ; 5 chips usine (cid 47-51).", motif: /loop ?rec/i },
  { cle: "audiorec", titre: "Audio Recorder", doc: "4 commandes (2056/2055/29/3084 discussion) — commandes logicielles pures → chips Learn.", motif: /audio ?rec|broadcast/i },
  { cle: "advanced", titre: "Advanced Panel", doc: "Panneau Remix avancé — p. 122-124 manuel NI (2 commandes discussion 2299/2298).", motif: /advanced panel|deck flavor/i },
  { cle: "live", titre: "Live Input", doc: "Deck Flavor Track/Remix/Live Input — §7.4.1-7.4.2 manuel NI (Live Input = deck flavor).", motif: /live input|deck flavor/i },
  { cle: "ableton", titre: "Ableton / MIDI", doc: "24 Global MIDI Controls (850-873 discussion — relais vers applications externes) + Ableton Link.", motif: /global midi control|ableton/i },
]

/** Commandes du module (dérivées) + chips physiques associés (table CC scellée). */
export function commandesModule(m: ModuleDoc): CommandeEtendue[] {
  return toutesCommandes().filter((c) => m.motif.test(c.nom))
}

export function chipsModule(m: ModuleDoc): { nom: string; cc: number; type: "fader" | "bouton" }[] {
  const motifsChips: Record<ModuleKey, RegExp> = {
    flux: /flux/i,
    remix: /remix slot/i,
    sequencer: /deck c|remix/i,
    looprec: /loop recorder/i,
    audiorec: /master/i,
    advanced: /hotcue/i,
    live: /deck b/i,
    ableton: /fx/i,
  }
  const out: { nom: string; cc: number; type: "fader" | "bouton" }[] = []
  for (const { chips } of Object.values(s4Controls.tableCC).map((lst) => ({ chips: lst }))) {
    for (const c of chips) if (motifsChips[m.cle].test(c.nom)) out.push(c)
  }
  return out
}
