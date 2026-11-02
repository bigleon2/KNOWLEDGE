# Rapport comparatif — Éléments de la discussion b6170b8b ↔ dépôt GitHub `bigleon2/KNOWLEDGE` (Task 40 / D003-D004)

> **Session** : web-6058b3ba · **Date** : 2026-11-02 · **Référentiel dépôt** : clone certifié `origin/main = fddbe94` (2026-11-02, tip poussé)
> **Tests de performances $FACON $FACON2** : `scripts/task40-perf-comparatif.py` → `work/task40-perf-comparatif.json` (3 runs médians par cible)

## 1. Comparaison mécanique élément-par-élément (D003)

| Élément (discussion b6170b8b) | État dans le dépôt GitHub (fddbe94) | Verdict |
|---|---|---|
| App LEON (`src/components/leon/`, `src/app/page.tsx` orchestrateur) | **ABSENT** — `src/components/` ne contient que `ui/` (squelette shadcn) | DIFFÉRENCE (absence) |
| Couche `src/lib/tsi/` (binary, format, types, midi, edit, catalog) | **ABSENT** — `src/lib/` sans répertoire tsi | DIFFÉRENCE (absence) |
| Couche `src/lib/midi/midi-access.ts` (Web MIDI + handlePortMessage) | **ABSENT** | DIFFÉRENCE (absence) |
| API `src/app/api/projects/*` (CRUD, export, verify) | **ABSENT** — `src/app/api/` squelette | DIFFÉRENCE (absence) |
| `prisma/schema.prisma` (projets) | Squelette par défaut du template | DIFFÉRENCE |
| Catalogue scellé (`reference/*.json` : commands.json 388 cmd / s4mk2-controls.json 125 in + 220 out) | **ABSENT** — équivalent partiel : `data/commandes-traktor.json` du tsi-toolkit Task 39 (**non poussé**, voir §2) | DIFFÉRENCE (recouvrement partiel, formats distincts) |
| Scripts d'extraction/tests (`verif-format-tsi.py`, `test-api-fonctionnel.sh`…) | **ABSENT** | DIFFÉRENCE (absence) |
| Docs (`rapport-validation.md` §1-§16, captures, clone) | **ABSENT** | DIFFÉRENCE (absence) |
| Tableau CC consolidé + catalogue par catégorie (ids vérifiés) | Partiellement couvert par le toolkit Task 39 (non poussé) : presets, karnaugh, commandes-traktor.json | DIFFÉRENCE (recouvrement partiel) |
| Éléments TSI arbitres (tsi-validator, analyse-doc-s4mk2, famille TSI) | **PRÉSENTS** — poussés Tasks 31-37 (v1.2.0 bi-racine, v1.2.0 cohérence) | CONFORME (aucune différence) |
| gen-plan | **v3.31.0** au dépôt vs **v3.32.0** certifié hôte (Task 38, arbitres ALL PASS ×2) | DIFFÉRENCE (version) |

**Bilan : 10 catégories d'éléments de la discussion, 0 présent intégralement au dépôt.** Les livrables Task 39 (tsi-toolkit, tsi-agent.md, construire-zip-tsi.py, bibliotheque-skills-ia, architecture studio v11) existent localement mais **n'ont jamais été poussés** (KO-L009 — push = propriétaire ; aucun push depuis fddbe94).

## 2. Tests de performances $FACON $FACON2 (D004) — exécutés le 2026-11-02

Méthode : 3 exécutions par cible, médiane ; seuils CDC (arbitre 10 s / unitaire 5 s). Cibles = éléments comparables des deux côtés (le dépôt ne porte AUCUN élément applicatif de la discussion — les mesures « côté dépôt » portent donc sur ses arbitres TSI réels).

| Famille | Cible | Médiane | Seuil | rc attendu | Verdict |
|---|---|---|---|---|---|
| dépôt (poussé) | tsi-validator v1.2.0 bi-racine — TSI DREW réel 623 Ko | **0,054 s** | 10 s | 0 (PASS [réel NIXML] — validation positive du format réel) | **PASS** |
| dépôt (poussé) | analyse-doc-s4mk2 pipeline — ZIP DJTT 1,8 Mo | **0,170 s** | 10 s | 0 | **PASS** |
| dépôt (poussé) | analyse-doc-s4mk2 pipeline — ZIP DREW 1,3 Mo | **0,148 s** | 10 s | 1 (idem) | **PASS** |
| discussion/Task 39 (local) | tsi_toolkit nixml — TSI DREW réel (pont DIOM) | **0,035 s** | 5 s | 0 | **PASS** |
| discussion/Task 39 (local) | tsi_toolkit convertisseurs — DREW → JSON | **0,038 s** | 5 s | 0 | **PASS** |
| discussion/Task 39 (local) | tsi_toolkit studio — scénario DSL complet | **0,038 s** | 5 s | 0 | **PASS** |

**VERDICT : PASS 6/6** — tous les éléments comparables des deux côtés sont fonctionnels et performants (médianes 0,037-0,174 s, 2 ordres de grandeur sous les seuils). Harnais documenté de la discussion (idempotence 12/12, API 15/15, ESLint 0, tsc 0) : non rejouable tel quel côté dépôt (les fichiers n'y existent pas) → re-certification prévue après régénération (G4).

**Note correct-work (exécution Task 40)** : la 1ʳᵉ passe de mesure a fait tourner un valider-tsi.py v1.0.0 reliquat (recyclage sandbox — rc=1 pour cause de format non reconnu, sémantique erronée) au lieu de la v1.2.0 bi-racine certifiée ; divergence détectée par byte-comparaison hôte↔dépôt (89/115 skills divergents), résorbée par sync complète dépôt→hôte (l'état poussé = état certifié), PUIS re-mesure v1.2.0 : PASS [réel NIXML] rc=0, 0,054 s. Les chiffres ci-dessus sont les chiffres post-correctif.

## 3. Conclusion — différences → génération $FACON (D006/D007)

1. **L'applicative LEON (toutes couches) est absente du dépôt** → régénérer $FACON la version la plus cohérente, optimisée et fonctionnelle : **Extension React du studio v11** (G3) — l'app LEON reconstruite en consommant le studio v11/toolkit comme moteur (R4 : jamais dupliquer le format TSI — pont vers la toolchain), préservation des correctifs critiques documentés (§3 du rapport d'analyse : onMessage/handlePortMessage, jalon tsc, contrats API).
2. **Les livrables Task 39 ne sont pas poussés** → intégration byte-identique au dépôt (G2) : tsi-toolkit, tsi-agent.md, construire-zip-tsi.py, bibliotheque-skills-ia, architecture-mapping-studio-v11.md, rapports.
3. **gen-plan v3.32.0 non poussé** → intégration de la montée certifiée Task 38 (G2).
4. **Catalogue** : la discussion (388 commandes / 125 in + 220 out, format app) et le toolkit (393 commandes / 163 contrôles, format toolchain) se recouvrent partiellement → réconciliation $FACON : le catalogue de l'app consomme la source scellée toolkit (source de vérité partagée), l'écart 388↔393 est analysé (catégories vs commandes, périmètres distincts) — G2.
5. Les arbitres du dépôt sont conformes et rapides — aucun correctif requis de ce côté.
