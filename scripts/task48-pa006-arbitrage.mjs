// Task 48 — PA-TEST-006 : arbitrage ciblé critère 5 (inscription t-shirt) — vision sur collage
// PNG produit par task48-pa006-arbitrage-crop.py (PIL). createVision + thinking disabled (remède SSE).
import fs from 'fs';
const SDK = '/home/z/.bun/install/global/node_modules/z-ai-web-dev-sdk/dist/index.js';
const [, , collagePng, outJson] = process.argv;
const b64 = `data:image/png;base64,${fs.readFileSync(collagePng).toString('base64')}`;

const PROMPT = `Voici deux extractions (côte à côte, séparées par une barre blanche) de la MÊME zone d'une photo : à GAUCHE l'ORIGINAL, à DROITE un rendu amélioré. La zone contient un homme au t-shirt gris avec une INSCRIPTION GRAPHIQUE rose/violette. Question d'arbitrage précise : 1) Le texte/graphisme de l'inscription est-il EXACTEMENT le même dans les deux (mêmes lettres, même motif, aucun texte inventé, modifié ou supprimé — garde G2) ? 2) La netteté/lisibilité de l'inscription est-elle conservée de manière acceptable (une très légère douceur due à l'agrandissement ×1,9 n'est PAS un défaut, une altération rendant le texte méconnaissable l'est) ? 3) L'expression du visage et les détails (piercing, bouche entrouverte) sont-ils identiques ? Réponds UNIQUEMENT par un JSON valide : {"inscription_identique": true/false, "lettres_identiques": "...", "nettete_acceptable": true/false, "visage_identique": true/false, "verdict": "intact|altere", "confiance": "haute|moyenne|basse", "justification": "..."}`;

const { default: ZAI } = await import(SDK);
const zai = await ZAI.create();
const response = await zai.chat.completions.createVision({
  messages: [{ role: 'user', content: [
    { type: 'text', text: PROMPT },
    { type: 'image_url', image_url: { url: b64 } },
  ]}],
  thinking: { type: 'disabled' },
});
const content = response.choices[0]?.message?.content || '';
const m = content.match(/\{[\s\S]*\}/);
if (!m) { console.error('Pas de JSON :', content.slice(0, 400)); process.exit(1); }
fs.writeFileSync(outJson, m[0]);
console.log(m[0]);
