#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""resume-youtube — Moteur 2 : transcripts multi-moteurs (D002), honnêteté R3.
Usage : fetch_transcripts.py --videos <videos.json> --out <dir> [--lang fr,en]
Ordre strict par vidéo :
  1. yt-dlp (binaire PATH ou .venv-yt/bin/yt-dlp)         -> sous-titres auto/manuels
  2. youtube-transcript-api (lib importable)               -> watch page
  3. Invidious rotation (api.invidious.io + fallbacks)     -> /api/v1/captions/VID
  4. agent-browser (open + eval get_transcript params réels)
  5. échec honnête : status "indisponible" (jamais de fabrication — R3)
Idempotent (KO-L001) : transcript existant avec n_chars>0 => skip.
Sortie : <out>/<videoId>.json {videoId, engine_used, status, lang, n_chars, transcript}
       + <out>/index_transcripts.json
"""
import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.parse

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
INVIDIOUS_FALLBACK = ["inv.nadeko.net", "invidious.tiekoetter.com", "yt.chocolatemoo53.com",
                      "invidious.f5.si", "invidious.nerdvpn.de"]

YT_DLP_BIN = None
for cand in (shutil.which("yt-dlp"), "/home/z/my-project/.venv-yt/bin/yt-dlp"):
    if cand and os.path.exists(cand):
        YT_DLP_BIN = cand
        break

try:
    import youtube_transcript_api  # noqa: F401
    HAS_YTA = True
except Exception:
    HAS_YTA = False


def curl(url, timeout=35):
    try:
        p = subprocess.run(["curl", "-sL", "--max-time", str(timeout), "--compressed",
                            "-A", UA, "-H", "Accept-Language: fr-FR,fr;q=0.9", url],
                           capture_output=True, text=True, timeout=timeout + 10)
        return p.stdout or ""
    except Exception:
        return ""


def vtt_to_text(raw):
    lines = []
    for ln in raw.splitlines():
        if not ln.strip() or ln.startswith(("WEBVTT", "NOTE", "Kind:", "Language:",
                                            "META")) or "-->" in ln or re.match(r"^\d+$", ln.strip()):
            continue
        t = html.unescape(re.sub(r"<[^>]+>", "", ln)).strip()
        if t and (not lines or t != lines[-1]):
            lines.append(t)
    return "\n".join(lines)


def eng_ytdlp(vid, langs):
    if not YT_DLP_BIN:
        return None
    tmp = "/tmp/ryt_{}".format(vid)
    cmd = [YT_DLP_BIN, "--skip-download", "--write-auto-sub", "--write-sub",
           "--sub-lang", ",".join(langs), "--sub-format", "vtt", "-o", tmp,
           "https://www.youtube.com/watch?v=" + vid]
    try:
        subprocess.run(cmd, capture_output=True, text=True, timeout=90)
        for suf in (".fr.vtt", ".en.vtt", ".vtt"):
            f = tmp + suf
            if os.path.exists(f):
                txt = vtt_to_text(open(f, encoding="utf-8", errors="ignore").read())
                os.remove(f)
                if txt:
                    return {"text": txt, "lang": suf[1:3]}
    except Exception:
        pass
    return None


def eng_yta(vid, langs):
    if not HAS_YTA:
        return None
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        api = YouTubeTranscriptApi()
        t = api.fetch(vid, languages=list(langs))
        txt = "\n".join(s.text.strip() for s in t.snippets if s.text.strip())
        return {"text": txt, "lang": t.language_code} if txt else None
    except Exception:
        return None


_INV_CACHE = None      # liste d'instances (1 fetch / run)
_INV_DISABLED = False  # disjoncteur : 2 vidéos consécutives sans succès -> moteur coupé
_INV_FAILS = 0


def _invidious_instances():
    global _INV_CACHE
    if _INV_CACHE is None:
        instances = list(INVIDIOUS_FALLBACK)
        try:
            lst = json.loads(curl("https://api.invidious.io/instances.json?sort_by=health", 15))
            inst = [i[0] for i in lst if len(i) > 1 and isinstance(i[1], dict) and i[1].get("type") == "https"]
            if inst:
                instances = (inst[:8] + [x for x in INVIDIOUS_FALLBACK if x not in inst[:8]])[:10]
        except Exception:
            pass
        _INV_CACHE = instances
    return _INV_CACHE


def eng_invidious(vid, langs):
    global _INV_DISABLED, _INV_FAILS
    if _INV_DISABLED:
        return None
    for base in _invidious_instances()[:4]:
        try:
            lst_raw = curl("{}/api/v1/captions/{}".format(base, vid), 12)
            caps = json.loads(lst_raw).get("captions", []) if lst_raw.strip().startswith("{") else []
            if not caps:
                continue
            caps.sort(key=lambda c: (0 if c.get("languageCode", "").startswith(langs[0][:2]) else
                                     (1 if c.get("languageCode", "").startswith(langs[-1][:2]) else 2)))
            url = base + caps[0]["url"]
            vtt = curl(url, 25)
            txt = vtt_to_text(vtt) if vtt else ""
            if txt:
                _INV_FAILS = 0
                return {"text": txt, "lang": caps[0].get("languageCode", "?"), "instance": base}
        except Exception:
            continue
    _INV_FAILS += 1
    if _INV_FAILS >= 2:
        _INV_DISABLED = True
        print("    [disjoncteur] invidious coupé (2 échecs consécutifs — blocage IP)", flush=True)
    return None


EVAL_GT = """(function(){try{var d=window.ytInitialData||{};var p=null;var ps=d.engagementPanels||[];
for(var i=0;i<ps.length;i++){try{var c=ps[i].engagementPanelSectionListRenderer||{};
var ce=((c.content||{}).continuationItemRenderer||{}).continuationEndpoint||{};
if((ce.getTranscriptEndpoint||{}).params){p=ce.getTranscriptEndpoint.params;break;}}catch(e){}}
if(!p)return JSON.stringify({err:'no_params'});
var ctx=window.ytcfg.get('INNERTUBE_CONTEXT');
var x=new XMLHttpRequest();x.open('POST','/youtubei/v1/get_transcript?prettyPrint=false',false);
x.setRequestHeader('Content-Type','application/json');
x.send(JSON.stringify({context:ctx,params:p}));
var j=JSON.parse(x.responseText);
var t=j.actions[0].updateEngagementPanelAction.content.transcriptRenderer
.content.transcriptSearchPanelRenderer.body.transcriptSegmentListRenderer.initialSegments;
var out=[];for(var k=0;k<t.length;k++){try{var s=t[k].transcriptSegmentRenderer;
var r=(s.snippet||{}).runs||[];out.push(r.map(function(x){return x.text}).join(''));}catch(e){}}
return JSON.stringify({n:out.length,text:out.join('\\n').slice(0,120000)});}catch(e){
return JSON.stringify({err:String(e).slice(0,120)});}})()"""


def eng_browser(vid, langs):
    ab = shutil.which("agent-browser")
    if not ab:
        return None
    try:
        subprocess.run([ab, "open", "https://www.youtube.com/watch?v=" + vid + "&hl=fr"],
                       capture_output=True, text=True, timeout=60)
        time.sleep(5)
        r = subprocess.run([ab, "eval", EVAL_GT], capture_output=True, text=True, timeout=60)
        m = re.search(r'\{.*\}', r.stdout or "", re.S)
        if not m:
            return None
        j = json.loads(m.group(0).encode().decode("unicode_escape", errors="ignore"))
        txt = j.get("text", "")
        return {"text": txt, "lang": "page"} if txt else None
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--videos", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--lang", default="fr,en")
    ap.add_argument("--keep-failed", action="store_true",
                    help="ne retente pas les vidéos déjà en échec (accélérateur campagne)")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    langs = [x.strip() for x in a.lang.split(",") if x.strip()]

    data = json.load(open(a.videos, encoding="utf-8"))
    vids = data.get("videos", data if isinstance(data, list) else [])
    stats = {"n_total": len(vids), "ok": 0, "skip": 0, "indisponible": 0}
    index = []
    for i, v in enumerate(vids, 1):
        vid = v["videoId"]
        outf = os.path.join(a.out, vid + ".json")
        if os.path.exists(outf):
            try:
                prev = json.load(open(outf, encoding="utf-8"))
                if prev.get("n_chars", 0) > 0:
                    stats["skip"] += 1
                    stats["ok"] += 1
                    index.append({"videoId": vid, "status": "skip-done",
                                  "engine_used": prev.get("engine_used", ""),
                                  "n_chars": prev["n_chars"]})
                    continue
                if a.keep_failed and prev.get("status") == "indisponible":
                    stats["indisponible"] += 1
                    index.append({"videoId": vid, "status": "indisponible (conservé)",
                                  "engine_used": "", "n_chars": 0})
                    continue
            except Exception:
                pass
        res, engine = None, ""
        for name, fn in (("yt-dlp", eng_ytdlp), ("youtube-transcript-api", eng_yta),
                         ("invidious", eng_invidious), ("agent-browser", eng_browser)):
            try:
                res = fn(vid, langs)
            except Exception:
                res = None
            if res and res.get("text"):
                engine = name
                break
        if res:
            rec = {"videoId": vid, "title": v.get("title", ""), "engine_used": engine,
                   "status": "OK", "lang": res.get("lang", "?"), "n_chars": len(res["text"]),
                   "transcript": res["text"][:120000]}
            stats["ok"] += 1
        else:
            rec = {"videoId": vid, "title": v.get("title", ""), "engine_used": "",
                   "status": "indisponible", "lang": "", "n_chars": 0, "transcript": ""}
            stats["indisponible"] += 1
        with open(outf, "w", encoding="utf-8") as f:
            json.dump(rec, f, ensure_ascii=False)
        index.append({"videoId": vid, "status": rec["status"], "engine_used": engine,
                      "n_chars": rec["n_chars"]})
        print("[{}/{}] {} {} ({})".format(i, len(vids), rec["status"], vid, engine or "-"),
              flush=True)
    with open(os.path.join(a.out, "index_transcripts.json"), "w", encoding="utf-8") as f:
        json.dump(dict(stats, videos=index), f, ensure_ascii=False, indent=2)
    print("TERMINE: OK={} skip={} indisponible={}".format(stats["ok"], stats["skip"],
                                                          stats["indisponible"]))


if __name__ == "__main__":
    main()
