---
name: stock_analysis
description: "Skill complet d'analyse boursière couvrant les actions A (Chine), Hong Kong et les États-Unis. Cas d'usage prioritaires : analyse d'une action et recommandation acheter/vendre/conserver par code ticker, génération de tableaux de bord de décision et de rapports de recherche avec analyse technique/fondamentale/sentiment, stratégies d'investissement tenant compte de la position selon le prix de revient de l'utilisateur, notation et analyse de sécurité du revenu dividendaire, balayage des rumeurs et signaux précoces de marché (M&A, mouvements d'initiés, actions d'analystes), gestion de la liste de suivi avec prix cible et alertes de stop-loss, et reconnaissance de figures en chandeliers japonais à partir d'images. Ce skill doit être le premier choix dès que l'utilisateur mentionne un ticker, demande s'il faut acheter ou vendre une action, fait référence à son prix de revient ou à sa position, demande une analyse de dividendes, s'interroge sur des rumeurs de marché ou des signaux précoces, veut ajouter/consulter/gérer une liste de suivi, ou télécharge l'image d'un graphique pour analyse technique."
---

## §0 — Contexte Système (SHARED v1.7.13)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# Stock Analysis Skill

## Dépendances envers les skills de la plateforme

- `finance skill` — toutes les données de marché (A/HK/US unifiées)
- `pdf skill` — génération de rapports PDF
- `docx skill` — génération de documents Word
- `vlm skill` (intégré) — reconnaissance de figures sur chandeliers japonais

---

## Commands & Triggers

| Commande | Exemples de déclencheurs |
|------|-----------|
| Analyse d'un titre | analyse 600519 / AAPL vaut-il l'achat / jette un œil à Tencent (腾讯) |
| Analyse avec position | ma position a un prix de revient de 1450, analyse Moutai (茅台) / j'ai acheté AAPL à 170, où j'en suis |
| Analyse de dividendes | que valent les dividendes de JNJ / analyse les dividendes de KO PG JNJ |
| Balayage des rumeurs | quelles rumeurs de M&A aujourd'hui / balaie les signaux précoces du marché |
| Ajout à la liste de suivi | surveille AAPL / ajoute 600519 à ma liste, cible 1600, stop 1350 |
| Consultation de la liste | ma liste de suivi / montre les titres que je surveille |
| Vérification des alertes | vérifie les alertes de ma liste / un stop-loss a-t-il été déclenché |
| Retrait de la liste | retire TSLA de ma liste de suivi |
| Analyse de graphique | (image téléversée) analyse ce graphique en chandeliers |
| Revue de marché | ajoute une revue de marché à l'analyse de 600519 |

---

## Input Schemas

### Analyse d'un titre
```typescript
{
  stocks: (string | { code: string; position?: { status: "empty"|"holding"; cost?: number; shares?: number } })[],
  outputFormat?: "markdown" | "pdf" | "word",  // markdown par défaut
  mode?: "full" | "quote",                      // full par défaut
  includeMarketReview?: boolean,                // false par défaut
  includeGlobalMacro?: boolean,                 // true par défaut
  includeDividend?: boolean,                    // analyse de dividendes (US) en complément, false par défaut
}
```

### Analyse de dividendes
```typescript
runDividend(tickers: string | string[])
```

### Balayage des rumeurs
```typescript
runRumorScan()  // sans paramètre, balaie automatiquement les signaux du jour
```

### Gestion de la liste de suivi
```typescript
runWatchlistAdd(ticker, { targetPrice?, stopPrice?, alertOnSignal?, notes? })
runWatchlistRemove(ticker)
runWatchlistList()
runWatchlistCheck()  // vérifie si une alerte de prix/signal est déclenchée
```

---

## Report Structure

```
# Rapport d'analyse intelligente d'actions

## 🌍 Aperçu macro mondial (activé par défaut)
## 🎯 Revue de marché (sur activation)
## 📊 Tableau de bord de décision par titre (pour chaque titre)
   ### 📰 Revue d'informations clés (sentiment/prévisions de résultats/🚨risques/✨favorables/dernières actualités)
   ### 📌 Conclusion centrale (verdict/résumé en une phrase/conseil sans position/conseil avec position + P&L)
   ### 📈 Cotation du jour
   ### 📊 Vue traversante des données (technique/fondamentale/flux)
   ### 🎯 Plan d'action (table des niveaux d'intervention/pilotage/contrôle du risque)
   ### ✅ Liste de contrôle (conclusion synthétique)
   ### 💰 Analyse de dividendes (US, sur activation de includeDividend)
```

---

## Dividend Analysis Metrics

| Indicateur | Description |
|------|------|
| Score de sécurité | 0-100, synthèse taux de distribution/croissance/années consécutives |
| Notation de revenu | excellent/bon/modeste/faible |
| Statut du taux de distribution | safe(<40%)/moderate/high/unsustainable |
| CAGR 5 ans | taux de croissance composé du dividende |
| Années de croissance consécutives | 25 ans et plus = aristocrate du dividende |

---

## Rumor Scanner Signal Types

| Type | Score d'impact | Description |
|------|--------|------|
| Rumeur de M&A (ma) | +5 | fusion-acquisition/offre publique |
| Mouvements d'initiés (insider) | +4 | achats/ventes du CEO ou du conseil |
| Révisions d'analystes (analyst) | +3 | surclassement/déclassement/objectif modifié |
| Actualité réglementaire (regulatory) | +3 | enquête SEC/risque de conformité |
| Prévisions de résultats (earnings) | +2 | alerte sur résultats/relevé |

---

## Watchlist Alert Types

| Type d'alerte | Condition de déclenchement |
|---------|---------|
| 🎯 Prix cible | prix courant ≥ targetPrice |
| 🛑 Prix de stop | prix courant ≤ stopPrice |
| 📊 Changement de signal | conclusion du jour ≠ conclusion précédente |

---

## Behavior Rules

- Écart de divergence > 5 % → la conclusion ne peut pas être acheter/achat renforcé
- Donnée manquante → marquer « indisponible », interdiction absolue d'inventer
- Prix de revient fourni → fournir obligatoirement l'analyse de P&L
- Position non renseignée → donner les deux conseils, sans position et avec position
- Après chaque analyse, mise à jour silencieuse automatique des signaux de la liste de suivi

---

## File Structure

```
stock-analysis-skill/
├── SKILL.md
├── package.json
├── tsconfig.json
└── src/
    ├── index.ts          # point d'entrée (routage de toutes les commandes)
    ├── types.ts          # définitions de types
    ├── dataFetcher.ts    # couche données (finance skill)
    ├── analyzer.ts       # analyse par titre (LLM/VLM)
    ├── dividend.ts       # analyse de dividendes
    ├── rumorScanner.ts   # balayage des rumeurs
    └── watchlist.ts      # gestion de la liste de suivi (persistance storage)
```

---

## Limitations

- Le balayage des rumeurs dépend de la qualité des données d'actualités du finance skill
- La persistance de la liste de suivi dépend de l'API storage de la plateforme
- Données fondamentales plus rares sur les valeurs de Hong Kong
- Futures, ETF et obligations convertibles non couverts
- A titre indicatif uniquement, ne constitue pas un conseil en investissement
