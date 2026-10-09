# Rapport — Task 11 : pipeline S2-δ → S1 → correct-work(projet) → test robuste (Phase F)

> Session web-b93f42fa · 2026-10-10 · gen-plan v3.21.0 + correct-work v2.7.0 PROJET
> Directive propriétaire : re-vérifier S2-δ en session saine, puis S1 réinstallation réelle, puis correct-work(projet), puis test robuste.

## 1. S2-δ — résorbée (byte-lock)

Scan canal sain : 13 occurrences du root auteur stale `/home/z/my-project/ecosystem` dans 8 hooks r*.py (10 littéraux + 3 fragments join de r3 sous PROJECT="/home/z/my-project") ; r8 L45 `os.makedirs` du répertoire fantôme confirmé en code. Fix appliqué (classe validée S2-γ, zéro logique) : sed ×7 littéraux + fragments r3 → `work_knowledge`. Hex-lock r1 L9 (`776f726b5f6b6e6f776c65646765` = work_knowledge), 0 restant, COMPILE_OK ×8, ghost-dir absent, smoke r5 (json 8 clés) + r8 sans création fantôme. R2-δ : 16/16, 60/60, 48/3/0 — baseline intacte.

## 2. S1 — réinstallation réelle (cycle D006 complet)

Prérequis appliqué : L24 `ensure-installed.py` → `work_knowledge` (hex-lock md5 a5592de1, compile OK) + task40 py/json archivés `scripts/_archive/` (git mv). Cycle hook 3 modes rc0 : `--check` **INSTALLE** (head 3eebe65, 0 manquants, KB 29) · `--reinstall` **no-op idempotent D006** · `--preempt` **PRIORITE-NONE**. La réinstallation garantie est opérationnelle : avant fix, les 3 modes retournaient rc1 (finding ③ résorbé). Le no-op est le résultat prescrit sur un écosystème sain (aucune action destructive sur un arbre dirty de 58 fichiers).

## 3. correct-work(projet) — PASS AVEC RÉSERVES

Arbitres : verify-correct-work **16/16** ALL PASS · integrity **60/60** · coherence **48/3/0** · verify-cross **83/84** (C006 héritée skill-finder-cn, 98,8 %) · generer-pm **3/3**. Matrice versions : gen-plan 3.21.0 / correct-work 2.7.0 / clone-chat 2.0.0 ≥ planchers (A1 croisé PASS). Chaîne : dirty 58 décomposé (couches B2.x/D.2 + Task 10/11 + tmp/ + rapports). 0 S1.

## 4. Test robuste Phase F — PASS AVEC RÉSERVES ×3 convergent

Input byte-verrouillé : `chat-assets/chat-discussion-b2b4e631.md` (117 541 o, sha256 0652d8b23bd2, 32 messages 16/16, alternance parfaite 0 rupture, contamination 0, message vide n°28 conforme à la documentation).
- **W1 structure** : PROPRE AVEC RÉSERVES (0 S1/S2 ; 1 S3 comptage 1449/1448 — convention split, consignée sans trancher) — sha b8b49078a5a4.
- **W2 claims** : CONCORDANT AVEC RÉSERVES — 39 claims : 27 concordants / 7 obsolètes / 5 non-vérifiables / **0 DIVERGENT** ; réserve : « verify-cross 84/84 » (M14) jamais persisté au repo — cohérent règle d'or n°2 ; I1-I3 internes mineures (tension 28 skills vs 29 entrées KB encore vivante).
- **W3 cohérence** : FIABLE AVEC RÉSERVES — matérialisation worklog↔disque 40 % pleine / 90 % ≥ partielle ; 8 correspondances discussion↔worklog (5 concordantes, 2 partielles, 1 absente — journal applicatif PS5Tube hors disque) ; fait verrouillé confirmé (rapports task9/task10/SO inexistants).
F3 arbitre : script compilé (md5 1a53480aa1) — stdout corrompu en cours d'exécution (échos contradictoires, champs inexistants du code) ; verdict fondé sur les mesures de fichiers byte-verrouillées ×2 canaux (KO-L003, protocole Task 5/6).

## 5. Anomalie canal — bilan KO-L003

Deux régimes documentés : (a) session Task 10 d'hier — les 4 gates + 3 rapports + rc0 aveugle JAMAIS matérialisés (échos, y compris byte-checks affichés) ; (b) rechute pendant F3 — stdout mort, fichiers vivants. Discipline tenue : hex/md5 byte-level, 2 canaux par fait critique, divergence consignée sans trancher, aucun verdict sur sortie douteuse.

## 6. État final et restant propriétaire

0 commit, 0 push — HEAD 3eebe65 inchangé ; dirty 58 + tmp/ + rapports Phase F. Restant : **S2-α/β re-validation** (shim arbitre + SKILL.md 5 lignes — jamais matérialisées, preuve d'hier corrompue) ; **S4** commit local + proposition push ; C006 (décision ancienne, non bloquante) ; tension « 28 skills vs 29 entrées KB » à réconcilier.
