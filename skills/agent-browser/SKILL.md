---
name: Agent Browser
version: "1.0.0"
category: "Autres"
tags:
  - agent
  - browser
description: Un CLI d'automatisation de navigateur headless rapide, basé sur Rust avec repli Node.js, qui permet aux agents IA de naviguer, cliquer, saisir du texte et capturer des pages via des commandes structurées.
language: fr
read_when:
  - Automatiser des interactions web
  - Extraire des données structurées de pages
  - Remplir des formulaires par programme
  - Tester des interfaces web
metadata: {"clawdbot":{"emoji":"🌐","requires":{"bins":["node","npm"]}}}
allowed-tools: Bash(agent-browser:*)

---

# Automatisation de navigateur avec agent-browser

## Installation

### npm recommandé

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
agent-browser open <url>        # Navigate to page
agent-browser snapshot -i       # Get interactive elements with refs
agent-browser click @e1         # Click element by ref
agent-browser fill @e2 "text"   # Fill input by ref
agent-browser close             # Close browser
```

## Workflow de base

1. Naviguer : `agent-browser open <url>`
2. Snapshot : `agent-browser snapshot -i` (renvoie les éléments avec des refs comme `@e1`, `@e2`)
3. Interagir en utilisant les refs issues du snapshot
4. Refaire un snapshot après une navigation ou un changement important du DOM

## Commandes

### Navigation

```bash
agent-browser open <url>      # Navigate to URL
agent-browser back            # Go back
agent-browser forward         # Go forward
agent-browser reload          # Reload page
agent-browser close           # Close browser
```

### Snapshot (analyse de page)

```bash
agent-browser snapshot            # Full accessibility tree
agent-browser snapshot -i         # Interactive elements only (recommended)
agent-browser snapshot -c         # Compact output
agent-browser snapshot -d 3       # Limit depth to 3
agent-browser snapshot -s "#main" # Scope to CSS selector
```

### Interactions (utiliser les @refs du snapshot)

```bash
agent-browser click @e1           # Click
agent-browser dblclick @e1        # Double-click
agent-browser focus @e1           # Focus element
agent-browser fill @e2 "text"     # Clear and type
agent-browser type @e2 "text"     # Type without clearing
agent-browser press Enter         # Press key
agent-browser press Control+a     # Key combination
agent-browser keydown Shift       # Hold key down
agent-browser keyup Shift         # Release key
agent-browser hover @e1           # Hover
agent-browser check @e1           # Check checkbox
agent-browser uncheck @e1         # Uncheck checkbox
agent-browser select @e1 "value"  # Select dropdown
agent-browser scroll down 500     # Scroll page
agent-browser scrollintoview @e1  # Scroll element into view
agent-browser drag @e1 @e2        # Drag and drop
agent-browser upload @e1 file.pdf # Upload files
```

### Obtenir des informations

```bash
agent-browser get text @e1        # Get element text
agent-browser get html @e1        # Get innerHTML
agent-browser get value @e1       # Get input value
agent-browser get attr @e1 href   # Get attribute
agent-browser get title           # Get page title
agent-browser get url             # Get current URL
agent-browser get count ".item"   # Count matching elements
agent-browser get box @e1         # Get bounding box
```

### Vérifier l'état

```bash
agent-browser is visible @e1      # Check if visible
agent-browser is enabled @e1      # Check if enabled
agent-browser is checked @e1      # Check if checked
```

### Captures d'écran et PDF

```bash
agent-browser screenshot          # Screenshot to stdout
agent-browser screenshot path.png # Save to file
agent-browser screenshot --full   # Full page
agent-browser pdf output.pdf      # Save as PDF
```

### Enregistrement vidéo

```bash
agent-browser record start ./demo.webm    # Start recording (uses current URL + state)
agent-browser click @e1                   # Perform actions
agent-browser record stop                 # Stop and save video
agent-browser record restart ./take2.webm # Stop current + start new recording
```

L'enregistrement crée un contexte neuf mais préserve les cookies/stockage de votre session. Si aucune URL n'est fournie, il retourne automatiquement à votre page courante. Pour des démos fluides, explorez d'abord, puis démarrez l'enregistrement.

### Attendre

```bash
agent-browser wait @e1                     # Wait for element
agent-browser wait 2000                    # Wait milliseconds
agent-browser wait --text "Success"        # Wait for text
agent-browser wait --url "/dashboard"    # Wait for URL pattern
agent-browser wait --load networkidle      # Wait for network idle
agent-browser wait --fn "window.ready"     # Wait for JS condition
```

### Contrôle de la souris

```bash
agent-browser mouse move 100 200      # Move mouse
agent-browser mouse down left         # Press button
agent-browser mouse up left           # Release button
agent-browser mouse wheel 100         # Scroll wheel
```

### Localisateurs sémantiques (alternative aux refs)

```bash
agent-browser find role button click --name "Submit"
agent-browser find text "Sign In" click
agent-browser find label "Email" fill "user@test.com"
agent-browser find first ".item" click
agent-browser find nth 2 "a" text
```

### Réglages du navigateur

```bash
agent-browser set viewport 1920 1080      # Set viewport size
agent-browser set device "iPhone 14"      # Emulate device
agent-browser set geo 37.7749 -122.4194   # Set geolocation
agent-browser set offline on              # Toggle offline mode
agent-browser set headers '{"X-Key":"v"}' # Extra HTTP headers
agent-browser set credentials user pass   # HTTP basic auth
agent-browser set media dark              # Emulate color scheme
```

### Cookies et stockage

```bash
agent-browser cookies                     # Get all cookies
agent-browser cookies set name value      # Set cookie
agent-browser cookies clear               # Clear cookies
agent-browser storage local               # Get all localStorage
agent-browser storage local key           # Get specific key
agent-browser storage local set k v       # Set value
agent-browser storage local clear         # Clear all
```

### Réseau

```bash
agent-browser network route <url>              # Intercept requests
agent-browser network route <url> --abort      # Block requests
agent-browser network route <url> --body '{}'  # Mock response
agent-browser network unroute [url]            # Remove routes
agent-browser network requests                 # View tracked requests
agent-browser network requests --filter api    # Filter requests
```

### Onglets et fenêtres

```bash
agent-browser tab                 # List tabs
agent-browser tab new [url]       # New tab
agent-browser tab 2               # Switch to tab
agent-browser tab close           # Close tab
agent-browser window new          # New window
```

### Frames

```bash
agent-browser frame "#iframe"     # Switch to iframe
agent-browser frame main          # Back to main frame
```

### Boîtes de dialogue

```bash
agent-browser dialog accept [text]  # Accept dialog
agent-browser dialog dismiss        # Dismiss dialog
```

### JavaScript

```bash
agent-browser eval "document.title"   # Run JavaScript
```

### Gestion de l'état

```bash
agent-browser state save auth.json    # Save session state
agent-browser state load auth.json    # Load saved state
```

## Exemple : soumission de formulaire

```bash
agent-browser open https://example.com/form
agent-browser snapshot -i
# Output shows: textbox "Email" [ref=e1], textbox "Password" [ref=e2], button "Submit" [ref=e3]

agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password123"
agent-browser click @e3
agent-browser wait --load networkidle
agent-browser snapshot -i  # Check result
```

## Exemple : authentification avec état sauvegardé

```bash
# Login once
agent-browser open https://app.example.com/login
agent-browser snapshot -i
agent-browser fill @e1 "username"
agent-browser fill @e2 "password"
agent-browser click @e3
agent-browser wait --url "/dashboard"
agent-browser state save auth.json

# Later sessions: load saved state
agent-browser state load auth.json
agent-browser open https://app.example.com/dashboard
```

## Sessions (navigateurs parallèles)

```bash
agent-browser --session test1 open site-a.com
agent-browser --session test2 open site-b.com
agent-browser session list
```

## Sortie JSON (pour le parsing)

Ajoutez `--json` pour une sortie lisible par une machine :

```bash
agent-browser snapshot -i --json
agent-browser get text @e1 --json
```

## Débogage

```bash
agent-browser open example.com --headed              # Show browser window
agent-browser console                                # View console messages
agent-browser console --clear                        # Clear console
agent-browser errors                                 # View page errors
agent-browser errors --clear                         # Clear errors
agent-browser highlight @e1                          # Highlight element
agent-browser trace start                            # Start recording trace
agent-browser trace stop trace.zip                   # Stop and save trace
agent-browser record start ./debug.webm              # Record from current page
agent-browser record stop                            # Save recording
agent-browser --cdp 9222 snapshot                    # Connect via CDP
```

## Dépannage

- Si la commande est introuvable sous Linux ARM64, utilisez le chemin complet du dossier bin.
- Si un élément est introuvable, utilisez snapshot pour trouver la bonne ref.
- Si la page n'est pas chargée, ajoutez une commande wait après la navigation.
- Utilisez --headed pour afficher la fenêtre du navigateur lors du débogage.

## Options

- --session <name> utilise une session isolée.
- --json fournit une sortie JSON.
- --full prend une capture de la page entière.
- --headed affiche la fenêtre du navigateur.
- --timeout définit le timeout de la commande en millisecondes.
- --cdp <port> se connecte via le Chrome DevTools Protocol.

## Notes

- Les refs sont stables pour un chargement de page donné mais changent à la navigation.
- Faites toujours un snapshot après une navigation pour obtenir de nouvelles refs.
- Utilisez fill plutôt que type pour les champs de saisie afin de garantir l'effacement du texte existant.

## Signaler des problèmes

- Problèmes du skill : ouvrez une issue sur https://github.com/TheSethRose/Agent-Browser-CLI
- Problèmes du CLI agent-browser : ouvrez une issue sur https://github.com/vercel-labs/agent-browser
