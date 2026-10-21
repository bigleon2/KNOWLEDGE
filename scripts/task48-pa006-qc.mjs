// Task 48 — PA-TEST-006 : QC §5 (grille 13 critères v0.10.0 — rendu iphone19_max ANTICIPÉ avec
// émulation pixel binning R19) — REMÈDE SSE : zai.chat.completions.createVision + thinking
// disabled (pattern éprouvé task46-s2-qc.mjs / task47-pa005-qc.mjs) — jamais de stream.
// Usage: bun scripts/task48-pa006-qc.mjs <original> <sortie> <photo:copines|potos> <sortie_json>
import fs from 'fs';
const SDK = '/home/z/.bun/install/global/node_modules/z-ai-web-dev-sdk/dist/index.js';
const [,, origFile, outFile_, photo, outJson] = process.argv;
if (!origFile || !outFile_ || !photo || !outJson) {
  console.error('Usage: bun task48-pa006-qc.mjs <original> <sortie> <photo:copines|potos> <sortie_json>');
  process.exit(2);
}
const b64 = p => `data:${p.toLowerCase().endsWith('.png') ? 'image/png' : 'image/jpeg'};base64,${fs.readFileSync(p).toString('base64')}`;

const B6 = {
  copines: `six femmes : queue-de-cheval châtain clair sourire discret tête penchée droite (débardeur noir, bracelets, verre brun, sac ethnique) ; brune mi-longue large sourire dents (débardeur gris, collier ras-du-cou) ; châtaine courte sourire très large yeux plissés tête tournée à droite (haut rouge, accessoire vert cou) ; casquette noire sourire éclatant bouche ouverte (collier perlé blanc, badge FESTIVAL lanière verte, verre rosé) ; blonde attachée rire franc yeux fermés tête rejetée arrière tournée à gauche (débardeur kaki, manchette) ; brune courte grand sourire tête penchée gauche (caraco blanc, boucles pendantes). Décor : tente blanche h.g., fond nocturne noir, homme torse nu partiel à droite.`,
  potos: `six personnes en cercle : longue brune raie au milieu TÊTE EN BAS au centre sourire large bouche ouverte (piercing septum, objet vert, maquillage yeux) ; brune longue sourire timide tête penchée visage partiellement chevauché par les cheveux de la première (chevauchement à préserver) ; longue brune ondulée sourire en coin (haut moutarde, casquette noire À L'ENVERS, eye-liner, piercing nostril droit) ; homme dégarni dessus NEUTRE sérieux lèvres serrées strictement de face ; homme tempes dégarnies neutre (lunettes fines métalliques, barbe plusieurs jours) ; homme châtains dégarnis air surpris bouche entrouverte (t-shirt gris INSCRIPTION graphique rose/violette, piercing nostril). Décor : mur intérieur clair, ligne d'angle verticale.`,
};

const PROMPT = `Voici deux photos : la PREMIÈRE est l'ORIGINAL, la SECONDE est un rendu « iPhone 19 Pro Max qualité max » (génération anticipée, v0.10.0 avec émulation pixel binning) obtenu par amélioration technique complète puis rendu nuit propre. CONTRAINTE ABSOLUE DU PROPRIÉTAIRE : AUCUNE modification ni retouche de contenu — uniquement l'amélioration de la qualité. Compare-les avec une exigence de fidélité maximale et réponds UNIQUEMENT par un JSON valide.

Évalue ces 13 critères (OK=true / KO=false, 1 phrase de justification chacun) :
1. Visages naturels, identité préservée
2. Expressions faciales strictement identiques à l'original : sourire, regard, orientation de CHAQUE tête (détaille personne par personne)
3. Coupes de cheveux, vêtements, accessoires, morphologie identiques — inventaire de référence : ${B6[photo]}
4. Aucun élément ajouté à la scène (décor, objets, personnes, piercings, lunettes, texte) ni supprimé
5. Aucun halo/écrêtage sur les sources lumineuses, aucun banding, aucun artefact résiduel ; texte intact (badge/inscription) si applicable
6. Bruit perceptible quasi nul, sans effet plastique (peau naturelle, textures conservées)
7. Rendu iphone19_max respecté : netteté maximale zones utiles (visages prioritaires), mode nuit propre, netteté étendue du groupe avant-arrière (ouverture ƒ/4.0), dynamique étendue sans HDR visible, textures réalistes
8. Cadrage/plan identique à l'original (aucun recadrage)
9. Ratio 4:3 exact et résolution supérieure ou égale à l'original
10. Adéquation résolution source ↔ sortie (agrandissement propre, pas de détails inventés grossièrement)
11. Focale : aucune demandée — vérifie simplement la conservation du cadre et du cadrage
12. Ouverture simulée ƒ/4.0 respectée : netteté étendue de l'avant à l'arrière, sans altération des sujets
13. Émulation pixel binning (R19) respectée : caractère « pixels fusionnés » — SNR accru, bruit maîtrisé, micro-détail préservé, SANS lissage plastique et SANS altération des sujets

Puis une vérification de FIDÉLITÉ détaillée : liste TOUTE divergence (expression, orientation de tête, coiffure, vêtement, accessoire, piercing, lunette, élément de décor, personne en plus/en moins, texte, objet, changement de style au-delà de l'amélioration qualité). Sois exhaustive et honnête : "aucune divergence" seulement si c'est vraiment le cas.

Format exact : {"qc": {"1": {"ok": true, "justif": "..."}, ..., "13": {"ok": true, "justif": "..."}}, "fidelite": {"divergences": ["..."] ou [], "verdict": "fidèle|divergences mineures|divergences majeures"}, "bilan": "..."}`;

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
console.log(`QC ${photo} : ${oks}/13 OK` + (kos.length ? ` — KO: ${kos.join(',')}` : ' — 13/13'));
console.log('Fidélité :', parsed.fidelite?.verdict, '| divergences :', JSON.stringify(parsed.fidelite?.divergences));
