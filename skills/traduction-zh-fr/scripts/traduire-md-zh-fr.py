#!/usr/bin/env python3
"""traduire-md-zh-fr.py — Traduction des skills .md chinois vers le français via backends gratuits (z-ai LLM → googletrans → gtx → MyMemory).

Conventions script-creator : Python stdlib uniquement (N3), idempotent ×2 (GF-3),
--dry/--exec/--selftest, journal JSON append-only.
Politique P1/P2 (chantier P2 francisation) : traduire la PROSE, conserver les
données fonctionnelles — blocs de code, code en ligne, URLs, valeurs chiffrées.

Chaîne de backends (v1.1.0 — optimisation G5/G6, recherche 2026-11-01 ; v1.2.0 — candidats du
rapport G5 livrés, E13 n°5 trace 1a1936e781a223a9) :
  1. zai        — CLI `z-ai chat` (LLM glm de l'écosystème, qualité maximale, sans quota 429)
  2. googletrans — conformément à la directive propriétaire (paquet dysfonctionnel détecté par la garde)
  3. gtx        — endpoint Google Translate public (sans clé)
  4. mymemory   — MyMemory API publique (sans clé)
  + hors-ligne : Argos Translate recommandé sur la machine du propriétaire (pivot ZH→EN→FR intégré — voir rapport G5)

Usage :
    traduire-md-zh-fr.py --dry   --fichier <md> [md ...] [--racine DIR] [--seuil N]
    traduire-md-zh-fr.py --exec  --fichier <md> [md ...] [--journal PATH] [--cache PATH]
                            [--glossaire glossaire.tsv] [--tmx memoire.tmx] [--src zh] [--dest fr]
    traduire-md-zh-fr.py --selftest

v1.2.0 (candidats du rapport G5 — livrés) : --glossaire (terminologie fixée : masquage
par jetons + restauration FR), --tmx (export TMX 1.4b de la mémoire de traduction),
--src/--dest (axes explicites ZH→FR [défaut], ZH→EN, EN→FR — garde par morceau
« mots vides » pour les sources latines : idempotence des re-jeux).
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
from xml.sax.saxutils import escape

# ---------------------------------------------------------------- constantes
RE_CJK = re.compile(r"[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]")
RE_URL = re.compile(r"(https?://[^\s\)\]]+|<[^>]+>|`[^`]+`|\[\d+\])")
SEUIL_CJK = 20
SEUIL_FUSION = 3000  # caractères max par requête (fusion de segments)
SEUIL_RATIO_CJK = 0.08  # P2 : segment déjà francisé si les CJK pèsent < 8 % (termes résiduels) — optimisation G6 issue du test réel
SEUIL_ECHO_CIBLE = 0.20  # v1.2.0 : écho du LLM sur segment MAJORITAIREMENT cible (CJK < 20 %) = conservation P2 ;
#                          un refus réel porte sur de la prose chinoise (observations G10 : ratio 0,29-0,55)
DEBIT_S = 0.25       # intervalle minimal entre requêtes (≤ 4 req/s, garde 5 req/s Google)
BACKOFF = [2, 5, 12]  # secondes, 3 tentatives par segment

BACKENDS = ("zai", "googletrans", "gtx", "mymemory")

VERSION = "1.2.0"
LANGUES = {"zh": "zh-CN", "en": "en", "fr": "fr"}  # codes courts → codes complets
NOMS_LANGUES = {"zh-CN": "chinois", "en": "anglais", "fr": "français"}
MOTS_VIDES_EN = frozenset(
    "the and of to in is are was for with that this on as be by from at or an not it".split())
MOTS_VIDES_FR = frozenset(
    "le la les de des du et est dans pour avec sur un une que qui au aux ne pas plus sont".split())


def _invite_zai(src: str, dest: str) -> tuple[str, str]:
    """(systeme, invite) du backend zai — paramétré par l'axe (v1.2.0 --src/--dest)."""
    systeme = (f"Tu es un traducteur technique {NOMS_LANGUES[src]}→{NOMS_LANGUES[dest]} expert. "
               "Traduis fidèlement le texte fourni en " + NOMS_LANGUES[dest]
               + ", registre technique, sans ajouter ni omettre d'information. "
               "Conserve tels quels : les URLs, le code, les noms de fichiers, les valeurs chiffrées "
               "et les jetons de protection \u2063N\u2063. Réponds UNIQUEMENT avec la traduction.")
    invite = f"Traduis en {NOMS_LANGUES[dest]}, réponds uniquement avec la traduction :\n"
    return systeme, invite


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


def charger_glossaire(chemin: str) -> list:
    """Glossaire TSV : terme source <TAB> terme cible ; lignes # = commentaires.

    Tri par terme le plus long d'abord (v1.2.0 — candidat « glossaire FR » du rapport G5).
    """
    entrees: list[tuple[str, str]] = []
    with open(chemin, encoding="utf-8") as f:
        for ligne in f:
            if not ligne.strip() or ligne.lstrip().startswith("#"):
                continue
            parties = [p.strip() for p in ligne.rstrip("\n").split("\t")]
            if len(parties) >= 2 and parties[0] and parties[1]:
                entrees.append((parties[0], parties[1]))
    entrees.sort(key=lambda p: len(p[0]), reverse=True)
    return entrees


def appliquer_glossaire_avant(texte: str, glossaire: list) -> tuple[str, int]:
    """Substitue les termes du glossaire par leurs équivalents FR AVANT traduction
    (v1.2.0 — candidat « glossaire FR » ; adaptation règle d'or n°1 : le masquage
    opaque par jetons dégradait la qualité LLM à forte densité — termes fixés visibles,
    conservés nativement par le traducteur, zones URLs/inline déjà masquées exemptes)."""
    total = 0
    for terme, cible in glossaire:
        nb = texte.count(terme)
        if nb:
            texte = texte.replace(terme, cible)
            total += nb
    return texte, total


def appliquer_glossaire_apres(texte: str, glossaire: list) -> str:
    """Passe déterministe POST-traduction (v1.2.0) : tout terme du glossaire resté
    en chinois dans la sortie est remplacé mécaniquement par son équivalent FR fixé."""
    for terme, cible in glossaire:
        if terme in texte:
            texte = texte.replace(terme, cible)
    return texte


def _score_mots_vides(texte: str, mots: frozenset) -> int:
    """Compte les occurrences de mots vides (heursique latine — v1.2.0 --src/--dest)."""
    if not mots:
        return 0
    return sum(1 for t in re.split(r"\W+", texte.lower()) if t in mots)


def _bloc_a_traduire(bloc: str, stat: dict) -> bool:
    """Garde P2 : code exclu ; pour source zh — CJK requis (ratio ≥ seuil, comportement v1.1.0)."""
    if stat["src"].startswith("zh"):
        n_cjk = compter_cjk(bloc)
        if n_cjk == 0 or n_cjk / max(len(bloc), 1) < SEUIL_RATIO_CJK:
            return False
    return True


def _morceau_dans_langue_source(cible: str, stat: dict) -> bool:
    """Garde d'axe (sources latines — v1.2.0) : morceau déjà en langue cible ⇒ conservé (idempotence)."""
    if stat["src"].startswith("zh"):
        return True  # la garde CJK a déjà tranché au niveau bloc
    mots_src = MOTS_VIDES_EN if stat["src"].startswith("en") else frozenset()
    if stat["dest"].startswith("fr"):
        mots_dst = MOTS_VIDES_FR
    elif stat["dest"].startswith("en"):
        mots_dst = MOTS_VIDES_EN
    else:
        mots_dst = frozenset()
    return _score_mots_vides(cible, mots_src) > _score_mots_vides(cible, mots_dst)


def _cle_bloc(bloc: str, stat: dict) -> str:
    """Clé du marqueur de bloc stabilisé (point fixe — v1.2.0) : contenu + axe + glossaire.
    Sortie de bloc traduite → enregistrée ; un re-jeu la rencontre → no-op byte-stable."""
    sig = stat.get("glossaire_sig", "")
    return "bloc:" + hashlib.sha256(f"{stat['src']}|{stat['dest']}|{sig}|{bloc}".encode()).hexdigest()


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
        url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) traduction-zh-fr/1.2"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as rep:
        return rep.read().decode("utf-8")


def _traduire_zai(texte: str, limiteur: Debit, stat: dict) -> str:
    """Backend z-ai chat (LLM glm de l'écosystème — le plus qualitatif, sans quota 429)."""
    if not shutil.which("z-ai"):
        raise RuntimeError("CLI z-ai absent")
    systeme, invite = _invite_zai(stat["src"], stat["dest"])
    limiteur.attendre()
    fd, chemin = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    try:
        r = subprocess.run(
            ["z-ai", "chat", "-s", systeme,
             "-p", invite + texte,
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


def _traduire_gtx(texte: str, limiteur: Debit, stat: dict) -> str:
    """Backend endpoint gtx (Google Translate public, sans clé)."""
    params = urllib.parse.urlencode(
        {"client": "gtx", "sl": stat["src"], "tl": stat["dest"], "dt": "t", "q": texte}
    )
    limiteur.attendre()
    brut = _http_get(f"https://translate.googleapis.com/translate_a/single?{params}")
    data = json.loads(brut)
    return "".join(seg[0] for seg in data[0] if seg and seg[0])


def _traduire_mymemory(texte: str, limiteur: Debit, stat: dict) -> str:
    """Backend MyMemory API publique (gratuit, sans clé, ≤ 500 car/requête)."""
    sortie: list[str] = []
    dest = "fr-FR" if stat["dest"] == "fr" else stat["dest"]
    for morceau in re.findall(r".{1,490}", texte):
        params = urllib.parse.urlencode({"q": morceau, "langpair": f"{stat['src']}|{dest}"})
        limiteur.attendre()
        brut = _http_get(f"https://api.mymemory.translated.net/get?{params}")
        data = json.loads(brut)
        sortie.append(data["responseData"]["translatedText"])
    return " ".join(sortie)


def _traduire_googletrans(texte: str, limiteur: Debit, stat: dict) -> str:
    """Backend googletrans (conformément à la directive propriétaire — optionnel)."""
    import asyncio

    from googletrans import Translator  # type: ignore[import-untyped]

    async def _une() -> str:
        rep = await Translator().translate(texte, src=stat["src"], dest=stat["dest"])
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
    cle = hashlib.sha256(f"{stat['src']}|{stat['dest']}|{texte}".encode()).hexdigest()
    horodatage = datetime.now(timezone.utc).isoformat()
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
            dst = globals()[f"_traduire_{nom}"](texte, limiteur, stat)
        except Exception as exc:  # noqa: BLE001 — chaîne de repli volontaire
            erreur_derniere = exc
            if journalise:
                journalise(f"backend {nom} KO : {exc}")
            continue
        if dst and dst != texte:
            cache[cle] = {"src": texte, "dst": dst, "lang_src": stat["src"],
                          "lang_dest": stat["dest"], "backend": nom, "ts": horodatage}
            stat["requetes"] += 1
            return dst
        if nom == "zai" and dst == texte:
            # Verdict d'identité du LLM de confiance (tête de chaîne) : rien à traduire
            # (prose déjà francisée ou données fonctionnelles P2) — segment conservé tel
            # quel, SANS échec (optimisation G6 issue du test réel — re-jeux idempotents).
            # Garde v1.2.0 (issue du test réel G10) : un segment renvoyé inchangé ALORS
            # qu'il est encore en langue SOURCE est un REFUS du LLM, pas un « rien à
            # traduire » — en mode glossaire (ou source latine) c'est traité comme un
            # échec honnête ; l'identité P2 sans glossaire demeure acceptée (v1.1.0).
            if stat["src"].startswith("zh"):
                deja_cible = compter_cjk(texte) / max(len(texte), 1) < SEUIL_ECHO_CIBLE
            else:
                deja_cible = not _morceau_dans_langue_source(texte, stat)
            refus_source = (not deja_cible) and (bool(stat.get("glossaire"))
                                                or not stat["src"].startswith("zh"))
            if not refus_source:
                cache[cle] = {"src": texte, "dst": texte, "lang_src": stat["src"],
                              "lang_dest": stat["dest"], "backend": "zai-identité", "ts": horodatage}
                stat["inchangés"] = stat.get("inchangés", 0) + 1
                if journalise:
                    journalise("backend zai : verdict identité — rien à traduire (P2/déjà francisé), segment conservé")
                return texte
            if journalise:
                journalise("backend zai : segment renvoyé inchangé alors qu'il est en langue source — refus traité comme échec")
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


def _traduire_par_paragraphes(cible: str, cache: dict, stat: dict, journalise=None) -> str:
    """Repli anti-refus (v1.2.0) : morceau en échec re-découpé en paragraphes
    individuels — segments plus petits, tâches plus simples pour le LLM ; si un
    paragraphe échoue, l'échec remonte honnêtement."""
    sortie = []
    for partie in re.split(r"(\n\s*\n)", cible):
        if not partie.strip():
            sortie.append(partie)
            continue
        traduit = traduire_texte(partie.strip(), cache, stat, journalise)
        sortie.append(partie.replace(partie.strip(), traduit, 1))
    return "".join(sortie)


def _traduire_corps(texte: str, cache: dict, stat: dict, journalise=None) -> str:
    sortie = []
    for bloc, a_traduire in decouper_markdown(texte):
        if not a_traduire:
            # P2 : bloc de code — conservé tel quel
            sortie.append(bloc)
            continue
        if cache.get(_cle_bloc(bloc, stat), {}).get("final"):
            # v1.2.0 — marqueur de bloc stabilisé : déjà traduit pour cet axe + glossaire ;
            # re-jeu = no-op byte-stable SANS appel réseau (point fixe mécanique — les
            # re-traductions stochastiques ne peuvent plus dériver entre les passes).
            stat["blocs_figes"] = stat.get("blocs_figes", 0) + 1
            sortie.append(bloc)
            continue
        if not _bloc_a_traduire(bloc, stat):
            # P2 : hors langue source, ou prose déjà francisée — conservé tel quel
            sortie.append(bloc)
            continue
        brut, jetons = limiter_urls(bloc)
        if stat.get("glossaire"):
            brut, nb_gloss = appliquer_glossaire_avant(brut, stat["glossaire"])
            stat["glossaire_hits"] = stat.get("glossaire_hits", 0) + nb_gloss
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
            if not _morceau_dans_langue_source(cible, stat):
                # garde d'axe (sources latines — v1.2.0) : morceau déjà en langue cible, conservé
                final.append(morceau)
                continue
            traduit = None
            echec: Exception | None = None
            for tentative in range(3):
                try:
                    traduit = traduire_texte(cible, cache, stat, journalise)
                    break
                except Exception as exc:  # noqa: BLE001 — repli volontaire
                    echec = exc
                    if tentative < 2:
                        time.sleep(BACKOFF[tentative])
            if traduit is None:
                # Repli anti-refus (v1.2.0) : dernier essai par paragraphes individuels
                if journalise:
                    journalise(f"repli paragraphes individuels — morceau en échec ({echec})")
                traduit = _traduire_par_paragraphes(cible, cache, stat, journalise)
            if stat.get("glossaire"):
                traduit = appliquer_glossaire_apres(traduit, stat["glossaire"])
            final.append(morceau.replace(cible, traduit, 1))
        resultat = restaurer_urls("".join(final), jetons)
        sortie.append(resultat)
        # v1.2.0 — point fixe : la SORTIE du bloc est enregistrée comme stabilisée
        cache[_cle_bloc(resultat, stat)] = {"final": True}
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


def exporter_tmx(cache: dict, chemin: str, src: str, dest: str) -> int:
    """Exporte la mémoire de traduction (cache) au format TMX 1.4b — déterministe
    (tri par clé sha256 ; seules les entrées complètes src+dst partent ; v1.2.0 candidat
    « export TMX » du rapport G5)."""
    unites = sorted((cle, v) for cle, v in cache.items()
                    if isinstance(v, dict) and v.get("src") and v.get("dst"))
    creationdate = "19700101T000000Z"
    dates = [v.get("ts", "") for _, v in unites]
    if dates and len(max(dates)) >= 19:
        brute = max(dates)
        creationdate = f"{brute[:4]}{brute[5:7]}{brute[8:10]}T{brute[11:13]}{brute[14:16]}{brute[17:19]}Z"
    lignes = ['<?xml version="1.0" encoding="UTF-8"?>', '<tmx version="1.4">',
              f'  <header creationtool="traduire-md-zh-fr" creationtoolversion="{VERSION}"'
              f' datatype="plaintext" segtype="paragraph" adminlang="fr" srclang="{escape(src)}"'
              f' o-tmf="traduction-zh-fr" creationdate="{creationdate}"/>',
              '  <body>']
    for cle, v in unites:
        lignes.append(f'    <tu tuid="{cle}" datatype="plaintext">')
        lignes.append(f'      <tuv xml:lang="{escape(v.get("lang_src", src))}">'
                      f'<seg>{escape(v["src"])}</seg></tuv>')
        lignes.append(f'      <tuv xml:lang="{escape(v.get("lang_dest", dest))}">'
                      f'<seg>{escape(v["dst"])}</seg></tuv>')
        lignes.append('    </tu>')
    lignes += ['  </body>', '</tmx>', '']
    dossier = os.path.dirname(chemin)
    if dossier:
        os.makedirs(dossier, exist_ok=True)
    with open(chemin, "w", encoding="utf-8") as f:
        f.write("\n".join(lignes))
    return len(unites)


# ---------------------------------------------------------------- selftest
def selftest() -> int:
    """Auto-test hors-ligne : logique prouvée sans réseau (backends simulés) — 20 contrôles."""
    echecs: list[str] = []

    def _verifier(nom: str, condition: bool) -> None:
        if not condition:
            echecs.append(nom)

    _verifier("detect-cjk", compter_cjk("hello world") == 0 and compter_cjk("这是测试") == 4)

    # Injection d'un backend simulé (hors-ligne) — la chaîne réelle zai→googletrans→gtx→mymemory est conservée en production
    globals()["BACKENDS"] = ("gtx",)
    globals()["_traduire_gtx"] = lambda texte, limiteur, stat: f"TRADUIT[{texte}]"

    md = ("---\ntitle: 测试\n---\n\n这是一个测试句子。\n\n"
          "```python\nprint('不要翻译我')\n```\n\nVoir https://exemple.cn/页面 `code 中式`\n")
    stat = {"cache": 0, "requetes": 0, "limiteur": Debit(0.01), "src": "zh-CN", "dest": "fr"}
    cache: dict = {}
    rep = traduire_markdown(md, cache, stat, None)
    _verifier("frontmatter-intact", rep.startswith("---\ntitle: 测试\n---\n"))
    _verifier("code-protect", "print('不要翻译我')" in rep)
    _verifier("url-protect", "https://exemple.cn/页面" in rep)
    _verifier("inline-protect", "`code 中式`" in rep)
    _verifier("run1-requetes", stat["requetes"] >= 1 and len(cache) >= 1)

    # idempotence ×2 : re-traduire avec le cache chaud = 0 requête réseau
    stat2 = {"cache": 0, "requetes": 0, "limiteur": Debit(0.01), "src": "zh-CN", "dest": "fr"}
    rep2 = traduire_markdown(md, cache, stat2, None)
    _verifier("idempotent-x2", stat2["requetes"] == 0 and stat2["cache"] >= 1 and rep2 == rep)

    # garde anti-surtraduction : les CJK résiduels = données protégées uniquement
    _verifier("residuels-protect", 0 < compter_cjk(rep) < SEUIL_CJK)

    # v1.2.0 candidat 1/3 — glossaire FR : substitution visible avant + enforcement déterministe après
    stat3 = {"cache": 0, "requetes": 0, "limiteur": Debit(0.01), "src": "zh-CN", "dest": "fr",
             "glossaire": [("版心", "zone de composition"), ("字号", "corps")]}
    cache3: dict = {}
    rep3 = traduire_markdown("版心 由 字号 决定，版心 居中。", cache3, stat3, None)
    _verifier("glossaire-avant",
              "zone de composition" in rep3 and "corps" in rep3
              and "版心" not in rep3 and "字号" not in rep3
              and stat3.get("glossaire_hits", 0) >= 3)
    globals()["_traduire_gtx"] = lambda texte, limiteur, stat: texte.replace("zone de composition", "版心")
    stat3b = {"cache": 0, "requetes": 0, "limiteur": Debit(0.01), "src": "zh-CN", "dest": "fr",
              "glossaire": [("版心", "zone de composition")]}
    rep3b = traduire_markdown("版心 决定。", {}, stat3b, None)
    _verifier("glossaire-apres", "版心" not in rep3b and "zone de composition" in rep3b)
    globals()["_traduire_gtx"] = lambda texte, limiteur, stat: f"TRADUIT[{texte}]"

    # v1.2.0 candidat 2/3 — export TMX : XML valide, entrées complètes seules, déterminisme byte ×2
    dossier = tempfile.mkdtemp(prefix="selftest-tmx-")
    try:
        import xml.etree.ElementTree as ET
        fixture = {
            "cle1": {"src": "这是测试", "dst": "C'est un test", "lang_src": "zh-CN",
                     "lang_dest": "fr", "backend": "zai", "ts": "2026-11-01T02:44:30+00:00"},
            "cle2": {"src": "The data layer", "dst": "La couche de données", "lang_src": "en",
                     "lang_dest": "fr", "backend": "zai", "ts": "2026-11-01T02:45:10+00:00"},
            "cle3": {"dst": "entrée v1.1.0 sans source — non exportable"},
        }
        chemin_tmx = os.path.join(dossier, "memoire.tmx")
        nb = exporter_tmx(fixture, chemin_tmx, "zh-CN", "fr")
        arbre = ET.parse(chemin_tmx)
        segs = [s.text for s in arbre.findall(".//seg")]
        _verifier("tmx-valide", nb == len(arbre.findall(".//tu")) == 2
                  and arbre.getroot().get("version") == "1.4"
                  and "这是测试" in segs and "C'est un test" in segs)
        premiere = open(chemin_tmx, encoding="utf-8").read()
        exporter_tmx(fixture, chemin_tmx, "zh-CN", "fr")
        _verifier("tmx-deterministe", open(chemin_tmx, encoding="utf-8").read() == premiere)
    finally:
        shutil.rmtree(dossier, ignore_errors=True)

    # v1.2.0 candidat 3/3 — axes --src/--dest : clés séparées, prompt paramétré, garde EN→FR
    k1 = hashlib.sha256("zh-CN|fr|X".encode()).hexdigest()
    k2 = hashlib.sha256("en|fr|X".encode()).hexdigest()
    k3 = hashlib.sha256("zh-CN|en|X".encode()).hexdigest()
    _verifier("axes-cles-distinctes", len({k1, k2, k3}) == 3)
    s1, i1 = _invite_zai("zh-CN", "fr")
    s2, i2 = _invite_zai("en", "fr")
    _verifier("axes-prompt", "chinois→français" in s1 and "français" in i1
              and "anglais→français" in s2 and "chinois" not in s2)
    stat_en = {"cache": 0, "requetes": 0, "limiteur": Debit(0.01), "src": "en", "dest": "fr"}
    cache_en: dict = {}
    mix = ("The synchronization layer handles retries and timeouts.\n\n"
           "```\nFR\n```\n\nLa couche de synchronisation gère les reprises et les délais.")
    rep_en = traduire_markdown(mix, cache_en, stat_en, None)
    _verifier("axe-enfr-garde", "TRADUIT[" in rep_en
              and "La couche de synchronisation gère les reprises" in rep_en
              and stat_en["requetes"] == 1)

    # v1.2.0 — garde anti-refus du verdict d'identité (glossaire actif / source latine)
    globals()["BACKENDS"] = ("zai",)
    globals()["_traduire_zai"] = lambda texte, limiteur, stat: texte  # renvoie inchangé
    stat_refus = {"cache": 0, "requetes": 0, "limiteur": Debit(0.01), "src": "zh-CN", "dest": "fr",
                  "glossaire": [("版心", "zone de composition")]}
    try:
        traduire_texte("版心 是核心排版规则。", {}, stat_refus, None)
        _verifier("identite-refus-glossaire", False)
    except RuntimeError:
        _verifier("identite-refus-glossaire", True)
    stat_p2 = {"cache": 0, "requetes": 0, "limiteur": Debit(0.01), "src": "zh-CN", "dest": "fr"}
    rep_p2 = traduire_texte("排版 数据 术语。", {}, stat_p2, None)
    _verifier("identite-p2-sans-glossaire", rep_p2 == "排版 数据 术语。" and stat_p2.get("inchangés", 0) == 1)

    # v1.2.0 — écho sur segment majoritairement CIBLE (CJK < 20 %, données P2 résiduelles)
    # = conservation acceptée même en mode glossaire (le refus réel porte sur la prose ≥ 20 %)
    stat_mix = {"cache": 0, "requetes": 0, "limiteur": Debit(0.01), "src": "zh-CN", "dest": "fr",
                "glossaire": [("版心", "zone de composition")]}
    seg_mix = ("La zone de composition conserve les marges et l'interligne, avec 思源宋体 "
               "et 方正书宋 en spécimens de données.")
    rep_mix = traduire_texte(seg_mix, {}, stat_mix, None)
    _verifier("echo-donnees-conservé", rep_mix == seg_mix and stat_mix.get("inchangés", 0) == 1)

    # v1.2.0 — repli anti-refus : morceau en échec re-découpé en paragraphes individuels
    globals()["BACKENDS"] = ("gtx",)
    globals()["BACKOFF"] = [0, 0, 0]

    def _stub_refus(texte, limiteur, stat):
        if len(texte) > 40:
            raise RuntimeError("refus simulé (gros segment)")
        return f"TRADUIT[{texte}]"

    globals()["_traduire_gtx"] = _stub_refus
    stat_pp = {"cache": 0, "requetes": 0, "limiteur": Debit(0.01), "src": "zh-CN", "dest": "fr"}
    md_pp = ("这是第一个段落的内容。\n\n这是第二个段落的内容。\n\n"
             "这是第三个段落的内容。\n\n这是第四个段落的内容。")
    rep_pp = traduire_markdown(md_pp, {}, stat_pp, None)
    _verifier("repli-paragraphes", rep_pp.count("TRADUIT[") == 4 and stat_pp["requetes"] == 4)

    # v1.2.0 — marqueur de bloc stabilisé : point fixe mécanique (re-jeu no-op, sans réseau,
    # même si le LLM répondait différemment à chaque appel) + sensibilité au glossaire
    compteur = {"n": 0}

    def _stub_variable(texte, limiteur, stat):
        compteur["n"] += 1
        return f"TRADUCTION-{compteur['n']}[{texte}]"

    globals()["_traduire_gtx"] = _stub_variable
    stat_m = {"cache": 0, "requetes": 0, "limiteur": Debit(0.01), "src": "zh-CN", "dest": "fr",
              "glossaire_sig": "sig-test"}
    cache_m: dict = {}
    rep_m1 = traduire_markdown("这是要翻译的段落内容，比较长一点的测试。", cache_m, stat_m, None)
    stat_m2 = {"cache": 0, "requetes": 0, "limiteur": Debit(0.01), "src": "zh-CN", "dest": "fr",
               "glossaire_sig": "sig-test"}
    rep_m2 = traduire_markdown(rep_m1, cache_m, stat_m2, None)  # re-jeu sur la SORTIE
    _verifier("bloc-stabilise", rep_m2 == rep_m1 and stat_m2["requetes"] == 0)
    stat_m3 = {"cache": 0, "requetes": 0, "limiteur": Debit(0.01), "src": "zh-CN", "dest": "fr",
               "glossaire_sig": "AUTRE-glossaire"}
    rep_m3 = traduire_markdown(rep_m1, cache_m, stat_m3, None)
    _verifier("bloc-glossaire-sensible", rep_m3 != rep_m1 and stat_m3["requetes"] >= 1)

    if echecs:
        print("SELFTEST FAIL :", echecs)
        return 1
    print("SELFTEST PASS (20/20) — détection, frontmatter, code, URLs, inline, cache, idempotence ×2, "
          "seuil, glossaire avant/après, TMX valide, TMX déterministe, clés d'axes, prompt d'axes, "
          "garde EN→FR, identité refusée en glossaire / P2 conservée sans glossaire, écho données P2, "
          "repli paragraphes, bloc stabilisé (point fixe) + sensibilité glossaire")
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
    p.add_argument("--glossaire", default=None, help="glossaire TSV : terme source <TAB> terme cible (v1.2.0)")
    p.add_argument("--tmx", default=None, help="exporter la mémoire de traduction en TMX 1.4b (v1.2.0)")
    p.add_argument("--src", default="zh", help="langue source : zh (défaut), en (v1.2.0)")
    p.add_argument("--dest", default="fr", help="langue cible : fr (défaut), en (v1.2.0)")
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
    src = LANGUES.get(a.src, a.src)
    dest = LANGUES.get(a.dest, a.dest)
    if a.glossaire and not os.path.exists(a.glossaire):
        print(f"  GLOSSAIRE ABSENT : {a.glossaire}")
        return 2
    glossaire = charger_glossaire(a.glossaire) if a.glossaire else []
    glossaire_sig = hashlib.sha256("|".join(f"{t}->{c}" for t, c in glossaire).encode()).hexdigest()
    stat = {"cache": 0, "requetes": 0, "limiteur": Debit(DEBIT_S),
            "src": src, "dest": dest, "glossaire": glossaire, "glossaire_sig": glossaire_sig}
    if glossaire:
        print(f"  [glossaire] {len(glossaire)} terme(s) fixé(s) — axe {src}→{dest}")

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
        if src.startswith("zh") and n_avant < a.seuil:
            print(f"  SAUTE (< {a.seuil} CJK) : {rel} ({n_avant})")
            continue
        if a.dry:
            if src.startswith("zh"):
                print(f"  DRY : {rel} — {n_avant} CJK, ~{n_avant // 500 + 1} requête(s) estimée(s)")
            else:
                print(f"  DRY : {rel} — {len(texte)} caractères, axe {src}→{dest}, garde par morceau (mots vides)")
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
        statut = "TRADUIT" if sha_apres != sha_avant else "INCHANGÉ"
        if a.journal:
            journaliser(
                journal,
                a.journal,
                {
                    "fichier": rel,
                    "zh_avant": n_avant,
                    "sha_avant": sha_avant[:12],
                    "zh_apres": n_apres,
                    "statut": statut,
                    "sha_apres": sha_apres[:12],
                    "outil": "traduction-zh-fr/traduire-md-zh-fr.py",
                    "axe": f"{src}->{dest}",
                    "ts": datetime.now(timezone.utc).isoformat(),
                },
            )
        if statut == "INCHANGÉ":
            print(f"  INCHANGÉ : {rel} — {n_avant} CJK (cache {stat['cache']}, requêtes {stat['requetes']}) — déjà en langue cible / données P2")
        else:
            note_gloss = f", glossaire {stat['glossaire_hits']} remplacement(s)" if stat.get("glossaire_hits") else ""
            print(f"  TRADUIT : {rel} — {n_avant} → {n_apres} CJK, axe {src}→{dest} (cache {stat['cache']}, requêtes {stat['requetes']}{note_gloss})")

    os.makedirs(os.path.dirname(cache_chemin) or ".", exist_ok=True)
    with open(cache_chemin, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=1)
    if a.tmx:
        nb_tu = exporter_tmx(cache, a.tmx, src, dest)
        print(f"  TMX EXPORTÉ : {a.tmx} — {nb_tu} unité(s) de traduction (TMX 1.4b)")
    return rc


if __name__ == "__main__":
    sys.exit(main())
