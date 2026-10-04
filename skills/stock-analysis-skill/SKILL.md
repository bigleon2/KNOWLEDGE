---
name: stock_analysis
version: "1.0.0"
category: "Autres"
tags:
  - stock
  - analysis
  - skill
description: "Skill complet d'analyse boursière couvrant les actions A-share (Chine), Hong Kong et US. Cas d'usage prioritaires : analyse d'actions et recommandations achat/vente/conserver par code ticker, génération de dashboards de décision et de rapports de recherche avec analyses technique/fondamentale/sentiment, stratégies d'investissement tenant compte de la position et du prix de revient de l'utilisateur, scoring et analyse de sécurité des revenus de dividendes, scan des rumeurs et des signaux précoces de marché (M&A, activité des initiés, actions d'analystes), gestion de watchlist avec alertes d'objectif de cours et de stop-loss, et reconnaissance de figures en chandeliers japonais (K-line) à partir d'images. Ce skill doit être le choix principal chaque fois que l'utilisateur mentionne un ticker, demande s'il faut acheter ou vendre une action, évoque son prix de revient ou sa position, demande une analyse de dividendes, s'enquiert de rumeurs de marché ou de signaux précoces, veut ajouter/consulter/gérer une watchlist, ou téléverse une image de graphique pour une analyse technique."
language: fr

read_when:
  - Déclencher quand la demande concerne : "Skill complet d'analyse boursière couvrant les actions A-share (Chine), Hong Kong et US
  - Déclencher si la demande mentionne : analyse, actions, skill
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

# Stock Analysis Skill

## Skills de plateforme requis

- `finance skill` — toutes les données de marché (A-share/HK/US unifiées)
- `pdf skill` — génération de rapports PDF
- `docx skill` — génération de documents Word
- `vlm skill` (intégré) — reconnaissance de figures en chandeliers japonais (K-line)

---

## Commandes & déclencheurs

| Commande | Exemples de déclencheurs |
|------|-----------|
| Analyse d'une action | Analyse 600519 / AAPL vaut-il le coup d'achat / regarde Tencent pour moi |
| Analyse avec position | Mon prix de revient est 1450, analyse Moutai / AAPL acheté à 170, où en est-on |
| Analyse des dividendes | Les dividendes de JNJ ? / Analyse les dividendes de ces actions KO PG JNJ |
| Scan des rumeurs | Quelles rumeurs de M&A aujourd'hui / Scanne les signaux précoces du marché |
| Ajouter à la watchlist | Suivre AAPL / Ajoute 600519 à la watchlist, objectif 1600 stop 1350 |
| Consulter la watchlist | Ma liste de watchlist / Montre les actions que je suis |
| Vérifier les alertes | Vérifie les alertes de la watchlist / Un stop-loss a-t-il été déclenché |
| Retirer de la watchlist | Retire TSLA de la watchlist |
| Analyse de graphique K-line | (image téléversée) Analyse ce graphique en chandeliers |
| Revue du marché | Avec une revue du marché, analyse 600519 |

---

## Schémas d'entrée

### Analyse d'une action
```typescript
{
  stocks: (string | { code: string; position?: { status: "empty"|"holding"; cost?: number; shares?: number } })[],
  outputFormat?: "markdown" | "pdf" | "word",  // défaut : markdown
  mode?: "full" | "quote",                      // défaut : full
  includeMarketReview?: boolean,                // défaut : false
  includeGlobalMacro?: boolean,                 // défaut : true
  includeDividend?: boolean,                    // analyse des dividendes en supplément pour les actions US, défaut : false
}
```

### Analyse des dividendes
```typescript
runDividend(tickers: string | string[])
```

### Scan des rumeurs
```typescript
runRumorScan()  // sans paramètre, scanne automatiquement les signaux du jour
```

### Gestion de la watchlist
```typescript
runWatchlistAdd(ticker, { targetPrice?, stopPrice?, alertOnSignal?, notes? })
runWatchlistRemove(ticker)
runWatchlistList()
runWatchlistCheck()  // vérifie si des alertes de prix/signal se sont déclenchées
```

---

## Structure du rapport

```
# Rapport d'analyse boursière intelligent

## 🌍 Aperçu macro mondial (activé par défaut)
## 🎯 Revue du marché (à activer)
## 📊 Tableau de bord de décision par action (pour chacune)
   ### 📰 Aperçu des informations clés (sentiment/attentes de résultats/🚨risques/✨points favorables/dernières actualités)
   ### 📌 Conclusion centrale (conclusion/en une phrase/conseil hors position/conseil en position + P&L)
   ### 📈 Cours du jour
   ### 📊 Lecture des données (technique/fondamental/flux de capitaux)
   ### 🎯 Plan d'action (tableau des points d'entrée/taille de position/gestion du risque)
   ### ✅ Liste de contrôle (conclusion globale)
   ### 💰 Analyse des dividendes (actions US, à activer via includeDividend)
```

---

## Métriques d'analyse des dividendes

| Métrique | Description |
|------|------|
| Score de sécurité | 0-100, combinant taux de distribution/croissance/années consécutives |
| Note de revenu | excellent/good/moderate/poor |
| Statut du taux de distribution | safe(<40%)/moderate/high/unsustainable |
| CAGR 5 ans | Taux de croissance annuel composé du dividende |
| Années consécutives de croissance | 25 ans et plus = aristocrate du dividende |

---

## Types de signaux du scanneur de rumeurs

| Type | Score d'impact | Description |
|------|--------|------|
| Rumeur de M&A (ma) | +5 | Fusion-acquisition/achat/offre publique |
| Mouvement d'initiés (insider) | +4 | Achats/ventes de CEO/directeurs |
| Ajustement d'analyste (analyst) | +3 | Hausse/baisse de note, changement d'objectif de cours |
| Action réglementaire (regulatory) | +3 | Enquête SEC/risque de conformité |
| Prévision de résultats (earnings) | +2 | Alerte aux profits/révision à la hausse |

---

## Types d'alertes de la watchlist

| Type d'alerte | Condition de déclenchement |
|---------|---------|
| 🎯 Objectif de cours | Prix actuel ≥ targetPrice |
| 🛑 Stop-loss | Prix actuel ≤ stopPrice |
| 📊 Changement de signal | Conclusion actuelle ≠ conclusion précédente |

---

## Règles de comportement

- Biais par rapport à la moyenne > 5 % → la conclusion ne peut pas être Achat/Achat fort
- Donnée manquante → marquer « temporairement indisponible », interdiction absolue d'inventer
- Prix de revient fourni → l'analyse de plus-value/moins-value est obligatoire
- Position non fournie → donner à la fois les recommandations hors position et en position
- Après chaque analyse, mise à jour silencieuse automatique des signaux de la watchlist

---

## Structure des fichiers

```
stock-analysis-skill/
├── SKILL.md
├── package.json
├── tsconfig.json
└── src/
    ├── index.ts          # point d'entrée principal (routage de toutes les commandes)
    ├── types.ts          # définitions de types
    ├── dataFetcher.ts    # couche de données (finance skill)
    ├── analyzer.ts       # analyse d'actions individuelles (LLM/VLM)
    ├── dividend.ts       # analyse des dividendes
    ├── rumorScanner.ts   # scan des rumeurs
    └── watchlist.ts      # gestion de la watchlist (persistance storage)
```

---

## Limites

- Le scan des rumeurs dépend de la qualité des données d'actualité du `finance skill`
- La persistance des données de watchlist dépend de l'API storage de la plateforme
- Les données fondamentales sont moins abondantes pour Hong Kong
- Futures, ETF et obligations convertibles non pris en charge
- À titre informatif uniquement, ne constitue pas un conseil en investissement
