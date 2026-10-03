#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Task 21 — campagne P4 : résorption des incohérences agents/skills (constats A1-A7 du
rapport Task 19, recommandations R2/R4/R5) — corpus VIVANT uniquement (PMs figés et
entrées historiques intouchés, R2).

- A1 : memory-engineering §7 — référence vive « gen-plan v3.15.0 §1.9 » → « gen-plan
  v3.18.0 §1.9 (PM) / §1.6 (SKILL.md) ». L'entrée §6 (historique v1.0.0, N34) reste
  légitime et n'est PAS touchée.
- A2 (option libellés — décision D2x consignée) : les 3 descriptions n°54 affirment
  « source de vérité : SHARED §7 » alors que leur registre effectif est §8 local + KB ;
  KB « Dépend de » de gen-plan : « détention §1.9 (intégration v3.15.0 — version perdue) »
  → « détention orchestrée — registre décentralisé §8 + registre KB ».
- A7 : qualification des références « §1.9 » (numérotation du PM uniquement — le SKILL.md
  gen-plan saute §1.8→§1.14) : « gen-plan (§1.9 » → « gen-plan (PM §1.9 ».
- A6 : clone-chat — double §0 (le second devient §0bis) ; « mention 80 skills » →
  corpus réel recalibré.
- A3 : en-têtes « Contexte Système (SHARED vX) » des 26 SKILL.md + PMs vivants → v1.6.4
  (sync mécanique KO-L004 ; PMs figés exclus).
- A4 : en-tête courant profils-ressource.md « gen-plan v3.7.0 » → v3.18.0 (les mentions
  « intégré phase N20 (v3.13.0) » des patterns sont des historiques légitimes — intactes).
"""
import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SKILLS = BASE / "skills"
KB = SKILLS / "KNOWLEDGE.md"
SHARED_VERSION = "1.6.4"
GENPLAN_VERSION = "3.18.0"
REPORT = {"edits": [], "notes": []}

N54 = ["fleet-engineering", "spec-driven-development", "memory-engineering"]


def note(msg):
    REPORT["edits"].append(msg)
    print("  ·", msg)


def edit_file(path, transforms, label):
    text = path.read_text(encoding="utf-8")
    orig = text
    for pat, repl in transforms:
        if re.search(pat, text):
            text = re.sub(pat, repl, text)
            note(f"{label} : « {pat[:58]}… » appliqué")
        else:
            REPORT["notes"].append(f"{label} : motif introuvable « {pat[:58]} »")
            print(f"  ⚠ {label} : motif introuvable « {pat[:58]} »")
    if text != orig:
        path.write_text(text, encoding="utf-8")
    return text != orig


print("=== A1 — memory-engineering §7 (référence vive) ===")
edit_file(
    SKILLS / "memory-engineering" / "SKILL.md",
    [(r"- gen-plan v3\.15\.0 §1\.9 — routage autonome",
      f"- gen-plan v{GENPLAN_VERSION} §1.9 (PM) / §1.6 (SKILL.md) — routage autonome")],
    "A1 memory-engineering",
)

print("=== A2 — descriptions n°54 (libellé registre effectif) + KB gen-plan ===")
for skill in N54:
    edit_file(
        SKILLS / skill / "SKILL.md",
        [(r"source\s+de\s+vérité\s*:\s*SHARED\s+§7", "registre décentralisé : §8 local + registre KB")],
        f"A2 {skill}",
    )
kb_text = KB.read_text(encoding="utf-8")
for skill in N54:
    kb_text, n = re.subn(
        rf"({re.escape(skill)} \(détention) §1\.9[^)]*\)",
        r"\1 orchestrée — registre décentralisé §8 du skill + registre KB)",
        kb_text, count=1)
    note(f"A2 KB gen-plan « Dépend de » {skill} : libellé détention orchestrée ({n})")
KB.write_text(kb_text, encoding="utf-8")

print("=== A7 — qualification des références §1.9 (3 skills n°54) ===")
for skill in N54:
    edit_file(
        SKILLS / skill / "SKILL.md",
        [
            (r"gen-plan \(§1\.9", "gen-plan (PM §1.9"),
            (r"`gen-plan` §1\.9", "`gen-plan` PM §1.9"),
        ],
        f"A7 {skill}",
    )

print("=== A6 — clone-chat (double §0 + 80 skills) ===")
edit_file(
    SKILLS / "clone-chat" / "SKILL.md",
    [
        (r"## §0 — RÈGLE ZÉRO \(résumé de SHARED §0\)", "## §0bis — Règle zéro (résumé de SHARED §0)"),
        (r"mention 80 skills", "mention du corpus de skills (nombre réel courant, recalibré)"),
    ],
    "A6 clone-chat",
)

print("=== A3 — en-têtes §0 SHARED sync v1.6.4 (SKILL.md + PMs vivants) ===")
n_sync = 0
for sdir in sorted(SKILLS.iterdir()):
    sp = sdir / "SKILL.md"
    if not sdir.is_dir() or sdir.name.startswith(("_", ".")) or sdir.name == "@mon-ecosysteme" or not sp.exists():
        continue
    text = sp.read_text(encoding="utf-8")
    new = re.sub(r"Contexte Système \(SHARED v[0-9.]+\)",
                 f"Contexte Système (SHARED v{SHARED_VERSION})", text)
    if new != text:
        sp.write_text(new, encoding="utf-8")
        n_sync += 1
note(f"A3 : {n_sync} SKILL.md en-têtes §0 synchronisés v{SHARED_VERSION}")
for pm in ["PROMPT-MAITRE-CORRECT-WORK-v2.7.0.md", "PROMPT-MAITRE-GEN-PLAN-v3.18.0.md",
           "PROMPT-MAITRE-INSTALL-ECOSYSTEME.md", "PROMPT-ULTRA-MAITRE-ORCHESTRATION.md",
           "SYNC-CONTEXT.md"]:
    pp = SKILLS / "@mon-ecosysteme" / pm
    if pp.exists():
        text = pp.read_text(encoding="utf-8")
        # sync UNIQUEMENT les en-têtes d'extrait de contexte vivant (pas l'historique §6/§7)
        new2 = re.sub(r"(CONTEXTE SYSTÈME \(Extrait SHARED v|Contexte Système \(SHARED v)[0-9.]+",
                      lambda m: m.group(1) + SHARED_VERSION, text)
        if new2 != text:
            pp.write_text(new2, encoding="utf-8")
            note(f"A3 PM vivant synchronisé : {pm}")

print("=== A4 — en-tête courant profils-ressource.md ===")
edit_file(
    SKILLS / "gen-plan" / "references" / "profils-ressource.md",
    [(r"# Profils ressource — gen-plan v3\.7\.0", f"# Profils ressource — gen-plan v{GENPLAN_VERSION}")],
    "A4 profils-ressource",
)

out = BASE / "scripts" / "task21-p4-agents-report.json"
out.write_text(json.dumps(REPORT, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nRapport : {out} — {len(REPORT['edits'])} éditions, {len(REPORT['notes'])} notes")
