#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.7)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.

alias-manager.py — Gestionnaire mécanique du système d'alias $<ALIAS> (skill alias-eco v1.2.0).

Directive propriétaire 2026-10-23 : remplacer les grandes phrases récurrentes des
discussions par des alias au format $<ALIAS> (ex : « mon écosystème personnel » →
$ECO-LEON). Le gestionnaire :
  - détecte les phrases récurrentes (n-grammes maximaux, >= 3 occurrences,
    >= 3 mots, >= 12 caractères — règle SKILL.md §1.4) ;
  - liste, TRIE par ordre alphabétique et DÉDUPLIQUE (aucun doublon strictement
    identique, normalisation espaces/ponctuation d'extrémité) en JSON ;
  - sauvegarde le registre dans skills/@historique/@Alias/aliases.json
    (dossier @ = infrastructure non-skill, SHARED §1.2 — racine dérivée de
    l'emplacement du script : fonctionne au dépôt comme au profil local) ;
  - « alias-eco (chat) » (--chat) : exporte en plus une liste TXT de toutes les
    phrases récurrentes de la discussion, triée par ordre alphabétique
    (download/alias-eco-chat-<date>.txt) ;
  - résout les $<ALIAS> d'un texte (--resolve) ;
  - attribue un alias explicitement (--add — l'alias n'est JAMAIS inventé par
    la détection, règle §1.4.4) ou via la GRAMMAIRE B (--trigger, v1.2.0 —
    `alias-eco "<texte>" --add <ALIAS>`, variantes « » / $ALIAS, GO propriétaire) ;
  --selftest : tests internes sur fixtures (aucune écriture du registre réel).

Codes retour : 0 OK · 1 échec (selftest/assert) · 2 usage invalide.
Idempotence : re-scan d'une même entrée = registre stable (occurrences du
dernier scan mises à jour, cumul incrémenté, alias préservés, tri stable).
"""
import json
import os
import re
import sys
from datetime import date

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
ALIAS_DIR = os.path.join(BASE, "skills", "@historique", "@Alias")
JSON_PATH = os.path.join(ALIAS_DIR, "aliases.json")
DOWNLOAD = os.path.join(BASE, "download")

ALIAS_RE = re.compile(r"\$([A-Z0-9][A-Z0-9-]*)")
ALIAS_NAME_RE = re.compile(r"^[A-Z0-9][A-Z0-9-]*$")
WORDCHAR_RE = re.compile(r"[\wàâäéèêëîïôöùûüçÀÂÄÉÈÊËÎÏÔÖÙÛÜÇ]", re.UNICODE)
SENT_FINAL = ".!?…"
MIN_OCC = 3
MIN_WORDS = 3
MIN_CHARS = 12
MAX_N = 10


def normalize_key(phrase):
    """Clé de déduplication stricte : espaces repliés, ponctuation d'extrémité retirée."""
    s = re.sub(r"\s+", " ", phrase.strip())
    s = s.strip(" \t\n\r,;:.!?…«»\"'()[]")
    return s


def sort_key(phrase):
    return phrase.casefold()


def load_registry():
    if os.path.isfile(JSON_PATH):
        with open(JSON_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {"format": "aliases-eco v1", "mis_a_jour": None, "source": "alias-eco v1.1.0",
            "phrases": []}


def save_registry(reg):
    reg["phrases"] = sorted(reg["phrases"], key=lambda e: sort_key(e["phrase"]))
    seen = set()
    dedup = []
    for e in reg["phrases"]:  # garde anti-doublon strict (SKILL.md §1.4.2)
        k = normalize_key(e["phrase"])
        if k in seen:
            continue
        seen.add(k)
        dedup.append(e)
    reg["phrases"] = dedup
    reg["mis_a_jour"] = date.today().isoformat()
    os.makedirs(ALIAS_DIR, exist_ok=True)
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(reg, f, ensure_ascii=False, indent=2, sort_keys=False)
        f.write("\n")


def tokens(text):
    """Tokénisation par espaces — ponctuation ATTACHÉE aux mots (les virgules restent
    intra-phrase : « de façon cohérente, optimisée et fonctionnelle » est UN n-gramme)."""
    return text.split()


def is_word(tok):
    """Un token est un mot s'il contient au moins un caractère alphabétique/chiffre."""
    return bool(WORDCHAR_RE.search(tok))


def is_sentence_final(tok):
    """Token final de phrase (. ! ? …) — interdit AU MILIEU d'un n-gramme (garde
    anti-franchissement de phrase : jamais de phrase candidate à cheval sur 2 phrases)."""
    return tok and tok[-1] in SENT_FINAL


def detect_phrases(text, min_occ=MIN_OCC):
    """N-grammes maximaux de mots répétés >= min_occ (>= MIN_WORDS mots, >= MIN_CHARS car.).

    Candidats = fenêtres glissantes de tokens (ponctuation attachée) répétées >= min_occ,
    sans token final-de-phrase en position interne ; la clé de comptage est la phrase
    normalisée (casse repliée, ponctuation d'extrémité retirée) ; les candidats
    sous-chaînes d'un candidat plus long sont retirés (n-grammes MAXIMAUX)."""
    toks = tokens(text)
    n_tok = len(toks)
    counts = {}
    for n in range(MIN_WORDS, MAX_N + 1):
        if n > n_tok:
            break
        for i in range(n_tok - n + 1):
            gram = toks[i:i + n]
            if not all(is_word(t) for t in gram):
                continue
            if any(is_sentence_final(t) for t in gram[:-1]):
                continue  # franchissement de phrase — rejeté
            phrase = " ".join(gram)
            if len(normalize_key(phrase)) < MIN_CHARS:
                continue
            key = normalize_key(phrase).casefold()
            counts.setdefault(key, {"rep": phrase, "n": n, "pos": []})
            counts[key]["pos"].append(i)
    # candidats : occurrences >= min_occ
    cands = {k: v for k, v in counts.items() if len(v["pos"]) >= min_occ}
    # n-grammes maximaux : retirer tout candidat sous-chaîne d'un candidat plus long
    kept = {}
    for k, v in sorted(cands.items(), key=lambda kv: -kv[1]["n"]):
        sub = False
        for k2 in kept:
            if (" %s " % k) in (" %s " % k2):
                sub = True
                break
        if not sub:
            kept[k] = v
    # représentant : première occurrence, ponctuation d'extrémité retirée (naturelle)
    reps = {}
    for k, v in kept.items():
        m = re.search(re.escape(v["rep"]).replace(r"\ ", r"\s+"), text, re.IGNORECASE)
        rep = m.group(0) if m else v["rep"]
        reps[k] = (rep.strip(" \t\n\r,;:.!?…«»\"'()[]"), len(v["pos"]))
    return reps


def merge_scan(reg, reps, src):
    today = date.today().isoformat()
    by_key = {normalize_key(e["phrase"]).casefold(): e for e in reg["phrases"]}
    for k, (rep, occ) in reps.items():
        e = by_key.get(k)
        if e is None:
            e = {"phrase": rep, "alias": None, "occurrences": occ,
                 "occurrences_cumulees": occ, "premiere_detection": today,
                 "derniere_detection": today, "source": src}
            reg["phrases"].append(e)
            by_key[k] = e
        else:
            e["occurrences"] = occ
            e["occurrences_cumulees"] = e.get("occurrences_cumulees", occ) + occ
            e["derniere_detection"] = today
    save_registry(reg)


def cmd_resolve(text):
    reg = load_registry()
    amap = {e["alias"]: e["phrase"] for e in reg["phrases"] if e.get("alias")}

    def sub(m):
        return amap.get(m.group(1), m.group(0))
    out = ALIAS_RE.sub(sub, text)
    unknown = [m.group(1) for m in ALIAS_RE.finditer(text) if m.group(1) not in amap]
    print(out)
    if unknown:
        print("[NOTE] alias non enregistrés (laissés tels quels) : %s"
              % ", ".join("$" + a for a in unknown), file=sys.stderr)
        sys.exit(1)
    return 0


def cmd_list():
    reg = load_registry()
    n_alias = sum(1 for e in reg["phrases"] if e.get("alias"))
    print("Registre des alias (%d phrases, %d alias) — %s"
          % (len(reg["phrases"]), n_alias, JSON_PATH))
    for e in reg["phrases"]:
        mark = "$%s" % e["alias"] if e.get("alias") else "—"
        print("  %-12s %s" % (mark, e["phrase"]))
    return 0


GRAMMAIRE_B_RE = re.compile(
    r'^alias-eco\s+(?:«\s*(.+?)\s*»|"(.*?)")\s*--add\s+\$?([A-Za-z0-9()çéèêëàâäùûüôöîï\-]+)\s*$',
    re.S)


def cmd_trigger(expression):
    """Grammaire B (v1.2.0, GO propriétaire) : parse et applique.
    rc 0 = attribué · rc 2 = expression mal formée ou alias hors format."""
    m = GRAMMAIRE_B_RE.match(expression.strip())
    if not m:
        print("ABANDON : expression grammaire B mal formée (attendu : "
              "alias-eco \"<texte>\" --add <ALIAS>)", file=sys.stderr)
        return 2
    texte = m.group(1) if m.group(1) is not None else m.group(2)
    return cmd_add(m.group(3), texte)


def cmd_add(alias, phrase):
    if not ALIAS_NAME_RE.match(alias):
        print("ABANDON : format d'alias invalide %r (attendu ^[A-Z0-9][A-Z0-9-]*$)" % alias,
              file=sys.stderr)
        return 2
    reg = load_registry()
    k = normalize_key(phrase).casefold()
    for e in reg["phrases"]:
        if normalize_key(e["phrase"]).casefold() == k:
            e["alias"] = alias
            e["source"] = e.get("source", "") + " ; alias attribué %s" % date.today().isoformat()
            save_registry(reg)
            print("Alias mis à jour : $%s = %s" % (alias, e["phrase"]))
            return 0
    reg["phrases"].append({"phrase": phrase, "alias": alias, "occurrences": 0,
                           "occurrences_cumulees": 0, "premiere_detection": date.today().isoformat(),
                           "derniere_detection": date.today().isoformat(),
                           "source": "attribution manuelle %s" % date.today().isoformat()})
    save_registry(reg)
    print("Alias enregistré : $%s = %s" % (alias, phrase))
    return 0


def read_inputs(paths):
    parts = []
    for p in paths:
        with open(p, encoding="utf-8", errors="replace") as f:
            parts.append(f.read())
    return "\n".join(parts)


def cmd_scan(paths, chat=False):
    text = read_inputs(paths)
    reps = detect_phrases(text)
    reg = load_registry()
    merge_scan(reg, reps, "scan %s" % ", ".join(os.path.basename(p) for p in paths))
    print("Registre mis à jour : %d phrases récurrentes détectées (total %d)"
          % (len(reps), len(reg["phrases"])))
    if chat:  # mode « alias-eco (chat) » : liste TXT triée alphabétiquement
        os.makedirs(DOWNLOAD, exist_ok=True)
        out_txt = os.path.join(DOWNLOAD, "alias-eco-chat-%s.txt" % date.today().isoformat())
        with open(out_txt, "w", encoding="utf-8") as f:
            f.write("alias-eco (chat) — phrases récurrentes de la discussion (tri alphabétique)\n")
            f.write("Source : %s · %s\n" % (", ".join(paths), date.today().isoformat()))
            f.write("=" * 72 + "\n")
            for e in reg["phrases"]:
                line = e["phrase"]
                if e.get("alias"):
                    line += "  [$%s]" % e["alias"]
                f.write(line + "\n")
        print("Liste TXT (tri alphabétique) : %s (%d phrases)" % (out_txt, len(reg["phrases"])))
    return 0


def selftest():
    """Tests internes sur fixtures — AUCUNE écriture du registre réel (tmp isolé)."""
    global JSON_PATH, ALIAS_DIR, DOWNLOAD
    import tempfile
    tmp = tempfile.mkdtemp(prefix="alias-eco-selftest-")
    ALIAS_DIR = os.path.join(tmp, "alias")
    JSON_PATH = os.path.join(ALIAS_DIR, "aliases.json")
    DOWNLOAD = tmp
    fixture = (" optimise mon écosystème personnel de façon cohérente. "
               "optimise mon écosystème personnel de façon cohérente. "
               "optimise mon écosystème personnel de façon cohérente. "
               "installe de façon cohérente, optimisée et fonctionnelle. "
               "installe de façon cohérente, optimisée et fonctionnelle. "
               "installe de façon cohérente, optimisée et fonctionnelle. "
               "phrase unique sans répétition ici. ")
    reps = detect_phrases(fixture)
    ok = []
    keys = [normalize_key(p).casefold() for p in reps]
    ok.append(("détection ≥ 2 phrases récurrentes", len(reps) >= 2))
    ok.append(("détection contient la phrase écosystème",
               any("écosystème personnel" in k for k in keys)))
    ok.append(("détection contient la phrase virgule intra-phrase",
               any("cohérente, optimisée et fonctionnelle" in k for k in keys)))
    ok.append(("phrase unique NON détectée",
               not any("phrase unique" in k for k in keys)))
    ok.append(("jamais de phrase à cheval sur 2 phrases",
               not any(k.endswith("cohérente.") or " ici optimise " in k for k in keys)))
    # tri + déduplication + sauvegarde
    reg = load_registry()
    merge_scan(reg, reps, "selftest")
    loaded = json.load(open(JSON_PATH, encoding="utf-8"))
    phrases = [e["phrase"] for e in loaded["phrases"]]
    ok.append(("registre trié alphabétiquement", phrases == sorted(phrases, key=sort_key)))
    ok.append(("zéro doublon strict", len(phrases) == len(set(map(normalize_key, phrases)))))
    # re-scan idempotent (mêmes phrases, pas de doublon)
    reps2 = detect_phrases(fixture)
    merge_scan(loaded, reps2, "selftest-2")
    loaded2 = json.load(open(JSON_PATH, encoding="utf-8"))
    ok.append(("re-scan sans doublon", len(loaded2["phrases"]) == len(phrases)))
    # alias + résolution
    target = [e for e in loaded2["phrases"] if "écosystème" in e["phrase"]]
    ok.append(("phrase cible présente", len(target) == 1))
    if target:
        cmd_add_output = None
        r = cmd_add("ECO-TEST", target[0]["phrase"])
        ok.append(("ajout alias rc=0", r == 0))
        reg3 = load_registry()
        amap = {e["alias"]: e["phrase"] for e in reg3["phrases"] if e.get("alias")}
        out = ALIAS_RE.sub(lambda m: amap.get(m.group(1), m.group(0)), "de $ECO-TEST local")
        ok.append(("résolution $ECO-TEST", "écosystème" in out and "$ECO-TEST" not in out))
        ok.append(("garde format alias", cmd_add("invalide", "x") == 2))
    # grammaire B (v1.2.0) : parse + gardes
    g1 = cmd_trigger('alias-eco "phrase test grammaire" --add G-B-TEST')
    ok.append(("grammaire B rc=0", g1 == 0))
    reg_g = load_registry()
    ok.append(("grammaire B alias enregistré",
               any(e.get("alias") == "G-B-TEST" and "grammaire" in e["phrase"] for e in reg_g["phrases"])))
    ok.append(("grammaire B variante « » + $ALIAS",
               cmd_trigger('alias-eco «phrase test bis» --add $G-B-TEST2') == 0))
    ok.append(("grammaire B texte avec --add interne",
               cmd_trigger('alias-eco "écrire --add ici est du texte" --add G-B-TEST3') == 0))
    ok.append(("grammaire B alias hors format (façon()) rejeté",
               cmd_trigger('alias-eco "x" --add façon()') == 2))
    ok.append(("grammaire B expression mal formée rejetée",
               cmd_trigger('alias-eco (chat)') == 2))
    # mode chat : TXT trié
    src = os.path.join(tmp, "chat.txt")
    with open(src, "w", encoding="utf-8") as f:
        f.write(fixture)
    r = cmd_scan([src], chat=True)
    txt = os.path.join(DOWNLOAD, "alias-eco-chat-%s.txt" % date.today().isoformat())
    ok.append(("mode chat rc=0", r == 0))
    lines = [l.rstrip("\n") for l in open(txt, encoding="utf-8").read().splitlines()
             if l and not l.startswith("=") and not l.startswith("alias-eco (chat)")
             and not l.startswith("Source :")]
    bodies = [re.sub(r"\s*\$\[?[A-Z0-9-]+\]?$", "", l).strip() for l in lines]
    ok.append(("TXT trié alphabétiquement", bodies == sorted(bodies, key=sort_key)))
    ok.append(("TXT sans doublon", len(bodies) == len(set(bodies))))
    fails = [name for name, passed in ok if not passed]
    for name, passed in ok:
        print("  [%s] %s" % ("PASS" if passed else "FAIL", name))
    print("SELFTEST : %d/%d PASS" % (len(ok) - len(fails), len(ok)))
    import shutil
    shutil.rmtree(tmp, ignore_errors=True)
    return 1 if fails else 0


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2
    if args[0] == "--selftest":
        return selftest()
    if args[0] == "--resolve":
        if len(args) < 2:
            print("usage : --resolve \"<texte>\"", file=sys.stderr)
            return 2
        return cmd_resolve(" ".join(args[1:]))
    if args[0] == "--list":
        return cmd_list()
    if args[0] == "--add":
        if len(args) < 3:
            print("usage : --add <ALIAS> \"<phrase>\"", file=sys.stderr)
            return 2
        return cmd_add(args[1], " ".join(args[2:]))
    if args[0] == "--trigger":
        if len(args) < 2:
            print('usage : --trigger "alias-eco \\"<texte>\\" --add <ALIAS>"', file=sys.stderr)
            return 2
        return cmd_trigger(" ".join(args[1:]))
    if args[0] in ("--scan", "--chat"):
        if len(args) < 2:
            print("usage : %s <fichier>…" % args[0], file=sys.stderr)
            return 2
        return cmd_scan(args[1:], chat=(args[0] == "--chat"))
    print("commande inconnue : %s" % args[0], file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
