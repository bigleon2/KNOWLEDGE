#!/usr/bin/env bash
# git-deploy.sh — Automatise commit + push du dépôt KNOWLEDGE
# Usage:
#   bash scripts/git-deploy.sh                    # commit + push interactif
#   bash scripts/git-deploy.sh --auto "message"    # commit + push automatique
#   bash scripts/git-deploy.sh --push-only         # push sans nouveau commit
#   bash scripts/git-deploy.sh --status            # affiche le statut uniquement

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
REMOTE_URL="https://github.com/bigleon2/KNOWLEDGE.git"
BRANCH="main"

# --- Couleurs ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# --- Fonctions ---
info()  { echo -e "${BLUE}[INFO]${NC}  $*"; }
ok()    { echo -e "${GREEN}[OK]${NC}    $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
err()   { echo -e "${RED}[ERR]${NC}   $*"; exit 1; }

# Charge le token GitHub
load_token() {
    # Priorité : env GITHUB_TOKEN > fichier .env > fichier upload
    if [[ -n "${GITHUB_TOKEN:-}" ]]; then
        TOKEN="$GITHUB_TOKEN"
    elif [[ -f "$PROJECT_DIR/.env" ]] && grep -q 'GITHUB_TOKEN' "$PROJECT_DIR/.env"; then
        TOKEN=$(grep 'GITHUB_TOKEN' "$PROJECT_DIR/.env" | head -1 | cut -d'=' -f2- | tr -d '"'\''\n\r' | tr -d ' ')
    else
        err "Token GitHub introuvable. Exportez GITHUB_TOKEN ou créez .env"
    fi
    AUTH_URL="https://x-access-token:${TOKEN}@github.com/bigleon2/KNOWLEDGE.git"
}

# Vérifie les prérequis
check_prereqs() {
    info "Vérification des prérequis..."
    cd "$PROJECT_DIR" || err "Répertoire projet introuvable"
    command -v git >/dev/null 2>&1 || err "git n'est pas installé"
    [[ -d .git ]] || err "Pas de dépôt git dans $PROJECT_DIR"
    ok "Dépôt git détecté"
}

# Affiche le statut
show_status() {
    info "Statut du dépôt"
    echo ""
    echo "  Branche   : $(git rev-parse --abbrev-ref HEAD)"
    echo "  Commit    : $(git log --oneline -1)"
    echo "  Fichiers  : $(git ls-files | wc -l) trackés"
    echo ""
    local staged=$(git diff --cached --stat 2>/dev/null | tail -1)
    local unstaged=$(git diff --stat 2>/dev/null | tail -1)
    local untracked=$(git ls-files --others --exclude-standard | wc -l)
    [[ -n "$staged" ]] && echo "  Staged    : $staged"
    [[ -n "$unstaged" ]] && echo "  Modified  : $unstaged"
    [[ "$untracked" -gt 0 ]] && echo "  Untracked : $untracked fichiers"
    [[ -z "$staged" && -z "$unstaged" && "$untracked" -eq 0 ]] && echo "  ${GREEN}Working tree clean${NC}"
}

# Commit toutes les modifications
do_commit() {
    local msg="${1:-Mise à jour écosystème Knowledge}"
    info "Commit : $msg"
    
    # Stage tout (sauf upload/ et tool-results/)
    git add -A
    
    # Unstage les fichiers exclus
    git reset HEAD upload/ 2>/dev/null || true
    git reset HEAD tool-results/ 2>/dev/null || true
    git reset HEAD .env 2>/dev/null || true
    git reset HEAD node_modules/ 2>/dev/null || true
    
    # Vérifier s'il y a quelque chose à commiter
    if git diff --cached --quiet 2>/dev/null; then
        warn "Rien à commiter (working tree déjà à jour)"
        return 0
    fi
    
    local count=$(git diff --cached --numstat | wc -l)
    info "${count} fichiers à commiter"
    
    git commit -m "$msg"
    ok "Commit créé"
}

# Push vers GitHub
do_push() {
    load_token
    info "Push vers ${BRANCH}..."
    
    local output
    output=$(git push "$AUTH_URL" "$BRANCH" 2>&1) && ok "Push réussi" || {
        echo "$output"
        # Essai force-push si le remote a divergé
        if echo "$output" | grep -q 'updates were rejected\|would clobber'; then
            warn "Le remote a divergé. Force-push ?"
            read -p "  Confirmer force-push ? [o/N] " confirm
            if [[ "$confirm" == "o" || "$confirm" == "O" ]]; then
                git push --force "$AUTH_URL" "$BRANCH" 2>&1 && ok "Force-push réussi"
            else
                err "Push annulé"
            fi
        else
            err "Push échoué"
        fi
    }
}

# --- Main ---
cd "$PROJECT_DIR"
check_prereqs

MODE="${1:-}"

case "$MODE" in
    --status)
        show_status
        ;;
    --push-only)
        do_push
        ;;
    --auto)
        do_commit "${2:-Mise à jour écosystème Knowledge}"
        do_push
        ;;
    "")
        show_status
        echo ""
        read -p "  Message du commit [Mise à jour écosystème Knowledge] : " custom_msg
        do_commit "${custom_msg:-Mise à jour écosystème Knowledge}"
        do_push
        ;;
    *)
        echo "Usage: bash scripts/git-deploy.sh [--status|--push-only|--auto "message"]"
        exit 1
        ;;
esac
