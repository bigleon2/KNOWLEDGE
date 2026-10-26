# Grille de relecture de script — script-reviewer v1.0.0

Référence détaillée des 8 checks (§1.2 du SKILL.md) et du modèle de rapport.

## G1 — Syntaxe Python valide

- Preuve : `py_compile.compile(path, doraise=True)` sans exception.
- S1 si échec : le script n'est même pas exécutable ; correction côté script-creator.

## G2 — Stdlib uniquement (N3)

- Preuve : scan des lignes `import X` / `from X import` ; la liste blanche est la
  stdlib Python 3 (json, re, sys, hashlib, zipfile, pathlib, subprocess, os, …).
- S1 si une dépendance externe (pip) n'est pas explicitement justifiée dans la
  docstring d'intention.

## G3 — Docstring d'intention + sortie JSON déterministe

- Preuve : docstring en tête de fichier (intention, entrées/sorties) ; présence de
  `json.dumps(..., ensure_ascii=False)` pour les sorties machine.
- S2 si sortie machine non déterministe (horodatage brut, ordre non trié sans
  justification, texte libre non structuré).

## G4 — Code de retour explicite

- Preuve : `sys.exit(0)` en succès, codes non nuls documentés en échec.
- S2 si le processus se termine sans code explicite (ambiguïté pour les harnais).

## G5 — Idempotence ×2

- Preuve : deux exécutions consécutives, comparaison stricte des sorties (stdout)
  ou des hachages d'artefacts produits.
- S1 pour un arbitre de vérification non idempotent (le verdict doit être une
  fonction pure de l'état audités — esprit L003).

## G6 — Persistance R9 + nommage

- Preuve : le fichier vit sous `scripts/` à la racine du projet ; nom kebab-case
  descriptif (outils durables) ou préfixe de session `nXX-…` (arbitres de session).
- S3 si inline historique non persisté ou nommage hors convention.

## G7 — Traçabilité

- Preuve : une entrée worklog correspondante existe (recherche `Task ID` + nom du
  script) — règle d'or n°1 : jamais d'édition silencieuse.
- S2 si le script est livré sans trace de session.

## G8 — Auto-test des cas limites (P2)

- Preuve : pour les arbitres génériques, les cas limites connus (entrées vides,
  fences complets, multi-lignes, racine absente) sont embarqués dans l'auto-test.
- n/a justifié pour les outils one-shot sans logique générique.

## Modèle de rapport de relecture (§2.4)

```markdown
# Rapport de relecture — <nom-du-script>

## Métadonnées
- **Date** : YYYY-MM-DD
- **Grille** : script-reviewer v1.0.0 (G1-G8)
- **Cible** : scripts/<nom>.py

## Résultats
| Check | Statut | Preuve |
|-------|--------|--------|
| G1 … | PASS/FAIL/n/a | … |

## Sévérités
- S1 : — / S2 : — / S3 : — / S4 : —

## Verdict
**PASS** | **PASS AVEC RÉSERVES** | **FAIL**
Escalade : — (correct-work mode CIBLE si FAIL)
```
