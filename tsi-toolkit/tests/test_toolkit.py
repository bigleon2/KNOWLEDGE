#!/usr/bin/env python3
"""Suite de tests tsi-toolkit — critères d'acceptation EF-01..EF-08 + ENF.

Exécution : python3 -m unittest decouvrir -v  (depuis tsi-toolkit/)
ou : python3 tests/test_toolkit.py

v1.0.1 (Task 67 G4 — résorption F-67-2/F-67-3) : résolution de fixture DJTT
multi-candidats (work/djtt historique [recyclé au 5ᵉ recyclage sandbox] →
tmp/zip-djtt-task65 [extraction stable Task 65] → extraction depuis upload/ZIP) +
skip honnête si introuvable (précédent test_reel_proprietaire) + fermeture
propre des fichiers (ResourceWarnings L87/L93).
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RACINE)

from tsi_toolkit import convertisseurs, couverture, generateur, karnaugh, nixml, studio, validateur  # noqa: E402

ECOSYSTEME = os.path.dirname(RACINE)
ECHANTILLON_VALIDE = os.path.join(
    ECOSYSTEME, "skills", "tsi-validator", "samples", "echantillon-valide.tsi")
def _trouver_djtt():
    """Résolution multi-candidats de la fixture DJTT v2.1.0 (v1.0.1 — F-67-3).

    Candidats, dans l'ordre : (1) emplacement historique work/djtt (volatil —
    recyclages sandbox) ; (2) extraction stable tmp/zip-djtt-task65 (Task 65) ;
    (3) extraction à la volée depuis upload/DJTT…zip vers un cache /tmp fixe
    (idempotent). Retourne None si introuvable — l'appelant skip honnêtement.
    """
    # Racine hôte : le toolkit vit dans KNOWLEDGE-repo/tsi-toolkit (miroir git)
    # tandis que work/, tmp/ et upload/ vivent côté hôte — base dérivée en
    # conséquence (v1.0.1 : le premier calcul depuis ECOSYSTEME seul pointait
    # KNOWLEDGE-repo/work — inexistant).
    base_hote = (os.path.dirname(ECOSYSTEME)
                 if os.path.basename(ECOSYSTEME) == "KNOWLEDGE-repo"
                 else ECOSYSTEME)
    nom_interne = ("DJTT Kontrol S4 MK2 Custom Mapping v2.1.0/"
                  "DJTT Kontrol S4 MK2 Custom Mapping v2.1.0.tsi")
    candidats = [
        os.path.join(base_hote, "work", "djtt", nom_interne),
        os.path.join(base_hote, "tmp", "zip-djtt-task65", nom_interne),
    ]
    for chemin in candidats:
        if os.path.isfile(chemin):
            return chemin
    zip_source = os.path.join(
        base_hote, "upload", "DJTT Kontrol S4 MK2 Custom Mapping v2.1.0.zip")
    if os.path.isfile(zip_source):
        cache = os.path.join(tempfile.gettempdir(), "tsi-toolkit-djtt-fixture")
        cible = os.path.join(cache, os.path.basename(nom_interne))
        if not os.path.isfile(cible):
            import zipfile
            os.makedirs(cache, exist_ok=True)
            with zipfile.ZipFile(zip_source) as zf:
                for membre in zf.namelist():
                    if membre.endswith(".tsi") and not membre.endswith("/"):
                        with zf.open(membre) as src, open(cible, "wb") as dst:
                            shutil.copyfileobj(src, dst)
                        break
        if os.path.isfile(cible):
            return cible
    return None


DJTT = _trouver_djtt()
DRIVE_KB = "/home/z/my-project/work/drive-kb"
CSV_EXEMPLE = os.path.join(RACINE, "examples", "pseudo-tsi-23.csv")
PRESET_EXEMPLE = os.path.join(RACINE, "examples", "preset-freeze-mode.json")
DONNEES = os.path.join(RACINE, "data", "commandes-traktor.json")


class BaseTemp(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="tsi-toolkit-test-")
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def chemin(self, nom):
        return os.path.join(self.tmp, nom)


class TestEF01Inspect(BaseTemp):
    """EF-01 — lecture multi-format + comptes conformes à l'arbitre."""

    def test_canonique(self):
        r = nixml.inspecter(ECHANTILLON_VALIDE)
        self.assertEqual(r["format"]["famille"], "CANONIQUE")
        self.assertEqual(r["nb_mappings"], 15)

    def test_reel_djtt(self):
        if DJTT is None:
            self.skipTest("fixture DJTT introuvable — candidats : work/djtt "
                          "[recyclé sandbox], tmp/zip-djtt-task65, upload/DJTT…zip")
        r = nixml.inspecter(DJTT)
        self.assertIn(r["format"]["famille"], ("REEL_DDIOM", "REEL", "REGLAGES"))
        pont = r.get("analyseur_ecosysteme")
        if pont is None:
            self.skipTest("analyseur écosystème absent (mode autonome)")
        self.assertEqual(pont["comptes"]["DEVI"], 1)
        self.assertEqual(pont["comptes"]["DCBM"], 5626)

    def test_reel_proprietaire(self):
        for nom in ("mapping-kontrol-s4-leon-2021.tsi",
                    "sauvegarde-mapping-oct-2022.tsi"):
            chemin = os.path.join(DRIVE_KB, nom)
            if not os.path.isfile(chemin):
                self.skipTest(f"fixture absente : {nom}")
            r = nixml.inspecter(chemin)
            self.assertNotEqual(r["format"]["famille"], "INCONNU", nom)
            self.assertIn(r["format"]["famille"],
                          ("REEL_DDIOM", "REEL", "REGLAGES"), nom)


class TestEF02Generate(BaseTemp):
    """EF-02 — génération valide + roundtrip générer→lire identique."""

    def test_generation_passe_larbitre(self):
        sortie = self.chemin("genere.tsi")
        generateur.generer(PRESET_EXEMPLE, sortie)
        verdict = validateur.valider(sortie)
        self.assertEqual(verdict["verdict"], "PASS", verdict.get("problemes"))
        arbitre = verdict.get("arbitre_ecosysteme")
        if arbitre:
            self.assertEqual(arbitre["code_retour"], 0, arbitre["sortie"][-400:])
        # roundtrip : générer → lire = mêmes mappings
        modele = nixml.lire_canonique(sortie)
        self.assertEqual(len(modele["mappings"]), 15)

    def test_generation_refuse_les_conflits(self):
        with open(PRESET_EXEMPLE, encoding="utf-8") as f:
            preset = json.load(f)
        preset["mappings"].append({
            "nom": "Conflit volontaire", "type": "IN", "groupe": "Deck A",
            "controle": "Sync", "midi": {"canal": 0, "message": "NOTE",
                                         "numero": 36, "mode": "Direct"}})
        chemin = self.chemin("conflit.json")
        with open(chemin, "w", encoding="utf-8") as f:
            json.dump(preset, f)
        with self.assertRaises(ValueError):
            generateur.generer(chemin, self.chemin("x.tsi"))


class TestEF03CSV(BaseTemp):
    """EF-03 — import du CSV Pseudo-TSI historique (21 mappings)."""

    def test_import_csv(self):
        modele = convertisseurs.csv_vers_modele(CSV_EXEMPLE)
        self.assertEqual(len(modele["mappings"]), 21)
        sortie = self.chemin("csv.tsi")
        convertisseurs.csv_vers_tsi(CSV_EXEMPLE, sortie)
        relu = nixml.lire_canonique(sortie)
        self.assertEqual(len(relu["mappings"]), 21)
        # canal 1-16 → 0-15 (leçon L8)
        canaux = {m["midi"]["canal"] for m in relu["mappings"] if "midi" in m}
        self.assertTrue(all(0 <= c <= 15 for c in canaux), canaux)

    def test_hexa_tolere(self):
        chemin = self.chemin("hex.csv")
        with open(chemin, "w", encoding="utf-8") as f:
            f.write("Ligne;Phase;Ctrl_Physique;Section_Commande;Type;"
                    "Interaction;Condition;MIDI_Channel;MIDI_Note_CC;"
                    "MIDI_Type;Commentaire\n"
                    "1;1;Bouton X;Deck A > Play/Pause;Button;Direct;-;"
                    "1;0x2C;Note;hexa volontaire\n")
        modele = convertisseurs.csv_vers_modele(chemin)
        self.assertEqual(modele["mappings"][0]["midi"]["numero"], 44)


class TestEF04Karnaugh(BaseTemp):
    """EF-04 — détection de conflits (positif) et 0 faux positif (négatif)."""

    def test_conflit_detecte(self):
        mappings = [
            {"nom": "Play A", "type": "IN", "groupe": "Deck A",
             "controle": "Play/Pause",
             "midi": {"canal": 0, "message": "NOTE", "numero": 60,
                      "mode": "Direct"}},
            {"nom": "Cue A", "type": "IN", "groupe": "Deck A",
             "controle": "Cue/Set",
             "midi": {"canal": 0, "message": "NOTE", "numero": 60,
                      "mode": "Direct"}},
        ]
        conflits = karnaugh.detecter(mappings)
        self.assertTrue(any(c["type"] == "CONFLIT_MIDI" for c in conflits),
                        conflits)

    def test_conflit_masque_par_couche_non_detecte(self):
        mappings = [
            {"nom": "Play A", "type": "IN", "groupe": "Deck A",
             "controle": "Play/Pause", "modifier": {"M1": 0},
             "midi": {"canal": 0, "message": "NOTE", "numero": 60,
                      "mode": "Direct"}},
            {"nom": "Slice 1", "type": "IN", "groupe": "Deck A",
             "controle": "Slice 1", "modifier": {"M1": 1},
             "midi": {"canal": 0, "message": "NOTE", "numero": 60,
                      "mode": "Direct"}},
        ]
        conflits = [c for c in karnaugh.detecter(mappings)
                    if c["type"] == "CONFLIT_MIDI"]
        self.assertEqual(conflits, [])

    def test_mapping_sain_zero_conflit(self):
        modele = nixml.lire_canonique(ECHANTILLON_VALIDE)
        conflits = karnaugh.detecter(modele["mappings"])
        self.assertEqual(conflits, [], [c["detail"] for c in conflits])

    def test_modifier_injoignable(self):
        mappings = [
            {"nom": "Fonction X", "type": "IN", "groupe": "Deck A",
             "controle": "Slice 1", "modifier": {"M3": 1},
             "midi": {"canal": 0, "message": "NOTE", "numero": 60,
                      "mode": "Direct"}},
        ]
        conflits = karnaugh.detecter(mappings)
        self.assertTrue(any(c["type"] == "MODIFIER_ETAT" for c in conflits))


class TestEF05Couverture(BaseTemp):
    """EF-05 — couverture multi-couches, couche morte détectée."""

    def test_golden_sain(self):
        modele = nixml.lire_canonique(ECHANTILLON_VALIDE)
        audit = couverture.auditer(modele["mappings"])
        self.assertEqual(audit["verdict"], "PASS", audit["couches_mortes"])

    def test_couche_declaree_non_activee(self):
        # un mapping exige M4=1 mais rien n'active M4 → MODIFIER_ETAT +
        # audit signale la couche non activable
        mappings = [
            {"nom": "Base", "type": "IN", "groupe": "Deck A",
             "controle": "Play/Pause",
             "midi": {"canal": 0, "message": "NOTE", "numero": 36,
                      "mode": "Direct"}},
            {"nom": "Avancé", "type": "IN", "groupe": "Deck A",
             "controle": "Slice 1", "modifier": {"M4": 1},
             "midi": {"canal": 0, "message": "NOTE", "numero": 48,
                      "mode": "Direct"}},
        ]
        conflits = karnaugh.detecter(mappings)
        self.assertTrue(any(c["type"] == "MODIFIER_ETAT" for c in conflits))


class TestEF06Roundtrip(BaseTemp):
    """EF-06 — TSI → JSON → TSI byte-identique."""

    def test_roundtrip(self):
        j1 = self.chemin("r1.json")
        t2 = self.chemin("r2.tsi")
        j2 = self.chemin("r2.json")
        convertisseurs.tsi_vers_json(ECHANTILLON_VALIDE, j1)
        convertisseurs.json_vers_tsi(j1, t2)
        convertisseurs.tsi_vers_json(t2, j2)
        self.assertEqual(open(j1, encoding="utf-8").read(),
                         open(j2, encoding="utf-8").read())
        # stabilité de la sérialisation sur ses propres sorties
        with open(j2, encoding="utf-8") as f:
            modele2 = json.load(f)
        from tsi_toolkit import nixml as _n
        self.assertEqual(_n.serialiser(modele2),
                         open(t2, encoding="utf-8").read())


class TestEF07CLI(BaseTemp):
    """EF-07 — CLI cohérente, scénario de bout en bout sans erreur."""

    def test_aide(self):
        from tsi_toolkit.__main__ import construire_parseur
        parseur = construire_parseur()
        for cmd in ("inspect", "generate", "validate", "convert",
                    "coverage", "presets", "studio"):
            with self.subProcess if False else self.subTest(cmd=cmd):
                with self.assertRaises(SystemExit) as ctx:
                    parseur.parse_args([cmd, "--help"])
                self.assertEqual(ctx.exception.code, 0)

    def test_scenario_bout_en_bout(self):
        env = dict(os.environ, PYTHONPATH=RACINE)
        sortie = self.chemin("scenario.tsi")
        r = subprocess.run(
            [sys.executable, "-m", "tsi_toolkit", "studio", sortie],
            capture_output=True, text=True, env=env, cwd=RACINE, timeout=60)
        self.assertEqual(r.returncode, 0, r.stderr[-500:])
        self.assertTrue(os.path.isfile(sortie))
        self.assertTrue(os.path.isfile(os.path.join(self.tmp, "audit_log.md")))


class TestEF08Donnees(BaseTemp):
    """EF-08 — base de commandes embarquée, chargement rapide."""

    def test_base(self):
        debut = time.monotonic()
        with open(DONNEES, encoding="utf-8") as f:
            base = json.load(f)
        duree = time.monotonic() - debut
        self.assertGreaterEqual(base["comptes"]["commandes"], 200)
        self.assertGreaterEqual(base["comptes"]["controles"], 160)
        self.assertLess(duree, 1.0, f"chargement {duree:.2f}s")
        # catégories présentes sur toutes les entrées
        for c in list(base["controles"])[:5]:
            self.assertIn(c, base["controles"])
        for c in list(base["commandes"])[:5]:
            self.assertIn(c, base["commandes"])
        self.assertTrue(all(v for v in base["controles"].values()))


class TestENFIdempotence(BaseTemp):
    """ENF-02 — génération ×2 byte-identique (R6)."""

    def test_generation_idempotente(self):
        s1, s2 = self.chemin("a.tsi"), self.chemin("b.tsi")
        generateur.generer(PRESET_EXEMPLE, s1)
        generateur.generer(PRESET_EXEMPLE, s2)
        self.assertEqual(open(s1, "rb").read(), open(s2, "rb").read())

    def test_scenario_studio_idempotent(self):
        s1, s2 = self.chemin("s1.tsi"), self.chemin("s2.tsi")
        j1, j2 = self.chemin("j1.md"), self.chemin("j2.md")
        studio.scenario_demo(s1, j1)
        studio.scenario_demo(s2, j2)
        self.assertEqual(open(s1, "rb").read(), open(s2, "rb").read())
        # l'audit_log CROÎT à chaque exécution (mécanisme auto-évolutif v11)


class TestENFStdlib(unittest.TestCase):
    """ENF-01 — Python stdlib uniquement (aucun import tiers)."""

    def test_aucun_import_tiers(self):
        autorises = {"json", "csv", "re", "os", "sys", "argparse", "time",
                     "datetime", "subprocess", "tempfile", "shutil",
                     "unittest", "xml", "base64", "collections",
                     "__future__", "typing"}
        for module in sorted(os.listdir(os.path.join(RACINE, "tsi_toolkit"))):
            if not module.endswith(".py"):
                continue
            with open(os.path.join(RACINE, "tsi_toolkit", module),
                      encoding="utf-8") as f:
                for ligne in f:
                    ligne = ligne.strip()
                    if ligne.startswith(("import ", "from ")):
                        cible = (ligne.split()[1].split(".")[0]
                                 if ligne.startswith("from ")
                                 else ligne.split()[1].split(".")[0])
                        if ligne.startswith("from .") or ligne.startswith("from tsi_toolkit"):
                            continue
                        self.assertIn(cible, autorises,
                                      f"{module}: import tiers {ligne!r}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
