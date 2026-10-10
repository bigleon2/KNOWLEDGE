#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.6.8)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

"""R3 — Politique de consolidation de la mémoire (Task 36, vague 2 ; --apply armé Task 37).
Fenêtres / statuts / preuves conservées : analyse worklog.md + KNOWLEDGE.md,
proposition DRY-RUN d'archivage. Sans --apply : aucune modification du disque.
Avec --apply : archivage EFFECTIF (déplacement verbatim) des sections Task les plus
anciennes (au-delà du seuil) vers worklog-archive-<AAAA-MM>.md — autorisé uniquement
sur confirmation explicite du propriétaire (R2 : ne jamais rétrograder ; preuves
TOUJOURS conservées, aucune suppression destructive). Idempotent, sortie JSON.
Usage : r3-memory-consolidation.py [--seuil N] [--apply]
"""
import json, os, re, sys, time, hashlib

PROJECT = "/home/z/my-project"
WORKLOG = os.path.join(PROJECT, "worklog.md")
KB = os.path.join(PROJECT, "work_knowledge/skills/KNOWLEDGE.md")
OUT = os.path.join(PROJECT, "work_knowledge/tmp/r3-memory-consolidation.json")
BACKUP = os.path.join(PROJECT, "work_knowledge/tmp/worklog-backup-pre-r3-apply.md")


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def load_blocks():
    with open(WORKLOG, encoding="utf-8") as f:
        wl = f.read()
    # Découpage byte-fidèle : rejonction par '---' restaure l'original
    blocks = re.split(r"(?m)^---$", wl)
    ids = [m.group(1).strip() for b in blocks[1:]
           for m in [re.match(r"\s*Task ID: (.+)", b)] if m]
    return wl, blocks, ids


def main():
    apply_mode = "--apply" in sys.argv
    seuil = int(sys.argv[sys.argv.index("--seuil") + 1]) if "--seuil" in sys.argv else 10
    wl, blocks, ids = load_blocks()
    kb_txt = open(KB, encoding="utf-8").read()
    kb_entries = re.findall(r"^## ([A-Za-z0-9_.-]+) v([0-9.]+)", kb_txt, re.M)
    n_archivables = max(0, len(ids) - seuil)
    cand_ids = ids[:n_archivables]
    dup = [n for n, _ in kb_entries]
    dups = sorted({x for x in dup if dup.count(x) > 1})

    result = {
        "politique": "R3 — fenêtres : au-delà du seuil, les sections Task les plus anciennes deviennent candidates à l'archivage (worklog-archive-<mois>.md) ; statuts : ACTIF / ARCHIVABLE / ARCHIVÉ ; preuves TOUJOURS conservées (aucune suppression destructive sans confirmation propriétaire)",
        "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
        "mode": "APPLY" if apply_mode else "DRY-RUN",
        "worklog": {"octets": len(wl.encode()), "sections_task": len(ids),
                    "plus_ancienne": ids[0] if ids else None,
                    "plus_recente": ids[-1] if ids else None},
        "seuil_consolidation": seuil,
        "candidats_archivage": cand_ids,
        "kb": {"entrees_versionnees": len(kb_entries),
               "doublons_de_nom": dups if dups else "aucun"},
    }

    if not apply_mode:
        result["action"] = "DRY-RUN — proposition seulement (--apply requiert la confirmation explicite du propriétaire)"
    elif n_archivables == 0:
        result["action"] = "APPLY no-op — 0 candidat (idempotence : rien à archiver)"
    else:
        # ---- Archivage effectif (déplacement verbatim) ----
        mois = time.strftime("%Y-%m")
        archive_path = os.path.join(PROJECT, f"worklog-archive-{mois}.md")
        with open(BACKUP, "w", encoding="utf-8") as f:
            f.write(wl)
        wl_sha_avant = sha256(WORKLOG)

        # blocs candidats = blocks[1 .. n_archivables] (blocks[0] = en-tête)
        cand_blocks = blocks[1:1 + n_archivables]
        kept_blocks = blocks[1 + n_archivables:]

        verbatim = "----".join(cand_blocks[1:])  # contrôle interne (sans séparateur de section)
        for cb in cand_blocks:
            assert cb in wl, "bloc candidat absent du worklog source (abort)"

        if os.path.exists(archive_path):
            with open(archive_path, encoding="utf-8") as f:
                arch = f.read()
            arch_new = arch.rstrip("\n") + "\n---" + "---".join(cand_blocks)
            mode_note = "ajout en fin d'archive existante"
        else:
            entete = (
                f"# Worklog — Archive R3 ({mois})\n\n"
                f"> Archivage effectif R3 ({time.strftime('%Y-%m-%d')}) : les {n_archivables} sections Task les plus anciennes "
                f"({cand_ids[0]} → {cand_ids[-1]}) déplacées VERBATIM depuis worklog.md "
                f"(politique R3 — fenêtre seuil {seuil} ; confirmation propriétaire explicite ; "
                f"preuves conservées, aucune suppression destructive).\n"
                f"> Source : worklog.md sha256 {wl_sha_avant[:12]}… (écosystème 48f71c4).\n"
            )
            arch_new = entete + "---" + "---".join(cand_blocks)
            mode_note = "archive créée"

        notice = (
            f"<!-- ARCHIVAGE R3 (Task 37, {time.strftime('%Y-%m-%d')}) : les {n_archivables} sections Task les plus "
            f"anciennes ({cand_ids[0]} → {cand_ids[-1]}) sont archivées intégralement (verbatim) dans "
            f"worklog-archive-{mois}.md (même répertoire) — politique R3, fenêtre seuil {seuil}, confirmation "
            f"propriétaire explicite ; preuves conservées. Les sections ACTIVES suivent. -->\n"
        )
        wl_new = blocks[0] + notice + "---" + "---".join(kept_blocks)

        with open(archive_path, "w", encoding="utf-8") as f:
            f.write(arch_new)
        with open(WORKLOG, "w", encoding="utf-8") as f:
            f.write(wl_new)

        # Vérifications post-opération
        _, b2, ids2 = load_blocks()
        arch_ids = re.findall(r"^Task ID: (.+)$", arch_new, re.M)
        verif = {
            "archive_sections": len(arch_ids),
            "worklog_sections": len(ids2),
            "verbatim_integre": all(cb in arch_new for cb in cand_blocks),
            "aucune_perte": (sorted(arch_ids + ids2) == sorted(ids)),
            "archive": archive_path,
            "mode_fichier": mode_note,
        }
        result["action"] = f"ARCHIVAGE EFFECTIF — {n_archivables} sections déplacées verbatim ({mode_note})"
        result["application"] = {
            "archive_sha256": sha256(archive_path),
            "worklog_sha256_apres": sha256(WORKLOG),
            "worklog_sha256_avant": wl_sha_avant,
            "backup": BACKUP,
            "verifications": verif,
        }
        result["worklog_apres"] = {"octets": len(wl_new.encode()), "sections_task": len(ids2)}

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"R3 [{result['mode']}] : worklog {len(ids)} sections Task, seuil {seuil} → "
          f"{n_archivables} candidat(s) ; KB {len(kb_entries)} entrées, doublons : {'oui' if dups else 'non'} ; "
          f"action : {result['action']}")
    if apply_mode and n_archivables > 0:
        v = result["application"]["verifications"]
        ok = (v["archive_sections"] == n_archivables and v["worklog_sections"] == len(ids) - n_archivables
              and v["verbatim_integre"] and v["aucune_perte"])
        print(f"Vérifications : {v} → {'OK' if ok else 'ÉCHEC'}")
        return 0 if ok else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
