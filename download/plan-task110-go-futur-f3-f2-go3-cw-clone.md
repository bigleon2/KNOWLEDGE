# Plan d'actions — Task 110 : « GO futur + GO-3 » (correctifs structurels F3/F2 + convention canons)

> Directive propriétaire trace `1a1f2297d90c957d` : `gen-plan : "GO futur + GO-3"` — le message CONSTITUE le GO propriétaire pour les tâches 3-4-5 du livrable `download/taches-restantes-task108.md` (P2 F3 injecteur, P2 F2 scelleur, P3 GO-3 canons). Mode NULL (v3.21.0) : exécution classique sans portes de confirmation. Session web-ecef7f80, suite worklog 156. Généré le 2026-11-19 par gen-plan v3.43.0 (E1-E8).

**Horodatage plan : 2026-11-19T05:05:00Z**

## E1 — Analyse de la demande (answer key ci-dessous)

Périmètre GO (3 tâches sources, critères d'extinction verbatim du livrable) :
- **Tâche 3 (P2)** — F3 : injecteur `scripts/propagate-context.py` — gabarit littéral périmé sur la branche injection (classe F-70-2, la dynamisation v2.1.1 ne couvre que la branche remplacement) + insertion qui casse les scripts à docstring suivie de `from __future__` (SyntaxError : second littéral avant import future) ; 5 scripts protégés par revert (task98/101/102/104/106) demeurent SANS bloc CONTEXTE.
- **Tâche 4 (P2)** — F2 : garde anti-perte du scelleur v2.3 (`scripts/task-f5-seal-archive-v23.py`) traite toute divergence corpus↔archive comme une dérive (ECHEC sans distinction dérive/légitime) — bloque toute évolution de corpus légitime depuis Task 100.
- **Tâche 5 (P3)** — GO-3 : convention « docstring d'abord, bloc CONTEXTE ensuite » (démontrée par `bootstrap-ecosysteme.py`, Task 105 S3/F4) aux canons `skills/script-creator/SKILL.md` + `skills/correct-py/SKILL.md`.

HORS périmètre (tâches du livrable NON couvertes par ce GO) : tâche 1 (révocation ancien PAT — PROPRIÉTAIRE), tâche 6 (décision cron 531684 — PROPRIÉTAIRE), tâche 7 (surveillance F3 prochain bootstrap — AUTO), tâche 8 (PMs §0 — AUTO). Correctifs proposés (CW 107, verbatim) : F3 « dynamiser CONTEXT_HEADER_L3 + insertion après la docstring d'en-tête » ; F2 « drapeau d'évolution contrôlé ou comparaison git ».

## E2 — Inventaire des ressources (mesuré au disque, 2026-11-19)

| Ressource | État mesuré |
|---|---|
| `scripts/propagate-context.py` (×2 arbres) | v2.1.1, 221 lignes, parité hôte↔dépôt md5 `570bc0bf…` ; défauts : `.replace("(SHARED v1.7.31)")` clé figée (la substitution échoue silencieusement quand le littéral est bumpé manuellement — cause racine du gabarit périmé v1.7.39) ; triple gabarit littéral L2/L3_HEADER/L3_INNER (dérive inter-gabarits : bases 1.7.31 vs 1.7.40) ; branche injection lignes 159-166 = docstring pré-pendue SANS détection de docstring existante (casse `from __future__`) |
| 5 scripts protégés | `task98-simulation-extinction.py`, `task101-scan-differes.py`, `task102-extraction-blocs.py`, `task104-genere-fiche.py`, `task106-inventaire-familles.py` — parité ×2 arbres vérifiée, 0 bloc CONTEXTE, `from __future__` présents dans task101 + task102 (les 2 compilations cassées, CW 107) |
| `scripts/task-f5-seal-archive-v23.py` (×2) | v2.3, 101 lignes, parité `6dfac1a6…` ; garde anti-perte lignes 65-70 : divergence = ECHEC rc=2 sans distinction ; EPOQUE_FIXE 1980-01-01 (byte-stabilité R6) ; .bak natif ; round-trip 15 entrées (9 corpus + 6 piliers) |
| `scripts/eco_install_pipeline.py` (×2) | parité `46be4055…` ; 3 références au scelleur v23 : docstring l.41, étapes l.55, exécution l.276 (`HOST/scripts/task-f5-seal-archive-v23.py`, rc propagés F1 Task 22) |
| Canons | `script-creator` v1.1.0, `correct-py` v1.1.0 (§4 CONVENTIONS présents ×2, HISTORIQUE DES VERSIONS chez correct-py) |
| Corpus | SHARED v1.7.40 ; SYNC-CONTEXT v1.5.11 — mentions propagate/scelleur uniquement HISTORIQUES (révisions v1.4.x, enregistrements R2/R6 jamais édités) → **corpus @mon-ecosysteme/ INCHANGÉ ce tour** |
| Dépôt git | HEAD = a5daa964 = origin/main (0 unpushed), arbre propre ; precedent véhicules scelleur : task21-f2 (v2.2) → task-f5-seal-archive-v23 (v2.3) = NOUVEAU fichier par version, ancien conservé R4 |
| G-RES | OK (disque 8,1 Go, mémoire 3,6 Go, charge 0,06) — profil NORMAL |

## E3 — Classification : Type 4 (maintenance outillage écosystème — scripts Python + canons + cascade, livrables = correctifs + rapports mécaniques).

## E4 — Estimation #token

| Groupe | #token estimé |
|---|---|
| G0 préflight | 600 |
| G1 F3 injecteur | 3500 |
| G2 F2 scelleur | 3500 |
| G3 GO-3 canons | 2500 |
| G4 clôture | 3000 |
| **Total** | **~13 100** (profil NORMAL, plage exécution complexe 10-20 k) |

Contingence : profil frais local ×3-4 sur la part découverte — PARTIELLEMENT résorbée (inventaire E2 déjà exécuté ce tour, contexte de continuation) ; aucune récupération externe requise.

## E5 — Skills mobilisés : gen-plan (pilote, ce plan) · script-creator v1.1.0 (création scelleur v2.4 + harnais — le script démontre la convention GO-3 par construction) · correct-py v1.1.0 (contrôle post-création) · correct-work (E8 + hook par phase G4) · clone-chat (clôture) · resource-monitor (E1-RES collecté : OK). Arbitres : answer-key-checker, check_plan_protocol, certification-complete, verify-correct-work, check-triggers-replay, task14-scan-doublons, check-tool-routing.

## E6 — Profil NORMAL (G-RES OK, 0 signal de pression).

---

## Groupes d'exécution

### G0 — Préflight (lecture seule) — #token 600

| Tâche | Description | Statut |
|---|---|---|
| T0.1 | État git (HEAD, arbre, 0 unpushed) + parités md5 ×2 arbres (propagate, pipeline, scelleur, 5 scripts) — MESURÉ ci-dessus | [TERMINÉ] |
| T0.2 | Baseline arbitres : check-tool-routing (N1 AVANT), verify-correct-work 16/16, check-triggers-replay, task14-scan-doublons | [À FAIRE] |
| T0.3 | Consignation état initial : 5 scripts SHA + 0 bloc CONTEXTE + `from __future__` ×2 (task101/102) | [TERMINÉ] |

### G1 — F3 : injecteur propagate-context.py v2.1.1 → v2.2.0 — #token 3500

| Tâche | Description | Statut |
|---|---|---|
| T1.1 | Harnais `scripts/task110-test-injecteur.py` AVANT correctif (règle d'or n°5 — mesurer avant corriger) : cas synthétiques en bac à sable — (a) docstring + `from __future__` → doit compiler ET porter le bloc ; (b) docstring simple ; (c) sans docstring avec shebang ; (d) sans shebang ; (e) porteur forme docstring → remplacement version ; (f) porteur forme commentée → remplacement version ; (g) script embarqué → jamais injecté. Verdicts attendus ROUGES sur l'injecteur v2.1.1 (a cassé, f non couvert) | [À FAIRE] |
| T1.2 | Correctif v2.2.0 (les DEUX arbres, parité) : (1) **dynamisation robuste** — `re.sub(r'\(SHARED v[0-9.]+\)', …)` sur les 3 gabarits (remplace la clé figée `.replace("(SHARED v1.7.31)")` qui échoue silencieusement) ; (2) **DRY** — L3_BLOCK_INNER DÉRIVÉ de CONTEXT_HEADER_L3 (suppression de la duplication littérale) ; (3) **branche injection** : détection de docstring de module → bloc CONTEXTE en LIGNES COMMENTÉES (`# ⚙️ …`, canon bootstrap) APRÈS la docstring — jamais de second littéral (`from __future__` préservé) ; sans docstring → forme docstring après shebang (légale avant import future) ; (4) **branche remplacement** : support de la forme commentée mono-ligne en plus de la forme docstring ; (5) docstring du script : bump v2.2.0 + delta documenté. Harnais re-jeu → VERT, idempotence ×2 | [À FAIRE] |
| T1.3 | Propagation re-jeuée sur les DEUX arbres : les 5 scripts restaurés portent le bloc §0 v1.7.40 (forme commentée), `python3 -m py_compile` sur les 6 scripts racine touchés (5 + injecteur) = 0 SyntaxError, 2ᵉ passe idempotente (porteurs byte-stables), `bootstrap-ecosysteme.py` NON modifié (R2 — sa forme commentée enveloppée reste stable) | [À FAIRE] |
| T1.4 | Arbitres post-G1 : certification-complete ALL PASS 6/6 (§0 alignés v1.7.40) | [À FAIRE] |

### G2 — F2 : scelleur v2.4 — NOUVEAU `scripts/task-f5-seal-archive-v24.py` — #token 3500

| Tâche | Description | Statut |
|---|---|---|
| T2.1 | Création du scelleur v2.4 (canons script-creator — docstring d'abord, bloc CONTEXTE ensuite : le script DÉMONTRE la convention GO-3) : garde anti-perte DISCRIMINANTE — (1) PERTE = entrée d'archive corpus sans contrepartie locale → ECHEC rc=2 (sémantique inchangée, jamais contournable) ; (2) ÉVOLUTION LÉGITIME = divergence corpus locale↔archive AVEC contenu local commité (comparaison `git show HEAD:<file>` == local) → rescellement AUTORISÉ + tracé « évolution légitime (git) : [fichiers] » ; (3) divergence NON commitée → ECHEC rc=3 + guidance (commiter l'évolution OU drapeau `--autoriser-evolution` = acceptation explicite opérateur) ; EPOQUE_FIXE byte-stabilité R6 préservée ; round-trip 15 entrées + .bak natif inchangés ; v2.3 conservé intact (R4) | [À FAIRE] |
| T2.2 | Harnais `scripts/task110-test-scelleur.py` (bac à sable : mini-arbre git + corpus 9 + piliers 6 + scelleur v2.4 copié) : T1 évolution commitée → rescellage SANS ECHEC ni intervention manuelle (critère d'extinction F2) · T2 perte (entrée archive absente localement) → rc=2 bloqué · T3 divergence non commitée → rc=3 + guidance · T3b `--autoriser-evolution` → OK tracé · T4 idempotence ×2 byte-stable · T5 parité v23/v24 sur état propre (SHA archives identiques). PASS = 6/6 cas, ×2 | [À FAIRE] |
| T2.3 | Repointage pipeline `eco_install_pipeline.py` ×2 arbres : l.276 exécution v23→v24 + docstring l.41/l.55 (note Task 110 : véhicule canonique v2.4, discrimination perte/évolution, GO futur trace 1a1f2297d90c957d) — rc propagés F1 inchangés | [À FAIRE] |
| T2.4 | Preuve réelle état propre : exécution v2.4 sur l'hôte (corpus inchangé, 0 divergence) → archive byte-stable (SHA identique à l'archive v2.3 courante) + manifeste vérifié (check-ecosysteme-integrity) | [À FAIRE] |

### G3 — GO-3 : convention aux canons — #token 2500

| Tâche | Description | Statut |
|---|---|---|
| T3.1 | `skills/script-creator/SKILL.md` v1.1.0 → v1.2.0 (MINOR) : §2/§4 convention « docstring d'abord, bloc CONTEXTE ensuite » — pour tout script de l'écosystème : docstring de module PEP 257 en tête (premier énoncé), bloc CONTEXTE §0 en lignes commentées APRÈS la docstring, JAMAIS en second littéral (SyntaxError `from __future__`) — évite le FAIL N1 silencieux (Task 105 S3/F4) | [À FAIRE] |
| T3.2 | `skills/correct-py/SKILL.md` v1.1.0 → v1.2.0 (MINOR) : §4 même convention côté correcteur — reconnaît et PRÉSERVE la forme (docstring en tête, bloc commenté après : jamais de fusion, déplacement ou suppression du bloc lors des corrections P257/CM) | [À FAIRE] |
| T3.3 | Cascade KO-L004 (périmètre non-PM) : lignage `@historique/historiques-par-skill/{script-creator,correct-py}.md` (entrées v1.2.0) + KB `skills/KNOWLEDGE.md` (lignes versions des 2 entrées) + miroirs hôte↔dépôt ×2 | [À FAIRE] |
| T3.4 | tool-routing N1 APRÈS → PASS inchangé (critère d'extinction GO-3) ; vérification frontmatters v1.2.0 ×2 arbres | [À FAIRE] |

### G4 — Clôture écosystème — #token 3000

| Tâche | Description | Statut |
|---|---|---|
| T4.1 | correct-work(projet) sur le tour → rapport `download/rapport-cw-task110-projet.md` | [À FAIRE] |
| T4.2 | clone-chat 22ᵉ scellage S1-S8 8/8 → `download/clone-chat-session-web-ecef7f80-20261119-task110.md` | [À FAIRE] |
| T4.3 | Rescellement final v2.4 (pilier KB mis à jour par la cascade GO-3 — évolution réelle via la voie mécanique) + manifeste régénéré ; livrables download/ + miroirs dépôt ; worklog suite 156 parité hôte↔dépôt md5 ; mise à jour du livrable `taches-restantes-task108.md` (tâches 3-4-5 ÉTEINTES avec preuves) | [À FAIRE] |
| T4.4 | Arbitres pré-commit ALL PASS (vcw 16/16 · certification 6/6 · triggers · doublons · answer-key-checker 16/16 ×2 · check_plan_protocol P1-P5) + COMMIT LOCAL « Task 110 CLOSE » SANS PUSH (0 PAT fourni ce tour — 0 manipulation KO-L009, pendance PUSH consignée, leçon Task 98/101) | [À FAIRE] |

**Dépendances** : G1 ∥ G2 indépendants (fichiers disjoints — preuve : périmètres d'écriture sans intersection) ; G3 APRÈS G2 (le rescellement final T4.3/G4 et la cascade KB exigent le scelleur v2.4 en place) ; G4 en dernier. Exécution : série G0→G1→G2→G3→G4, parallélisme interne par commandes indépendantes (fan-out).

## Critères d'extinction (mapping livrable taches-restantes-task108.md)

| Tâche source | Critère verbatim | Couverture |
|---|---|---|
| 3 (F3) | « propagation re-jeuée idempotente ×2 → 0 SyntaxError, 0 revert requis, les 5 scripts restaurés portent un bloc §0 v1.7.40 correct ; certification ALL PASS 6/6 » | T1.3 + T1.4 |
| 4 (F2) | « une montée de version de corpus (bump PM) rescellée SANS ECHEC transitoire ni intervention manuelle — la voie opérationnelle documentée devient mécanique » | T2.2-T1 (bac à sable : bump corpus commité → SANS ECHEC) + T4.3 (évolution réelle pilier KB via v2.4) |
| 5 (GO-3) | « les 2 SKILL.md portent la convention (montée de version mineure + cascade KO-L004) ; tool-routing N1 inchangé (PASS) » | T3.1-T3.4 |

## Answer key (hook E1 — decisions vérifiables)

```yaml
decisions:
  - id: "D001"
    criterion: "Le périmètre GO couvre exactement les tâches 3-4-5 du livrable taches-restantes-task108.md (F3, F2, GO-3) ; les tâches 1/6/7/8 restent ouvertes et non exécutées"
    verification: "python3 -c \"from pathlib import Path; t=Path('download/taches-restantes-task108.md').read_text(encoding='utf-8'); p=Path('download/plan-task110-go-futur-f3-f2-go3-cw-clone.md').read_text(encoding='utf-8'); assert '## 3. Correctif structurel F3' in t and '## 4. Correctif structurel F2' in t and '### 5. GO-3' in t and 'HORS périmètre' in p and 'cron 531684' in p\""
    source: "directive propriétaire trace 1a1f2297d90c957d (gen-plan : GO futur + GO-3) + livrable Task 108 G2"
    priority: "S1"
    status: "pending"
  - id: "D002"
    criterion: "L'injecteur propagate-context.py v2.2.0 dynamise la version des 3 gabarits par re.sub robuste (plus de clé figée), dérive L3_BLOCK_INNER de CONTEXT_HEADER_L3 (DRY), insère après la docstring en lignes commentées et remplace les formes docstring ET commentée"
    verification: "python3 scripts/task110-test-injecteur.py --check && python3 -c \"import re,pathlib; s=pathlib.Path('scripts/propagate-context.py').read_text(encoding='utf-8'); assert 'v2.2.0' in s and 'replace(\"(SHARED v1.7.31)\"' not in s and 'CONTEXTE en lignes comment' in s\""
    source: "CW Task 107 finding F3 (voie proposée : dynamiser CONTEXT_HEADER_L3 + insertion après la docstring d'en-tête)"
    priority: "S2"
    status: "pending"
  - id: "D003"
    criterion: "Les 5 scripts protégés (task98/101/102/104/106) portent un bloc §0 v1.7.40 correct sur les DEUX arbres, 0 SyntaxError, 0 revert"
    verification: "python3 -c \"from pathlib import Path; import py_compile; [py_compile.compile(str(f), doraise=True) for tree in ['.','KNOWLEDGE-repo'] for f in [Path(tree)/'scripts'/n for n in ['task98-simulation-extinction.py','task101-scan-differes.py','task102-extraction-blocs.py','task104-genere-fiche.py','task106-inventaire-familles.py']]]; assert all('CONTEXTE SYSTÈME' in (Path(t)/'scripts'/n).read_text(encoding='utf-8') for t in ['.','KNOWLEDGE-repo'] for n in ['task98-simulation-extinction.py','task101-scan-differes.py','task102-extraction-blocs.py','task104-genere-fiche.py','task106-inventaire-familles.py'])\""
    source: "CW Task 107 F3 (5 scripts protégés par revert) + critère d'extinction tâche 3"
    priority: "S2"
    status: "pending"
  - id: "D004"
    criterion: "Non-régression propagation : 2ᵉ passe idempotente (porteurs byte-stables), bootstrap-ecosysteme.py NON modifié (R2), certification-complete ALL PASS 6/6"
    verification: "python3 scripts/certification-complete.py > /dev/null; echo $?"
    source: "R2 zéro-régression + KO-L003 (verdicts honnêtes sur état mesuré)"
    priority: "S2"
    status: "pending"
  - id: "D005"
    criterion: "Le scelleur v2.4 (task-f5-seal-archive-v24.py NOUVEAU, v2.3 conservé R4) discrimine : PERTE bloquée rc=2, évolution commitée rescellée SANS ECHEC (tracée), divergence non commitée rc=3 + guidance, drapeau --autoriser-evolution explicite"
    verification: "python3 scripts/task110-test-scelleur.py --check"
    source: "CW Task 107 finding F2 (voie proposée : drapeau d'évolution contrôlé ou comparaison git) + critère d'extinction tâche 4"
    priority: "S2"
    status: "pending"
  - id: "D006"
    criterion: "Pipeline repointé v23→v24 sur les DEUX arbres (3 références, rc propagés inchangés) ; exécution réelle v2.4 sur état propre = archive byte-stable"
    verification: "python3 -c \"from pathlib import Path; [assert 'task-f5-seal-archive-v24.py' in Path(t+'/scripts/eco_install_pipeline.py').read_text(encoding='utf-8') for t in ['.','KNOWLEDGE-repo']]\" && python3 -c \"from pathlib import Path; p=Path('scripts/eco_install_pipeline.py').read_text(encoding='utf-8'); import re; assert len(re.findall(r'task-f5-seal-archive-v2[34]\\.py', p))==3\""
    source: "précédent véhicules v2.2→v2.3 (Task 100, nouveau fichier) + pipeline étape 2 (rc propagés F1 Task 22)"
    priority: "S2"
    status: "pending"
  - id: "D007"
    criterion: "script-creator ET correct-py v1.2.0 (MINOR) portent la convention « docstring d'abord, bloc CONTEXTE ensuite » + cascade (lignage @historique, KB, miroirs ×2 arbres)"
    verification: "python3 -c \"from pathlib import Path; [assert 'docstring d' + chr(39) + 'abord' in Path(t+'/skills/'+sk+'/SKILL.md').read_text(encoding='utf-8') and 'version: 1.2.0' in Path(t+'/skills/'+sk+'/SKILL.md').read_text(encoding='utf-8') for t in ['.','KNOWLEDGE-repo'] for sk in ['script-creator','correct-py']]\""
    source: "feuille de route §8.3 rapport Task 105 (GO-3, S3/F4) + critère d'extinction tâche 5"
    priority: "S2"
    status: "pending"
  - id: "D008"
    criterion: "tool-routing N1 PASS AVANT et APRÈS (inchangé)"
    verification: "python3 scripts/check-tool-routing.py > /dev/null; echo $?"
    source: "critère d'extinction tâche 5 (GO-3) — tool-routing N1 inchangé"
    priority: "S3"
    status: "pending"
  - id: "D009"
    criterion: "Clôture : correct-work(projet) PASS + clone-chat 22ᵉ scellé 8/8 + worklog suite 156 parité hôte↔dépôt + livrables download/ + commit LOCAL"
    verification: "python3 -c \"from pathlib import Path; import hashlib; h=hashlib.md5(Path('worklog.md').read_bytes()).hexdigest(); r=hashlib.md5(Path('KNOWLEDGE-repo/worklog.md').read_bytes()).hexdigest(); assert h==r\" && test -s download/rapport-cw-task110-projet.md && test -s download/clone-chat-session-web-ecef7f80-20261119-task110.md"
    source: "hooks correct-work (§5.4) + clone-chat (E15) + R5 journalisation"
    priority: "S1"
    status: "pending"
  - id: "D010"
    criterion: "0 PAT fourni ce tour : aucun push, 0 manipulation de jeton (KO-L009), pendance PUSH consignée au worklog et au livrable"
    verification: "python3 -c \"import subprocess; r=subprocess.run(['git','rev-list','--count','origin/main..HEAD'],capture_output=True,text=True,cwd='KNOWLEDGE-repo'); assert int(r.stdout.strip())>=1\""
    source: "KO-L009 + leçon Task 98/101 (push immédiat dès PAT frais — aucun PAT ce tour)"
    priority: "S2"
    status: "pending"
```

## Hooks de validation (E8)

- Arbitres : answer-key-checker (16 checks) · check_plan_protocol P1-P5 (horodatages couplés) · verdict consigné ci-dessous après exécution réelle.
- Verdict E8 : PASS (answer-key-checker **16/16 ALL PASS ×2 byte-identiques** md5 `7f626e87…` ; check_plan_protocol **P1-P5 PASS** — plan présent 19 114 car. · answer key 10 décisions/10 vérifications · worklog R5 + PLAN-AFFICHE même entrée — Horodatage vérifié : 2026-11-19T05:05:00Z)
