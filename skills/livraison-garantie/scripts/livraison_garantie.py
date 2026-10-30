#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""livraison-garantie v1.0.0 — ORCHESTRATEUR DE LIVRAISON EN BOUCLE FERMÉE.

Task 8 (directive propriétaire 2026-10-31 « crée $facon ces trois skills » —
suggestion D018-2, douleur prouvée du 2026-10-25 : 4 tours de livraison manuels,
mauvais fichier détecté par chance via des logs stderr perdus en voie chaude).

UN appel remplace la séquence manuelle :
  1. GARDE de dépendance : primitives vue-upload chargées par chemin, VERSION
     vérifiée >= 1.5.0 (rc 7 sinon) ;
  2. IDENTIFICATION : cible cherchée (nom exact assaini) dans download/ puis
     upload/ (rc 6 si absente) ; famille multi-versions / suspect au nom proche
     signalés (hygiène vue-upload v1.5.0) — jamais modifiés ici ;
  3. ÉPINGLAGE AVANT la fenêtre : marker featured posé (format vue-upload) —
     bannière ★ en tête du portail ;
  4. PORTAIL : start_inprocess de vue-upload (thread daemon, zéro subprocess) ;
  5. SURVEILLANCE : journal lu par POSITION (pré-fenêtre écarté), poll --poll s ;
  6. ARRÊT MÉCANIQUE : cible journalisée → CONFIRME immédiat (arrêt anticipé) ;
     fenêtre expirée → PARTIEL (mauvais fichier nommé, nom_proche marqué) ou
     AUCUN ;
  7. GUIDANCE mécanique dans la sortie (re-ciblage / hygiène / share).

Codes retour : 0 CONFIRME · 1 PARTIEL · 2 bind impossible · 6 cible absente ou nom
invalide · 7 AUCUN (ou dépendance vue-upload < 1.5.0).

R4 : ZÉRO duplication — le portail, le marker, le journal et la détection de
familles restent détenus par vue-upload ; ce skill ORCHESTRE.
"""
import argparse
import contextlib
import importlib.util
import io
import json
import os
import sys
import time

SKILL = "livraison-garantie"
VERSION = "1.0.0"
VUE_UPLOAD_REQUIS = (1, 5, 0)

PANEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "..", "vue-upload", "scripts", "vue_upload_panel.py")


def charge_vue_upload():
    """Charge les primitives vue-upload et vérifie la garde de version (>= 1.5.0)."""
    spec = importlib.util.spec_from_file_location("vue_upload_panel_orch", PANEL_PATH)
    mod = module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    ver = tuple(int(x) for x in mod.VERSION.split("."))
    if ver < VUE_UPLOAD_REQUIS:
        raise SystemExit("[%s] dépendance insuffisante : vue-upload %s < 1.5.0 "
                         "(journal/épinglage/hygiène requis) — réinstallez vue-upload"
                         % (SKILL, mod.VERSION))
    return mod


VU = charge_vue_upload()


def _taille_h(n):
    return VU.human(n)


def lit_journal_position(root, depart_lignes):
    """Nouvelles entrées du journal DEPUIS depart_lignes (position de départ).
    Best-effort : journal absent/corrompu = liste vide (ne fait jamais échouer)."""
    p = os.path.join(root, VU.JOURNAL)
    try:
        with open(p, encoding="utf-8") as f:
            lignes = [l.strip() for l in f if l.strip()]
    except Exception:
        return []
    out = []
    for l in lignes[depart_lignes:]:
        try:
            out.append(json.loads(l))
        except Exception:
            continue
    return out


def compte_lignes_journal(root):
    p = os.path.join(root, VU.JOURNAL)
    try:
        with open(p, encoding="utf-8") as f:
            return sum(1 for l in f if l.strip())
    except Exception:
        return 0


def epingle(root, dossier, fichier):
    """Pose le marker featured (MÊME format que vue-upload — interface documentée)."""
    ent = {"fichier": fichier, "dossier": dossier,
           "horodatage": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
           "pose_par": "%s v%s" % (SKILL, VERSION)}
    with open(os.path.join(root, VU.MARKER), "w", encoding="utf-8") as f:
        json.dump(ent, f, ensure_ascii=False, indent=1)
    return ent


def nom_proche(fichier_a, cible):
    """Vrai si fichier_a partage le radical exact ou le 1er token (>= 3 car.) de cible."""
    ra, rc = VU.radical_livrable(fichier_a), VU.radical_livrable(cible)
    if not ra or not rc:
        return False
    if ra == rc:
        return True
    ta, tc = ra.split("_")[0], rc.split("_")[0]
    return len(ta) >= 3 and ta == tc


def _fin(as_json, msg, code, extra=None):
    res = {"commande": "livraison-garantie", "skill": SKILL, "version": VERSION,
           "verdict": ("ERREUR" if code >= 2 else "ECHEC"), "erreur": msg, "rc": code}
    if extra:
        res.update(extra)
    if as_json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print("[%s] ERREUR : %s" % (SKILL, msg))
    return code


def main():
    ap = argparse.ArgumentParser(
        description="livraison-garantie — boucle fermée : épingler, surveiller, confirmer")
    ap.add_argument("--fichier", required=True, help="nom EXACT du livrable (download/ ou upload/)")
    ap.add_argument("--dir", default="auto", choices=["auto", "download", "upload"])
    ap.add_argument("--port", type=int, default=3000)
    ap.add_argument("--root", default="/home/z/my-project")
    ap.add_argument("--hold", type=int, default=540, help="fenêtre d'accès en secondes (<= 600)")
    ap.add_argument("--poll", type=float, default=0.5, help="période de sondage du journal (s)")
    ap.add_argument("--json", action="store_true", help="sortie machine-readable")
    a = ap.parse_args()
    t0 = time.perf_counter()
    root = os.path.realpath(a.root)
    as_json = a.json

    # 1-2. identification de la cible
    nom = VU.sanitize_name(a.fichier)
    if not nom:
        return _fin(as_json, "nom refusé (caché ou vide après assainissement) : %s" % a.fichier, 6)
    dirs = ("download", "upload") if a.dir == "auto" else (a.dir,)
    dossier = None
    for d in dirs:
        if os.path.isfile(os.path.join(root, d, nom)):
            dossier = d
            break
    if dossier is None:
        return _fin(as_json, "livrable introuvable dans %s : %s — poussez-le d'abord "
                             "(vue-upload push <source>)" % ("/".join(dirs), nom), 6,
                    {"cible": None})
    octets = os.path.getsize(os.path.join(root, dossier, nom))
    cible = {"dossier": dossier, "fichier": nom, "octets": octets, "taille": _taille_h(octets)}

    # hygiène : famille multi-versions / suspect impliquant la cible (signal, jamais action)
    avertissement = []
    det = VU.detect_versions(root)
    for e in det["exactes"]:
        if e["dossier"] == dossier and nom in e["fichiers"]:
            avertissement.append("famille multi-versions « %s » : %s — recommandé : push de "
                                 "la finale (archivage automatique v1.5.0) AVANT la livraison"
                                 % (e["radical"], ", ".join(e["fichiers"])))
    for s in det["suspects"]:
        if s["dossier"] == dossier and nom in s["fichiers"]:
            avertissement.append("suspect au nom proche « %s » : %s — annoncez le nom EXACT "
                                 "(+ taille) au propriétaire" % (s["token"], ", ".join(s["fichiers"])))

    # 3. épinglage AVANT la fenêtre
    epingle(root, dossier, nom)

    # 4. portail (primitives vue-upload)
    if VU.port_alive(a.port, 0.15):
        voie = "CHAUDE (portail déjà vivant)"
    else:
        try:
            _, bind = VU.start_inprocess(a.port, root)
            voie = "FROIDE (démarrage in-process, %s)" % bind
        except OSError as e:
            return _fin(as_json, "bind impossible :%d — %s" % (a.port, e), 2, {"cible": cible})
        for _ in range(30):
            if VU.port_alive(a.port, 0.1):
                break
            time.sleep(0.05)
    portail_vivant = VU.port_alive(a.port, 0.3)
    if not portail_vivant:
        return _fin(as_json, "portail mort après démarrage (:%d)" % a.port, 3, {"cible": cible})

    # 5-6. surveillance en boucle fermée (arrêt mécanique)
    depart_lignes = compte_lignes_journal(root)
    hold = max(1, min(a.hold, 600))
    fin = time.monotonic() + hold
    telechargements, mauvais_fichiers = [], []
    verdict, critere = None, None
    while True:
        for ent in lit_journal_position(root, depart_lignes):
            depart_lignes += 1
            f, d = ent.get("fichier", ""), ent.get("dossier", "")
            if f == nom and d == dossier:
                telechargements.append(ent)
                verdict, critere = "CONFIRME", "cible_telechargee"
                break
            telechargements.append(ent)
            mauvais_fichiers.append({"fichier": f, "dossier": d,
                                     "octets": ent.get("octets", 0),
                                     "nom_proche": nom_proche(f, nom)})
        if verdict:
            break
        if time.monotonic() >= fin:
            break
        time.sleep(max(0.1, a.poll))
    if verdict is None:
        if telechargements:
            verdict, critere = "PARTIEL", "fenetre_expiree_mauvais_fichier"
        else:
            verdict, critere = "AUCUN", "fenetre_expiree_sans_telechargement"

    # 7. guidance mécanique
    if verdict == "CONFIRME":
        guidance = ("livraison confirmée — consigner au worklog ; retirer l'épingle si "
                    "terminé (vue-upload featured --off)")
    elif verdict == "PARTIEL":
        guidance = ("MAUVAIS fichier pris (%s) — l'épinglé reste posé : réouvrir "
                    "(vue_upload_panel.py --hold 540) en annonçant le nom EXACT « %s » (%s) ; "
                    "si le mauvais fichier est une version supersédée : push de la finale "
                    "(archivage automatique) ; repli : share" % (
                        ", ".join(m["fichier"] for m in mauvais_fichiers) or "?", nom, cible["taille"]))
    else:
        edge = VU.edge_alive()
        guidance = ("aucun téléchargement pendant la fenêtre — vérifier que le preview a été "
                    "cliqué (%s) ; réouvrir une fenêtre ou basculer sur share (liens externes "
                    "vérifiés sha256)" % ("edge :81 vivant" if edge else "edge :81 ABSENT"))

    res = {
        "commande": "livraison-garantie", "skill": SKILL, "version": VERSION,
        "cible": cible, "epingle": {"fichier": nom, "dossier": dossier},
        "voie": voie, "portail_vivant": portail_vivant,
        "url_locale": "http://127.0.0.1:%d/" % a.port,
        "routage_preview": ("edge :81 vivant → proxifie vers :%d (cliquer le bouton preview "
                            "pendant la fenêtre)" % a.port) if VU.edge_alive()
                           else "edge :81 absent — voie locale seulement",
        "fenetre_s": hold, "avertissement_famille": avertissement,
        "telechargements": telechargements, "mauvais_fichiers": mauvais_fichiers,
        "verdict": verdict, "critere_arret": critere,
        "arret_anticipe": critere == "cible_telechargee",
        "duree_s": round(time.perf_counter() - t0, 2),
        "guidance": guidance,
    }
    if as_json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print("╔═ %s v%s — LIVRAISON EN BOUCLE FERMÉE — %.2f s" % (SKILL, VERSION, res["duree_s"]))
        print("║ cible : %s/%s — %s — épinglée ★ AVANT la fenêtre" % (dossier, nom, cible["taille"]))
        print("║ %s — portail vivant : %s" % (voie, portail_vivant))
        for w in avertissement:
            print("║ ⚠ %s" % w)
        print("║ verdict : %s (critère d'arrêt : %s)" % (verdict, critere))
        for e in telechargements:
            print("║   ↓ %s/%s — %s" % (e.get("dossier", "?"), e.get("fichier", "?"),
                                          _taille_h(e.get("octets", 0))))
        for m in mauvais_fichiers:
            print("║ ✗ mauvais fichier : %s/%s%s" % (m["dossier"], m["fichier"],
                                                     " (nom proche)" if m["nom_proche"] else ""))
        print("║ guidance : %s" % guidance)
        print("╚═" + "═" * 60)
    return {"CONFIRME": 0, "PARTIEL": 1, "AUCUN": 7}[verdict]


if __name__ == "__main__":
    sys.exit(main())
