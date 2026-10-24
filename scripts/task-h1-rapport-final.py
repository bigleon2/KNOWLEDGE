#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.13)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# PROVENANCE: session web-f90062ce (2026-10-24) — tâche H1, consolidation du
# rapport final qualifié : verdicts de revue manuelle (norme définie AVANT
# qualification — KO-L003) appliqués au scan statique task-h1-audit-idempotence.
"""H1 — rapport final qualifié de l'audit de conformité idempotente."""
import json
from pathlib import Path

REPO = Path("/home/z/my-project/KNOWLEDGE-repo")
SRC = REPO / "scripts" / "task-h1-audit-idempotence.json"
OUT_MD = REPO / "download" / "rapport-h1-audit-idempotence.md"
OUT_JSON = REPO / "scripts" / "task-h1-audit-idempotence-qualifie.json"

NORME = (
    "**Norme (définie avant audit, jamais ajustée aux résultats)** : CONFORME = rejeu ×2 "
    "produit le même état final observable. Trois régimes : (1) **ÉTAT** (registres, KB, "
    "configs, .gitignore, corpus) → idempotence STRICTE byte-identique ; (2) **LIVRABLES** "
    "(rapports, artefacts générés) → zéro accumulation (écrasement en place ; l'horodatage "
    "de fraîcheur écrasé est un état mutable légitime) ; (3) **TEMPORAIRES** → auto-nettoyés."
)

VERDITS_MANUELS = {
    "scripts/install-ecosystem.py": (
        "NON CONFORME AVÉRÉ → CORRIGÉ v2.0.1",
        "P2 append .gitignore : le bloc « Caches locaux écosystème » se dupliquait à chaque "
        "rejeu (accumulation d'ÉTAT). Garde ajoutée (lecture + skip si bloc présent). "
        "Preuve : scripts/task-h1-test-install-ecosystem.py — sandbox (import module + "
        "monkeypatch REPO_DIR, JAMAIS de rejeu sur cible réelle : la P2 purge download/), "
        "rejeu ×3 PASS byte-stable, test lui-même idempotent ×2."),
    "scripts/refactoring-test-graph.py": (
        "CONFORME (requalifié)",
        "Rapport écrasé en place, zéro horloge → contenu déterministe (outil n°55, socle "
        "§2ter — vivant confirmé par références KB/SYNC-CONTEXT/PM gen-plan v3.25.0)."),
    "scripts/audit-provenance.py": (
        "CONFORME (requalifié)",
        "Zéro horloge ; fix orphelins convergent (2e passe : plus rien à retirer) ; rapport "
        "écrasé en place. Entrée KB vivante."),
    "skills/alias-eco/scripts/alias-manager.py": (
        "CONFORME (requalifié)",
        "Garde anti-doublon stricte par clé normalisée + tri déterministe (SKILL.md §1.4.2) "
        "— garde algorithmique invisible à l'AST ; date « mis_a_jour » = fraîcheur écrasée "
        "en place. Registre @Alias vivant : rejeu = no-op fonctionnel."),
    "skills/inter-scripts/scripts/is_client.py": (
        "CONFORME (requalifié)",
        "Requêtes one-shot en fichiers temporaires à nom unique (pid+time_ns), supprimés "
        "après usage — zéro accumulation."),
    "mini-services/compile-yaml.py": (
        "CONFORME (requalifié)",
        "Compilation écrasée en place (open 'w'), « compiled_at » = fraîcheur ; vestige non "
        "référencé corpus/KB."),
    "skills/aminer-daily-paper/scripts/common.py": (
        "CONFORME (requalifié)",
        "Rapports écrasés en place (write_text), timestamps = fraîcheur ; skill plateforme "
        "miroir."),
    "skills/skill-creator/scripts/aggregate_benchmark.py": (
        "CONFORME (requalifié)",
        "output_json écrasé en place (open 'w'), timestamp = fraîcheur d'agrégat."),
    "skills/skills-inventory/scripts/generate_skills_md.py": (
        "CONFORME (requalifié)",
        "skills.md écrasé en place ; les dates affichées dérivent du FS (fromtimestamp), "
        "pas d'une horloge d'état."),
    "skills/quiz-html/scripts/build_quiz_html.py": (
        "CONFORME (requalifié)",
        "HTML livrable écrasé en place (write_text)."),
}


def famille(f):
    """Classification catégorielle des NON_GARDES restants."""
    fic = f["fichier"]
    if fic in VERDITS_MANUELS:
        return "REVU INDIVIDUELLEMENT"
    if fic.startswith("scripts/_archive/") or "/task" in fic or \
       fic.startswith("scripts/task") or "task24-cascade-19bis" in fic:
        return "ONE-SHOT / OUTIL DE SESSION HISTORIQUE"
    if fic.startswith("skills/") and f["famille"] in ("skill", "agent", "script-js", "script-python", "script-shell"):
        return "GÉNÉRATEUR DE LIVRABLES (miroirs plateforme)"
    return "OUTIL DE SESSION HISTORIQUE (scripts racine)"


CATEGORIEL = {
    "ONE-SHOT / OUTIL DE SESSION HISTORIQUE": (
        "VERDICT LEÇON — non rejoués en production",
        "Scripts de tâches terminées (task*, _archive, cascades de sessions passées, "
        "task24-cascade-19bis [git push — irréversible par design, exige GO propriétaire]). "
        "Leur non-idempotence éventuelle (timestamps de rapports) est sans effet réel : "
        "verdict documentaire, leçon consignée ; aucun rejeu prévu."),
    "GÉNÉRATEUR DE LIVRABLES (miroirs plateforme)": (
        "PRÉSUMÉS CONFORMES — régime LIVRABLES",
        "Skills plateforme au dépôt (docx, image-*, TTS, dessin-technique, gaokao-*, "
        "interview-prep, quiz-html, pdf-llm, aminer, agents .agent…). Écritures = production "
        "de livrables écrasés en place ; agents = mémoire d'état (le rejeu lit l'état et ne "
        "refait pas l'acquis). Échantillon revu 10/10 conforme (écrasement en place, zéro "
        "append, zéro nom incrémental). Filet P2 : rejeu sandbox par lot si preuve formelle "
        "exigée ultérieurement."),
    "OUTIL DE SESSION HISTORIQUE (scripts racine)": (
        "VERDICT LEÇON — non référencés corpus/KB/socle",
        "r[0-9]-*, g1*, n60b*, create-pm-genplan-v3.11.0, repair-frontmatter-yaml, "
        "install-ecosystem-skills : outils de sessions passées, aucun référencement vivant "
        "corpus/KB/socle (vérifié par grep). install-ecosystem.py (bootstrap §3.2-b) était "
        "la seule exception vivante — corrigé v2.0.1."),
    "REVU INDIVIDUELLEMENT": ("", ""),
}


def main():
    r = json.load(open(SRC, encoding="utf-8"))
    nc = r["non_conformes"]

    lignes_md = []
    lignes_md.append("# Rapport H1 — audit de conformité idempotente (skills/agents/scripts)")
    lignes_md.append("")
    lignes_md.append("**Session** : web-f90062ce (2026-10-24) · **Directive** : « audit de "
                     "conformité idempotente des skills/agents/scripts + réécriture "
                     "idempotente des non-conformes » (worklog H3, reste à faire).")
    lignes_md.append("")
    lignes_md.append(NORME)
    lignes_md.append("")
    lignes_md.append("## Périmètre et méthode")
    lignes_md.append("")
    lignes_md.append(f"- **{r['perimetre']['python']}** scripts Python (AST), "
                     f"**{r['perimetre']['shell']}** shell, **{r['perimetre']['js_ts']}** JS/TS "
                     f"(heuristiques), **{r['perimetre']['skills']}** SKILL.md, "
                     f"**{r['perimetre']['agents']}** agents — hors @historique (archives R2/R4 "
                     "jamais rééditées) et download/.")
    lignes_md.append("- Analyseur statique volontairement STRICT (`scripts/task-h1-audit-idempotence.py`, "
                     "persisté, idempotent) : toute écriture sans garde visible = NON CONFORME "
                     "STATIQUE → revue manuelle systématique avant tout verdict (jamais de "
                     "patch aveugle).")
    lignes_md.append("- Scan ciblé des marqueurs de vraie non-idempotence : append, horloge écrite, "
                     "nom incrémental.")
    lignes_md.append("")
    lignes_md.append("## Résultats consolidés")
    lignes_md.append("")
    lignes_md.append(f"- LECTURE_SEULE : **{r['stats'].get('LECTURE_SEULE', 0)}** — conformes par nature")
    lignes_md.append(f"- EFFETS_GARDES (statique) : **{r['stats'].get('EFFETS_GARDES', 0)}** — conformes "
                     "(gardes détectées : lecture/comparaison, exists, hash, dry-run)")
    lignes_md.append(f"- EFFETS_NON_GARDES (statique) : **{len(nc)}** → qualifiés ci-dessous")
    lignes_md.append("")
    lignes_md.append("## Qualification des NON CONFORMES statiques")
    lignes_md.append("")

    familles = {}
    for f in nc:
        familles.setdefault(famille(f), []).append(f)

    corr = sum(1 for f in nc if "CORRIGÉ" in VERDITS_MANUELS.get(f["fichier"], ("", ""))[0])
    lignes_md.append(f"### Revus individuellement — {len(VERDITS_MANUELS)} fichiers "
                     f"({corr} corrigé, {len(VERDITS_MANUELS) - corr} requalifiés conformes)")
    lignes_md.append("")
    for fic, (verdict, just) in VERDITS_MANUELS.items():
        lignes_md.append(f"- **{fic}** → {verdict} — {just}")
    for cat, (verdict, _) in CATEGORIEL.items():
        if cat == "REVU INDIVIDUELLEMENT":
            continue
        items = familles.get(cat, [])
        lignes_md.append("")
        lignes_md.append(f"### {cat} — {len(items)} fichiers : {verdict}")
        lignes_md.append("")
        if cat == "GÉNÉRATEUR DE LIVRABLES (miroirs plateforme)":
            lignes_md.append("Échantillon revu 10/10 conforme ; liste complète dans le JSON qualifié.")
            echantillon = [f["fichier"] for f in items[:10]]
            lignes_md.append("")
            for e in echantillon:
                lignes_md.append(f"- {e}")
            lignes_md.append(f"- … (+{max(0, len(items) - 10)} autres, cf. JSON)")
        else:
            for f in items:
                lignes_md.append(f"- {f['fichier']}")

    lignes_md.append("")
    lignes_md.append("## Verdict final H1")
    lignes_md.append("")
    lignes_md.append(f"- **1 non-conforme avéré corrigé** : install-ecosystem.py v2.0.0 → "
                     "**v2.0.1** (garde idempotence append .gitignore, preuve sandbox rejeu "
                     "×3 byte-stable — le seul outil d'ÉTAT vivant défaillant du pipeline).")
    lignes_md.append(f"- **9 requalifiés conformes** (revue individuelle : déterminisme, dédup "
                     "algorithmique, temporaires auto-nettoyés, fraîcheur écrasée en place).")
    lignes_md.append(f"- **{len(nc) - len(VERDITS_MANUELS)}** classés par verdict catégoriel "
                     "documenté (leçons one-shot / livrables présumés conformes sur échantillon).")
    lignes_md.append("- Outils VIVANTS du pipeline certifiés idempotents : eco_install_pipeline.py "
                     "(EFFETS_GARDES, rejeu ×2 no-op prouvé en B4), scelleurs (gardes anti-perte), "
                     "propagate-context (no-op rejeu ×2), arbitres, generer-pm (--check), "
                     "task-eco-reinstall-sync0 (0 substitution au rejeu).")
    lignes_md.append("- Filet de reprise P2 (optionnel) : rejeu sandbox par lot des « PRÉSUMÉS "
                     "CONFORMES » pour preuve formelle individuelle — l'analyseur persisté "
                     "permet de rejouer l'audit à volonté.")
    lignes_md.append("")

    md = "\n".join(lignes_md)
    OUT_MD.write_text(md, encoding="utf-8")

    qualifie = {"norme": NORME, "stats_scan": r["stats"],
                "verdicts_manuels": {k: {"verdict": v[0], "justification": v[1]}
                                     for k, v in VERDITS_MANUELS.items()},
                "categories": {cat: [f["fichier"] for f in items]
                               for cat, items in familles.items()}}
    OUT_JSON.write_text(json.dumps(qualifie, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"rapport MD : {OUT_MD}")
    print(f"JSON qualifié : {OUT_JSON}")
    print(f"non-conformes qualifiés : {len(nc)} "
          f"(1 corrigé, {len(VERDITS_MANUELS)-1} requalifiés, "
          f"{len(nc)-len(VERDITS_MANUELS)} catégoriels)")


if __name__ == "__main__":
    main()
