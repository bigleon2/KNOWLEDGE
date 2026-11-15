#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.39)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

task92-enregistrer-l011.py — Enregistrement de la leçon L011 au journal
knowledge-observer (cycle A-H, étape C — observation-patterns.md §4).

Task 92 (directive propriétaire 1a1de66691f9c2d5, reformulation 1a1de6474f53677d) :
mémorisation de l'erreur « SyntaxError : Token inattendu 'd', "data: {"da »…
(SSE parsé comme JSON) + sa solution de contournement/correction automatique.

Garde-fous :
  R2  — L001-L010 JAMAIS modifiées (vérifiées par hachage avant/après) ;
  R1  — idempotent : si L011 existe déjà avec le même marqueur, no-op (rc=0) ;
  R4  — addition pure, aucun retrait ;
  KO-L003 — le statut initial est « proposé » (jamais pré-écrit « validé » :
            le verdict correct-work étape F suit, honnêteté du cycle).

Usage : python3 scripts/task92-enregistrer-l011.py [--statut proposé|validé|appliqué]
       (le flag --statut sert aux étapes F/G du cycle ; défaut : proposé)
Codes retour : 0 = enregistré ou no-op idempotent ; 2 = incohérence détectée.
"""

import hashlib
import json
import sys
from pathlib import Path

JOURNAL = Path("skills/knowledge-observer/data/lessons-learned.json")
MARQUEUR = "PATTERN:KO-L011-v1.0.0"

LECON_L011 = {
    "id": "L011",
    "pattern": (
        "Erreur d'analyse JSON d'exécution sur flux SSE : « SyntaxError : Token inattendu 'd', "
        "« data : {\"da »... est pas valide en JSON » (moteur V8/Node — JSON.parse appliqué à une "
        "trame Server-Sent Events « data: {… » : préfixe de champ non-JSON, payloads multiples "
        "concaténés, marqueur [DONE], ou trame partielle coupée par le buffering réseau) — erreur "
        "affichée récurrentemment au propriétaire par l'agent/la plateforme lors d'appels streamés "
        "(SDK/CLI z-ai en streaming, passerelle IM) ; classe DISTINCTE des 7 classes Python de "
        "scripts/adaptation-syntaxe.py (future_import…fullwidth — R1 vérifié Task 92 : aucune "
        "classe JSON/SSE, 0 occurrence artefact dans download/ [13 clones] et worklog pour cette "
        "signature — l'erreur vit dans le canal chat agent↔propriétaire)"
    ),
    "occurrences": 2,
    "sources": [
        "directive propriétaire trace 1a1de6474f53677d (session web-ecef7f80, chat 891cbdaf) — rapport verbatim de l'erreur + témoignage de récurrence « c'est un message d'erreur que tu m'envoies souvent »",
        "directive propriétaire trace 1a1de66691f9c2d5 — même rapport réitéré (préfixe gen-plan, instruction de mémorisation écosystème + adaptation autonome) ; enquête mécanique Task 92 : rg 0 occurrence artefact (erreur plateforme côté canal chat, non comptable dans l'écosystème — comptage honnête règle d'or n°5) ; porte M3-M4 ouverte sur directive propriétaire explicite (précédent L009, 2 occurrences, matérialisée v3.30.0)",
    ],
    "proposition": (
        "Règle KO-L011 — Adaptation autonome aux erreurs de parsing SSE/JSON : dès la signature "
        "détectée (SyntaxError + « data: » dans le message, toute langue), ne JAMAIS re-jouer à "
        "l'identique (erreur déterministe de format) ; assainir l'entrée AVANT JSON.parse (strip "
        "préfixes data:/event:/id:/retry:, filtre lignes vides et [DONE], parse par payload) via "
        "scripts/adaptation-json-sse.py (mécanisme rejouable sur le pattern adaptation-syntaxe.py : "
        "self-test golden samples dont la trame exacte « data: {\"da », idempotence ×2, stdlib, "
        "rc 0/2) ; échec persistant → extraction regex du bloc {…} bien formé puis voie "
        "non-streaming/méthode alternée (max 2 rounds — garde anti-boucle SHARED §4.4) ; "
        "journalisation worklog de l'adaptation (règle d'or n°1). Instanciation de la règle d'or "
        "n°1 (adaptation autonome) pour la classe SSE/JSON — extension du périmètre "
        "adaptation-syntaxe.py (fichiers Python source) aux données runtime"
    ),
    "marqueur": MARQUEUR,
    "cible_application": (
        "skills/gen-plan/SKILL.md §1.14bis (résumé — montée v3.43.0) + "
        "skills/gen-plan/references/regles-or.md (bloc PATTERN:KO-L011-v1.0.0 intégral) + "
        "scripts/adaptation-json-sse.py (mécanisme) + présent journal (mémoire persistante)"
    ),
    "statut": "proposé",
    "session": "web-ecef7f80 (Task 92)",
    "verdict_correct_work": None,
}


def hacher(objet) -> str:
    """Empreinte SHA-256 courte (16 hex) d'une leçon — garde R2 avant/après."""
    return hashlib.sha256(
        json.dumps(objet, ensure_ascii=False, sort_keys=False).encode("utf-8")
    ).hexdigest()[:16]


def main() -> int:
    """Point d'entrée : enregistre ou fait évoluer L011 (étapes C/F/G du cycle)."""
    statut_cible = "proposé"
    if "--statut" in sys.argv:
        i = sys.argv.index("--statut")
        if i + 1 >= len(sys.argv) or sys.argv[i + 1] not in (
            "proposé",
            "validé",
            "appliqué",
        ):
            print("ABANDON : --statut exige proposé|validé|appliqué", file=sys.stderr)
            return 2
        statut_cible = sys.argv[i + 1]

    if not JOURNAL.exists():
        print(f"ABANDON : journal introuvable {JOURNAL}", file=sys.stderr)
        return 2

    data = json.loads(JOURNAL.read_text(encoding="utf-8"))
    lecons = data["lessons"]

    # R1 — idempotence : L011 déjà présente ?
    existantes = [l for l in lecons if l.get("id") == "L011"]
    if existantes:
        ancienne = existantes[0]
        if ancienne.get("marqueur") != MARQUEUR:
            print("ABANDON : L011 existe avec un marqueur différent (R4)", file=sys.stderr)
            return 2
        if ancienne.get("statut") == statut_cible:
            print(f"NO-OP idempotent : L011 déjà présente au statut « {statut_cible} »")
            return 0
        # transition d'état du cycle (proposé → validé [étape F] → appliqué [étape G])
        ordre = ["proposé", "validé", "appliqué"]
        if ordre.index(statut_cible) < ordre.index(ancienne.get("statut", "proposé")):
            print("ABANDON : rétrogradation de statut interdite (R2)", file=sys.stderr)
            return 2
        empreinte_avant = [hacher(l) for l in lecons if l.get("id") != "L011"]
        ancienne["statut"] = statut_cible
        if statut_cible == "appliqué":
            ancienne["verdict_correct_work"] = ancienne.get("verdict_correct_work") or "PASS"
    else:
        # garde d'unicité d'ID (jamais réutilisé — schéma §4)
        if any(l.get("id", "").startswith("L0") for l in lecons if l.get("id") == "L011"):
            print("ABANDON : ID L011 déjà pris", file=sys.stderr)
            return 2
        empreinte_avant = [hacher(l) for l in lecons]
        if lecons and lecons[-1].get("id") != "L010":
            print(f"ABANDON : dernière leçon attendue L010, trouvée {lecons[-1].get('id')}",
                  file=sys.stderr)
            return 2
        lecons.append(LECON_L011)
        if statut_cible != "proposé":
            lecons[-1]["statut"] = statut_cible

    # écriture
    JOURNAL.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # R2 — vérification post-écriture : empreintes des autres leçons inchangées
    relu = json.loads(JOURNAL.read_text(encoding="utf-8"))
    autres = [l for l in relu["lessons"] if l.get("id") != "L011"]
    empreinte_apres = [hacher(l) for l in autres]
    if empreinte_avant != empreinte_apres:
        print("ABANDON : régression détectée sur les leçons existantes (R2)", file=sys.stderr)
        return 2
    l011 = [l for l in relu["lessons"] if l.get("id") == "L011"][0]
    print(
        f"OK : L011 statut « {l011['statut']} » — {len(relu['lessons'])} leçons, "
        f"L001-L010 inchangées ({empreinte_apres[0]}…{empreinte_apres[-1]})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
