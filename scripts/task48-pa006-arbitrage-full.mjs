// Task 48 — PA-TEST-006 : arbitrage pleine image de l'inscription du t-shirt (critère 5 / G2).
// Collage vertical : HAUT = original (604×453), BAS = candidat (1152×864 réduit à 604×453 pour
// comparaison à échelle commune). createVision + thinking disabled (remède SSE).
import fs from 'fs';
import { execSync } from 'child_process';
const SDK = '/home/z/.bun/install/global/node_modules/z-ai-web-dev-sdk/dist/index.js';
const [, , origFile, candFile, outPng, outJson] = process.argv;

// collage via PIL (python3) — pas de dépendance canvas
execSync(`python3 - <<'PY'
from PIL import Image, ImageDraw
orig = Image.open("${origFile}").convert("RGB")
cand = Image.open("${candFile}").convert("RGB").resize(orig.size, Image.LANCZOS)
W, H = orig.size
cv = Image.new("RGB", (W, H * 2 + 40), (255, 255, 255))
d = ImageDraw.Draw(cv)
cv.paste(orig, (0, 0))
cv.paste(cand, (0, H + 40))
d.rectangle([0, H, W, H + 40], fill=(20, 20, 20))
cv.save("${outPng}")
print("collage", cv.size)
PY`);

const b64 = `data:image/png;base64,${fs.readFileSync(outPng).toString('base64')}`;
const PROMPT = `Deux versions de la même photo, l'une sous l'autre : en HAUT l'ORIGINAL, en BAS un rendu amélioré (agrandissement ×1,9 ré-affiché à l'échelle de l'original). Dans le groupe de six personnes, un homme porte un T-SHIRT GRIS CLAIR avec une INSCRIPTION GRAPHIQUE ROSE/VIOLETTE (partiellement visible, épaule gauche) ; un autre porte un haut moutarde. 1) Localise le t-shirt gris à inscription. 2) Compare l'inscription entre HAUT et BAS : le graphisme/les lettres sont-ils EXACTEMENT les mêmes (aucune lettre inventée, modifiée ou supprimé — garde : jamais inventer de texte) ? 3) Sa lisibilité est-elle acceptable (une très légère douceur d'agrandissement n'est PAS un défaut) ? Réponds UNIQUEMENT par un JSON valide : {"localisation": "...", "inscription_identique": true/false, "nettete_acceptable": true/false, "verdict": "intact|altere", "confiance": "haute|moyenne|basse", "justification": "..."}`;

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
