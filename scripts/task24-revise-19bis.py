#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.10)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# PROVENANCE: Task 24 (2026-10-23, session web-fdf5963c) — révision des §1.9bis
# des 16 éléments (directive propriétaire « révisez les §1.9bis des 16 éléments »).
# 15 sections restructurées (bullets apport → application locale + Sources
# normalisé + note de révision) + §1.9bis CRÉÉE pour agent-creator (16e).
# Garde anti-perte MÉCANIQUE : chaque lead-in (mots significatifs) et chaque
# source du bloc Task 22 doit se retrouver dans le bloc révisé — échec sinon
# (leçon Task 17 : échec si 0 match / perte). Idempotent ×2.
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from task24_contenu_19bis import REVISED, NOTE_REV, NOTE_ADD, HIST_AGC_ROW  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
SK = REPO / "skills"
HOTE_SK = Path("/home/z/my-project/skills")
HOTE_SEUL = {"cahier-des-charges", "inter-scripts", "agent-prompt-engineering"}
TITRE = "### §1.9bis — Apports de veille 2025-2026 (Task 22 — recherches web ciblées)"
STOPWORDS = set("""le la les de des du en et ou à au aux un une pour par sur dans avec
vs pas ne jamais plus très non oui son sa ses leur leurs ce cet cette ces qui que quoi
dont ainsi alors donc car mais où est sont être avoir fait faire sans sous entre vers
the of and to in is are""".split())


def bump_skill_version(text, old, new, skill):
    pat = re.compile(r"^version:\s*[\"']?%s[\"']?\s*$" % re.escape(old), re.M)
    ms = pat.findall(text)
    assert len(ms) == 1, f"{skill}: version {old} trouvée {len(ms)} fois (attendu 1)"
    return pat.sub(f"version: {new}", text, count=1)


def mots_significatifs(chaine):
    mots = set()
    for m in re.findall(r"[A-Za-zÀ-ÿ0-9][\w'/-]*", chaine.lower()):
        m = m.strip("'-_/«»")
        if len(m) >= 4 and m not in STOPWORDS:
            mots.add(m)
    return mots


def garde_anti_perte(old_block, new_content, skill):
    """Chaque lead-in (mots significatifs) et chaque source du bloc Task 22
    doit se retrouver dans le bloc révisé — sinon ABANDON SANS ÉCRITURE."""
    leads = [l for l in re.findall(r"\*\*(.+?)\*\*", old_block)
             if l not in ("Sources", "Références")]
    new_norm = new_content.lower()
    perdus = []
    for lead in leads:
        manquants = mots_significatifs(lead) - set(re.findall(r"[\w'/-]+", new_norm))
        if manquants:
            perdus.append((lead, sorted(manquants)))
    src = re.search(r"\*\*(?:Sources|Références)\*\* : (.+)$", old_block, re.M)
    src_perdues = []
    if src:
        for token in src.group(1).split("·"):
            base = token.strip().split(" (")[0].strip()
            if base and base.lower() not in new_norm:
                src_perdues.append(base)
    assert not perdus and not src_perdues, (
        f"{skill}: GARDE ANTI-PERTE — leads {perdus} sources {src_perdues} — ABANDON")


def reviser(text, skill, old_v, new_v, contenu, note):
    assert note not in text, f"{skill}: déjà révisé (idempotence)"
    text = bump_skill_version(text, old_v, new_v, skill)
    i = text.find(TITRE)
    assert i > 0, f"{skill}: titre §1.9bis introuvable"
    j = text.find("\n## §2", i)
    assert j > i, f"{skill}: ancre §2 introuvable après le titre"
    old_block = text[i + len(TITRE):j].strip()
    garde_anti_perte(old_block, contenu, skill)
    nouveau = TITRE + "\n\n" + contenu.strip() + "\n\n" + note + "\n"
    return text[:i] + nouveau + text[j:]


def inserer_agent_creator(text, old_v, new_v, contenu, note):
    assert note not in text, "agent-creator: déjà inséré (idempotence)"
    text = bump_skill_version(text, old_v, new_v, "agent-creator")
    j = text.find("\n## §2")
    assert j > 0, "agent-creator: ancre §2 introuvable"
    bloc = TITRE + "\n\n" + contenu.strip() + "\n\n" + note + "\n"
    text = text[:j] + bloc + text[j:]
    # Historique des versions : ligne 2.3.0 avant la ligne 2.2.0
    ancre = "| 2.2.0 | 2026-10-23 | Task 22"
    assert text.count(ancre) == 1, "agent-creator: ancre HISTORIQUE 2.2.0 introuvable"
    text = text.replace(ancre, HIST_AGC_ROW.rstrip("\n") + "\n" + ancre, 1)
    return text


def main():
    revises, insere, skipped = [], [], []
    for skill, (old_v, new_v, contenu) in REVISED.items():
        p = (HOTE_SK if skill in HOTE_SEUL else SK) / skill / "SKILL.md"
        t = p.read_text(encoding="utf-8")
        note = NOTE_ADD if skill == "agent-creator" else NOTE_REV
        if note in t and re.search(r"^version:\s*%s\s*$" % re.escape(new_v), t, re.M):
            skipped.append(skill)
            continue
        if skill == "agent-creator":
            t2 = inserer_agent_creator(t, old_v, new_v, contenu, note)
            insere.append(skill)
        else:
            t2 = reviser(t, skill, old_v, new_v, contenu, note)
            revises.append(skill)
        p.write_text(t2, encoding="utf-8")

    # Vérification finale : 16 sections conformes
    for skill, (old_v, new_v, contenu) in REVISED.items():
        p = (HOTE_SK if skill in HOTE_SEUL else SK) / skill / "SKILL.md"
        t = p.read_text(encoding="utf-8")
        note = NOTE_ADD if skill == "agent-creator" else NOTE_REV
        assert note in t, f"{skill}: note absente après écriture"
        assert re.search(r"^version:\s*%s\s*$" % re.escape(new_v), t, re.M), \
            f"{skill}: version {new_v} absente après écriture"
        assert "- **Sources** :" in t, f"{skill}: bullet Sources absent"
        nb_bullets = t[t.find(TITRE):t.find("\n## §2", t.find(TITRE))].count("\n- **")
        assert nb_bullets >= 4, f"{skill}: {nb_bullets} bullets (attendu >= 4)"

    print(f"SKILL.md révisés : {len(revises)} -> {revises}")
    print(f"agent-creator : §1.9bis insérée (v2.3.0) -> {insere}")
    print(f"Déjà conformes (idempotence) : {len(skipped)} -> {skipped}")
    print("Garde anti-perte : PASS ×16 (lead-ins + sources préservés).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
