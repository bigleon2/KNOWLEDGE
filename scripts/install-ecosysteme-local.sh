#!/bin/bash
# ============================================================================
# install-ecosysteme-local.sh — Pipeline PM-INSTALL v1.7.1 (§2, 11 étapes)
# Profil local : /home/z/my-project  ({{SKILLS_ROOT}} = skills/)
# Deux modes (F3 — ré-ancrage post-résorption du clone éphémère) :
#   MODE CLONE (source externe) : bash install-ecosysteme-local.sh <chemin-clone>
#       — réinstallation complète depuis un clone certifié (ex. re-clone avec PAT frais)
#   MODE AUTONOME (défaut sans clone) : réparation du corpus ET des piliers (manquant OU
#       SHA divergent) via archive v2.3 + garde SHA de l'archive vs manifeste scellé
#       (F4/F5) + contrôle SHA des 32 SKILL.md vs manifeste + arbitre integrity (68 contrôles)
#       ; dérives résiduelles = source externe requise.
# Idempotent : ré-exécution = no-op si l'état est déjà conforme.
# ============================================================================
set -u
LOCAL="/home/z/my-project"
REPO="${1:-$LOCAL/KNOWLEDGE-repo}"
ARCHIVE="$LOCAL/download/mon-ecosysteme_archive.zip"
SK="$LOCAL/skills"
TS=$(date '+%Y-%m-%d %H:%M:%S')
echo "=== INSTALLATION ÉCOSYSTÈME KNOWLEDGE — $TS ==="

# --- Routage de mode (F3) : sans clone, le profil se vérifie/répare seul ---
if [ ! -d "$REPO" ]; then
  echo "--- MODE AUTONOME (clone absent : $REPO) — F3/F4/F5 ---"
  python3 - "$LOCAL" "$ARCHIVE" <<'PYEOF'
import hashlib, json, subprocess, sys, zipfile
from pathlib import Path
local, archive = Path(sys.argv[1]), Path(sys.argv[2])
corpus = local / "skills" / "@mon-ecosysteme"
tmp = local / "scripts" / "outputs" / ".selfrestore-tmp"
# F5 — piliers scellés dans l'archive v2.3 (préfixe piliers/) → réparation autonome
PILIERS = {
    "piliers/skills/gen-plan/SKILL.md": "skills/gen-plan/SKILL.md",
    "piliers/skills/correct-work/SKILL.md": "skills/correct-work/SKILL.md",
    "piliers/skills/KNOWLEDGE.md": "skills/KNOWLEDGE.md",
    "piliers/scripts/certification-complete.py": "scripts/certification-complete.py",
    "piliers/scripts/check-ecosysteme-integrity.py": "scripts/check-ecosysteme-integrity.py",
    "piliers/scripts/install-ecosysteme-local.sh": "scripts/install-ecosysteme-local.sh",
}
SELF = "piliers/scripts/install-ecosysteme-local.sh"
derives = []  # dérives résiduelles post-réparation — non réparables en autonome
try:
    mani = json.loads((local / "scripts" / "ecosysteme-integrity.json").read_text(encoding="utf-8"))
    att = mani.get("corpus", {})
except Exception as exc:
    print(f"  ⚠ manifeste illisible ({exc}) — réparation indisponible")
    att, rep = {}, 0
else:
    rep = 0
    saine = archive.exists()
    if not saine:
        print("  ⚠ archive absente — réparation corpus/piliers indisponible")
    else:
        sha_att = mani.get("download", {}).get("mon-ecosysteme_archive.zip")
        if sha_att and hashlib.sha256(archive.read_bytes()).hexdigest() != sha_att:
            saine = False
            print("  ⚠ archive DIVERGENTE du manifeste scellé — réparations refusées (source de vérité compromise)")
    if saine:
        with zipfile.ZipFile(archive) as z:
            noms = set(z.namelist())
            # F5 — réparation des piliers (manquant OU SHA divergent) depuis l'archive v2.3
            for arc, rel in sorted(PILIERS.items()):
                if arc not in noms:
                    continue  # archive v2.2 (sans piliers) — réparation piliers = MODE CLONE
                cible = local / rel
                sha_ref = hashlib.sha256(z.read(arc)).hexdigest()
                sha_loc = hashlib.sha256(cible.read_bytes()).hexdigest() if cible.exists() else None
                if sha_loc == sha_ref:
                    continue
                motif = "manquant" if sha_loc is None else "SHA divergent"
                if arc == SELF:
                    # auto-restauration du réinstallateur en cours d'exécution :
                    # copie détachée APRÈS sortie (on n'écrase jamais le script courant)
                    tmp.parent.mkdir(parents=True, exist_ok=True)
                    tmp.write_bytes(z.read(arc))
                    subprocess.Popen(["sh", "-c", f"sleep 2 && mv -f '{tmp}' '{cible}'"],
                                     start_new_session=True)
                    print(f"  pilier auto-restauré (après sortie) : {rel} ({motif}) — RELANCER le réinstallateur")
                    sys.exit(3)
                cible.parent.mkdir(parents=True, exist_ok=True)
                cible.write_bytes(z.read(arc))
                rep += 1
                print(f"  pilier restauré depuis archive v2.3 : {rel} ({motif})")
            # F4 — réparation corpus élargie : manquant OU SHA divergent → ré-extraction
            for nom, sha_c in att.items():
                cible = corpus / nom
                arc = f"@mon-ecosysteme/{nom}"
                sha_loc = hashlib.sha256(cible.read_bytes()).hexdigest() if cible.exists() else None
                if sha_loc == sha_c:
                    continue
                motif = "manquant" if sha_loc is None else "SHA divergent"
                if arc in noms:
                    z.extract(arc, local / "skills")
                    rep += 1
                    print(f"  corpus restauré depuis archive v2.3 : {nom} ({motif})")
                else:
                    print(f"  ⚠ {nom} {motif} — introuvable dans l'archive")
        # F4 — contrôle SHA des 32 SKILL.md vs manifeste scellé (post-réparation)
        for skill, meta in sorted(mani.get("skills", {}).items()):
            sp = local / "skills" / skill / "SKILL.md"
            if not sp.exists():
                derives.append(f"{skill}/SKILL.md (manquant)")
            elif hashlib.sha256(sp.read_bytes()).hexdigest() != meta.get("sha256"):
                derives.append(f"{skill}/SKILL.md (SHA divergent)")
        print(f"corpus : {len(att)} attendus · piliers : {len(PILIERS)} scellés v2.3 · réparations : {rep}")
        if derives:
            print(f"  ⚠ dérives résiduelles ({len(derives)}) — réparation = MODE CLONE (re-clone PAT frais) :")
            for d in derives:
                print(f"    - {d}")
sys.exit(1 if derives else 0)
PYEOF
  PY_RC=$?
  if [ "$PY_RC" -eq 3 ]; then
    echo "=== MODE AUTONOME : AUTO-RESTAURATION DU RÉINSTALLATEUR PLANIFIÉE — relancer la commande ==="
    exit 3
  fi
  for p in skills/gen-plan/SKILL.md skills/correct-work/SKILL.md skills/KNOWLEDGE.md scripts/certification-complete.py scripts/install-ecosysteme-local.sh; do
    if [ -f "$LOCAL/$p" ]; then echo "  pilier OK : $p"; else echo "  ⚠ pilier ABSENT : $p (réparation = re-clone avec PAT frais + mode clone)"; fi
  done
  echo "--- Arbitre integrity (mode --check, lecture seule) ---"
  if python3 "$LOCAL/scripts/check-ecosysteme-integrity.py" --check; then
    if [ "$PY_RC" -eq 0 ]; then
      echo "=== MODE AUTONOME : ÉTAT CONFORME — aucune source externe requise ==="
      exit 0
    fi
    echo "=== MODE AUTONOME : integrity conforme MAIS dérives SHA piliers/skills — réparation = re-clone avec PAT frais ==="
    exit 1
  fi
  echo "=== MODE AUTONOME : DÉRIVES DÉTECTÉES (voir résumé) ==="
  exit 1
fi
echo "--- MODE CLONE (source : $REPO) — règle d'or n°4 ---"

# --- Étape 1 : Corpus canonique @mon-ecosysteme (9 fichiers, invariant CORPUS_ATTENDU) ---
echo "--- Étape 1 : corpus ---"
mkdir -p "$SK/@mon-ecosysteme"
n_corpus=$(ls -1 "$REPO/skills/@mon-ecosysteme" | wc -l)
cp -p "$REPO/skills/@mon-ecosysteme/"*.md "$SK/@mon-ecosysteme/"
echo "corpus déployé : $n_corpus fichiers (attendu 9)"

# --- Étapes 3-4 : gen-plan v3.23.1 + correct-work v2.7.0 (formes installées du clone certifié) ---
echo "--- Étapes 3-4 : gen-plan + correct-work ---"
rsync -a --delete "$REPO/skills/gen-plan/" "$SK/gen-plan/"
rsync -a --delete "$REPO/skills/correct-work/" "$SK/correct-work/"
echo "gen-plan v$(rg -m1 '^version:' $SK/gen-plan/SKILL.md | rg -o '[\d.]+') · correct-work v$(rg -m1 '^version:' $SK/correct-work/SKILL.md | rg -o '[\d.]+') installés"

# --- Étapes 5-6 : clone-chat v2.0.1 + refactor-guard v1.7.0 (vérif drift, garde R2 : jamais rétrograder) ---
echo "--- Étapes 5-6 : clone-chat + refactor-guard (drift check) ---"
for s in clone-chat refactor-guard; do
  if diff -rq "$REPO/skills/$s" "$SK/$s" >/dev/null 2>&1; then
    echo "$s : byte-identique au clone → no-op idempotent"
  else
    echo "$s : drift détecté → restauration depuis le clone certifié"
    rsync -a --delete "$REPO/skills/$s/" "$SK/$s/"
  fi
done

# --- Drift check : entrées ECO_SKILLS (arbitre) — réparation depuis le clone si divergence ---
echo "--- Drift check ECO_SKILLS ---"
ECO_SKILLS="gen-plan knowledge-observer correct-work clone-chat skills-inventory skill-creator agent-creator script-creator script-reviewer audit-provenance prompt-engineering context-engineering loop-engineering graph-engineering harness-engineering script-mon-ecosysteme-infrastructure audio-metadata cpp-analysis pdf-llm resource-monitor version-management skill-finder-cn autonomous-agent correct-py fleet-engineering memory-engineering spec-driven-development refactoring-engineering refactor-guard fullstack-dev refactoring-test vue-upload"
for s in $ECO_SKILLS; do
  if [ ! -d "$REPO/skills/$s" ]; then echo "  $s : absent du clone (hors périmètre) — ignoré"; continue; fi
  if [ ! -d "$SK/$s" ]; then
    echo "  $s : ABSENT local → installation depuis le clone"
    rsync -a --delete "$REPO/skills/$s/" "$SK/$s/"
  elif ! diff -rq "$REPO/skills/$s" "$SK/$s" >/dev/null 2>&1; then
    echo "  $s : drift → restauration certifiée"
    rsync -a --delete "$REPO/skills/$s/" "$SK/$s/"
  else
    echo "  $s : conforme"
  fi
done

# --- Étape 7 : Registre KB skills/KNOWLEDGE.md (source de vérité) ---
echo "--- Étape 7 : registre KB ---"
cp -p "$REPO/skills/KNOWLEDGE.md" "$SK/KNOWLEDGE.md"
n_kb=$(rg -c '^## [\w-]+ v[\d.]+' "$SK/KNOWLEDGE.md" || echo 0)
echo "KNOWLEDGE.md déployé : $n_kb entrées versionnées (attendu ≥ 14)"

# --- Étape 8 : Outillage scripts/ (socle §2ter) ---
echo "--- Étape 8 : outillage ---"
mkdir -p "$LOCAL/scripts"
SCRIPTS="check-ecosysteme-integrity.py verify-cross.py certification-complete.py task14-scan-doublons.py task21-f2-rebuild-archive.py refactoring-test-graph.py ensure-installed.py install-ecosystem.py install-ecosystem-skills.py generer-pm-skill.py propagate-context.py sync-context-block.py gen-ultra-maitre.py scan-versions-reelles.py audit-provenance.py install-profile.json ecosysteme-integrity.json"
for f in $SCRIPTS; do
  if [ -f "$REPO/scripts/$f" ]; then
    if [ "$f" = "task21-f2-rebuild-archive.py" ]; then
      # Adaptation mécanique du chemin (règle d'or n°1, §3.4) : BASE machine d'origine → profil local
      sed 's|^BASE = Path("/home/z/my-project/work_knowledge")|BASE = Path("/home/z/my-project")|' "$REPO/scripts/$f" > "$LOCAL/scripts/$f"
    else
      cp -p "$REPO/scripts/$f" "$LOCAL/scripts/$f"
    fi
  else
    echo "  ⚠ $f absent du clone"
  fi
done
echo "outillage déployé dans scripts/"

# --- Syntaxe Python (critère étape 8) ---
echo "--- Vérification syntaxe arbitres ---"
ok=0; ko=0
for py in "$LOCAL/scripts/"*.py; do
  if python3 -c "import ast; ast.parse(open('$py').read())" 2>/dev/null; then ok=$((ok+1)); else ko=$((ko+1)); echo "  ⚠ SYNTAXE KO : $py"; fi
done
echo "scripts exécutables : $ok OK, $ko KO"

echo "=== INSTALLATION TERMINÉE — $TS ==="
