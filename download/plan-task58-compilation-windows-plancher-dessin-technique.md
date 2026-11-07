# Plan d'actions Task 58 — Différés propriétaire : branche compilation-windows (clé K3) · plancher dessin-technique ≥1.3.0 (évolution du skill)

**Générateur** : skill `gen-plan` v3.35.2 (mode **STEP** — directive propriétaire « gen-plan (step) : génère à nouveau le plan d'action actuel via mon skill gen-plan », 4ᵉ application règle d'or n°9 chemin a→d complet : PM SHARED v1.7.26 lu intégralement → installation PM-INSTALL voie directe rc=0 [pipeline preflight clone certifié 3ace5b5, pin b75a620 ancêtre] → certification arbitres → plan régénéré via le gen-plan fraîchement installé, règle d'or n°2). **Reprise 2026-11-07** (session web-c30e6506, directive « gen-plan (step): continue » après clôture Task 60) : E1-RES INSTALLE-REPARÉ (18ᵉ disparition vm auto-réparée) ; G1 requalifié EXÉCUTÉ-RECYCLÉ (détail §0-bis) ; G2/G3 restent à exécuter — ARRÊT step à la frontière G2.
**Session** : web-c30e6506 · **Date** : 2026-11-06 (reprise 2026-11-07) · **Exécution** : G1 → G2 (indépendance prouvée : écritures disjointes — G1 = ~/GitHub + distant cmdr + journal ; G2 = skills/dessin-technique + KB + pin arbitre + archive + miroir), G3 séquentiel, `correct-work(groupe)` après chaque groupe (max 2 rounds), `correct-work (projet) --bloc` en fin de chaîne (v3.22.0).

---

## §0 État d'ouverture (E1-RES — dérivé du disque, règle d'or n°5)

| Vérification préalable | Résultat |
|---|---|
| É1-INSTALL (garde n°9, préalable) | **INSTALLE-REPARÉ** rc=0 (version-management restauré — 14ᵉ matérialisation) → re-jeux **INSTALLE** ×2 (idempotent, 0 manquant, KB 52) |
| Installation PM INSTALL (directive ce tour, pin b75a620) | **FAITE — pipeline voie directe rc=0** : preflight `3ace5b5` (pin b75a620 ancêtre — descendant-tolérant règle d'or n°4), 52 skills + @historique 71 fichiers + scripts/ 281 fichiers syncés, garde R2 **0 rétrogradation**, archive rescellée round-trip (garde anti-perte 0 PM déplacé), F3 post-install **52/52 SHA-256, 0 divergence** |
| Certification (chemin c) | verify-cross **100 %** (0 WARN/0 ERR) · integrity **108/108 PASS ×2** · coherence **53 PASS/23 WARN/0 FAIL** · verify-correct-work **16/16** · tool-routing **PASS** · ensure-installed **INSTALLE ×2** · miroir KNOWLEDGE-repo `3ace5b5` porcelain 0 |
| G-RES (resource-monitor) | **OK → PARALLELE** (disque 7,1 Go libres, mémoire 2,5 Go disponibles, charge 0,0) |
| Clé propriétaire K3 (fournie ce tour) | **TESTÉE — auth 200 `bigleon2`**, perms **admin/maintain/push TRUE** sur `bigleon2/cmdr` ET `bigleon2/KNOWLEDGE` (sonde API lecture seule — KO-L001) ; jeton jamais persisté (inline one-shot, scan 0 secret pré-push) |
| État distant cmdr (dérivé API) | master **83d8c84** == pin manifeste · **`test/compilation-windows@04accb8` PRÉSENTE** (push Task 53 réussi — le 403 constaté Tasks 51-52 = ancienne clé, K3 le lève) · PR #1-#4 toutes closed (merged) · runs : 42258574189 failure (MSB3644, documenté Task 53) → 42259236575 **success** (2026-11-06T17:10Z) |
| Workflow compilation Windows | **WF 409580955** `.github/workflows/test-compilation-windows.yml` state **active** (re-run dispatchable via K3) |
| Arbre local ~/GitHub | **DÉTRUIT — 4ᵉ recyclage sandbox** (clone cmdr, ghorg, Go tarball, journal `etat-ghorg-ecosysteme.json` : à reconstruire) |
| dessin-technique (état disque) | **v1.1.1** installé (5 scripts Python : capture_forme, mise_a_echelle, generer_dessin, mesurer_filet, mesurer_profondeur) · `scripts/trigo-euler.cpp` + binaire **ABSENTS** — le nœud C++ du registre inter-scripts n'est pas matérialisé |
| Registre inter-scripts (source de vérité du nœud) | `trigo-euler` déclaré : binaire `skills/dessin-technique/scripts/trigo-euler`, source `.cpp`, compilation `g++ -O2 -std=c++17 -pthread -Wall`, interface json-ndjson, modes one-shot/stdin/daemon, daemon socket `/tmp/trigo-euler.sock` + ready/pid files + **max_clients 8**, **15 capacités** (trig.eval, trig.resoudre, canonique.cercle, canonique.ellipse, analyse.derivee, analyse.primitive, analyse.integrale, fourier.serie, fourier.eval, euler.formule, euler.rotation, euler.projection, euler.caracteristique, piece.profil_2d, piece.modele_iso), concurrent true, version_script 1.0.0 |
| Plancher déclaré | frontmatter inter-scripts : `dessin-technique >= 1.3.0` — **insatisfaisable** (installé 1.1.1, finding S3 Task 55 §7.1 : « monter dessin-technique » = la voie choisie par le propriétaire ce tour) |
| Outil compilation local | **g++ 14.2.0 présent** (Debian) — compilation trigo-euler faisable sur le profil |
| Diagnostic volatilité (nouveau, L55-3) | Le projet hôte est **auto-committé par la plateforme** par snapshots UUID (0a3b74a « 02b78679-… ») — un recyclage restaurant un snapshot antérieur explique les disparitions récurrentes de version-management (à consigner E15) |

**Requalification du différé 1 (règle d'or n°5 — état vérifiable)** : la branche `test/compilation-windows@04accb8` **est déjà sur le distant** (vérifié API ce tour) et la compilation Windows a déjà **succédé** (run 42259236575, Task 53). Le 403 des Tasks 51-52 concernait l'ancienne clé. Ce qui reste à corriger avec la clé K3 : **(a)** l'arbre local cmdr détruit (4ᵉ recyclage) ; **(b)** la re-validation de la fenêtre de compilation sur l'état courant (re-run du workflow) ; **(c)** le journal d'état détruit. La fusion éventuelle du workflow vers master reste décision propriétaire (hors périmètre §5).

---

## §0-bis Reprise 2026-11-07 (règle d'or n°5 — état vérifiable après clôture Task 60)

| Vérification de reprise | Résultat |
|---|---|
| É1-INSTALL (garde n°9) | **INSTALLE-REPARÉ** rc=0 (version-management — 18ᵉ disparition, auto-réparée garde Task 56) ; piliers Task 60 intacts : correct-work v2.11.0 · gen-plan v3.35.2 · pm-skill v1.0.0 · SHARED v1.7.28 · KB 53 entrées |
| G1 (compilation-windows) | **EXÉCUTÉ le 2026-11-06 22:18-22:23** (plan-task59 §0 : clone cmdr 83d8c84/04accb8 porcelain 0, run WF **42303936370 SUCCESS**, artefact 1 758 544 o, journal 22:22:57Z) — **puis RECYCLÉ** (5ᵉ recyclage sandbox : ~/GitHub + journal absents au 2026-11-07). **Requalification** : la correction du différé 1 est LIVRÉE (fenêtre de compilation validée sur l'état courant, branche publiée, run vert — preuves documentées plan-task59 §0) ; les artefacts LOCAUX (clone, journal) sont volatils par nature (L55-3) et leur reconstruction serait du travail jetable — consignés §5 comme pendances, D582-D584 statut done-documenté (preuves = documentation horodatée, plus le disque) |
| G2 (plancher dessin-technique v1.3.0) | **INTACT À FAIRE** : trigo-euler.cpp absent · preuves tmp/mission-task58/trigo-node/ absentes · dessin-technique v1.1.1 (5 scripts Python) · registre inter-scripts v1.0.0 présent (contrat du nœud : 15 capacités, modes, NDJSON, max_clients 8) · g++ à re-vérifier à l'exécution |
| G3 (clôture) | **À FAIRE** (après G2) |
| Décision step | **ARRÊT EXPLICITE à la frontière G2** — G2 = chantier lourd (nœud C++ + preuves + cascade, ~24 k#token planifiés) : confirmation propriétaire avant exécution (porte mode step) |
| **Reprise G2 (2026-11-07 suite 11 — 8ᵉ/9ᵉ directives)** | **PORTE FRANCHIE — EXÉCUTION AUTONOME** : « oui, puis exécute le reste de plan d'actions de façon autonome » + sémantique STEP clarifiée et enregistrée : `gen-plan (step)` = TOUJOURS autonome (aucune porte aux frontières), demande de validation UNIQUEMENT sur `gen-plan (step-ok)`. Incident de langue n°2 corrigé définitivement (9ᵉ directive — français exclusif dès le premier mot, toute reprise, tout canal) |
| **E13-5 (10ᵉ directive — affinage par les discussions d'origine)** | « pour affiner le skill "dessin-technique", tu peux relire les discussions [chat.z.ai/s/1de508c4…] et [chat.z.ai/s/55afc1b5…] » → **lues et intégrées à G2** (extraction tmp/mission-task58/discussions/) : (a) discussion « COOLING VOSS #2 » (2026-10-22) = session d'origine de la mission TRIGO-INTER-SCRIPTS — la v1.3.0 d'origine (bump v1.2.0, perdue au recyclage) répondait à la douleur du rendu z-ai **stochastique** (proportions/côtes/perspective non respectées) par la **voie géométrique déterministe** ; (b) discussion « Rasta Mouton » (2026-10-25) = livraison vue-upload share vérifié + fidélité par itération — voie de livraison confirmée, rien de structurel pour le moteur. **Lignage honnête** : la voie --geo Python (geometry_from_cotes.py + extension generer_dessin.py) de la v1.3.0 originale est PERDUE — documentée en §1.8 comme suggestion de reconstruction (suggestion ① de la discussion d'origine), hors contrat D585 (registre = nœud C++) |
| **E13-6 (11ᵉ directive — discussion 3 d'origine)** | « continue mais avant lis aussi la discussion [chat.z.ai/s/0d14e61c…] » → extraite et analysée (tmp/mission-task58/discussions/discussion-3.txt) : « VOSS COOLING » (07-13/10/2026) = **session d'origine du skill lui-même** (mission VOSS-C, v1.0.0 du 2026-10-13 — croisé avec @historique/historiques-par-skill/dessin-technique.md) : problème réel (joint VOSS 40 Nm dans carter alu qui se desserre), 7 photos de pièces, analyse hydraulique hiérarchisée, fiche atelier PDF (§4+§5), ordre d'assemblage 6 étapes (40/120 Nm). Les dessins techniques (dont joint_5c) dérivent de CES photos — la douleur d'origine de toute la chaîne TRIGO |
| **E13-7 (12ᵉ/13ᵉ directives — inventaire mathématique intégral des 3 discussions + dossiers)** | « prends en compte tout ce qui concerne les calculs mathématiques que mon skill dessin-technique doit intégrer, tu peux chercher des éléments pertinents dans les dossiers de ces projets » → **inventaire compilé et mappé aux 15 capacités** (consigné worklog suite 12) : (a) discussion 1 verbatim : trigonométrie, **équations canoniques**, primitives, dérivés, intégrales, **séries de Fourier**, **théorème d'Euler**, **la perspective**, « d'autres mathématiques » = Maclaurin/Fourier, algèbre linéaire (matrices rotation Euler), Simpson/**Gauss-Legendre 5 pts (1e-6)**, géométrie algorithmique ; ratio ellipse par **valeurs singulières** (bbox = faux), caps ≈ **sin 35,26°** (vérification mécanique), painter trié par profondeur, caps n′z>0, arcs moitié externe, arêtes locales, formatage français ; profil axial joint 5c (44,9 × 35,2 ; filet G Ø 28,5 × 22,7 ; O-ring 22,7→23,9 ; hexagone entre-pointes 35,2 × 23,9→33,8 ; filet D 34,5→41,9 ; bores Ø 15,4/12,0/6,0) ; (b) discussion 3 (dossiers projets croisés) : mission VOSS-C v1.0.0 (F1 monnaie circularité ≥ 0,60 / aspect 0,85-1,15 / échelle px/mm ; F2 s_i = part_i×surface/max_dim, commune = min ; F3 DNA verbatim + annotations PIL) ; Tasks 10-12 : F4 filetage (ACF par latitude — invariante de phase, ISO 261, tests vivants M12×1,75 / **M26×1,5 DKO VOSS** / Ø20-p12-φ35, remplissage bbox 0,785 vs 1,0) ; F5 profondeur (PCA ellipse, φ = acos(b/a), p = δ/(px_mm·sin φ), trou-ness 60 %/3 px/max(4, 0,2δ)) ; couples **40/120 N·m**, serrage 2 passes 30 %/100 %, rayon courbure ≥ 10×Ø — cotes N·m dans la chaîne de cotation (type « couple » de generer_dessin) ; (c) discussion 2 : rien de mathématique (livraison GIF — confirmé par relecture intégrale) ; (d) dossiers : registre (contrat 15 capacités = traduction mécanique), style-dna.json (palette DNA #d8d8f8/#b8b8c0/#a8a8b0/#4b4b51 + cotation Ø/mm/°), references/filets-normaux.md (ISO 261), pieces-centimes.md (Ø euros). **Mappage intégral → 15/15 capacités du nœud, aucun calcul orphelin** (détail worklog suite 12) |

---

## §1 Objectif (éléments restants de la discussion — règle d'or n°7)

Demandes du tour (couverture vérifiable — chaque élément ∈ {tâche, livrable, pendance}) :

1. « installe mon écosystème personnel … grâce à mon fichier {URL pin b75a620} » → **FAITE en préalable** (§0 : installation + certification) — chemin a→c règle d'or n°9.
2. « prend en compte mon skill gen-plan fraichement installé pour générer le plan d'actions … gen-plan (step) : génère à nouveau le plan d'action actuel » → **le présent document** (chemin d, règle d'or n°2 — KO-L005 : gen-plan v3.35.2 inchangé = version génératrice).
3. « corrige le différé "Fenêtres de compilation Branche" avec ma clé {K3} » → **G1** : restauration de l'arbre local cmdr, re-run de la fenêtre de compilation Windows (workflow_dispatch avec K3, verdict success attendu), journal d'état recréé.
4. « corrige le différé "Plancher dessin-technique ≥1.3.0" en faisant évoluant le skill » → **G2** : montée dessin-technique v1.1.1 → **v1.3.0** par matérialisation du nœud C++ `trigo-euler` (15 capacités, daemon NDJSON multi-clients) + cascade KO-L004 complète (L57-1 : 5 touches).
5. Clôture canonique → **G3** : correct-work (projet) --bloc + rapport final + RAPPELS OBLIGATOIRES + clone-chat.

---

## Answer key (hook E1)

```yaml
decisions:
  - id: "D581"
    libelle: "Installation PM INSTALL (pin b75a620) + certification — préalable du plan, exécutée ce tour avant génération"
    criterion: "Pipeline voie directe rc=0 (preflight 3ace5b5 ancêtre du pin, R2 0 rétrogradation, archive rescellée, F3 52/52 SHA 0 divergence) + batterie certification verte (verify-cross 100 %, integrity 108/108 ×2, coherence 53/23/0, correct-work 16/16, tool-routing PASS, ensure-installed INSTALLE ×2)"
    verification: "Sorties pipeline + arbitres au §0 du plan et au worklog (couplage horodatage) ; PM SHARED v1.7.26 lu intégralement (chemin a)"
    source: "Directive propriétaire : « installe mon écosystème personnel … grâce à mon fichier {URL b75a620} »"
    priority: S1
    status: done
    note_execution: "Exécuté en préalable 2026-11-06 (§0 + worklog suite 9)"
  - id: "D582"
    libelle: "Arbre local cmdr reconstruit (Karnaugh F1L0S0B0 → règle 2 : clone depuis le fork bigleon2/cmdr) — branche test/compilation-windows vérifiée == 04accb8 == distant"
    criterion: "Clone ~/GitHub/bigleon2/cmdr avec origin=fork (K3 inline one-shot, jamais persisté), upstream=cmdr-editor/cmdr, master == 83d8c84 == pin manifeste ; checkout test/compilation-windows ; diff local vs origin/test/compilation-windows == 0 (contenu inchangé)"
    verification: "git remote -v + rev-parse master/test + git status --porcelain 0 + diff origin 0 — journalisés"
    source: "4ᵉ recyclage sandbox : ~/GitHub détruit (constat §0) — différé 1 point (a)"
    priority: S1
    status: done
    note_execution: "Exécuté 2026-11-06 22:18 (clone 83d8c84/04accb8 porcelain 0 — plan-task59 §0) ; arbre recyclé au 5ᵉ recyclage sandbox 2026-11-07 — preuve = documentation horodatée (requalification §0-bis)"
  - id: "D583"
    libelle: "Fenêtre de compilation Windows re-validée : workflow_dispatch WF 409580955 (ref test/compilation-windows) avec K3 → run NEUF verdict success"
    criterion: "POST dispatches accepté (204) ; nouveau run créé sur la branche ; conclusion == success ; l'artefact cmdr-binaires-windows.zip est produit (SHA-256 journalisé)"
    verification: "API runs : id nouveau run > 42259236575, status completed, conclusion success ; artefact présent avec taille + SHA-256"
    source: "Différé 1 point (b) : re-validation sur l'état courant (le 403 historique est levé par K3 — perms push/admin vérifiées §0)"
    priority: S1
    status: done
    note_execution: "Exécuté 2026-11-06 : run WF 42303936370 SUCCESS, artefact 1 758 544 o (plan-task59 §0) — validation distante acquise, ne dépend pas du disque local"
  - id: "D584"
    libelle: "Journal d'état etat-ghorg-ecosysteme.json recréé (~/GitHub/_outils/) — état local restauré et traçable"
    criterion: "Journal JSON présent : clone cmdr (chemin, branches, SHAs vérifiés), dernier run compilation Windows (id + conclusion), horodatage ; ghorg/Go documentés comme non-reconstruits ce tour (hors périmètre du différé, consigné §5)"
    verification: "Fichier JSON valide (json.load OK) + champs vérifiables contre git/API réels"
    source: "Différé 1 point (c) : journal détruit avec ~/GitHub"
    priority: S2
    status: done
    note_execution: "Exécuté 2026-11-06 22:22:57Z puis journal recyclé (5ᵉ recyclage) — requalification §0-bis : reconstruction = travail jetable, consigné §5"
  - id: "D585"
    libelle: "dessin-technique v1.3.0 — nœud C++ trigo-euler matérialisé : source + binaire + preuves mécaniques"
    criterion: "scripts/trigo-euler.cpp créé (contrat registre : 15 capacités + echo + daemon.stop ; modes one-shot --request/--out, stdin, daemon --daemon --socket --ready-file --pid-file --max-clients ; NDJSON ; saturation non-bloquante « daemon sature ») ; compilé avec la commande EXACTE du registre (g++ -O2 -std=c++17 -pthread -Wall) ; preuves : 15/15 op vérifiées (une par capacité, valeurs contrôlées), daemon démarré via is_client.py (ready-file + health-check echo), concurrence 4 clients × 25 requêtes = 100/100 ok, saturation 8+1 → « daemon sature », daemon.stop propre (socket supprimée), orchestrer.py mini-plan (2 tâches, dép) exécuté ×2 idempotent (sha16 identiques)"
    verification: "Preuves dans tmp/mission-task58/trigo-node/ (journal + sorties) ; binaire présent ; re-jeu démontré"
    source: "Différé 2 : « corrige le différé Plancher dessin-technique ≥1.3.0 en faisant évoluer le skill » — registre inter-scripts v1.0.0 déclare le nœud (contrat)"
    priority: S1
    status: pending
  - id: "D586"
    libelle: "Cascade KO-L004 complète (5 touches, L57-1) — plancher satisfait mécaniquement"
    criterion: "(1) SKILL.md v1.3.0 : description += F6 nœud trigo-euler, §1.8 nouveau (F6), T7/T8 au tableau §1.5, §2 emplacements + stack C++ ; (2) evals.json v1.3.0 + T7 (self-test nœud) + T8 (concurrence daemon) ; (3) KB : entrée ## dessin-technique v1.3.0 (description F6 + ligne calibration Task 58) + mention skill-creator « Utilisé par » recalée v1.3.0 ; (4) pin arbitre ECO_SKILLS dessin-technique 1.1.1 → 1.3.0 (commentaire Task 58) ; (5) ligne historiques-par-skill v1.3.0 + archive v2.3 rescellée (piliers) ; puis sync miroir (commit) + re-certification integrity ×2 arbres + coherence + verify-correct-work ; plancher frontmatter inter-scripts >=1.3.0 satisfait (1.3.0 installé == déclaré)"
    verification: "integrity 108/108 ×2 arbres (le bump sans cascade échouerait : L57-1 integrity = détecteur unique) ; coherence sans FAIL ; verify-correct-work 16/16 ; git log miroir +1 commit Task 58"
    source: "Différé 2 (suite) : la montée de version d'un skill déclenche la cascade 5 touches (leçon L57-1)"
    priority: S1
    status: pending
  - id: "D587"
    libelle: "correct-work (projet) --bloc : 3 blocs (B1 compilation-windows / B2 plancher dessin-technique / B3 clôture)"
    criterion: "Mode bloc par bloc en fin de chaîne ; verdict global = pire des blocs ; findings corrigés en vol (max 2 rounds)"
    verification: "Rapport correct-work --bloc Task 58 dans download/ ; 3× PASS → global PASS"
    source: "Protocole mode step (v3.22.0) reconduit (Tasks 55/56/57)"
    priority: S1
    status: pending
  - id: "D588"
    libelle: "Rapport final + RAPPELS OBLIGATOIRES propriétaire + clone-chat scellé + worklog (R5)"
    criterion: "download/rapport-final-task58.md (couverture 5/5 demandes, état final dérivé du disque) ; rappels en tête : rotation PAT K1/K2/K3 + GHORG_GITHUB_TOKEN (13ᵉ+ expositions — K3 fournie ce tour) · GO push miroir (59a5805 + 1e7e541 + 2adbd7a + 3ace5b5 + commit Task 58) · ghorg/Go non reconstruits · F1 import Traktor · F3 décision P1b · option fusion workflow → master ; clone-chat scellé download/clone-discussion-2026-11-06-task58.md"
    verification: "Fichiers présents + worklog complété + leçons knowledge-observer (E15 : cause racine volatilité snapshots UUID)"
    source: "Clôture canonique (Pendances Task 57 §3 reconduites + leçons E15)"
    priority: S1
    status: pending
```

---

## §2 Groupes et tâches

### G1 — Branche compilation-windows (clé K3) — indépendant de G2
- **SG1.1** Re-clone cmdr (Karnaugh F1L0S0B0 → règle 2) : `git clone` du fork avec K3 inline one-shot → `~/GitHub/bigleon2/cmdr` ; `git remote add upstream https://github.com/cmdr-editor/cmdr` ; vérifs : master == 83d8c84 == pin manifeste ecosystem/manifest.yaml, porcelain 0.
- **SG1.2** Branche test : `git fetch origin test/compilation-windows` → checkout → rev-parse == 04accb8 == distant (requalification §0 : contenu déjà publié — aucune écriture de contenu nécessaire, jamais de force-push).
- **SG1.3** Re-run fenêtre de compilation : POST `/repos/bigleon2/cmdr/actions/workflows/409580955/dispatches` (K3, ref `test/compilation-windows`) → attente sonde API (conclusion attendue success — workflow inchangé depuis le run 42259236575 vert) ; artefact SHA-256 journalisé.
- **SG1.4** Journal `~/GitHub/_outils/etat-ghorg-ecosysteme.json` recréé (clone cmdr vérifié, run frais, horodatage) + consignation ghorg/Go non-reconstruits.

### G2 — Plancher dessin-technique v1.3.0 (évolution du skill) — indépendant de G1
- **SG2.1** `skills/dessin-technique/scripts/trigo-euler.cpp` : implémentation du contrat registre — 15 capacités (trig.eval, trig.resoudre [triangle rectangle], canonique.cercle, canonique.ellipse, analyse.derivee [différences centrées], analyse.primitive [poly formelle / Simpson], analyse.integrale [Simpson adaptatif], fourier.serie [coefficients par intégration], fourier.eval, euler.formule [complexe], euler.rotation [matrice ZXZ + quaternion], euler.projection [iso CAO/orthographique], euler.caracteristique [angle/axe/quaternion], piece.profil_2d [aires/inerties], piece.modele_iso [faces flat-shaded boîte/cylindre]) + `echo` (health-check) + `daemon.stop` ; modes one-shot/stdin/daemon ; NDJSON ; saturation max_clients 8 → « daemon sature » non-bloquant ; réponses déterministes (idempotence R3).
- **SG2.2** Compilation (commande EXACTE du registre) + preuves `tmp/mission-task58/trigo-node/` : 15/15 op contrôlées ; is_client.py one-shot + daemon demarrer/etat/arreter ; concurrence 4×25 = 100/100 (ThreadPool) ; saturation 8+1 ; orchestrer.py mini-plan ×2 idempotent (sha16).
- **SG2.3** SKILL.md v1.3.0 (§1.8 F6, T7/T8, §2, description, tags/read_when += trigo-euler) + evals.json v1.3.0 (T7/T8).
- **SG2.4** Cascade KO-L004 5 touches (D586) + sync miroir + commit + re-certification ×2 arbres.

### G3 — Clôture (après G1+G2)
- **SG3.1** correct-work (projet) --bloc : B1 (G1) / B2 (G2) / B3 (clôture).
- **SG3.2** Rapport final `download/rapport-final-task58.md` + RAPPELS OBLIGATOIRES + worklog.
- **SG3.3** clone-chat scellé `download/clone-discussion-2026-11-06-task58.md`.

---

## §3 Budget #token (E4) et profil (E6)

~42 k#token (G1 ~8 k · G2 ~24 k · G3 ~10 k) × 1,3 pire cas ≈ **55 k**. Profil **NORMAL / PARALLELE** (G-RES OK §0). Skills mobilisés (E5) : gen-plan v3.35.2 (porteur), inter-scripts v1.0.0 (registre + is_client + orchestrer — preuves G2), correct-work v2.9.0 (portes step + --bloc), clone-chat v2.0.2 (clôture), knowledge-observer (leçons E15), resource-monitor (hook E1-RES — collecté §0), script-creator (conventions d'écriture du nœud C++).

## §4 Risques et adaptations (règle d'or n°1)

- Recyclage sandbox en cours de chaîne (4ᵉ recyclage constaté ce tour — snapshots UUID) → reprise E1-RES (garde auto-réparante, preuves vivantes ×4) ; le plan est rejouable.
- Clé K3 exposée au canal (13ᵉ+ exposition) → JAMAIS persistée sur disque ni dans un commit (inline one-shot), scan `github_pat_/ghp_/gho_` sur les arbres avant tout push, RAPPEL rotation en clôture.
- Échec du re-run Actions → diagnostic (le run 1 historique 42258574189 = MSB3644 documenté et corrigé sans toucher au code par 71138eb+fix ; le workflow est inchangé depuis le run vert) ; en cas d'échec : logs analysés, correction uniquement si cause nouvelle, jamais de contournement silencieux.
- Échec compilation g++ / preuves C++ → max 2 rounds de correction (correct-work(groupe)) ; au-delà : ABANDON honnête documenté + différé re-consigné (R3 — jamais de résultat fabriqué).
- Fusion workflow → master : hors périmètre (§5) — recommandation seule.

## §5 Hors périmètre (différés/propriétaire)

Fusion du workflow compilation Windows vers master (décision propriétaire — la branche test reste la référence) · reconstruction ghorg + Go tarball (binaire outil — pendance propriétaire existante, documentée au journal D584) · push distant KNOWLEDGE (GO propriétaire — KO-L009 point 5 : commits 59a5805 + 1e7e541 + 2adbd7a + 3ace5b5 + commit Task 58) · F1 import Traktor côté propriétaire · F3 décision complément P1b · rotation PAT K1/K2/K3 + GHORG_GITHUB_TOKEN (RAPPEL clôture).

---

## Hooks de validation (E8)

Horodatage plan : 2026-11-06T22:15:00Z

Verdict E8 : PASS (P1 plan présent · P2 answer key 8 décisions/8 vérifications · P3 worklog R5 · P4 PLAN-AFFICHE · P5 frais — Horodatage vérifié : 2026-11-06T22:15:00Z)
