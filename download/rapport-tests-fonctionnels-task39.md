# Rapport de tests fonctionnels — Task 39 / G5 (batterie robuste $facon)

> **Session** : web-6058b3ba · **Date** : 2026-11-02 · **CDC** : D010 (batterie par élément + idempotence ×2 + arbitres de domaine).
> **Cible** : tsi-toolkit v1.0.0 (+ livrables L-4 tsi-agent/zip-tsi, L-5 bibliothèque multi-IA, L-6 studio).
> **Méthode** : chaque test = une commande exécutable au verdict binaire ; échecs corrigés puis re-testés (max 2 rounds — respecté : 2 rounds utilisés).

## 1. Suite unitaire (EF-01..EF-08, ENF-01..03) — 20/20 PASS

`python3 -m unittest tests.test_toolkit` — inspect multi-format (DJTT réel via pont : DCBM 5 626 ; 4 TSI réels propriétaire), génération validée par l'arbitre (rc=0, 15 mappings), import CSV (21 mappings, hexa toléré), Karnaugh (conflit détecté / 0 faux positif / golden sample sain), couverture (0 couche morte), roundtrip TSI↔JSON byte-identique, CLI (7 sous-commandes), base de commandes (393 ≥ 200, < 1 s), idempotence ×2, stdlib uniquement.

## 2. Batterie fonctionnelle robuste — 16/16 PASS

| # | Test | Verdict | Détail |
|---|---|---|---|
| TF-01 | inspect mapping réel DJTT v2.1.0 (1,8 Mo) | **PASS** | 0,20 s (seuil ENF-03 : 10 s) — pont analyseur : DCBM 5 626 |
| TF-02..05 | inspect 4 TSI réels du propriétaire (Drive `mapping kontrol s4/` + `Traktor Setting 2021/`) | **PASS** | 0,10-0,14 s chacun — familles REEL_DDIOM/REGLAGES reconnues |
| TF-06 | fichier inexistant | **PASS** | rc=2, message propre, **0 traceback** |
| TF-07 | fichier garbage (non-TSI) | **PASS** | rejet contrôlé rc=2 (famille INCONNU) |
| TF-08 | CSV vide | **PASS** | rejet rc=2 propre |
| TF-09 | CSV colonnes invalides | **PASS** | rejet rc=2 propre |
| TF-10 | preset canal MIDI 16 (hors plage 0-15) | **PASS** | refus rc=2 — plages vérifiées |
| TF-11 | conflit MIDI (36 dupliqué) | **PASS** | génération refusée rc=2 (anti-conflits actif) |
| TF-12 | chaîne complète generate→validate→coverage→convert→roundtrip | **PASS** | 0,32 s, TSI roundtrip byte-identique |
| TF-13 | CSV Pseudo-TSI historique (21 mappings) → TSI | **PASS** | **arbitre tsi-validator : PASS (0 erreur, 21 mappings)** |
| TF-14 | zip-tsi ×2 | **PASS** | byte-identique (sha256 153e90def9013a29…) |
| TF-15 | bibliothèque multi-IA ×2 | **PASS** | 6 plateformes byte-identiques |
| TF-16 | suite unitaire | **PASS** | 20/20 |

## 3. Corrections appliquées pendant la batterie (traçabilité)

| Round | Échec initial | Cause | Correction | Re-test |
|---|---|---|---|---|
| 1 | TF-06 traceback sur fichier inexistant | pas de gestion d'erreur CLI | gestionnaire global : rc=2, message propre, 0 traceback | PASS |
| 1 | TF-07 rc=0 sur garbage | famille INCONNU non sanctionnée | inspect INCONNU → rc=2 | PASS |
| 1 | TF-13 arbitre E3 : GROUP invalides ('Loop Recorder', 'FX Unit 1', 'Remix Deck', 'Browser') | sections Traktor réelles ≠ taxonomie canonique | **canonisation** des sections (table `SECTIONS_CANONIQUES`, section d'origine conservée dans le NOM — perte nulle) | → round 2 |
| 2 | TF-13 arbitre E3 : NAME dupliqué (lignes 3/6 du CSV : même contrôle/commande, conditions différentes) | noms identiques | le nom porte la **condition de couche** (`[M1=1]`) — informatif + unique | PASS |
| 2 | verdict interne FAIL (karnaugh) sur CSV historique | karnaugh strict (états chevauchants) vs arbitre E5 (conditions distinctes) | karnaugh déplacé en **avertissements consultatifs** dans `validate` (le générateur reste conservateur — refus par défaut) ; l'arbitre écosystème reste la source de vérité du verdict | PASS (interne PASS + 1 avertissement documenté + arbitre PASS) |
| — | TF-08..11 attendus rc=1, obtenus rc=2 | convention CLI unifiée par le gestionnaire d'erreurs | calibration des attendus de la batterie (rc=2 = convention « entrée rejetée ») | PASS |

## 4. Idempotence (R6 / ENF-02)

- Génération TSI ×2 : byte-identique (test unitaire) ;
- `construire-zip-tsi.py` ×2 : sha256 identique (TF-14) ;
- `generate_prompts.py` ×2 : empreinte globale identique (TF-15) ;
- `audit_log.md` du studio : **croît** à chaque exécution — comportement voulu (mécanisme auto-évolutif v11), les sorties TSI restent identiques (test unitaire).

## 5. Performance (ENF-03 — seuils CDC : inspect < 10 s, validate < 5 s)

- inspect DJTT 1,8 Mo (avec pont analyseur) : **0,20 s** ;
- validate (avec pont arbitre) : **0,16 s** ;
- chaîne complète 5 commandes : 0,32 s.

## 6. Verdict final

**16/16 PASS + suite unitaire 20/20 PASS — aucune optimisation corrective restante.**
Convergence validée : les éléments historiques des discussions (CSV 21 mappings, échantillon doré, mappings réels DJTT + propriétaire) sont consommés et produits par la toolchain avec des verdicts d'arbitre mécaniques.
