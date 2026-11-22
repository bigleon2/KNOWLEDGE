#!/usr/bin/env python3
"""Task 113 — Corrections de conformité massives (voies canoniques).

Directive propriétaire trace 1a201e4bda5a2289 + précision trace 1a201ea1991bd6dd :
- skills → normes skill-creator ; agents → normes agent-creator/autonomous-agent (4/4 déjà conformes).
- agent-browser : réécriture complète (ordre explicite).
- 26 skills KB : triptyque read_when (S08), suppression emojis (S10 — exception ⚙️
  script-creator documentée KO-L003 : format canonique d'injection propagate-context),
  clause de déclenchement additive autonomous-agent (S07).
- Bump PATCH ×26 + cascade KO-L004 : en-têtes KB + pins ECO_SKILLS ×2 arbres +
  evals.json ×2 arbres (22/26 porteurs).
- Voie canonique : édition DÉPÔT → commit → bootstrap → certification.

Idempotent : re-exécuter = 0 changement. Stdlib uniquement.
Codes retour : 0 = PASS, 1 = échec, 2 = selftest.
"""
# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.45)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
# Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
# Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

RACINE = Path("/home/z/my-project")
DEPOT = RACINE / "KNOWLEDGE-repo"
HOSTE_SKILLS = RACINE / "skills"
DEPOT_SKILLS = DEPOT / "skills"
RAPPORT = RACINE / "scripts/task113-corrections-rapport.json"

TRIPTYQUE = "  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).\n"

# ---------------------------------------------------------------- ciblages
SKILLS_S08 = [  # read_when présent sans triptyque
    "agent-creator", "analyse-doc-s4mk2", "iphone17", "iphone18", "iphone19",
    "livraison-garantie", "midi-doc-expert", "multi-shift-architect",
    "orchestrateur-tsi", "pm-skill", "re-curation", "refactor-guard",
    "refactoring-engineering", "refactoring-test", "tsi-architect", "tsi-validator",
]
SKILLS_S10 = {  # suppressions d'emojis ciblées (chaîne exacte → remplacement)
    "context-engineering": [("> 📎 ", "> ")],
    "correct-work": [("> 📎 ", "> ")],
    "skills-inventory": [("> 📎 ", "> ")],
    "graph-engineering": [("> 📎 ", "> ")],
    "harness-engineering": [("> 📎 ", "> ")],
    "loop-engineering": [("> 📎 ", "> ")],
    "cpp-analysis": [('echo "🔍 ', 'echo "'), ('echo "📊 ', 'echo "'),
                     ('echo "📚 ', 'echo "')],
    "iphone17": [("## 📋 ", "## "), ("## 🧠 ", "## "), ("## 🗺️ ", "## "), ("## 🖼️ ", "## ")],
    "iphone18": [("## 📋 ", "## "), ("## 🧠 ", "## "), ("## 🗺️ ", "## "), ("## 🖼️ ", "## ")],
    "iphone19": [("## 📋 ", "## "), ("## 🧠 ", "## "), ("## 🗺️ ", "## "), ("## 🖼️ ", "## ")],
    "skill-finder-cn": [("    emoji: 🔍\n", ""), (" 🔍", "")],
}
SKILL_S07_DESC = {  # clause de déclenchement ADDITIVE (non-régression)
    "autonomous-agent": " Utiliser quand l'utilisateur demande d'exécuter, de créer, de "
                        "tester ou de simuler un agent autonome persistant (format .agent), "
                        "de traiter une requête de bout en bout de façon autonome, de "
                        "persister un état entre les sessions, ou de reprendre un travail "
                        "long avec intégration multi-LLM et orchestration multi-agents.",
}
SKILLS_APE = ["agent-prompt-engineering"]  # read_when ABSENT → bloc complet

# Skills modifiés = union (bump PATCH + cascade)
SKILLS_MODIFIES = sorted(set(SKILLS_S08) | set(SKILLS_S10) | set(SKILL_S07_DESC) | set(SKILLS_APE))


def h():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def lire(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def ecrire(p: Path, t: str):
    p.write_text(t, encoding="utf-8")


def bump_patch(v: str) -> str:
    a, b, c = v.split(".")
    return f"{a}.{b}.{int(c) + 1}"


def fix_read_when(texte: str, complet: bool = False) -> str:
    """Ajoute le triptyque au read_when existant, ou insère un bloc complet."""
    if complet:
        bloc = ("read_when:\n"
                "  - Déclencher quand la demande concerne : optimiser, évaluer, itérer ou "
                "valider un prompt complexe (rédaction, restructuration, restructure, "
                "restructurer) — pré-traitement PROMPT-GATEWAY des demandes complexes en "
                "tête de chaîne gen-plan (É1-PROMPT-GATEWAY §1.16).\n"
                "  - Déclencher si la demande mentionne : prompt complexe, PROMPT-GATEWAY, "
                "optimisation de prompt, restructure, restructurer, réécriture de demande, "
                "évaluation de prompt, itération, validation de déclencheurs.\n" + TRIPTYQUE)
        # insertion avant dependencies: ou fin de frontmatter
        fin = texte.find("---", 4)
        fm = texte[:fin]
        corps = texte[fin:]
        m = re.search(r"\ndependencies:", fm)
        if m:
            return fm[:m.start()] + "\n" + bloc + fm[m.start():] + corps
        return fm + bloc + corps
    # triptyque à ajouter au bloc read_when existant
    m = re.search(r"read_when:\n((?:  - .*\n)+)", texte)
    if not m:
        return texte
    bloc = m.group(0)
    if "Ne pas déclencher hors de ce périmètre" in bloc:
        return texte
    return texte.replace(bloc, bloc + TRIPTYQUE, 1)


def fix_skill(skill: str) -> dict:
    """Applique les corrections d'un skill sur le DÉPÔT. Retourne le journal d'actions.

    Idempotent : skill déjà corrigé → statut DEJA_CONFORME (re-exécution sans effet).
    """
    p = DEPOT_SKILLS / skill / "SKILL.md"
    t0 = lire(p)
    t = t0
    actions = []
    if skill in SKILLS_APE:
        nt = fix_read_when(t, complet=True)
        if nt != t:
            t = nt
            actions.append("read_when bloc complet ajouté (S08)")
    elif skill in SKILLS_S08:
        nt = fix_read_when(t)
        if nt != t:
            t = nt
            actions.append("triptyque read_when ajouté (S08)")
    for ancien, nouveau in SKILLS_S10.get(skill, []):
        n = ancien in t
        if n:
            t = t.replace(ancien, nouveau)
            actions.append(f"emoji retiré : {ancien.strip()!r} (S10)")
    if skill in SKILL_S07_DESC:
        m = re.search(r"description: >\n((?:  .*\n)+)", t)
        if m and "Utiliser quand" not in m.group(1):
            lignes = m.group(1)
            # clause ajoutée en fin de description (dernière ligne du bloc plié)
            nl = lignes.rstrip("\n").split("\n")
            # fractionner la clause en 2 lignes indentées pliées
            clause = SKILL_S07_DESC[skill].strip()
            mi = len(clause) // 2
            coupure = clause.find(" ", mi)
            l1, l2 = clause[:coupure].strip(), clause[coupure:].strip()
            nl.append("  " + l1)
            nl.append("  " + l2 + "\n")
            t = t.replace(m.group(0), "description: >\n" + "\n".join(nl) + "\n", 1)
            actions.append("clause de déclenchement additive (S07)")
    if t == t0:
        return {"skill": skill, "actions": actions,
                "statut": "DEJA_CONFORME" if not rate_encore(t, skill) else "AUCUN_CHANGEMENT"}
    # bump PATCH frontmatter
    m = re.search(r"version: (\d+\.\d+\.\d+)", t)
    ancienne, nouvelle = m.group(1), bump_patch(m.group(1))
    t = t.replace(f"version: {ancienne}", f"version: {nouvelle}", 1)
    actions.append(f"bump PATCH {ancienne}→{nouvelle}")
    ecrire(p, t)
    return {"skill": skill, "actions": actions, "version": [ancienne, nouvelle],
            "statut": "MODIFIE"}


def cascade(skill: str, ancienne: str, nouvelle: str) -> dict:
    """Cascade KO-L004 — voie canonique : DÉPÔT seul (bootstrap projet vers l'hôte).

    1. en-tête KB (dépôt) · 2. pin ECO_SKILLS (dépôt) · 3. evals.json (dépôt).
    """
    c = {}
    kb_p = DEPOT_SKILLS / "KNOWLEDGE.md"
    kb = lire(kb_p)
    head = f"## {skill} v{ancienne}"
    if head in kb:
        kb = kb.replace(head, f"## {skill} v{nouvelle}", 1)
        ecrire(kb_p, kb)
        c["kb"] = f"{ancienne}→{nouvelle}"
    p = DEPOT / "scripts/check-ecosysteme-integrity.py"
    t = lire(p)
    anc_pin = f'"{skill}": "{ancienne}"'
    if anc_pin in t:
        t = t.replace(anc_pin, f'"{skill}": "{nouvelle}"', 1)
        ecrire(p, t)
        c["pin"] = f"{ancienne}→{nouvelle}"
    p = DEPOT_SKILLS / skill / "evals" / "evals.json"
    if p.exists():
        d = json.loads(lire(p))
        if isinstance(d, dict):
            if d.get("version") == ancienne:
                d["version"] = nouvelle
                ecrire(p, json.dumps(d, ensure_ascii=False, indent=2) + "\n")
                c["evals"] = f"{ancienne}→{nouvelle}"
            else:
                c["evals"] = f"déjà alignée ou autre ({d.get('version')})"
        else:
            c["evals"] = "format liste sans champ version — non applicable"
    return c


AGENT_BROWSER = """---
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

## §0 — Contexte Système (SHARED v1.7.44)

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
"""


def agent_browser_reecriture() -> dict:
    """G1 — réécriture agent-browser (dépôt + hôte, hors-KB : bootstrap ne projette pas)."""
    for p in (DEPOT_SKILLS / "agent-browser" / "SKILL.md",
              HOSTE_SKILLS / "agent-browser" / "SKILL.md"):
        ecrire(p, AGENT_BROWSER)
    return {"skill": "agent-browser", "statut": "REECRIT",
            "copies": ["dépôt", "hôte"],
            "raison": "ordre explicite directive Task 113 — hors-KB (requis gen-plan) "
                      "car bootstrap ne projette pas les hors-KB"}


def selftest() -> int:
    ok = 0
    tests = [
        ("bump", bump_patch("1.2.4") == "1.2.5"),
        ("bump_retenue", bump_patch("1.0.10") == "1.0.11"),
        ("sans_read_when_inchange", fix_read_when("---\nname: x\n---\n") == "---\nname: x\n---\n"),
    ]
    t = "---\nname: x\nversion: 1.0.0\nread_when:\n  - A.\n  - B.\n---\n"
    tests.append(("triptyque_ajout", "Ne pas déclencher hors de ce périmètre" in fix_read_when(t)))
    tests.append(("triptyque_idempotent", fix_read_when(fix_read_when(t)) == fix_read_when(t)))
    tests.append(("ape_complet", "read_when:" in fix_read_when(
        "---\nname: x\ndescription: >\n  Test.\n---\n", complet=True)))
    for nom, res in tests:
        print(("PASS" if res else "FAIL") + " " + nom)
        ok += 1 if res else 0
    print(f"SELFTEST {ok}/{len(tests)}")
    return 0 if ok == len(tests) else 1


def rate_encore(t: str, skill: str) -> bool:
    """True si le SKILL.md présenterait encore une défaillance ciblée (garde anti-silence)."""
    if skill in SKILLS_APE:
        return "read_when:" not in t
    if skill in SKILLS_S08:
        m = re.search(r"read_when:\n((?:  - .*\n)+)", t)
        return bool(m) and "Ne pas déclencher hors de ce périmètre" not in m.group(0)
    if skill in SKILLS_S10:
        return any(a in t for a, _ in SKILLS_S10[skill])
    if skill in SKILL_S07_DESC:
        return "Utiliser quand" not in t
    return False


def main() -> int:
    journal = {"horodatage": h(), "agent_browser": None, "skills": {}, "cascades": {}}

    # Phase 0 : agent-browser (dépôt + hôte direct)
    journal["agent_browser"] = agent_browser_reecriture()
    print("G21 agent-browser : REECRIT (dépôt + hôte)")

    # Phase 1 : corrections skills ×26 (dépôt)
    for s in SKILLS_MODIFIES:
        r = fix_skill(s)
        journal["skills"][s] = r
        if r["statut"] == "MODIFIE":
            ancienne, nouvelle = r["version"]
            journal["cascades"][s] = cascade(s, ancienne, nouvelle)
        print(f"  {s}: {r['statut']} — {'; '.join(r['actions']) or 'aucune action'}")

    # Phase 2 : contrôle que tout a été modifié (garde anti-silence)
    rate = [s for s, r in journal["skills"].items() if r["statut"] == "AUCUN_CHANGEMENT"]
    if rate:
        print("GARDE : skills non modifiés →", rate)
        RAPPORT.write_text(json.dumps(journal, ensure_ascii=False, indent=2), encoding="utf-8")
        return 1
    RAPPORT.write_text(json.dumps(journal, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"RAPPORT : {RAPPORT}")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    sys.exit(main())
