// Task 48 — PA-TEST-007 : analyse §1 ANALYSE-v2 de « libération après guerre » (photo inédite,
// 1944 présumé). createVision + thinking disabled (remède SSE). Sortie JSON verrouillée B6.
import fs from 'fs';
const SDK = '/home/z/.bun/install/global/node_modules/z-ai-web-dev-sdk/dist/index.js';
const [, , imgFile, outJson] = process.argv;
const b64 = `data:image/png;base64,${fs.readFileSync(imgFile).toString('base64')}`;

const PROMPT = `Voici une photographie historique présumée de 1944 (libération d'une ville française — camion militaire, foule, drapeaux). Analyse-la selon la grille ANALYSE-v2. Note chaque critère de 0 (sain/absent) à 4 (critique) + 1 phrase d'observation, et produis un INVENTAIRE DE RÉFÉRENCE exhaustif.

Axe technique : A1 exposition globale ; A2 écrêtage (ombres bouchées/hautes lumières brûlées) ; A3 bruit OU grain (PRÉCISE : grain argentique authentique vs bruit de numérisation — le grain argentique constitutif n'est PAS un défaut) ; A4 flou (bougé, mise au point) ; A5 artéfacts de compression ; A6 résolution/piqué ; A7 dominante (sépia/verdissage d'un tirage N&B ancien ?) ; A8 dynamique/contraste (plage étroite de tirage ancien ?) ; A9 défauts optiques (vignettage, flare) ; A10 dégâts physiques (rayures, poussières, taches, plis, émulsion).

Axe sémantique : B1 nombre de visages + importance (1er plan/arrière-plan) ; B2 texte/panneaux lisibles (à préserver strictement — drapeaux ? inscriptions ?) ; B3 type de scène ; B4 sources lumineuses ; B5 composition/plan/cadrage ; B6 inventaire de référence COMPLET : pour chaque sujet ou groupe visible (positions, expressions, postures, couvre-chefs, vêtements, objets tenus — fusils, drapeaux [lesquels : tricolore français, américain ?], banderoles) + éléments du décor (camion [marquages ?], bâtiments, chaussée, autres véhicules/passants) — tout ce qui doit rester strictement identique.

Axe contextuel : C1 support probable (tirage argentique scanné ?) ; C2 ère/décennie ; C3 (non demandé — note "défaut").

Réponds UNIQUEMENT par un JSON valide : {"A": {"A1": {"score": n, "obs": "..."}, ..., "A10": {...}}, "B": {"B1": "...", "B2": "...", "B3": "...", "B4": "...", "B5": "...", "B6": "inventaire exhaustif"}, "C": {"C1": "...", "C2": "...", "C3": "défaut"}, "monochrome": true/false, "resume": "2 phrases"}`;

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
console.log(m[0].slice(0, 1500));
console.log('\n[JSON complet écrit :', outJson, ']');
