#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vue-upload v1.2.0 — Serveur de fichiers local (portail d'accès aux livrables).
(Marqueur aligné v1.2.0, Task 39 — logique inchangée depuis v1.0.0.)
Task 31 (directive propriétaire 2026-10-05) : donner au propriétaire un accès
direct au dossier download/ (et upload/) depuis son navigateur.

Usage :
    python3 vue_upload_server.py [--port 3000] [--root /home/z/my-project]

Endpoints :
    GET  /                    → UI (liste download/ + upload/, formulaire d'envoi)
    GET  /files?dir=...       → JSON (rafraîchissement)
    GET  /get/<dir>/<fichier> → téléchargement
    POST /upload/<dir>        → téléversement (multipart/form-data)

Sécurité : racine verrouillée (anti-traversée realpath), noms assainis,
taille max d'envoi 200 Mo, méthodes limitées à GET/POST.
Dépendance : aucune (bibliothèque standard uniquement).
"""
import argparse
import html
import json
import mimetypes
import os
import re
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs, unquote

MAX_UPLOAD = 200 * 1024 * 1024  # 200 Mo
DIRS = {"download", "upload"}

PALETTE = {
    "bg": "162235", "surface": "1C2A3D", "line": "2A3B52",
    "text": "E8EEF6", "muted": "8FA3BC", "accent": "37DCF2", "accentDark": "1B6B7A",
}

PAGE = """<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>vue-upload — accès livrables</title>
<style>
:root {{ color-scheme: dark; }}
* {{ box-sizing: border-box; }}
body {{ margin:0; background:{bg}; color:{text};
       font-family:'Segoe UI',Arial,'Noto Sans',sans-serif; }}
.wrap {{ max-width:960px; margin:0 auto; padding:28px 18px 60px; }}
h1 {{ font-size:1.35rem; letter-spacing:.4px; margin:0 0 4px; }}
h1 .dot {{ color:{accent}; }}
.sub {{ color:{muted}; font-size:.86rem; margin-bottom:22px; }}
.card {{ background:{surface}; border:1px solid {line}; border-radius:12px;
        padding:16px 18px; margin-bottom:18px; }}
.drop {{ border:2px dashed {accentDark}; border-radius:10px; padding:18px;
        text-align:center; color:{muted}; cursor:pointer; transition:.15s; }}
.drop.over {{ border-color:{accent}; color:{accent}; }}
input[type=file] {{ display:none; }}
.btn {{ display:inline-block; background:{accentDark}; color:#fff; border:0;
       border-radius:8px; padding:8px 16px; font-size:.88rem; cursor:pointer; }}
.btn:hover {{ filter:brightness(1.15); }}
table {{ width:100%; border-collapse:collapse; font-size:.9rem; }}
th {{ text-align:left; color:{muted}; font-weight:600; font-size:.78rem;
     text-transform:uppercase; letter-spacing:.6px; padding:8px 6px;
     border-bottom:1px solid {line}; }}
td {{ padding:9px 6px; border-bottom:1px solid {line}; }}
tr:hover td {{ background:rgba(55,220,242,.05); }}
a.f {{ color:{accent}; text-decoration:none; word-break:break-all; }}
a.f:hover {{ text-decoration:underline; }}
.sz {{ color:{muted}; white-space:nowrap; }}
.dt {{ color:{muted}; white-space:nowrap; font-size:.82rem; }}
.tag {{ font-size:.68rem; border:1px solid {accentDark}; color:{accent};
       border-radius:99px; padding:2px 8px; margin-left:8px; vertical-align:middle; }}
.empty {{ color:{muted}; padding:14px 6px; }}
#toast {{ position:fixed; bottom:18px; left:50%; transform:translateX(-50%);
         background:{accentDark}; color:#fff; padding:10px 22px; border-radius:99px;
         font-size:.88rem; opacity:0; pointer-events:none; transition:.25s; }}
#toast.on {{ opacity:1; }}
</style></head><body><div class="wrap">
<h1>vue-upload<span class="dot"> ▮</span></h1>
<div class="sub">Portail d'accès aux livrables — dossier racine : {root}</div>

<div class="card">
  <table><thead><tr><th>Livrables (download/)</th><th>Taille</th><th>Modifié</th></tr></thead>
  <tbody id="dl"></tbody></table>
</div>

<div class="card">
  <table><thead><tr><th>Fichiers reçus (upload/)</th><th>Taille</th><th>Modifié</th></tr></thead>
  <tbody id="up"></tbody></table>
</div>

<div class="card">
  <form id="form" action="/upload/{{DIR}}" method="post" enctype="multipart/form-data">
    <div class="drop" id="drop">Glissez vos fichiers ici ou cliquez pour choisir
      <div style="margin-top:10px"><button class="btn" type="button" id="pick">Choisir…</button></div>
      <input type="file" id="files" multiple>
    </div>
    <div style="margin-top:12px; display:flex; gap:14px; align-items:center;">
      <label style="font-size:.85rem;color:{muted}">Destination :
        <select name="dir" id="dirsel" style="background:{bg};color:{text};
                border:1px solid {line};border-radius:6px;padding:5px 8px">
          <option value="upload">upload/ (fichiers pour l'agent)</option>
          <option value="download">download/ (livrables)</option>
        </select></label>
      <button class="btn" type="submit">Téléverser</button>
      <span id="prog" style="color:{muted};font-size:.84rem"></span>
    </div>
  </form>
</div>
<div id="toast"></div>
<script>
const fmt = b => b<1024 ? b+' o' : b<1048576 ? (b/1024).toFixed(1)+' Ko' : (b/1048576).toFixed(1)+' Mo';
const esc = s => s.replace(/[&<>"']/g, c => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}})[c]);
async function refresh() {{
  const r = await fetch('/files'); const j = await r.json();
  for (const [dir, tb] of [['download', '#dl'], ['upload', '#up']]) {{
    const rows = (j[dir] || []).map(f =>
      `<tr><td><a class="f" href="/get/${{dir}}/${{encodeURIComponent(f.name)}}">${{esc(f.name)}}</a></td>` +
      `<td class="sz">${{fmt(f.size)}}</td><td class="dt">${{f.mtime}}</td></tr>`);
    document.querySelector(tb).innerHTML =
      rows.length ? rows.join('') : '<tr><td colspan="3" class="empty">— vide —</td></tr>';
  }}
}}
const drop = document.getElementById('drop'), input = document.getElementById('files');
document.getElementById('pick').onclick = e => {{ e.stopPropagation(); input.click(); }};
drop.onclick = () => input.click();
['dragover','dragenter'].forEach(ev => drop.addEventListener(ev, e => {{ e.preventDefault(); drop.classList.add('over'); }}));
['dragleave','drop'].forEach(ev => drop.addEventListener(ev, e => {{ e.preventDefault(); drop.classList.remove('over'); }}));
drop.addEventListener('drop', e => {{ input.files = e.dataTransfer.files; }});
document.getElementById('form').addEventListener('submit', async e => {{
  e.preventDefault();
  const dir = document.getElementById('dirsel').value;
  if (!input.files.length) {{ toast('Aucun fichier choisi'); return; }}
  const fd = new FormData();
  for (const f of input.files) fd.append('files', f, f.name);
  document.getElementById('prog').textContent = 'envoi en cours…';
  const r = await fetch('/upload/' + dir, {{ method:'POST', body:fd }});
  const j = await r.json();
  document.getElementById('prog').textContent = '';
  toast(j.saved ? j.saved.length + ' fichier(s) téléversé(s) vers ' + dir + '/' : (j.error || 'échec'));
  if (j.saved) {{ input.value = ''; refresh(); }}
}});
let tt; function toast(m) {{
  const t = document.getElementById('toast'); t.textContent = m; t.classList.add('on');
  clearTimeout(tt); tt = setTimeout(() => t.classList.remove('on'), 2600);
}}
refresh(); setInterval(refresh, 15000);
</script></div></body></html>"""


def safe_join(root, name):
    """Joins et verrouille name sous root (anti-traversée)."""
    name = os.path.basename(name or "")
    if not name or name.startswith("."):
        return None
    p = os.path.realpath(os.path.join(root, name))
    if p != os.path.join(os.path.realpath(root), name):
        return None
    return p


class Handler(BaseHTTPRequestHandler):
    server_version = "vue-upload/1.2.0"
    root = "/home/z/my-project"

    def log_message(self, fmt, *args):
        sys.stderr.write("[vue-upload] %s\n" % (fmt % args))

    # ── helpers ──────────────────────────────────────────────
    def _json(self, obj, code=200):
        b = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(b)

    def _listing(self):
        out = {}
        for d in DIRS:
            base = os.path.join(self.root, d)
            os.makedirs(base, exist_ok=True)
            items = []
            for n in sorted(os.listdir(base)):
                p = os.path.join(base, n)
                if os.path.isfile(p):
                    st = os.stat(p)
                    items.append({"name": n, "size": st.st_size,
                                  "mtime": time.strftime("%Y-%m-%d %H:%M", time.localtime(st.st_mtime))})
            out[d] = items
        return out

    # ── GET ──────────────────────────────────────────────────
    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/":
            page = PAGE.format(root=html.escape(self.root), DIR="upload", **PALETTE)
            b = page.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(b)))
            self.end_headers()
            self.wfile.write(b)
        elif u.path == "/files":
            self._json(self._listing())
        elif u.path.startswith("/get/"):
            parts = [unquote(x) for x in u.path.split("/")[2:] if x]
            if len(parts) != 2 or parts[0] not in DIRS:
                return self._json({"error": "chemin invalide"}, 400)
            p = safe_join(os.path.join(self.root, parts[0]), parts[1])
            if not p or not os.path.isfile(p):
                return self._json({"error": "fichier introuvable"}, 404)
            ctype = mimetypes.guess_type(p)[0] or "application/octet-stream"
            size = os.path.getsize(p)
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(size))
            self.send_header("Content-Disposition",
                             'attachment; filename="%s"' % parts[1].replace('"', ""))
            self.end_headers()
            with open(p, "rb") as f:
                while chunk := f.read(65536):
                    self.wfile.write(chunk)
        else:
            self._json({"error": "introuvable"}, 404)

    # ── POST (multipart maison, sans dépendance) ─────────────
    def do_POST(self):
        u = urlparse(self.path)
        m = re.match(r"^/upload/(download|upload)$", u.path)
        if not m:
            return self._json({"error": "endpoint inconnu"}, 404)
        dest_dir = m.group(1)
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = 0
        if length <= 0 or length > MAX_UPLOAD:
            return self._json({"error": "taille invalide ou > 200 Mo"}, 413)
        ctype = self.headers.get("Content-Type", "")
        mm = re.search(r'boundary=(?:"([^"]+)"|([^;]+))', ctype)
        if "multipart/form-data" not in ctype or not mm:
            return self._json({"error": "multipart requis"}, 400)
        boundary = (mm.group(1) or mm.group(2)).strip().encode()
        body = self.rfile.read(length)

        saved, errors = [], []
        for part in body.split(b"--" + boundary):
            part = part.strip(b"\r\n")
            if not part or part == b"--":
                continue
            if b"\r\n\r\n" not in part:
                continue
            head, _, data = part.partition(b"\r\n\r\n")
            htxt = head.decode("utf-8", "replace")
            fn = re.search(r'filename="([^"]*)"', htxt)
            if not fn or fn.group(1) == "":
                continue  # champ non-fichier
            name = os.path.basename(fn.group(1))
            name = re.sub(r'[\\/:*?"<>|]', "_", name).strip() or "sans-nom"
            p = safe_join(os.path.join(self.root, dest_dir), name)
            if not p:
                errors.append(name + " : nom refusé")
                continue
            if data.endswith(b"\r\n"):
                data = data[:-2]
            with open(p, "wb") as f:
                f.write(data)
            saved.append(dest_dir + "/" + name)
        self._json({"saved": saved, "errors": errors})


def main():
    import socket
    ap = argparse.ArgumentParser(description="vue-upload — portail d'accès aux livrables")
    ap.add_argument("--port", type=int, default=3000)
    ap.add_argument("--root", default="/home/z/my-project")
    a = ap.parse_args()
    Handler.root = os.path.realpath(a.root)
    for d in DIRS:
        os.makedirs(os.path.join(Handler.root, d), exist_ok=True)

    class DualStackServer(ThreadingHTTPServer):
        address_family = socket.AF_INET6
        daemon_threads = True

        def server_bind(self):
            try:
                self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
            except OSError:
                pass
            super().server_bind()

    try:
        srv = DualStackServer(("::", a.port), Handler)
    except OSError:
        ThreadingHTTPServer.address_family = socket.AF_INET
        srv = ThreadingHTTPServer(("0.0.0.0", a.port), Handler)
    print("vue-upload v1.2.0 — écoute [::]:%d (dual-stack) — racine %s" % (a.port, Handler.root), flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
