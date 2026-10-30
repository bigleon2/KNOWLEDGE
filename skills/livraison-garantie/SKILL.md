---
name: livraison-garantie
version: 1.0.0
category: ecosystem
language: fr
tags:
  - livraison
  - livrables
  - vérification
  - boucle-fermée
  - portail
description: >
  Skill d'orchestration de LIVRAISON GARANTIE en boucle fermée (Task 8, directive
  propriétaire 2026-10-31 « crée $facon ces trois skills » — suggestion D018-2, douleur
  prouvée de la session du 2026-10-25 : séquence de livraison = 4 tours entièrement
  manuels, mauvais fichier détecté par chance via des logs stderr perdus). Un seul
  appel : identifier le livrable cible (famille multi-versions signalée — hygiène
  vue-upload v1.5.0), l'ÉPINGLER (featured) AVANT la fenêtre d'accès, démarrer le
  portail (primitives vue-upload réutilisées — zéro duplication R4), SURVEILLER le
  journal des téléchargements (.journal-vue-upload.jsonl) pendant la fenêtre --hold
  et rendre un VERDICT MÉCANIQUE avec critère d'arrêt explicite : CONFIRME (la cible
  a été téléchargée — arrêt anticipé, la fenêtre se referme tôt), PARTIEL (un MAUVAIS
  fichier au nom proche a été pris — listé, guidance de re-ciblage), AUCUN (rien
  téléchargé — guidance preview/share). Dépendance : vue-upload >= 1.5.0 (garde de
  version vérifiée à l'exécution).
dependencies:
  - skill: vue-upload
    version: ">=1.5.0"
    used_at: "Orchestration (import des primitives : start_inprocess, lit_journal, lit_featured, detect_versions, sanitize_name — garde de version >= 1.5.0 vérifiée au chargement)"
  - skill: gen-plan
    version: ">=3.20.0"
    used_at: "Étape 0 (garde É1-INSTALL avant toute action)"
read_when:
  - Déclencher quand la demande concerne : livrer UN livrable précis avec GARANTIE que le propriétaire télécharge le BON fichier
  - Déclencher si la demande mentionne : livraison garantie, livraison-garantie, delivery-warden, boucle fermée, vérifier que le bon fichier a été téléchargé, mauvais fichier, mauvais fichier téléchargé
  - Déclencher aussi si la demande mentionne : épingle et surveille, fenêtre de livraison, confirme le téléchargement, livrer le GIF / le rapport / le document final au propriétaire
  - Ne pas déclencher pour un simple accès aux dossiers (portail seul → vue-upload) ni pour l'hygiène seule (versions → vue-upload).
---

## §0 — Contexte Système (SHARED v1.7.14)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.

## §A — DÉCLENCHEURS

- `livraison-garantie` ou `delivery-warden`
- « livre-moi ce fichier en garantie / avec confirmation »
- « vérifie que j'ai téléchargé le bon fichier »
- « j'ai téléchargé le mauvais fichier » (diagnostic + re-ciblage)
- « épingle et surveille la livraison »
- « ferme la boucle sur la livraison du GIF / du rapport / du livrable »

## §1 — SPÉCIFICATION FONCTIONNELLE

### §1.1 Description

livraison-garantie matérialise la boucle fermée de livraison que la session du
2026-10-25 a révélée manquante : le portail vue-upload montrait les fichiers et
journalisait les téléchargements, mais l'AGENT devait orchestrer à la main
(épingler, ouvrir la fenêtre, relire le journal, réagir) — 4 tours, erreur détectée
par chance. Ce skill transforme cette séquence en UN appel mécanique : épinglage
AVANT la fenêtre, surveillance du journal PENDANT, verdict APRÈS (ou arrêt anticipé
dès que la cible est téléchargée). Le mauvais fichier au nom proche — la douleur
exacte du 2026-10-25 (2 mauvais fichiers pris sur 3) — est détecté par le journal
et nommé dans le verdict.

### §1.2 Comportement de l'agent

1. **Garde préalable** : `python3 skills/gen-plan/scripts/ensure-installed.py --preempt`
   (É1-INSTALL) — SANS correct-work automatique (KB Task 36).
2. **Orchestrateur (UN appel, boucle fermée)** :
   `python3 {{SKILLS_ROOT}}livraison-garantie/scripts/livraison_garantie.py \
      --fichier <nom-exact> [--dir auto|download|upload] [--port 3000] [--hold 540] \
      [--poll 0.5] [--root /home/z/my-project] [--json]`
   - **garde de dépendance** : la primitive vue-upload est chargée par chemin et sa
     VERSION vérifiée >= 1.5.0 (rc 7 si inférieure — jamais de livraison sur une
     base non journalisée) ;
   - **identification** : la cible est cherchée (nom assaini, exact) dans download/
     puis upload/ (rc 6 si absente — guidance : `push` d'abord) ; une famille
     multi-versions ou un suspect au nom proche impliquant la cible est SIGNALÉ
     (`avertissement_famille`) avec la recommandation d'hygiène (push de la finale +
     archivage automatique, puis re-ciblage) ;
   - **épinglage AVANT la fenêtre** : marker `featured` posé sur la cible (même format
     que vue-upload — lu par le serveur : bannière ★ en tête du portail) ;
   - **démarrage du portail** : `start_inprocess` de vue-upload (thread daemon,
     zéro subprocess, zéro setsid) ; rc 2 si bind impossible ;
   - **surveillance** : lecture du journal par POSITION (lignes pré-fenêtre écartées —
     seuls les téléchargements survenus PENDANT la fenêtre comptent), poll `--poll` s ;
   - **arrêt mécanique** : ① la cible apparaît au journal → verdict CONFIRME immédiat
     (arrêt anticipé, fenêtre close tôt) ; ② la fenêtre expire → verdict selon le
     journal : PARTIEL si des téléchargements hors-cible sont survenus (mauvais
     fichiers nommés, `nom_proche` marqué si radical/1er-token commun avec la cible),
     AUCUN sinon ;
   - **verdicts et codes retour** : 0 CONFIRME · 1 PARTIEL · 2 bind impossible ·
     6 cible absente/nom invalide · 7 AUCUN · 7 aussi si dépendance < 1.5.0 ;
   - `--json` : sortie machine-readable (evals LG-1..3, intégrations mécaniques).
3. **Guidance mécanique (dans la sortie)** :
   - CONFIRME → consigner (worklog) ; retirer l'épingle si la livraison est terminée
     (`featured --off`) ;
   - PARTIEL → l'épinglé reste posé : réouvrir une fenêtre (`vue_upload_panel.py
     --hold 540`) en annonçant À NOUVEAU le nom EXACT + la taille ; si le mauvais
     fichier est une version supersédée, appliquer l'hygiène (`push` de la finale →
     archivage automatique v1.5.0) avant de réouvrir ; repli : `share <fichier>` ;
   - AUCUN → vérifier que le preview a été cliqué pendant la fenêtre (edge :81 vivant ?),
     réouvrir, ou basculer sur `share` (liens externes vérifiés sha256).
4. **Communication** : annoncer le verdict + le critère d'arrêt + le nom exact de la
   cible ; en PARTIEL, nommer explicitement le fichier erroné pris au journal.
5. **Journalisation** : entrée worklog (Task ID, cible, verdict, téléchargements
   constatés, durée de fenêtre effective).

### §1.3 Sources de vérité (lecture seule)

| Source | Rôle |
|--------|------|
| `.featured-vue-upload.json` | marker d'épinglage (écrit AVANT la fenêtre — même format que vue-upload) |
| `.journal-vue-upload.jsonl` | journal des téléchargements (append par le serveur vue-upload sur chaque /get/) |
| `download/archive/`, `upload/archive/` | hygiène v1.5.0 (signalée via `detect_versions`, jamais modifiée ici) |

### §1.4 Sécurité et honnêteté (R3)

- Le skill NE modifie AUCUN livrable : il lit, épingle (marker), démarre le portail
  et lit le journal — l'archivage/restauration reste du ressort de vue-upload.
- AUCUNE déduction subjective : le verdict repose UNIQUEMENT sur les entrées du
  journal survenues pendant la fenêtre (position de départ consignée).
- Un téléchargement partiel (connexion interrompue) reste journalisé côté serveur
  (append post-envoi) — le verdict CONFIRME signifie « le fichier a été servi
  intégralement par le portail », pas « le fichier est intact chez le propriétaire »
  (limite documentée §3).

## §2 — SPÉCIFICATION TECHNIQUE

### §2.1 Stack

- Python ≥ 3.10, bibliothèque standard uniquement.
- Réutilisation R4 : import par chemin des primitives `vue_upload_panel.py`
  (start_inprocess, lit_journal, lit_featured, detect_versions, sanitize_name,
  port_alive, edge_alive, human, MARKER, JOURNAL) — ZÉRO duplication.
- Aucune dépendance externe ; le portail et le journal restent détenus par vue-upload.

### §2.2 Structure

```
{{SKILLS_ROOT}}livraison-garantie/
├── SKILL.md
├── scripts/
│   └── livraison_garantie.py   # orchestrateur boucle fermée (v1.0.0)
└── evals/
    ├── evals.json
    └── trigger_evals.json
```

Fichiers d'état (racine du projet, hors dépôt — détenus par vue-upload) :
`.featured-vue-upload.json` et `.journal-vue-upload.jsonl`.

### §2.3 Provenance et journal

- Provenance : CRÉÉ-VIA-PROTOCOLE (skill-creator, Task 8, session web-eb6c8580,
  directive propriétaire 2026-10-31 « crée $facon ces trois skills » — suggestion
  D018-2 du worklog Task 7, douleur prouvée de la session du 2026-10-25 :
  4 tours de livraison manuels, mauvais fichier détecté par chance).
- Test mécanique : `scripts/task8/test-livraison-garantie.py` (portail réel
  in-process, /get simulés : CONFIRME avec arrêt anticipé, PARTIEL avec mauvais
  fichier au nom proche, AUCUN, rc 6, épinglage préalable vérifié).
- Intégration KB : entrée registre (Task 8) — voir {{KB_PATH}} ; réciproque :
  « Utilisé par » vue-upload (dépendance déclarée >= 1.5.0).

## §3 — LIMITES CONNUES (honnêteté R3)

- La fenêtre d'accès hérite de la contrainte sandbox de vue-upload (processus
  éphémère — `--hold` ≤ 540 s ≤ 600 s plateforme) ; en cas de preview indisponible,
  la guidance AUCUN bascule sur `share` (liens externes vérifiés).
- CONFIRME prouve un téléchargement SERVI, pas l'intégrité chez le propriétaire
  (une vérification sha256 côté propriétaire n'est pas mécaniquement accessible ;
  le repli `share` de vue-upload vérifie l'intégrité du lien, pas du poste client).
- La détection « mauvais fichier » couvre les téléchargements SURVENUS PENDANT la
  fenêtre (journal) — un mauvais fichier pris dans une fenêtre antérieure n'est
  visible que dans l'historique du journal (l'orchestrateur écarte le pré-fenêtre
  pour ne jamais accuser à tort).
- Le routage preview edge :81 est un mécanisme plateforme (KB Task 34) : son absence
  dégrade la fenêtre en accès local uniquement (verdict AUCUN probable) — guidance
  share émise.
