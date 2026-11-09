#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.37)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

Task 81 G2 — P6/P7 : PREUVE R4 BYTE-IDENTITÉ (references/ ↔ PM source intégral).
Directive propriétaire trace 1a1bcf4fecbf5f29 (item 2 : re-curation divulgation
progressive P1→P7). Pour chacun des 6 blocs déplacés par
scripts/task81-recuration-iphone19.py (moves R4 byte-identité, méthode
moves-r4-pur arbitrée --compare P2), ce vérificateur prouve MÉCANIQUEMENT :
  (a) le bloc tel qu'il vit dans skills/iphone19/references/<fichier> est
      INTACT — son SHA-256 == le SHA de provenance inscrit dans son en-tête ;
  (b) le bloc est BYTE-IDENTIQUE au PM source intégral
      skills/@photos/iphone19-photos.md v0.12.0 (extraction entre les mêmes
      marqueurs début/fin que la passe — source unique : import du script de
      passe, zéro duplication R4) ;
  (c) le pointeur inline (remplacement) est présent dans le SKILL.md curé.
Idempotent : lecture seule, aucun write. Verdict : R4-INTÈGRE (rc 0) si
6/6 blocs × 3 preuves, sinon DÉRIVE (rc 1). Python stdlib (N3).
Usage : python3 scripts/task81-verif-r4-iphone19.py [--json]
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

R = Path("/home/z/my-project/KNOWLEDGE-repo")
SKILL = R / "skills" / "iphone19" / "SKILL.md"
REFS = R / "skills" / "iphone19" / "references"
PM = R / "skills" / "@photos" / "iphone19-photos.md"


def main() -> int:
    fmt = "--json" in sys.argv
    # Source unique : définitions BLOCS/provenance importées du script de passe.
    spec = importlib.util.spec_from_file_location(
        "t81", R / "scripts" / "task81-recuration-iphone19.py")
    t81 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(t81)  # garde __main__ → aucune écriture (NO-OP sûr)

    pm_texte = PM.read_text(encoding="utf-8")
    skill_texte = SKILL.read_text(encoding="utf-8")
    preuves, fails = [], []
    for b in t81.BLOCS:
        ref_texte = (REFS / b["fichier"]).read_text(encoding="utf-8")
        m = re.search(r"SHA-256 du bloc : `([0-9a-f]{64})`", ref_texte)
        sha_prov = m.group(1) if m else None
        # (a) bloc tel qu'il vit en references/ : depuis le marqueur début.
        i = ref_texte.find(b["debut"])
        bloc_ref = ref_texte[i:] if i >= 0 else None
        sha_ref = t81.sha256(bloc_ref) if bloc_ref is not None else None
        # (b) bloc byte-identique au PM source intégral (mêmes bornes que la passe).
        ip = pm_texte.find(b["debut"])
        jp = pm_texte.find(b["fin"])
        bloc_pm = pm_texte[ip:jp] if ip >= 0 and jp > ip else None
        sha_pm = t81.sha256(bloc_pm) if bloc_pm is not None else None
        # (c) pointeur inline présent dans le SKILL.md curé : préfixe littéral du
        # remplacement (avant tout placeholder {kio}/{sha16}) + citation du fichier.
        prefixe = b["remplacement"].split("{")[0]
        pointeur = (len(prefixe) >= 30 and prefixe in skill_texte
                    and f"references/{b['fichier']}" in skill_texte)
        ok = (sha_prov is not None and sha_ref == sha_prov == sha_pm
              and bloc_ref == bloc_pm and pointeur)
        preuves.append({
            "fichier": b["fichier"], "section": b["section"],
            "sha_provenance": sha_prov, "sha_references": sha_ref, "sha_pm_source": sha_pm,
            "byte_identique_ref_pm": bloc_ref == bloc_pm,
            "octets_bloc": len(bloc_ref.encode("utf-8")) if bloc_ref else 0,
            "pointeur_inline": pointeur, "verdict": "INTÈGRE" if ok else "DÉRIVE",
        })
        if not ok:
            fails.append(b["fichier"])
    rapport = {
        "skill": "iphone19", "version": "0.12.0",
        "protocole": "Task 81 G2 — preuve R4 byte-identité (P6/P7)",
        "pm_source": "skills/@photos/iphone19-photos.md v0.12.0 [ANTICIPÉE]",
        "blocs": preuves, "blocs_integres": len(preuves) - len(fails),
        "blocs_total": len(preuves),
        "somme_octets_deplaces": sum(p["octets_bloc"] for p in preuves),
        "verdict": "R4-INTÈGRE" if not fails else "DÉRIVE",
    }
    if fmt:
        print(json.dumps(rapport, ensure_ascii=False, indent=1))
    else:
        for p in preuves:
            print(f"[{p['verdict']}] {p['fichier']} — {p['octets_bloc']} o · "
                  f"provenance==references==pm_source : "
                  f"{p['sha_provenance'] == p['sha_references'] == p['sha_pm_source'] if p['sha_provenance'] else False} "
                  f"(SHA {str(p['sha_provenance'])[:16]}…) · pointeur inline : {p['pointeur_inline']}")
        print(f"SOMME déplacée : {rapport['somme_octets_deplaces']} o — "
              f"{rapport['blocs_integres']}/{rapport['blocs_total']} blocs intègres")
        print(f"VERDICT : {rapport['verdict']}")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
