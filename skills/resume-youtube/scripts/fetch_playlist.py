#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""resume-youtube — Moteur 1 : extraction playlist YouTube (page + lockupViewModel).
Usage : fetch_playlist.py --url <url_playlist> --out <videos.json> [--n-max N]
Robuste : découpage par blocs '"lockupViewModel":{' (layout 2024+), fallback
playlistVideoRenderer (ancien layout). Ordre d'apparition = ordre de la playlist.
Sortie : {playlist_id, title, n_videos, videos: [{index, videoId, title, duration, author, url}]}
"""
import argparse
import json
import re
import subprocess
import sys

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")


def curl(url, timeout=40):
    p = subprocess.run(["curl", "-sL", "--max-time", str(timeout), "-A", UA,
                        "-H", "Accept-Language: fr-FR,fr;q=0.9", url],
                       capture_output=True, text=True, timeout=timeout + 10)
    return p.stdout or ""


def jstr(s):
    try:
        return json.loads('"' + s + '"')
    except Exception:
        return s


def parse_lockups(raw):
    videos, seen = [], set()
    for ch in raw.split('"lockupViewModel":{')[1:]:
        m_vid = re.search(r'"contentId":"([A-Za-z0-9_-]{11})"', ch)
        if not m_vid:
            continue
        vid = m_vid.group(1)
        m_tit = re.search(r'"lockupMetadataViewModel":\{"title":\{"content":"((?:[^"\\]|\\.)*)"', ch)
        title = jstr(m_tit.group(1)) if m_tit else ""
        m_dur = re.search(r'"thumbnailBadgeViewModel":\{"text":"(\d{1,2}:\d{2}(?::\d{2})?)"', ch)
        dur = m_dur.group(1) if m_dur else ""
        m_au = re.search(r'"a11yLabel":"(?:Accéder à la chaîne|Go to channel|Visiter la chaîne|Aller à la chaîne)\s*([^"]+)"', ch)
        author = jstr(m_au.group(1)).strip() if m_au else ""
        if vid not in seen and title:
            seen.add(vid)
            videos.append({"index": str(len(videos) + 1), "videoId": vid, "title": title,
                           "duration": dur, "author": author,
                           "url": "https://www.youtube.com/watch?v=" + vid})
    if not videos:  # fallback ancien layout
        for ch in raw.split('"playlistVideoRenderer":{')[1:]:
            m_vid = re.search(r'"videoId":"([A-Za-z0-9_-]{11})"', ch)
            m_tit = re.search(r'"title":\{"runs":\[\{"text":"((?:[^"\\]|\\.)*)"', ch)
            if m_vid and m_tit:
                vid = m_vid.group(1)
                if vid not in seen:
                    seen.add(vid)
                    videos.append({"index": str(len(videos) + 1), "videoId": vid,
                                   "title": jstr(m_tit.group(1)), "duration": "",
                                   "author": "", "url": "https://www.youtube.com/watch?v=" + vid})
    return videos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--n-max", type=int, default=0)
    a = ap.parse_args()

    m = re.search(r"[?&]list=([A-Za-z0-9_-]+)", a.url)
    if not m:
        print("ERREUR: pas d'ID de playlist dans l'URL", file=sys.stderr)
        sys.exit(2)
    pid = m.group(1)
    raw = curl("https://www.youtube.com/playlist?list=" + pid + "&hl=fr")
    videos = parse_lockups(raw)
    if a.n_max > 0:
        videos = videos[:a.n_max]
    title = ""
    mt = re.search(r"<title>([^<]*)</title>", raw)
    if mt:
        title = mt.group(1).replace(" - YouTube", "").strip()
    out = {"playlist_id": pid, "title": title, "n_videos": len(videos), "videos": videos}
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("PLAYLIST: {} | {} vidéos -> {}".format(title, len(videos), a.out))


if __name__ == "__main__":
    main()
