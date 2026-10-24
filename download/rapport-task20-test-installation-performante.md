# Rapport — Task 20 : test de performance de l'installation de $ECO-LEON

> **Session** : web-fdf5963c · **Date** : 2026-10-23 · **gen-plan** : v3.23.2 (mode NULL — exécution classique)
> **Directive propriétaire** : `gen-plan : "test si l'installation de $ECO-LEON est performante"` — **expansion alias appliquée à la lecture** (registre `skills/@historique/@Alias/aliases.json`, G2 plan Task 19) : *test si l'installation de mon écosystème personnel est performante*.
> **Plan** : `download/plan-task20-test-installation-performante.md` (answer key D001-D012, seuils §5) · **Harnais** : `scripts/task20-tests-installation.py` (T1-T9) · **Relevé machine** : `scripts/task20-tests-report.json`.
> **Cible** : le PROFIL INSTALLÉ (`/home/z/my-project/skills/` — projection hôte Task 18) ET le PROCESSUS d'installation (exécuteur canonique `scripts/eco_install_pipeline.py`, PM-INSTALL v1.8.0 voie directe, pin b75a620).

## §1 — Verdict

# ✅ PERFORMANT

**L'installation de mon écosystème personnel EST performante** au sens de la définition opérationnelle à 5 axes du plan (§2) : complète, intègre, fonctionnelle, rapide et sûre, idempotente au niveau byte. Le verdict est atteint **à l'issue d'une boucle E12-E13** (1 round de correction, dans la limite des 2 autorisés) : la première campagne a rendu le verdict *PARTIELLEMENT PERFORMANT* en raison de trois findings réels (§4) dont deux ont été corrigés dans la session (F1, F3) et un documenté comme comportement de conception (F2) ; la campagne de re-mesure confirme **PERFORMANT** sur tous les critères S1/S2. La réponse est donc nuancée mais tranchée : **oui — et le test lui-même a amélioré le système testé** (c'est la fonction d'une campagne de tests sérieuse).

## §2 — Méthodologie

La question « installation performante ? » a été opérationnalisée en 5 axes mesurables (plan §2), testés par 9 tests mécaniques (T1-T9) exécutés par un harnais unique auto-suffisant, avec snapshots SHA-256 de l'arbre projeté (hors `__pycache__` — artefacts de compilation) autour de chaque exécution de l'installeur. Les seuils de verdict (plan §5) : **PERFORMANT** ⟺ axes d'état (D002-D007) tous vérifiés ET processus (D008 : preflight, garde R2, purges 0, durée < 60 s) ET idempotence byte (D009) ; **PARTIELLEMENT PERFORMANT** ⟺ état sain mais processus/imperfections ; **NON PERFORMANT** ⟺ au moins un échec S1 d'état. Toutes les mesures sont consignées au relevé machine `scripts/task20-tests-report.json` (régénéré à chaque campagne, écrit après les runs — jamais synchronisé pendant la session).

## §3 — Résultats par axe (campagne finale)

| Axe | Test | Résultat | Décision |
|-----|------|----------|----------|
| Complétude | T1 — inventaire dérivé du registre KB (périmètre dynamique KO-L003, jamais de liste figée) | **34/34 skills écosystème projetés** au profil hôte, 0 manquant, 0 divergence de version (host = dépôt partout) | D002 ✅ |
| Intégrité | T2 — arbitre d'intégrité depuis la projection hôte (`--check`, lecture seule) | **72/72 PASS, 0 FAIL** (0,04 s) — re-certification de l'état laissé par la Task 18 | D003 ✅ |
| Intégrité (source) | T3 — certification complète du dépôt (5 arbitres orchestrés + tool-routing) | **rc 0 — VERDICT : CERTIFICATION COMPLÈTE : ALL PASS (6/6)** (0,49 s) | D004 ✅ |
| Fonctionnalité | T4 — gen-plan hôte v3.23.2 | frontmatter 6/6 champs, déclencheurs 5/5 (gen-plan(step), plan d'actions, E15, É1-INSTALL, correct-work), 381 lignes ; **garde É1-INSTALL : verdict INSTALLE, rc 0, 0 fichier manquant, 34 entrées KB** | D005 ✅ |
| Fonctionnalité | T5 — arbitre correct-work (forme installée hôte) | **16/16 ALL PASS, rc 0** (0,02 s) | D006 ✅ |
| Fonctionnalité | T6 — alias-eco v1.0.0 | **selftest 15/15 rc 0**, `--list` rc 0, registre vivant : 7 phrases, trié, dédupliqué strict, **ECO-LEON = « mon écosystème personnel »** ; la résolution à la lecture est démontrée en direct (le message propriétaire a été expansé à l'ouverture de la session) | D007 ✅ |
| Performance (processus) | T7 — ré-installation instrumentée run 1 | **rc 0, 0,10 s** (seuil < 60 s), preflight pin b75a620 OK (descendant-tolérant), garde R2 « 0 rétrogradation — host ≤ repo partout », **purges []**, diff A→B : **0 modifié, 0 supprimé, 0 nouveau** ; certification post-install (étape 9 canonique) rc 0 | D008 ✅ |
| Idempotence | T8 — run 2 + convergence | **rc 0, 0,10 s** — diff B2→C : 1 modifié (le seul manifeste d'état par arbre — classe F2 documentée), 0 supprimé, 0 nouveau ; **manifeste convergent inter-cycles : OUI** ; **archive byte-stable : OUI** | D009 ✅ |
| Mesures | T9 — relevés consolidés | cf. §5 | D010 ✅ |

**Answer key finale** : D001 ✅ (harnais `task20-answer-key-check.py` 16/16 rc 0 — validé à E8 avant exécution) · D002-D009 ✅ (tableau ci-dessus) · D010 ✅ (§5) · D011 ✅ (le présent rapport, verdict + seuils appliqués + traçabilité) · D012 ✅ (§6-§7 : registre tenu, worklog, E15).

## §4 — Findings et correctifs (boucle E12-E13, round 1/2)

La première campagne (conservée dans le fil de session) a produit le verdict *PARTIELLEMENT PERFORMANT* : état installé parfait (T1-T6 identiques), mais processus imparfait. Trois findings, analysés jusqu'à leur cause racine :

### F1 (S3 — corrigé) : purge combattant la sync — shim certifié dans la liste NON_CANONIQUES
- **Constat** : chaque exécution de l'installeur rapportait `purges: ['scripts/verify-correct-work.py']` alors que le fichier reparaissait au run suivant.
- **Cause racine** : `scripts/verify-correct-work.py` à la racine du dépôt est un **shim de compatibilité certifié** (décision S2-α Task 12, re-validée propriétaire 2026-10-10 : délégation pure à l'arbitre canonique du skill, refus explicite rc=64 en mode rapport). L'étape 8 (union sync) le projette légitimement à l'hôte (chemin relatif identique), puis la liste `NON_CANONIQUES` de l'installeur — conçue pour purger des *reconstitutions provisoires* — le supprimait. Contradiction introduite à la Task 18 entre la liste de purge et la décision certifiée Task 12.
- **Remédiation** : retrait du chemin de la liste (`NON_CANONIQUES = ["config.json"]`), justifié en commentaire dans `scripts/eco_install_pipeline.py`. Le shim est désormais projeté à l'hôte comme tout l'outillage — **vérifié fonctionnel à l'hôte : 16/16 ALL PASS rc 0 via la délégation**.
- **Preuve** : campagne finale `purges: []` ×2 runs ; shim hôte opérationnel.

### F2 (S4 — documenté, comportement de conception) : fichiers d'état par arbre projetés par l'union sync
- **Constat** : l'installeur seul n'est pas un point fixe sur les fichiers d'**état** : le manifeste d'intégrité (`scripts/ecosysteme-integrity.json`, contenu propre à chaque arbre — le dépôt projette le sien sur celui de l'hôte) et les rapports d'arbitres (`interactions-report.json`, `tool-routing-report.json`, régénérés quand les arbitres tournent entre deux installations).
- **Qualification** : comportement attendu de la voie union — le pipeline canonique le compense **par conception** : l'étape 9 (certification post-install) réécrit le manifeste de l'arbre installé. La mesure retenue est donc la **convergence inter-cycles** (manifeste post-certification du cycle 1 == celui du cycle 2) et non le retour à un état pré-run possiblement périmé — critère recalibré dans le harnais (cause : le manifeste pré-run pouvait enregistrer un hash d'archive antérieur ; l'étape 9 le remet à jour légitimement).
- **Preuve** : convergence OUI ×2 cycles ; diff run 2 limité au seul manifeste.

### F3 (S2 — corrigé) : rescellement d'archive byte-instable (horloge murale)
- **Constat** : chaque rescellement réussi modifiait les octets de l'archive (`writestr(nom, données)` horodate chaque entrée à l'heure courante). Chaîne causale complète : hash archive changeant → manifeste (qui enregistre ce hash) jamais stable → installation non idempotente au niveau byte. L'« idempotence round-trip ×2 » certifiée à la Task 18 était une idempotence de **contenu** (corpus ⊆ archive), pas de **fichier** — et le diff « propre » du run 2 de la première campagne tenait à une coïncidence de granularité DOS (2 secondes) entre deux rescellements rapprochés.
- **Remédiation** : `scripts/task21-f2-rebuild-archive.py` — capture des dates d'entrées de l'ancienne archive et réécriture via `ZipInfo` explicite (dates préservées, époque fixe 1980-01-01 pour une entrée nouvelle, compression DEFLATED et attributs 0o600 répliqués exactement comme `writestr(nom)`), afin que le premier rescellement post-correctif soit byte-identique à l'archive existante puis stable à l'infini.
- **Preuve** : rescellements successifs byte-stables ×3 (hash inchangé) ; campagne finale `archive byte-stable : OUI` ; round-trip vérifié (« Archive régénérée et round-trip vérifié », 9 entrées, 0 divergent, 0 extra) ; intégrité hôte 72/72 et certification dépôt 6/6 re-passées après correctif.

**Aucun finding S1/S2 restant.** Les deux correctifs touchent des instruments certifiés (l'installeur canonique et le rescelleur) : modifications locales, chirurgicales, commentées (cause + référence finding), pré-checks avant (round-trip PASS, garde R2) et re-certifications après (72/72 hôte, 6/6 dépôt, campaignes ×2) — conforme refactoring-engineering (petites transformations, comportement observable préservé : le contenu de l'archive et la vérification round-trip sont inchangés ; seule la stabilité byte des métadonnées ZIP est acquise).

## §5 — Mesures consolidées (D010)

| Mesure | Valeur | Seuil | Marge |
|--------|--------|-------|-------|
| Durée ré-installation run 1 | **0,10 s** | < 60 s | ×600 |
| Durée ré-installation run 2 | **0,10 s** | < 60 s | ×600 |
| Certification complète dépôt (6 arbitres) | **0,49 s** | — | — |
| Intégrité hôte (72 checks) | **0,04 s** | — | — |
| Arbitre correct-work (16 checks) | **0,02 s** | — | — |
| Garde É1-INSTALL | instantanée (subprocess) | — | — |
| Empreinte hôte — 34 skills écosystème | **1,12 Mo** | — | — |
| Empreinte hôte — corpus @mon-ecosysteme (9 PMs) | **0,30 Mo** | — | — |
| Empreinte hôte — scripts projetés (109+ fichiers) | **1,35 Mo** | — | — |
| Empreinte hôte — archive d'intégrité | **0,10 Mo** | — | — |
| **Total projection écosystème hôte** | **≈ 2,87 Mo** | — | léger |

La réinstallation complète tient en un dixième de seconde (copies de contenu identique sur arbre chaud, machine rapide) et l'empreinte totale de l'écosystème est sous les 3 Mo — l'installation est **négligeable en coût** devant n'importe quelle tâche de session.

## §6 — Portée et limites

Le test mesure la **ré-installation sur profil déjà installé** (scénario de maintenance/idempotence — le cas d'usage documenté « ré-exécution depuis l'étape 2 » du PM-INSTALL §3.4) et l'**état** de la projection. L'installation **à froid post-wipe** (profil absent) a été prouvée à la Task 18 Phase E (36 éléments projetés dont 3 skills alors absents, purge, rescellement, certification hôte 72/72) ; la reproduire ici aurait été destructif et sans valeur ajoutée — les gardes (preflight pin, R2, union-merge) sont identiques dans les deux cas. Deuxième limite : le compte mesuré **34 skills** (périmètre dérivé du registre KB : 34 entrées avec forme installée, toutes projetées, 0 divergence) vs la mention « 36 skills » du worklog Task 18 — écart de narration sans divergence de substance (le registre KB, source de vérité, est intégralement projeté) ; la mention « 36 » du worklog comptait vraisemblablement des répertoires hors registre (corpus/@historique). Troisième limite : la coïncidence DOS 2 s de la première campagne a été identifiée et neutralisée par le correctif F3 (les verdicts finaux ne dépendent plus d'aucune fenêtre temporelle).

## §7 — État, clôture écosystème et suivi (D012)

- **Règle d'or n°2 — 0 commit, 0 push** : tous les artefacts Task 20 (plan, harnais ×2, rapport, relevé, 2 correctifs d'instruments) rejoignent la couche locale non publiée (dépôt de travail + hôte). La publication attend le **GO propriétaire + PAT éphémère** (groupe G1 du plan Task 19 — inchangé, la Task 20 s'y adjoint comme couche terminée ; les correctifs F1/F3 seront publiés avec l'ensemble).
- **Registre alias (délégation correct-work v2.8.0 §10.1)** : registre analysé après la campagne — 7 phrases, trié, dédupliqué ; 1 usage propriétaire de `$ECO-LEON` relevé cette session (compteur d'usage cumulé incrémenté, registre dépôt + hôte maintenus byte-identiques) ; **aucune nouvelle phrase n'atteint le seuil de récurrence (≥ 3)** dans les messages propriétaires de la session — aucune proposition d'alias à soumettre.
- **E15 — bilan et auto-calibration** : la boucle E12-E13 (campagne → findings → correctifs → re-mesure) a été productive au round 1 ; leçon consignée : *un instrument d'intégrité qui produit lui-même des artefacts horodatés (archive, manifeste, rapports) casse l'idempotence byte du pipeline qui l'embarque — les artefacts d'état doivent être déterministes ou exclus du périmètre projeté*. Le plan actif reste le **plan Task 19 (mode step)** — aucun plan suivant à générer : la Task 20 était une campagne autonome dont tous les groupes sont terminés, et les groupes Task 19 (G1 publication bloquée sur GO, G2 amorçage alias en cours au fil des discussions, G3-G4 à la demande) restent les suivantes.
- **Restant propriétaire** (inchangé, consolidé) : GO commit+push des couches Tasks 18-20 (jeton éphémère, audit anti-persistance) ; rotation du PAT (consignée de longue date) ; re-mesure voie L du cas QUOTA agent-creator (héritée Task 17).
