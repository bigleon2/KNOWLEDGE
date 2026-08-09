# CLONE — Écosystème Knowledge

> **Date du clone** : 2026-08-09
> **Skill** : clone-chat v2.0.0
> **Profil** : NORMAL
> **Sessions clonées** : 21 (Task ID 1-21)
> **Source** : worklog.md + arborescence live
> **Intégrité** : SHA-256 `d41c5016383fe0a09ce300790da22ed857c2515167aa1a655269079803c0442a` (pré-optimisation)

---

## §0 — Règle zéro

**Contexte perdu** : ce clone est la seule source de vérité. Tout doit être
reconstruit depuis ce fichier seul.

**Environnement cible** :
- **Racine projet** : `./` (racine du projet)
- **Skills** : `skills/` (78 skills : 6 écosystème + 72 métier)
- **Registre KB** : `skills/KNOWLEDGE.md`
- **Prompts maîtres** : `skills/_prompts-maitres/` (infrastructure, préfixe `_`)
- **Scripts écosystème** : `scripts/`
- **Worklog** : `worklog.md` (racine)
- **Download** : `download/` (livrables + backups)
- **Conventions** : kebab-case, semver, YAML frontmatter, sections `§`
- **Worklog format** : SHARED §1.4 (Task ID, Agent, Task, Work Log, Stage Summary)

---

## §1 — Chronologie

### §1.1 Résumé global

21 sessions couvrant la construction complète de l'écosystème Knowledge :
harmonisation clone-chat, vérifications correct-work, intégration
autonomous-agent, améliorations gen-plan, création de scripts
d'infrastructure (sync, spell-check, verify), corrections orthographiques,
mise à jour README, pushes GitHub, et clonage + vérification du clone.

### §1.2 Table des sessions

| # | Task ID | Agent | Tâche résumée | Résultat |
|---|---------|-------|---------------|----------|
| 1 | 1 | gen-plan v3.6.0 | Harmoniser clone-chat v1.2.0 → v2.0.0 | 12 écarts D1-D12 corrigés, 6 fichiers modifiés |
| 2 | 2 | correct-work v2.3.0 | Vérification CIBLE clone-chat v2.0.0 | 2 problèmes (S2, S3), 2 corrections, PASS |
| 3 | 3 | gen-plan v3.6.0 | Réécriture integrate-clone-chat-kb v2→v3 | Script v3.0.0 (250 lignes), 10/10 checks PASS |
| 4 | 4 | gen-plan v3.6.0 | 3 tâches : gen-plan v3.4.0, autonomous-agent, correct-work | gen-plan enrichi, autonomous-agent v1.0.0 créé, 78 skills |
| 5 | 5 | correct-work v2.3.0 | Cross-refs écosystème (gen-plan + correct-work) | 9 problèmes, 6 fichiers modifiés, PASS AVEC RÉSERVES |
| 6 | 6 | correct-work v2.3.0 | Vérification PROJET écosystème complet | 5 problèmes, 4 fichiers modifiés, PASS |
| 7 | 7 | gen-plan v3.6.0 | Script sync-download.py + CHECK 6 verify-cross | sync-download.py créé, verify-cross 55→60 checks |
| 8 | 8 | correct-work v2.3.0 | Vérification scripts Python (sync + verify) | 10 findings, 7 corrections, 3 fichiers modifiés, PASS |
| 9 | 9 | correct-work v2.3.0 | README.md mise à jour + sync | 1 S2 corrigé, README synchronisé, PASS |
| 10 | 10 | gen-plan v3.6.0 | Push GitHub (download/) | 15 fichiers pushés, token sécurisé |
| 11 | 11 | gen-plan v3.6.0 | Phase A — Reconstruction _prompts-maitres/ + skills | 13 fichiers restaurés, 7/9 + 10/10 checks PASS |
| 12 | 12 | gen-plan v3.6.0 | Phase B — Recréer KNOWLEDGE.md | 91 lignes, 6 skills, 13 relations |
| 13 | 13 | correct-work + gen-plan | Phase C+D — Audit GLOBAL + corrections | 8 findings, 4 corrections, PASS final |
| 14 | 14 | gen-plan v3.6.0 | Push Phase D vers GitHub | 1129 fichiers, .gitignore enrichi, commit squashé |
| 15 | 15 | gen-plan v3.6.0 | correct-work v2.3.0→v2.4.0 (E9-E15) | 8/10 écarts traités, verify-correct-work.py, evals.json |
| 16 | 16 | correct-work v2.4.0 | Post-migration PM v2.3.0→v2.4.0 | 21 findings, PM v2.4.0 créé, _archive/ introduit |
| 17 | 17 | gen-plan + correct-work | Spell-check + lexique + spell-check.py | 126 corrections ortho, 216 entrées lexique, 31/31 tests |
| 18 | 18 | gen-plan + correct-work | Aliases double-pointeurs + nettoyage lexique-fr | 13 groupes/29 alias, 40/40 tests, lexique-fr.py supprimé |
| 19 | 19 | gen-plan v3.6.0 | ECOSYSTEM_FILES, aliases 13 groupes, préfixe `_` | verify-correct-work.py ajouté, convention `_` = infrastructure |
| 20 | 20 | clone-chat v2.0.0 | Clonage de discussion — écosystème complet | Clone produit, 8/8 checks PASS, profil NORMAL |
| 21 | 21 | correct-work v2.4.0 | Vérification CIBLE du clone | 5 findings (2 S2, 2 S3, 1 S4), 3 corrections, PASS |

### §1.3 Détail des 5 dernières sessions

**Session 15 (Task ID 15)** — correct-work v2.3.0 → v2.4.0
- Agent : gen-plan v3.6.0, exécution E9-E15, profil NORMAL
- 8 écarts traités sur 10 (D1-D6, D9-D10 ; D7-D8 reportés v2.5.0+)
- Création `scripts/verify-correct-work.py` (16 checks automatisés)
- Intégration checklists opérationnelles §10.6-§10.10 dans SKILL.md
- Ajout 5 métriques de performance §2.8
- Découplage gen-plan (autonome si absent) + support multi-cibles
- Hook correct-work dans gen-plan E8
- KNOWLEDGE.md v2.3.0 → v2.4.0, SHARED §5.2 mis à jour
- Vérifications finales : 60/60 + 76/76 + 16/16 + SYNC OK
- Backlog : D7 (rapport JSON), D8 (nettoyage PM §8-9) reportés

**Session 16 (Task ID 16)** — Post-migration PM v2.3.0 → v2.4.0
- Agent : correct-work v2.4.0 DIRECT
- 21 findings (2 S1, 12 S2, 4 S3, 3 S4)
- S1 : PM v2.3.0 jamais migré → création PM v2.4.0 (528 lignes)
- S1 : verify-correct-work.py réfère fichier inexistant (déjà corrigé)
- 12 S2 : verify-cross.py, sync-download.py, SHARED §6.1, README.md (8 edits), KNOWLEDGE.md (typo), verify-cross CHECK 5 label
- Archivage PM v2.3.0 dans `_prompts-maitres/_archive/`
- 7 fichiers modifiés, 1 créé, 1 archivé, 1 supprimé
- Convention `_archive/` introduite pour anciennes versions de PMs

**Session 17 (Task ID 17)** — Spell-check écosystème
- Agent : gen-plan v3.6.0 + correct-work v2.4.0
- Extraction corpus FR : 3148 mots uniques, 619 FR probables
- Lexique dynamique : 216 entrées (185 FR accents + 31 EN tech)
- Création `scripts/spell-check.py` v1.0.0 (5 modes : scan/fix/learn/test/stats)
- 126 corrections orthographiques dans 15 fichiers
- 31/31 tests PASS
- verify-cross 60/60, sync OK

**Session 18 (Task ID 18)** — Aliases double-pointeurs
- Agent : gen-plan v3.6.0 + correct-work v2.4.0
- Suppression `scripts/lexique-fr.py` (430 lignes, obsolète)
- Implémentation système double-pointeurs dans spell-check.py
- 8→13 groupes canoniques, 17→29 alias
- 9 nouveaux tests (40 total), 40/40 PASS
- Principe : même rôle = alias, rôles différents = pas d'alias

**Session 19 (Task ID 19)** — ECOSYSTEM_FILES + aliases + convention `_`
- Agent : gen-plan v3.6.0
- D1 : verify-correct-work.py ajouté dans ECOSYSTEM_FILES (18 fichiers)
- D1-bis : 33 corrections verify-correct-work.py + 34 worklog.md
- D2 : Aliases enrichis 8→13 canoniques, 17→29 alias
- D3 : Analyse préfixe `_` dans `_prompts-maitres/` → GARDER (infrastructure)
- SHARED §1.2 : exception « préfixe `_` = infrastructure » ajoutée
- README `_prompts-maitres` : annotation explicative

**Session 21 (Task ID 21)** — Vérification CIBLE du clone
- Agent : correct-work v2.4.0 DIRECT
- Plan autonome (mode CIBLE), 7 sections à vérifier
- 5 findings (2 S2, 2 S3, 1 S4)
  - F1 S2 corrigé : §1.2 session 2 « (S1, S2) » → « (S2, S3) »
  - F2 S2 corrigé : chemin verify-correct-work.py → skills/correct-work/scripts/
  - F3 S3 corrigé : §0 chemin absolu → relatif « ./ »
  - F4 S4 accepté : 76 non documenté (spell-check interne)
  - F5 S3 accepté : références accent (convention FR)
- Verdict : PASS

---

## §2 — Écosystème skills

### §2.1 Skills écosystème (6)

| Skill | Version | Fichiers clés | Statut |
|-------|---------|-------------|--------|
| **gen-plan** | v3.6.0 | `skills/gen-plan/SKILL.md` (179L), 5 refs, evals | stable |
| **correct-work** | v2.4.0 | `skills/correct-work/SKILL.md` (316L), scripts/verify-correct-work.py, evals | stable |
| **clone-chat** | v2.0.0 | `skills/clone-chat/SKILL.md` (362L), références/clone-template.md | stable |
| **skills-inventory** | v1.0.0 | (existant, non modifié dans ces sessions) | stable |
| **skill-creator** | v1.0.0 | (existant, non modifié dans ces sessions) | stable |
| **autonomous-agent** | v1.0.0 | `skills/autonomous-agent/SKILL.md`, références/agent-format.md | stable |

### §2.2 Scripts écosystème

| Script | Lignes | Description |
|--------|--------|-------------|
| `scripts/verify-cross.py` | 231 | Vérification croisée 6 axes (60 checks) des prompts maîtres + sync |
| `scripts/sync-download.py` | 179 | Synchronisation `download/` ↔ `skills/_prompts-maitres/` (CHECK + SYNC) |
| `scripts/spell-check.py` | 872 | Vérification orthographique (FR+EN), lexique 216 entrées, 13 groupes aliases, 40 tests |
| `scripts/compile-yaml.py` | 106 | Compilation YAML frontmatter |
| `skills/correct-work/scripts/verify-correct-work.py` | — | 16 checks post-install correct-work |
| `scripts/lexique-domain.json` | — | Lexique FR+EN dynamique (216 entrées, 13 groupes aliases) |

### §2.3 Spécifications techniques

| Fichier | Taille | Description | Traitement clone |
|---------|--------|-------------|------------------|
| `skills/gen-plan/SKILL.md` | ~195L | Planification 15 étapes E1-E15, 4 modes, 3 profils | Résumé structuré |
| `skills/correct-work/SKILL.md` | ~316L | Vérification 5 étapes, 3 modes, multi-cibles, métriques | Résumé structuré |
| `skills/clone-chat/SKILL.md` | ~362L | Clonage 7+1 étapes, 8 checks, 5 drifts, auto-clonage | Résumé structuré |
| `skills/autonomous-agent/SKILL.md` | — | Mémoire 2 niveaux, 5 modules, 4 modes, pipeline A-H | Résumé structuré |
| `skills/_prompts-maitres/PROMPT-MAITRE-SHARED.md` | 221L | Socle commun §0-§6 (règle zéro, registre KB, relations) | In extenso si < 200L sinon condensé |
| `scripts/verify-cross.py` | 231L | Vérification croisée 6 axes, 60 checks | Résumé structuré |
| `scripts/spell-check.py` | 872L | Scan/fix/learn/test/stats, 13 groupes aliases, 40 tests | Résumé structuré (objectifs, modules clés) |
| `scripts/sync-download.py` | 179L | Sync download/ ↔ _prompts-maitres/, 2 modes | In extenso si < 200L sinon condensé |
| `scripts/lexique-domain.json` | — | 216 entrées FR+EN, 13 groupes aliases | Métadonnées (entrée, groupes, taille) |

### §2.4 Prompts maîtres

| Fichier | Lignes | Rôle |
|---------|--------|------|
| `skills/_prompts-maitres/PROMPT-MAITRE-SHARED.md` | 221 | Socle commun (§0-§6) |
| `skills/_prompts-maitres/PROMPT-MAITRE-GEN-PLAN-v3.6.0.md` | ~912 | Spécification complète gen-plan |
| `skills/_prompts-maitres/PROMPT-MAITRE-CORRECT-WORK-v2.4.0.md` | ~528 | Spécification complète correct-work |
| `skills/_prompts-maitres/PROMPT-MAITRE-CLONE-CHAT-v2.0.0.md` | ~662 | Spécification complète clone-chat |
| `skills/_prompts-maitres/_archive/PROMPT-MAITRE-CORRECT-WORK-v2.3.0.md` | ~490 | Archive version précédente |
| `skills/_prompts-maitres/README.md` | 341 | Documentation architecture 3 PMs + workflow |

### §2.5 Historique des interactions clés

> **Note de différenciation** : Cette section §2.5 trace les **interactions entre skills** (qui a invoqué/vérifié/archivé qui, dans quelle session). La section §3.1 trace les **décisions utilisateur** (choix conscients avec contexte et conséquences). Une même session peut apparaître dans les deux sections sous des angles complémentaires.

| Session | Interaction | Détails |
|---------|-----------|--------|
| 1 | clone-chat → SHARED | Harmonisation v1.2.0→v2.0.0, 12 écarts corrigés |
| 2 | correct-work → clone-chat | Vérification CIBLE, 2 corrections (guillemet, version PM) |
| 4 | gen-plan → autonomous-agent | Nouveau skill créé (mémoire court+long, pipeline A-H) |
| 5 | correct-work → gen-plan + SHARED | 9 corrections cross-refs, README, KNOWLEDGE |
| 7 | gen-plan → verify-cross | CHECK 6 ajouté (55→60 checks), sync-download créé |
| 11 | gen-plan → _prompts-maitres/ | Reconstruction complète (git reset recovery) |
| 15 | gen-plan → correct-work | Mise à jour v2.3.0→v2.4.0, verify-correct-work.py, evals |
| 16 | correct-work → écosystème | Post-migration 21 findings, PM v2.4.0, _archive/ |
| 17 | gen-plan → spell-check | Création spell-check.py, 126 corrections ortho |
| 18 | correct-work → spell-check | Aliases double-pointeurs, 40/40 tests |
| 19 | gen-plan → SHARED | Convention préfixe `_` = infrastructure |

---

## §3 — Décisions clés

### §3.1 Décisions utilisateur

| # | Décision | Contexte | Conséquence |
|---|----------|----------|-------------|
| 1 | Garder le préfixe `_` pour `_prompts-maitres/` | Session 19, analyse gen-plan E1-E8 | Convention SHARED §1.2 : `_` = dossier infrastructure, pas un skill |
| 2 | Introduire `_archive/` pour anciens PMs | Session 16, migration v2.3.0→v2.4.0 | Historique des versions conservé, PM actuel propre |
| 3 | Downgrade profil irréversible | Session 4, amélioration gen-plan v3.4.0 | Principe #8 : NORMAL→ECO possible, jamais ECO→NORMAL auto |
| 4 | Signaux de pression pour VIEUX PC | Session 4 | 3 signaux (disque, timeout, budget) × 2 seuils (warning, critique) |

### §3.2 Bugs corrigés

| # | Bug | Cause | Fix | Résultat |
|---|-----|-------|-----|----------|
| 1 | Guillemet non fermé §5 clone-chat | Écriture rapide | Fermeture ajoutée | PASS (session 2) |
| 2 | PM correct-work encore à v1.2.0 | Migration incomplète | 3 occurrences mises à jour | PASS (session 2) |
| 3 | file_hash() jamais appelée | Code mort | Suppression + import hashlib | PASS (session 8) |
| 4 | Chemins absolus en dur verify-cross | Hardcoding | `os.path.dirname` dynamique | PASS (session 8) |
| 5 | sync_ok jamais lue | Variable inutilisée | Suppression | PASS (session 8) |
| 6 | README 55 checks vs réel 60 | Incohérence numérique | 55→60, 5→6 axes | PASS (session 8) |
| 7 | CHECK 5 label ~850 vs réel 912 | Label trompeur | ~850→~912, plage 750-1000 | PASS (session 8) |
| 8 | do_sync copie fichiers identiques | Optimisation manquante | Skip si fichiers identiques | SYNC OK (session 8) |
| 9 | PM v2.3.0 jamais migré en v2.4.0 | Oubli post-session 15 | Création PM v2.4.0 (528 lignes) | ALL PASS (session 16) |
| 10 | 126 fautes orthographiques | Pas de spell-check | Création spell-check.py + correction | 0 finding (session 17) |

### §3.3 Conventions établies

| # | Convention | Règle | Exemple |
|---|-----------|-------|--------|
| 1 | kebab-case | Tous les répertoires et fichiers | `gen-plan`, `spell-check.py` |
| 2 | Semver | Versions MAJEUR.MINEUR.PATCH | `3.6.0`, `2.4.0` |
| 3 | Préfixe `_` = infrastructure | Dossiers `_X` ne sont pas des skills | `_prompts-maitres/`, `_archive/` |
| 4 | YAML frontmatter | Chaque SKILL.md commence par `---` YAML | name, version, category, dependencies |
| 5 | Sections `§` | Numérotation des sections | §0, §1, §1.1, §3.5 |
| 6 | Worklog SHARED §1.4 | Format unique partagé | Task ID, Agent, Task, Work Log, Stage Summary |
| 7 | Double-pointeurs (aliases) | Même rôle = alias, rôles différents = pas d'alias | `correct-work` → `vérifie ton travail` ; `corriger` ≠ `éditer` |
| 8 | Chemins relatifs | Jamais absolus dans les documents | `skills/clone-chat/SKILL.md` |
| 9 | In extenso < 200 lignes | Seuil pour contenu complet dans clones | Au-delà : résumé structuré |
| 10 | Cross-refs bidirectionnelles | Relations maintenues dans les deux sens | Frontmatter + KNOWLEDGE.md + §3 Relations |

### §3.4 Données de calibration

- **verify-cross.py** : 60/60 checks (6 axes : duplication, SHARED, relations, contenu, tailles, sync)
- **spell-check.py** : 40/40 tests unitaires, 0 finding écosystème cible
- **sync-download.py** : 5 fichiers synchronisés (SHARED, gen-plan PM, correct-work PM, clone-chat PM, README)
- **correct-work total checks** : 152 (60 + 76 + 16)

**Grille #token clone-chat v2.0.0** :

| Mode | #token estimé | Profil min. | Plage |
|------|--------------|-------------|-------|
| Discussion courte (< 5 sessions) | 2750 | ECO | 2000-3500 |
| Discussion moyenne (5-15 sessions) | 4500 | NORMAL | 3500-5500 |
| Discussion longue (> 15 sessions) | 7250 | NORMAL | 5500-9000 |

---

## §3.5 — Context Drift

| # | Type | Avant | Après | Session | Raison |
|---|------|-------|-------|---------|--------|
| 1 | ENRICHISSEMENT | correct-work v2.3.0 (5 étapes, 3 modes) | v2.4.0 (+ verify-correct-work.py, evals, métriques, multi-cibles) | 15 | Amélioration post-gen-plan E9-E15, 8/10 écarts traités |
| 2 | CORRECTION | PM correct-work v2.3.0 utilisé comme actif | v2.4.0 créé, v2.3.0 archivé dans `_archive/` | 16 | Migration manquée découverte par audit 21 findings |
| 3 | ENRICHISSEMENT | 8 groupes d'aliases, 17 alias | 13 groupes, 29 alias (+autonomous-agent, cross-references, prompt-maitre, skill-creator, skills-inventory) | 19 | Scan automatique écosystème par gen-plan |
| 4 | ENRICHISSEMENT | Aucune convention préfixe `_` | `_` = dossier infrastructure (SHARED §1.2) | 19 | Analyse gen-plan E1-E8, 9 fichiers référençant le chemin |
| 5 | MODIFICATION | 77 skills (5 écosystème + 72 métier) | 78 skills (6 écosystème + 72 métier) | 4 | Création autonomous-agent v1.0.0 |
| 6 | MODIFICATION | verify-cross.py 55 checks | 60 checks (CHECK 6 sync ajouté) | 7 | Création sync-download.py, nécessité de vérifier la synchronisation |
| 7 | RECALIBRAGE | README.md « deux autres » PMs | « trois autres » PMs (clone-chat ajouté) | 6 | Correction S4 audit PROJET |
| 8 | CORRECTION | lexique-fr.py (430 lignes, standalone) | Supprimé, remplacé par spell-check.py (lexique intégré) | 18 | Obsolète, aucune cross-référence |
| 9 | ENRICHISSEMENT | _prompts-maitres/ sans distinction sémantique | Annotation README explicative + convention SHARED §1.2 | 19 | Prévenir confusion skill vs infrastructure |

---

## §4 — Instructions

### Comment utiliser ce clone

1. **Lire ce fichier intégralement** — il est auto-suffisant, aucune dépendance externe
2. **Restaurer les fichiers prioritaires** dans cet ordre :
   1. `skills/_prompts-maitres/PROMPT-MAITRE-SHARED.md` (socle commun)
   2. `skills/KNOWLEDGE.md` (registre KB)
   3. `skills/gen-plan/SKILL.md` + 5 références + evals
   4. `skills/correct-work/SKILL.md` + `skills/correct-work/scripts/verify-correct-work.py` + evals
   5. `skills/clone-chat/SKILL.md` + `références/clone-template.md`
   6. `skills/autonomous-agent/SKILL.md` + `références/agent-format.md`
   7. `scripts/verify-cross.py`, `scripts/sync-download.py`, `scripts/spell-check.py`
   8. `scripts/lexique-domain.json`

### Vérifications post-restauration

```bash
python3 scripts/verify-cross.py          # 60/60 PASS
python3 scripts/sync-download.py --check # SYNC OK
python3 scripts/spell-check.py --test    # 40/40 PASS
```

### Points d'attention

- Le préfixe `_` dans `_prompts-maitres/` signifie **infrastructure** (pas un skill)
- `_archive/` contient les anciennes versions de PMs (historique)
- Les 13 groupes d'aliases du spell-check protègent les termes métier
- correct-work v2.4.0 a 2 écarts reportés à v2.5.0+ (D7 rapport JSON, D8 nettoyage PM §8-9)
- Le fichier `upload/README.md` (233 lignes) documente l'architecture complète des 3 PMs

---

## §5 — Auto-clonage

Ce clone est **auto-référentiel**. Il contient les instructions pour se
cloner lui-même via le skill clone-chat v2.0.0.

**Mécanisme de croissance** :
1. Exécuter `clone-chat` sur la discussion en cours
2. Le nouveau clone incorpore tout le contexte de ce clone plus les
   nouvelles sessions
3. Les sections §1-§3 (données historiques) sont **enrichies**, tandis que
   §0, §4-§5 (auto-référentielles) sont **régénérées à l'identique**
4. Le nouveau clone remplace le précédent — chaîne de clonage
   théoriquement infinie sans perte d'information

**Propriété fondamentale** : un clone peut se cloner lui-même.

Pour exécuter un clonage : invoquer le skill `clone-chat` dans une nouvelle
session. Le skill lira le `worklog.md`, collectera les artefacts, et
produira un nouveau clone enrichi dans `download/`.