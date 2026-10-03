---
name: seo-content-writer
version: "2.0.1"
category: "Contenu & Marketing"
tags:
  - seo
  - content
  - writer
description: 'À utiliser quand l''utilisateur demande de "write SEO content", "create a blog post", "write an article", "content writing", "draft optimized content", "write me an article", "create a blog post about", "help me write SEO content" ou "draft content for". Crée un contenu de haute qualité optimisé SEO qui se classe bien dans les moteurs de recherche. Applique les bonnes pratiques SEO on-page, l''optimisation par mots-clés et une structure de contenu pensée pour une visibilité et un engagement maximaux. Pour l''optimisation des citations par les IA, voir geo-content-optimizer. Pour mettre à jour un contenu existant, voir content-refresher.'
license: Apache-2.0
language: fr
metadata:
  author: aaron-he-zhu
  version: "2.0.1"
  geo-relevance: "medium"
  tags:
    - seo
    - content writing
    - blog post
    - article
    - copywriting
    - content creation
    - on-page seo
  triggers:
    - "write SEO content"
    - "create blog post"
    - "write an article"
    - "content writing"
    - "draft optimized content"
    - "write for SEO"
    - "blog writing"
    - "write me an article"
    - "create a blog post about"
    - "help me write SEO content"
    - "draft content for"

---

# SEO Content Writer


> **[SEO & GEO Skills Library](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills)** · 20 skills pour SEO + GEO · Tout installer : `npx skills add aaron-he-zhu/seo-geo-claude-skills`

<details>
<summary>Browse all 20 skills</summary>

**Research** · [keyword-research](../../research/keyword-research/) · [competitor-analysis](../../research/competitor-analysis/) · [serp-analysis](../../research/serp-analysis/) · [content-gap-analysis](../../research/content-gap-analysis/)

**Build** · **seo-content-writer** · [geo-content-optimizer](../geo-content-optimizer/) · [meta-tags-optimizer](../meta-tags-optimizer/) · [schema-markup-generator](../schema-markup-generator/)

**Optimize** · [on-page-seo-auditor](../../optimize/on-page-seo-auditor/) · [technical-seo-checker](../../optimize/technical-seo-checker/) · [internal-linking-optimizer](../../optimize/internal-linking-optimizer/) · [content-refresher](../../optimize/content-refresher/)

**Monitor** · [rank-tracker](../../monitor/rank-tracker/) · [backlink-analyzer](../../monitor/backlink-analyzer/) · [performance-reporter](../../monitor/performance-reporter/) · [alert-manager](../../monitor/alert-manager/)

**Cross-cutting** · [content-quality-auditor](../../cross-cutting/content-quality-auditor/) · [domain-authority-auditor](../../cross-cutting/domain-authority-auditor/) · [entity-optimizer](../../cross-cutting/entity-optimizer/) · [memory-management](../../cross-cutting/memory-management/)

</details>

Ce skill crée du contenu optimisé pour les moteurs de recherche qui se classe bien tout en apportant une vraie valeur aux lecteurs. Il applique des techniques éprouvées de rédaction SEO, une intégration correcte des mots-clés et une structure de contenu optimale.

## Quand utiliser ce skill

- Rédiger des articles de blog ciblant des mots-clés précis
- Créer des landing pages optimisées pour la recherche
- Développer du contenu pilier pour des clusters de sujets
- Rédiger des descriptions produits pour l'e-commerce
- Créer des pages de services pour le SEO local
- Produire des guides pratiques et des tutoriels
- Rédiger des articles comparatifs et des critiques

## Ce que fait ce skill

1. **Intégration des mots-clés** : incorpore naturellement les mots-clés cibles et associés
2. **Optimisation de la structure** : crée un contenu balayable et bien organisé
3. **Création du titre et de la méta** : écrit des titres accrocheurs qui donnent envie de cliquer
4. **Optimisation des en-têtes** : utilise une hiérarchie H1-H6 stratégique
5. **Maillage interne** : suggère les opportunités de liens internes pertinentes
6. **Amélioration de la lisibilité** : garantit un contenu accessible et engageant
7. **Optimisation pour les extraits optimisés** : met en forme pour les opportunités de fonctionnalités SERP

## Comment l'utiliser

### Création de contenu basique

```
Write an SEO-optimized article about [topic] targeting the keyword [keyword]
```

```
Create a blog post for [topic] with these keywords: [keyword list]
```

### Avec des exigences spécifiques

```
Write a 2,000-word guide about [topic] targeting [keyword],
include FAQ section for featured snippets
```

### Briefs de contenu

```
Here's my content brief: [brief]. Write SEO-optimized content following this outline.
```

## Sources de données

> Voir [CONNECTORS.md](../../CONNECTORS.md) pour les placeholders de catégories d'outils.

**Avec outil ~~SEO + ~~search console connectés :**
Récupérez automatiquement les métriques de mots-clés (volume de recherche, difficulté, CPC), l'analyse du contenu des concurrents (pages les mieux classées, longueur des contenus, sujets communs), les fonctionnalités SERP (extraits optimisés, questions PAA) et les opportunités de mots-clés (mots-clés associés, requêtes sous forme de questions).

**Avec données manuelles uniquement :**
Demandez à l'utilisateur de fournir :
1. Le mot-clé principal cible et 3 à 5 mots-clés secondaires
2. L'audience cible et l'intention de recherche (informationnelle/commerciale/transactionnelle)
3. Le nombre de mots cible et le ton souhaité
4. D'éventuelles URLs de concurrents ou exemples de contenu à référencer

Poursuivez avec le workflow complet en utilisant les données fournies. Indiquez dans la sortie quelles métriques proviennent de la collecte automatisée et lesquelles sont fournies par l'utilisateur.

## Instructions

Quand un utilisateur demande du contenu SEO :

1. **Collecter les exigences**

   Confirmez ou demandez :
   
   ```markdown
   ### Content Requirements
   
   **Primary Keyword**: [main keyword]
   **Secondary Keywords**: [2-5 related keywords]
   **Target Word Count**: [length]
   **Content Type**: [blog/guide/landing page/etc.]
   **Target Audience**: [who is this for]
   **Search Intent**: [informational/commercial/transactional]
   **Tone**: [professional/casual/technical/friendly]
   **CTA Goal**: [what action should readers take]
   **Competitor URLs**: [top ranking content to beat]
   ```

2. **Charger les contraintes de qualité CORE-EEAT**

   Avant de rédiger, chargez les standards de qualité de contenu depuis le [CORE-EEAT Benchmark](../../references/core-eeat-benchmark.md) :

   ```markdown
   ### CORE-EEAT Pre-Write Checklist

   **Content Type**: [identified from requirements above]
   **Loaded Constraints** (high-weight items for this content type):

   Apply these standards while writing:

   | ID | Standard | How to Apply |
   |----|----------|-------------|
   | C01 | Intent Alignment | Title promise must match content delivery |
   | C02 | Direct Answer | Core answer in first 150 words |
   | C06 | Audience Targeting | State "this article is for..." |
   | C10 | Semantic Closure | Conclusion answers opening question + next steps |
   | O01 | Heading Hierarchy | H1→H2→H3, no level skipping |
   | O02 | Summary Box | Include TL;DR or Key Takeaways |
   | O06 | Section Chunking | Each section single topic; paragraphs 3–5 sentences |
   | O09 | Information Density | No filler; consistent terminology |
   | R01 | Data Precision | ≥5 precise numbers with units |
   | R02 | Citation Density | ≥1 external citation per 500 words |
   | R04 | Evidence-Claim Mapping | Every claim backed by evidence |
   | R07 | Entity Precision | Full names for people/orgs/products |
   | C03 | Query Coverage | Cover ≥3 query variants (synonyms, long-tail) |
   | O08 | Anchor Navigation | Table of contents with jump links |
   | O10 | Multimedia Structure | Images/videos have captions and carry information |
   | E07 | Practical Tools | Include downloadable templates, checklists, or calculators |

   _These 16 items apply across all content types. For content-type-specific dimension weights, see the Content-Type Weight Table in [core-eeat-benchmark.md](../../references/core-eeat-benchmark.md)._
   _Full 80-item benchmark: [references/core-eeat-benchmark.md](../../references/core-eeat-benchmark.md)_
   _For complete content quality audit: use [content-quality-auditor](../../cross-cutting/content-quality-auditor/)_
   ```

3. **Rechercher et planifier**

   Avant de rédiger :
   
   ```markdown
   ### Content Research
   
   **SERP Analysis**:
   - Top results format: [what's ranking]
   - Average word count: [X] words
   - Common sections: [list]
   - SERP features: [snippets, PAA, etc.]
   
   **Keyword Map**:
   - Primary: [keyword] - use in title, H1, intro, conclusion
   - Secondary: [keywords] - use in H2s, body paragraphs
   - LSI/Related: [terms] - sprinkle naturally throughout
   - Questions: [PAA questions] - use as H2/H3s or FAQ
   
   **Content Angle**:
   [What unique perspective or value will this content provide?]
   ```

4. **Créer un titre optimisé**

   ```markdown
   ### Title Optimization
   
   **Requirements**:
   - Include primary keyword (preferably at start)
   - Under 60 characters for full SERP display
   - Compelling and click-worthy
   - Match search intent
   
   **Title Options**:
   
   1. [Title option 1] ([X] chars)
      - Keyword position: [front/middle]
      - Power words: [list]
   
   2. [Title option 2] ([X] chars)
      - Keyword position: [front/middle]
      - Power words: [list]
   
   **Recommended**: [Best option with reasoning]
   ```

5. **Rédiger la méta description**

   ```markdown
   ### Meta Description
   
   **Requirements**:
   - 150-160 characters
   - Include primary keyword naturally
   - Include call-to-action
   - Compelling and specific
   
   **Meta Description**:
   "[Description text]" ([X] characters)
   
   **Elements included**:
   - ✅ Primary keyword
   - ✅ Value proposition
   - ✅ CTA or curiosity hook
   ```

6. **Structurer le contenu avec des en-têtes SEO**

   ```markdown
   ### Content Structure
   
   **H1**: [Primary keyword in H1 - only one per page]
   
   **Introduction** (100-150 words)
   - Hook reader in first sentence
   - State what they'll learn
   - Include primary keyword in first 100 words
   
   **H2**: [Secondary keyword or question]
   [Content section]
   
   **H2**: [Secondary keyword or question]
   
   **H3**: [Sub-topic]
   [Content]
   
   **H3**: [Sub-topic]
   [Content]
   
   **H2**: [Secondary keyword or question]
   [Content]
   
   **H2**: Frequently Asked Questions
   [FAQ section for PAA optimization]
   
   **Conclusion**
   - Summarize key points
   - Include primary keyword
   - Clear call-to-action
   ```

7. **Appliquer les bonnes pratiques SEO on-page**

   ```markdown
   ### On-Page SEO Checklist
   
   **Keyword Placement**:
   - [ ] Primary keyword in title
   - [ ] Primary keyword in H1
   - [ ] Primary keyword in first 100 words
   - [ ] Primary keyword in at least one H2
   - [ ] Primary keyword in conclusion
   - [ ] Primary keyword in meta description
   - [ ] Secondary keywords in H2s/H3s
   - [ ] Related terms throughout body
   
   **Content Quality**:
   - [ ] Comprehensive coverage of topic
   - [ ] Original insights or data
   - [ ] Actionable takeaways
   - [ ] Examples and illustrations
   - [ ] Expert quotes or citations (for E-E-A-T)
   
   **Readability**:
   - [ ] Paragraphs of 3-5 sentences (per CORE-EEAT O06 Section Chunking standard)
   - [ ] Varied sentence length
   - [ ] Bullet points and lists
   - [ ] Bold key phrases
   - [ ] Table of contents for long content
   
   **Technical**:
   - [ ] Internal links to relevant pages (2-5)
   - [ ] External links to authoritative sources (2-3)
   - [ ] Image alt text with keywords
   - [ ] URL slug includes keyword
   ```

8. **Rédiger le contenu**

   Suivez cette structure :

   ```markdown
   # [H1 with Primary Keyword]
   
   [Hook sentence that grabs attention]
   
   [Problem statement or context - why this matters]
   
   [Promise - what the reader will learn/gain] [Include primary keyword naturally]
   
   [Brief overview of what's covered - can be bullet points for scanability]
   
   ## [H2 - First Main Section with Secondary Keyword]
   
   [Introduction to section - 1-2 sentences]
   
   [Main content with valuable information]
   
   [Examples, data, or evidence to support points]
   
   [Transition to next section]
   
   ### [H3 - Sub-section if needed]
   
   [Detailed content]
   
   [Key points in bullet format]:
   - Point 1
   - Point 2
   - Point 3
   
   ## [H2 - Second Main Section]
   
   [Continue with valuable content...]
   
   > **Pro Tip**: [Highlighted tip or key insight]
   
   | Column 1 | Column 2 | Column 3 |
   |----------|----------|----------|
   | Data | Data | Data |
   
   ## [H2 - Additional Sections as Needed]
   
   [Content...]
   
   ## Frequently Asked Questions
   
   ### [Question from PAA or common query]?
   
   [Direct, concise answer in 40-60 words for featured snippet opportunity]
   
   ### [Question 2]?
   
   [Answer]
   
   ### [Question 3]?
   
   [Answer]
   
   ## Conclusion
   
   [Summary of key points - include primary keyword]
   
   [Final thought or insight]
   
   [Clear call-to-action: what should reader do next?]
   ```

9. **Optimiser pour les extraits optimisés (featured snippets)**

   ```markdown
   ### Featured Snippet Optimization
   
   **For Definition Snippets**:
   "[Term] is [clear, concise definition in 40-60 words]"
   
   **For List Snippets**:
   Create clear, numbered or bulleted lists under H2s
   
   **For Table Snippets**:
   Use comparison tables with clear headers
   
   **For How-To Snippets**:
   Number each step clearly: "Step 1:", "Step 2:", etc.
   ```

10. **Ajouter les liens internes/externes**

   ```markdown
   ### Link Recommendations
   
   **Internal Links** (include 2-5):
   1. "[anchor text]" → [/your-page-url] (relevant because: [reason])
   2. "[anchor text]" → [/your-page-url] (relevant because: [reason])
   
   **External Links** (include 2-3 authoritative sources):
   1. "[anchor text]" → [authoritative-source.com] (supports: [claim])
   2. "[anchor text]" → [authoritative-source.com] (supports: [claim])
   ```

11. **Revue SEO finale**

    ```markdown
    ### Content SEO Score

    | Factor | Status | Notes |
    |--------|--------|-------|
    | Title optimized | ✅/⚠️/❌ | [notes] |
    | Meta description | ✅/⚠️/❌ | [notes] |
    | H1 with keyword | ✅/⚠️/❌ | [notes] |
    | Keyword in first 100 words | ✅/⚠️/❌ | [notes] |
    | H2s optimized | ✅/⚠️/❌ | [notes] |
    | Internal links | ✅/⚠️/❌ | [notes] |
    | External links | ✅/⚠️/❌ | [notes] |
    | FAQ section | ✅/⚠️/❌ | [notes] |
    | Readability | ✅/⚠️/❌ | [notes] |
    | Word count | ✅/⚠️/❌ | [X] words |

    **Overall SEO Score**: [X]/10

    **Improvements to Consider**:
    1. [Suggestion]
    2. [Suggestion]
    ```

12. **Auto-vérification CORE-EEAT**

    Après la rédaction, vérifiez le contenu par rapport aux contraintes CORE-EEAT chargées :

    ```markdown
    ### CORE-EEAT Post-Write Check

    | ID | Standard | Status | Notes |
    |----|----------|--------|-------|
    | C01 | Intent Alignment: title = content | ✅/⚠️/❌ | [notes] |
    | C02 | Direct Answer in first 150 words | ✅/⚠️/❌ | [notes] |
    | C06 | Audience explicitly stated | ✅/⚠️/❌ | [notes] |
    | C10 | Conclusion answers opening question | ✅/⚠️/❌ | [notes] |
    | O01 | Heading hierarchy correct | ✅/⚠️/❌ | [notes] |
    | O02 | Summary/Key Takeaways present | ✅/⚠️/❌ | [notes] |
    | O06 | Paragraphs 3–5 sentences | ✅/⚠️/❌ | [notes] |
    | O09 | No filler; consistent terms | ✅/⚠️/❌ | [notes] |
    | R01 | ≥5 precise data points with units | ✅/⚠️/❌ | [notes] |
    | R02 | ≥1 citation per 500 words | ✅/⚠️/❌ | [notes] |
    | R04 | Claims backed by evidence | ✅/⚠️/❌ | [notes] |
    | R07 | Full entity names used | ✅/⚠️/❌ | [notes] |
    | C03 | ≥3 query variants covered | ✅/⚠️/❌ | [notes] |
    | O08 | Table of contents with jump links | ✅/⚠️/❌ | [notes] |
    | O10 | Images/videos captioned and informative | ✅/⚠️/❌ | [notes] |
    | E07 | Downloadable template/checklist included | ✅/⚠️/❌ | [notes] |

    **Items Needing Attention**: [list any ⚠️/❌ items]

    _For full 80-item audit, use [content-quality-auditor](../../cross-cutting/content-quality-auditor/)_
    ```

## Points de contrôle de validation

### Validation des entrées
- [ ] Mot-clé principal confirmé et conforme à l'intention de recherche
- [ ] Nombre de mots cible spécifié (minimum 800 mots pour un contenu substantiel)
- [ ] Type de contenu et audience clairement définis
- [ ] URLs de concurrents examinées ou fonctionnalités SERP cibles identifiées

### Validation des sorties
- [ ] Densité du mot-clé principal entre 1 et 2 % (Remarque : la densité de mots-clés est une ligne directrice, pas une règle dure. Les moteurs de recherche modernes privilégient la pertinence sémantique et le langage naturel aux cibles de densité exactes. Concentrez-vous sur une couverture complète du sujet avec des variantes sémantiques plutôt que sur un pourcentage précis.)
- [ ] Toutes les sections du plan entièrement couvertes
- [ ] Liens internes inclus (2 à 5 liens pertinents)
- [ ] Section FAQ présente avec au moins 3 questions
- [ ] Score de lisibilité adapté à l'audience cible
- [ ] Source de chaque donnée clairement indiquée (~~données d'outil SEO, fournies par l'utilisateur, ou estimées)

## Exemple

**Utilisateur** : « Écris un article optimisé SEO sur les "bonnes pratiques du marketing par email" ciblant les petites entreprises »

**Sortie** :

```markdown
# Email Marketing Best Practices: A Complete Guide for Small Businesses

**Meta Description**: Discover proven email marketing best practices that help small businesses increase open rates, boost engagement, and drive sales. Start improving your campaigns today. (158 chars)

---

Want to know the secret behind small businesses that consistently turn subscribers into loyal customers? It's not luck—it's strategic email marketing.

Email marketing remains one of the most effective channels for small businesses, delivering an average ROI of $42 for every $1 spent. But with inboxes more crowded than ever, following email marketing best practices isn't optional—it's essential for survival.

In this guide, you'll learn:
- How to build a quality email list that converts
- Proven strategies to increase open and click rates
- Advanced personalization techniques that drive results
- Common mistakes that kill email performance

Let's dive into the strategies that will transform your email marketing.

## Why Email Marketing Matters for Small Businesses

Before we explore the best practices, let's understand why email deserves your attention.

Unlike social media where algorithms control who sees your content, email gives you direct access to your audience. You own your email list—no platform can take it away.

**Key email marketing statistics for small businesses**:
- 81% of SMBs rely on email as their primary customer acquisition channel
- Email subscribers are 3x more likely to share content on social media
- Personalized emails generate 6x higher transaction rates

## Building a High-Quality Email List

### Use Strategic Opt-in Incentives

The foundation of effective email marketing is a quality list. Here's how to grow yours:

**Lead magnets that convert**:
- Industry-specific templates
- Exclusive discounts or early access
- Free tools or calculators
- Educational email courses

> **Pro Tip**: The best lead magnets solve a specific, immediate problem for your target audience.

### Implement Double Opt-in

Double opt-in confirms subscriber intent and improves deliverability. Yes, you'll have fewer subscribers, but they'll be more engaged.

| Single Opt-in | Double Opt-in |
|---------------|---------------|
| More subscribers | Fewer subscribers |
| Higher bounce rates | Lower bounce rates |
| Lower engagement | Higher engagement |
| Spam risk | Better deliverability |

## Crafting Emails That Get Opened

### Write Compelling Subject Lines

Your subject line determines whether emails get opened or ignored.

**Subject line best practices**:
1. Keep it under 50 characters
2. Create urgency without being spammy
3. Use numbers and specifics
4. Personalize when possible
5. A/B test consistently

### Optimize Preview Text

The preview text (preheader) is your second chance to convince someone to open. Use it to expand on your subject line, not repeat it.

## Personalization Strategies That Work

Generic emails perform poorly. Here's how to personalize effectively:

### Segment Your Email List

Divide your list based on:
- Purchase history
- Engagement level
- Demographics
- Interests or preferences
- Customer lifecycle stage

### Use Dynamic Content

Send the same email but show different content blocks based on subscriber data.

## Frequently Asked Questions

### How often should small businesses send marketing emails?

For most small businesses, sending 1-2 emails per week strikes the right balance. This keeps you top-of-mind without overwhelming subscribers. Monitor your unsubscribe rates—if they spike after increasing frequency, scale back.

### What is a good email open rate for small businesses?

A good email open rate for small businesses is 20-25%. However, this varies by industry. E-commerce averages 15-20%, while B2B services often see 25-30%. Focus on improving your own benchmarks rather than industry averages.

### Should I buy email lists to grow faster?

Never buy email lists. Purchased lists violate GDPR and CAN-SPAM regulations, damage your sender reputation, and result in poor engagement. Organic list growth, while slower, produces much better results.

## Conclusion

Implementing these email marketing best practices will help your small business build stronger customer relationships and drive consistent revenue. Remember: quality always beats quantity in email marketing.

Start with one improvement today. Whether it's segmenting your list, testing subject lines, or cleaning inactive subscribers, small changes compound into significant results.

**Ready to level up your email marketing?** Download our free Email Marketing Checklist to ensure every campaign you send follows these best practices.

---

*Further reading: [Internal link: "How to Write Email Copy That Converts"]*

*Sources: [Litmus Email Marketing Statistics](https://litmus.com), [Campaign Monitor Email Benchmarks](https://campaignmonitor.com)*
```

## Templates par type de contenu

### Guide pratique

```
Write a how-to guide for [task] targeting [keyword]
```

### Article comparatif

```
Write a comparison article: [Option A] vs [Option B] for [keyword]
```

### Article à listes

```
Write a list post: "X Best [Items] for [Audience/Purpose]" targeting [keyword]
```

### Guide ultime

```
Write an ultimate guide about [topic] (3,000+ words) targeting [keyword]
```

## Conseils pour réussir

1. **Respectez l'intention de recherche** - les requêtes informationnelles appellent des guides, pas des pages de vente
2. **Donnez la valeur en tête** - placez les informations clés tôt, pour les lecteurs et les extraits
3. **Utilisez des données et des exemples** - le concret bat le générique à chaque fois
4. **Écrivez d'abord pour les humains** - l'optimisation SEO doit paraître naturelle
5. **Incluez des éléments visuels** - aérez le texte avec images, tableaux, listes
6. **Mettez à jour régulièrement** - le contenu frais est un signal positif pour les moteurs de recherche

## Documents de référence

- [Title Formulas](./references/title-formulas.md) - formules de titres éprouvées, mots puissants, schémas de CTR
- [Content Structure Templates](./references/content-structure-templates.md) - templates pour articles de blog, comparatifs, listicles, how-tos, pages piliers

## Skills associés

- [keyword-research](../../research/keyword-research/) — trouver les mots-clés à cibler
- [geo-content-optimizer](../geo-content-optimizer/) — optimiser pour les citations par les IA
- [meta-tags-optimizer](../meta-tags-optimizer/) — créer des balises méta accrocheuses
- [on-page-seo-auditor](../../optimize/on-page-seo-auditor/) — auditer les éléments SEO
- [internal-linking-optimizer](../../optimize/internal-linking-optimizer/) — placer les liens internes pendant la rédaction
- [content-refresher](../../optimize/content-refresher/) — rafraîchir et mettre à jour un contenu existant
- [content-quality-auditor](../../cross-cutting/content-quality-auditor/) — audit CORE-EEAT complet en 80 points
- [memory-management](../../cross-cutting/memory-management/) — suivre les performances du contenu dans le temps
- [content-gap-analysis](../../research/content-gap-analysis/) — identifier les opportunités de contenu à rédiger
- [schema-markup-generator](../schema-markup-generator/) — ajouter des données structurées au contenu publié
