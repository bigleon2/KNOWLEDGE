# gen-plan v3.6.1 — Plan de décision : Refactoring du dépôt Knowledge

> **Date** : 2026-08-10
> **Profil** : NORMAL
> **Question** : *« D'après ton analyse de mon dépôt knowledge, penses-tu qu'on doit le refactoriser ? »*
> **#token estimé** : ~12 000

---

## E1 — Analyse de la demande

**Livrable** : Plan de décision argumenté (refactoriser oui/non, périmètre, priorités)
**Contrainte** : Analyse basée sur les faits observés, pas sur des suppositions
**Critères de succès** : Décision claire, phases priorisées, estimation de charge par phase

---

## E2 — Inventaire des ressources analysées

| Source | Méthode | #token
|--------|---------|--------|
| `skills/KNOWLEDGE.md` (v2.0.0, 93 lignes) | Lecture directe | ~800
| `skills/_prompts-maitres/PROMPT-MAITRE-SHARED.md` (222 lignes) | Lecture directe | ~1 500
| `download/README.md` (342 lignes) | Lecture directe | ~1 800
| Structure complète skills/ (78 dossiers, 1 095 fichiers, 62 MB) | Agent Explore #1 | ~40 000
| `download/` + `scripts/` (17 fichiers) | Agent Explore #2 | ~63 000
| Frontmatter 20 skills échantillonnés | Agent Explore #3 | ~30 000
| `design/` interne + 82 READMEs | Agent Explore #4 | ~92 000
| `KNOWLEDGE.md` racine (895 lignes, v3.0.0 obsolète) | Bash head | ~200

---

## E3 — Classification

**Type de tâche** : Type 4 (Analyse / Data Processing) — aucun livrable fichier web, produit un plan de décision.
**Mode par défaut** : M1 (Planification) — E1 à E8 uniquement.

---

## E4 — Estimation #token

| Phase | #token estimé |
|-------|---------------|
| E1-E2 Collecte (4 agents parallèles) | ~8 000
| E3-E6 Analyse et classification | ~1 500 |
| E7-E8 Synthèse et production du plan | ~2 500 |
| **Total** | **~12 000** |

---

## E5 — Skills sélectionnés

| Skill | Version | Usage |
|-------|---------|-------|
| gen-plan | >= v3.6.1 | Cadre de planification (ce document) |
| Aucun autre skill requis | — | Analyse pure, pas de production de code |

---

## E6 — Profilage ressource

**Profil** : NORMAL. Aucun signal de pression détecté.

---

## E7 + E8 — PLAN DE DÉCISION : Refactoring du dépôt Knowledge

### Réponse courte

**OUI, le dépôt doit être refactorisé.** Mais il s'agit d'un refactoring **chirurgical et progressif**, pas d'une réécriture. L'écosystème central (6 skills écosystème + registre KB + prompts maîtres) est sain et bien gouverné. Les problèmes sont concentrés dans 4 zones spécifiques qui peuvent être traitées indépendamment.

---

### État de santé global

| Axe | Score | Verdict |
|------|-------|---------|
| Skills écosystème (6) | **9/10** | Frontmatter complet, cross-refs bidirectionnelles, versions semver, 81/81 checks PASS |
| Registre KB (KNOWLEDGE.md) | **9/10** | 6 entrées cohérentes, 14 relations validées, source de vérité fonctionnelle |
| Prompts maîtres (4 fichiers) | **9/10** | Architecture SHARED+spécifiques propre, sync vérifiée |
| Scripts d'automatisation | **7/10** | verify-cross + sync-download + spell-check solides ; 2 scripts obsolètes |
| Frontmatter métier (71 skills) | **3/10** | 70% n'ont que `name`+`description`, pas de version/category/tags/dependencies |
| Structure `design/` | **2/10** | Méga-conteneur 54 MB, 113 sous-skills, router hybride fr/zh |
| Fichiers racine | **4/10** | KNOWLEDGE.md v3.0.0 obsolète (895 lignes), doublon avec skills/KNOWLEDGE.md |
| READMEs | **5/10** | 69/82 sont des stubs redirect morts dans design/brand-inspiration/ |
| `download/` | **6/10** | Miroir sync fonctionnel mais 2 scripts doublonnent + 1 zip artefact |
| **Score global** | **6/10** | Noyau sain, périphérie encombrée |

---

### Les 7 findings majeurs

#### 🔴 F1 — `design/` est un méga-conteneur de 113 sous-skills (54 MB, 87% du repo)

- Le root `SKILL.md` est un **routeur** en chinois, pas un skill opérationnel
- 77 style-skills, 24+ templates, 89 brand-inspiration dirs, 20 horizontal-craft refs
- Aucun des 113 sous-SKILL.md n'est déclaré dans KNOWLEDGE.md
- Le frontmatter root n'est pas conforme §1.3 (pas de version, pas de kebab-case, pas de category)
- **Impact** : Le registre KB ne voit qu'1 skill au lieu de ~113. `skills-inventory` est aveugle sur 87% du repo.

#### 🔴 F2 — Frontmatter métier : 70% non conformes au schéma §1.3

- Sur 20 skills échantillonnés : 14/20 manquent de `category`, `language`, `tags`, `dependencies`
- Les 6 skills écosystème sont 100% conformes → preuve que le schéma est viable
- 4 skills Z.AI (pdf, docx, xlsx, charts) utilisent un schéma alternatif (`metadata.version`)
- `pptx` a un nom de frontmatter (`ppt`) ≠ nom de dossier (`pptx`)
- **Impact** : Tout outil parsant le frontmatter n'a des données structurées que pour 30% du repo.

#### 🟠 F3 — `KNOWLEDGE.md` racine (895 lignes) est obsolète et contradictoire

- Version v3.0.0 datée 2026-07-12, mentionne « 12 agents spécialisés + 72+ skills »
- La source de vérité est `skills/KNOWLEDGE.md` v2.0.0 (6 eco + 71 métier)
- Risque de confusion pour tout agent qui lit la racine au lieu de `skills/`
- **Impact** : Ambiguïté sur le nombre de skills, les agents, et l'architecture.

#### 🟠 F4 — 69 READMEs stubs morts dans `design/brand-inspiration/`

- Contenu identique : redirect vers `getdesign.md` (5 lignes)
- La donnée réelle est dans `DESIGN.md`, déjà consommée par le système
- **Impact** : Bruit inutile, gonfle le compte de fichiers sans valeur.

#### 🟡 F5 — `download/` contient 2 scripts doublons + 1 artefact

- `verify-cross.py` et `sync-download.py` existent à la fois dans `scripts/` ET `download/`
- `clone-chat.zip` (116 KB) est un artefact généré qui ne devrait pas être versionné
- **Impact** : Confusion sur la source canonique des scripts.

#### 🟡 F6 — 2 scripts obsolètes dans `scripts/`

- `generate-knowledge-v3.py` (49 KB) : chemin hardcoded `/tmp/`, métadonnées stale
- `generate-clone-genplan.py` (32 KB) : one-shot avec 800+ lignes de contenu embarqué
- **Impact** : 81 KB de code mort qui risque d'être confondu avec des outils actifs.

#### 🟡 F7 — `download/README.md` référence un `_archive/` inexistant

- Ligne 29 : `└── _archive/  ← Anciennes versions de PMs (historique)`
- Ce dossier n'existe pas dans le repo actuel
- Le README mentionne aussi « 78 skills » et « 13 relations » (données stale)
- **Impact** : Documentation mensongère.

---

### Plan de refactoring — 4 phases indépendantes

#### Phase 1 — Nettoyage rapide (impact immédiat, risque zéro)
**#token estimé : ~3 000 | Priorité : HAUTE**

| # | Action | Fichiers | Risque |
|---|--------|----------|--------|
| 1.1 | Supprimer les 69 READMEs stubs morts | `design/design-systems/brand-inspiration/*/README.md` | Zéro — ce sont des redirects morts |
| 1.2 | Supprimer `clone-chat.zip` + ajouter `*.zip` au `.gitignore` | `download/clone-chat.zip` | Zéro — artefact régénérable |
| 1.3 | Supprimer les 2 scripts doublons de `download/` | `download/verify-cross.py`, `download/sync-download.py` | Zéro — canonical dans `scripts/` |
| 1.4 | Archiver les 2 scripts obsolètes | `scripts/generate-knowledge-v3.py`, `scripts/generate-clone-genplan.py` → `scripts/_archive/` | Zéro — plus utilisés |
| 1.5 | Supprimer `KNOWLEDGE.md` racine (895 lignes obsolètes) | `/home/z/my-project/KNOWLEDGE.md` | Faible — source de vérité est `skills/KNOWLEDGE.md` |
| 1.6 | Corriger `download/README.md` : mettre à jour les counts (78→77, 13→14), retirer la référence `_archive/` | `download/README.md` | Zéro |

**Résultat attendu** : -72 fichiers, -81 KB de code mort, documentation corrigée.

---

#### Phase 2 — Standardisation frontmatter métier (impact moyen, risque faible)
**#token estimé : ~15 000 | Priorité : MOYENNE | Peut se faire par lots**

| # | Action | Portée | Risque |
|---|--------|--------|--------|
| 2.1 | Écrire un script Python `scripts/fix-frontmatter.py` qui : détecte les SKILL.md sans frontmatter complet, ajoute les champs manquants (category: metier, language: fr, tags: [], version: 1.0.0, dependencies: []), préserve les champs existants | 65+ fichiers | Faible — ajoutatif, ne supprime rien |
| 2.2 | Corriger le cas `pptx` (name: ppt → pptx) | 1 fichier | Zéro |
| 2.3 | Corriger les 4 skills Z.AI (pdf, docx, xlsx, charts) : migrer `metadata.version: "1.0"` → `version: 1.0.0` au top-level | 4 fichiers | Faible |
| 2.4 | Exécuter `verify-cross.py` post-correction pour valider | — | Zéro |

**Résultat attendu** : 100% des SKILL.md avec frontmatter conforme §1.3.

---

#### Phase 3 — Traitement du méga-conteneur `design/` (impact fort, risque moyen)
**#token estimé : ~25 000 | Priorité : BASSE (long terme) | Nécessite une réflexion architecturale**

Cette phase est la plus complexe et mérite une session dédiée. Voici les options :

**Option A — Maintenir le statut quo partiel** :
- Corriger uniquement le frontmatter du root `design/SKILL.md` pour le rendre conforme §1.3
- Ajouter une entrée `design` dans KNOWLEDGE.md avec une note « conteneur multi-sous-skills »
- Avantage : zéro risque de casse. Inconvénient : le registre reste aveugle sur 113 sous-skills.

**Option B — Index partiel** :
- Même que A + ajouter les 77 style-skills au registre KB (en batch, via un script)
- Laisser les 24+ templates et 89 brands hors registre (ce sont des données de référence, pas des skills)
- Avantage : `skills-inventory` devient conscient des styles. Inconvénient : KNOWLEDGE.md gonfle (77 entrées).

**Option C — Décomposition complète** :
- Extraire les 77 style-skills vers `skills/style-*/SKILL.md` (à la racine de `skills/`)
- Extraire les 15 scenario `.md` en skills autonomes (`landing-page/`, `deck/`, etc.)
- Laisser `design/` en router mince + `design-templates/` + `horizontal-craft/`
- Avantage : architecture plate, chaque skill visible. Inconvénient : 90+ nouveaux dossiers à la racine, rupture potentielle des chemins internes.

**Recommandation** : Commencer par l'**Option A** (Phase 3a), puis évaluer après 2-3 sessions si l'Option B apporte assez de valeur pour justifier le coût.

---

#### Phase 4 — Amélioration continue de l'infrastructure
**#token estimé : ~5 000 | Priorité : BASSE | Quand le besoin se présente**

| # | Action | Détail |
|---|--------|--------|
| 4.1 | Relocater `compile-yaml.py` et `integrate-knowledge.py` | Dépendent de l'API Next.js → déplacer vers `mini-services/` ou `src/app/api/scripts/` |
| 4.2 | Uniformiser les fichiers racine de skills métier | Convention : aucun fichier au root hormis SKILL.md ; tout le reste dans `references/`, `scripts/`, `templates/` |
| 4.3 | Ajouter un check frontmatter à `verify-cross.py` | Détecter les SKILL.md sans frontmatter complet, signaler comme warning |
| 4.4 | Résoudre la duplication `ui-ux-pro-max/data/` vs `ui-ux-pro-max/assets/data/` | Supprimer un des deux, symlink l'autre |

---

### Matrice de priorité

| Phase | Impact | Effort | Risque | Ratio impact/effort | Quand |
|-------|--------|--------|--------|---------------------|------|
| **Phase 1** (nettoyage) | Moyen | Très faible | Zéro | ⭐⭐⭐⭐⭐ | Immédiatement |
| **Phase 2** (frontmatter) | Fort | Moyen | Faible | ⭐⭐⭐⭐ | Après Phase 1 |
| **Phase 3** (design/) | Très fort | Élevé | Moyen | ⭐⭐⭐ | Session dédiée |
| **Phase 4** (infra) | Faible | Faible | Faible | ⭐⭐ | Quand besoin |

---

### Conclusion

Le dépôt Knowledge a un **noyau excellent** (écosystème 6 skills, KB, prompts maîtres, scripts de vérification) mais une **périphérie encombrée** (frontmatter métier non standardisé, méga-conteneur design/, fichiers obsolètes, doublons).

Le refactoring est nécessaire et peut être lancé **immédiatement en Phase 1** avec un risque zéro et un gain immédiat en lisibilité. Les phases suivantes sont indépendantes et peuvent être espacées selon ton rythme.

**Verdict final : OUI, refactoriser — mais chirurgicalement, en 4 phases progressives.**
