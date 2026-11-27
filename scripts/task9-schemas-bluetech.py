#!/usr/bin/env python3
"""Task 9 G2 — 3 schémas structurels du full stack kps-converter.

Rendu Playwright+CSS (skill charts — jamais matplotlib pour les structurels).
Thème blue-tech (template skills/pdf/templates/blue-tech) : fond #111827,
surface #1f2937, accents #38bdf8 / #a5b4fc — palette sombre exclusive.
Règles charts _rules.md : 0 chevauchement, hiérarchie visible, fonds non saturés.
Sorties : download/schema-1-architecture.png / schema-2-flux-requete.png /
          schema-3-cycle-fiche.png
"""

# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.47)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
# Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
# Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

import asyncio
from pathlib import Path

from playwright.async_api import async_playwright

OUT = Path("/home/z/my-project/download")

BASE_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap');
* { margin:0; padding:0; box-sizing:border-box; }
body {
  background:#111827; color:#f8fafc;
  font-family:'Inter','Noto Sans SC',sans-serif;
  width:1400px; padding:48px 56px 56px 56px;
}
.head { margin-bottom:30px; }
.head .kicker { font-family:'JetBrains Mono',monospace; font-size:15px;
  color:#38bdf8; letter-spacing:3px; text-transform:uppercase; }
.head h1 { font-size:30px; font-weight:800; margin-top:6px; }
.head .sub { font-size:15px; color:#94a3b8; margin-top:6px; }
.phase { background:#1f2937; border:1px solid #334155; border-left:5px solid #38bdf8;
  border-radius:12px; padding:20px 24px; }
.phase + .arrow { text-align:center; color:#38bdf8; font-size:26px;
  font-weight:800; padding:8px 0; }
.phase h2 { font-size:16px; font-weight:700; color:#38bdf8; letter-spacing:2px;
  text-transform:uppercase; margin-bottom:14px; }
.row { display:flex; gap:16px; }
.node { flex:1; background:#111827; border:2px solid #38bdf8; border-radius:10px;
  padding:14px 16px; }
.node.alt { border-color:#a5b4fc; }
.node .t { font-size:16px; font-weight:700; }
.node .d { font-size:13px; color:#94a3b8; margin-top:5px; line-height:1.45; }
.node .tag { display:inline-block; font-family:'JetBrains Mono',monospace;
  font-size:11px; color:#a5b4fc; border:1px solid #a5b4fc; border-radius:5px;
  padding:1px 7px; margin-bottom:7px; }
.foot { margin-top:16px; font-family:'JetBrains Mono',monospace; font-size:12px;
  color:#94a3b8; text-align:right; }
"""

DOC1 = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>{BASE_CSS}</style></head><body>
<div class="head">
  <div class="kicker">Schéma 1 / 3 — Architecture</div>
  <h1>Architecture monorepo — kps-converter</h1>
  <div class="sub">Convertisseur KPS Standardized Work (Kubota Production System) · fiche démo TA-S-3055-020</div>
</div>
<div class="phase">
  <h2>Phase A — Client navigateur (port 5173)</h2>
  <div class="row">
    <div class="node"><span class="tag">React 18 + TS + Vite</span>
      <div class="t">6 vues</div>
      <div class="d">Sélecteur · fiche KPS · éditeur temps + simulateur · import non-KPS · photos · audit C1-C10</div></div>
    <div class="node alt"><span class="tag">Tailwind</span>
      <div class="t">Composant cerclé CSS ①..⑩</div>
      <div class="d">Rendu garanti en atelier — aucune police d'icônes requise</div></div>
    <div class="node"><span class="tag">proxy Vite</span>
      <div class="t">/api et /uploads → 3001</div>
      <div class="d">Aiguillage unique vers l'API en développement</div></div>
  </div>
</div>
<div class="arrow">▼&nbsp;&nbsp;HTTP JSON · multipart</div>
<div class="phase">
  <h2>Phase B — Serveur API (port 3001)</h2>
  <div class="row">
    <div class="node"><span class="tag">Express + TS</span>
      <div class="t">11 contrats REST</div>
      <div class="d">health · standards CRUD · demo/reset · convert/parse · uploads · vision 501 · exports md/json</div></div>
    <div class="node alt"><span class="tag">Zod</span>
      <div class="t">Validation unifiée</div>
      <div class="d">400 « Validation échouée » + details[] — format unique toutes routes</div></div>
    <div class="node"><span class="tag">Idempotency-Key</span>
      <div class="t">SHA-256 + cache 2xx</div>
      <div class="d">même clé + hash différent → 409 · purge 7 jours au démarrage</div></div>
    <div class="node alt"><span class="tag">kpsAudit</span>
      <div class="t">C1-C10 miroir</div>
      <div class="d">algorithme byte-identique client/serveur (test dédié) — démo 100 %</div></div>
  </div>
</div>
<div class="arrow">▼&nbsp;&nbsp;Prisma Client (transactions)</div>
<div class="phase">
  <h2>Phase C — Persistance &amp; déploiement</h2>
  <div class="row">
    <div class="node"><span class="tag">Prisma + SQLite</span>
      <div class="t">5 modèles</div>
      <div class="d">AssemblyStandard · BomPart · ProcessStep · MediaAsset · IdempotencyRecord</div></div>
    <div class="node alt"><span class="tag">Seed idempotent</span>
      <div class="t">UPSERT TA-S-3055-020</div>
      <div class="d">enfants remplacés en transaction — ×10 sans duplication (7 pièces, 5 étapes, 144 s / Takt 150 s)</div></div>
    <div class="node"><span class="tag">Docker multi-stage</span>
      <div class="t">Node 20 Alpine</div>
      <div class="d">volumes kps_db / kps_uploads · healthcheck /api/health · entrypoint db push + seed + node dist</div></div>
  </div>
</div>
<div class="foot">production : Express sert client/dist — repli SPA hors /api et /uploads</div>
</body></html>"""

DOC2 = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>{BASE_CSS}</style></head><body>
<div class="head">
  <div class="kicker">Schéma 2 / 3 — Flux de données</div>
  <h1>Parcours d'une requête API — garanties d'idempotence</h1>
  <div class="sub">Chaque étape applique une garantie vérifiée par les 26 tests Vitest + Supertest</div>
</div>
<div class="phase">
  <h2>Étape 1 — Émission</h2>
  <div class="row">
    <div class="node"><span class="tag">Client React</span>
      <div class="t">fetch /api/…</div>
      <div class="d">Idempotency-Key optionnelle dans les en-têtes · uploads multipart 10 Mo max (PNG/JPEG/WebP/PDF)</div></div>
    <div class="node alt"><span class="tag">proxy</span>
      <div class="t">Vite :5173 → :3001</div>
      <div class="d">/api et /uploads aiguillés sans réécriture</div></div>
  </div>
</div>
<div class="arrow">▼</div>
<div class="phase">
  <h2>Étape 2 — Validation Zod</h2>
  <div class="row">
    <div class="node"><span class="tag">schémas partagés</span>
      <div class="t">refine métier</div>
      <div class="d">linkedPartIndexes cohérents · continuité des étapes signalée en warning — jamais d'invention</div></div>
    <div class="node alt"><span class="tag">échec → 400</span>
      <div class="t">format unique</div>
      <div class="d">{{ error, details: [{{ path, message }}] }} — même contrat sur les 11 routes</div></div>
  </div>
</div>
<div class="arrow">▼</div>
<div class="phase">
  <h2>Étape 3 — Garde d'idempotence</h2>
  <div class="row">
    <div class="node"><span class="tag">requestHash SHA-256</span>
      <div class="t">méthode + chemin + corps</div>
      <div class="d">empreinte du fichier intégrée pour les uploads multipart</div></div>
    <div class="node alt"><span class="tag">même clé, même hash</span>
      <div class="t">rejeu du 2xx en cache</div>
      <div class="d">aucun doublon créé — les 4xx/5xx ne sont jamais mis en cache</div></div>
    <div class="node"><span class="tag">même clé, autre hash</span>
      <div class="t">409 Conflict</div>
      <div class="d">collision détectée avant toute écriture</div></div>
  </div>
</div>
<div class="arrow">▼</div>
<div class="phase">
  <h2>Étape 4 — Persistance transactionnelle</h2>
  <div class="row">
    <div class="node"><span class="tag">Prisma $transaction</span>
      <div class="t">enfants remplacés atomiquement</div>
      <div class="d">bomParts + steps supprimés puis recréés — count contrôlé à chaque rejeu</div></div>
    <div class="node alt"><span class="tag">uploads dédupliqués</span>
      <div class="t">stockage &lt;sha256&gt;.ext</span></div>
      <div class="d">contenu déjà connu → MediaAsset existant renvoyé (200), rien réécrit</div></div>
  </div>
</div>
<div class="arrow">▼</div>
<div class="phase">
  <h2>Étape 5 — Réponse</h2>
  <div class="row">
    <div class="node"><span class="tag">JSON</span>
      <div class="t">fiche + auditScore %</div>
      <div class="d">standards triés docNumber ASC / revision DESC · exports markdown &amp; json</div></div>
    <div class="node alt"><span class="tag">DELETE idempotent</span>
      <div class="t">200 {{ deleted: true|false }}</div>
      <div class="d">re-supprimer une fiche déjà supprimée reste un succès</div></div>
  </div>
</div>
<div class="foot">purge automatique des enregistrements d'idempotence de plus de 7 jours au démarrage</div>
</body></html>"""

DOC3 = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>{BASE_CSS}</style></head><body>
<div class="head">
  <div class="kicker">Schéma 3 / 3 — Cycle de vie</div>
  <h1>Du standard non-KPS à la fiche KPS imprimable</h1>
  <div class="sub">Le parcours complet d'une fiche d'assemblage dans l'application</div>
</div>
<div class="phase">
  <h2>1 · Import du standard non-KPS</h2>
  <div class="row">
    <div class="node"><span class="tag">formats</span>
      <div class="t">texte · CSV · JSON</div>
      <div class="d">collage ou fichier — prévisualisation avant intégration</div></div>
    <div class="node alt"><span class="tag">parseur</span>
      <div class="t">warnings, jamais d'invention</div>
      <div class="d">champ absent → 0 + warning explicite, signalé « à compléter manuellement »</div></div>
  </div>
</div>
<div class="arrow">▼</div>
<div class="phase">
  <h2>2 · Conversion vers KPS Standardized Work</h2>
  <div class="row">
    <div class="node"><span class="tag">structure</span>
      <div class="t">en-tête · nomenclature · étapes</div>
      <div class="d">7 pièces + 5 étapes sur la fiche démo TA-S-3055-020 rév. D</div></div>
    <div class="node alt"><span class="tag">photos</span>
      <div class="t">association aux étapes</div>
      <div class="d">upload dédupliqué SHA-256 · vignettes par étape</div></div>
  </div>
</div>
<div class="arrow">▼</div>
<div class="phase">
  <h2>3 · Audit KPS temps réel C1-C10</h2>
  <div class="row">
    <div class="node"><span class="tag">10 critères, 10 points</span>
      <div class="t">miroir byte-identique</div>
      <div class="d">C1 en-tête · C2 double vérif · C3 Takt &gt; 0 · C4 SWIP · C5 anomalie · C6-C10 nomenclature &amp; étapes</div></div>
    <div class="node alt"><span class="tag">panneau vue 6</span>
      <div class="t">score en %</div>
      <div class="d">fiche démo = 100 % — même algorithme client et serveur (test miroir)</div></div>
  </div>
</div>
<div class="arrow">▼</div>
<div class="phase">
  <h2>4 · Équilibrage des temps</h2>
  <div class="row">
    <div class="node"><span class="tag">éditeur vue 3</span>
      <div class="t">CRUD temps par étape</div>
      <div class="d">somme 144 s vs Takt 150 s — jauge Cycle/Takt masquée si takt absent ou nul</div></div>
    <div class="node alt"><span class="tag">simulateur 70/20/10</span>
      <div class="t">répartition déterministe</div>
      <div class="d">manuel round(0,7·takt/M) · machine 0,2 · marche 0,1 — désactivé sans Takt</div></div>
  </div>
</div>
<div class="arrow">▼</div>
<div class="phase">
  <h2>5 · Diffusion atelier</h2>
  <div class="row">
    <div class="node"><span class="tag">exports</span>
      <div class="t">markdown · json</div>
      <div class="d">ré-import d'un JSON exporté → mise à jour par (docNumber, revision), sans duplication</div></div>
    <div class="node alt"><span class="tag">impression</span>
      <div class="t">A4 paysage</div>
      <div class="d">fiche complète prête à poster — cerclés ①..⑩ rendus à l'identique</div></div>
  </div>
</div>
<div class="foot">fiche démo pré-chargée : POST /api/demo/reset rejoue le seed TA-S-3055-020 à tout moment</div>
</body></html>"""

JOBS = [
    ("schema-1-architecture", DOC1),
    ("schema-2-flux-requete", DOC2),
    ("schema-3-cycle-fiche", DOC3),
]

async def main():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        page = await browser.new_page(viewport={"width": 1400, "height": 900},
                                      device_scale_factor=2)
        for name, html in JOBS:
            tmp = OUT / f"_{name}.html"
            tmp.write_text(html, encoding="utf-8")
            await page.goto(tmp.as_uri())
            await page.wait_for_load_state("networkidle")
            await page.evaluate("document.fonts.ready")
            await page.screenshot(path=str(OUT / f"{name}.png"), full_page=True)
            tmp.unlink()
            print("OK", name)
        await browser.close()

asyncio.run(main())
