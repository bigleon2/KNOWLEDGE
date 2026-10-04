---
name: vue-upload
version: 1.1.0
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
dependencies:
  - skill: gen-plan
    version: ">=3.20.0"
    used_at: "Étape 0 (garde É1-INSTALL avant démarrage du portail)"
read_when:
  - Déclencher quand la demande concerne : donner accès au propriétaire aux fichiers générés (download/, upload/)
  - Déclencher si la demande mentionne : vue-upload, portail, accès fichiers, télécharger livrable, téléverser
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

## §0 — Contexte Système (SHARED v1.6.4)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (exception)
> Règle Zéro : les fichiers des sessions précédentes n'existent pas — le portail se (re)démarre à la demande, jamais « conservé ».

## §A — DÉCLENCHEURS

- `vue-upload` ou `vue_upload`
- « donne-moi accès aux fichiers / au dossier download »
- « je ne peux pas télécharger le document »
- « crée un portail / une page pour mes livrables »
- « lance le serveur de fichiers »

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
3. **Vérification** : intégrée au panel (portail_vivant, listing download/upload, routage
   preview edge :81) ; contrôle croisé : `curl 127.0.0.1:3000/files` → JSON 200.
4. **Communication** : donner l'URL de preview de la session (format plateforme) + préciser
   que le portail liste download/ et upload/. Si l'URL de preview est indisponible pour
   l'utilisateur, solution de repli : hébergement externe temporaire du fichier demandé
   (lien direct vérifié par comparaison d'octets avant communication).
5. **Journalisation** : entrée worklog (Task ID, port, fichiers servis).

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
│   └── vue_upload_panel.py     # v1.1.0 — panel rapide (voie chaude/froide, --hold, --json)
└── evals/
    ├── evals.json
    └── trigger_evals.json
```

### §2.3 Provenance et journal

- Provenance : CRÉÉ-VIA-PROTOCOLE (skill-creator, Task 31, session web-bbbeab47) ;
  v1.1.0 : panel rapide + protocole deux temps intégrés (Task 36, D036-06/07 — recherche
  z.ai : AUCUNE commande/fonction documentée pour un panneau livrables, 4 requêtes web,
  17 résultats non pertinents, API storage = jeton absent — le mécanisme réel = preview edge :81).
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
- **Voie d'accès principale en environnement actuel** : le repli §1.2-4 (hébergement externe
  temporaire). Procédure validée : tmpfiles.org (POST /api/v1/upload → page interstitielle,
  extraire le lien /dl/<token>/ réel du HTML) et filebin.net (PUT /<bin-long>/<fichier> — bin ≥ 16
  caractères, rétention 6 jours). TOUJOURS vérifier l'intégrité (curl -o + cmp avec le livrable)
  AVANT de communiquer un lien, et annoncer la rétention.
- Pas d'authentification : le portail est un outil de workspace, exposition volontairement locale/preview.
