#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.11)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.

task18-pm-install-v180.py — Régénération PM-INSTALL v1.7.2 -> v1.8.0 (Task 18, session
web-fdf5963c, directive propriétaire 2026-10-23 : « optimise le système d'installation
de mon écosystème en regénérant » + prérequis A « assemble au lieu d'installer »).

Contenu de l'optimisation (discipline sub_locked — ABANDON sans écriture si compte != attendu) :
  1. Mécanisme DUAL d'installation codifié (§1 #2, §2 note, §3.2 réécrit) :
     (a) installation DIRECTE des formes certifiées du dépôt = voie PAR DÉFAUT
         (clone git règle d'or n°4, garde R2, arbitres — exécutant canonique :
         scripts/eco_install_pipeline.py) ;
     (b) ASSEMBLAGE depuis les PMs = voie BOOTSTRAP (corpus/archive seul) — les §5
         des PMs demeurent la SPÉCIFICATION de la forme installée.
  2. alias-eco intégré au périmètre : §2bis fermeture MINIMALE, §4 interactions,
     §A.3 extensions, instantané §A.3 rafraîchi.
  3. §7 : ligne d'historique v1.8.0.
"""
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PM_INSTALL = os.path.join(BASE, "skills", "@mon-ecosysteme",
                          "PROMPT-MAITRE-INSTALL-ECOSYSTEME.md")


def sub_locked(text, motif, remplace, n, label):
    c = text.count(motif)
    if c != n:
        print("ABANDON : motif [%s] trouvé %d fois (attendu %d) : %r" % (label, c, n, motif[:70]))
        sys.exit(2)
    return text.replace(motif, remplace)


def main():
    t = open(PM_INSTALL, encoding="utf-8").read()

    # 1. Version
    t = sub_locked(t, "Version : 1.7.2", "Version : 1.8.0", 1, "version")

    # 2. En-tête — ligne « Complète » étendue
    t = sub_locked(t,
        "+ critères de passage (§3).",
        "+ critères de passage (§3) + MÉCANISME DUAL d'installation (v1.8.0, §3.2 : installation directe des formes certifiées du dépôt par défaut — exécutant canonique `scripts/eco_install_pipeline.py` ; assemblage depuis les PMs = voie bootstrap corpus-seul) + intégration du registre d'alias `alias-eco` au périmètre (v1.8.0 : §2bis/§4/§A.3).",
        1, "en-tête Complète")

    # 3. §1 principe 2 — authentification de la SOURCE (dual)
    t = sub_locked(t,
        "2. **Rien ne s'installe depuis un corpus non authentifié** — les formes installées sont assemblées DEPUIS les PMs ; si le corpus est corrompu, tout le reste l'est → intégrité en étape 2.",
        "2. **Rien ne s'installe depuis une source non authentifiée** — installation directe (v1.8.0, §3.2-a) : les formes certifiées du DÉPÔT (garde R2 + arbitres) ; bootstrap (§3.2-b) : les formes installées sont assemblées DEPUIS les PMs du corpus authentifié (archive scellée) ; si la source est corrompue, tout le reste l'est → intégrité en étape 2.",
        1, "§1 principe 2")

    # 4. §2 — note mécanisme dual après la table du pipeline
    t = sub_locked(t,
        "Note (correct-work CIBLE, 2026-09-06, S3 ; révisée session A9, 2026-09-06) :",
        "Note (mécanisme dual, v1.8.0 — directive propriétaire « PM INSTALL assemble au lieu d'installer ») : les étapes 3-6 s'exécutent par **installation DIRECTE des formes certifiées du dépôt** (voie par défaut, §3.2-a) ; la colonne « Source → Destination » de la table décrit la **voie bootstrap** (§3.2-b, assemblage depuis les PMs — environnement nu, corpus/archive seul). Réponse à la question propriétaire : l'assemblage a historiquement garanti l'unique source de vérité (R4), l'authenticité (archive scellée) et la portabilité (le corpus suffit à tout reconstruire) ; depuis KO-L004 v1.1.0 la direction de génération est SKILL.md → PM (le PM est dérivé mécaniquement) et le dépôt porte les formes certifiées par les arbitres — l'installation directe est donc devenue la voie la plus judicieuse quand le dépôt est disponible, l'assemblage demeurant la voie bootstrap équivalente.\n\nNote (correct-work CIBLE, 2026-09-06, S3 ; révisée session A9, 2026-09-06) :",
        1, "§2 note dual")

    # 5. §3.2 — réécriture mécanisme dual
    t = sub_locked(t,
        "### §3.2 Étapes 3-6 — Assemblage des formes installées\nLes SKILL.md sont ASSEMBLÉS depuis les PMs (jamais copiés à l'aveugle) : YAML frontmatter (§4 du PM) + règle zéro + spécifications (§1-§2) + relations (§3) + sections spécifiques.",
        "### §3.2 Étapes 3-6 — Mécanisme dual : installation directe (défaut) / assemblage (bootstrap)\n\n**(a) Installation DIRECTE — voie PAR DÉFAUT (v1.8.0)** : lorsque le dépôt est disponible (clone git local, règle d'or n°4), les étapes 3-6 copient telles quelles les **formes installées certifiées** du dépôt (`skills/<famille>/` + `skills/<skill>/` du registre KB — SKILL.md, references/, evals/, scripts/), certifiées par les arbitres de l'étape 9 ; la **garde R2 anti-rétrogradation** s'applique (jamais de version inférieure à la forme installée existante) et la **garde d'authenticité** demeure (le dépôt est vérifié au pin descendant-tolérant, l'archive round-trip à l'étape 2). Exécutant canonique : `scripts/eco_install_pipeline.py` (sync union + garde R2 + rescellement archive), versionné au dépôt.\n\n**(b) Assemblage depuis les PMs — voie BOOTSTRAP (corpus/archive seul)** : les SKILL.md sont ASSEMBLÉS depuis les PMs (jamais copiés à l'aveugle) : YAML frontmatter (§4 du PM) + règle zéro + spécifications (§1-§2) + relations (§3) + sections spécifiques — les §5 des 4 PMs familles demeurent la SPÉCIFICATION de la forme installée (la voie (a) copie exactement ce que la voie (b) reconstruit ; les deux produisent des formes byte-identiques).",
        1, "§3.2 dual")

    # 6. §2bis — fermeture MINIMALE += alias-eco
    t = sub_locked(t,
        "`skill-finder-cn` (fallback §1.16 gen-plan v3.21.0) ;",
        "`skill-finder-cn` (fallback §1.16 gen-plan v3.21.0), `alias-eco` (registre des phrases récurrentes $<ALIAS> — délégation correct-work v2.8.0, registre `@historique/@Alias/`) ;",
        1, "§2bis alias-eco")

    # 7. §4 — interaction correct-work -> alias-eco
    t = sub_locked(t,
        "| gen-plan —délègue→ prompt-engineering | 0-11 | Optimisation fine des prompts |",
        "| gen-plan —délègue→ prompt-engineering | 0-11 | Optimisation fine des prompts |\n| correct-work —délègue→ alias-eco | 4, 9(b) | Mode PROJET — tenue du registre des phrases récurrentes de la discussion analysée (v1.8.0) |",
        1, "§4 alias-eco")

    # 8. §A.3 — instantané + extensions += alias-eco
    t = sub_locked(t,
        "Instantané courant (v1.7.1, 2026-10-12) : gen-plan v3.23.2 · correct-work v2.8.0 · clone-chat v2.0.2 · refactor-guard v1.7.1 — cf. §2ter.",
        "Instantané courant (v1.8.0, 2026-10-23) : gen-plan v3.23.2 · correct-work v2.8.0 · clone-chat v2.0.2 · refactor-guard v1.7.1 — cf. §2ter.",
        1, "§A.3 instantané")
    t = sub_locked(t,
        "| refactor-guard | v1.7.0 |",
        "| refactor-guard | v1.7.0 |\n| alias-eco | v1.0.0 |",
        1, "§A.3 extensions alias-eco")

    # 9. §7 — historique v1.8.0
    anchor = "\n| v1.7.2 | "
    if t.count(anchor) < 1:
        print("ABANDON : ancre historique v1.7.2 introuvable")
        sys.exit(2)
    idx = t.index(anchor)
    row = ("\n| v1.8.0 | 2026-10-23 | Directive propriétaire (session web-fdf5963c, Task 18 — "
           "« optimise le système d'installation en regénérant, toutes disciplines et refactoring » "
           "+ prérequis A « assemble au lieu d'installer ») : MÉCANISME DUAL d'installation codifié "
           "— §3.2 réécrit : (a) installation DIRECTE des formes certifiées du dépôt = voie PAR "
           "DÉFAUT (exécutant canonique scripts/eco_install_pipeline.py — chemin REPO paramétrable, "
           "pin descendant-tolérant), (b) assemblage depuis les PMs = voie BOOTSTRAP (les §5 des PMs "
           "demeurent la spécification de la forme — 4 PMs familles régénérés mécaniquement KO-L004 "
           "avec note §5 mécanisme dual : gen-plan v3.23.2, correct-work v2.8.0, clone-chat v2.0.2, "
           "refactor-guard v1.7.1) ; intégration alias-eco (skill v1.0.0 — registre d'alias "
           "$<ALIAS>, déclencheurs « alias-eco »/« liste mes alias »/« alias-eco (chat) », registre "
           "JSON @historique/@Alias/, délégation correct-work v2.8.0 mode PROJET) au périmètre "
           "(§2bis, §4, §A.3) ; §1 #2 et §2 recalibrés |")
    t = t[:idx] + row + t[idx:]

    with open(PM_INSTALL, "w", encoding="utf-8") as f:
        f.write(t)
    print("PM-INSTALL v1.8.0 écrit — 10 substitutions verrouillées")
    return 0


if __name__ == "__main__":
    sys.exit(main())
