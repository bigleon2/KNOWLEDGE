#!/usr/bin/env python3
"""⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.9)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.

Task 45 — Groupe C : génération des skills métier `iphone18` + `iphone17`
(précédent dessin-technique Task 8 dépôt — projection PM → SKILL.md).
- Source : PMs skills/@photos/ du dépôt @ 1020518 (lignage byte-identique R2 — jamais édités).
- Corps §PROMPT MAÎTRE→§13 repris VERBATIM du PM source (de la ligne « ## PROMPT MAÎTRE » à EOF).
- SKILL.md = frontmatter 6 champs + §0 Contexte Système N2 + note de lignage + corps PM.
- scripts/editer-image.mjs : contournement SDK base64 (CLI z-ai image-edit erreur 1210 — Task 42).
- evals/evals.json (schéma écosystème) + evals/trigger_evals.json.
- KB : 33 → 35 entrées + cross-ref bidirectionnelle skill-creator « Utilisé par ».
- KO-L004 : ECO_SKILLS de check-ecosysteme-integrity.py += 2 (compteurs dérivés dynamiquement
  par test-coherence-interactions.py — KO-L003).
Idempotent par reconstruction : re-exécution = mêmes contenus (assertions chirurgicales count==1).
"""
import json
import subprocess
import sys
from pathlib import Path

HOST = Path("/home/z/my-project")
REPO = HOST / "tmp" / "KNOWLEDGE-repo"
PHOTOS = REPO / "skills" / "@photos"
SKILLS = HOST / "skills"
KB = SKILLS / "KNOWLEDGE.md"
ARBITRE = HOST / "scripts" / "check-ecosysteme-integrity.py"

CTX_SYSTEME = """## §0 — Contexte Système (SHARED v1.7.7)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.
"""

FM_18 = """---
name: iphone18
version: 1.0.0
category: metier
language: fr
tags:
  - "#photo"
  - "#amelioration-photo"
  - "#iphone18-pro-max"
  - "#preset-iphone18-max"
  - "#r18-ouverture-variable"
  - "#mode-serie"
description: >
  Pipeline d'amélioration photo « iPhone 18 Pro Max, qualité max » (CPE — Computational
  Photo Engine) : analyse complète par grille ANALYSE-v2 (A1-A10, B1-B6 dont inventaire
  B6 verrouillé, C1-C3), moteur de décision R1-R18 (R18 : ouverture variable simulée
  ƒ/1.48-ƒ/4.0), plan d'actions YAML affiché AVANT toute exécution, pipeline P0-P8 dans
  l'ordre strict, contrôle qualité 12 critères avec itération contrôlée (max 2), presets
  de rendu §6 (défaut iphone18_max — ancrage A20 Pro / Dual Neural Engine 32 cœurs),
  rendus d'époque (années 70 → 2010), restauration de photos anciennes (scans, tirages),
  mode poster/print A4 300 DPI, mode série multi-sorties, rapport final en français +
  question utilisateur obligatoire. Garde-fous photo G1-G7 : fidélité stricte des
  visages (expressions, orientation des têtes), zéro élément ajouté, original
  non-destructif. Pensez à utiliser ce skill dès que l'utilisateur veut améliorer,
  retoucher ou restaurer une photo, demande le preset iphone18_max, une ouverture
  ƒ/…, un rendu d'époque ou un poster — même sans mentionner « iPhone ».
dependencies:
  - skill: skill-creator
    version: ">=1.0.0"
    used_at: "conventions structurelles (frontmatter, evals)"
  - skill: VLM
    version: ">=1.0.0"
    used_at: "analyse §1 (vision) + QC §5 comparatif original↔sortie"
  - skill: image-edit
    version: ">=1.0.0"
    used_at: "exécution §4 P1-P7 — contournement SDK base64 scripts/editer-image.mjs (CLI z-ai erreur 1210)"
read_when:
  - Déclencher quand la demande concerne : améliorer/retoucher/restaurer une photo, rendu « iPhone 18 Pro Max qualité max », preset iphone18_max, ouverture variable ƒ/1.48-ƒ/4.0, rendus d'époque, poster/print A4 300 DPI, mode série multi-photos
  - Déclencher si la demande mentionne : iphone18, photo qualité max, CPE, preset photo, ouverture ƒ, photo de concert/fête/famille à améliorer
  - Ne pas déclencher pour : périmètre iPhone 17 (→ skill iphone17), dessin technique coté (→ dessin-technique), génération d'image sans photo source (→ image-generation), vidéo (hors périmètre)
---
"""

FM_17 = """---
name: iphone17
version: 1.0.0
category: metier
language: fr
tags:
  - "#photo"
  - "#amelioration-photo"
  - "#iphone17-pro-max"
  - "#preset-iphone17-max"
  - "#r17-focales-equivalentes"
  - "#mode-serie"
description: >
  Pipeline d'amélioration photo « iPhone 17 Pro Max, qualité max » (CPE — Computational
  Photo Engine) — PÉRIMÈTRE D'ÉPOQUE (génération 17, supersédée par le skill iphone18
  depuis l'activation de la règle §6.10 du PM source : keynote Apple 9/9/2026 — le
  pipeline reste opérationnel pour un rendu génération 17 demandé explicitement).
  Analyse complète par grille ANALYSE-v2 (A1-A10, B1-B6 dont inventaire B6 verrouillé,
  C1-C3), moteur de décision R1-R17 (R17 : focales équivalentes 13-200 mm — sans R18 :
  l'ouverture est celle de l'appareil source), plan d'actions YAML affiché AVANT toute
  exécution, pipeline P0-P8 dans l'ordre strict, contrôle qualité 11 critères avec
  itération contrôlée (max 2), presets de rendu §6 (défaut iphone17_max — ancrage
  A19 Pro / Photonic Engine nouvelle génération), rendus d'époque (années 70 → 2010),
  restauration de photos anciennes, mode poster/print A4 300 DPI, mode série
  multi-sorties, rapport final en français + question utilisateur obligatoire.
  Garde-fous photo G1-G7 : fidélité stricte des visages, zéro élément ajouté, original
  non-destructif. Pensez à utiliser ce skill dès que l'utilisateur demande
  explicitement le rendu « iPhone 17 Pro Max » ou le preset iphone17_max.
dependencies:
  - skill: skill-creator
    version: ">=1.0.0"
    used_at: "conventions structurelles (frontmatter, evals)"
  - skill: VLM
    version: ">=1.0.0"
    used_at: "analyse §1 (vision) + QC §5 comparatif original↔sortie"
  - skill: image-edit
    version: ">=1.0.0"
    used_at: "exécution §4 P1-P7 — contournement SDK base64 scripts/editer-image.mjs (CLI z-ai erreur 1210)"
read_when:
  - Déclencher quand la demande concerne : rendu « iPhone 17 Pro Max qualité max » demandé explicitement, preset iphone17_max, focale équivalente 13-200 mm, rendu d'époque génération 17, restauration, poster/print, mode série
  - Déclencher si la demande mentionne : iphone17, preset iphone17_max, focale équivalente, CPE génération 17
  - Ne pas déclencher pour : périmètre iPhone 18 (→ skill iphone18 — génération courante), dessin technique coté (→ dessin-technique), génération d'image sans photo source (→ image-generation), vidéo (hors périmètre)
---
"""


def lignage(pm_file, version_pm, statut, extra=""):
    return f"""## Lignage — projection skill ← prompt maître source

> Skill métier projeté depuis le prompt maître `skills/@photos/{pm_file}` **{version_pm}** ({statut}) — fichier du dépôt, **byte-identique, jamais édité (R2)**. Le corps ci-dessous (« ## PROMPT MAÎTRE » → §13) est repris **VERBATIM** de cette source ; dans ce skill, « le document » y désigne le présent SKILL.md, et la discipline §11 (auto-audit) s'exécute à l'occasion d'un bump de version du skill (semver + recalibrage du registre KB). {extra}P8b (recadrage) : le PM source référence `crop_utils.py` (livrable historique du projet CLUB, non embarqué — un recadrage PIL équivalent est produit à la demande).

"""


def editer_image_mjs():
    return """// Contournement SDK base64 — le CLI `z-ai image-edit` ne transmet pas les images
// locales (erreur 1210, constat Task 42, session web-38713acd). Voie SDK directe.
// Usage : bun <ce-script>.mjs <prompt_file> <image_file> <output_file> [size] [retries]
import fs from 'fs';

const SDK = '/home/z/.bun/install/global/node_modules/z-ai-web-dev-sdk/dist/index.js';
const [,, promptFile, imageFile, outputFile, sizeArg, retriesArg] = process.argv;
if (!promptFile || !imageFile || !outputFile) {
  console.error('Usage: bun editer-image.mjs <prompt_file> <image_file> <output_file> [size] [retries]');
  process.exit(2);
}
const size = sizeArg || '1152x864';
const RETRIES = parseInt(retriesArg || '3', 10);
const prompt = fs.readFileSync(promptFile, 'utf-8').trim();
const b64 = fs.readFileSync(imageFile).toString('base64');
const mime = imageFile.toLowerCase().endsWith('.png') ? 'image/png' : 'image/jpeg';
const dataUrl = `data:${mime};base64,${b64}`;

const { default: ZAI } = await import(SDK);
const zai = await ZAI.create();

for (let attempt = 1; attempt <= RETRIES; attempt++) {
  try {
    const response = await zai.images.generations.edit({
      prompt,
      images: [{ url: dataUrl }],
      size,
    });
    if (!response?.data?.[0]?.base64) throw new Error('reponse invalide (pas de base64)');
    const out = Buffer.from(response.data[0].base64, 'base64');
    fs.writeFileSync(outputFile, out);
    console.log(`OK (tentative ${attempt}) -> ${outputFile} : ${out.length} octets (size=${size})`);
    process.exit(0);
  } catch (e) {
    console.error(`Tentative ${attempt} echouee: ${e.message}`);
    if (attempt < RETRIES) await new Promise(r => setTimeout(r, 2000 * attempt));
  }
}
process.exit(1);
"""


EVALS_18 = {
    "skill": "iphone18", "version": "1.0.0", "evals": [
        {"id": "E1-pipeline-complet", "description": "Photo réelle + demande d'amélioration → pipeline §1→§9 complet : analyse ANALYSE-v2 (scores + inventaire B6), moteur R1-R18, plan YAML affiché AVANT exécution (règle 3), sortie nommée PA-<CAS>-<seq>, rapport §8 + question §9", "commande": "« Améliore cette photo qualité max » + photo uploadée", "attendu": "sortie + rapport complet (analyse, diagnostic R, plan YAML, QC 12/12, limites honnêtes, question §9)", "priorite": "S1"},
        {"id": "E2-preset-defaut", "description": "Rendu par défaut iphone18_max (§6.1) déclenché par le moteur — jamais appliqué à l'aveugle (règle 2)", "commande": "analyse §1→§2 d'une photo standard", "attendu": "rendu_cible: iphone18_max dans le plan YAML + rendu conforme (netteté étendue R18)", "priorite": "S1"},
        {"id": "E3-r18-ouverture", "description": "Demande d'ouverture explicite → R18 : ouverture_cible au plan + avis honnête « simulation computationnelle, non optique » + critère QC 12", "commande": "« détache le sujet, ouverture ƒ/1.8 »", "attendu": "ouverture_cible dans le YAML + avis R18 au rapport §8", "priorite": "S2"},
        {"id": "E4-mode-serie", "description": "2+ photos → mode série §10 : sorties une par une, QC unitaire par sortie, rapport unifié, question unique finale", "commande": "« traite ces deux photos »", "attendu": "PA-<CAS>-1 / PA-<CAS>-2 + rapport unifié + UNE question", "priorite": "S2"},
        {"id": "E5-garde-fous-b6", "description": "Fidélité stricte : expressions/orientations des têtes + inventaire B6 + décor (critères QC 1-4) ; aucune retouche spontanée après réponse « non » à §9 (fin de traitement)", "commande": "QC comparatif original↔sortie puis réponse « non »", "attendu": "critères 1-4 PASS + fin de traitement sans itération", "priorite": "S1"},
        {"id": "E6-commandes-refus", "description": "Interface §13 : preset:iphone18 / preset:iphone18_max → preset défaut ; preset:iphone19 → REFUS (règle 14 — section SPÉCULATIF inactive)", "commande": "« preset:iphone19 »", "attendu": "refus explicite motivé (section inactive, jamais de valeur par défaut)", "priorite": "S2"},
    ],
}

EVALS_17 = {
    "skill": "iphone17", "version": "1.0.0", "evals": [
        {"id": "E1-pipeline-complet", "description": "Photo réelle + demande d'amélioration → pipeline §1→§9 complet : analyse ANALYSE-v2, moteur R1-R17, plan YAML affiché AVANT exécution (règle 3), sortie PA-<CAS>-<seq>, rapport §8 + question §9", "commande": "« Améliore cette photo qualité max » + photo uploadée", "attendu": "sortie + rapport complet (analyse, diagnostic R, plan YAML, QC 11/11, limites honnêtes, question §9)", "priorite": "S1"},
        {"id": "E2-preset-defaut", "description": "Rendu par défaut iphone17_max (§6.1) déclenché par le moteur — jamais appliqué à l'aveugle (règle 2)", "commande": "analyse §1→§2 d'une photo standard", "attendu": "rendu_cible: iphone17_max dans le plan YAML", "priorite": "S1"},
        {"id": "E3-r17-focale", "description": "Demande de focale équivalente → R17 : focale_cible au plan (gamme 13-200 mm) + critère QC 11", "commande": "« resserre le cadrage, focale équivalente 85 mm »", "attendu": "focale_cible dans le YAML + avis R17 au rapport §8", "priorite": "S2"},
        {"id": "E4-mode-serie", "description": "2+ photos → mode série §10 : sorties une par une, QC unitaire, rapport unifié, question unique finale", "commande": "« traite ces deux photos »", "attendu": "PA-<CAS>-1 / PA-<CAS>-2 + rapport unifié + UNE question", "priorite": "S2"},
        {"id": "E5-garde-fous-b6", "description": "Fidélité stricte : expressions/orientations + inventaire B6 + décor (critères QC 1-4) ; aucune retouche spontanée après réponse « non » à §9", "commande": "QC comparatif original↔sortie puis réponse « non »", "attendu": "critères 1-4 PASS + fin de traitement sans itération", "priorite": "S1"},
        {"id": "E6-commandes-refus", "description": "Interface §13 : preset:iphone17 / preset:iphone17_max → preset défaut ; preset:iphone18 → REFUS (règle 14 — section inactive dans le PM v2.0)", "commande": "« preset:iphone18 »", "attendu": "refus explicite motivé (section inactive — migration générationnelle via skill iphone18)", "priorite": "S2"},
    ],
}

TRIGGERS_18 = [
    {"query": "Améliore cette photo avec le rendu iPhone 18 Pro Max qualité max.", "should_trigger": True},
    {"query": "Applique le preset iphone18_max sur cette photo de mariage.", "should_trigger": True},
    {"query": "Peux-tu détacher le sujet avec une ouverture ƒ/1.8 sur cette photo de concert ?", "should_trigger": True},
    {"query": "Retouche ces deux photos de fête en mode série, qualité iPhone 18 max.", "should_trigger": True},
    {"query": "Restaure ce scan de photo ancienne des années 80, rendu propre et net.", "should_trigger": True},
    {"query": "Prépare cette photo en poster A4 à 300 DPI pour impression.", "should_trigger": True},
    {"query": "Fais le rendu iPhone 17 Pro Max de cette photo.", "should_trigger": False},
    {"query": "Reproduis cette pièce photographiée en dessin technique coté (isométrie CAO).", "should_trigger": False},
]

TRIGGERS_17 = [
    {"query": "Améliore cette photo avec le rendu iPhone 17 Pro Max qualité max.", "should_trigger": True},
    {"query": "Applique le preset iphone17_max sur cette photo.", "should_trigger": True},
    {"query": "Fais un portrait serré avec la focale équivalente 85 mm sur cette photo.", "should_trigger": True},
    {"query": "Retouche ces deux vieilles photos en mode série, rendu iPhone 17.", "should_trigger": True},
    {"query": "Restaure ce tirage argentique abîmé des années 70.", "should_trigger": True},
    {"query": "Prépare un poster A4 300 DPI de cette photo de famille.", "should_trigger": True},
    {"query": "Améliore cette photo au rendu iPhone 18 Pro Max qualité max.", "should_trigger": False},
    {"query": "Reproduis cette pièce photographiée en dessin technique coté (isométrie CAO).", "should_trigger": False},
]

KB_18 = """## iphone18 v1.0.0

- **Category** : métier
- **Description** : Pipeline d'amélioration photo « iPhone 18 Pro Max, qualité max » (CPE — Computational Photo Engine) : grille ANALYSE-v2 (A1-A10, B1-B6 dont inventaire B6 verrouillé, C1-C3), moteur de décision R1-R18 (R18 = ouverture variable simulée ƒ/1.48-ƒ/4.0 — rendu computationnel non optique), plan d'actions YAML affiché AVANT exécution (règle 3), pipeline P0-P8 ordre strict, QC 12 critères avec itération contrôlée max 2, presets §6 (défaut iphone18_max — ancrage A20 Pro / Dual Neural Engine 32 cœurs, calibrage DXOMARK 172/nuit 150 avec limites honnêtes), rendus d'époque (années 70 → 2010), restauration de photos anciennes, poster/print A4 300 DPI, mode série §10 (sorties une par une, QC unitaire, rapport unifié, question unique), interface de commandes §13 (preset:<nom> ; preset:iphone19 refusé — règle 14 SPÉCULATIF), rapport français §8 + question §9 obligatoire (aucune retouche spontanée). Garde-fous G1-G7 + inventaire B6 : fidélité stricte des visages, zéro élément ajouté. Lignage : projection VERBATIM du PM skills/@photos/iphone18-photos.md v1.0 (byte-identité R2 — jamais édité) ; test empirique PA-TEST-001 (Task 42, session web-38713acd) QC 12/12 PASS + validation propriétaire §9 sans réserve.
- **Dépend de** : skill-creator >= v1.0.0 (conventions structurelles), VLM >= v1.0.0 (analyse §1 + QC §5 — skill plateforme), image-edit >= v1.0.0 (exécution P1-P7 — skill plateforme, contournement SDK base64 scripts/editer-image.mjs)
- **Utilisé par** : Main (missions d'amélioration photo — périmètre iPhone 18, génération courante)
- **Dernière calibration** : création v1.0.0 (Task 45 Groupe C, session web-38713acd — mission gen-plan(step), génération depuis PM @photos v1.0 ; tests robustes 2 photos Groupes E/F de la mission — résultats consignés worklog + rapport mission)
- **Statut** : stable

"""

KB_17 = """## iphone17 v1.0.0

- **Category** : métier
- **Description** : Pipeline d'amélioration photo « iPhone 17 Pro Max, qualité max » (CPE) — PÉRIMÈTRE D'ÉPOQUE honnête : génération 17, supersédée par le skill iphone18 depuis l'activation de la règle §6.10 du PM source v2.0 (génération iPhone 18 confirmée par Apple le 9/9/2026) ; le pipeline reste opérationnel pour un rendu génération 17 demandé explicitement. Grille ANALYSE-v2, moteur R1-R17 (R17 = focales équivalentes 13-200 mm ; sans R18 — l'ouverture est celle de l'appareil source), plan YAML AVANT exécution, pipeline P0-P8, QC 11 critères, presets §6 (défaut iphone17_max — ancrage A19 Pro / Photonic Engine NG), rendus d'époque, restauration, poster/print A4 300 DPI, mode série §10, commandes §13 (preset:iphone18 refusé — règle 14), rapport §8 + question §9. Garde-fous G1-G7 + inventaire B6. Lignage : projection VERBATIM du PM skills/@photos/iphone17-photos.md v2.0 ARCHIVÉ (byte-identité R2 — jamais édité).
- **Dépend de** : skill-creator >= v1.0.0 (conventions structurelles), VLM >= v1.0.0 (analyse §1 + QC §5 — skill plateforme), image-edit >= v1.0.0 (exécution P1-P7 — skill plateforme, contournement SDK base64 scripts/editer-image.mjs)
- **Utilisé par** : Main (missions d'amélioration photo — périmètre iPhone 17 sur demande explicite / rendu d'époque)
- **Dernière calibration** : création v1.0.0 (Task 45 Groupe C, session web-38713acd — mission gen-plan(step), génération depuis PM @photos v2.0 archivé ; tests robustes 2 photos Groupe F de la mission — résultats consignés worklog + rapport mission)
- **Statut** : stable

"""


def corps_pm(pm_path):
    """Extrait le corps du PM de la ligne '## PROMPT MAÎTRE' à EOF (H1 du PM écarté)."""
    lines = pm_path.read_text(encoding="utf-8").splitlines()
    for i, ln in enumerate(lines):
        if ln.startswith("## PROMPT MAÎTRE"):
            return "\n".join(lines[i:]) + "\n"
    raise SystemExit(f"FAIL : en-tête PROMPT MAÎTRE introuvable dans {pm_path}")


def ecrire_skill(nom, fm, pm_file, version_pm, statut, evals, triggers, extra=""):
    d = SKILLS / nom
    (d / "scripts").mkdir(parents=True, exist_ok=True)
    (d / "evals").mkdir(parents=True, exist_ok=True)
    pm_body = corps_pm(PHOTOS / pm_file)
    skill_md = fm + "\n" + CTX_SYSTEME + "\n" + lignage(pm_file, version_pm, statut, extra) + pm_body
    (d / "SKILL.md").write_text(skill_md, encoding="utf-8")
    (d / "scripts" / "editer-image.mjs").write_text(editer_image_mjs(), encoding="utf-8")
    (d / "evals" / "evals.json").write_text(json.dumps(evals, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (d / "evals" / "trigger_evals.json").write_text(json.dumps(triggers, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return len(skill_md.splitlines())


def maj_kb():
    text = KB.read_text(encoding="utf-8")
    if "## iphone18 v1.0.0" in text and "## iphone17 v1.0.0" in text:
        print("KB : entrées iphone18/iphone17 déjà présentes (rejeu — no-op)")
        return
    anchor = "## Décisions d'architecture (corrige-ecosysteme v2.0.0)"
    assert text.count(anchor) == 1, "ancre KB (Décisions d'architecture) introuvable ou non unique"
    for e in (KB_18, KB_17):
        assert e.splitlines()[0] not in text, f"entrée KB déjà présente : {e.splitlines()[0]}"
    text = text.replace(anchor, KB_18 + KB_17 + anchor)
    # Cross-ref bidirectionnelle : skill-creator « Utilisé par » += iphone18/iphone17
    uc = "- **Utilisé par** : clone-chat (conventions), prompt-engineering (création), script-mon-ecosysteme-infrastructure v1.1.0 (conventions + évals — INFRA-1/2/3), knowledge-observer (application des mises à jour), script-creator v1.0.0 (conventions), script-reviewer v1.0.0 (conventions), correct-py v1.0.0 (conventions de description, d'évals et de frontmatter, §1.4), dessin-technique v1.1.1 (conventions structurelles — dependencies frontmatter)"
    assert text.count(uc) == 1, "ligne « Utilisé par » de skill-creator introuvable ou non unique"
    text = text.replace(uc, uc + ", iphone18 v1.0.0 (conventions structurelles — projection PM → SKILL.md), iphone17 v1.0.0 (idem)")
    KB.write_text(text, encoding="utf-8")


def maj_arbitre():
    text = ARBITRE.read_text(encoding="utf-8")
    if '"iphone18"' in text and '"iphone17"' in text:
        print("KO-L004 : ECO_SKILLS déjà recalibré (rejeu — no-op)")
        return
    anchor = '    "dessin-technique": "1.1.1",'
    assert text.count(anchor) == 1, "ancre ECO_SKILLS (dessin-technique) introuvable ou non unique"
    assert '"iphone18"' not in text and '"iphone17"' not in text, "ECO_SKILLS déjà recalibré"
    ajout = (anchor + '\n    "iphone18": "1.0.0",  # Task 45 (session web-38713acd) : projection PM @photos/iphone18-photos.md v1.0 (R18 ouverture variable, preset iphone18_max, PA-TEST-001 QC 12/12)\n'
             '    "iphone17": "1.0.0",  # Task 45 (session web-38713acd) : projection PM @photos/iphone17-photos.md v2.0 archivé (R1-R17 d\'époque, preset iphone17_max)')
    text = text.replace(anchor, ajout)
    ARBITRE.write_text(text, encoding="utf-8")


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=HOST)
    tail = [l for l in (r.stdout + r.stderr).splitlines() if "RESUME" in l or "FAIL" in l or "RAPPORT" in l or "PASS :" in l or "Vérifications" in l]
    return r.returncode, "\n".join(tail[-8:])


def main():
    sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=REPO, capture_output=True, text=True).stdout.strip()
    print(f"dépôt source : {sha}")
    n18 = ecrire_skill("iphone18", FM_18, "iphone18-photos.md", "v1.0", "COURANT — génération iPhone 18", EVALS_18, TRIGGERS_18,
                       extra="Test empirique de référence : PA-TEST-001 (Task 42, QC 12/12 PASS, validation propriétaire §9 sans réserve). ")
    n17 = ecrire_skill("iphone17", FM_17, "iphone17-photos.md", "v2.0", "ARCHIVÉ — génération 17, supersédé par iphone18 (règle §6.10 activée)", EVALS_17, TRIGGERS_17)
    maj_kb()
    maj_arbitre()
    # Rescellement archive v2.3 (idempotent) — KB et arbitre sont des PILIERS :
    # toute modification de pilier => re-scellement canonique avant arbitres.
    r = subprocess.run(["python3", "scripts/task-f5-seal-archive-v23.py"],
                       capture_output=True, text=True, cwd=HOST)
    print("rescellement archive :", (r.stdout.strip().splitlines() or ["?"])[-2:])
    print(f"skills/iphone18/SKILL.md : {n18} lignes")
    print(f"skills/iphone17/SKILL.md : {n17} lignes")
    print("KB : 33 → 35 entrées ; skill-creator « Utilisé par » += iphone18, iphone17")
    print("KO-L004 : ECO_SKILLS += iphone18, iphone17")
    for label, cmd in [
        ("check-ecosysteme-integrity.py", ["python3", "scripts/check-ecosysteme-integrity.py"]),
        ("test-coherence-interactions.py", ["python3", "scripts/test-coherence-interactions.py"]),
        ("verify-cross.py", ["python3", "scripts/verify-cross.py"]),
    ]:
        rc, out = run(cmd)
        print(f"\n=== {label} (rc={rc}) ===\n{out}")
        if rc != 0:
            print("FAIL — voir sortie complète")
            return 1
    print("\nGROUPE C : génération + KB + KO-L004 + arbitres — TERMINÉ")
    return 0


if __name__ == "__main__":
    sys.exit(main())
