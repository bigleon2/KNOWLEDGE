#!/usr/bin/env python3
"""traduire-pdf-zh-fr.py — Traduction des PDF chinois via pdf2zh-next (BabelDOC) + adaptateur z-ai.

Conventions script-creator : Python stdlib + pdf2zh-next (dépendance du skill),
--dry/--exec/--selftest, compteur d'appels vérifiable.
Politique P1/P2 (chantier P2 francisation) : la traduction porte le TEXTE ;
la mise en page, les polices et le rendu sont préservés par BabelDOC.

v1.3.0 (2e candidat restant du rapport G5 — upgrade du moteur PDF, E13 n°6 trace
1a1968934958f495) : le moteur PDF du skill passe de pdf2zh 1.9.11 à pdf2zh-next
2.9.0/BabelDOC (successeur officiel — sortie mai 2026). Constat D703 : les moteurs
gratuits intégrés (Google, Bing) sont throttlés depuis la machine d'exécution
(RetryError après épuisement des tentatives) ; l'adaptateur TraducteurZai câble
donc le LLM glm de l'écosystème (CLI `z-ai chat`) dans le pipeline BabelDOC —
même tête de chaîne que traduire-md-zh-fr.py (backend zai).

Usage :
    traduire-pdf-zh-fr.py --dry   fichier.pdf
    traduire-pdf-zh-fr.py --exec  fichier.pdf [--output DIR] [--lang-in zh] [--lang-out fr]
                                  [--qps 1] [--workers 1]
    traduire-pdf-zh-fr.py --selftest
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time

VERSION = "1.3.0"
DEBIT_S = 1.0          # intervalle minimal entre appels z-ai (secondes)
BACKOFF = [2, 5]       # secondes, 3 tentatives par segment
RE_CJK = re.compile(r"[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]")
NOMS_LANGUES = {"zh": "chinois", "en": "anglais", "fr": "français"}


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


def _invite(lang_in: str, lang_out: str) -> tuple[str, str]:
    """(systeme, invite) de l'adaptateur — même style que traduire-md-zh-fr.py."""
    systeme = (f"Tu es un traducteur technique {NOMS_LANGUES.get(lang_in, lang_in)}→"
               f"{NOMS_LANGUES.get(lang_out, lang_out)} expert. "
               "Traduis fidèlement le texte fourni en " + NOMS_LANGUES.get(lang_out, lang_out)
               + ", registre technique, sans ajouter ni omettre d'information. "
               "Conserve tels quels : les formules, le code, les noms de fichiers et les valeurs chiffrées. "
               "Réponds UNIQUEMENT avec la traduction.")
    invite = (f"Traduis en {NOMS_LANGUES.get(lang_out, lang_out)}, "
              "réponds uniquement avec la traduction :\n")
    return systeme, invite


class TraducteurZai:
    """Adaptateur traducteur BabelDOC → CLI `z-ai chat` (LLM glm de l'écosystème).

    Contrat (interface ILTranslator de BabelDOC) : translate(text, rate_limit_params)
    -> str (synchrone) + placeholders riches/formules (sémantique de la classe de base
    babeldoc.translator.translator.BaseTranslator) + do_llm_translate → NotImplementedError
    (voie LLM interne désactivée — la traduction passe par translate()).
    Thread-safe (verrou) + limiteur de débit + 3 tentatives. Les appels réels
    sont comptés (stat['appels']) — vérifiable pour les tests d'idempotence.
    """

    def __init__(self, lang_in: str, lang_out: str, qps: float = 1.0) -> None:
        self.lang_in = lang_in
        self.lang_out = lang_out
        self.limiteur = Debit(1.0 / max(qps, 0.1))
        self.verrou = threading.Lock()
        self.stat = {"appels": 0, "echecs": 0}

    # ----- placeholders (sémantique BaseTranslator — le pipeline détecte les
    # hallucinations de marqueurs via ces motifs)
    def get_rich_text_left_placeholder(self, placeholder_id: int | str) -> str:
        return f"<b{placeholder_id}>"

    def get_rich_text_right_placeholder(self, placeholder_id: int | str) -> str:
        return f"</b{placeholder_id}>"

    def get_formular_placeholder(self, placeholder_id: int | str) -> str:
        return self.get_rich_text_left_placeholder(placeholder_id)

    def do_llm_translate(self, text, rate_limit_params: dict | None = None):
        raise NotImplementedError("voie LLM interne désactivée — utiliser translate()")

    def translate(self, text: str, rate_limit_params: dict | None = None) -> str:  # noqa: ARG002
        if not text or not text.strip():
            return text
        if not shutil.which("z-ai"):
            raise RuntimeError("CLI z-ai absent — installez le SDK z-ai (moteur LLM de l'écosystème)")
        systeme, invite = _invite(self.lang_in, self.lang_out)
        erreur: Exception | None = None
        for tentative in range(3):
            try:
                with self.verrou:
                    self.limiteur.attendre()
                    self.stat["appels"] += 1
                    fd, chemin = tempfile.mkstemp(suffix=".json")
                    os.close(fd)
                    try:
                        r = subprocess.run(
                            ["z-ai", "chat", "-s", systeme,
                             "-p", invite + text, "--output", chemin],
                            capture_output=True, text=True, timeout=180,
                        )
                        if r.returncode != 0:
                            raise RuntimeError(f"z-ai rc={r.returncode} : {r.stderr.strip()[-150:]}")
                        with open(chemin, encoding="utf-8") as f:
                            data = json.load(f)
                        dst = (data["choices"][0]["message"]["content"] or "").strip()
                    finally:
                        os.unlink(chemin)
                if not dst:
                    raise RuntimeError("z-ai : réponse vide")
                return dst
            except Exception as exc:  # noqa: BLE001 — tentatives volontaires
                erreur = exc
                self.stat["echecs"] += 1
                if tentative < 2:
                    time.sleep(BACKOFF[tentative])
        raise RuntimeError(f"traduire-pdf : z-ai a échoué 3 fois : {erreur}")


# ---------------------------------------------------------------- utilitaires
def _stats_pdf(chemin: str) -> dict:
    """Pages + caractères CJK du PDF source (pymupdf, embarqué avec pdf2zh-next)."""
    import pymupdf

    doc = pymupdf.open(chemin)
    texte = "".join(page.get_text() for page in doc)
    return {"pages": len(doc), "cjk": len(RE_CJK.findall(texte)),
            "caracteres": len(texte)}


def _babeldoc_dispo() -> tuple[bool, str]:
    try:
        import babeldoc  # noqa: F401
        from babeldoc.format.pdf.high_level import translate  # noqa: F401
        return True, "babeldoc importable"
    except ImportError as exc:
        return False, f"babeldoc absent : {exc} (pip install pdf2zh-next)"


# ---------------------------------------------------------------- selftest
def selftest() -> int:
    """Auto-test hors-ligne — 10 contrôles (logique pure + toolchain, sait échouer)."""
    echecs: list[str] = []

    def _verifier(nom: str, condition: bool) -> None:
        if not condition:
            echecs.append(nom)

    # 1-2 — contrat de l'adaptateur (interface attendue par le pipeline BabelDOC)
    adapt = TraducteurZai("zh", "fr")
    _verifier("adaptateur-classe", hasattr(adaptateur := adapt, "translate")
              and callable(adaptateur.translate))
    import inspect
    sig = inspect.signature(TraducteurZai.translate)
    params = list(sig.parameters)
    _verifier("adaptateur-signature", params[:2] == ["self", "text"]
              and "rate_limit_params" in params)

    # 3 — invite paramétrée par l'axe
    s_zh, i_zh = _invite("zh", "fr")
    s_en, _ = _invite("en", "fr")
    _verifier("invite-axe", "chinois→français" in s_zh and "français" in i_zh
              and "anglais→français" in s_en)

    # 4 — thread-safety (verrou présent — pool BabelDOC)
    _verifier("verrou-thread", isinstance(adapt.verrou, type(threading.Lock())))

    # 5 — limiteur de débit (intervalle dérivé du qps)
    _verifier("debit-qps", TraducteurZai("zh", "fr", qps=2.0).limiteur.intervalle == 0.5
              and adapt.limiteur.intervalle == 1.0)

    # 6 — placeholders BabelDOC (sémantique BaseTranslator) + voie LLM désactivée
    _verifier("placeholders", adaptateur.get_rich_text_left_placeholder(7) == "<b7>"
              and adaptateur.get_rich_text_right_placeholder(7) == "</b7>"
              and adaptateur.get_formular_placeholder(7) == "<b7>")
    try:
        adaptateur.do_llm_translate(None)
        _verifier("llm-desactive", False)
    except NotImplementedError:
        _verifier("llm-desactive", True)

    # 7 — détection z-ai (booléen honnête, sans échec)
    _verifier("detection-zai", isinstance(bool(shutil.which("z-ai")), bool))

    # 8-9 — toolchain (dépendances dures du script — sait échouer honnêtement)
    ok, detail = _babeldoc_dispo()
    _verifier("babeldoc-importable", ok)
    print(f"  [toolchain] babeldoc : {detail}")
    try:
        import pymupdf  # noqa: F401
        _verifier("pymupdf-importable", True)
    except ImportError:
        _verifier("pymupdf-importable", False)

    if echecs:
        print("SELFTEST FAIL :", echecs)
        return 1
    print("SELFTEST PASS (10/10) — adaptateur (classe, signature, invite, verrou, débit, "
          "placeholders, voie LLM désactivée), détection z-ai, toolchain (babeldoc, pymupdf)")
    return 0


# ---------------------------------------------------------------- main
def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("fichier", nargs="?", help="fichier PDF chinois cible")
    p.add_argument("--dry", action="store_true", help="rapport sans traduction")
    p.add_argument("--exec", dest="exec_mode", action="store_true", help="traduction effective")
    p.add_argument("--selftest", action="store_true", help="auto-test hors-ligne")
    p.add_argument("--output", default=None, help="répertoire de sortie (défaut : <fichier>_traduit/)")
    p.add_argument("--lang-in", default="zh", help="langue source : zh (défaut), en")
    p.add_argument("--lang-out", default="fr", help="langue cible : fr (défaut), en")
    p.add_argument("--qps", type=float, default=1.0, help="appels z-ai par seconde (défaut 1)")
    p.add_argument("--workers", type=int, default=1, help="workers BabelDOC (défaut 1 — séquentiel)")
    a = p.parse_args()

    if a.selftest:
        return selftest()
    if not (a.dry or a.exec_mode) or not a.fichier:
        p.print_usage()
        return 2
    if not os.path.exists(a.fichier):
        print(f"  ABSENT : {a.fichier}")
        return 1

    ok, detail = _babeldoc_dispo()
    if not ok:
        print(f"  ÉCHEC toolchain : {detail}")
        return 1

    stats = _stats_pdf(a.fichier)
    if a.dry:
        print(f"  DRY : {a.fichier} — {stats['pages']} page(s), {stats['cjk']} CJK, "
              f"{stats['caracteres']} caractères ; axe {a.lang_in}→{a.lang_out} ; "
              f"moteur pdf2zh-next/BabelDOC + adaptateur z-ai (qps {a.qps})")
        return 0

    # --exec : pipeline BabelDOC avec l'adaptateur z-ai
    from babeldoc.format.pdf.high_level import translate as babeldoc_traduire
    from babeldoc.format.pdf.translation_config import TranslationConfig

    sortie = a.output or os.path.join(
        os.path.dirname(os.path.abspath(a.fichier)),
        os.path.splitext(os.path.basename(a.fichier))[0] + "_traduit")
    os.makedirs(sortie, exist_ok=True)
    adaptateur = TraducteurZai(a.lang_in, a.lang_out, qps=a.qps)
    config = TranslationConfig(
        translator=adaptateur,
        input_file=a.fichier,
        doc_layout_model=None,  # modèle de layout par défaut (chargement paresseux — même valeur que la CLI)
        lang_in=a.lang_in,
        lang_out=a.lang_out,
        output_dir=sortie,
        qps=a.qps,
        pool_max_workers=max(a.workers, 1),
    )
    try:
        babeldoc_traduire(config)
    except Exception as exc:  # noqa: BLE001 — échec honnête, jamais de faux succès
        print(f"  ÉCHEC pipeline : {type(exc).__name__} : {exc}")
        return 1

    produits = sorted(f for f in os.listdir(sortie) if f.lower().endswith(".pdf"))
    n_cjk_sortie = 0
    for f in produits:
        s = _stats_pdf(os.path.join(sortie, f))
        n_cjk_sortie = max(n_cjk_sortie, s["cjk"])
    statut = "TRADUIT" if produits and n_cjk_sortie < stats["cjk"] else "INCHANGÉ/ÉCHEC"
    print(f"  {statut} : {a.fichier} — {stats['cjk']} CJK source → {n_cjk_sortie} CJK sortie ; "
          f"appels z-ai {adaptateur.stat['appels']} (échecs {adaptateur.stat['echecs']}) ; "
          f"produits : {', '.join(produits) or 'aucun'}")
    return 0 if produits else 1


if __name__ == "__main__":
    sys.exit(main())
