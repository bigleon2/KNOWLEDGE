---
name: vue-upload
version: 1.2.0
category: ecosystem
language: fr
tags:
  - livrables
  - fichier
  - accès
  - portail
  - upload
description: >
  Skill de portail d'accès aux livrables (Task 31, directive propriétaire 2026-10-05).
  Sert une interface web (palette DM-1, français) listant download/ (livrables) et
  upload/ (fichiers reçus), avec téléchargement en un clic et téléversement
  (glisser-déposer) vers download/ ou upload/. Serveur HTTP bibliothèque standard
  uniquement (zéro dépendance), dual-stack IPv4/IPv6, anti-traversée realpath,
  taille max 200 Mo. Répond à la douleur : « les chemins de fichiers s'affichent
  en texte brut dans le chat, le propriétaire ne peut pas accéder au dossier ».
  v1.1.0 (Task 36) : panel RAPIDE vue_upload_panel.py — voie chaude < 1 s (portail
  déjà vivant, zéro démarrage), voie froide in-process < 2 s (thread daemon, zéro
  subprocess/setsid), --hold N pour la session d'accès deux temps, --json machine-readable.
  v1.2.0 (Task 39, approfondissement — directive propriétaire) : ce qui était MANUEL devient
  une commande — share <fichier> (repli externe AUTOMATISÉ filebin.net ≈ 6 j + tmpfiles.org
  ≈ 60 min, VÉRIFICATION sha256 par re-téléchargement : un lien n'est annoncé VÉRIFIÉ
  qu'après preuve d'intégrité), push <source> (inscription dans download/ ou upload/ avec
  les règles serveur : assainissement, cachés refusés, 200 Mo max, no-op honnête, --force),
  doctor (diagnostic < 1 s + voie recommandée — répond à « pourquoi ça ne fonctionne pas
  à tous les coups »). Rétrocompatible : sans sous-commande = panel v1.1.0 inchangé
  (listing enrichi : tri --sort, filtre --filter, dates).
dependencies:
  - skill: gen-plan
    version: ">=3.20.0"
    used_at: "Étape 0 (garde É1-INSTALL avant démarrage du portail)"
read_when:
  - Déclencher quand la demande concerne : donner accès au propriétaire aux fichiers générés (download/, upload/)
  - Déclencher si la demande mentionne : vue-upload, portail, accès fichiers, télécharger livrable, téléverser
  - Déclencher aussi si la demande mentionne : share, partager un fichier, lien externe vérifié, push vers download, doctor, diagnostic portail, « ça ne fonctionne pas à tous les coups »
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

## §0 — Contexte Système (SHARED v1.6.8)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.

## §A — DÉCLENCHEURS

- `vue-upload` ou `vue_upload`
- « donne-moi accès aux fichiers / au dossier download »
- « je ne peux pas télécharger le document »
- « crée un portail / une page pour mes livrables »
- « lance le serveur de fichiers »
- « partage ce fichier / donne-moi un lien vérifié » (share)
- « mets ce fichier dans download / dans les livrables » (push)
- « pourquoi ça ne fonctionne pas / diagnostique le portail » (doctor)

## §1 — SPÉCIFICATION FONCTIONNELLE

### §1.1 Description

vue-upload matérialise le lien manquant entre les livrables produits par l'agent
(`/home/z/my-project/download/`, `/home/z/my-project/upload/`) et le navigateur du
propriétaire. À la demande (ou dès qu'un livrable doit être consulté), l'agent démarre
le serveur `scripts/vue_upload_server.py` sur le port d'écoute de l'espace de travail
(défaut 3000 — convention plateforme, cf. FC_CUSTOM_LISTEN_PORT / preview) et communique
l'URL de preview de la session. Le portail affiche les deux dossiers, permet de
télécharger chaque fichier et de téléverser des fichiers (destination au choix),
rafraîchissement automatique 15 s.

### §1.2 Comportement de l'agent

1. **Garde préalable** : `python3 skills/gen-plan/scripts/ensure-installed.py --preempt` (É1-INSTALL) —
   SANS correct-work automatique (KB Task 36 : correct-work = demande explicite ou vérification finale).
2. **PANEL RAPIDE (v1.1.0 — voie par défaut, idempotent)** :
   `python3 {{SKILLS_ROOT}}vue-upload/scripts/vue_upload_panel.py [--port 3000] [--hold N] [--json]`
   - voie CHAUDE (portail déjà vivant) : rapport immédiat < 1 s, aucun démarrage (no-op honnête) ;
   - voie FROIDE : serveur démarré IN-PROCESS (thread daemon, import du Handler de
     vue_upload_server.py — zéro subprocess, zéro setsid) → vivant en < 2 s, vérification intégrée ;
   - `--hold N` : MAINTIENT le portail N secondes pendant l'appel d'outil (session d'accès
     deux temps, KB Task 34 — edge :81 → :3000 ; ≤ 540 s ≤ 600 s max plateforme) ;
   - `--json` : sortie machine-readable (evals VU-6, intégrations mécaniques).
   (L'ancienne voie setsid de v1.0.0 reste possible pour un démon détaché mais n'est plus
   recommandée : processus fauché entre les appels — constats Tasks 31/33 ; jamais
   `python -c` inline — règle Script Persistence.)
3. **SOUS-COMMANDES (v1.2.0 — boîte à outils ; sans sous-commande = panel v1.1.0 inchangé)** :
   - `share <fichier> [--as NOM] [--bin BIN] [--no-filebin] [--no-tmpfiles] [--json]` :
     repli externe AUTOMATISÉ — filebin.net (≈ 6 jours) + tmpfiles.org (≈ 60 min) ;
     VÉRIFICATION sha256 par re-téléchargement intégrée — un lien n'est annoncé VÉRIFIÉ
     qu'après preuve d'intégrité (rc 4 si aucun lien vérifié ; filebin exige un bin ≥ 16
     caractères — défaut : bin aléatoire) ;
   - `push <source> [--as NOM] [--dir download|upload] [--force]` : inscription d'un
     fichier dans download/ ou upload/ avec les MÊMES règles que le serveur (assainissement,
     cachés refusés, 200 Mo max) ; no-op honnête si contenu identique ; --force requis
     pour écraser un contenu différent (rc 5 sinon) ;
   - `doctor` : diagnostic < 1 s (racine, dossiers, port, edge :81, disque, python) +
     VOIE RECOMMANDÉE (pret / local / a-demarrer / repli) — répond à « pourquoi ça
     ne fonctionne pas à tous les coups » ;
   - parseur tolérant : les drapeaux globaux (--json, --port, --root, --sort, --filter)
     sont acceptés AVANT ou APRÈS la sous-commande.
   Codes retour : 0 OK · 2 bind impossible · 3 portail mort · 4 vérification impossible ·
   5 push destination existante (sans --force) · 6 source ou nom invalide.
4. **Vérification** : intégrée au panel (portail_vivant, listing download/upload, routage
   preview edge :81) ; contrôle croisé : `curl 127.0.0.1:3000/files` → JSON 200.
5. **Communication** : donner l'URL de preview de la session (format plateforme) + préciser
   que le portail liste download/ et upload/. Si l'URL de preview est indisponible pour
   l'utilisateur, solution de repli : `share <fichier>` (§1.2-3) — l'hébergement externe
   temporaire est désormais UNE COMMANDE, avec vérification sha256 automatique.
6. **Journalisation** : entrée worklog (Task ID, port, fichiers servis).

### §1.3 Endpoints du serveur

| Méthode | Route | Effet |
|---------|-------|-------|
| GET | `/` | UI (liste + formulaire de téléversement, palette DM-1) |
| GET | `/files` | JSON des deux dossiers (nom, taille, mtime) |
| GET | `/get/<dir>/<fichier>` | téléchargement (Content-Disposition attachment) |
| POST | `/upload/<dir>` | téléversement multipart (dir ∈ {download, upload}) |

### §1.4 Sécurité

- Racine verrouillée : `safe_join` (realpath + basename) — traversée `../` refusée (HTTP 400/404).
- Noms assainis (`[\\/:*?"<>|]` → `_`, basename forcé, refus des noms cachés).
- Taille max d'envoi 200 Mo (HTTP 413 au-delà).
- Méthodes limitées GET/POST ; lecture seule hors download/ et upload/.

## §2 — SPÉCIFICATION TECHNIQUE

### §2.1 Stack

- Python ≥ 3.10, bibliothèque standard uniquement (http.server, ThreadingHTTPServer).
- Dual-stack : bind `::` avec IPV6_V6ONLY=0, repli IPv4 `0.0.0.0`.
- Aucune dépendance externe ; état sans serveur (listing filesystem à chaque requête).

### §2.2 Structure

```
{{SKILLS_ROOT}}vue-upload/
├── SKILL.md
├── scripts/
│   ├── vue_upload_server.py    # serveur + UI (un fichier, stdlib)
│   └── vue_upload_panel.py     # v1.2.0 — panel (voie chaude/froide, --hold, --json,
│                               #   tri/filtre) + sous-commandes share / push / doctor
└── evals/
    ├── evals.json
    └── trigger_evals.json
```

### §2.3 Provenance et journal

- Provenance : CRÉÉ-VIA-PROTOCOLE (skill-creator, Task 31, session web-bbbeab47) ;
  v1.1.0 : panel rapide + protocole deux temps intégrés (Task 36, D036-06/07 — recherche
  z.ai : AUCUNE commande/fonction documentée pour un panneau livrables, 4 requêtes web,
  17 résultats non pertinents, API storage = jeton absent — le mécanisme réel = preview edge :81) ;
  v1.2.0 (Task 39, approfondissement — directive propriétaire) : share/push/doctor
  automatisés + listing trié/filtré ; suite task39 14/14 PASS dont régression Task 33
  15/15 (scripts/task39-test-vue-upload-v120.json).
- Journal serveur : `/home/z/my-project/scripts/vue-upload.log` (voie setsid héritée) ;
  v1.1.0 : panneau éphémère in-process, sans journal persistant (état = listing filesystem).
- Intégration KB : entrée registre (Task 31) — voir {{KB_PATH}}.

## §3 — LIMITES CONNUES (honnêteté R3)

- **Contrainte sandbox vérifiée (Task 31)** : le conteneur fauche tous les processus de fond entre
  les appels d'outils (serveur setsid et boucle watchdog tués ; tmux/crontab/systemd bus absents).
  Le portail ne peut PAS persister : il se démarre À LA DEMANDE (§1.2) et meurt quelques instants
  après la fin de l'appel. **v1.1.0 — session d'accès deux temps (KB Task 34)** : l'agent lance
  `vue_upload_panel.py --hold 540` (≤ 600 s max plateforme) et l'utilisateur clique son bouton
  preview pendant la fenêtre — routage edge :81 → :3000 prouvé empiriquement (Server: Caddy →
  Server: vue-upload). `vue-upload-hold.sh` (Task 34) est remplacé par `--hold` (même protocole,
  voie in-process plus rapide).
- **Voie d'accès principale en environnement actuel** : le repli (hébergement externe
  temporaire) — **AUTOMATISÉ depuis v1.2.0 : `vue_upload_panel.py share <fichier>`**
  (tmpfiles.org POST /api/v1/upload avec sonde d'interstitiel + extraction du lien /dl/ réel,
  filebin.net PUT /<bin-long>/<fichier> — bin ≥ 16 caractères, rétention ≈ 6 jours) ;
  la vérification sha256 par re-téléchargement est intégrée (fin de la procédure manuelle
  curl -o + cmp de v1.1.0) et un lien n'est annoncé VÉRIFIÉ qu'après preuve d'intégrité.
  Diagnostic « pourquoi ça ne fonctionne pas » : `doctor` (< 1 s, voie recommandée).
- Pas d'authentification : le portail est un outil de workspace, exposition volontairement locale/preview.
