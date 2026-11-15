#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.37)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour tous les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

adaptation-json-sse.py — Garde d'assainissement SSE vers JSON de l'écosystème.

Mécanisme de la règle KO-L011 (leçon L011, Task 92 — directive propriétaire
1a1de66691f9c2d5, reformulation 1a1de6474f53677d) : l'erreur récurrente
« SyntaxError : Token inattendu 'd', « data : {"da »... est pas valide en JSON »
est un JSON.parse appliqué à une trame Server-Sent Events. Ce script assainit
la trame AVANT le parse (solution de correction) et extrait les payloads
récupérables (solution de contournement). Sœur runtime de
scripts/adaptation-syntaxe.py (qui couvre les fichiers Python source — 7
classes ; présent script couvre les DONNÉES JSON/SSE d'exécution).

Sous-commandes :
  sanitize <fichier|->     Trame SSE → JSON propre sur stdout (rc 0) ;
                           aucun payload récupérable → diagnostic + rc 2.
  detect <texte>           Détecte la signature de l'erreur KO-L011 dans un
                           message d'erreur (rc 0 = signature présente, 1 = non).
  --selftest               Golden samples embarqués (rc 0 si tous PASS).

Comportement (sanitize) :
  1. entrée déjà-propre (JSON valide sans préfixe SSE) → passerelle (no-op) ;
  2. lignes de champs SSE (data:, event:, id:, retry:) → seules les valeurs
     des lignes data: sont retenues (marqueur data: [DONE] et lignes vides
     filtrés ; la ligne vide sépare les événements) ;
  3. chaque ligne data: est d'abord parsée individuellement (cas dominant
     réel : un JSON complet par ligne — jamais de concaténation brute) ;
  4. lignes non parsables → repli groupé : jointure \n (vrai événement
     multi-lignes SSE) puis sans séparateur ;
  5. encore non parsable → dernier recours : extraction du premier bloc
     {...} équilibré ;
  6. sortie : payload unique → JSON compact ; plusieurs → tableau JSON ;
     zéro → rc 2 avec diagnostic (trame partielle : attendre la suite du flux).

Sécurité par construction :
  1. stdlib uniquement, déterministe, aucune écriture hors stdout/stderr ;
  2. idempotent : la sortie réinjectée en entrée est un no-op (déjà propre) ;
  3. jamais de re-jeu à l'identique de la commande bloquante sans
     assainissement (règle KO-L011 — l'erreur de format est déterministe).

Codes retour : 0 = succès (ou signature détectée) ; 1 = signature absente
(detect) ; 2 = aucun JSON récupérable (sanitize) ; 3 = appel invalide.
"""

import json
import re
import sys

CHAMPS_SSE = ("data:", "event:", "id:", "retry:")
MARQUEUR_FIN = "[DONE]"
# Signature de l'erreur (toute langue) : SyntaxError + « data: » dans le message.
RE_SIGNATURE = re.compile(r"SyntaxError", re.IGNORECASE)
RE_DATA_DANS_ERREUR = re.compile(r"data\s*:", re.IGNORECASE)
# Repli : premier bloc objet équilibré (accolades comptées, chaînes respectées).
RE_BLOC_OBJET = re.compile(r"\{[^{}]*\}", re.DOTALL)


def extraire_payloads(texte: str) -> list:
    """Extrait les payloads JSON d'une trame SSE (ou passe une entrée propre).

    Retourne la liste des payloads parsés (objets Python) ; liste vide si
    aucun n'est récupérable (trame partielle, entrée non-JSON).
    """
    texte = texte.strip() if texte else ""
    if not texte:
        return []

    # (1) entrée déjà propre : JSON unique valide → passerelle (idempotence)
    try:
        charge = json.loads(texte)
        return [charge] if isinstance(charge, (dict, list)) else [charge]
    except (json.JSONDecodeError, ValueError):
        pass

    # (2) regroupement par événement : lignes data: jointes par saut de ligne
    lignes = texte.splitlines()
    evenements = []
    courant = []
    for ligne in lignes:
        propre = ligne.strip()
        if not propre:
            # séparateur d'événement SSE
            if courant:
                evenements.append(courant)
                courant = []
            continue
        champ = None
        for c in CHAMPS_SSE:
            if propre.lower().startswith(c):
                champ = c
                break
        if champ == "data:":
            valeur = propre[len("data:"):].strip()
            if valeur == MARQUEUR_FIN:
                continue
            courant.append(valeur)
        # autres champs SSE (event/id/retry) : ignorés
    if courant:
        evenements.append(courant)

    # (3) parse par événement : individuellement d'abord (cas dominant réel :
    #     un JSON complet par ligne data:), groupage en repli (vrai événement
    #     multi-lignes SSE), puis extraction de bloc équilibré en dernier recours
    payloads = []
    for parties in evenements:
        individuels = []
        for candidat in parties:
            try:
                individuels.append(json.loads(candidat))
            except (json.JSONDecodeError, ValueError):
                individuels.append(None)
        if all(p is not None for p in individuels) and individuels:
            # chaque ligne est un JSON complet → payloads distincts
            payloads.extend(individuels)
            continue
        # repli groupé : jointure \n (spécification SSE) puis sans séparateur,
        # sur les lignes non parsées individuellement (dans l'ordre d'origine)
        restants = [c for c, p in zip(parties, individuels) if p is None]
        pour_cet_evenement = None
        if restants:
            for candidat in ["\n".join(restants), "".join(restants)]:
                try:
                    pour_cet_evenement = json.loads(candidat)
                    break
                except (json.JSONDecodeError, ValueError):
                    continue
        if pour_cet_evenement is None and restants:
            # dernier recours : extraction du premier bloc objet équilibré
            for candidat in restants:
                bloc = RE_BLOC_OBJET.search(candidat)
                if bloc:
                    try:
                        pour_cet_evenement = json.loads(bloc.group(0))
                        break
                    except (json.JSONDecodeError, ValueError):
                        continue
        # les lignes individuellement valides restent des payloads à part entière
        payloads.extend(p for p in individuels if p is not None)
        if pour_cet_evenement is not None:
            payloads.append(pour_cet_evenement)
    return payloads


def cmd_sanitize(chemin: str) -> int:
    """Assainit une trame SSE (fichier ou stdin) et émet le JSON propre."""
    if chemin == "-":
        texte = sys.stdin.read()
    else:
        try:
            with open(chemin, "r", encoding="utf-8", errors="replace") as f:
                texte = f.read()
        except OSError as e:
            print(f"ERREUR : lecture impossible {chemin} — {e}", file=sys.stderr)
            return 3
    payloads = extraire_payloads(texte)
    if not payloads:
        # diagnostic honnête : trame partielle ou aucun JSON
        extrait = texte[:60].replace("\n", "\\n")
        print(
            "AUCUN-JSON-RÉCUPÉRABLE — trame partielle ou non-JSON "
            f"(extrait : {extrait!r}) ; KO-L011 : attendre la suite du flux, "
            "ré-extraire le dernier payload complet, ou basculer sur une voie "
            "non-streaming (max 2 rounds — garde anti-boucle SHARED §4.4)",
            file=sys.stderr,
        )
        return 2
    if len(payloads) == 1:
        print(json.dumps(payloads[0], ensure_ascii=False, separators=(",", ":")))
    else:
        print(json.dumps(payloads, ensure_ascii=False, separators=(",", ":")))
    return 0


def cmd_detect(texte: str) -> int:
    """Détecte la signature de l'erreur KO-L011 dans un message d'erreur."""
    if RE_SIGNATURE.search(texte) and RE_DATA_DANS_ERREUR.search(texte):
        print("SIGNATURE KO-L011 PRÉSENTE — erreur de parsing SSE/JSON : "
              "assainir avant re-jeu (adaptation-json-sse.py sanitize), "
              "jamais de re-jeu à l'identique")
        return 0
    print("signature KO-L011 absente", file=sys.stderr)
    return 1


def cmd_selftest() -> int:
    """Golden samples embarqués — reproduction littérale des cas réels."""
    cas = [
        # (nom, entrée, attendu_payloads_ou_None, rc_attendu)
        (
            "trame-exacte-propriétaire (partielle)",
            'data: {"da',
            None,
            2,
        ),
        (
            "trame-streaming-complète",
            'data: {"delta":"Bonjour"}\ndata: {"delta":" !"}\ndata: [DONE]\n',
            [{"delta": "Bonjour"}, {"delta": " !"}],
            0,
        ),
        (
            "payload-unique",
            'data: {"ok": true}\n\n',
            [{"ok": True}],
            0,
        ),
        (
            "entrée-déjà-propre (idempotence passerelle)",
            '{"ok": true}',
            [{"ok": True}],
            0,
        ),
        (
            "champs-non-data ignorés",
            'event: delta\nid: 7\nretry: 1000\ndata: {"n": 7}\n\n',
            [{"n": 7}],
            0,
        ),
        (
            "payload-corrompu → repli bloc équilibré",
            'data: préfixe parasite {"n": 9} suffixe\n',
            [{"n": 9}],
            0,
        ),
        (
            "événement-multi-lignes (SSE)",
            'data: {"a":\ndata: 1}\n\n',
            [{"a": 1}],
            0,
        ),
        (
            "entrées-non-JSON pures",
            "hello world\n",
            None,
            2,
        ),
    ]
    echecs = 0
    for nom, entree, attendu, rc_attendu in cas:
        payloads = extraire_payloads(entree)
        rc = 0 if payloads else 2
        conforme = (
            (attendu is None and not payloads)
            or (attendu is not None and payloads == attendu)
        ) and rc == rc_attendu
        if not conforme:
            echecs += 1
            print(f"  [FAIL] {nom} — obtenu {payloads!r} (rc {rc}), "
                  f"attendu {attendu!r} (rc {rc_attendu})")
        else:
            print(f"  [PASS] {nom}")
    # détection de signature — messages réels FR/EN
    signatures = [
        "SyntaxError : Token inattendu 'd', « data : {\"da »... est pas valide en JSON",
        "SyntaxError: Unexpected token 'd', \"data: {\"da\"... is not valid JSON",
    ]
    for sig in signatures:
        if cmd_detect_quiet(sig):
            print(f"  [PASS] signature détectée — {sig[:42]}…")
        else:
            echecs += 1
            print(f"  [FAIL] signature NON détectée — {sig[:42]}…")
    # contre-échantillon : SyntaxError Python (classe adaptation-syntaxe.py) ≠ KO-L011
    contre = "SyntaxError: invalid syntax (fichier.py, line 3)"
    if cmd_detect_quiet(contre):
        echecs += 1
        print("  [FAIL] contre-échantillon — SyntaxError Python détecté à tort "
              "comme KO-L011")
    else:
        print("  [PASS] contre-échantillon — SyntaxError Python hors signature "
              "KO-L011 (classe adaptation-syntaxe.py)")
    total = len(cas) + 3
    print(f"SELFTEST : {'PASS' if echecs == 0 else 'FAIL'} — "
          f"{total - echecs}/{total}")
    return 0 if echecs == 0 else 1


def cmd_detect_quiet(texte: str) -> bool:
    """Variante silencieuse de cmd_detect pour le selftest."""
    return bool(
        RE_SIGNATURE.search(texte) and RE_DATA_DANS_ERREUR.search(texte)
    )


def main() -> int:
    """Point d'entrée : route les sous-commandes (sanitize/detect/--selftest)."""
    args = sys.argv[1:]
    if not args:
        usage = "Usage : adaptation-json-sse.py sanitize <fichier|->"
        usage += " | detect <texte> | --selftest"
        print(usage, file=sys.stderr)
        return 3
    if args[0] == "--selftest":
        return cmd_selftest()
    if args[0] == "sanitize" and len(args) == 2:
        return cmd_sanitize(args[1])
    if args[0] == "detect" and len(args) >= 2:
        return cmd_detect(" ".join(args[1:]))
    print("appel invalide — voir --selftest", file=sys.stderr)
    return 3


if __name__ == "__main__":
    sys.exit(main())
