/**
 * context-utils.js — v2.0.0 (OPTIMISÉ, test en staging avant intégration)
 * Discipline : context-engineering — modes M1 (Composition), M2 (Contrôle), M3 (Restitution).
 *
 * Optimisations v2 (chaque point ancre un mécanisme documenté, rien de normatif nouveau) :
 *  O1. Scoring de pertinence TF-IDF léger (FR/EN, stopwords) — priorité au « signal fort »
 *      (context-engineering §1.2 M2 : « priorité au signal fort »).
 *  O2. Extraction d'ancres (versions semver, sections §, décisions D0NN/D-rNN, #token,
 *      chemins kebab) — provenance enrichie (context-engineering §1.4).
 *  O3. Déduplication par empreinte (SHARED §6.3 / R4 : ne jamais dupliquer).
 *  O4. Lecture blocs ADAPTATIFS : taille 200-800 L selon densité de pertinence, blocs
 *      sans pertinence sautés avec provenance « skipped » (M2 : budget d'attention,
 *      compaction par synthèses — gen-plan §1.7 #7 conservé pour les blocs lus).
 *  O5. Assemblage RANKÉ : socle SHARED épinglé en tête (règle documentée), puis
 *      pertinence × poids de type au lieu de l'ordre fixe aveugle.
 *  O6. Cache LRU du sous-graphe KB (graph-engineering M1 : traversal réutilisable).
 *
 * Contrat : sur-ensemble compatible de l'API v1 (mêmes noms, mêmes formes de retour).
 */

'use strict';

const fs = require('fs');
const path = require('path');

// ---------- Constantes (documentées + plages d'optimisation) ----------
const BLOCK_LINES = 500;          // seuil documenté (gen-plan §1.7 #7)
const BLOCK_MIN = 200;            // O4 : borne basse bloc adaptatif
const BLOCK_MAX = 800;            // O4 : borne haute bloc adaptatif
const CHAR_PER_TOKEN = 4;         // référence v1 (conservée pour comparabilité)
const RELEV_SKIP = 0.02;          // O4 : sous ce score, bloc sauté (provenance 'skipped')
const RELEV_BIG = 0.30;           // O4 : au-dessus, bloc étendu (800 L)
const CACHE_MAX = 128;            // O6 : capacité cache LRU

// ---------- O1 : tokenizer + stopwords (FR/EN) ----------
const STOPWORDS = new Set(('le la les un une des de du au aux et ou mais donc or ni car que qui quoi ' +
  'dont où à a en dans sur pour par avec sans sous vers chez ce cet cette ces mon ma mes ton ta tes ' +
  'son sa ses notre nos votre vos leur leurs est sont être avoir ont eu fait faire plus moins tout ' +
  'toute tous toutes autre autres même déjà puis alors ainsi comme tant très peu lors afin selon ' +
  'the of and or to in on for with without from by is are be been this that these those it its as ' +
  'at an each which who what into over under between across per via use used using').split(' '));

function tokenize(text) {
  return String(text || '')
    .toLowerCase()
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '') // accents -> ascii
    .split(/[^a-z0-9]+/)
    .filter((w) => w.length >= 3 && !STOPWORDS.has(w));
}

function termFreq(tokens) {
  const tf = new Map();
  for (const t of tokens) tf.set(t, (tf.get(t) || 0) + 1);
  return tf;
}

// IDF calculé sur l'ensemble des blocs du corpus courant (léger, sans dépendance).
function buildIdf(docsTokens) {
  const df = new Map();
  for (const toks of docsTokens) {
    for (const t of new Set(toks)) df.set(t, (df.get(t) || 0) + 1);
  }
  const N = Math.max(1, docsTokens.length);
  const idf = new Map();
  for (const [t, d] of df) idf.set(t, Math.log(1 + N / d));
  return idf;
}

// Score de pertinence : somme IDF des termes partagés, normalisée par racine carrée
// de la longueur du bloc (évite le biais volumétrie). ∈ [0, ~10].
function relevanceScore(queryTokens, blockTokens, idf) {
  if (!queryTokens.length || !blockTokens.length) return 0;
  const bt = termFreq(blockTokens);
  let s = 0;
  for (const q of new Set(queryTokens)) {
    if (bt.has(q)) s += (idf.get(q) || Math.log(2)) * Math.min(bt.get(q), 3);
  }
  return s / Math.sqrt(blockTokens.length);
}

// ---------- O2 : extraction d'ancres ----------
function extractAnchors(text) {
  const t = String(text || '');
  const uniq = (arr) => [...new Set(arr)];
  return {
    versions: uniq((t.match(/\bv?\d+\.\d+\.\d+\b/g) || []).map((s) => (s.startsWith('v') ? s : `v${s}`))).slice(0, 8),
    sections: uniq(t.match(/§\s?[0-9]+(?:\.[0-9]+)*/g) || []).slice(0, 12),
    decisions: uniq(t.match(/\bD0\d{1,3}\b|\bD-r\d+-\d+\b/g) || []).slice(0, 10),
    tokenTags: uniq(t.match(/#token[a-z0-9:-]*/g) || []).slice(0, 6),
    // Chemins réels : enracinés (skills/, download/, tmp/, scripts/, …) ou fichiers à extension connue.
    paths: uniq([
      ...(t.match(/\b(?:skills|download|tmp|scripts|upload|docs|data|references)\/[a-zA-Z0-9.@_/-]+/g) || []),
      ...(t.match(/\b[a-zA-Z0-9][a-zA-Z0-9.@_-]*\.(?:md|js|py|json|zip|yaml|yml|txt)\b/g) || []),
    ]).slice(0, 20),
  };
}
function anchorCount(anchors) {
  if (!anchors) return 0;
  return anchors.versions.length + anchors.sections.length + anchors.decisions.length +
    anchors.tokenTags.length + anchors.paths.length;
}

// ---------- O3 : empreinte + déduplication ----------
function fnv1a(str) {
  let h = 0x811c9dc5;
  for (let i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i);
    h = (h * 0x01000193) >>> 0;
  }
  return ('00000000' + h.toString(16)).slice(-8);
}
function dedupeBlocks(blocks) {
  const seen = new Map(); // empreinte -> premier bloc
  const kept = [];
  let duplicates = 0;
  for (const b of blocks) {
    const sig = fnv1a(String(b.content || '').replace(/\s+/g, ' ').trim().slice(0, 4000));
    if (seen.has(sig)) { duplicates++; b.duplicateOf = seen.get(sig); continue; }
    seen.set(sig, b.provenance ? b.provenance.lines : kept.length);
    kept.push(b);
  }
  return { kept, duplicates };
}

// ---------- Estimation #token (v1 conservée ; v2 calibrée côté filter-utils) ----------
function estimateTokens(text) {
  if (!text) return 0;
  return Math.ceil(String(text).length / CHAR_PER_TOKEN);
}

// ---------- O4 : lecture bloc par bloc ADAPTATIVE ----------
function splitBlockwise(content, blockSize) {
  const size = blockSize || BLOCK_LINES;
  const lines = String(content).split('\n');
  const blocks = [];
  for (let i = 0; i < lines.length; i += size) {
    blocks.push({ start: i + 1, end: Math.min(i + size, lines.length), lines: lines.slice(i, i + size) });
  }
  return blocks;
}

function synthesizeBlock(block, provenanceFile) {
  const first = block.lines.find((l) => l.trim().length > 0) || '(bloc vide)';
  return {
    synthese: `${first.trim().slice(0, 120)} … [${block.end - block.start + 1} lignes]`,
    provenance: { file: provenanceFile, section: 'bloc', lines: `${block.start}-${block.end}` },
  };
}

function readBlockwise(filePath) { // compat v1 : lecture intégrale par blocs fixes
  const abs = path.resolve(filePath);
  const content = fs.readFileSync(abs, 'utf8');
  const totalLines = content.split('\n').length;
  const blocks = splitBlockwise(content);
  return {
    file: abs, totalLines, readFully: true, blocksRead: blocks.length,
    synthese: totalLines > BLOCK_LINES ? blocks.map((b) => synthesizeBlock(b, abs)) : null,
    content, blocks,
  };
}

// Lecture adaptative : blocs pondérés par pertinence, saut des blocs hors signal.
function readBlockwiseAdaptive(filePath, { queryTokens, idf, budgetTokens }) {
  const abs = path.resolve(filePath);
  const content = fs.readFileSync(abs, 'utf8');
  const lines = content.split('\n');
  const totalLines = lines.length;
  const out = [];
  let blocksRead = 0, blocksSkipped = 0, charsRead = 0;
  let i = 0;
  let size = Math.min(BLOCK_LINES, Math.max(BLOCK_MIN, Math.floor(budgetTokens * CHAR_PER_TOKEN / 200) || BLOCK_LINES));
  while (i < totalLines) {
    const end = Math.min(i + size, totalLines);
    const chunk = lines.slice(i, end).join('\n');
    const toks = tokenize(chunk);
    const score = relevanceScore(queryTokens, toks, idf);
    if (score < RELEV_SKIP && i > 0) {
      // O4 : saut tracé (provenance 'skipped') — le premier bloc est toujours lu (règle socle/tête).
      blocksSkipped++;
      out.push({
        content: `(bloc sauté — pertinence ${score.toFixed(3)} < ${RELEV_SKIP})`,
        tokens: 0, skipped: true,
        anchors: extractAnchors(lines.slice(i, end).filter((l) => /^\s*(#{1,3} |<!-- )/.test(l)).join('\n')),
        provenance: { file: abs, section: 'skipped', lines: `${i + 1}-${end}` },
      });
    } else {
      blocksRead++; charsRead += chunk.length;
      out.push({
        content: chunk, tokens: estimateTokens(chunk), skipped: false,
        anchors: extractAnchors(chunk),
        provenance: { file: abs, section: 'bloc-adaptatif', lines: `${i + 1}-${end}` },
      });
    }
    // O4 : adaptation de la taille du PROCHAIN bloc selon la densité observée
    size = score >= RELEV_BIG ? BLOCK_MAX : score >= RELEV_SKIP ? BLOCK_LINES : BLOCK_MIN;
    i = end;
  }
  return { file: abs, totalLines, blocks: out, blocksRead, blocksSkipped, charsRead };
}

// ---------- Registre KB + O6 : cache LRU du sous-graphe ----------
function parseKB(content) {
  const entries = [];
  for (const line of String(content).split('\n')) {
    const m = line.match(/^\|\s*`([a-z0-9-]+)`\s*\|\s*([0-9]+\.[0-9]+\.[0-9]+)\s*\|/);
    if (m) {
      const cells = line.split('|').map((c) => c.trim()).filter(Boolean);
      entries.push({ name: m[1], version: m[2], raw: cells });
    }
  }
  return entries;
}

class KbCache { // O6 : LRU simple sur Map
  constructor(max = CACHE_MAX) { this.max = max; this.map = new Map(); }
  get(k) {
    if (!this.map.has(k)) return undefined;
    const v = this.map.get(k);
    this.map.delete(k); this.map.set(k, v); // rafraîchit la récence
    return v;
  }
  set(k, v) {
    if (this.map.has(k)) this.map.delete(k);
    this.map.set(k, v);
    if (this.map.size > this.max) this.map.delete(this.map.keys().next().value);
  }
  get size() { return this.map.size; }
}
const kbCache = new KbCache();

function discoverCandidates(kbEntries, demande) {
  const key = `cands:${fnv1a(String(demande || ''))}:${kbEntries.length}`;
  const hit = kbCache.get(key);
  if (hit) return hit;
  const qTokens = tokenize(demande);
  const cands = [];
  for (const e of kbEntries) {
    const hay = [e.name, ...(e.raw || [])].join(' ');
    const toks = tokenize(hay);
    const score = relevanceScore(qTokens, toks, buildIdf([toks, qTokens]));
    if (score > 0) cands.push({ name: e.name, version: e.version, score: +score.toFixed(3), hits: toks.filter((t) => qTokens.includes(t)).length });
  }
  cands.sort((a, b) => b.score - a.score);
  kbCache.set(key, cands);
  return cands;
}

// ---------- O5 : assemblage RANKÉ (socle épinglé, puis pertinence × poids) ----------
const TYPE_WEIGHT = { socle: 1.0, kb: 0.9, skill: 0.8, reference: 0.7, corpus: 0.6, demande: 0.5, plan: 0.4 };

function assembleContext({ demande, sources, budgetTokens }) {
  const queryTokens = tokenize(demande);
  const warned = { w80: false, w95: false };
  const usedType = new Set();

  // 1) Matérialisation des blocs candidats
  const raw = [];
  for (const src of sources || []) {
    if (src.content !== undefined && src.content !== null) {
      raw.push({
        type: src.type, content: String(src.content), tokens: estimateTokens(src.content),
        anchors: extractAnchors(src.content), skipped: false,
        provenance: { file: src.file || '(mémoire)', section: 'fourni', lines: '1-?' },
      });
    } else if (src.file) {
      const adaptive = readBlockwiseAdaptive(src.file, { queryTokens, idf: buildIdf([queryTokens]), budgetTokens });
      for (const b of adaptive.blocks) raw.push({ type: src.type, ...b, provenance: { ...b.provenance, file: b.provenance.file } });
    }
  }

  // 2) Déduplication (O3)
  const { kept, duplicates } = dedupeBlocks(raw);

  // 3) IDF global puis ranking (socle épinglé en tête — règle documentée)
  const idf = buildIdf(kept.filter((b) => !b.skipped).map((b) => tokenize(b.content)));
  const ranked = kept
    .filter((b) => b.type !== 'socle')
    .map((b) => ({
      ...b,
      relevance: b.skipped ? 0 : relevanceScore(queryTokens, tokenize(b.content), idf),
    }))
    .sort((a, b) => (b.relevance * (TYPE_WEIGHT[b.type] || 0.5)) - (a.relevance * (TYPE_WEIGHT[a.type] || 0.5)));
  const socle = kept.filter((b) => b.type === 'socle');

  // 4) Inclusion dans le budget (graceful degradation : synthèse d'exclusion 1 ligne)
  const items = [];
  let used = 0;
  const excluded = [];
  for (const b of [...socle, ...ranked]) {
    if (b.skipped) { excluded.push(b); continue; }
    if (used + b.tokens <= budgetTokens) {
      items.push(b); used += b.tokens; usedType.add(b.type);
    } else {
      const firstLine = (b.content.split('\n').find((l) => l.trim()) || '').slice(0, 140);
      excluded.push({
        ...b, excludedBudget: true, content: `(exclusion budgétaire — synthèse : ${firstLine} …)`,
        tokens: estimateTokens(`(exclusion budgétaire — synthèse : ${firstLine} …)`),
      });
    }
  }
  for (const ex of excluded) { items.push(ex); used += ex.tokens || 0; } // tracés, hors budget utile

  // 5) Métriques mécaniques
  const relevant = items.filter((b) => !b.skipped);
  const included = relevant.filter((b) => !b.excludedBudget);
  const tracedSyntheses = relevant.filter((b) => b.excludedBudget);
  const withAnchors = included.filter((b) => anchorCount(b.anchors) > 0);
  const actualTokens = included.reduce((s, b) => s + b.tokens, 0); // contenu réellement inclus (hors synthèses tracées)
  const estimatedTokens = included.reduce((s, b) => s + (b.tokens || 0), 0);
  if (used / budgetTokens > 0.95) warned.w95 = true; else if (used / budgetTokens > 0.80) warned.w80 = true;

  return {
    items,
    metrics: {
      estimatedTokens, actualTokens, blocksRead: included.length,
      blocksSkipped: excluded.filter((b) => b.skipped).length,
      truncated: actualTokens > budgetTokens, budgetUsedPct: +(100 * actualTokens / budgetTokens).toFixed(1),
      warn80: warned.w80, warn95: warned.w95,
      sourcesRetained: included.length, provenanceRate: 1,
      dedupRatio: raw.length ? +(duplicates / raw.length).toFixed(3) : 0,
      duplicatesRemoved: duplicates,
      tracedSyntheses: tracedSyntheses.length,
      anchorRate: included.length ? +(withAnchors.length / included.length).toFixed(3) : 0,
      kbCandidates: 0, // rempli par le harnais après discoverCandidates
      cacheSize: kbCache.size,
    },
  };
}

module.exports = {
  BLOCK_LINES, BLOCK_MIN, BLOCK_MAX,
  tokenize, termFreq, buildIdf, relevanceScore, extractAnchors, anchorCount, fnv1a, dedupeBlocks,
  estimateTokens, splitBlockwise, synthesizeBlock, readBlockwise, readBlockwiseAdaptive,
  parseKB, discoverCandidates, KbCache, assembleContext,
};
