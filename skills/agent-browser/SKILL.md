---
name: agent-browser
version: 1.0.0
category: infrastructure
language: fr
tags:
  - agent-browser
  - navigateur
  - headless
  - automatisation-web
  - snapshot
description: >
  Skill d'automatisation de navigateur headless via la CLI agent-browser (vercel-labs,
  Rust avec repli Node.js) : naviguer, cliquer, saisir, extraire et capturer des pages
  via des commandes structurées avec refs (@e1…). Utiliser quand l'utilisateur demande
  d'automatiser des interactions web (navigation, clics, formulaires), d'extraire des
  données structurées de pages, de tester des interfaces web, de capturer des
  instantanés ou des captures d'écran, ou quand une escalade E5 de gen-plan atteint
  la contingence agent-browser (WebFetch → curl → agent-browser → z-ai). Requis
  gen-plan hors-KB (SKILLS_REQUIS_GENPLAN, garde ensure-installed.py — Task 112 G15).
dependencies:
  - skill: gen-plan
    version: ">=3.15.0"
    used_at: "escalade E5 — contingence agent-browser des sondages web"
read_when:
  - Déclencher quand la demande concerne : automatiser un navigateur headless (ouvrir,
    cliquer, remplir, extraire, capturer) via la CLI agent-browser, ou restaurer la
    contingence E5 de gen-plan quand WebFetch et curl sont insuffisants.
  - Déclencher si la demande mentionne : agent-browser, navigateur headless, snapshot,
    ref @e, automatisation web, scraping structuré, capture d'écran, test d'UI, CDP.
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

## §0 — Contexte Système (SHARED v1.7.47)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.
> Langue : FRANÇAIS exclusif pour tous les échanges avec le propriétaire (règle d'or n°6 gen-plan — directive 2026-10-31, renforcée 2026-11-06) : dès le PREMIER mot de toute session ou reprise, la langue d'un message, d'un résumé de continuation ou d'un canal ne dérive JAMAIS la réponse ; toute dérive est corrigée immédiatement.
> Règles d'or & lecture SHARED à l'exécution (directive propriétaire 2026-11-06 — SHARED §9) : tout skill/agent/script exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or de l'écosystème (résumé §9 — canonique gen-plan §1.5).
> Référence canonique skill/agent (directive propriétaire 2026-11-07 — SHARED §0/§1.2) : toute référence à « mon skill X »/« mon agent X » désigne la forme installée à la racine `skills/X/SKILL.md`, JAMAIS le prompt maître du corpus `@mon-ecosysteme/` (ex-nommé `@PM-SKILLS/`) — les PMs sont des spécifications générées mécaniquement (KO-L004), les skills installés sont les formes exécutables.

## §0 — RÈGLE ZÉRO (résumé de SHARED §0)

Skill auto-contenu versionné semver ; les commandes CLI de l'outil tiers `agent-browser`
restent en anglais verbatim (syntaxe d'outil externe — artefact technique, règle d'or n°6) ;
la documentation, les titres et les notes sont en français. Hors-KB mais requis par
gen-plan (escalade E5, garde ensure-installed.py). Provenance : HÉRITÉ-CORPUS
(TheSethRose/Agent-Browser-CLI) RÉÉCRIT via les normes skill-creator — directive
propriétaire Task 113 (trace 1a201e4bda5a2289).

## Installation

### npm (recommandé)

```bash
npm install -g agent-browser
agent-browser install
agent-browser install --with-deps
```

### Depuis les sources

```bash
git clone https://github.com/vercel-labs/agent-browser
cd agent-browser
pnpm install
pnpm build
agent-browser install
```

## Démarrage rapide

```bash
agent-browser open <url>        # Naviguer vers la page
agent-browser snapshot -i       # Éléments interactifs avec refs
agent-browser click @e1         # Cliquer un élément par ref
agent-browser fill @e2 "texte"  # Remplir un champ par ref
agent-browser close             # Fermer le navigateur
```

## Flux de travail principal

1. Naviguer : `agent-browser open <url>`
2. Instantané : `agent-browser snapshot -i` (renvoie des refs comme `@e1`, `@e2`)
3. Interagir via les refs issues de l'instantané
4. Re-snapshotter après navigation ou changement significatif du DOM

## Commandes

### Navigation

```bash
agent-browser open <url>      # Naviguer vers l'URL
agent-browser back            # Retour
agent-browser forward         # Avancer
agent-browser reload          # Recharger
agent-browser close           # Fermer
```

### Snapshot (analyse de page)

```bash
agent-browser snapshot            # Arbre d'accessibilité complet
agent-browser snapshot -i         # Éléments interactifs seuls (recommandé)
agent-browser snapshot -c         # Sortie compacte
agent-browser snapshot -d 3       # Profondeur limitée à 3
agent-browser snapshot -s "#main" # Cibler un sélecteur CSS
```

### Interactions (refs issues du snapshot)

```bash
agent-browser click @e1           # Clic
agent-browser dblclick @e1        # Double-clic
agent-browser focus @e1           # Focaliser
agent-browser fill @e2 "texte"    # Vider puis saisir
agent-browser type @e2 "texte"    # Saisir sans vider
agent-browser press Enter         # Toucher
agent-browser press Control+a     # Combinaison de touches
agent-browser keydown Shift       # Maintenir
agent-browser keyup Shift         # Relâcher
agent-browser hover @e1           # Survol
agent-browser check @e1           # Cocher
agent-browser uncheck @e1         # Décocher
agent-browser select @e1 "valeur" # Sélectionner une option
agent-browser scroll down 500     # Défiler
agent-browser scrollintoview @e1  # Amener en vue
agent-browser drag @e1 @e2        # Glisser-déposer
agent-browser upload @e1 f.pdf    # Téléverser des fichiers
```

### Lecture d'informations

```bash
agent-browser get text @e1        # Texte de l'élément
agent-browser get html @e1        # innerHTML
agent-browser get value @e1       # Valeur du champ
agent-browser get attr @e1 href   # Attribut
agent-browser get title           # Titre de la page
agent-browser get url             # URL courante
agent-browser get count ".item"   # Nombre d'éléments correspondants
agent-browser get box @e1         # Boîte englobante
```

### Vérifier un état

```bash
agent-browser is visible @e1      # Visibilité
agent-browser is enabled @e1      # Activité
agent-browser is checked @e1      # État de case à cocher
```

### Captures d'écran et PDF

```bash
agent-browser screenshot          # Capture vers stdout
agent-browser screenshot p.png    # Vers fichier
agent-browser screenshot --full   # Page entière
agent-browser pdf sorties.pdf     # PDF
```

### Enregistrement vidéo

```bash
agent-browser record start ./demo.webm    # Démarrer (URL et état courants)
agent-browser record stop                 # Arrêter et sauver
agent-browser record restart ./prise2.webm  # Arrêter puis redémarrer
```

L'enregistrement crée un contexte frais mais préserve cookies et stockage de la
session ; sans URL fournie il revient automatiquement à la page courante. Pour une
démo fluide : explorer d'abord, démarrer l'enregistrement ensuite.

### Attente

```bash
agent-browser wait @e1                   # Attendre un élément
agent-browser wait 2000                  # Attendre en millisecondes
agent-browser wait --text "Succès"       # Attendre un texte
agent-browser wait --url "/tableau-bord" # Attendre un motif d'URL
agent-browser wait --load networkidle    # Attendre le repos du réseau
agent-browser wait --fn "window.ready"   # Attendre une condition JS
```

### Souris

```bash
agent-browser mouse move 100 200   # Déplacer
agent-browser mouse down left      # Appuyer
agent-browser mouse up left        # Relâcher
agent-browser mouse wheel 100      # Molette
```

### Localisateurs sémantiques (alternative aux refs)

```bash
agent-browser find role button click --name "Envoyer"
agent-browser find text "Connexion" click
agent-browser find label "Email" fill "utilisateur@test.com"
agent-browser find first ".item" click
agent-browser find nth 2 "a" text
```

### Réglages du navigateur

```bash
agent-browser set viewport 1920 1080     # Taille de la fenêtre
agent-browser set device "iPhone 14"     # Émuler un appareil
agent-browser set geo 37.7749 -122.4194  # Géolocalisation
agent-browser set offline on             # Mode hors-ligne
agent-browser set headers '{"X-Cle":"v"}' # En-têtes HTTP additionnels
agent-browser set credentials user pass  # Authentification basique
agent-browser set media dark             # Schéma de couleurs
```

### Cookies et stockage

```bash
agent-browser cookies                    # Tous les cookies
agent-browser cookies set nom valeur     # Définir un cookie
agent-browser cookies clear              # Vider les cookies
agent-browser storage local              # Tout le localStorage
agent-browser storage local cle          # Clé spécifique
agent-browser storage local set c v      # Définir une valeur
agent-browser storage local clear        # Tout vider
```

### Réseau

```bash
agent-browser network route <url>              # Intercepter les requêtes
agent-browser network route <url> --abort      # Bloquer
agent-browser network route <url> --body '{}'  # Réponse simulée
agent-browser network unroute [url]            # Retirer les routes
agent-browser network requests                 # Requêtes suivies
agent-browser network requests --filter api    # Filtrer
```

### Onglets et fenêtres

```bash
agent-browser tab                 # Lister
agent-browser tab new [url]       # Nouvel onglet
agent-browser tab 2               # Basculer vers l'onglet
agent-browser tab close           # Fermer l'onglet
agent-browser window new          # Nouvelle fenêtre
```

### Cadres (iframes)

```bash
agent-browser frame "#iframe"     # Basculer vers l'iframe
agent-browser frame main          # Revenir au cadre principal
```

### Boîtes de dialogue

```bash
agent-browser dialog accept [texte]  # Accepter
agent-browser dialog dismiss         # Rejeter
```

### JavaScript

```bash
agent-browser eval "document.title"   # Exécuter du JS
```

### Gestion d'état de session

```bash
agent-browser state save auth.json    # Sauver l'état de session
agent-browser state load auth.json    # Charger un état sauvegardé
```

## Exemple : soumission de formulaire

```bash
agent-browser open https://exemple.com/formulaire
agent-browser snapshot -i
# Sortie : textbox "Email" [ref=e1], textbox "Mot de passe" [ref=e2], button "Envoyer" [ref=e3]

agent-browser fill @e1 "utilisateur@exemple.com"
agent-browser fill @e2 "motdepasse123"
agent-browser click @e3
agent-browser wait --load networkidle
agent-browser snapshot -i  # Vérifier le résultat
```

## Exemple : authentification avec état sauvegardé

```bash
# Connexion unique
agent-browser open https://app.exemple.com/connexion
agent-browser snapshot -i
agent-browser fill @e1 "utilisateur"
agent-browser fill @e2 "motdepasse"
agent-browser click @e3
agent-browser wait --url "/tableau-bord"
agent-browser state save auth.json

# Sessions ultérieures : charger l'état sauvegardé
agent-browser state load auth.json
agent-browser open https://app.exemple.com/tableau-bord
```

## Sessions (navigateurs parallèles)

```bash
agent-browser --session test1 open site-a.com
agent-browser --session test2 open site-b.com
agent-browser session list
```

## Sortie JSON (pour parsing)

Ajouter `--json` pour une sortie lisible par machine :

```bash
agent-browser snapshot -i --json
agent-browser get text @e1 --json
```

## Débogage

```bash
agent-browser open exemple.com --headed              # Afficher la fenêtre
agent-browser console                                # Messages console
agent-browser console --clear                        # Vider la console
agent-browser errors                                 # Erreurs de page
agent-browser errors --clear                         # Vider les erreurs
agent-browser highlight @e1                          # Surligner l'élément
agent-browser trace start                            # Démarrer une trace
agent-browser trace stop trace.zip                   # Arrêter et sauver la trace
agent-browser --cdp 9222 snapshot                    # Connexion via CDP
```

## Dépannage

- Commande introuvable sur Linux ARM64 : utiliser le chemin complet du dossier bin.
- Élément introuvable : faire un snapshot pour obtenir la bonne ref.
- Page non chargée : ajouter une commande wait après la navigation.
- Utiliser `--headed` pour voir la fenêtre pendant le débogage.

## Options

- `--session <nom>` : session isolée.
- `--json` : sortie JSON.
- `--full` : capture de page entière.
- `--headed` : afficher la fenêtre du navigateur.
- `--timeout` : délai d'expiration des commandes en millisecondes.
- `--cdp <port>` : connexion via Chrome DevTools Protocol.

## Notes

- Les refs sont stables par chargement de page mais changent à la navigation.
- Toujours snapshotter après navigation pour obtenir les nouvelles refs.
- Préférer `fill` à `type` pour les champs afin de vider le texte existant.

## Provenance et signalement

- Skill réécrit selon les normes skill-creator de l'écosystème (Task 113) ; contenu
  technique issu de la documentation verbatim de la CLI agent-browser (vercel-labs).
- Problèmes CLI : https://github.com/vercel-labs/agent-browser
