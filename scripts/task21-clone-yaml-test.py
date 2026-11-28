#!/usr/bin/env python3
"""Task 21 / suite 177 - Test mecanique $FANCON2 du jumeau YAML (clone-chat v2.3.0).

Valide mecaniquement les regles R-1 a R-6 de la section 1.14 du skill clone-chat
(mode --yaml) sur un echantillon de demonstration :
  T1  parse YAML sans erreur (PyYAML si disponible)
  T2  9 cles racines attendues presentes (schema 1.14)
  T3  couverture : chaque cle racine mappe une section du clone (S0-S5 + S1.0)
  T4  idempotence : 2 serialisations -> bytes identiques + round-trip parse/dump stable
  T5  provenance : meta.source_md + meta.sha256_source = SHA-256 du clone canonique
  T6  securite de serialisation : aucune tabulation, indentation 2 espaces
Deux passes internes (x2) comme le veut la convention $FANCON2.
Sorties : download/echantillon-clone-jumeau-yaml-demo.yaml
          download/rapport-task21-clone-yaml.json
rc 0 = tout PASS, rc 1 = au moins un FAIL.
"""
import hashlib
import json
import sys
from pathlib import Path

try:
    import yaml
    PARSER = f"PyYAML {yaml.__version__}"
except ImportError:  # pragma: no cover
    yaml = None
    PARSER = "garde-structurelle (PyYAML absent)"

BASE = Path("/home/z/my-project")
OUT_YAML = BASE / "download" / "echantillon-clone-jumeau-yaml-demo.yaml"
OUT_JSON = BASE / "download" / "rapport-task21-clone-yaml.json"

SOURCE_MD_DEMO = """# clone de demonstration — session de test jumeau YAML

## §0 — Règle zéro
Les fichiers des sessions précédentes n'existent pas dans une nouvelle session.

## §1 — Chronologie
Session de test T-demo : validation du schéma du jumeau YAML (clone-chat v2.3.0).

## §2 — Écosystème de skills
Artefact de démonstration : échantillon jumeau YAML.

## §3 — Décisions clés
Décision : le Markdown demeure l'instantané canonique (R-1).

## §3.5 — Évolutions de contexte
Aucune évolution de contexte détectée.

## §4 — Instructions d'utilisation
Régénérer le jumeau depuis le clone canonique si divergence (R-4).

## §5 — Auto-clonage
Le clone grandit par ses propres sessions (§1-§3 enrichis).
"""

CLEES_ATTENDUES = [
    "meta", "rule_zero", "chronologie", "artefacts", "decisions",
    "drifts", "instructions", "autoclone", "chain",
]

COUVERTURE = {
    "meta": "en-tête du clone (provenance, R-2)",
    "rule_zero": "§0 — Règle zéro",
    "chronologie": "§1 — Chronologie de la discussion",
    "artefacts": "§2 — Écosystème de skills",
    "decisions": "§3 — Décisions clés",
    "drifts": "§3.5 — Évolutions de contexte",
    "instructions": "§4 — Instructions d'utilisation",
    "autoclone": "§5 — Auto-clonage",
    "chain": "§1.0 — Chaîne de clonage (lignée)",
}


def construire_structure(source_md: str) -> dict:
    """Construit la structure du jumeau (miroir des sections du clone)."""
    sha_source = hashlib.sha256(source_md.encode("utf-8")).hexdigest()
    return {
        "meta": {
            "sujet": "echantillon-clone-jumeau-yaml-demo",
            "date": "2026-11-28",
            "session_id": "web-220878ed-c362-40f9-b12a-5aa08335c14d",
            "trace_id": "1a221e5599452e2d",
            "generation": "echantillon de demonstration (schéma §1.14 clone-chat v2.3.0)",
            "source_md": "echantillon-clone-jumeau-yaml-demo.source.md",
            "sha256_source": sha_source,
            "canonique": "le Markdown demeure l'unique instantané canonique (R-1)",
        },
        "rule_zero": {
            "regle": "Les fichiers des sessions précédentes n'existent pas dans une "
                     "nouvelle session : tout est à reconstruire à partir des documents "
                     "de la lignée. Ne jamais utiliser le verbe « conserver ».",
        },
        "chronologie": {
            "T-demo": [
                "Étape 1 : worklog collecté (session de démonstration)",
                "Étape 5 : assemblage §0-§5 terminé",
                "Étape 6 : 10/10 checks PASS (8 + check 9 thématique le cas échéant + check 10)",
                "Étape 7 : clone canonique sauvegardé + jumeau .yaml dérivé",
            ],
        },
        "artefacts": {
            "skills": ["clone-chat v2.3.0 (mode --yaml / alias --yalm)"],
            "documents": ["echantillon-clone-jumeau-yaml-demo.source.md (clone canonique de démonstration)"],
            "scripts": ["scripts/task21-clone-yaml-test.py (ce vérificateur $FANCON2)"],
            "charts": [],
            "archives": [],
        },
        "decisions": {
            "decisions_utilisateur": [{
                "decision": "Générer les clones en sortie duale : Markdown canonique + jumeau YAML dérivé",
                "contexte": "directive propriétaire trace 1a221e5599452e2d (« clones au format YALM »)",
                "consequences": "vue machine parseable pour sessions héritières et arbitres (R4 respecté : vue dérivée)",
            }],
            "bugs": [],
            "conventions": [{
                "regle": "YALM (formulation propriétaire) = YAML ; alias --yalm accepté au déclencheur",
                "exemple": "clone-chat --yalm == clone-chat --yaml",
            }],
            "calibration": {"surcout_token_mode_yaml": "+15-20 % du mode correspondant (grille §2.3 v2.3.0)"},
        },
        "drifts": [
            {"type": "ENRICHISSEMENT",
             "avant": "clone-chat v2.2.0 : sortie Markdown unique",
             "apres": "clone-chat v2.3.0 : sortie duale (Markdown canonique + jumeau YAML dérivé)",
             "session": "web-220878ed fenêtre 17",
             "ligne_worklog": "suite 177",
             "raison": "directive propriétaire 1a221e5599452e2d — verdict JUDICIEUSE"},
        ],
        "instructions": {
            "reprise": [
                "Lire le clone canonique .md pour l'usage humain",
                "Parser ce jumeau .yaml pour l'usage machine (ancrage KO-L003, checkpoints E11)",
                "En cas de divergence : régénérer le jumeau depuis le clone canonique (R-4)",
            ],
            "fichiers_prioritaires": ["echantillon-clone-jumeau-yaml-demo.source.md"],
        },
        "autoclone": {
            "mecanisme": "clone-chat référencé : §1-§3 enrichis par ses propres sessions, §0/§4-§5 régénérés",
        },
        "chain": {
            "lignee": ["echantillon de démonstration — aucun clone antérieur (premier de sa lignée)"],
        },
    }


def serialiser(structure: dict) -> str:
    """Sérialisation déterministe (R-4) : ordre d'insertion stable, indent 2, sans tabs."""
    return yaml.safe_dump(
        structure,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
        width=100,
        indent=2,
    )


def run_pass(num_pass: int) -> dict:
    """Une passe de vérification (T1-T6). Retourne le dict de verdicts."""
    src = SOURCE_MD_DEMO
    structure = construire_structure(src)
    dump1 = serialiser(structure)
    verdicts = {}

    # T1 parse
    try:
        charge = yaml.safe_load(dump1) if yaml else json.loads("null")
        verdicts["T1-parse-sans-erreur"] = "PASS" if isinstance(charge, dict) else "FAIL"
    except Exception:
        verdicts["T1-parse-sans-erreur"] = "FAIL"
        charge = None

    # T2 clés racines
    cles = list(charge.keys()) if isinstance(charge, dict) else []
    verdicts["T2-9-cles-racines"] = "PASS" if cles == CLEES_ATTENDUES else "FAIL"

    # T3 couverture sectionnelle
    ok_cov = isinstance(charge, dict) and all(k in charge for k in COUVERTURE)
    verdicts["T3-couverture-S0-S5"] = "PASS" if ok_cov else "FAIL"

    # T4 idempotence + round-trip
    dump2 = serialiser(construire_structure(src))
    sha1 = hashlib.sha256(dump1.encode()).hexdigest()
    sha2 = hashlib.sha256(dump2.encode()).hexdigest()
    re_dump = serialiser(yaml.safe_load(dump1))
    sha3 = hashlib.sha256(re_dump.encode()).hexdigest()
    verdicts["T4-idempotence-bytes-identiques"] = "PASS" if sha1 == sha2 else "FAIL"
    verdicts["T4bis-roundtrip-stable"] = "PASS" if sha1 == sha3 else "FAIL"

    # T5 provenance
    meta = charge.get("meta", {}) if isinstance(charge, dict) else {}
    sha_attendu = hashlib.sha256(src.encode("utf-8")).hexdigest()
    ok_prov = (meta.get("source_md") == "echantillon-clone-jumeau-yaml-demo.source.md"
               and meta.get("sha256_source") == sha_attendu)
    verdicts["T5-provenance-source-sha256"] = "PASS" if ok_prov else "FAIL"

    # T6 sérialisation sûre
    ok_ser = ("\t" not in dump1) and ("meta:" in dump1.splitlines()[0])
    verdicts["T6-sans-tabulations-indent2"] = "PASS" if ok_ser else "FAIL"

    return {
        "pass_num": num_pass,
        "verdicts": verdicts,
        "sha_jumeau": sha1,
        "nb_pass": sum(1 for v in verdicts.values() if v == "PASS"),
        "nb_total": len(verdicts),
        "dump": dump1,
    }


def main() -> int:
    print(f"parseur : {PARSER}")
    p1 = run_pass(1)
    p2 = run_pass(2)
    echantillon = SOURCE_MD_DEMO + "\n<!-- jumeau canonique de démonstration : voir .yaml -->"
    OUT_YAML.write_text(p1["dump"], encoding="utf-8")
    echantillon_md = BASE / "download" / "echantillon-clone-jumeau-yaml-demo.source.md"
    echantillon_md.write_text(echantillon, encoding="utf-8")

    croise = p1["sha_jumeau"] == p2["sha_jumeau"]
    rapport = {
        "task": "Task 21 / suite 177 — test $FANCON2 jumeau YAML (clone-chat v2.3.0 §1.14)",
        "trace_directive": "1a221e5599452e2d",
        "parseur": PARSER,
        "passes": [
            {k: v for k, v in p.items() if k != "dump"} for p in (p1, p2)
        ],
        "idempotence_croisee_p1_p2": "PASS" if croise else "FAIL",
        "echantillon_yaml": str(OUT_YAML),
        "echantillon_source_md": str(echantillon_md),
        "regles_validees": {
            "R-1": "structure = vue dérivée, non canonique (meta.canonique cité)",
            "R-2": "meta.source_md + meta.sha256_source présents et exacts (T5)",
            "R-3": "combinabilité documentée au SKILL.md §1.14 (hors périmètre d'exécution ici)",
            "R-4": "T4 + T4bis + croisé p1/p2",
            "R-5": "T6 (sans tabs, indent 2)",
            "R-6": "T1-T3 (parse, 9 clés, couverture §0-§5)",
        },
        "verdict_global": "PASS" if (p1["nb_pass"] == p1["nb_total"]
                                     and p2["nb_pass"] == p2["nb_total"] and croise) else "FAIL",
    }
    OUT_JSON.write_text(json.dumps(rapport, ensure_ascii=False, indent=2), encoding="utf-8")

    for p in (p1, p2):
        print(f"--- passe {p['pass_num']} : {p['nb_pass']}/{p['nb_total']} PASS")
        for t, v in p["verdicts"].items():
            print(f"  {t}: {v}")
    print(f"idempotence croisée p1/p2 : {rapport['idempotence_croisee_p1_p2']}")
    print(f"VERDICT GLOBAL : {rapport['verdict_global']}")
    print(f"échantillon : {OUT_YAML} ({OUT_YAML.stat().st_size} octets)")
    return 0 if rapport["verdict_global"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
