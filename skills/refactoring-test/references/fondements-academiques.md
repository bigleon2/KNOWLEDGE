# Fondements académiques et veille — refactoring-test (n°55)

> Sources de la recherche web approfondie (Task 7, session web-b4d7dd19, 2026-10-12 — subagent de recherche, ~17 requêtes ; seules les sources effectivement retournées sont citées — R3).

## Détection du besoin de refactoring (M1/M2)
- **Code smells — taxonomies** : les 22 smells de Fowler comme symptômes de problèmes de conception, non des défauts en soi — https://codesai.com/posts/2022%2F11 ; https://blog.codinghorror.com/code-smells ; https://www.ibm.com/think/topics/code-smells
- **Complexité cyclomatique** — quantification de la structure de contrôle (outillage 2024) — https://www.iieta.org
- **Hotspots & couplage temporel (Tornhill)** : fichier qui change souvent ET complexe = risque majeur ; « interest rate » de la dette ≈ fréquence de changement — https://guidefari.com ; https://se-radio.net ; https://www.usenix.org
- **Code Health + hotspots (CodeScene)** : score de santé et delta par changement — https://docs.enterprise.codescene.io ; https://codescene.com
- **Dette induite par le code IA (signaux 2024-2026)** : churn ×2 projeté (GitClear 2023), clones ×4 / blocs dupliqués ×8 (rapport 2025), part du refactoring 25 % → <10 % (Tembo) — https://www.gitclear.com ; https://www.tembo.io ; https://cerfacs.fr ; DORA 2024 via https://leaddev.com/technical-direction/how-ai-generated-code-accelerates-technical-debt

## Scoring principal/intérêt (M2)
- **SQALE (Letouzey)** : dette quantifiée en temps de remédiation, modèle orthogonal (ACM 2012, ~237 citations) — https://www.sonarsource.com ; https://dl.acm.org ; https://nhimg.org
- **Principal vs intérêt** : coût de remédiation ET coût de non-remédiation — https://devopedia.org
- **Krauchanka et al.** : estimation paramétrable du principal à partir des données de qualité structurelle — https://www.researchgate.net/publication/260649631_Estimating_the_Principal_of_an_Application's_Technical_Debt

## Graphe d'interactions & blast radius (M3)
- **Change impact analysis** : techniques à base de graphe dominantes (program dependency graphs, call graphs, graphs de messages — Wang 2014) — https://pmc.ncbi.nlm.nih.gov/articles/PMC3984771
- **Couplage afférent/efférent + instabilité** — https://coupling.dev/posts/related-topics/afferent-and-efferent-coupling
- **Blast radius** : « prédit le périmètre d'impact si un changement proposé ou une action d'agent échoue » — https://www.nofire.ai/glossary/blast-radius-analysis ; mesure/réduction par reachability — https://www.endorlabs.com/learn/vulnerability-blast-radius-how-to-measure-and-reduce-impact ; graphes avec lineage forward/backward — https://www.relyance.ai
- **Fitness functions d'architecture** (ThoughtWorks 2017 ; Ford/Parsons/Kua) : verdicts automatisés et continus — https://www.thoughtworks.com ; https://ebrary.net

## Indépendance de l'évaluateur (anti-auto-certification)
- **« The 40 % Problem »** (Janea Systems, 2026) : où les LLM achoppent en refactoring complexe et pourquoi les revues ratent les problèmes — https://www.janeasystems.com
- **Characterization tests / golden master (Feathers)** : le code legacy = code sans tests ; filet AVANT transformation — https://en.wikipedia.org/wiki/Characterization_test ; https://michaelfeathers.silvrback.com
- **AI-friendliness** : refactorabilité mesurée par LLM via Code Health (arXiv, 2026, 5 000 fichiers) — https://arxiv.org

## Signal de veille
- Étude à grande échelle sur la dette introduite par les assistants IA (arXiv 2026) ; hidden cost of AI-generated code in production (ResearchGate 2026, travaux Microsoft Research/Meta 2024-2025).

## Limites documentées
- Pas de source dédiée retournée pour le property-based testing comme filet (à sourcer avant ancrage normatif) ; canary/shadow deployment documentés indirectement via strangler fig/branch by abstraction (voir fondements refactoring-engineering).
