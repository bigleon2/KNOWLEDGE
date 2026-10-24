// Task 48 — PA-TEST-007 : QC §5 par skill (11 critères iphone17 / 12 iphone18 / 13 iphone19)
// sur « libération après guerre » (photographie argentique N&B 1944 — extension §6.6 :
// monochrome natif, grain préservé, aucune colorisation). createVision + thinking disabled.
// Usage: bun scripts/task48-pa007-qc.mjs <original> <sortie> <skill:17|18|19> <out_json>
import fs from 'fs';
const SDK = '/home/z/.bun/install/global/node_modules/z-ai-web-dev-sdk/dist/index.js';
const [,, origFile, outFile_, skill, outJson] = process.argv;
if (!origFile || !outFile_ || !skill || !outJson) {
  console.error('Usage: bun task48-pa007-qc.mjs <original> <sortie> <skill:17|18|19> <out_json>');
  process.exit(2);
}
const b64 = p => `data:${p.toLowerCase().endsWith('.png') ? 'image/png' : 'image/jpeg'};base64,${fs.readFileSync(p).toString('base64')}`;

const B6 = `camion militaire sombre à calandre verticale, câbles sur le pare-choc, AUCUN marquage ; homme casqué au sommet bras droit levé tenant un drapeau ; drapeau TRICOLORE français agité à gauche par un homme penché + drapeau AMÉRICAIN (étoiles et bandes) tenu plus bas ; jeune homme sourisant pull à col en V tenant une carabine posée sur ses genoux ; jeune femme robe claire à motifs jambes pendantes ; homme debout sur le pare-choc (costume sombre, cravate claire, main dans la poche, casque posé près de son pied droit) ; trois hommes en costumes sombres qui poussent le camion à gauche ; homme en chemise claire marchant vers la caméra ; garçon en chemise blanche courant vers la droite ; silhouette partielle de dos à l'extrême gauche ; immeuble haussmannien à gauche, bâtiment bas à droite (fenêtres grillagées, cheminées), arbres, rue étroite.`;

const RENDU = {
  17: 'rendu iPhone 17 Pro Max d\'époque (Photonic Engine NG) : monochrome strict, grain argentique préservé, netteté homogène propre, lumière maîtrisée sans halo, tone-mapping doux',
  18: 'rendu iPhone 18 Pro Max (ƒ/4.0 netteté étendue avant-arrière + Styles 3 texture/grain naturels) : monochrome strict, grain préservé',
  19: 'rendu iPhone 19 Pro Max ANTICIPÉ (ƒ/4.0 + pixel binning 16-en-1 « pixels fusionnés » : SNR accru, micro-détail préservé) : monochrome strict, grain préservé',
};

const is1944 = `CONTEXTE 1944 (extension v-bump §6.6) : photographie argentique N&B d'août 1944 — CONTRAINTE ABSOLUE : la sortie DOIT demeurer MONOCHROME (toute colorisation ou teinte colorée = KO grave, critère 4) et PRÉSERVER le grain argentique authentique (un grain écrasé/lissé = KO, critère 6 ; le grain du tirage d'époque fait partie du caractère de l'image).`;

let crit;
if (skill === '17') {
  crit = `Évalue ces 11 critères (OK=true / KO=false, 1 phrase chacun) :
1. Visages naturels, identité préservée (foule 1944 : expressions et postures des sujets identifiables)
2. Expressions, postures et orientations strictement identiques à l'original (homme casqué bras levé, jeune homme souriant à la carabine, pousseurs, garçon qui court…)
3. Éléments de scène identiques — inventaire de référence : ${B6}
4. Aucun élément ajouté ni supprimé (personnes, drapeaux, armes, véhicules, bâtiments, textes/marquages) ET AUCUNE COLORISATION (monochrome strict)
5. Aucun halo/écrêtage nouveau, aucun banding, aucun artéfact ; aucune teinte colorée ajoutée
6. Grain argentique authentique PRÉSERVÉ (pas écrasé, pas lissé en plastique ; nettoyage des taches/poussières uniquement)
7. Rendu demandé respecté : ${RENDU[17]}
8. Cadrage/plan identique (aucun recadrage, composition 3:2 entière)
9. Ratio 3:2 exact et résolution supérieure ou égale à l'original
10. Adéquation résolution source ↔ sortie (tirage 828×550 : agrandissement propre, aucun détail grossièrement inventé)
11. Focale : aucune demandée — conservation du cadre vérifiée`;
} else if (skill === '18') {
  crit = `Évalue ces 12 critères (OK=true / KO=false, 1 phrase chacun) :
1. Visages naturels, identité préservée (foule 1944 : expressions et postures des sujets identifiables)
2. Expressions, postures et orientations strictement identiques à l'original
3. Éléments de scène identiques — inventaire de référence : ${B6}
4. Aucun élément ajouté ni supprimé (personnes, drapeaux, armes, véhicules, bâtiments, textes/marquages) ET AUCUNE COLORISATION (monochrome strict)
5. Aucun halo/écrêtage nouveau, aucun banding, aucun artéfact ; aucune teinte colorée ajoutée
6. Grain argentique authentique PRÉSERVÉ (pas écrasé, pas lissé en plastique)
7. Rendu demandé respecté : ${RENDU[18]}
8. Cadrage/plan identique (aucun recadrage, composition 3:2 entière)
9. Ratio 3:2 exact et résolution supérieure ou égale à l'original
10. Adéquation résolution source ↔ sortie (agrandissement propre, aucun détail grossièrement inventé)
11. Focale : aucune demandée — conservation du cadre vérifiée
12. Ouverture simulée ƒ/4.0 respectée : netteté étendue de l'avant à l'arrière (camion, foule, immeubles), sans altération des sujets`;
} else {
  crit = `Évalue ces 13 critères (OK=true / KO=false, 1 phrase chacun) :
1. Visages naturels, identité préservée (foule 1944 : expressions et postures des sujets identifiables)
2. Expressions, postures et orientations strictement identiques à l'original
3. Éléments de scène identiques — inventaire de référence : ${B6}
4. Aucun élément ajouté ni supprimé (personnes, drapeaux, armes, véhicules, bâtiments, textes/marquages) ET AUCUNE COLORISATION (monochrome strict)
5. Aucun halo/écrêtage nouveau, aucun banding, aucun artéfact ; aucune teinte colorée ajoutée
6. Grain argentique authentique PRÉSERVÉ (pas écrasé, pas lissé en plastique)
7. Rendu demandé respecté : ${RENDU[19]}
8. Cadrage/plan identique (aucun recadrage, composition 3:2 entière)
9. Ratio 3:2 exact et résolution supérieure ou égale à l'original
10. Adéquation résolution source ↔ sortie (agrandissement propre, aucun détail grossièrement inventé)
11. Focale : aucune demandée — conservation du cadre vérifiée
12. Ouverture simulée ƒ/4.0 respectée : netteté étendue de l'avant à l'arrière, sans altération des sujets
13. Émulation pixel binning (R19) respectée : caractère « pixels fusionnés » (SNR accru, micro-détail fin préservé), SANS lissage plastique et SANS écraser le grain argentique`;
}

const N = skill === '17' ? 11 : (skill === '18' ? 12 : 13);
const PROMPT = `Voici deux photos : la PREMIÈRE est l'ORIGINAL, la SECONDE est un rendu « iPhone ${skill === '17' ? '17 Pro Max (génération 17, d\'époque)' : skill + ' Pro Max'} qualité max » obtenu par amélioration technique complète puis rendu conservateur. ${is1944} CONTRAINTE ABSOLUE DU PROPRIÉTAIRE : AUCUNE modification ni retouche de contenu — uniquement l'amélioration de la qualité. Compare-les avec une exigence de fidélité maximale et réponds UNIQUEMENT par un JSON valide.

${crit}

Puis une vérification de FIDÉLITÉ détaillée : liste TOUTE divergence (personne en plus/en moins, drapeau modifié, arme, véhicule, bâtiment, texte, colorisation, écrasement du grain, changement de contraste au-delà de l'amélioration demandée). Sois exhaustive et honnête : "aucune divergence" seulement si c'est vraiment le cas.

Format exact : {"qc": {"1": {"ok": true, "justif": "..."}, ..., "${N}": {"ok": true, "justif": "..."}}, "fidelite": {"divergences": ["..."] ou [], "verdict": "fidèle|divergences mineures|divergences majeures"}, "bilan": "..."}`;

const { default: ZAI } = await import(SDK);
const zai = await ZAI.create();
const response = await zai.chat.completions.createVision({
  messages: [{ role: 'user', content: [
    { type: 'text', text: PROMPT },
    { type: 'image_url', image_url: { url: b64(origFile) } },
    { type: 'image_url', image_url: { url: b64(outFile_) } },
  ]}],
  thinking: { type: 'disabled' },
});
const content = response.choices[0]?.message?.content || '';
const m = content.match(/\{[\s\S]*\}/);
if (!m) { console.error('Pas de JSON :', content.slice(0, 400)); process.exit(1); }
const parsed = JSON.parse(m[0]);
fs.writeFileSync(outJson, JSON.stringify(parsed, null, 2));
const qc = parsed.qc || {};
const oks = Object.entries(qc).filter(([, v]) => v.ok).length;
const kos = Object.keys(qc).filter(k => !qc[k]?.ok);
console.log(`QC skill ${skill} : ${oks}/${N} OK` + (kos.length ? ` — KO: ${kos.join(',')}` : ` — ${N}/${N}`));
console.log('Fidélité :', parsed.fidelite?.verdict, '| divergences :', JSON.stringify(parsed.fidelite?.divergences));
