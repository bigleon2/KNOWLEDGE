# Analyse $FACON — Idée PM-skill précisée (PM éphémère extrait de SKILL.md, usage IA externe) — Task 60 G3 / D603

> **Directives analysées (verbatim, 2 tours)** — (i) idée originale : « à la place de sauvegarder les prompts maitres… il faudrait créer un skill "PM-skill" qui lorsque j'écrirai "PM-skill(gen-plan)" alors "PM-skill" générera le prompt maître de mon skill "gen-plan" et l'exécutera automatiquement via un script PY. analyse $FACON cette idée… Si cela augmente les performances de fonctionnement de mon écosystème alors applique-la $FACON à mon écosystème » — (ii) précision E13 : « mon skill "PM-skill" devra extraire les informations de mes skills (avec "skill.md") en pour générer une nouvelle version prompt maitre (sans "skill.md" comme dans "PM-SKILL/") éphémère en format MD comme cela je pourrais l'utiliser dans une IA. si tu connais une meilleure manière d'appliquer ce principe de fonctionnement, propose-le puis après ma validation, intègre-le à mon écosystème ».
> **Ancrage** (règle d'or n°5 — zéro invention) : chaque chiffre/affirmation est sourcé — inventaire D601 (`download/inventaire-historique-task60.md`) ou vérification directe de ce tour (chemin:ligne cité).

---

## 0. Faits structurants du disque (vérifiés ce tour)

**F1 — La génération PM actuelle dérive du PM précédent, PAS de SKILL.md seul.** `scripts/generer-pm-skill.py:182-189` : la base de génération est « le PM le plus récent du corpus » (dérivation dynamique KO-L003) sur laquelle s'appliquent des substitutions verrouillées ; `:114-119` : SKILL.md est la **source de vérité du numéro de version** (frontmatter `version:`), mais le **corps** du PM vient du PM précédent + delta JSON (`:36-38` : « le script n'invente jamais de contenu »). Conséquence mécanique : sans corpus, KO-L004 ne sait plus générer (abandon `:182` si aucun PM de base).

**F2 — Le corpus ne couvre que 4 familles sur 68 skills.** `skills/@mon-ecosysteme/` : 9 fichiers, 396 Ko (inventaire c.2) — 5 PMs (gen-plan v3.35.2, correct-work v2.9.0, clone-chat v2.0.2, refactor-guard v1.8.1, + SHARED + INSTALL + ULTRA + SYNC + README). Or la racine compte **68 skills avec SKILL.md** (`ls skills/*/SKILL.md | wc -l` = 68, ce tour). **64 skills n'ont aujourd'hui aucune voie PM** — le principe « PM-skill(<skill>) » n'existe pour personne hors les 4 familles.

**F3 — L'auto-portance §6.2 est incohérente sur le disque.** SHARED §6.2 (ligne 157) : « Les prompts maîtres sont auto-porteurs (Architecture v2.0) : le Contexte Système est embarqué dans chaque prompt maître — aucune lecture externe n'est requise ». Réalité : PM correct-work v2.9.0 embarque son CONTEXTE SYSTÈME (grep = 2 occurrences) mais **PM gen-plan v3.35.2 ne l'embarque PAS** (grep = 0 ; en-tête : « Dépend : `PROMPT-MAITRE-SHARED.md` (lire en premier) » + §B « Lire PROMPT-MAITRE-SHARED.md avant de continuer »). **Le PM le plus utilisé de l'écosystème ne fonctionne pas seul dans une IA externe** — preuve que la simple « extraction » sans injection de contexte ne répond pas au besoin « l'utiliser dans une IA ».

**F4 — Le coût de la voie PM corpus est chiffré et lourd.** 17 touches/montée MINOR (inventaire c.1, worklog Task 48) ; 13 montées gen-plan en ~2 semaines (c.1) ; lags PM ×4+ documentés (c.4 : « lag 29/23/v3.26.0 résorbé », « lag hérité v2.7.0 », « lag §11 résorbé », « lag hérité SHARED §6.1 ») ; corpus exposé à la volatilité (3ᵉ recyclage corpus live en début de Task 60 — c.3 ; 1 montée entière perdue : v2.10.0 ; **4ᵉ manifestation ce tour** : perte ciblée du fichier plan, cf. §5).

**F5 — Les primitives de livraison existent déjà (zéro code à écrire — R4).** vue-upload v1.5.0 (`skills/vue-upload/SKILL.md`, KB) : `push <source>` (inscription download/, v1.2.0), `featured <fichier>` (épinglage livrable courant ★, v1.4.0), `share <fichier>` (lien externe VÉRIFIÉ sha256, v1.2.0), journal des téléchargements (v1.4.0), hygiène des versions (v1.5.0).

**F6 — Le bloc CONTEXTE SYSTÈME est déjà propagé mécaniquement.** propagate-context.py v2.0.8 (G2 ce tour, worklog) : 68 skills + 150 scripts + 2 agents portent le bloc §0 — **la matière première d'injection d'un PM auto-portant existe déjà** et est maintenue par la propagation.

**F7 — Précédent mécanique de lecture SKILL.md.** `generer-pm-skill.py:114-119` lit déjà SKILL.md comme source de vérité ; `:145-148` calcule déjà la couverture sections SKILL.md ↔ PM. La projection SKILL.md → PM est une extension naturelle d'une mécanique certifiée, pas une invention.

## 1. Analyse $FACON par critères chiffrés

### (i) Coût de la voie PM — corpus vs éphémère
| Voie | Coût par PM | Fréquence observée | Charge totale |
|---|---|---|---|
| PM corpus (KO-L004, 4 familles) | **17 touches**/montée (F4) — dont recalibrage croisé SHARED §6.1 + PM-INSTALL §2ter/§A.3 obligatoire (`generer-pm-skill.py:233-283`) | 13 montées gen-plan/~2 semaines (c.1) | Cascade 5 touches minimum (leçon L57-1) ; lags ×4+ (c.4) |
| PM éphémère (génération à la demande) | **0 touche d'état** — le PM éphémère n'est pas un artefact versionné, c'est une **projection du SKILL.md vivant** ; régénérer = relire | à la demande | 0 (rien à cascader, rien à recalibrer, rien à resceller) |

### (ii) Surface de volatilité
- Corpus : 396 Ko/9 fichiers exposés — **perdus 3 fois en direct** (c.3) ; la montée v2.10.0 entière a été anéantie faute de commit miroir (KO-L009) ; 4ᵉ manifestation ce tour (fichier plan).
- Éphémère : **0 octet de stockage permanent dans l'écosystème** — le PM se régénère depuis le SKILL.md, lui-même restauré par `eco_install_pipeline.py` depuis le miroir (preuve vivante début Task 60 : 52/52 SHA-256, 0 divergence après recyclage). La régénération est le chemin de rétablissement le plus court possible : **la volatilité est absorbée par construction**.

### (iii) Respect R4 (archive, jamais dupliquer)
- PM corpus = **spécification versionnée** (archive légitime R4) — les 7 PMs correct-work archivés (~250 Ko, inventaire c.2) sont l'historique des contrats des 4 familles.
- PM éphémère = **projection dérivée, pas un stock** — source de vérité unique : le SKILL.md installé (règle canonique G2 : la forme installée à la racine EST la référence). La sortie vit dans `download/` (livrable), pas dans l'état de l'écosystème. **R4 parfaitement respecté.**

### (iv) Risque de régression des arbitres
- **Retirer le corpus** (lecture littérale de l'idée originale « à la place de sauvegarder ») : verify-cross (100 % aujourd'hui) vérifie les PMs corpus ; integrity 108/108 manifeste le corpus ; `generer-pm-skill.py` exige un PM de base (F1) ; KO-L004 casse (récursion de dérivation rompue) ; l'archive R4 des spécifications est perdue. **Régression majeure et certaine.**
- **Ajouter la génération éphémère SANS toucher au corpus** : aucun arbitre ne change, aucune certification ne bouge, aucun fichier existant n'est modifié. **Régression nulle.**

### (v) Auto-portance (§6.2) — condition nécessaire de l'usage « dans une IA »
- Une IA externe (ChatGPT, Claude, Gemini…) n'a **pas accès au disque** : le PM éphémère DOIT embarquer son CONTEXTE SYSTÈME. C'est exactement le principe §6.2 — appliqué incohéremment aujourd'hui (F3).
- La matière première d'injection existe (F6) et l'échec du PM gen-plan corpus (non auto-portant, F3) démontre a contrario qu'une extraction sans injection **ne fonctionnerait pas** dans une IA externe.

### (vi) Faisabilité de l'extraction SKILL.md → PM éphémère (précision propriétaire)
- **Ce que SKILL.md contient** : frontmatter (name, version, category, description → mission + §4 YAML ; dependencies → §3 Relations) + corps (déclencheurs, spécification §..., checklists, conventions).
- **Ce qui manque et où le trouver** : CONTEXTE SYSTÈME → extrait SHARED §0 (F6 — déjà propagé, donc déjà normalisé) ; historique des versions → `skills/@historique/historiques-par-skill/<skill>.md` (71 fichiers archivés) ; mode d'emploi IA externe → gabarit standard fixe.
- **Précédent** : F7 — la lecture mécanique de SKILL.md et la couverture sections sont déjà certifiées dans `generer-pm-skill.py`.
- **Verdict : FAISABLE** — projection mécanique, déterministe, sans invention (le contenu vient du SKILL.md ; le script structure, il ne rédige pas — aligné KO-L003 et sur la garde « le script n'invente jamais »).

### (vii) Portabilité IA externe (précision propriétaire)
- Contraintes : pas d'accès disque (→ v) ; boîte system-prompt/permier message (→ gabarit d'emploi explicite : « coller ce fichier comme prompt système ») ; traçabilité (→ bloc provenance : skill, version, date, **SHA-256 du SKILL.md source** — reproductibilité prouvable).
- Livraison : `download/PM-ephemere-<skill>-v<version>.md` + vue-upload push + épinglage featured (F5) + share optionnel (lien vérifié sha256). Le propriétaire récupère le fichier en un clic depuis le portail et le colle dans l'IA de son choix.

## 2. Verdict $FACON (mécanique — les deux issues étaient valides, les chiffres décident)

**Usage PORTABILITÉ (directive précisée : PM éphémère extrait de SKILL.md, format MD, sans SKILL.md, pour IA externe) : AUGMENTE les performances de l'écosystème.** Chiffré :
- **Couverture : 4 familles → 68 skills (×17)** — 64 skills sans voie PM aujourd'hui (F2) ;
- **Coût : 17 touches/PM → 0** (i) ;
- **Lag : 4+ lags documentés → 0 structurel** — le PM éphémère est TOUJOURS à la version du SKILL.md vivant (le lag est impossible par construction) ;
- **Volatilité : 396 Ko exposés → 0 octet** (ii) — la 4ᵉ manifestation de ce tour renforce la preuve ;
- **Auto-portance : incohérente (F3) → garantie par construction** (v).

**Usage REMPLACEMENT DU CORPUS (idée originale : « à la place de sauvegarder ») : NE PAS APPLIQUER.** Motif mécanique (iv + F1) : `generer-pm-skill.py` exige un PM de base ; verify-cross/integrity certifient le corpus ; l'archive R4 des spécifications serait perdue. Régression certaine des arbitres pour un gain nul (le corpus ne coûte rien à conserver — il ne grandit qu'aux montées des 4 familles, déjà couvertes par KO-L004).

## 3. Proposition — meilleure manière d'appliquer le principe (directive : « propose-le puis après ma validation, intègre-le »)

**« PM-skill = couche de portabilité universelle, additive, corpus intact »** — l'idée précisée est conservée INTEGRALEMENT (extraction depuis SKILL.md, PM éphémère MD sans format SKILL.md, génération à la demande, usage IA), enrichie de 5 ajouts que l'idée brute n'avait pas :

1. **Skill `pm-skill` à la racine** (`skills/pm-skill/`, kebab-case, SKILL.md 200-500 L) — déclencheur verbatim `PM-skill(<nom-du-skill>)` (+ alias `pm-skill(<nom>)`, « génère le prompt maître de X », « exporte X pour une IA »).
2. **Script `scripts/generer-pm-ephemere.py`** (Python stdlib, self-test embarqué, idempotent ×2 — conventions script-creator) :
   - `--generate <skill>` : lit `skills/<skill>/SKILL.md` (frontmatter + corps) → **injecte le CONTEXTE SYSTÈME** (extrait SHARED §0 — même bloc que propagate-context, F6) → assemble le PM éphémère auto-portant : bloc provenance (skill, version, date, SHA-256 du SKILL.md source) + **mode d'emploi IA externe** + CONTEXTE SYSTÈME + mission (description) + déclencheurs + spécification (corps SKILL.md) + Relations (dependencies YAML) + historique condensé (depuis @historique si présent) → écrit `download/PM-ephemere-<skill>-v<version>.md` ;
   - `--check <skill>` : éligibilité + cohérence ; `--list` : les 68 skills éligibles ;
   - **déterministe** : même SKILL.md (même jour) → sortie byte-identique ; **zéro invention** : le contenu provient exclusivement du SKILL.md + blocs SHARED — le script projette, il ne rédige pas (KO-L003).
3. **Livraison intégrée vue-upload** (R4 — zéro nouveau code, F5) : le PM éphémère atterrit dans `download/` → `push` l'inscrit, `featured` l'épingle en livrable courant ★, `share` donne un lien externe vérifié sha256 sur demande — récupération en un clic, collage dans l'IA de votre choix.
4. **Corpus @mon-ecosysteme INTACT** : KO-L004 continue pour les 4 familles (spécifications versionnées + arbitres verts + archive R4). Le PM éphémère d'une famille se génère AUSSI depuis son SKILL.md vivant (toujours courant — le lag c.4 est neutralisé pour l'usage externe **sans toucher au corpus**).
5. **Cascade légère** (hors KO-L004 — pas de PM corpus, donc pas de recalibrage SHARED §6.1/PM-INSTALL) : SKILL.md + script + evals + KB + pin ECO_SKILLS + historiques-par-skill + ensure-installed — la voie d'intégration standard d'un skill non-famille (précédents : les 64 skills non-famille existants).

**Ce que la proposition apporte EN PLUS de l'idée brute** : (a) **l'injection CONTEXTE SYSTÈME** — sans elle, le PM éphémère serait non-auto-portant comme le PM gen-plan actuel (F3) et ne fonctionnerait pas dans une IA externe ; (b) **la livraison vue-upload intégrée** — l'idée brute s'arrêtait à la génération, le dernier kilomètre (récupérer le fichier) est couvert par les primitives existantes ; (c) **la préservation du corpus** — l'idée originale (« à la place de sauvegarder ») cassait KO-L004 et les arbitres (iv/F1) ; (d) **la traçabilité SHA-256** — reproductibilité prouvable du PM éphémère ; (e) **le mode d'emploi IA externe** — le fichier est immédiatement utilisable dans n'importe quelle IA sans connaissance de l'écosystème.

**Variantes secondaires (documentées pour transparence, non recommandées)** :
- **V1 « remplacement corpus »** : rejetée — §2 (régression arbitres certaine).
- **V2 « exécution interne automatique »** (l'idée originale : le script PY exécute le PM généré DANS l'écosystème) : superflue — dans l'écosystème, le skill installé EST déjà la forme exécutable (règle canonique G2) ; exécuter un PM généré reviendrait à dupliquer la voie native (R4). L'exécution via PM reste utile UNIQUEMENT hors écosystème (IA externe) — ce que la proposition couvre par le mode d'emploi embarqué.

## 4. Prochaine étape — VALIDATION PROPRIÉTAIRE REQUISE (directive verbatim)

Conformément à « propose-le puis après ma validation, intègre-le à mon écosystème » : **aucune intégration n'est effectuée avant validation explicite**.

- **Si la proposition §3 est validée** → G3 SG2 : création du skill pm-skill + script + evals + KB + cascade légère (D604 branche validée), puis G4 (correct-work v2.11.0 — DERNIÈRE action) puis G5 (clôture).
- **Si ajustement demandé** → E13 sur le présent rapport, re-proposition.
- **Si rejet définitif** → consignation motivée (worklog + présent rapport), enchaînement direct G4.

## 5. Incident de volatilité n°4 (journalisé — règle d'or n°1)

Au tour G3, lors de l'édition E13 du plan : perte ciblée du fichier `download/plan-task60-ordre-directive-4-2-3-1.md` (entrée de répertoire fantôme — `ls` le liste, `stat`/`wc` échouent ; inode disparu). Tous les autres artefacts intacts (inventaire 9 250 o, plan-task59, worklog 240 603 o, piliers correct-work v2.9.0 / gen-plan v3.35.2 / SHARED v1.7.27) ; écriture download/ vérifiée fonctionnelle. Rétablissement : réécriture du plan depuis le contexte de session (contenu identique) avec la précision E13 intégrée dans la même passe. **Ce fait alimente le critère (ii)** : la volatilité L55-3 frappe les fichiers d'état ; la génération éphémère à la demande y est structurellement insensible.
