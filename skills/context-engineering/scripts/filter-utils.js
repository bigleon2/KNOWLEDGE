/**
 * filter-utils.js — v2.0.0 (OPTIMISÉ, test en staging avant intégration)
 * Discipline : context-engineering (M2 Contrôle) + harness-engineering (profils, budget).
 *
 * Optimisations v2 (chacune ancre un mécanisme documenté, rien de normatif nouveau) :
 *  O7. Estimation #token CALIBRÉE : ratio lexical (FR accentué ~3.6 c/token vs ASCII ~4),
 *      densité de tokens uniques, coefficient de complexité de la grille (0.8x-1.5x) et
 *      coefficient profil (ECO 0.7x, VIEUX PC 0.5x) — grille-token.md.
 *  O8. Signaux de pression mesurés RÉELLEMENT quand possible (fs.statfsSync pour le disque)
 *      + gestionnaire de budget d'attention 80 %/95 % (gen-plan §2.4).
 *  O9. Filtrage par profil avec COMPACTION au lieu d'exclusion sèche : un item surdimensionné
 *      mais pertinent est synthétisé sous le seuil (M2 « compaction », gen-plan §1.7 #7) ;
 *      l'exclusion reste réservée aux items sans pertinence.
 *  O10. Budget cumulé glouton par densité de pertinence (tokens/point) avec synthèse
 *      d'exclusion tracée, au lieu de l'arrêt sec v1.
 *
 * Contrat : sur-ensemble compatible de l'API v1.
 */

'use strict';

const fs = require('fs');

const CHAR_PER_TOKEN = 4;      // référence v1 (conservée)
const RATIO_FR = 3.6;          // O7 : ratio empirique texte français accentué (c/token)
const DENSITY_REF = 0.55;      // O7 : densité lexicale de référence (uniques/tokens)

// Coefficients de complexité (grille-token.md — plage midpoints intégrés côté harnais)
const COMPLEXITY = { faible: 0.8, standard: 1.0, elevee: 1.3, critique: 1.5 };
const PROFILE_COEF = { NORMAL: 1.0, ECO: 0.7, 'VIEUX PC': 0.5 };

// ---------- Estimation #token ----------
function estimateTokens(text) { // v1 conservée (comparabilité)
  if (!text) return 0;
  return Math.ceil(String(text).length / CHAR_PER_TOKEN);
}

// O7 : estimation calibrée (ratio langage + densité + coefficients grille).
function estimateTokensCalibrated(text, opts = {}) {
  if (!text) return 0;
  const s = String(text);
  const accents = (s.match(/[\u00c0-\u017f]/g) || []).length;
  const accentRatio = s.length ? accents / s.length : 0;      // ~0 ASCII pur, >0.02 FR dense
  const ratio = CHAR_PER_TOKEN + accentRatio * (RATIO_FR - CHAR_PER_TOKEN) * 4; // jusqu'à 3.6
  const tokens = tokenizeLite(s);
  const uniq = new Set(tokens).size;
  const density = tokens.length ? uniq / tokens.length : 0;    // redondance -> moins de tokens réels
  const densityFactor = 0.85 + 0.3 * Math.min(1, density / DENSITY_REF) / 2;
  const base = s.length / ratio / Math.max(0.7, densityFactor);
  const kComp = COMPLEXITY[opts.complexity] !== undefined ? COMPLEXITY[opts.complexity] : 1.0;
  const kProf = PROFILE_COEF[opts.profile] !== undefined ? PROFILE_COEF[opts.profile] : 1.0;
  return Math.ceil(base * (opts.applyCoefficients === false ? 1 : kComp * kProf));
}

function tokenizeLite(s) {
  return String(s).toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .split(/[^a-z0-9]+/).filter((w) => w.length >= 3);
}

// ---------- O8 : signaux de pression mesurés ----------
function realDiskFreeGB(mountPath = '.') {
  try {
    if (typeof fs.statfsSync === 'function') {
      const st = fs.statfsSync(mountPath);
      return (st.bavail * st.bsize) / (1024 * 1024 * 1024);
    }
  } catch (_e) { /* repli silencieux : mesure manuelle uniquement */ }
  return null;
}

// ctx : { diskFreeGB?, timeoutsConsecutifs?, budgetUsedPct?, mountPath? }
function detectPressureSignals(ctx) {
  const c = ctx || {};
  const disk = typeof c.diskFreeGB === 'number' ? c.diskFreeGB : realDiskFreeGB(c.mountPath || '.');
  const signals = [];
  if (typeof disk === 'number') {
    if (disk < 3) signals.push({ type: 'disk', severity: 'critique', value: +disk.toFixed(2), measured: true });
    else if (disk < 5) signals.push({ type: 'disk', severity: 'pression', value: +disk.toFixed(2), measured: true });
  }
  if (typeof c.timeoutsConsecutifs === 'number' && c.timeoutsConsecutifs >= 2) {
    signals.push({ type: 'timeout', severity: c.timeoutsConsecutifs >= 4 ? 'critique' : 'pression', value: c.timeoutsConsecutifs });
  }
  if (typeof c.budgetUsedPct === 'number' && c.budgetUsedPct > 80) {
    signals.push({ type: 'budget', severity: c.budgetUsedPct > 95 ? 'critique' : 'pression', value: c.budgetUsedPct });
  }
  return signals;
}

// O8 : gestionnaire de budget d'attention (alimente les signaux §2.4).
class AttentionBudgetManager {
  constructor(budgetTokens) { this.budget = budgetTokens; this.used = 0; this.events = []; }
  consume(tokens, label = '') {
    this.used += tokens;
    const pct = 100 * this.used / this.budget;
    if (pct > 95) this.events.push({ level: 'critique', pct: +pct.toFixed(1), label });
    else if (pct > 80) this.events.push({ level: 'pression', pct: +pct.toFixed(1), label });
    return pct;
  }
  signals() {
    return this.events.length
      ? [{ type: 'budget', severity: this.events.some((e) => e.level === 'critique') ? 'critique' : 'pression', value: this.events[this.events.length - 1].pct }]
      : [];
  }
}

// ---------- Profil (inchangé v1 : seuils documentés) ----------
function resolveProfile(signals) {
  const s = signals || [];
  const hasCritique = s.some((x) => x.severity === 'critique');
  if (hasCritique || s.length >= 2) return 'VIEUX PC';
  if (s.length === 1) return 'ECO';
  return 'NORMAL';
}

const RANK = { 'VIEUX PC': 0, ECO: 1, NORMAL: 2 };
function downgradeProfile(current, target) {
  const cur = RANK[current] !== undefined ? current : 'NORMAL';
  const tgt = RANK[target] !== undefined ? target : 'NORMAL';
  return RANK[tgt] < RANK[cur] ? tgt : cur;
}

// ---------- O9 : filtrage profil avec compaction ----------
// item : { content, tokens?, relevance? } — options : { synthesizer? }
function filterByProfile(items, profile, opts = {}) {
  const list = Array.isArray(items) ? items.slice() : [];
  if (profile === 'NORMAL') return { retained: list, excluded: [], compacted: [] };
  const seuil = profile === 'VIEUX PC' ? 5000 : 8000;
  const retained = [], excluded = [], compacted = [];
  for (const it of list) {
    const tokens = typeof it.tokens === 'number' ? it.tokens : estimateTokens(it.content || '');
    if (tokens <= seuil) { retained.push(it); continue; }
    const relevance = typeof it.relevance === 'number' ? it.relevance : 1; // sans scoring : pertinent par défaut
    if (relevance > 0 && typeof opts.synthesizer === 'function') {
      const compact = opts.synthesizer(it, seuil); // synthèse sous seuil, provenance conservée
      if (compact && compact.tokens <= seuil) { compacted.push({ from: tokens, to: compact.tokens }); retained.push(compact); continue; }
    }
    excluded.push(it); // O9 : exclusion réservée aux items non compactables / sans pertinence
  }
  return { retained, excluded, compacted };
}

// ---------- O10 : budget cumulé glouton par densité de pertinence ----------
function filterByTokenBudget(steps, budgetTokens) {
  const arr = (steps || []).map((st, i) => ({
    ...st, _i: i,
    tokens: typeof st.tokens === 'number' ? st.tokens : estimateTokens(st.content || ''),
    relevance: typeof st.relevance === 'number' ? st.relevance : 1,
  }));
  const kept = [];
  let used = 0;
  const restants = arr.slice();
  while (restants.length) {
    // choix glouton : meilleure densité pertinence/tokens parmi ce qui rentre encore
    let bestIdx = -1, bestDensity = -1;
    for (let i = 0; i < restants.length; i++) {
      const t = Math.max(1, restants[i].tokens);
      if (used + t <= budgetTokens) {
        const d = restants[i].relevance / t;
        if (d > bestDensity) { bestDensity = d; bestIdx = i; }
      }
    }
    if (bestIdx < 0) break;
    const chosen = restants.splice(bestIdx, 1)[0];
    used += chosen.tokens;
    kept.push(chosen);
  }
  // synthèse d'exclusion tracée pour tout ce qui n'entre pas
  const dropped = restants.map((d) => ({
    ...d, content: `(exclusion budgétaire — synthèse : ${(String(d.content || '').split('\n').find((l) => l && l.trim()) || '').slice(0, 140)} …)`,
  }));
  return { kept, used, dropped: dropped.length + (arr.length - kept.length - dropped.length ? 0 : 0), exclusions: dropped };
}

module.exports = {
  CHAR_PER_TOKEN, RATIO_FR, COMPLEXITY, PROFILE_COEF,
  estimateTokens, estimateTokensCalibrated, tokenizeLite,
  realDiskFreeGB, detectPressureSignals, AttentionBudgetManager,
  resolveProfile, downgradeProfile, filterByProfile, filterByTokenBudget,
};
