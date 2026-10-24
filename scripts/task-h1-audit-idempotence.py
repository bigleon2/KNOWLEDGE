#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.13)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# PROVENANCE: session web-f90062ce (2026-10-24) — tâche H1 (directive propriétaire
# en suspens, tracée worklog H3 « Reste à faire ») : « audit de conformité
# idempotente des skills/agents/scripts + réécriture idempotente des non-
# conformes ».
# NORME DÉFINIE AVANT AUDIT (mesurable, jamais ajustée aux résultats — KO-L003) :
#   Un élément est CONFORME si son rejeu ×2 produit le même état final observable
#   (fichiers, registres, dépôt) que son exécution unique.
#   - LECTURE_SEULE          : aucun effet de bord → conforme par nature
#   - EFFETS_GARDES          : effets de bord + gardes d'idempotence détectées
#                              (lecture/comparaison avant écriture, exists(), hash,
#                              skip si identique, dry-run/--check) → conforme
#   - EFFETS_NON_GARDES      : effets de bord SANS garde détectée → NON CONFORME
#   - IRREVERSIBLE_PAR_DESIGN: effets irréversibles par conception (git push,
#                              purge) → conformité = garde anti-double-effet
# Méthode : analyseur AST Python (effets/gardes) + heuristiques textuelles
# .sh/.js/.ts + déclarations pour SKILL.md/.agent. Classification PUIS revue
# manuelle avant toute réécriture (jamais de patch aveugle).
# Idempotence de l'outil lui-même : rapport écrit seulement si contenu différent.
"""H1 — audit de conformité idempotente des skills/agents/scripts (dépôt)."""
import ast
import json
import hashlib
import re
import sys
from pathlib import Path

REPO = Path("/home/z/my-project/KNOWLEDGE-repo")
OUT = REPO / "scripts" / "task-h1-audit-idempotence.json"
EXCLUS = ("@historique",)  # archives figées R2/R4 — jamais réécrites, hors audit vivant

# --- Python AST : nœuds d'effet (écriture/modification) ---
PY_OPEN_WRITE = re.compile(r"^[wax]")


class Analyseur(ast.NodeVisitor):
    """Collecte effets et gardes d'un arbre Python."""

    EFF_OPEN_W = "open(mode écriture)"
    EFF_PATH_WRITE = "Path.write_text/write_bytes"
    EFF_PATH_MKDIR = "Path.mkdir"
    EFF_PATH_RENAME = "Path.rename/replace"
    EFF_PATH_UNLINK = "Path.unlink/touch"
    EFF_OS_FS = "os.rename/replace/remove/mkdir/makedirs/chmod"
    EFF_SHUTIL = "shutil.rmtree/copy/copytree/move"
    EFF_GIT_WRITE = "git commit/push/mv/rm/checkout/reset/clean/stash/apply/rebase/merge"
    GARDE_LECTURE = "open(mode lecture)"
    GARDE_EXISTS = "exists()/is_file()/is_dir()"
    GARDE_CMP_CONTENU = "comparaison contenu lu (== / !=)"
    GARDE_HASH = "comparaison hash (sha256/md5)"
    GARDE_DRYRUN = "dry-run / --check / no-op"

    def __init__(self):
        self.effets = set()
        self.gardes = set()

    # -- effets --
    def visit_Call(self, node):
        f = node.func
        name = self._qname(f)
        # open(path, 'w'/'a'/...)
        if name == "open" and len(node.args) >= 2:
            mode = self._const(node.args[1])
            if isinstance(mode, str) and PY_OPEN_WRITE.match(mode):
                self.effets.add(self.EFF_OPEN_W)
            elif isinstance(mode, str):
                self.gardes.add(self.GARDE_LECTURE)
        # Path.write_text / write_bytes / mkdir / rename / replace / unlink / touch
        if name in ("write_text", "write_bytes"):
            self.effets.add(self.EFF_PATH_WRITE)
        if name == "mkdir":
            self.effets.add(self.EFF_PATH_MKDIR)
        if name in ("rename", "replace") and "." not in name:
            self.effets.add(self.EFF_PATH_RENAME)
        if name in ("unlink", "touch"):
            self.effets.add(self.EFF_PATH_UNLINK)
        if name in ("exists", "is_file", "is_dir"):
            self.gardes.add(self.GARDE_EXISTS)
        # os.* / shutil.*
        if name.startswith("os.") and name.split(".")[-1] in (
                "rename", "replace", "remove", "unlink", "mkdir", "makedirs", "chmod"):
            self.effets.add(self.EFF_OS_FS)
        if name.startswith("shutil.") and name.split(".")[-1] in (
                "rmtree", "copy", "copy2", "copytree", "move"):
            self.effets.add(self.EFF_SHUTIL)
        # subprocess git écriture (run/check_output/Popen avec liste contenant git)
        if name in ("run", "check_output", "check_call", "Popen", "call"):
            for a in node.args:
                if isinstance(a, (ast.List, ast.Tuple)):
                    mots = {self._const(e) for e in a.elts if isinstance(e, ast.Constant)}
                    if "git" in mots and mots & {"commit", "push", "mv", "rm", "clean",
                                                 "stash", "apply", "rebase", "merge"}:
                        self.effets.add(self.EFF_GIT_WRITE)
                    if "git" in mots and mots & {"checkout", "reset"}:
                        self.effets.add(self.EFF_GIT_WRITE)
        # sursis : print ne compte pas
        self.generic_visit(node)

    # -- gardes : comparaisons de contenu lu --
    def visit_Compare(self, node):
        gauche, droite = node.left, node.comparators[0] if node.comparators else None
        for cote in (gauche, droite):
            if self._lit_contenu(cote):
                self.gardes.add(self.GARDE_CMP_CONTENU)
        self.generic_visit(node)

    def visit_Assert(self, node):
        # assert == contenu : garde faible (vérification), comptée
        self.generic_visit(node)

    # -- helpers --
    @staticmethod
    def _qname(f):
        if isinstance(f, ast.Name):
            return f.id
        if isinstance(f, ast.Attribute):
            base = f.value
            parts = []
            while isinstance(base, ast.Attribute):
                parts.append(base.attr)
                base = base.value
            if isinstance(base, ast.Name):
                parts.append(base.id)
            return ".".join(reversed(parts)) + "." + f.attr if parts else f.attr
        return getattr(f, "attr", "?") if isinstance(f, ast.Attribute) else "?"

    @staticmethod
    def _const(n):
        return n.value if isinstance(n, ast.Constant) else None

    def _lit_contenu(self, n):
        if isinstance(n, ast.Call):
            qn = self._qname(n.func)
            return qn in ("read", "read_text", "read_bytes", "readline", "readlines")
        return False


def audit_python(p: Path):
    try:
        tree = ast.parse(p.read_text(encoding="utf-8", errors="replace"))
    except SyntaxError:
        return None, None, None
    src = p.read_text(encoding="utf-8", errors="replace")
    an = Analyseur()
    an.visit(tree)
    effets, gardes = an.effets, an.gardes
    if any(e == Analyseur.EFF_GIT_WRITE for e in effets) and not gardes:
        cat = "IRREVERSIBLE_PAR_DESIGN"
    elif not effets:
        cat = "LECTURE_SEULE"
    elif effets and gardes:
        cat = "EFFETS_GARDES"
    else:
        cat = "EFFETS_NON_GARDES"
    # garde dry-run textuelle (flags argparse)
    if "dry" in src or "--check" in src or "DRY_RUN" in src or "dry_run" in src:
        gardes = gardes | {Analyseur.GARDE_DRYRUN}
        if cat == "EFFETS_NON_GARDES":
            cat = "EFFETS_GARDES"
    return cat, sorted(effets), sorted(gardes)


# --- heuristiques shell / js / ts ---
def audit_sh(p: Path):
    src = p.read_text(encoding="utf-8", errors="replace")
    effets, gardes = set(), set()
    if re.search(r"\b rm\b|\bmv \b|\bcp \b|\bmkdir\b|\brmdir\b", src):
        effets.add("fs shell (rm/mv/cp/mkdir)")
    if re.search(r"(?<!>)>(?!>)", "\n".join(l for l in src.splitlines()
                                             if not l.strip().startswith("#"))):
        effets.add("redirection écrasement (>)")
    if re.search(r"git (push|commit|mv|rm|clean|stash|apply|rebase|merge)\b", src):
        effets.add("git écriture")
    if re.search(r"\[ -f |\[ ! -f |\[ -e |\bcmp\b|\bdiff\b|\bmd5sum\b|\bsha256sum\b|grep -q", src):
        gardes.add("garde shell (test -f/cmp/diff/hash)")
    if not effets:
        return "LECTURE_SEULE", sorted(effets), sorted(gardes)
    return ("EFFETS_GARDES" if gardes else "EFFETS_NON_GARDES"), sorted(effets), sorted(gardes)


def audit_js(p: Path):
    src = p.read_text(encoding="utf-8", errors="replace")
    effets, gardes = set(), set()
    if re.search(r"writeFileSync|appendFileSync|rmSync|rmdirSync|renameSync|mkdirSync|copyFileSync|truncateSync", src):
        effets.add("fs sync écriture")
    if re.search(r"\.write\(|\.createWriteStream|fs\.promises\.(writeFile|rename|rm|mkdir)", src):
        effets.add("fs async écriture")
    if re.search(r"existsSync|statSync|readFileSync", src):
        gardes.add("lecture/exists avant écriture")
    if not effets:
        return "LECTURE_SEULE", sorted(effets), sorted(gardes)
    return ("EFFETS_GARDES" if gardes else "EFFETS_NON_GARDES"), sorted(effets), sorted(gardes)


def audit_skill_md(p: Path):
    """SKILL.md : conformité = déclaration/garantie d'idempotence quand le skill
    porte des scripts écrivants ou un processus d'écriture."""
    src = p.read_text(encoding="utf-8", errors="replace")
    scripts_dir = p.parent / "scripts"
    ecrit = False
    if scripts_dir.is_dir():
        for s in scripts_dir.rglob("*"):
            if s.suffix in (".py", ".sh", ".js", ".mjs", ".ts"):
                try:
                    src_s = s.read_text(encoding="utf-8", errors="replace")
                except OSError:
                    continue
                if re.search(r"open\([^)]*,\s*['\"][wa]|write_text|write_bytes|writeFileSync"
                             r"|shutil\.(copy|rmtree|move)|os\.(rename|replace|remove)", src_s):
                    ecrit = True
                    break
    if not ecrit and not re.search(r"écrit|réécrit|modifie|génère|crée", src, re.I):
        return "LECTURE_SEULE", [], []
    declares = bool(re.search(r"idempoten", src, re.I))
    if declares or not ecrit:
        return ("EFFETS_GARDES" if ecrit else "EFFETS_GARDES"), \
               (["scripts écrivants"] if ecrit else ["processus documenté d'écriture"]), \
               (["idempotence déclarée"] if declares else ["aucun script écrivant"])
    return "EFFETS_NON_GARDES", ["scripts écrivants"], []


def audit_agent(p: Path):
    src = p.read_text(encoding="utf-8", errors="replace")
    declares = bool(re.search(r"idempoten|rejeu|no-op", src, re.I))
    return ("EFFETS_GARDES" if declares else "EFFETS_NON_GARDES"), ["agent à états"], \
           (["rejeu garanti"] if declares else [])


def main():
    fichiers = []
    for p in sorted(REPO.rglob("*")):
        rel = p.relative_to(REPO).as_posix()
        if not p.is_file():
            continue
        if any(x in rel for x in EXCLUS) or rel.startswith("download/"):
            continue
        if p.suffix == ".py":
            cat, eff, gar = audit_python(p)
            famille = "script-python"
        elif p.suffix == ".sh":
            cat, eff, gar = audit_sh(p); famille = "script-shell"
        elif p.suffix in (".js", ".mjs", ".ts"):
            cat, eff, gar = audit_js(p); famille = "script-js"
        elif p.name == "SKILL.md":
            cat, eff, gar = audit_skill_md(p); famille = "skill"
        elif p.suffix == ".agent":
            cat, eff, gar = audit_agent(p); famille = "agent"
        else:
            continue
        if cat is None:  # syntax error python
            fichiers.append({"fichier": rel, "famille": famille,
                             "categorie": "NON_ANALYSABLE", "effets": [], "gardes": []})
            continue
        fichiers.append({"fichier": rel, "famille": famille, "categorie": cat,
                         "effets": eff, "gardes": gar})

    # classification vivant vs one-shot (préfixes de tâches de session)
    one_shot = re.compile(r"/task[\w-]*[-_]|PA-TEST|task\d+")
    stats = {}
    for f in fichiers:
        f["usage"] = "one-shot" if one_shot.search(f["fichier"]) else "vivant"
        stats[f["categorie"]] = stats.get(f["categorie"], 0) + 1

    non_conformes = [f for f in fichiers if f["categorie"] == "EFFETS_NON_GARDES"]
    rapport = {
        "type": "audit-conformite-idempotence",
        "tache": "H1 — audit de conformité idempotente des skills/agents/scripts",
        "norme": ("CONFORME = rejeu ×2 produit le même état final observable "
                  "(fichiers, registres, dépôt) que l'exécution unique"),
        "perimetre": {"python": sum(1 for f in fichiers if f["famille"] == "script-python"),
                      "shell": sum(1 for f in fichiers if f["famille"] == "script-shell"),
                      "js_ts": sum(1 for f in fichiers if f["famille"] == "script-js"),
                      "skills": sum(1 for f in fichiers if f["famille"] == "skill"),
                      "agents": sum(1 for f in fichiers if f["famille"] == "agent")},
        "stats": stats,
        "non_conformes": non_conformes,
        "fichiers": fichiers,
    }

    # idempotence de l'outil : n'écrire le rapport que s'il diffère
    contenu = json.dumps(rapport, ensure_ascii=False, indent=2)
    if OUT.exists() and OUT.read_text(encoding="utf-8") == contenu:
        print("rapport inchangé (no-op idempotent)")
    else:
        OUT.write_text(contenu, encoding="utf-8")
        print("rapport écrit")

    print(f"périmètre : {rapport['perimetre']}")
    print(f"stats : {stats}")
    print(f"non-conformes : {len(non_conformes)} "
          f"(dont vivants : {sum(1 for f in non_conformes if f['usage'] == 'vivant')})")
    for f in non_conformes:
        print(f"  [NON CONFORME][{f['usage']}] {f['fichier']} — effets: {', '.join(f['effets'])}")
    # exits 0 si audité ; le verdict de conformité est dans le rapport
    return 0


if __name__ == "__main__":
    sys.exit(main())
