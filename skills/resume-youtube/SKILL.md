---
name: resume-youtube
version: "1.1.0"
category: metier
language: fr
tags:
  - youtube
  - resume
  - video
  - playlist
  - sous-titres
  - transcript
description: Skill autonome de résumé de vidéos YouTube — déclencher dès que la tâche demande de résumer, analyser ou extraire le contenu d'une vidéo ou d'une playlist YouTube (URL youtube.com/watch, youtu.be, playlist?list=, ou mention explicite « vidéo YouTube » / « playlist »), que ce soit pour un résumé par vidéo, une synthèse thématique d'ensemble, l'extraction de sous-titres/transcripts, ou l'analyse de points clés applicables à un projet. Pipeline multi-moteurs avec dégradation honnête : transcripts (yt-dlp / youtube-transcript-api / Invidious / agent-browser) puis métadonnées, jamais de contenu fabriqué (R3). Intègre une FONCTION DE VÉRIFICATION ANTI-HALLUCINATION en 5 gardes (G1 ancrage, G2 votes LLM réels par affirmation, G3 ancrage horodaté, G4 citations verbatim, G5 enveloppe honnête) — exigence propriétaire 2026-10-04. Répond aussi aux demandes de rapport structuré sur une playlist et d'identification des sujets traités.
read_when:
  - Déclencher quand la demande concerne : skill autonome de résumé de vidéos YouTube — déclencher dès que la tâche demande de résumer, analyser ou extra…
  - Déclencher si la demande mentionne : youtube, playlist, vidéo
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

## §0 — Contexte Système (SHARED v1.6.8)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# resume-youtube — Résumés de vidéos et playlists YouTube

> **Provenance** : créé Task 26 (2026-10-04) via gen-plan v3.19.0 — plan
> `download/plan-task26-resume-youtube.md` (D001-D007). Architecture inspirée du skill
> `agent-browser` (KNOWLEDGE@2165a28, moteur principal d'empreinte navigateur) et des
> patterns du dépôt manus-agent (orchestration multi-agents, exposé MCP — inspiration
> seulement, aucune dépendance).

## §1 — Objectif

Produire, pour une vidéo ou une playlist YouTube :
1. La liste des vidéos (titre, chaîne, durée, lien) — extraction depuis la page playlist.
2. Les sous-titres/transcripts quand ils sont accessibles (multi-moteurs).
3. Un résumé structuré par vidéo (sujet, points clés, outils/concepts, leçons) + une
   synthèse thématique d'ensemble + un rapport Markdown.

**Règle d'honnêteté (R3, absolue)** : chaque résumé porte son `niveau_preuve` —
`transcript` (sous-titres réels), `description` (métadonnées enrichies) ou `metadata`
(titre/chaîne/durée seuls). AUCUN contenu n'est jamais fabriqué : si aucune source
n'est accessible, le statut est « indisponible » et le résumé est libellé comme
inférence de titre uniquement.

## §2 — Architecture multi-moteurs (ordre strict par vidéo)

| # | Moteur | Condition | Apport |
|---|--------|-----------|--------|
| 1 | yt-dlp | binaire présent (PATH ou `.venv-yt/bin/yt-dlp`) | sous-titres auto/manuels fr/en |
| 2 | youtube-transcript-api | lib importable | transcripts via watch page |
| 3 | Invidious (rotation) | instances joignables | VTT via `/api/v1/captions/VID` |
| 4 | agent-browser | CLI présent | empreinte navigateur réelle (open + eval get_transcript) |
| 5 | page_reader Z.ai | CLI z-ai | description/métadonnées côté serveur |
| 6 | métadonnées playlist | toujours | titres/durées/chaînes (page playlist se charge même sur IP flaggée) |

Chaque vidéo consigne `engine_used` et `status`. Un moteur qui échoue est essayé en
suivant ; l'échec TOTAL n'empêche jamais la livraison du rapport (dégradation gracieuse).

> **Limites connues (2026-10)** : YouTube bot-bloque durement les IP datacenter
> (innertube LOGIN_REQUIRED, get_transcript 400, instances Invidious/Piped touchées,
> Tactiq 401, kome.ai 522). Sur une telle IP, le moteur 6 est la voie finale attendue.

## §3 — Usage

```bash
# Playlist complète (recommandé)
python3 skills/resume-youtube/scripts/resume_youtube.py \
  --url "https://youtube.com/playlist?list=PLeMSII5vMQlA" \
  --out <rep_sortie> [--n-max 10] [--no-summaries]

# Étapes individuelles
python3 skills/resume-youtube/scripts/fetch_playlist.py    --url <url> --out videos.json
python3 skills/resume-youtube/scripts/fetch_transcripts.py --videos videos.json --out transcripts/
python3 skills/resume-youtube/scripts/summarize.py         --videos videos.json --transcripts transcripts/ --out resumes.json
```

Sorties dans `--out` : `videos.json`, `transcripts/<videoId>.json`, `resumes.json`,
`rapport.md`. Toutes les étapes sont **idempotentes** (skip-done — KO-L001) : relancer
l'orchestrateur ne refait que ce qui manque.

## §3.5 — Fonction de vérification anti-hallucination (exigence 2026-10-04)

Chaque résumé passe par `verify_summary.py` — 5 gardes successives :

| Garde | Contrôle | Effet |
|-------|----------|-------|
| **G1 ancrage** | Pas de transcript réel -> AUCUN vote tenté, statut `NON-VÉRIFIÉ` immédiat. Le mode « métadonnées seul » est une inférence de titre clairement étiquetée, jamais présentée comme issue de la vidéo. | empêche la fabrication |
| **G2 claims↔preuves** | Extraction des affirmations (points clés + phrases assertives) puis vote LLM RÉEL par affirmation contre le transcript : `SUPPORTÉE` / `RÉFUTÉE` / `INVÉRIFIABLE` + citation de preuve. Protocole R3 : jamais simulé — si le CLI LLM échoue, `NON_EXECUTÉ` est consigné. | détecte l'invention |
| **G3 ancrage horodaté** | Chaque point clé est ancré au segment de transcript au meilleur recouvrement de Jaccard -> horodatage `mm:ss` réel ou null (seuil 0.12). | traçabilité |
| **G4 citations verbatim** | Toute citation réputée verbatim (« … ») doit matcher par sous-chaîne normalisée le transcript, sinon `NON-TROUVÉE`. | interdit les fausses citations |
| **G5 enveloppe honnête** | Statut `VÉRIFIÉ` (support >= seuil 0.8) / `PARTIEL` (>= seuil-0.2) / `NON-VÉRIFIÉ` ; toute affirmation RÉFUTÉE => `revision_requise` et repasse de synthèse ciblée (`--force-video`). | boucle de révision |

```bash
# autonome
python3 skills/resume-youtube/scripts/verify_summary.py \
  --videos videos.json --transcripts transcripts/ --resumes resumes.json \
  --out verification.json [--seuil 0.8] [--no-llm] [--force]
```

Sortie `verification.json` : `{videos:[{videoId, statut, support_rate, claims:[{claim, verdict, preuve}], ancrage:[{point, horodatage}], citations:[{citation, trouvee}], gardes:{G1..G5}, revision_requise}], synthese}`. L'orchestrateur l'exécute automatiquement (étape 3.5) et le rapport intègre le statut par vidéo + la table G1-G5.

## §4 — Formats

- `videos.json` : `{playlist_id, title, n_videos, videos:[{index, videoId, title, duration, author, url}]}`
- `transcripts/<videoId>.json` : `{videoId, lang, engine_used, status, n_chars, transcript}`
- `resumes.json` : `[{videoId, title, author, niveau_preuve, resume, points_cles[], outils[], lecons_planification[], pour_ecosysteme}]`
- `verification.json` : enveloppe anti-hallucination G1-G5 par vidéo (statut, support_rate, claims, ancrage, citations).
- `rapport.md` : synthèse exécutive + sections par vidéo (statut anti-hallucination inclus) + synthèse thématique + tables de provenance et G1-G5.

## §5 — Intégration écosystème

- **Déclencheur** : URL YouTube ou mention « vidéo/playlist YouTube » + verbe
  résumer/analyser/extraire. Les evals (`evals/trigger_evals.json`, 8 cas) sont
  calibrés pour le baseline runner (voie M + voie L, seuil 0.5).
- **Dépend de** : python3, curl ; optionnel : yt-dlp, youtube-transcript-api,
  agent-browser, z-ai CLI (résumés LLM).
- **Utilisé par** : gen-plan (phases d'analyse documentaire), l'agent principal
  (demandes de résumés vidéo), futurs flux MCP multi-IA (chapitre CLAUDE du rapport
  Task 26-d — partage de tâches inter-IA).

## §6 — Statut

- **Statut** : stable — v1.1.0 (fonction anti-hallucination G1-G5 intégrée et branchée).
- **Calibration** : 2026-10-04 (v1.0.0 initiale ; v1.1.0 anti-hallucination — exigence propriétaire,
  testée en conditions réelles : 0 transcript accessible sur IP datacenter => 36/36 statuts
  `NON-VÉRIFIÉ` honnêtes G1, zéro faux « VÉRIFIÉ », zéro vote simulé).
- **Changelog v1.1.0** : scripts/verify_summary.py (G1-G5) ; orchestrateur étape 3.5 avec
  repasses ciblées (`--max-repasses`, `--force-video`) ; rapport enrichi (statut + ancrage G3).
