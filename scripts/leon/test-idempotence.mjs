// test-idempotence.mjs — Round-trips TSI byte-exacts $FACON2 du LEON TSI EDITEUR v11.
//
// Héritage : harnais discussion b6170b8b (12/12 racine, 23 avec toolchain) — Task 40.
// Méthode : pour chaque source (preset scellé, DSL généré, projet réel enrichi),
// serializeTsi → parseTsi → serializeTsi DOIT être un point fixe (byte-exact),
// et l'export d'un projet non modifié DOIT être stable au re-jeu (idempotence ×2).
import { serializeTsi, parseTsi } from "/home/z/my-project/src/lib/tsi/binary.ts"
import { compilerDsl, mappingsDepuisDsl, appliquerPreset } from "/home/z/my-project/src/lib/studio/studio.ts"
import preset from "/home/z/my-project/src/data/presets/freeze-mode.json" with { type: "json" }

let passed = 0, failed = 0
const check = (ok, nom, detail = "") => {
  if (ok) { passed++; console.log(`  [PASS] ${nom}`) }
  else { failed++; console.log(`  [FAIL] ${nom} — ${detail}`) }
}

const base = {
  device: { name: "Traktor Kontrol S4 MK2", type: "MIDI", in_port: "In", out_port: "Out", deck_target: "Focus" },
  mappings: [],
}

// 1. Preset scellé (source de vérité partagée toolkit)
const projPreset = { device: (preset).device, mappings: appliquerPreset(base, preset) }
const t1 = serializeTsi(projPreset)
check(t1 === serializeTsi(parseTsi(t1)), "1. preset Freeze Mode (15 mappings) round-trip byte-exact")

// 2. DSL → mappings → round-trip
const dsl = `# contrôle -> fonction [couche]\nplay -> Play/Pause\nsync -> Sync [M1=1]\ncue -> Cue/Set\nloop_in -> Loop Set [M2=1]\nflux -> Flux Mode`
const { lignes, erreurs } = compilerDsl(dsl)
check(erreurs.length === 0 && lignes.length === 5, "2. DSL 5 lignes compilé sans erreur", erreurs.join("; "))
const projDsl = { ...base, mappings: [...base.mappings, ...mappingsDepuisDsl(lignes, base)] }
const t2 = serializeTsi(projDsl)
check(t2 === serializeTsi(parseTsi(t2)), "3. projet DSL (modifiers M1/M2) round-trip byte-exact")

// 4. Round-trip ×2 (idempotence : re-jeu du re-jeu)
const r1 = serializeTsi(parseTsi(t2))
const r2 = serializeTsi(parseTsi(r1))
check(r1 === r2, "4. idempotence ×2 (re-jeu byte-stable)")

// 5. XML échappement (nom avec quotes/ampersand — convention regex.test + replace)
const projXml = { ...base, mappings: [{ nom: `Deck "A" & B — test`, type: "IN", groupe: "Deck A", controle: "Play/Pause", midi: { canal: 0, message: "NOTE", numero: 60, mode: "Direct" } }] }
const t5 = serializeTsi(projXml)
check(t5.includes("&quot;") && t5.includes("&amp;"), "5. échappement XML des quotes/&")
const p5 = parseTsi(t5)
check(p5.mappings[0].nom === `Deck "A" & B — test`, "6. déséchappement round-trip (nom intact)")

// 7. Rejet propre du format réel Traktor (blob DIOM — pont écosystème R4)
let rejetOk = false
try { parseTsi('<?xml version="1.0"?><NIXML><TraktorSettings><Entry Name="DeviceIO.Config.Controller" Type="3"/></TraktorSettings></NIXML>') }
catch (e) { rejetOk = e.message.includes("pont écosystème") }
check(rejetOk, "7. rejet propre du format réel (TraktorSettings → pont écosystème)")

// 8. Rejet propre racine inconnue
let rejet2 = false
try { parseTsi("<HTML><body>pas un tsi</body></HTML>") }
catch (e) { rejet2 = e.message.includes("Racine inconnue") }
check(rejet2, "8. rejet propre racine inconnue")

// 9. Modifier M1-M8 (ATTR_RE A-Z0-9_ — bug historique attrapé par verify Task 40)
const projMod = { ...base, mappings: [{ nom: "Slice 8", type: "IN", groupe: "Deck A", controle: "Slice 8", modifier: { M1: 1, M8: 0 }, midi: { canal: 0, message: "NOTE", numero: 55, mode: "Direct" } }] }
const t9 = serializeTsi(projMod)
const p9 = parseTsi(t9)
check(p9.mappings[0].modifier?.M1 === 1 && p9.mappings[0].modifier?.M8 === 0 && t9 === serializeTsi(p9), "9. modifiers M1-M8 round-trip (chiffres)")

// 10-12. Anti-collision générateur DSL + conflits + LED OUT
const avecConflit = { ...base, mappings: [
  { nom: "A", type: "IN", groupe: "D", controle: "X", midi: { canal: 0, message: "NOTE", numero: 36, mode: "Direct" } },
  { nom: "B", type: "IN", groupe: "D", controle: "X", midi: { canal: 0, message: "NOTE", numero: 36, mode: "Direct" } },
] }
const { detecterConflits } = await import("/home/z/my-project/src/lib/tsi/edit.ts")
check(detecterConflits(avecConflit.mappings).length === 1, "10. détection conflit (même canal/note/couche)")
const projLed = { ...base, mappings: [{ nom: "LED", type: "OUT", groupe: "Deck A", controle: "Play LED", led: { numero: 36, on: 127, off: 0 } }] }
const t11 = serializeTsi(projLed)
check(t11.includes('<LED NUMBER="36" ON="127" OFF="0" MODE="Output"/>') && t11 === serializeTsi(parseTsi(t11)), "11. spec LED OUT round-trip (canon NISYSTEM + MODE Output E6)")
check(serializeTsi(projPreset).length > 3000, "12. taille export preset réaliste (>3 Ko)")

console.log(`HARNAIS : ${passed}/12 PASS, ${failed} FAIL`)
process.exit(failed === 0 ? 0 : 1)
