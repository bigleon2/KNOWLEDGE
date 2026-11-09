#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.37)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).
"""

"""task72-delta-v3390.py — Construction MÉCANIQUE du delta verrouillé de la montée
gen-plan v3.38.0 → v3.39.0 (Task 72 G1/SG1.4 — cascade KO-L004).

Méthode B1 (substitutions verrouillées — generer-pm-skill.py) :
  - chaque `old` est extrait PAR PROGRAMME du PM v3.38.0 (aucune copie manuelle) ;
  - chaque `new` est extrait du SKILL.md v3.39.0 (post-amendement SG1.3bis) ou des
    fichiers references/ réels (in extenso) — le script n'invente RIEN (KO-L003) ;
  - vérification count==1 de chaque old dans le PM AVANT écriture du delta ;
  - sortie : scripts/delta-genplan-v3390.json (format history+subs, calé sur
    delta-genplan-v3380.json).

Transformations :
  1. §1.8 Règles d'or       → résumé compact SKILL §1.5 (intégral → §9.8)
  2. §1.9 Disciplines       → résumé compact SKILL §1.6 (intégral → §9.9)
  3. §1.12 Hooks patterns   → résumé compact SKILL §1.2bis (intégral → §9.10)
  4. §1.16 Routage/garde    → résumé compact SKILL §1.16 (intégral → §9.10)
  5. §2.2 arbre             → arbre à jour SKILL (15 références, adapté {{SKILLS_ROOT}})
  6. §4 description YAML    → + ligne progressive disclosure (miroir frontmatter SKILL)
  7. §5.2/§5.3/§9 intro     → lags résorbés (nb lignes, pointeur §9, nb fichiers 10)
  8. §9.2 grille-token      → fichier courant (append contingences v3.39.0)
  9. queue §9.6             → + §9.7-§9.10 (4 nouveaux fichiers in extenso)
 10. history                → ligne v3.39.0 pour la table §7 (insérée par le générateur)

Aucune duplication intra-PM : les intégraux vivent UNE fois en §9 (in extenso),
les §1.8/§1.9/§1.12/§1.16 deviennent les résumés compacts (miroirs du SKILL.md).
"""
import json
import sys
from pathlib import Path

RACINE = Path("/home/z/my-project")
CORPUS = RACINE / "skills" / "@mon-ecosysteme"
PM = CORPUS / "PROMPT-MAITRE-GEN-PLAN-v3.38.0.md"
SKILL = RACINE / "skills" / "gen-plan" / "SKILL.md"
REFS = RACINE / "skills" / "gen-plan" / "references"
SORTIE = RACINE / "scripts" / "delta-genplan-v3390.json"


def span_par_lignes(texte: str, debut: str, fin: str) -> str:
    """Span [debut, fin) : de la ligne contenant debut (incluse) à la ligne
    contenant fin (exclue). Abandon si marqueur introuvable ou ambigu."""
    lignes = texte.splitlines()
    idx = [i for i, l in enumerate(lignes) if debut in l]
    if len(idx) != 1:
        raise SystemExit(f"ABANDON : marqueur début {debut!r} trouvé {len(idx)} fois")
    i0 = idx[0]
    rest = [i for i in range(i0, len(lignes)) if fin in lignes[i]]
    if not rest:
        raise SystemExit(f"ABANDON : marqueur fin {fin!r} introuvable après début")
    return "\n".join(lignes[i0:rest[0]]) + "\n"


def ligne_unique(texte: str, motif: str) -> str:
    lignes = [l for l in texte.splitlines() if motif in l]
    if len(lignes) != 1:
        raise SystemExit(f"ABANDON : ligne {motif!r} trouvée {len(lignes)} fois (attendu 1)")
    return lignes[0]


def fence(nom: str, contenu: str) -> str:
    """Section in extenso au format §9 : ### §9.x `references/<nom>` + fence markdown."""
    corps = contenu.rstrip("\n")
    return f"### §9.{nom} "


def main() -> int:
    pm = PM.read_text(encoding="utf-8")
    sk = SKILL.read_text(encoding="utf-8")

    # ---- Spans PM (old) — extraits du fichier réel --------------------------
    pm_18 = span_par_lignes(pm, "### §1.8 Règles d'or", "### §1.9 Disciplines")
    pm_19 = span_par_lignes(pm, "### §1.9 Disciplines", "### §1.10 Pipeline")
    pm_112 = span_par_lignes(pm, "### §1.12 Hooks patterns", "### §1.12bis")
    pm_116 = span_par_lignes(pm, "### §1.16 Routage", "## §2 — ")
    pm_22 = span_par_lignes(pm, "### §2.2 Structure", "### §2.3")
    pm_92 = span_par_lignes(pm, "### §9.2 `references/grille-token.md`", "### §9.3")
    pm_l_52 = ligne_unique(pm, "Le fichier `SKILL.md` (~")
    pm_l_53 = ligne_unique(pm, "Le contenu in extenso de chaque fichier est en")
    pm_l_9intro = ligne_unique(pm, "fichiers référence suivants doivent être créés")
    # queue : dernière phrase de la Note d'intégration PEK + fence fermante
    lignes_pm = pm.splitlines()
    queue_note = [l for l in lignes_pm if l.startswith("**Note d'intégration**")]
    if len(queue_note) != 1 or lignes_pm[-1] != "```":
        raise SystemExit("ABANDON : queue PM inattendue (Note d'intégration / fence)")
    pm_queue = "L'implémentation de référence reste documentée dans l'archive source (upload/pek-v4.1.zip).\n```"
    if pm.count(pm_queue) != 1:
        raise SystemExit("ABANDON : ancre de queue introuvable ou ambiguë")

    # ---- Spans SKILL (new) — extraits du fichier réel post-amendement --------
    sk_12bis = span_par_lignes(sk, "### §1.2bis Hooks patterns", "### §1.3 Normes")
    sk_15 = span_par_lignes(sk, "### §1.5 Règles d'or", "### §1.6 Disciplines")
    sk_16 = span_par_lignes(sk, "### §1.6 Disciplines", "### §1.7 Pipeline")
    sk_116 = span_par_lignes(sk, "### §1.16 Routage", "## §2 — ")
    sk_22 = span_par_lignes(sk, "### §2.2 Structure", "### §2.3")
    sk_desc_tail = ligne_unique(sk, "progressive disclosure R1 (v3.39.0)")
    pm_desc_tail = ligne_unique(pm, "glossaire alias-eco inline $FACON/$FACON2 (§A — auto-contenu, v3.37.0)")
    nb_lignes_sk = len(sk.splitlines())

    # ---- Adaptations d'en-tête (numérotation PM + pointeur §9) --------------
    def adapte_header(span: str, old_h: str, new_h: str) -> str:
        if span.count(old_h) != 1:
            raise SystemExit(f"ABANDON : en-tête {old_h!r} introuvable dans le span SKILL")
        return span.replace(old_h, new_h, 1)

    new_18 = adapte_header(
        sk_15,
        "### §1.5 Règles d'or (résumé opérationnel — intégral : `references/regles-or.md` ; miroir SHARED §9)",
        "### §1.8 Règles d'or (résumé opérationnel — intégral : §9.8 `references/regles-or.md` ; miroir SHARED §9)")
    new_19 = adapte_header(
        sk_16,
        "### §1.6 Disciplines d'ingénierie de prompts (résumé — tables intégrales : `references/disciplines-mobilisation.md`)",
        "### §1.9 Disciplines d'ingénierie de prompts (résumé — tables intégrales : §9.9 `references/disciplines-mobilisation.md`)")
    new_112 = adapte_header(
        sk_12bis,
        "### §1.2bis Hooks patterns avancés (v3.13.0, phase N20)",
        "### §1.12 Hooks patterns avancés (v3.13.0, phase N20 — résumés compacts, intégraux : §9.10 `references/protocoles-detailles.md`)")
    new_116 = adapte_header(
        sk_116,
        "### §1.16 Routage de découverte des skills + garde d'installation (résumé — intégral : `references/protocoles-detailles.md`)",
        "### §1.16 Routage de découverte des skills + garde d'installation (résumé — intégral : §9.10 `references/protocoles-detailles.md`)")
    # arbre : préfixe {{SKILLS_ROOT}} (convention PM)
    if sk_22.count("skills/gen-plan/") < 1:
        raise SystemExit("ABANDON : racine arbre SKILL introuvable")
    new_22 = sk_22.replace("skills/gen-plan/", "{{SKILLS_ROOT}}gen-plan/", 1)

    # ---- §9.7-§9.10 : in extenso (fichiers réels, verbatim) -----------------
    def extenso(num: int, nom_fichier: str) -> str:
        contenu = (REFS / nom_fichier).read_text(encoding="utf-8")
        if "```" in contenu:
            raise SystemExit(f"ABANDON : {nom_fichier} contient des fences internes")
        return (f"### §9.{num} `references/{nom_fichier}`\n\n"
                f"```markdown\n{contenu.rstrip(chr(10))}\n```\n")

    # grille-token : fichier auto-clôturé (```markdown l.1, ``` l.63) + append
    # contingences → embed VERBATIM (le fichier porte sa propre présentation)
    grille = (REFS / "grille-token.md").read_text(encoding="utf-8")
    new_92 = f"### §9.2 `references/grille-token.md`\n\n{grille.rstrip(chr(10))}\n"

    blocs_extenso = (
        "\n" + extenso(7, "journal-versions.md")
        + "\n" + extenso(8, "regles-or.md")
        + "\n" + extenso(9, "disciplines-mobilisation.md")
        + "\n" + extenso(10, "protocoles-detailles.md"))

    # ---- Subs ---------------------------------------------------------------
    subs = [
        {"old": pm_18, "new": new_18, "count": 1},
        {"old": pm_19, "new": new_19, "count": 1},
        {"old": pm_112, "new": new_112, "count": 1},
        {"old": pm_116, "new": new_116, "count": 1},
        {"old": pm_22, "new": new_22, "count": 1},
        {"old": pm_92, "new": new_92, "count": 1},
        {"old": pm_desc_tail, "new": pm_desc_tail + "\n" + sk_desc_tail, "count": 1},
        {"old": pm_l_52, "new": f"Le fichier `SKILL.md` (~{nb_lignes_sk} lignes — progressive disclosure v3.39.0 : résumés inline, intégraux en §9) doit contenir :", "count": 1},
        {"old": pm_l_53, "new": "Le contenu in extenso de chaque fichier est en §9.", "count": 1},
        {"old": pm_l_9intro, "new": "Les 10 fichiers référence suivants doivent être créés dans `{{SKILLS_ROOT}}gen-plan/references/` (plus 1 fichier evals). Voici leur contenu intégral.", "count": 1},
        {"old": pm_queue, "new": pm_queue + blocs_extenso, "count": 1},
    ]

    # ---- Vérification count==1 de chaque old AVANT écriture -----------------
    for i, s in enumerate(subs, 1):
        c = pm.count(s["old"])
        if c != s["count"]:
            print(f"ABANDON : sub {i} — old trouvé {c} fois (attendu {s['count']}) "
                  f"[{s['old'][:60]!r}...]")
            return 2

    history = (
        "MINOR re-curation progressive disclosure R1 (directive propriétaire « Chantier R1 : "
        "re-curation progressive disclosure de gen-plan », Task 72 G1 — étude Task 70 R1) + "
        "directives complémentaires 1a1b7b297b7b4975 (skill re-curation implémenté d'un script — "
        "plan Task 72 : tests AVANT re-curation, protocole-test.py PRE/POST/--compare) et "
        "1a1b7fe1c7238e8d (fenêtre native AFFICHE-PLAN) : 9 blocs déplacés R4 byte-identité vers "
        "references/ (journal-versions · regles-or [+ leçons KO] · disciplines-mobilisation · "
        "protocoles-detailles) + append contingences grille-token.md — résumés NOUVEAUX inline "
        "(SKILL.md 104,0 → 29,95 Kio, −71,2 % #token, CRITIQUE → INTERMÉDIAIRE) ; contrats "
        "baseline golden master D001-D005 PASS (task72-baseline-verifier.py, re-vérifiés "
        "post-amendement) ; E7-DISP point 6 « fenêtre native » : la fenêtre des étapes du plan "
        "s'affiche via le mécanisme natif de l'agent dédié à ce rôle (Z.ai : liste de tâches "
        "TodoWrite/TodoRead) au début de l'exécution du plan d'actions + mise à jour à chaque "
        "fin d'étape (canal supplémentaire — bloc chat, marqueur worklog PLAN-AFFICHE et garde "
        "check_plan_protocol.py P1-P5 inchangés) ; PM : §1.8/§1.9/§1.12/§1.16 → résumés compacts "
        "miroirs du SKILL.md, intégraux reportés in extenso en §9.7-§9.10 (aucune duplication "
        "intra-PM), §9.2 grille-token à jour (append contingences), description + progressive "
        "disclosure, lags §5.2/§5.3/§9 résorbés.")

    delta = {"history": history, "subs": subs}
    SORTIE.write_text(json.dumps(delta, ensure_ascii=False, indent=1), encoding="utf-8")

    # Rapport
    total_old = sum(len(s["old"].encode()) for s in subs)
    total_new = sum(len(s["new"].encode()) for s in subs)
    print(f"DELTA écrit : {SORTIE} ({SORTIE.stat().st_size} octets)")
    print(f"  subs : {len(subs)} — old {total_old} o → new {total_new} o "
          f"(delta PM estimé {total_new - total_old:+d} o)")
    for i, s in enumerate(subs, 1):
        print(f"  sub {i:>2} : old {len(s['old'].encode()):>6} o → new {len(s['new'].encode()):>6} o")
    print(f"  history : {len(history.encode())} o")
    return 0


if __name__ == "__main__":
    sys.exit(main())
