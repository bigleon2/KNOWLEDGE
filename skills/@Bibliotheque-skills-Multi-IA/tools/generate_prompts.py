#!/usr/bin/env python3
"""generate_prompts.py — déclinaisons par plateforme (déterministe ×2).

Génère platforms/<plateforme>/prompt_systeme.md depuis core/processus.md.
Re-exécution : sorties byte-identiques (R6). Python stdlib uniquement.
"""
from __future__ import annotations

import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Adapter le prompt au mode d'invocation propre à chaque plateforme.
PLATEFORMES = {
    "qwen": {
        "invocation": "Collez le prompt ci-dessous dans le champ de saisie "
                      "Qwen (ou référencez-le comme prompt système d'une "
                      "discussion).",
        "contraintes": "Réponses en français. Les fichiers se partagent par "
                       "copier-coller de blocs de code complets.",
    },
    "claude": {
        "invocation": "Placez ce texte en préambule de votre message Claude, "
                      "ou dans un Project (Custom Instructions).",
        "contraintes": "Réponses en français. Précisez les fichiers en pièce "
                       "jointe quand la plateforme le permet.",
    },
    "chatgpt": {
        "invocation": "Utilisez ce texte dans les Instructions "
                      "personnalisées (Custom Instructions) du projet.",
        "contraintes": "Réponses en français. Déclarez chaque livrable en "
                       "bloc de code complet.",
    },
    "copilot": {
        "invocation": "Invocable en prompt inline en tête de conversation "
                      "GitHub Copilot Chat.",
        "contraintes": "Réponses en français. Travailler fichier ouvert "
                       "dans l'éditeur.",
    },
    "perplexity": {
        "invocation": "Utilisez ce texte comme prompt d'ouverture d'un "
                      "thread Perplexity (mode Pro pour les fichiers).",
        "contraintes": "Réponses en français. Citez les sources consultées "
                       "pour toute affirmation externe.",
    },
    "gemini": {
        "invocation": "Placez ce texte dans les instructions sauvegardées "
                      "Gemini (Saved Instructions) ou en tête de discussion.",
        "contraintes": "Réponses en français. Validez chaque livrable avec "
                       "la checklist avant de le déclarer terminé.",
    },
}


def generer() -> int:
    with open(os.path.join(RACINE, "core", "processus.md"),
              encoding="utf-8") as f:
        core = f.read()
    corps = core.split("\n", 3)[3]  # saute l'en-tête de version/avertissement
    for nom, spec in sorted(PLATEFORMES.items()):
        sortie = os.path.join(RACINE, "platforms", nom, "prompt_systeme.md")
        contenu = (
            f"# Prompt système — @processus pour {nom.capitalize()}\n\n"
            f"> Généré automatiquement depuis `core/processus.md` par "
            f"`tools/generate_prompts.py` — ne pas éditer à la main.\n\n"
            f"## Mode d'invocation\n\n{spec['invocation']}\n\n"
            f"## Contraintes de la plateforme\n\n{spec['contraintes']}\n\n"
            f"## Spécification des processus (source de vérité)\n"
            + corps)
        with open(sortie, "w", encoding="utf-8", newline="\n") as f:
            f.write(contenu)
        print(f"  ✅ platforms/{nom}/prompt_systeme.md "
              f"({len(contenu)} caractères)")
    return 0


if __name__ == "__main__":
    sys.exit(generer())
