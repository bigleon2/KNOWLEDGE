#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.9)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""
Task 47 — D3 : Génération du PM iphone19-photos.md v0.9.0 [ANTICIPÉE] + skill skills/iphone19/.
Migration ANTICIPÉE depuis skills/@photos/iphone18-photos.md v1.0 (source INTACTE — R2).
Procédure : PM iphone-photos-migration.md — Phases 4 (génération) + 5 (auto-audit A1-A8 + blocs intangibles).
Chaque remplacement est chirurgical (assertion count==1) ; les blocs intangibles sont vérifiés byte-identiques.
"""
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import task47_migration_blocks as B
import task47_skill_iphone19_assets as A

SRC = "/home/z/my-project/skills/@photos/iphone18-photos.md"
PM_OUT = "/home/z/my-project/skills/@photos/iphone19-photos.md"
SKILL_DIR = "/home/z/my-project/skills/iphone19"
RAPPORT = "/home/z/my-project/scripts/task47-migration-audit.json"

src = open(SRC, encoding="utf-8").read()
out = src
journal = []


def remplacer(old, new, label, attendu=1):
    global out
    n = out.count(old)
    assert n == attendu, f"[{label}] occurrences={n} attendu={attendu} — ABANDON (édition non chirurgicale)"
    out = out.replace(old, new)
    journal.append({"label": label, "occurrences": n, "octets_old": len(old), "octets_new": len(new)})


def bloc(start, end, new, label):
    """Remplace le bloc [start..fin de end] (inclus) par new — start et end uniques."""
    global out
    assert out.count(start) == 1, f"[{label}] marqueur start non unique"
    assert out.count(end) == 1, f"[{label}] marqueur end non unique"
    i = out.index(start)
    j = out.index(end, i) + len(end)
    old_bloc = out[i:j]
    out = out[:i] + new + out[j:]
    journal.append({"label": label, "octets_old": len(old_bloc), "octets_new": len(new)})


# ============ PHASE 4 — GÉNÉRATION (remplacements chirurgicaux) ============
remplacer("# 📱 iphone18-photos.md", B.TITRE_DOC, "titre document")
remplacer("## PROMPT MAÎTRE — Pipeline d'amélioration photo « iPhone 18 Pro Max, qualité max » + rendus d'époques + posters",
          B.TITRE_PM, "titre PM")
remplacer("**Version 1.0 — Langue : français — Mode : data-driven (Analyse → Décision → Plan → Exécution → QC → Question utilisateur)**",
          B.VERSION, "version")
remplacer("> **Origine v1.0 (reset de version — prompt maître `iphone-photos-migration.md` §6-1) :** document généré par migration depuis `iphone17-photos.md` v2.0 le 2026-10-09, à l'activation de la règle §6.10 de cette dernière (génération iPhone 18 confirmée par Apple le 9/9/2026).",
          B.ORIGINE, "origine")
bloc("### Changelog `iphone17-photos.md` v2.0 → `iphone18-photos.md` v1.0",
     "règle 14 maintenue et généralisée au squelette `iphone19`.**",
     B.CHANGELOG, "changelog")
remplacer("(cible : **iPhone 18 Pro Max, réglages photo au maximum**)", B.CIBLE_S0, "cible §0")
bloc("**Contexte matériel de référence** (ancrage v1.0) :",
     "hors périmètre de rendu.)*",
     B.CONTEXTE_MATERIEL, "contexte matériel §0")
remplacer("14. **ÉLÉMENTS SPÉCULATIFS** : toute section taggée `[SPÉCULATIF]` (ex. §6.10 — squelette `iphone19`) est **inactive**",
          "14. **ÉLÉMENTS SPÉCULATIFS** : toute section taggée `[SPÉCULATIF]` (ex. §6.10 — squelette `iphone20`) est **inactive**",
          "règle 14 — squelette iphone20")
remplacer("(défaut = `iphone18_max`)", "(défaut = `iphone19_max`)", "C3 défaut preset")
remplacer("| R13 | C2 = ère ancienne ET C3 = iphone18_max |",
          "| R13 | C2 = ère ancienne ET C3 = iphone19_max |", "R13 preset")
remplacer("rendu_cible: iphone18_max | preset_<epoque>", "rendu_cible: iphone19_max | preset_<epoque>", "§3 rendu_cible")
bloc("### 6.1 `iphone18_max` (défaut — ancrage matériel iPhone 18 Pro Max)",
     "ne sont pas simulées.)*",
     B.SECTION_61, "§6.1 preset défaut")
remplacer("(source ancienne → `iphone18_max`)", "(source ancienne → `iphone19_max`)", "§6.5 restauration")
remplacer("- Simulation du rendu **caméra frontale iPhone 18 Pro Max** (18 MP, ƒ/1.9, Center Stage — caractéristiques inchangées vs génération 17) : recadrage **carré 1:1** centré sur le(s) sujet(s) (bbox visages/corps, adaptatif façon Center Stage), rendu grand-angle frontal léger, piqué doux optimisé visage, exposition prioritaire aux visages.",
          B.SECTION_69, "§6.9 frontale")
bloc("### 6.10 `iphone19` — **[SPÉCULATIF] — SECTION INACTIVE**",
     "a produit le présent document (migration exécutée le 2026-10-09).",
     B.SECTION_610, "§6.10 squelette iphone20")
remplacer("Critère QC 12 = nouveau, sans effet rétroactif ; règle 14 maintenue et généralisée au squelette `iphone19`.",
          "Critère QC 12 = nouveau, sans effet rétroactif ; règle 14 maintenue et généralisée au squelette `iphone19`.\n\n" + B.NOTE_RETRO_090,
          "§11 note rétroactive v0.9.0 (insertion)")
bloc("## §12 — LIVRABLES DU PROJET",
     "consolidés dans `crop_utils.py`.",
     B.SECTION_12, "§12 livrables")
remplacer("| `preset:<nom> [params]` | Exécute un preset §6 sur l'image courante (mode série §10 si plusieurs sorties) — y compris `log2_cinema`, `frontal_center_stage` ; `preset:iphone18` / `preset:iphone18_max` → preset par défaut (§6.1) ; **`preset:iphone19` → refus, section inactive (règle 14)** |",
          B.LIGNE_PRESET_13, "§13 preset row")

# ============ PHASE 5 — AUTO-AUDIT ============
audit = {"remplacements": journal, "controles": []}
ok_all = True


def check(nom, cond, detail=""):
    global ok_all
    audit["controles"].append({"nom": nom, "verdict": "OK" if cond else "KO", "detail": detail})
    if not cond:
        ok_all = False
    print(f"  [{'OK' if cond else 'KO'}] {nom}" + (f" — {detail}" if detail else ""))


def extrait(t, start, end):
    assert t.count(start) == 1 and t.count(end) == 1, f"marqueurs non uniques: {start[:40]}"
    i = t.index(start)
    j = t.index(end, i) + len(end)
    return t[i:j]


print("=== Phase 5 — Auto-audit (protocole §11 + A1-A8) ===")

# Blocs intangibles byte-identiques source → sortie
INTANGIBLES = [
    ("Règles absolues 1-13", "1. **Aucun traitement sans analyse préalable** (§1).",
     "déclarée dans le plan (`sortie_nom`, §3) et listée dans §12."),
    ("§1 grille A (axe technique)", "### A. Axe technique", "| A10 | Dégâts physiques (rayures, poussières, déchirures, plis — scans) |"),
    ("§1 grille B (axe sémantique)", "### B. Axe sémantique", "**zéro élément ajouté** |"),
    ("§1 C1-C2", "| C1 | Support probable", "| C2 | Ère / décennie estimée |"),
    ("§2 R1-R12", "| R1 | A5 ≥ 2 |", "| R12 | C3 = variation | Variation température/luminosité/format (§6.2–6.4) | P7/P8 |"),
    ("§2 R14-R18", "| R14 | C3 = poster/print", "rendu computationnel, pas une optique physique.** | P5/P6 |"),
    ("§2 garde-fous G1-G7", "**Garde-fous (toujours actifs) :**", "attendre la demande explicite de l'utilisateur (§9)."),
    ("§4 pipeline P0-P9", "| P0 | Référence |", "export qualité max |"),
    ("§5 QC 1-12 + itération + note v1.4", "1. Visages naturels, identité préservée (G1)",
     "elle aurait déclenché un KO fidélité → rejeu P4."),
    ("§6.2-6.8 presets", "### 6.2 Température", "le profil modifie la **réponse tonale**, jamais le contenu.",
     "rename_s65"),
    ("§7 intégration opérationnelle", "- Traduire le PLAN-ACTIONS en appels `image_edit`",
     "img = export_print(crop_ratio(img, 210/297, cx=0.5), 210, 297)   # poster A4 300 DPI\n```"),
    ("§8 gabarit rapport", "## 📋 Analyse (scores ANALYSE-v2", "## ❓ Souhaitez-vous des modifications ? (question OBLIGATOIRE — §9)"),
    ("§9 mode interaction", "1. Après livraison + rapport → **question obligatoire**", "puis question reposée."),
    ("§10 mode série", "1. Parser les sorties demandées", "4. **Question obligatoire posée une seule fois à la fin** (§9)."),
    ("§11 a-f + notes rétroactives v2.0/v1.0", "a) Références croisées §/R/G cohérentes",
     "Critère QC 12 = nouveau, sans effet rétroactif ; règle 14 maintenue et généralisée au squelette `iphone19`."),
    ("§13 lignes non-preset", "| `gen-plan:<spec>` |", "| tout autre message | Demande normale → pipeline complet (§1→§9) |",
     "replace_preset13"),
]
for item in INTANGIBLES:
    nom, s, e = item[0], item[1], item[2]
    mode = item[3] if len(item) > 3 else None
    try:
        b_src, b_out = extrait(src, s, e), extrait(out, s, e)
        if mode == "rename_s65":
            cond = b_out == b_src.replace("(source ancienne → `iphone18_max`)", "(source ancienne → `iphone19_max`)")
        elif mode == "replace_preset13":
            src13 = "| `preset:<nom> [params]` | Exécute un preset §6 sur l'image courante (mode série §10 si plusieurs sorties) — y compris `log2_cinema`, `frontal_center_stage` ; `preset:iphone18` / `preset:iphone18_max` → preset par défaut (§6.1) ; **`preset:iphone19` → refus, section inactive (règle 14)** |"
            cond = b_out == b_src.replace(src13, B.LIGNE_PRESET_13)
        else:
            cond = b_src == b_out
        check(f"INTANGIBLE {nom}", cond, f"{len(b_src)} octets" + (" (delta contrôlé)" if mode else ""))
    except AssertionError as err:
        check(f"INTANGIBLE {nom}", False, str(err)[:80])

# Blocs à delta contrôlé (renommage preset unique)
r13_src = extrait(src, "| R13 | C2 = ère ancienne", "| P1–P6 |")
r13_out = extrait(out, "| R13 | C2 = ère ancienne", "| P1–P6 |")
check("R13 = renommage preset seul (contrainte 5.2)", r13_out == r13_src.replace("iphone18_max", "iphone19_max"))
y_src = extrait(src, "plan_id: PA-<date>-<seq>", 'modifications_demandees: "aucune — attente de la demande utilisateur après livraison (G7)"')
y_out = extrait(out, "plan_id: PA-<date>-<seq>", 'modifications_demandees: "aucune — attente de la demande utilisateur après livraison (G7)"')
check("§3 YAML = renommage rendu_cible seul", y_out == y_src.replace("rendu_cible: iphone18_max", "rendu_cible: iphone19_max"))

# A1 — références croisées
check("A1a iphone19_max présent C3/R13/§3/§6.1/§6.5",
      all(m in out for m in ["(défaut = `iphone19_max`)", "C3 = iphone19_max",
                             "rendu_cible: iphone19_max", "### 6.1 `iphone19_max`", "(source ancienne → `iphone19_max`)"]))
check("A1b iphone20 (règle 14/§6.10/§13)", all(m in out for m in ["squelette `iphone20`", "### 6.10 `iphone20`", "`preset:iphone20` → refus"]))

# A2 — numérotation continue
secs = [f"## §{i} —" in out for i in range(14)]
check("A2a sections §0→§13 présentes", all(secs), f"{sum(secs)}/14")
regles = [f"| R{i} |" in out or f"| **R{i}** |" in out for i in range(1, 19)]
check("A2b règles R1→R18 (ni plus ni moins)", all(regles) and "| R19 |" not in out and "| **R19** |" not in out)
check("A2c garde-fous G1→G7", all(f"**G{i}**" in out for i in range(1, 8)))
check("A2d critères QC 1→12", all(f"\n{i}. " in ("\n" + extrait(out, "1. Visages naturels", "elle aurait déclenché un KO fidélité → rejeu P4.")) for i in range(1, 13)))

# A3 — champs YAML
check("A3 champs YAML §3", all(f in out for f in ["focale_cible:", "ouverture_cible:", "rendu_cible:", "sortie_nom:", "regles_declenchees:"]))

# A4 — aucune règle R19 fonctionnelle (mentions documentaires de son ABSENCE autorisées)
lignes_r19 = [l for l in out.splitlines() if "R19" in l]
check("A4 aucune règle R19 fonctionnelle",
      "| R19 |" not in out and "| **R19** |" not in out
      and all(("nouvelles règles R19+" in l) or ("aucune règle R19" in l) or ("Aucune règle R19" in l) for l in lignes_r19),
      f"{len(lignes_r19)} lignes mentionnant R19 (toutes documentaires)")

# A5 — preset renommé partout (occurrences résiduelles iphone18_max uniquement documentaires)
n_res = out.count("iphone18_max")
check("A5 résidus iphone18_max documentaires uniquement", n_res == 5,
      f"{n_res} occurrences (2 changelog + 1 baseline §6.1 + 1 note §11 v0.9.0 + 1 §13)")

# A6 — G1-G7 + B6 intacts (déjà couverts INTANGIBLES grille B + garde-fous) + tag [ANTICIPÉE]
check("A6a statut ANTICIPÉ visible (version/§0/§6.1)",
      all(m in out for m in ["Version 0.9.0 [ANTICIPÉE]", "génération ANTICIPÉE 2027", "ancrage matériel ANTICIPÉ"]))
check("A6b tags honnêteté [RUMEUR]/[NON VÉRIFIÉ]/[SPÉCULATIF]",
      all(m in out for m in ["[RUMEUR", "[NON VÉRIFIÉ", "[SPÉCULATIF]"]))

# A7 — intégrations tracées (12 lignes de zone au changelog)
chlog = extrait(out, "### Changelog `iphone18-photos.md`", "Écarts vs migration standard")
n_chlog = sum(1 for l in chlog.splitlines() if l.startswith("|") and not l.startswith("| Zone") and not l.startswith("|---"))
check("A7 changelog 12 lignes de zone", n_chlog == 12, f"{n_chlog} lignes zone")

# A8 — squelettes taggés
check("A8 §6.10 INACTIVE + règle 14", "**[SPÉCULATIF] — SECTION INACTIVE**" in out and "SECTION INACTIVE**" in out)

# ============ ÉCRITURE DES LIVRABLES ============
os.makedirs(os.path.dirname(PM_OUT), exist_ok=True)
with open(PM_OUT, "w", encoding="utf-8") as f:
    f.write(out)

os.makedirs(SKILL_DIR, exist_ok=True)
os.makedirs(os.path.join(SKILL_DIR, "scripts"), exist_ok=True)
os.makedirs(os.path.join(SKILL_DIR, "evals"), exist_ok=True)

# SKILL.md = frontmatter/contexte/lignage + corps PM VERBATIM (depuis « ## PROMPT MAÎTRE »)
corps_pm = out[out.index("## PROMPT MAÎTRE"):]
with open(os.path.join(SKILL_DIR, "SKILL.md"), "w", encoding="utf-8") as f:
    f.write(A.FRONTMATTER + "\n" + corps_pm)
check("SKILL.md corps PM VERBATIM (R2)", corps_pm in open(os.path.join(SKILL_DIR, "SKILL.md"), encoding="utf-8").read())

shutil.copy2("/home/z/my-project/skills/iphone18/scripts/editer-image.mjs",
             os.path.join(SKILL_DIR, "scripts", "editer-image.mjs"))
with open(os.path.join(SKILL_DIR, "evals", "evals.json"), "w", encoding="utf-8") as f:
    json.dump(A.EVALS, f, ensure_ascii=False, indent=2)
with open(os.path.join(SKILL_DIR, "evals", "trigger_evals.json"), "w", encoding="utf-8") as f:
    json.dump(A.TRIGGER_EVALS, f, ensure_ascii=False, indent=2)

audit["verdict"] = "PASS 100%" if ok_all else "KO — corriger et rejouer"
audit["fichiers"] = {"pm": PM_OUT, "skill": os.path.join(SKILL_DIR, "SKILL.md"),
                     "lignes_pm": out.count("\n") + 1, "octets_pm": len(out)}
with open(RAPPORT, "w", encoding="utf-8") as f:
    json.dump(audit, f, ensure_ascii=False, indent=2)
print(f"\nVerdict auto-audit : {audit['verdict']}")
print(f"PM : {PM_OUT} ({audit['fichiers']['lignes_pm']} lignes)")
print(f"Rapport : {RAPPORT}")
sys.exit(0 if ok_all else 1)
