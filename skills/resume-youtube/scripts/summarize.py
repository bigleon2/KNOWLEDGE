#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""resume-youtube — Moteur 3 : résumés LLM via CLI z-ai (D004), honnêteté R3.
Usage : summarize.py --videos <videos.json> --transcripts <dir> --out <resumes.json> [--limit N]
Niveaux de preuve (consignés, jamais fabriqués) :
  transcript  -> résumé depuis les sous-titres réels (chunking ≤12k, 2 chunks max)
  description -> résumé depuis description + titre (si moteur page_reader fourni dans le JSON)
  metadata    -> inférence de titre/chaîne seuls, explicitement libellée « inférence »
Idempotent : vidéos déjà présentes dans --out => skip (KO-L001).
Backoff 429 : 20 s × tentative, max 4 (pattern certifié runner Task 21).
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time

CHUNK = 12000
SYS = ("Tu es un analyste de contenus vidéo. Tu résumes avec précision, en français, "
       "sans rien inventer : uniquement ce que la source fournit.")


def zai_chat(prompt, timeout=150):
    for attempt in range(4):
        try:
            r = subprocess.run(["z-ai", "chat", "-p", prompt, "-s", SYS],
                               capture_output=True, text=True, timeout=timeout)
            out = (r.stdout or "") + "\n" + (r.stderr or "")
            answers = re.findall(r'"content"\s*:\s*"([^"]*)"', out)
            if answers:
                time.sleep(4)  # politesse inter-appels (KO-L001)
                return answers[-1]
            if "429" in out or "Too many requests" in out:
                wait = 20 * (attempt + 1)
                print("    [429] backoff {}s".format(wait), flush=True)
                time.sleep(wait)
                continue
            time.sleep(4)
            return ""
        except Exception:
            time.sleep(10)
    return ""


def chunk_text(txt):
    if len(txt) <= CHUNK:
        return [txt]
    return [txt[:CHUNK * 2 // 3], txt[-CHUNK // 3:]]


def build_prompt(v, chunks, level):
    meta = "TITRE : {}\nCHAÎNE : {}\nDURÉE : {}".format(
        v.get("title", ""), v.get("author", ""), v.get("duration", ""))
    if level == "transcript":
        src = "SOURCE : sous-titres réels de la vidéo.\n" + meta + "\n\nCONTENU :\n" + chunks[0]
    elif level == "description":
        src = "SOURCE : métadonnées enrichies (description).\n" + meta + \
              "\n\nDESCRIPTION :\n" + v.get("description", "")
    elif level == "metadata":
        src = ("SOURCE : MÉTADONNÉES SEULES (pas de sous-titres accessibles).\n" + meta +
               "\n\nConsigne d'honnêteté : déduis UNIQUEMENT ce que le titre/la durée "
               "permettent d'inférer. Commence « resume » par « [Inférence de titre] ». "
               "Si le titre est ambigu, dis-le explicitement dans « resume ».")
    else:
        return None
    return ("Analyse cette vidéo et produis en français, au format JSON strict avec les clés "
            "\"resume\" (2-4 phrases), \"points_cles\" (3-5 puces), \"outils_concepts\" "
            "(liste), \"lecons_planification\" (1-3 leçons applicables à la conception de "
            "plans d'actions robustes). N'invente RIEN au-delà de la source.\n\n" + src)


def merge_prompt(v, part_a, part_b):
    return ("Voici deux extraits (début/fin) des sous-titres d'une même vidéo. Produis en "
            "français un JSON strict {\"resume\", \"points_cles\", \"outils_concepts\", "
            "\"lecons_planification\"} fidèle aux extraits, sans invention.\n\nTITRE : {}\n"
            "\n--- EXTRAIT DÉBUT ---\n{}\n\n--- EXTRAIT FIN ---\n{}".format(
                v.get("title", ""), part_a, part_b))


def parse_json_loose(s):
    m = re.search(r"\{[\s\S]*\}", s)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--videos", required=True)
    ap.add_argument("--transcripts", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--force-video", default="", help="refaire la synthèse d'une vidéo précise (repasse anti-hallucination)")
    a = ap.parse_args()

    vids = json.load(open(a.videos, encoding="utf-8")).get("videos", [])
    resumes = {}
    if os.path.exists(a.out):
        try:
            for r in json.load(open(a.out, encoding="utf-8")):
                resumes[r["videoId"]] = r
        except Exception:
            resumes = {}
    if a.force_video:
        resumes.pop(a.force_video, None)

    done = 0
    for v in vids:
        if a.limit and done >= a.limit:
            break
        vid = v["videoId"]
        if vid in resumes:
            continue
        tfile = os.path.join(a.transcripts, vid + ".json")
        tdata = {}
        if os.path.exists(tfile):
            try:
                tdata = json.load(open(tfile, encoding="utf-8"))
            except Exception:
                tdata = {}
        level, summary = "metadata", None
        if tdata.get("n_chars", 0) > 0:
            level = "transcript"
            chunks = chunk_text(tdata["transcript"])
            if len(chunks) == 1:
                summary = parse_json_loose(zai_chat(build_prompt(v, chunks, "transcript")))
            else:
                pa = parse_json_loose(zai_chat(build_prompt(v, [chunks[0]], "transcript")))
                pb = parse_json_loose(zai_chat(build_prompt(v, [chunks[1]], "transcript")))
                summary = parse_json_loose(merge_prompt(v, json.dumps(pa or {}, ensure_ascii=False),
                                                        json.dumps(pb or {}, ensure_ascii=False)))
        elif v.get("description"):
            level = "description"
            summary = parse_json_loose(zai_chat(build_prompt(v, [], "description")))
        else:
            level = "metadata"
            summary = parse_json_loose(zai_chat(build_prompt(v, [], "metadata")))
        if not summary:
            summary = {"resume": "Indisponible dans cet environnement (aucune source accessible). "
                                 "Inférence de titre uniquement : « {} ».".format(v.get("title", "")),
                       "points_cles": [], "outils_concepts": [], "lecons_planification": []}
            level = "metadata"
        rec = {"videoId": vid, "title": v.get("title", ""), "author": v.get("author", ""),
               "url": v.get("url", ""), "niveau_preuve": level, **summary}
        resumes[vid] = rec
        done += 1
        print("[+] {} niveau={} {}".format(vid, level, v.get("title", "")[:40]), flush=True)
        with open(a.out, "w", encoding="utf-8") as f:
            json.dump(list(resumes.values()), f, ensure_ascii=False, indent=2)
    print("TERMINE: {} nouveaux, {} total".format(done, len(resumes)))


if __name__ == "__main__":
    main()
