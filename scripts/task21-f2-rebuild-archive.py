#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.9)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""Task 21 — F2 : régénération de l'archive d'intégrité (véhicule v2.2) après édition du corpus.
Processus établi (Tasks 16/18) : l'archive = copie byte-identique du corpus @mon-ecosysteme
+ homologues/ v2.1 (famille créateur/relecture). Idempotent : re-exécution = archive équivalente."""
import shutil
import zipfile
from pathlib import Path

# Portabilite L008 (garde E1) : derive de __file__ (jamais de chemin absolu figure)
BASE = Path(__file__).resolve().parent.parent
CORPUS = BASE / "skills" / "@mon-ecosysteme"
HISTORIQUE = BASE / "skills" / "@historique" / "prompts-maitres"  # Task 16 : destination des PMs déplacés
ARCHIVE = BASE / "download" / "mon-ecosysteme_archive.zip"
BAK = ARCHIVE.with_suffix(".zip.bak")

# Retraits sanctionnés : entrées de l'ancienne archive à supprimer du re-scellement
# (au lieu d'échouer en « extra hors homologues » — protection anti-perte conservée
# pour tout autre extra). Traçabilité : chaque retrait = suppression propriétaire
# publiée, référencée ici avec son commit et sa décision de calibration.
RETRAITS_SANCTIONNES = {
    # suppression propriétaire d72226a (UI web, couche Task 14-push) —
    # re-scellement Task 15 (D002, plan-task15-decisions-restantes.md)
    "clone-discussion-2026-09-27-ecosysteme-knowledge-b13-r7-f.md",
    # déduplication des PMs (directive propriétaire « ne garder que la dernière
    # version ») — re-scellement Task 16 (plan-task16-corpus-pms-historique-
    # reinstallation.md) : 19 PMs historiques DÉPLACÉS git mv vers
    # skills/@historique/prompts-maitres/{gen-plan,correct-work}/ — byte-identité
    # vérifiée ci-dessous contre l'ancienne archive (garde anti-perte renforcée).
    # cascade gen-plan v3.23.1 (Task 8, session web-b4d7dd19 — gen-plan(step),
    # correction outil n°55 + fusion discussion 468a4c26) : PM GEN-PLAN v3.23.0
    # DÉPLACÉ git mv vers skills/@historique/prompts-maitres/gen-plan/ —
    # byte-identité vérifiée ci-dessous (garde anti-perte ; SHA bba1b9c40dda…).
    # cascade Task 18 (2026-10-23, session web-fdf5963c — optimisation du système
    # d'installation + alias-eco) : 4 PMs familles supplantés par montées mécaniques
    # KO-L004 (gen-plan v3.23.2, correct-work v2.8.0, clone-chat v2.0.2,
    # refactor-guard v1.7.1) — DÉPLACÉS git mv vers skills/@historique/
    # prompts-maitres/<famille>/ — byte-identité SHA-256 scellée au README §5.
    "PROMPT-MAITRE-GEN-PLAN-v3.23.1.md",
    "PROMPT-MAITRE-CORRECT-WORK-v2.7.0.md",
    "PROMPT-MAITRE-CLONE-CHAT-v2.0.1.md",
    "PROMPT-MAITRE-REFACTOR-GUARD-v1.7.0.md",
    # cascade Task 22 (2026-10-23, même session — directive « disciplines/techniques »,
    # veille 2025-2026) : PM REFACTOR-GUARD v1.7.1 supplanté par la montée mécanique
    # KO-L004 (SKILL.md v1.8.0 — §1.9bis golden master AVANT + mutation testing +
    # rollback armé) — DÉPLACÉ vers skills/@historique/prompts-maitres/
    # refactor-guard/ — byte-identité SHA-256 scellée au README §5.
    "PROMPT-MAITRE-REFACTOR-GUARD-v1.7.1.md",
    # véhicule d'intégrité v2.3 « piliers » (reprise matinale 2026-10-23, session
    # web-fdf5963c — reinstallateur autonome) : RETIRÉ au profit du véhicule v2.2
    # corpus-seul (PM-INSTALL v1.8.0) ; le contenu des piliers vit dans l'arbre
    # (scripts/, skills/KNOWLEDGE.md, skills/<famille>/SKILL.md) — aucune perte.
    "piliers/scripts/certification-complete.py",
    "piliers/scripts/check-ecosysteme-integrity.py",
    "piliers/scripts/install-ecosysteme-local.sh",
    "piliers/skills/KNOWLEDGE.md",
    "piliers/skills/correct-work/SKILL.md",
    "piliers/skills/gen-plan/SKILL.md",
    "PROMPT-MAITRE-GEN-PLAN-v3.23.0.md",
    "PROMPT-MAITRE-GEN-PLAN-v3.6.1.md", "PROMPT-MAITRE-GEN-PLAN-v3.7.0.md",
    "PROMPT-MAITRE-GEN-PLAN-v3.8.0.md", "PROMPT-MAITRE-GEN-PLAN-v3.8.1.md",
    "PROMPT-MAITRE-GEN-PLAN-v3.9.0.md", "PROMPT-MAITRE-GEN-PLAN-v3.10.0.md",
    "PROMPT-MAITRE-GEN-PLAN-v3.11.0.md", "PROMPT-MAITRE-GEN-PLAN-v3.12.0.md",
    "PROMPT-MAITRE-GEN-PLAN-v3.13.0.md", "PROMPT-MAITRE-GEN-PLAN-v3.16.0.md",
    "PROMPT-MAITRE-GEN-PLAN-v3.17.0.md", "PROMPT-MAITRE-GEN-PLAN-v3.17.1.md",
    "PROMPT-MAITRE-GEN-PLAN-v3.17.2.md", "PROMPT-MAITRE-GEN-PLAN-v3.18.0.md",
    "PROMPT-MAITRE-GEN-PLAN-v3.19.0.md",
    "PROMPT-MAITRE-CORRECT-WORK-v2.4.0.md", "PROMPT-MAITRE-CORRECT-WORK-v2.5.0.md",
    "PROMPT-MAITRE-CORRECT-WORK-v2.5.1.md", "PROMPT-MAITRE-CORRECT-WORK-v2.6.0.md",
    # cascade gen-plan v3.22.0 (session web-b4d7dd19, KO-L004/§2quater) — re-scellement
    # post-cascade : PM v3.21.0 supplanté DÉPLACÉ git mv vers
    # skills/@historique/prompts-maitres/gen-plan/ — byte-identité vérifiée ci-dessous
    # (garde anti-perte renforcée ; SHA-256 scellé à l'index §5 du README @historique).
    "PROMPT-MAITRE-GEN-PLAN-v3.21.0.md",
    # cascade gen-plan v3.22.1 (session web-b4d7dd19, directive propriétaire
    # renommage step-confirm → step-ok + clause mode NULL) — re-scellement
    # post-cascade : PM v3.22.0 supplanté DÉPLACÉ mv byte-identité (fichier non
    # suivi — jamais commité ; adaptation règle d'or n°1 journalisée) vers
    # skills/@historique/prompts-maitres/gen-plan/ — byte-identité vérifiée
    # ci-dessous (garde anti-perte renforcée ; SHA-256 scellé à l'index §5 du
    # README @historique).
    "PROMPT-MAITRE-GEN-PLAN-v3.22.0.md",
    # gen-plan v3.23.0 (session web-b4d7dd19, Task 7 gen-plan(step) — matérialisation
    # disciplines de refactoring n°55) — re-scellement post-cascade : PM v3.22.1
    # supplanté DÉPLACÉ git mv vers skills/@historique/prompts-maitres/gen-plan/ —
    # byte-identité vérifiée ci-dessous (garde anti-perte renforcée ; SHA-256
    # scellé à l'index §5 du README @historique).
    "PROMPT-MAITRE-GEN-PLAN-v3.22.1.md",
    # cascade clone-chat v2.0.1 (Task 12, session web-b4d7dd19 — gen-plan(step),
    # directive propriétaire « appliquer les corrections » — C-12c : F-c1/F-c2) :
    # PM CLONE-CHAT v2.0.0 supplanté DÉPLACÉ git mv vers
    # skills/@historique/prompts-maitres/clone-chat/ — byte-identité vérifiée
    # ci-dessous (garde anti-perte renforcée).
    "PROMPT-MAITRE-CLONE-CHAT-v2.0.0.md",
}

# Task 16 — garde anti-perte renforcée pour les retraits DÉPLACÉS : chaque PM
# sanctionné doit exister en skills/@historique/prompts-maitres/ avec les MÊMES
# octets que l'entrée de l'ancienne archive (sinon : échec + restauration).
def dest_historique(short):
    if short.startswith("PROMPT-MAITRE-GEN-PLAN-"):
        return HISTORIQUE / "gen-plan" / short
    if short.startswith("PROMPT-MAITRE-CORRECT-WORK-"):
        return HISTORIQUE / "correct-work" / short
    if short.startswith("PROMPT-MAITRE-CLONE-CHAT-"):
        return HISTORIQUE / "clone-chat" / short
    if short.startswith("PROMPT-MAITRE-REFACTOR-GUARD-"):
        # Task 22 (2026-10-23) : KO-L003 — la liste figée ignorait la 4e famille
        # (refactor-guard) ; la garde anti-perte sautait silencieusement ses
        # retraits. Dynamisée = périmètre complet des 4 familles PM.
        return HISTORIQUE / "refactor-guard" / short
    return None

corpus_files = sorted(p.name for p in CORPUS.glob("*.md"))
print(f"corpus : {len(corpus_files)} fichiers .md")

# ADAPTATION LOCALE (règle d'or n°1 PM-INSTALL §3.4) : archive absente au premier
# rescellement (jamais commitée — .gitignore download/) -> pas de .bak, ancienne archive = {}
if ARCHIVE.exists():
    shutil.copy2(ARCHIVE, BAK)
    with zipfile.ZipFile(BAK) as z:
        old_names = z.namelist()
        old_bytes = {n: z.read(n) for n in old_names if not n.endswith("/")}
        # Task 20 (finding F3) : capture des dates d'entrées — le rescellement
        # doit être byte-STABLE (Z6/R6). Avant : writestr(nom, données) horodatait
        # chaque entrée à l'horloge murale → hash archive changeant à chaque
        # rescellement → manifeste (qui enregistre ce hash) jamais en point fixe
        # → installation non idempotente au niveau byte. Les dates existantes
        # sont désormais préservées ; époque fixe pour une entrée nouvelle.
        old_dates = {n: zi.date_time for n, zi in zip(z.namelist(), z.infolist())
                     if not n.endswith("/")}
else:
    old_bytes = {}
    old_dates = {}
print(f"ancienne archive : {len(old_bytes)} entrées")

# Task 16 — vérification anti-perte des retraits déplacés (avant toute écriture)
for name, data in old_bytes.items():
    short = name.split("@mon-ecosysteme/")[-1]
    if short in RETRAITS_SANCTIONNES:
        dest = dest_historique(short)
        if dest is None:
            continue  # retrait-suppression (clone-discussion) — vérifié Task 15
        if not dest.exists() or dest.read_bytes() != data:
            print(f"ECHEC anti-perte : {short} absent ou divergent en @historique/")
            raise SystemExit(2)
print(f"garde anti-perte : {sum(1 for n in old_bytes if n.split('@mon-ecosysteme/')[-1] in RETRAITS_SANCTIONNES and dest_historique(n.split('@mon-ecosysteme/')[-1]))} PMs déplacés vérifiés byte-identiques en @historique/")

with zipfile.ZipFile(ARCHIVE, "w", zipfile.ZIP_DEFLATED) as z:
    # ADAPTATION LOCALE (règle d'or n°1 PM-INSTALL §3.4) : premier scellement —
    # ancienne archive absente -> les 8 fichiers corpus sont ajoutés directement.
    corpus_set = set(corpus_files)
    planned, seen = [], set()
    if old_bytes:
        for name in old_names:
            if name.endswith("/"):
                continue
            short = name.split("@mon-ecosysteme/")[-1]
            if short in RETRAITS_SANCTIONNES or short in seen:
                continue
            planned.append((name, short))
            seen.add(short)
    for f in corpus_files:
        if f not in seen:
            planned.append((f"@mon-ecosysteme/{f}", f))
            seen.add(f)
    for name, short in planned:
        if short in corpus_set:
            data = (CORPUS / short).read_bytes()
        else:
            data = old_bytes[name]
        # Task 20 (F3) : ZipInfo explicite — dates préservées (époque fixe
        # 1980-01-01 pour une entrée absente de l'ancienne archive), compression
        # DEFLATED et attributs 0o600 répliqués exactement comme writestr(nom)
        # le faisait, afin que le premier rescellement post-correctif soit
        # byte-identique à l'archive existante puis stable à l'infini.
        zi = zipfile.ZipInfo(name, date_time=old_dates.get(name, (1980, 1, 1, 0, 0, 0)))
        zi.compress_type = zipfile.ZIP_DEFLATED
        zi.external_attr = 0o600 << 16
        z.writestr(zi, data)

# auto-vérification : corpus ⊆ archive byte-identique, extras seulement homologues/
with zipfile.ZipFile(ARCHIVE) as z:
    znames = [n for n in z.namelist() if not n.endswith("/")]
    divergent = [n for n in corpus_files
                 if not any(m.split("@mon-ecosysteme/")[-1] == n and z.read(m) == (CORPUS / n).read_bytes()
                            for m in znames)]
    extras = [n for n in znames
              if (n.split("@mon-ecosysteme/")[-1] if "@mon-ecosysteme/" in n else n) not in set(corpus_files)
              and (n.split("@mon-ecosysteme/")[-1] if "@mon-ecosysteme/" in n else n) not in RETRAITS_SANCTIONNES
              and not n.startswith("homologues/")]
print(f"nouvelle archive : {len(znames)} entrées ; divergents : {divergent or '—'} ; "
      f"extras hors homologues : {extras or '—'}")
if divergent or extras:
    shutil.copy2(BAK, ARCHIVE)
    print("ÉCHEC — archive restaurée depuis la sauvegarde")
    raise SystemExit(1)
if BAK.exists():
    BAK.unlink()
print("Archive régénérée et round-trip vérifié (véhicule v2.2).")
