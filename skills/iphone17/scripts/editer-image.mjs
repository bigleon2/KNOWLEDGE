// Contournement SDK base64 — le CLI `z-ai image-edit` ne transmet pas les images
// locales (erreur 1210, constat Task 42, session web-38713acd). Voie SDK directe.
// Usage : bun <ce-script>.mjs <prompt_file> <image_file> <output_file> [size] [retries]
import fs from 'fs';

const SDK = '/home/z/.bun/install/global/node_modules/z-ai-web-dev-sdk/dist/index.js';
const [,, promptFile, imageFile, outputFile, sizeArg, retriesArg] = process.argv;
if (!promptFile || !imageFile || !outputFile) {
  console.error('Usage: bun editer-image.mjs <prompt_file> <image_file> <output_file> [size] [retries]');
  process.exit(2);
}
const size = sizeArg || '1152x864';
const RETRIES = parseInt(retriesArg || '3', 10);
const prompt = fs.readFileSync(promptFile, 'utf-8').trim();
const b64 = fs.readFileSync(imageFile).toString('base64');
const mime = imageFile.toLowerCase().endsWith('.png') ? 'image/png' : 'image/jpeg';
const dataUrl = `data:${mime};base64,${b64}`;

const { default: ZAI } = await import(SDK);
const zai = await ZAI.create();

for (let attempt = 1; attempt <= RETRIES; attempt++) {
  try {
    const response = await zai.images.generations.edit({
      prompt,
      images: [{ url: dataUrl }],
      size,
    });
    if (!response?.data?.[0]?.base64) throw new Error('reponse invalide (pas de base64)');
    const out = Buffer.from(response.data[0].base64, 'base64');
    fs.writeFileSync(outputFile, out);
    console.log(`OK (tentative ${attempt}) -> ${outputFile} : ${out.length} octets (size=${size})`);
    process.exit(0);
  } catch (e) {
    console.error(`Tentative ${attempt} echouee: ${e.message}`);
    if (attempt < RETRIES) await new Promise(r => setTimeout(r, 2000 * attempt));
  }
}
process.exit(1);
