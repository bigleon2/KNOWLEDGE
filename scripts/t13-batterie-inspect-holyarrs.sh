#!/usr/bin/env bash
# t13-batterie-inspect-holyarrs.sh — T1 fonctionnel : doctor + batterie inspect-* sur bin/holyarrs
# Task ID 13 / G4.2 — tests REA×HolyArrs. Evidence : tools/rea/*-holyarrs-t13.out, timings vers stdout.
set -u
KIT=/home/z/my-project/tools/rea/REA_Reverse_All_Thing_Kit
BIN=/home/z/my-project/tools/holyarrs/HolyArrs/bin/holyarrs
EV=/home/z/my-project/tools/rea
export REA_PWNTOOLS_PYTHON=/home/z/my-project/tools/rea/venv/bin/python
export REA_PWNTOOLS_MAX_INPUT_BYTES=50331648
export GHIDRA_INSTALL_DIR=/home/z/my-project/tools/rea/ghidra/ghidra_12.2_PUBLIC
cd "$KIT" || exit 9

# 0) doctor (sonde moteurs)
S=$(date +%s%3N)
node scripts/rea.mjs doctor > "$EV/doctor-holyarrs-t13.out" 2>&1
RC=$?
E=$(date +%s%3N)
echo "doctor rc=$RC duree_ms=$((E-S))"

# 1) inventaire de surface (--help, rc + durée)
S=$(date +%s%3N)
node scripts/rea.mjs --help > "$EV/help-surface-t13.out" 2>&1
RC=$?
E=$(date +%s%3N)
echo "help rc=$RC duree_ms=$((E-S)) lignes=$(wc -l < "$EV/help-surface-t13.out")"

# 2) batterie inspect-* (5 commandes canoniques Task 9 + inspect-go-binary)
for cmd in inspect-binary-hardening inspect-binary-layout inspect-byte-entropy inspect-elf-notes inspect-native-exports inspect-go-binary; do
  S=$(date +%s%3N)
  node scripts/rea.mjs "$cmd" "$BIN" > "$EV/${cmd}-holyarrs-t13.out" 2> "$EV/${cmd}-holyarrs-t13.timings"
  RC=$?
  E=$(date +%s%3N)
  echo "$cmd rc=$RC duree_ms=$((E-S)) octets=$(wc -c < "$EV/${cmd}-holyarrs-t13.out")"
done
echo "BATTERIE TERMINÉE"
