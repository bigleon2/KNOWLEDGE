#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.12)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

"""Task 20 (D012) — tenue du registre alias via délégation alias-eco (correct-work v2.8.0 §10.1).

Relevé de la session : 1 usage propriétaire de l'alias $ECO-LEON
(« gen-plan : "test si l'installation de $ECO-LEON est performante" »).
Incrément du compteur d'usage cumulé de l'entrée ECO-LEON elle-même
(honnêteté : on trace l'usage de l'ALIAS sur son entrée, on n'inflate pas
le compteur de la phrase littérale). Registres dépôt + hôte maintenus
byte-identiques. Validation post-écriture : trié + dédupliqué strict.
"""
import json

CHEMINS = [
    "/home/z/my-project/KNOWLEDGE-repo/skills/@historique/@Alias/aliases.json",
    "/home/z/my-project/skills/@historique/@Alias/aliases.json",
]

blobs = []
for chemin in CHEMINS:
    with open(chemin, encoding="utf-8") as f:
        blobs.append(f.read())

if len(set(blobs)) != 1:
    raise SystemExit("ABANDON : registres dépôt/hôte divergents avant écriture")

reg = json.loads(blobs[0])
touches = 0
for p in reg.get("phrases", []):
    if p.get("alias") == "ECO-LEON":
        p["occurrences_cumulees"] = p.get("occurrences_cumulees", 0) + 1
        p["derniere_detection"] = "2026-10-23"
        touches += 1
if touches != 1:
    raise SystemExit(f"ABANDON : entrée ECO-LEON touchée {touches} fois (attendu 1)")

phrases = [p.get("phrase") for p in reg["phrases"]]
assert phrases == sorted(phrases), "registre non trié après édition"
assert len(phrases) == len(set(phrases)), "doublon strict après édition"
reg["mis_a_jour"] = "2026-10-23"

sortie = json.dumps(reg, ensure_ascii=False, indent=2) + "\n"
for chemin in CHEMINS:
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(sortie)

print("Registre tenu : ECO-LEON occurrences_cumulees +1 (usage session Task 20) ; "
      f"{len(phrases)} phrases, trié, dédupliqué — dépôt et hôte byte-identiques.")
