#!/usr/bin/env python3
"""
PEK v4.1 — Intégrateur Automatique de Skills
Orchestre l'ajout d'un nouveau skill dans le dépôt KNOWLEDGE et met à jour begin-know.md.

Usage :
    python integrate_skill.py --skill-name resume-chat --target-dir upload/gen-plan-ecosysteme
"""

import argparse
import os
import sys
import subprocess
from pathlib import Path
from datetime import date

# ─── Configuration du Skill à Intégrer ───────────────────────────
SKILL_CONTENT = """# Skill : resume-chat

> **Version** : 1.0.0  
> **Catégorie** : Méta-Analyse & Archivage  
> **Date** : 24 juillet 2026  
> **Auteur** : PEK v4.1 Architect  

## Description

Le skill `resume-chat` est conçu pour générer des résumés détaillés et structurés d'une discussion ou d'un projet. Il assure un tracking précis des versions des artefacts générés, reconstruit la chronologie des interactions et produit un livrable Markdown avec une Table des Matières (TOC) interactive.

## Paramètres d'Entrée

| Paramètre | Type | Valeurs par défaut | Description |
|---|---|---|---|
| `context` | string | Conversation history | Historique de la conversation ou fichiers joints à analyser. |
| `format` | enum | `markdown` | Format de sortie (`markdown`, `json`, `text`). |
| `include_toc` | boolean | `true` | Inclure une Table des Matières avec liens ancres. |
| `track_versions` | boolean | `true` | Activer le suivi des versions des artefacts mentionnés. |

## Pipeline d'Exécution (5 Étapes)

1.  **COLLECTE** : Lecture intégrale du contexte, identification des artefacts (code, docs, scripts) et extraction des métadonnées (versions, dates).
2.  **CHRONOLOGIE** : Reconstruction de la timeline des interactions, regroupement par phases thématiques et identification des points de bascule.
3.  **TRACKING VERSIONS** : Listing des versions successives pour chaque artefact, description concise de l'évolution (≤ 3 lignes) et calcul des gains/métriques.
4.  **STRUCTURATION** : Génération de la TOC, organisation en sections (Vue d'ensemble, Historique, Optimisations) et application du formatage Markdown strict.
5.  **VALIDATION** : Vérification de la complétude, validation des liens TOC et respect de la concision des descriptions.

## Sortie Attendue

Un fichier `.md` téléchargeable contenant :
*   Un titre principal et une Table des Matières interactive.
*   Une vue d'ensemble chronologique sous forme de tableau.
*   Un historique détaillé des artefacts avec leurs évolutions.
*   Une analyse des optimisations clés apportées durant la discussion.
*   Les annexes techniques (skills générés, scripts, configurations).

## Règles Critiques

*   **Préservation** : Ne jamais inventer de versions ou d'évolutions non présentes dans le contexte.
*   **Concision** : Les descriptions d'évolution doivent tenir en 3 lignes maximum.
*   **Exhaustivité** : Couvrir tous les artefacts majeurs mentionnés ou générés.
*   **Formatage** : Utiliser un Markdown strict avec des liens ancres fonctionnels pour la TOC.
*   **Tracking** : Indiquer clairement les numéros de version et les dates associées.

## Intégration dans l'Écosystème

*   **Emplacement** : `KNOWLEDGE.md` section 3.7 (Skills Intégrés).
*   **Invocation** : Déclenché par les phrases clés "résumé chat", "historique versions", "archive discussion".
*   **Dépendances** : Utilise `gen-plan` pour la structure de base et `correct-work` pour la validation finale du résumé.

## Exemple d'Utilisation

**Input** : "Fais un résumé structuré de notre discussion sur le PEK v4.1 en suivant les versions."
**Output** : Génération de `RESUME-DISCUSSION-PEK-v4.1.md` avec TOC et tracking des 5 artefacts principaux.
"""

BEGIN_KNOW_UPDATE = """
3.7 `resume-chat` — Générateur de Résumés Structurés (v1.0.0)
Description : Génère des résumés détaillés avec tracking des versions et TOC interactif.
Usage : Méta-analyse de conversations, archivage de projets.
Déclencheurs : `résumé chat`, `historique versions`, `archive discussion`
Pipeline : 5 étapes (Collecte → Chronologie → Tracking → Structuration → Validation)
Intégration : Dépend de `gen-plan` et `correct-work`.
"""

def run_command(cmd, cwd=None):
    """Exécute une commande shell et retourne le résultat."""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            cwd=cwd, 
            check=True, 
            capture_output=True, 
            text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur commande '{cmd}': {e.stderr}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Intégrateur automatique de skills PEK v4.1")
    parser.add_argument("--skill-name", default="resume-chat", help="Nom du skill (sans extension)")
    parser.add_argument("--target-dir", default="upload/gen-plan-ecosysteme", help="Dossier cible relatif")
    parser.add_argument("--know-file", default="begin-know.md", help="Fichier Knowledge à mettre à jour")
    
    args = parser.parse_args()
    
    repo_root = Path.cwd()
    target_path = repo_root / args.target_dir
    skill_file = target_path / f"{args.skill_name}.md"
    know_file = repo_root / args.know_file

    print(f"🚀 Démarrage de l'intégration du skill '{args.skill_name}'...")
    
    # 1. Vérifier que nous sommes bien dans un dépôt Git
    if not (repo_root / ".git").exists():
        print("❌ Ce dossier ne semble pas être un dépôt Git.")
        sys.exit(1)

    # 2. Créer le dossier cible s'il n'existe pas
    target_path.mkdir(parents=True, exist_ok=True)
    print(f"✅ Dossier cible vérifié : {args.target_dir}")

    # 3. Écrire le fichier du skill
    with open(skill_file, "w", encoding="utf-8") as f:
        f.write(SKILL_CONTENT)
    print(f"✅ Fichier créé : {skill_file.name}")

    # 4. Mettre à jour begin-know.md (Section 3.7)
    if know_file.exists():
        content = know_file.read_text(encoding="utf-8")
        if "resume-chat" not in content:
            # Chercher la fin de la section 3.6 ou le début de la section 4
            # Pour simplifier, on ajoute à la fin de la section 3 si elle existe, ou on crée la section
            if "3.6 `skills-inventory`" in content:
                insert_point = content.find("3.6 `skills-inventory`")
                # Trouver la fin de cette section (prochain saut de ligne double ou prochaine section)
                # Ici on fait simple : on ajoute après la section 3.6
                lines = content.split('\n')
                new_lines = []
                inserted = False
                for line in lines:
                    new_lines.append(line)
                    if "3.6 `skills-inventory`" in line and not inserted:
                        # On attend la fin du bloc 3.6 (ligne vide ou prochaine section 4.)
                        pass 
                
                # Méthode plus robuste : remplacement simple si le marqueur existe
                marker = "3.6 `skills-inventory`"
                if marker in content:
                    # On insère juste après la dernière ligne de la section 3.6
                    # Pour cet exemple, on ajoute simplement à la fin du fichier si la structure est complexe
                    with open(know_file, "a", encoding="utf-8") as kf:
                        kf.write("\n" + BEGIN_KNOW_UPDATE)
                    print(f"✅ Section ajoutée dans {args.know_file}")
            else:
                print("⚠️ Structure de begin-know.md non reconnue, ajout manuel requis.")
        else:
            print("ℹ️ Le skill est déjà présent dans begin-know.md")
    else:
        print(f"⚠️ Fichier {args.know_file} introuvable, mise à jour ignorée.")

    # 5. Git Add
    run_command(f"git add {skill_file}")
    if know_file.exists() and "resume-chat" not in open(know_file, 'r', encoding='utf-8').read():
         # Si on a ajouté le contenu, on l'add aussi
         run_command(f"git add {know_file}")
    elif know_file.exists():
         # Vérifier s'il a été modifié
         status = run_command(f"git status --porcelain {know_file}")
         if status:
             run_command(f"git add {know_file}")

    print("✅ Fichiers stagés (git add)")

    # 6. Git Commit
    commit_msg = f"feat: add {args.skill_name} skill v1.0.0 in markdown format"
    run_command(f'git commit -m "{commit_msg}"')
    print(f"✅ Commit effectué : {commit_msg}")

    # 7. Git Push
    print("📤 Push vers le dépôt distant...")
    run_command("git push origin HEAD")
    print("✅ Push terminé avec succès !")

    print("\n═══════════════════════════════════════════════════════════════")
    print(f"🎉 Intégration terminée ! Le skill '{args.skill_name}' est disponible.")
    print("═══════════════════════════════════════════════════════════════")

if __name__ == "__main__":
    main()