#!/usr/bin/env python3
"""Création de PROMPT-MAITRE-GEN-PLAN-v3.11.0.md depuis v3.10.0 (diffs chirurgicaux).

Intégration PEK v4.1 (session B1) :
  1. En-tête : version skill 3.10.0 → 3.11.0, prompt 1.5.0 → 1.5.1, date 2026-09-10
  2. §1.9 : ajout du paragraphe « Méthode de raisonnement adaptative PEK »
  3. §2.2 : 6e référence dans la structure des fichiers
  4. §7 : entrée d'historique v3.11.0
  5. §9.6 : contenu in extenso de references/prompt-engineering-kit.md
Conventions respectées : R1-R6 (idempotence), SHARED §3.2 règle 5 (planchers inchangés),
description frontmatter inchangée (non-régression triggers 9/9).
"""

import os

BASE = "/home/z/my-project/skills/@mon-ecosysteme"
SRC = os.path.join(BASE, "PROMPT-MAITRE-GEN-PLAN-v3.10.0.md")
DST = os.path.join(BASE, "PROMPT-MAITRE-GEN-PLAN-v3.11.0.md")
REF = "/home/z/my-project/skills/gen-plan/references/prompt-engineering-kit.md"

with open(SRC, encoding="utf-8") as f:
    content = f.read()
with open(REF, encoding="utf-8") as f:
    ref_content = f.read().rstrip("\n")

assert "```" not in ref_content, "La référence contient des fences — embedding à revoir"

# ---- 1. En-tête ----
content = content.replace(
    "# PROMPT MAÎTRE — Installation du skill gen-plan v3.10.0",
    "# PROMPT MAÎTRE — Installation du skill gen-plan v3.11.0", 1)
content = content.replace("> **Version du prompt** : 1.5.0",
                          "> **Version du prompt** : 1.5.1", 1)
content = content.replace("> **Skill cible** : gen-plan v3.10.0",
                          "> **Skill cible** : gen-plan v3.11.0", 1)
content = content.replace("> **Date** : 2026-09-07",
                          "> **Date** : 2026-09-10", 1)

# ---- 2. §1.9 : paragraphe PEK (inséré avant le séparateur qui précède §1.10) ----
pek_para = (
    "**Méthode de raisonnement adaptative PEK (v3.11.0, session B1)** : gen-plan mobilise "
    "le Prompt Engineering Kit v4.1 (méthode pure) comme couche de raisonnement opérationnelle "
    "de la méthode-mère — 3 modes d'exécution (CoT 7 étapes / Chaining 4 étapes / Hybride à "
    "bascule automatique selon la complexité détectée à E1-E3) alignés sur la philosophie "
    "§1.7 #6 (« CoT + Chaining avec auto-correction ») et calibrés par les profils §2.4 ; "
    "blocs de sortie adaptatifs A-J mappés sur la classification Type 1-4 (E3) ; 9 règles "
    "critiques et 12 checks de validation (scoring 25 pts, seuil 22/25) intégrés aux hooks "
    "correct-work par phase (E9-E14). Contenu opérationnel : "
    "`references/prompt-engineering-kit.md` (in extenso §9.6). Provenance : PEK "
    "v4.1-META-PROMPT-EDITED (upload utilisateur 2026-09-10), intégrée par assemblage — "
    "modules d'implémentation web écartés (règle zéro : skill auto-contenu, zéro dépendance "
    "d'infrastructure).\n\n"
)
anchor_1_10 = "---\n\n### §1.10 Pipeline d'optimisation écosystème (Z0-Z6)"
assert anchor_1_10 in content, "ancre §1.10 introuvable"
content = content.replace(anchor_1_10, pek_para + anchor_1_10, 1)

# ---- 3. §2.2 : 6e référence ----
old_struct = (
    "│   ├── profils-ressource.md          # NORMAL / ECO / VIEUX PC\n"
    "│   └── guide-selection-agent-skill.md # Arbre de décision + tableau\n"
)
new_struct = (
    "│   ├── profils-ressource.md          # NORMAL / ECO / VIEUX PC\n"
    "│   ├── guide-selection-agent-skill.md # Arbre de décision + tableau\n"
    "│   └── prompt-engineering-kit.md     # PEK v4.1 — raisonnement adaptatif (CoT/Chaining/Hybride, blocs A-J, 9 règles, 12 checks)\n"
)
assert old_struct in content, "ancre §2.2 introuvable"
content = content.replace(old_struct, new_struct, 1)

# ---- 4. §7 : historique v3.11.0 ----
hist_row = (
    "| v3.10.0 | 2026-09-07 | Gestion du plan d'actions de session (directive utilisateur, session A12) : "
)
assert hist_row in content
# Insérer la ligne v3.11.0 après la ligne v3.10.0 complète (fin de ligne avant la révision documentaire)
anchor_hist = (
    "planchers de dépendances inchangés (SHARED §3.2 règle 5) |\n\n"
    "Révision documentaire 2026-09-06"
)
new_hist = (
    "planchers de dépendances inchangés (SHARED §3.2 règle 5) |\n"
    "| v3.11.0 | 2026-09-10 | Intégration du Prompt Engineering Kit v4.1 (directive utilisateur, session B1) : "
    "couche de raisonnement adaptative — 3 modes d'exécution (CoT 7 étapes / Chaining 4 étapes / Hybride, "
    "bascule selon complexité E1-E3, calibrage profils §2.4), blocs de sortie adaptatifs A-J mappés sur les "
    "Types 1-4 (E3), 9 règles critiques, 12 checks + scoring 25 pts (seuil 22/25) alignés sur les hooks "
    "correct-work E9-E14 ; §1.9 enrichi de l'orchestration PEK ; 6e référence "
    "`references/prompt-engineering-kit.md` (in extenso §9.6) ; §2.2 actualisée. Description frontmatter "
    "inchangée (non-régression triggers 9/9) ; aucun changement de contrat d'intégration : planchers de "
    "dépendances inchangés (SHARED §3.2 règle 5) |\n\n"
    "Révision documentaire 2026-09-06"
)
assert anchor_hist in content, "ancre §7 introuvable"
content = content.replace(anchor_hist, new_hist, 1)

# ---- 5. §9.6 : contenu in extenso ----
if not content.endswith("\n"):
    content += "\n"
content += (
    "\n### §9.6 `references/prompt-engineering-kit.md`\n\n"
    "```markdown\n" + ref_content + "\n```\n"
)

with open(DST, "w", encoding="utf-8") as f:
    f.write(content)

src_lines = content.count("\n")
print(f"OK : {DST}")
print(f"Lignes : {src_lines} (source v3.10.0 : 1106)")
print(f"Référence embarquée §9.6 : {ref_content.count(chr(10)) + 1} lignes")
for token in ["v3.11.0", "Méthode de raisonnement adaptative PEK",
              "prompt-engineering-kit.md", "§9.6"]:
    assert token in content, f"token manquant : {token}"
print("Vérifications internes : OK")
