#!/usr/bin/env python3
"""traduire-md-zh-fr.py — Traduction des skills .md chinois vers le français via backends gratuits (z-ai LLM → googletrans → gtx → MyMemory).

Conventions script-creator : Python stdlib uniquement (N3), idempotent ×2 (GF-3),
--dry/--exec/--selftest, journal JSON append-only.
Politique P1/P2 (chantier P2 francisation) : traduire la PROSE, conserver les
données fonctionnelles — blocs de code, code en ligne, URLs, valeurs chiffrées.

Chaîne de backends (v1.1.0 — optimisation G5/G6, recherche 2026-11-01) :
  1. zai        — CLI `z-ai chat` (LLM glm de l'écosystème, qualité maximale, sans quota 429)
  2. googletrans — conformément à la directive propriétaire (paquet dysfonctionnel détecté par la garde)
  3. gtx        — endpoint Google Translate public (sans clé)
  4. mymemory   — MyMemory API publique (sans clé)
  + hors-ligne : Argos Translate recommandé sur la machine du propriétaire (pivot ZH→EN→FR intégré — voir rapport G5)

Usage :
    traduire-md-zh-fr.py --dry   --fichier <md> [md ...] [--racine DIR] [--seuil N]
    traduire-md-zh-fr.py --exec  --fichier <md> [md ...] [--journal PATH] [--cache PATH]
    traduire-md-zh-fr.py --selftest
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone

# ---------------------------------------------------------------- constantes
RE_CJK = re.compile(r"[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]")
RE_URL = re.compile(r"(https?://[^\s\)\]]+|<[^>]+>|`[^`]+`|\[\d+\])")
SEUIL_CJK = 20
SEUIL_FUSION = 3000  # caractères max par requête (fusion de segments)
SEUIL_RATIO_CJK = 0.08  # P2 : segment déjà francisé si les CJK pèsent < 8 % (termes résiduels) — optimisation G6 issue du test réel
DEBIT_S = 0.25       # intervalle minimal entre requêtes (≤ 4 req/s, garde 5 req/s Google)
BACKOFF = [2, 5, 12]  # secondes, 3 tentatives par segment

BACKENDS = ("zai", "googletrans", "gtx", "mymemory")

SYSTEME_ZAI = ("Tu es un traducteur technique chinois→français expert. Traduis fidèlement le texte "
               "fourni en français, registre technique, sans ajouter ni omettre d'information. "
               "Conserve tels quels : les URLs, le code, les noms de fichiers, les valeurs chiffrées "
               "et les jetons de protection \u2063N\u2063. Réponds UNIQUEMENT avec la traduction.")


# ---------------------------------------------------------------- utilitaires
def compter_cjk(texte: str) -> int:
    return len(RE_CJK.findall(texte))


def limiter_urls(segments: str) -> tuple[str, list[str]]:
    """Masque URLs / inline code / balises avant traduction, retourne (texte, jetons)."""
    jetons: list[str] = []

    def _sub(m: re.Match) -> str:
        jetons.append(m.group(0))
        return f"\u2063{len(jetons) - 1}\u2063"

    return RE_URL.sub(_sub, segments), jetons


def restaurer_urls(texte: str, jetons: list[str]) -> str:
    def _sub(m: re.Match) -> str:
        return jetons[int(m.group(1))]

    return re.sub("\u2063(\\d+)\u2063", _sub, texte)


class Debit:
    """Limiteur de débit — intervalle minimal entre deux requêtes."""

    def __init__(self, intervalle: float) -> None:
        self.intervalle = intervalle
        self.dernier = 0.0

    def attendre(self) -> None:
        delta = time.monotonic() - self.dernier
        if delta < self.intervalle:
            time.sleep(self.intervalle - delta)
        self.dernier = time.monotonic()


# ---------------------------------------------------------------- backends
def _http_get(url: str, timeout: int = 25) -> str:
    req = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) traduction-zh-fr/1.0"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as rep:
        return rep.read().decode("utf-8")


def _traduire_zai(texte: str, limiteur: Debit) -> str:
    """Backend z-ai chat (LLM glm de l'écosystème — le plus qualitatif, sans quota 429)."""
    if not shutil.which("z-ai"):
        raise RuntimeError("CLI z-ai absent")
    limiteur.attendre()
    fd, chemin = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    try:
        r = subprocess.run(
            ["z-ai", "chat", "-s", SYSTEME_ZAI,
             "-p", "Traduis en français, réponds uniquement avec la traduction :\n" + texte,
             "--output", chemin],
            capture_output=True, text=True, timeout=150,
        )
        if r.returncode != 0:
            raise RuntimeError(f"z-ai rc={r.returncode} : {r.stderr.strip()[-150:]}")
        with open(chemin, encoding="utf-8") as f:
            data = json.load(f)
        dst = data["choices"][0]["message"]["content"].strip()
    finally:
        os.unlink(chemin)
    if not dst:
        raise RuntimeError("z-ai : réponse vide")
    return dst


def _traduire_gtx(texte: str, limiteur: Debit) -> str:
    """Backend endpoint gtx (Google Translate public, sans clé)."""
    params = urllib.parse.urlencode(
        {"client": "gtx", "sl": "zh-CN", "tl": "fr", "dt": "t", "q": texte}
    )
    limiteur.attendre()
    brut = _http_get(f"https://translate.googleapis.com/translate_a/single?{params}")
    data = json.loads(brut)
    return "".join(seg[0] for seg in data[0] if seg and seg[0])


def _traduire_mymemory(texte: str, limiteur: Debit) -> str:
    """Backend MyMemory API publique (gratuit, sans clé, ≤ 500 car/requête)."""
    sortie: list[str] = []
    for morceau in re.findall(r".{1,490}", texte):
        params = urllib.parse.urlencode({"q": morceau, "langpair": "zh-CN|fr-FR"})
        limiteur.attendre()
        brut = _http_get(f"https://api.mymemory.translated.net/get?{params}")
        data = json.loads(brut)
        sortie.append(data["responseData"]["translatedText"])
    return " ".join(sortie)


def _traduire_googletrans(texte: str, limiteur: Debit) -> str:
    """Backend googletrans (conformément à la directive propriétaire — optionnel)."""
    import asyncio

    from googletrans import Translator  # type: ignore[import-untyped]

    async def _une() -> str:
        rep = await Translator().translate(texte, src="zh-CN", dest="fr")
        if not rep.text or rep.text == texte:
            raise RuntimeError("googletrans : texte source renvoyé inchangé (paquet dysfonctionnel)")
        return rep.text

    limiteur.attendre()
    return asyncio.run(_une())


def _import_ok(nom: str) -> bool:
    try:
        __import__(nom)
        return True
    except ImportError:
        return False


def traduire_texte(texte: str, cache: dict, stat: dict, journalise=None) -> str:
    """Traduit un segment via la chaîne de backends + cache persistant."""
    cle = hashlib.sha256(f"zh-CN|fr|{texte}".encode()).hexdigest()
    if cle in cache:
        stat["cache"] += 1
        return cache[cle]["dst"]
    erreur_derniere: Exception | None = None
    for nom in BACKENDS:
        if nom == "googletrans" and not _import_ok("googletrans"):
            continue
        if nom == "zai" and not shutil.which("z-ai"):
            continue
        try:
            limiteur = stat["limiteur"]
            dst = globals()[f"_traduire_{nom}"](texte, limiteur)
        except Exception as exc:  # noqa: BLE001 — chaîne de repli volontaire
            erreur_derniere = exc
            if journalise:
                journalise(f"backend {nom} KO : {exc}")
            continue
        if dst and dst != texte:
            cache[cle] = {"dst": dst, "backend": nom, "ts": datetime.now(timezone.utc).isoformat()}
            stat["requetes"] += 1
            return dst
        if nom == "zai" and dst == texte:
            # Verdict d'identité du LLM de confiance (tête de chaîne) : rien à traduire
            # (prose déjà francisée ou données fonctionnelles P2) — segment conservé tel
            # quel, SANS échec (optimisation G6 issue du test réel — re-jeux idempotents).
            cache[cle] = {"dst": texte, "backend": "zai-identité", "ts": datetime.now(timezone.utc).isoformat()}
            stat["inchangés"] = stat.get("inchangés", 0) + 1
            if journalise:
                journalise("backend zai : verdict identité — rien à traduire (P2/déjà francisé), segment conservé")
            return texte
        if journalise:
            journalise(f"backend {nom} : texte inchangé ou vide (repli — segment déjà traduit ou données P2)")
    raise RuntimeError(f"tous les backends ont échoué : {erreur_derniere}")


# ---------------------------------------------------------------- markdown
def decouper_markdown(texte: str) -> list[tuple[str, bool]]:
    """Découpe en blocs ; booléen = bloc à TRADUIRE (prose) ou CONSERVER (code)."""
    blocs: list[tuple[str, bool]] = []
    tampon: list[str] = []
    en_code = False
    for ligne in texte.splitlines(keepends=True):
        if ligne.lstrip().startswith("```"):
            if tampon:
                blocs.append(("".join(tampon), not en_code))
                tampon = []
            en_code = not en_code
            blocs.append((ligne, False))
            continue
        if en_code:
            blocs.append((ligne, False))
        else:
            tampon.append(ligne)
    if tampon:
        blocs.append(("".join(tampon), not en_code))
    return blocs


def traduire_markdown(texte: str, cache: dict, stat: dict, journalise=None) -> str:
    """Traduit la prose d'un .md ; code/URLs/inline code préservés (politique P1/P2)."""
    if texte.lstrip().startswith("---"):
        # frontmatter YAML : structure conservée, seule la prose du corps est traduite
        fin = texte.find("\n---", 3)
        if fin > 0:
            front, corps = texte[: fin + 4], texte[fin + 4 :]
            return front + _traduire_corps(corps, cache, stat, journalise)
    return _traduire_corps(texte, cache, stat, journalise)


def _traduire_corps(texte: str, cache: dict, stat: dict, journalise=None) -> str:
    sortie = []
    for bloc, a_traduire in decouper_markdown(texte):
        n_cjk = compter_cjk(bloc)
        if not a_traduire or n_cjk == 0 or n_cjk / max(len(bloc), 1) < SEUIL_RATIO_CJK:
            # P2 : bloc de code, sans CJK, ou prose déjà francisée avec termes résiduels — conservé tel quel
            sortie.append(bloc)
            continue
        brut, jetons = limiter_urls(bloc)
        morceaux, courant = [], ""
        for paragraphe in re.split(r"(\n\s*\n)", brut):
            if len(courant) + len(paragraphe) > SEUIL_FUSION and courant:
                morceaux.append(courant)
                courant = paragraphe
            else:
                courant += paragraphe
        if courant.strip():
            morceaux.append(courant)
        final = []
        for morceau in morceaux:
            cible = morceau.strip()
            if not cible:
                final.append(morceau)
                continue
            for tentative in range(3):
                try:
                    traduit = traduire_texte(cible, cache, stat, journalise)
                    final.append(morceau.replace(cible, traduit, 1))
                    break
                except Exception:
                    if tentative == 2:
                        raise
                    time.sleep(BACKOFF[tentative])
        sortie.append(restaurer_urls("".join(final), jetons))
    return "".join(sortie)


# ---------------------------------------------------------------- journal/cache
def charger_json(chemin: str, cle_defaut=None) -> dict:
    if os.path.exists(chemin):
        with open(chemin, encoding="utf-8") as f:
            return json.load(f)
    return cle_defaut if cle_defaut is not None else {}


def journaliser(journal: dict, chemin: str, entree: dict) -> None:
    journal.setdefault("traduction-zh-fr", {})
    journal["traduction-zh-fr"][entree["fichier"]] = entree
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(journal, f, ensure_ascii=False, indent=1)


# ---------------------------------------------------------------- selftest
def selftest() -> int:
    """Auto-test hors-ligne : logique prouvée sans réseau (backends simulés)."""
    echecs: list[str] = []

    def _verifier(nom: str, condition: bool) -> None:
        if not condition:
            echecs.append(nom)

    _verifier("detect-cjk", compter_cjk("hello world") == 0 and compter_cjk("这是测试") == 4)

    # Injection d'un backend simulé (hors-ligne) — la chaîne réelle googletrans→gtx→mymemory est conservée en production
    globals()["BACKENDS"] = ("gtx",)
    globals()["_traduire_gtx"] = lambda texte, limiteur: f"TRADUIT[{texte}]"

    md = ("---\ntitle: 测试\n---\n\n这是一个测试句子。\n\n"
          "```python\nprint('不要翻译我')\n```\n\nVoir https://exemple.cn/页面 `code 中式`\n")
    stat = {"cache": 0, "requetes": 0, "limiteur": Debit(0.01)}
    cache: dict = {}
    rep = traduire_markdown(md, cache, stat, None)
    _verifier("frontmatter-intact", rep.startswith("---\ntitle: 测试\n---\n"))
    _verifier("code-protect", "print('不要翻译我')" in rep)
    _verifier("url-protect", "https://exemple.cn/页面" in rep)
    _verifier("inline-protect", "`code 中式`" in rep)
    _verifier("run1-requetes", stat["requetes"] >= 1 and len(cache) >= 1)

    # idempotence ×2 : re-traduire avec le cache chaud = 0 requête réseau
    stat2 = {"cache": 0, "requetes": 0, "limiteur": Debit(0.01)}
    rep2 = traduire_markdown(md, cache, stat2, None)
    _verifier("idempotent-x2", stat2["requetes"] == 0 and stat2["cache"] >= 1 and rep2 == rep)

    # garde anti-surtraduction : les CJK résiduels = données protégées uniquement
    _verifier("residuels-protect", 0 < compter_cjk(rep) < SEUIL_CJK)

    if echecs:
        print("SELFTEST FAIL :", echecs)
        return 1
    print("SELFTEST PASS (8/8) — détection, frontmatter, code, URLs, inline, cache, idempotence ×2, seuil")
    return 0


# ---------------------------------------------------------------- main
def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--dry", action="store_true", help="rapport sans écriture")
    p.add_argument("--exec", dest="exec_mode", action="store_true", help="traduction effective")
    p.add_argument("--selftest", action="store_true", help="auto-test hors-ligne")
    p.add_argument("--fichier", action="append", default=[], help="fichier(s) .md cible(s)")
    p.add_argument("--racine", default=None, help="racine pour le journal (chemins relatifs)")
    p.add_argument("--seuil", type=int, default=SEUIL_CJK, help="seuil CJK minimal")
    p.add_argument("--cache", default=None, help="cache JSON persistant")
    p.add_argument("--journal", default=None, help="journal JSON (p2-etat.json compatible)")
    a = p.parse_args()

    if a.selftest:
        return selftest()
    if not (a.dry or a.exec_mode) or not a.fichier:
        p.print_usage()
        return 2

    racine = a.racine or os.getcwd()
    cache_chemin = a.cache or os.path.join(racine, "tmp", "cache-traduction-zh-fr.json")
    cache = charger_json(cache_chemin)
    journal = charger_json(a.journal) if a.journal else {}
    stat = {"cache": 0, "requetes": 0, "limiteur": Debit(DEBIT_S)}

    def _note(msg: str) -> None:
        print(f"  [note] {msg}", file=sys.stderr)

    rc = 0
    for fichier in a.fichier:
        rel = os.path.relpath(fichier, racine)
        if not os.path.exists(fichier):
            print(f"  ABSENT : {rel}")
            rc = 1
            continue
        texte = open(fichier, encoding="utf-8").read()
        n_avant = compter_cjk(texte)
        if n_avant < a.seuil:
            print(f"  SAUTE (< {a.seuil} CJK) : {rel} ({n_avant})")
            continue
        if a.dry:
            print(f"  DRY : {rel} — {n_avant} CJK, ~{n_avant // 500 + 1} requête(s) estimée(s)")
            continue
        sha_avant = hashlib.sha256(texte.encode()).hexdigest()
        try:
            traduit = traduire_markdown(texte, cache, stat, _note)
        except RuntimeError as exc:
            print(f"  ECHEC : {rel} — {exc}")
            rc = 1
            continue
        n_apres = compter_cjk(traduit)
        sha_apres = hashlib.sha256(traduit.encode()).hexdigest()
        with open(fichier, "w", encoding="utf-8") as f:
            f.write(traduit)
        if a.journal:
            journaliser(
                journal,
                a.journal,
                {
                    "fichier": rel,
                    "zh_avant": n_avant,
                    "sha_avant": sha_avant[:12],
                    "zh_apres": n_apres,
                    "statut": "TRADUIT",
                    "sha_apres": sha_apres[:12],
                    "outil": "traduction-zh-fr/traduire-md-zh-fr.py",
                    "ts": datetime.now(timezone.utc).isoformat(),
                },
            )
        print(f"  TRADUIT : {rel} — {n_avant} → {n_apres} CJK (cache {stat['cache']}, requêtes {stat['requetes']})")

    os.makedirs(os.path.dirname(cache_chemin) or ".", exist_ok=True)
    with open(cache_chemin, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=1)
    return rc


if __name__ == "__main__":
    sys.exit(main())
