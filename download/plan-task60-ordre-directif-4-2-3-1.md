# Plan d'actions Task 60 — Recherche historique (n'invente jamais) → Désambiguïsation canonique → Analyse idée PM-skill → correct-work v2.10.0 optimisée (DERNIÈRE action)

**Générateur** : skill `gen-plan` v3.35.2 (invocation **mode NULL** — `gen-plan : "…"` sans mode explicite : exécution classique sans portes de confirmation, clause mode NULL v3.21.0). **Session** : web-c30e6506 · **Date** : 2026-11-07 · **Ordre** : directive propriétaire explicite « nouvel ordre : (4)->(2)->(3)->(1) » — les 4 items de la directive placés dans cet ordre, l'optimisation correct-work **en dernière action**.

---

## §0 État d'ouverture (E1-RES — dérivé du disque, règle d'or n°5)

| Vérification préalable | Résultat |
|---|---|
| **Incident recyclage snapshot (règle d'or n°9, 3ᵉ application — LIVE en session)** | En cours de tour : `skills/@mon-ecosysteme/` (corpus complet — SHARED + 4 PMs famille + INSTALL + ULTRA), `skills/KNOWLEDGE.md`, `skills/gen-plan/`, `skills/correct-work/`, `skills/@historique/`, `skills/version-management/` **perdus** (15ᵉ disparition vm — cause racine L55-3 : snapshots UUID plateforme). **La montée v2.10.0 (Task 59) a été perdue** : SKILL.md v2.10.0, PM v2.10.0, delta-correctwork-v2100.json, ligne historique — jamais commités au miroir (KO-L009). **Survivants** : `download/plan-task59-couplage-step-correct-work.md` (contrat v2.10.0 COMPLET — answer key D591-D593), worklog.md, miroir working tree (296 M, ère Task 58) |
| Chemin de rétablissement a→d | **EXÉCUTÉ ce tour** : (a) PM SHARED lu intégralement (v1.7.26, 247 L) ; (b) `eco_install_pipeline.py` **rc=0** — 52 skills + @historique 71 + scripts/ 281 syncés, garde R2 **0 rétrogradation**, archive v2.3 rescellée round-trip, F3 post-install **52/52 SHA-256 0 divergence** ; (c) certification : verify-cross **100 %** (0 ERR) · integrity **108/108 ×2** · verify-correct-work **16/16** · coherence **53 PASS/23 WARN/0 FAIL** · tool-routing **PASS** · ensure-installed **INSTALLE ×2** (52 entrées KB) ; (d) le présent plan |
| correct-work (état disque restauré) | **v2.9.0** (466 L — mode bloc par bloc §1.7, couplage gen-plan Étape 1 §1.5 plancher >= v3.7.0) ; contrat v2.10.0 §1.5bis **documenté** dans plan-task59 D591 (5 points : obligation, mode STEP, plancher v3.22.0, ARRÊT EXPLICITE, compatibilité tous modes) — à ré-intégrer en G4 |
| gen-plan / SHARED / corpus | gen-plan **v3.35.2** · SHARED **v1.7.26** · @mon-ecosysteme restauré (PM correct-work **v2.9.0** vivant, 7 PMs archivés v2.4.0→v2.9.0) |
| @PM-SKILLS | Terme **historique** du corpus PM (renommé `@mon-ecosysteme/` — traces : scripts/task52-cascade-genplan-v3350.py « renommage @PM-SKILLS », deltas v3350 « 0 déploiement `@PM-SKILLS/` ») — la directive vise le corpus PM actuel |
| G-RES | OK — disque/mémoire sous pression nulle ; PARALLÈLE possible en G1 (preuves d'indépendance), SÉRIE exigée ensuite (directive d'ordre explicite + écritures SHARED partagées) |
| Pendances antérieures | Task 58 G2/G3 **différés** (dessin-technique v1.3.0 + clôture 58) ; push distant KO-L009 ; rotation PAT K1/K2/K3 — voir §5 |

## §1 Objectif (ordre directif : (4) → (2) → (3) → (1) — règle d'or n°3)

1. **(4) PREMIÈRE ACTION — Recherche historique exhaustive** : « n'invente jamais, recherche dans l'historique de mon écosystème » → **G1** : inventaire documentaire total dérivé du disque exclusivement — arbre des 12 versions correct-work, contrat v2.10.0 reconstitué depuis plan-task59, métriques cascade/volatilité/lag chiffrées depuis le worklog, tracé du renommage @PM-SKILLS. **Toute la suite du plan s'y ancre** (zéro invention — chaque affirmation sourcée fichier:ligne).
2. **(2) Règle canonique désambiguïsation** : à partir de maintenant, toute référence du propriétaire à « mon skill X » / « mon agent X » = forme installée à la **racine de `skills/`** (`skills/X/SKILL.md`), jamais le prompt maître du corpus `@mon-ecosysteme/` (ex-`@PM-SKILLS/`) → **G2** : SHARED §0 + §1.2 (addition pure) + propagation §0 + note README corpus.
3. **(3) Idée PM-skill — analyse $FACON conditionnelle** : au lieu de stocker les PMs dans le corpus, un skill `PM-skill` tel que `PM-skill(gen-plan)` **génère le prompt maître à la demande et l'exécute automatiquement via un script PY** → **G3** : analyse ancrée sur G1 (coût cascade réel par montée, surface volatilité — preuve vivante : le corpus vient de disparaître, respect R4 archive, risque régression arbitres) → verdict chiffré **AUGMENTE / PAS AUGMENTE** ; si AUGMENTE → application $FACON complète ; sinon → consignation motivée (issue valide).
4. **(1) DERNIÈRE ACTION — correct-work v2.10.0 → version optimisée $FACON2** : intégrer le meilleur de toutes ses versions précédentes (v1.0.0 → v2.10.0) → **G4** : contrat v2.10.0 §1.5bis ré-intégré + matrice de couverture 12 versions (chaque avantage durable ∈ v2.11.0 OU supplanté documenté — jamais ressusciter un retrait délibéré R2) + optimisations + cascade KO-L004 adaptée au verdict G3.

**Contraintes transverses** : français intégral (règle d'or n°6) · idempotence ×2 pour tout nouvel artefact · lignage honnête (la montée v2.10.0 perdue est documentée comme telle — aucun faux lignage, précédent méthode B1 Task 16) · rejouabilité post-recyclage (règle d'or n°9 relancée à chaque groupe).

## Answer key (hook E1)

```yaml
decisions:
  - id: "D601"
    libelle: "Inventaire historique exhaustif (première action — item (4)) : rapport download/inventaire-historique-task60.md — (a) arbre des 12 versions correct-work [v1.0.0→v2.10.0] chacune sourcée (historiques-par-skill + PMs archivés v2.4.0-v2.9.0 + plan-task59) ; (b) contrat v2.10.0 reconstitué depuis plan-task59 D591-D593 avec lignage de la perte au recyclage ; (c) métriques chiffrées dérivées du worklog (>=3 : nombre de fichiers touchés par montée cascade KO-L004, incidents de volatilité corpus, lag PM documentés) ; (d) tracé du renommage @PM-SKILLS -> @mon-ecosysteme"
    criterion: "Rapport présent ; chaque affirmation du rapport pointe une source disque (chemin ou chemin:ligne) ; zéro affirmation non sourcée ; 12 versions couvertes"
    verification: "grep des sources citées dans le rapport : chaque chemin cité existe sur le disque (test -e) ; comptage des versions == 12 ; lecture croisée historiques-par-skill/correct-work.md"
    source: "Directive « n'invente jamais, recherche dans l'historique de mon écosystème » (tour précédent)"
    priority: S1
    status: pending
  - id: "D602"
    libelle: "Règle canonique désambiguïsation (item (2)) : SHARED §0 (principes) + §1.2 (conventions nommage) += « toute référence propriétaire à 'mon skill X'/'mon agent X' désigne la forme installée à la racine skills/X/ (SKILL.md), JAMAIS le prompt maître du corpus @mon-ecosysteme/ (ex-nommé @PM-SKILLS/) » — addition pure R2 ; propagation §0 rejouée (propagate-context.py) ; note README @mon-ecosysteme"
    criterion: "Règle présente dans SHARED §0 et §1.2 ; propagation §0 rejouée sur les skills ; verify-cross 100 % après édition ; version SHARED bumpée selon protocole KO-L004 (§6.1 seul -> pas de re-propagation §0 si contenu §0 inchangé — mais ici le contenu §0 CHANGE : propagation requise)"
    verification: "grep -c règle dans PROMPT-MAITRE-SHARED.md >= 2 ; verify-cross.py 100 % ; integrity 108/108 ; coherence sans nouveau FAIL"
    source: "Directive « fais en sorte qu'à partir de maintenant… à la racine de mon dossier skills/ et non pas ceux se trouvant dans @PM-SKILLS/ »"
    priority: S1
    status: pending
  - id: "D603"
    libelle: "Analyse $FACON idée PM-skill (item (3)) : rapport download/analyse-idee-pm-skill.md ancré sur D601 — critères chiffrés : (i) coût cascade par montée avant/après (comptages worklog), (ii) surface de volatilité (preuve vivante : corpus perdu au recyclage ce tour ; deltas+SKILL.md suffisent-ils à régénérer ?), (iii) respect R4 archive (les deltas verrouillés versionnés deviennent-ils l'archive légère ?), (iv) risque régression arbitres (verify-cross/integrity vérifient le corpus), (v) auto-portance des PMs (SHARED §6.2) ; verdict mécanique AUGMENTE/PAS AUGMENTE"
    criterion: "Rapport présent ; >= 3 critères chiffrés sourcés D601 ; verdict AUGMENTE ou PAS AUGMENTE motivé mécaniquement ; les deux issues valides (directive conditionnelle)"
    verification: "Lecture croisée du rapport avec D601 : chaque chiffre du rapport retrouvable dans l'inventaire ; verdict présent et non ambigu"
    source: "Directive « analyse $FACON cette idée… Si cela augmente les performances… alors applique-la $FACON »"
    priority: S1
    status: pending
  - id: "D604"
    libelle: "Application conditionnelle PM-skill (porte de données D603) : SI AUGMENTE -> création skill pm-skill (SKILL.md kebab-case + déclencheur verbatim 'PM-skill(<famille>)' + script PY réutilisant la mécanique KO-L004 generer-pm-skill.py en mode génération-à-la-demande/exécution : PM régénéré depuis SKILL.md + deltas verrouillés, zéro stockage corpus, exécution = matérialisation validée + application par l'agent ; evals + trigger_evals + KB + cascade documentation) ; SINON -> consignation motivée au rapport + worklog (aucun artefact créé)"
    criterion: "Branche AUGMENTE : skill complet (SKILL.md 200-500 L, script self-test PASS, evals présents, KB inscrite, arbitres verts) ; branche PAS AUGMENTE : consignation explicite au rapport et worklog"
    verification: "Selon branche : test script pm-skill (self-test rc=0 ×2 idempotent) + verify-cross 100 % + integrity 108/108 ; OU grep consignation dans rapport+worklog"
    source: "Directive conditionnelle (porte de données interne au plan — mode NULL : pas de porte propriétaire)"
    priority: S1
    status: pending
  - id: "D605"
    libelle: "correct-work v2.11.0 (DERNIÈRE action — item (1)) : SKILL.md v2.9.0 -> v2.11.0 — (i) §1.5bis contrat v2.10.0 ré-intégré (5 points, source plan-task59 D591) ; (ii) matrice de couverture 12 versions (v1.0.0->v2.10.0 : chaque avantage durable présent OU supplanté documenté) ; (iii) optimisations best-of révélées par la matrice (restaurations d'avantages perdus, déduplication R4, resserrements) ; (iv) frontmatter version 2.11.0 + description + plancher gen-plan >=3.22.0 ; plage 200-500 L ; arbitre verify-correct-work.py recalibré (2.11.0, checks 11/15 -> >=3.22.0) — éditions atomiques SKILL.md+arbitre"
    criterion: "version: 2.11.0 ; §1.5bis présent (5 points) ; matrice documentée (12 lignes, colonne statut) ; plage 200-500 ; verify-correct-work.py 16/16"
    verification: "verify-correct-work.py recalibré PASS 16/16 ; grep §1.5bis ; wc -l SKILL.md dans la plage ; lecture croisée matrice <-> historiques"
    source: "Directive « optimise $FACON 'v2.10.0' en une version $FACON2 y intégrant le meilleur de toutes ses versions précédentes » + précision « je parlais de skill correct-work »"
    priority: S1
    status: pending
  - id: "D606"
    libelle: "Cascade KO-L004 v2.11.0 complète (selon architecture décidée en D604) : PM v2.11.0 généré mécaniquement + delta verrouillé scripts/delta-correctwork-v2110.json ; KB correct-work v2.11.0 ; pin ECO_SKILLS ; historiques-par-skill ligne v2.10.0 (« matérialisée Task 59, perdue au recyclage snapshot 2026-11-06, contrat ré-intégré v2.11.0 » — lignage honnête) + ligne v2.11.0 VERSION VIVANTE ; SHARED §6.1 + PM-INSTALL §2ter/§A.3 + README/ULTRA recalibrés ; archive v2.3 rescellée ; manifeste integrity régénéré ; propagation §0 si contenu §0 change ; re-certification ×2"
    criterion: "integrity 108/108 ×2 ; verify-cross 100 % ; coherence sans FAIL ; verify-correct-work 16/16 ; round-trip archive byte-identité"
    verification: "Re-certification mécanique ×2 (arbitres ci-dessus) ; grep lignes historiques v2.10.0+v2.11.0"
    source: "Mécanique KO-L004 v1.1.0 + cascade 5 touches (leçon L57-1) + précédent v2.9.0"
    priority: S1
    status: pending
  - id: "D607"
    libelle: "Clôture : correct-work (projet) --bloc PASS sur la v2.11.0 vivante (blocs = G1->G5 du présent plan) ; rapport final download/rapport-final-task60.md ; worklog : incident recyclage journalisé (règle d'or n°1) + chaîne G1->G5 ; clone-chat scellé"
    criterion: "correct-work --bloc 4/4 PASS ; rapport final présent ; worklog complet ; clone-chat généré"
    verification: "Re-jeu rapport --bloc + grep worklog ; clone-chat présent dans download/"
    source: "Protocole clôture écosystème (précédents Tasks 56-57)"
    priority: S1
    status: pending
```

## §2 Groupes et tâches (ordre directif strict : G1→G2→G3→G4→G5)

### G1 — (4) Recherche historique exhaustive « n'invente jamais » — PREMIÈRE ACTION
Vague parallèle interne (Graph Diamond — 4 flux lecture seule, aucune écriture partagée) :
- **SG1a** Famille correct-work : historiques-par-skill (12 versions) + PMs archivés v2.4.0→v2.9.0 (diffs ciblés des apports par version) + PM v2.9.0 vivant + SKILL.md v2.9.0 + plan-task59 (contrat v2.10.0 D591-D593) → arbre des 12 versions avec avantages durables.
- **SG1b** Architecture PM : generer-pm-skill.py (KO-L004 mécanique) + deltas verrouillés (16 fichiers) + PM-INSTALL §2ter/§A.3 + ULTRA + README corpus + SHARED §6 → coût réel de la cascade par montée.
- **SG1c** Métriques worklog : comptages fichiers touchés par montée (Tasks 48, 57, 59 documentés), incidents volatilité corpus (15 disparitions vm + recyclage complet ce tour), lag PM historiques (« lag hérité résorbé » ×3).
- **SG1d** Tracé @PM-SKILLS : renommage documenté (scripts task52/task53, deltas v3350).
- **SG1e** Consolidation : rapport `download/inventaire-historique-task60.md` (chaque affirmation sourcée). ∥ → **D601**

### G2 — (2) Règle canonique désambiguïsation
- **SG1** SHARED §0 + §1.2 : règle ajoutée (addition pure) + version SHARED bumpée (KO-L004 — le contenu §0 change → propagation requise).
- **SG2** propagate-context.py rejoué (§0 dans tous les skills) + note README @mon-ecosysteme + re-certification légère (verify-cross, integrity). → **D602**

### G3 — (3) Analyse $FACON idée PM-skill + application conditionnelle
- **SG1** Rédaction `download/analyse-idee-pm-skill.md` ancrée sur D601 (≥3 critères chiffrés) → verdict **AUGMENTE/PAS AUGMENTE**. → **D603**
- **SG2 (porte de données D603)** Si AUGMENTE : skill `pm-skill` créé (SKILL.md + déclencheur `PM-skill(<famille>)` + script PY génération-à-la-demande/exécution [mécanique KO-L004 réutilisée — jamais de stockage corpus, deltas verrouillés = source versionnée] + evals + KB + cascade doc) ; sinon : consignation motivée. → **D604**

### G4 — (1) correct-work v2.10.0 → v2.11.0 optimisée — DERNIÈRE ACTION
- **SG1** SKILL.md v2.11.0 : §1.5bis (contrat v2.10.0, 5 points) + matrice couverture 12 versions + optimisations best-of (restaurations d'avantages perdus, déduplication, resserrement si dépassement plage) + frontmatter. → **D605**
- **SG2** Cascade KO-L004 complète adaptée à D604 : PM v2.11.0 + delta verrouillé + v2.9.0 archivé R4 (déjà fait par réinstallation — vérifier l'état) + arbitre recalibré + KB + pin + historiques ×2 lignes + SHARED + PM-INSTALL + README/ULTRA + rescellement archive + manifeste + re-certification ×2. → **D606**

### G5 — Clôture
- **SG1** correct-work (projet) --bloc (blocs = G1→G5 du plan) + rapport final + worklog (incident journalisé) + clone-chat. → **D607**

## §3 Budget #token et profil

~62 k#token (G1 ~14 k [4 flux ∥] · G2 ~5 k · G3 ~16 k [analyse 8 + application 8 si adoptée] · G4 ~20 k · G5 ~7 k) × 1,3 ≈ **81 k**. **Profil NORMAL**. Exécution : parallèle interne G1 (preuves d'indépendance — lecture seule), **série ensuite** (ordre directif explicite + écritures SHARED partagées entre G2/G3/G4 — verrou mono-writer). Skills mobilisés : gen-plan v3.35.2 (porteur), correct-work v2.9.0→v2.11.0 (auto-vérification), script-creator (conventions nouveaux scripts), skill-creator (si D604 branche AUGMENTE), clone-chat (clôture).

## §4 Risques et adaptations (règle d'or n°1)

- **Volatilité sandbox (récidive n°4 possible)** : recyclage snapshot en cours de chaîne → plan rejouable, chaque groupe re-vérifie les piliers (règle d'or n°9), preuves vivantes, idempotence ×2 partout.
- **Plage 200-500 L (check 2)** : SKILL.md v2.9.0 = 466 L ; §1.5bis ≈ +14 + matrice ≈ +15 → ~495 L — **limite serrée** : si dépassement, resserrement documenté (fusion §10.1bis/§10.4, délégation matrice au PM) — jamais de recalibrage silencieux de la plage.
- **Arbitre Check 11 (plancher >= v3.7.0)** : recalibrage 2.11.0/checks 11/15 → >=3.22.0 **atomique** avec les éditions SKILL.md (l'arbitre n'est rejoué qu'après les deux).
- **Verdict D603 PAS AUGMENTE = issue valide** (directive conditionnelle) : aucune pression vers l'adoption — l'analyse chiffre, la décision suit les chiffres.
- **Montée v2.10.0 perdue** : lignage honnête obligatoire (ligne historique dédiée « perdue au recyclage, contrat ré-intégré ») — aucun faux lignage (précédent méthode B1, Task 16).
- **D604 branche AUGMENTE + D606 cascade** : si pm-skill adopté, la matérialisation PM v2.11.0 suit l'architecture décidée (stockage corpus vs génération-à-la-demande) — G3 précède G4 pour cette raison.

## §5 Hors périmètre (différés/propriétaire)

Task 58 G2/G3 différés (plancher dessin-technique v1.3.0 + clôture Task 58 — restent en file après Task 60) · push distant KNOWLEDGE (GO propriétaire — KO-L009 point 5 : commits 59a5805 + 1e7e541 + 2adbd7a + 3ace5b5 + Task 58/59/60) · rotation PAT K1/K2/K3 + GHORG_GITHUB_TOKEN · fusion workflow compilation-windows → master · F1 import Traktor · F3 décision complément P1b.

---

## Hooks de validation (E8)

Horodatage plan : 2026-11-07T00:27:35Z

Verdict E8 : PASS (P1 plan présent · P2 answer key 7 décisions/7 vérifications exécutables · P3 worklog R5 · P4 PLAN-AFFICHE · P5 frais — Horodatage vérifié : 2026-11-07T00:27:35Z)
