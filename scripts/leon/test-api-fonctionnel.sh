#!/usr/bin/env bash
# test-api-fonctionnel.sh — Batterie API 15 points $FACON2 du LEON TSI EDITEUR v11.
#
# Héritage : harnais de la discussion b6170b8b (15/15 itération 3) — Task 40.
# Cible : serveur dev local (port 3000). Verdict mécanique : 15/15 attendu.
# Idempotent : crée puis SUPPRIME son projet de test (restauration propre).
set -u
BASE="http://localhost:3000"
PASSED=0; FAILED=0
ok()   { PASSED=$((PASSED+1)); echo "  [PASS] $1"; }
ko()   { FAILED=$((FAILED+1)); echo "  [FAIL] $1 — $2"; }

echo "BATTERIE API \$FACON2 — LEON TSI EDITEUR v11 (15 points)"

# 1-2. Projets
curl -sf "$BASE/api/projects" | grep -q '"projets":\[' && ok "1. GET /api/projects (liste)" || ko "1. GET /api/projects" "réponse invalide"
ID=$(curl -sf -X POST "$BASE/api/projects" -H "Content-Type: application/json" -d '{"name":"harnais-api-15"}' | python3 -c 'import json,sys; print(json.load(sys.stdin)["projet"]["id"])') \
  && ok "2. POST /api/projects (création)" || ko "2. POST /api/projects" "création impossible"

# 3-4. PATCH contrat {data} (discussion : le PATCH attend { data: "<JSON string>" })
DATA=$(python3 - <<'PYEOF'
import json
projet = {"device": {"name": "Traktor Kontrol S4 MK2", "type": "MIDI", "in_port": "In", "out_port": "Out", "deck_target": "Focus"},
          "mappings": [{"nom": "Play/Pause — Deck A", "type": "IN", "groupe": "Deck A", "controle": "Play/Pause",
                        "midi": {"canal": 0, "message": "NOTE", "numero": 36, "mode": "Direct"}}]}
print(json.dumps({"data": json.dumps(projet, ensure_ascii=False)}))
PYEOF
)
RC=$(curl -s -o /dev/null -w "%{http_code}" -X PATCH "$BASE/api/projects/$ID" -H "Content-Type: application/json" -d "$DATA")
[ "$RC" = "200" ] && ok "3. PATCH {data: JSON string} → 200" || ko "3. PATCH {data}" "HTTP $RC"
RC=$(curl -s -o /dev/null -w "%{http_code}" -X PATCH "$BASE/api/projects/$ID" -H "Content-Type: application/json" -d '{"data":"pas un json"}')
[ "$RC" = "400" ] && ok "4. PATCH data invalide → 400 (rejet propre)" || ko "4. PATCH invalide" "HTTP $RC"

# 5-6. GET + verify (byte-exact)
curl -sf "$BASE/api/projects/$ID" | grep -q '"Play/Pause' && ok "5. GET /api/projects/:id (contenu persisté)" || ko "5. GET :id" "contenu absent"
V=$(curl -sf -X POST "$BASE/api/projects/$ID/verify")
echo "$V" | grep -q '"BYTE-EXACT"' && ok "6. verify → BYTE-EXACT (round-trip sérialiseur)" || ko "6. verify" "$V"

# 7-8. Export .tsi (XML canonique + DEVICE)
E=$(curl -sf "$BASE/api/projects/$ID/export")
echo "$E" | head -1 | grep -q '<?xml' && ok "7. export → XML (<?xml…)" || ko "7. export XML" "pas un XML"
echo "$E" | grep -q '<DEVICE NAME="Traktor Kontrol S4 MK2"' && echo "$E" | grep -q 'CONTROL="Play/Pause"' \
  && ok "8. export → DEVICE S4 MK2 + MAPPING Play/Pause" || ko "8. export DEVICE" "structure manquante"

# 9-10. Audit (POST → 201, GET → entrée lisible)
RC=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE/api/projects/$ID/audit" -H "Content-Type: application/json" -d '{"action":"harnais","detail":"entrée test"}')
[ "$RC" = "201" ] && ok "9. audit POST → 201 (auto-évolutif)" || ko "9. audit POST" "HTTP $RC"
curl -sf "$BASE/api/projects/$ID/audit" | grep -q '"action":"harnais"' && ok "10. audit GET (entrée relue)" || ko "10. audit GET" "entrée absente"

# 11-12. Presets (API studio v11 — source partagée)
P=$(curl -sf "$BASE/api/presets")
echo "$P" | grep -q 'Freeze Mode' && ok "11. presets → Freeze Mode (source toolchain)" || ko "11. presets" "preset absent"
echo "$P" | grep -q '"nbMappings":15' && ok "12. preset Freeze Mode = 15 mappings (byte-parité toolkit)" || ko "12. preset 15" "$P"

# 13. 404 propre (projet inexistant)
RC=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/api/projects/introuvable-xyz")
[ "$RC" = "404" ] && ok "13. projet introuvable → 404" || ko "13. 404" "HTTP $RC"

# 14. POST body invalide → 400
RC=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE/api/projects" -H "Content-Type: application/json" -d '{"autre": 1}')
[ "$RC" = "400" ] && ok "14. POST sans name → 400" || ko "14. POST invalide" "HTTP $RC"

# 15. DELETE + restauration propre de l'état projet
RC=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE "$BASE/api/projects/$ID")
[ "$RC" = "200" ] && ok "15. DELETE (restauration propre de l'état)" || ko "15. DELETE" "HTTP $RC"
N=$(curl -sf "$BASE/api/projects" | python3 -c 'import json,sys; print(len(json.load(sys.stdin)["projets"]))')
[ "$N" = "0" ] && ok "    état projet restauré : 0 projet résiduel" || ko "    état" "$N projets résiduels"

echo "BATTERIE : $PASSED/15 PASS, $FAILED FAIL"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
