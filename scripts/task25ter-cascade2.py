#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.13)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

"""Cascade KO-L004 Task 25ter — reliquat : SYNC-CONTEXT v1.5.3, README v2.1.11,
historique-autres-elements.md ×4 (les édits PMI/KB/journal sont déjà appliqués)."""
import re

REPO = "/home/z/my-project/KNOWLEDGE-repo"
done = []

# ── 4. SYNC-CONTEXT v1.5.3 ──────────────────────────────────────────
SC = f"{REPO}/skills/@mon-ecosysteme/SYNC-CONTEXT.md"
sc = open(SC, encoding="utf-8").read()
if "Révision v1.5.3" in sc:
    done.append("SYNC (déjà appliqué)")
else:
    sc_new, n = re.subn(r"> \*\*Révision v1\.5\.2 \(2026-10-23[^\n]*?",
        "> **Révision v1.5.3 (2026-10-23, cascade Task 25bis/25ter — session web-fdf5963c, GO propriétaire)** : alias-eco v1.2.0 (grammaire B --trigger + OPT-TRIO ; v1.1.0 Description Optimization) ; KB recalibrée ; PM-INSTALL v1.8.3 (§A.3) ; ULTRA régénéré ; registre @Alias : OPT-TRIO attribué (état vivant, non-cible resync). Précédent — ", sc, count=1)
    assert n == 1, "FAIL SYNC"
    open(SC, "w", encoding="utf-8").write(sc_new)
    done.append("SYNC v1.5.3")

# ── 5. README v2.1.11 ────────────────────────────────────────────────
RD = f"{REPO}/skills/@mon-ecosysteme/README.md"
rd = open(RD, encoding="utf-8").read()
if "Révision v2.1.11" in rd:
    done.append("README (déjà appliqué)")
else:
    rd_new, n = re.subn(r"> \*\*Révision v2\.1\.10 \(2026-10-23[^\n]*?",
        "> **Révision v2.1.11 (2026-10-23, Task 25bis/25ter — session web-fdf5963c, GO propriétaire)** : alias-eco v1.2.0 — grammaire B mécanique (`--trigger`) + attribution OPT-TRIO ; v1.1.0 Description Optimization (clause d'exclusion sans radicaux étrangers — replay 8/8) ; registre @Alias vivant (ECO-LEON, OPT-TRIO) ; KB, PM-INSTALL v1.8.3 (§A.3), SYNC v1.5.3, ULTRA recalibrés. Précédent — ", rd, count=1)
    assert n == 1, "FAIL README"
    open(RD, "w", encoding="utf-8").write(rd_new)
    done.append("README v2.1.11")

# ── 6. historique-autres-elements.md ×4 ─────────────────────────────
H = f"{REPO}/skills/@historique/historique-autres-elements.md"
h = open(H, encoding="utf-8").read()
if "v1.5.3 | 2026-10-23" not in h:
    sc_head = "## 2. SYNC-CONTEXT.md (procédure de synchronisation des blocs)\n\n| Version | Date | Résumé de révision |\n|---------|------|--------------------|\n"
    assert h.count(sc_head) == 1
    h = h.replace(sc_head, sc_head + "| v1.5.3 | 2026-10-23 | Cascade Task 25bis/25ter (GO propriétaire, session web-fdf5963c) : alias-eco v1.1.0→v1.2.0 (grammaire B --trigger + OPT-TRIO ; v1.1.0 Description Optimization replay 8/8) ; KB, PM-INSTALL v1.8.3 (§A.3), ULTRA recalibrés ; registre @Alias vivant (ECO-LEON, OPT-TRIO — non-cible resync) |\n", 1)
    done.append("H row SYNC v1.5.3")
if "v2.1.11 | 2026-10-23" not in h:
    rd_head = "## 3. README.md (guide de référence de l'écosystème)\n\n| Version | Date | Résumé de révision |\n|---------|------|--------------------|\n"
    assert h.count(rd_head) == 1
    h = h.replace(rd_head, rd_head + "| v2.1.11 | 2026-10-23 | Cascade Task 25bis/25ter (GO propriétaire, session web-fdf5963c) : alias-eco v1.2.0 (grammaire B --trigger + OPT-TRIO ; v1.1.0 Description Optimization) ; KB, PM-INSTALL v1.8.3, SYNC v1.5.3, ULTRA recalibrés |\n", 1)
    done.append("H row README v2.1.11")
if "v1.8.3 | 2026-10-23 | Cascade alias-eco" not in h:
    pmi_head = "## 5. PROMPT-MAITRE-INSTALL-ECOSYSTEME.md (pipeline d'installation — source unique)\n\n| Version | Date | Résumé de révision |\n|---------|------|--------------------|\n"
    assert h.count(pmi_head) == 1
    h = h.replace(pmi_head, pmi_head + "| v1.8.3 | 2026-10-23 | Cascade alias-eco v1.2.0 (Task 25bis/25ter, GO propriétaire) : §A.3 instantané recalibré (alias-eco v1.0.0→v1.2.0) — bump PATCH conformité semver |\n", 1)
    done.append("H row PM-INSTALL v1.8.3")
kb_row = re.search(r"\| alias-eco \| v1\.0\.0 \|", h)
assert kb_row, "FAIL KB snapshot row alias-eco"
h = h[:kb_row.start()] + "| alias-eco | v1.2.0 |" + h[kb_row.end():]
done.append("H snapshot KB alias-eco v1.2.0")
intro_kb = "instantané rafraîchi 2026-10-23 Task 18 — alias-eco v1.0.0 créé, 4 familles montées"
if intro_kb in h:
    h = h.replace(intro_kb, "instantané rafraîchi 2026-10-23 Task 18 (création alias-eco) puis Task 25bis/25ter (alias-eco v1.2.0 — grammaire B --trigger, OPT-TRIO)", 1)
    done.append("H intro KB")
open(H, "w", encoding="utf-8").write(h)

print("RELICAT CASCADE OK — %d ops :" % len(done))
for d in done:
    print(" -", d)
