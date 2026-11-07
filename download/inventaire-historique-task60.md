# Inventaire historique Task 60 — Recherche exhaustive « n'invente jamais » (première action, item (4))

> **Sources** : exclusivement l'état du disque au 2026-11-07T00:35Z (règle d'or n°5 — KO-L003 : l'état courant fait foi). Chaque affirmation pointe un chemin disque vérifiable. Aucune reconstruction mémorielle.

---

## (a) Arbre des 12 versions de la famille correct-work

**Source primaire** : `skills/@historique/historiques-par-skill/correct-work.md` (table §« Famille CORRECT-WORK », 29 L — lue intégralement). **PMs archivés** : `skills/@historique/prompts-maitres/correct-work/` (7 fichiers v2.4.0→v2.9.0 — tailles : v2.4.0 23 619 o · v2.5.0 28 481 o · v2.5.1 29 380 o · v2.6.0 37 535 o · v2.7.0 41 163 o · v2.8.0 42 934 o · v2.9.0 46 938 o). **PM vivant** : `skills/@mon-ecosysteme/PROMPT-MAITRE-CORRECT-WORK-v2.9.0.md` (§A Déclencheurs, §1.1-§1.7, §2.1-§2.8, §3 Relations — structure vérifiée par grep des titres). **Forme installée** : `skills/correct-work/SKILL.md` v2.9.0 (466 L).

| # | Version | Date | Apport durable (source : historiques-par-skill/correct-work.md) | Statut disque |
|---|---|---|---|---|
| 1 | v1.0.0 | 2026-07-18 | Version initiale, vérification basique | non archivée (pré-corpus) |
| 2 | v2.0.0 | 2026-07-29 | Mode CIBLE + rapport exploitable | non archivée |
| 3 | v2.1.0 | 2026-07-29 | Intégration gen-plan Étape 1 | non archivée |
| 4 | v2.2.0 | 2026-07-29 | Registre KB, kb_path, --kb-skill, matrice dynamique | non archivée |
| 5 | v2.3.0 | 2026-08-09 | Extraction socle SHARED (déduplication R4) | non archivée |
| 6 | v2.4.0 | 2026-08-09 | Multi-cibles, découplage gen-plan, métriques, checklists §4.6-§4.10, scripts/+evals/, hook E8, verify-cross 8 checks | PM archivé |
| 7 | v2.5.0 | 2026-09-06 | Unification schéma evals skill-creator (§5) | PM archivé |
| 8 | v2.5.1 | 2026-09-06 | Description Optimization — déclenchement 8/8 | PM archivé |
| 9 | v2.6.0 | 2026-09-19 | 4e mode AVEUGLE (Second Opinion, inputs filtrés), max 2 rounds, biais de confirmation éliminé | PM archivé |
| 10 | v2.7.0 | 2026-10-02 | Couplage gen-plan OBLIGATOIRE Étape 1 (résolution dynamique) + ARRÊT EXPLICITE si gen-plan indisponible | PM archivé |
| 11 | v2.8.0 | 2026-10-23 | Intégration alias-eco (délégation registre phrases récurrentes, §10.1 Phase 2) + mécanisme dual installation | PM archivé |
| 12 | v2.9.0 | 2026-11-04 | Mode PROJET « bloc par bloc » `--bloc` (§1.7 : BLOCS explicites, verdict PAR BLOC, agrégation pire des verdicts) | PM vivant + VERSION VIVANTE corpus |
| — | **v2.10.0** | 2026-11-06 | **PERDUE au recyclage** — voir (b) | **seule trace : plan-task59** |

**Leçons de lignage** (historiques-par-skill ligne 28) : reconstitutions méthode B1 Task 16 (v2.6.0/v2.7.0, originaux perdus au wipe — `scripts/materialise-pm-correct-work.py` documenté, provenance tracée, aucun faux lignage).

## (b) Contrat v2.10.0 reconstitué — lignage de la perte

**Source** : `download/plan-task59-couplage-step-correct-work.md` (answer key D591-D594, lue intégralement — 60+ L).

**Le contrat v2.10.0 (D591, verbatim)** : §1.5bis « Plan d'actions des correctifs via gen-plan en mode STEP » — contrat OBLIGATOIRE : tout lot de correctifs Étapes 2-5 planifié via gen-plan mode STEP avant application ; groupes + correct-work(groupe) max 2 rounds + correct-work(projet) en fin de chaîne ; plancher gen-plan >= v3.22.0 (version d'introduction du mode step — SHARED §3.2 règle 5) ; ARRÊT EXPLICITE si gen-plan indisponible ; compatibilité tous modes. Alignements : §1.3/§1.5/§2.2/§3/§4 YAML/§6 (checks 11-15)/§10.1 Phase 2 + description frontmatter. Cascade D593 : PM + delta verrouillé `scripts/delta-correctwork-v2100.json` + KB + pin ECO_SKILLS + historiques + SHARED v1.7.27 + PM-INSTALL v1.9.4 + README/ULTRA + archive rescellée.

**Lignage de la perte (constat disque, ce tour)** :
1. L'exécution Task 59 G_A1 a eu lieu sur l'hôte le 2026-11-06 en fin de session (PM v2.10.0 vu sur disque en début de session Task 60 : `skills/@mon-ecosysteme/PROMPT-MAITRE-CORRECT-WORK-v2.10.0.md` 256 L, `skills/correct-work/SKILL.md` version 2.10.0).
2. **Jamais journalisée** : `worklog.md` (hôte, 985 L pré-Task 60) ne contient AUCUNE entrée Task 59 — dernière entrée = Task 58 suite 9 (ligne 973) + note É1-INSTALL (ligne 985). Le miroir `KNOWLEDGE-repo/worklog.md` (965 L) s'arrête à Task 57 clôture (dernier PLAN-AFFICHE ligne 946).
3. **Jamais syncée au miroir** : le working tree miroir (296 M) est à correct-work v2.9.0 (grep `^version:` → 2.9.0).
4. **G_A2 jamais exécuté** : aucun `plan-task58*v2*` dans `download/` (seul v1 à 22:15Z).
5. **Recyclage snapshot** (3ᵉ manifestation live L55-3, ce tour) : corpus + piliers + `skills/correct-work/` restaurés à un état antérieur → v2.10.0 intégralement perdue (SKILL.md, PM, delta, KB, pin, arbitre, SHARED v1.7.27).
6. **Survivants** : `download/plan-task59-couplage-step-correct-work.md` (contrat complet) + le présent worklog Task 60.

**Conséquence G4** : la montée v2.11.0 part de v2.9.0 (état certifié réinstallé) et **ré-intègre** le contrat v2.10.0 — le saut 2.9.0→2.11.0 est un double-apport (contrat STEP + best-of 12 versions), lignage honnête : ligne historique v2.10.0 « matérialisée Task 59, jamais journalisée, perdue au recyclage 2026-11-06, contrat ré-intégré v2.11.0 ».

## (c) Métriques chiffrées (coûts réels de l'architecture PM actuelle)

**c.1 — Coût de la cascade KO-L004 par montée MINOR** (source : worklog Task 48 G1-SG1.3, ligne ~762) : **17 touches distinctes** — delta verrouillé + PM généré (771→772 L) + idempotence ×2 + --check 4 familles + SHARED bump + PM-INSTALL bump + KB ×2 (skill + générique) + historiques-par-skill + pin ECO_SKILLS + arbitre recalibré + trigger_evals + propagation §0 (**115 skills + 146 scripts + 4 agents** — v2.0.3) + ULTRA + README ×2 + rescellement archive v2.3 ×2 + manifeste integrity + complétion agent. Fréquence : **13 montées gen-plan en ~2 semaines** (v3.23.0→v3.35.2, source : `scripts/delta-genplan-*.json` ×13).

**c.2 — Surface de stockage corpus** : `skills/@mon-ecosysteme/` = **9 fichiers .md, 396 Ko** (du -sh) ; archive PMs correct-work = 7 fichiers ~250 Ko ; **16 deltas verrouillés** vivent dans `scripts/` (source : ls delta-*.json).

**c.3 — Volatilité (preuves vivantes)** : **15 disparitions** de version-management (14ᵉ matérialisation documentée Task 58 + 1 ce tour — worklog + grep INSTALLE-REPARÉ ×3) ; **3ᵉ recyclage corpus LIVE** ce tour (première perte complète du corpus @mon-ecosysteme + 4 piliers) ; **1 montée entière perdue** (v2.10.0 — cas (b)) ; pattern L55-3 : snapshots UUID plateforme, cause racine documentée Task 58 (worklog ligne 981).

**c.4 — Lags PM documentés** (source : worklog, grep « lag ») : ×4+ occurrences — « lag 29/23/v3.26.0 résorbé », « lag hérité v2.7.0 », « lag §11 résorbé au passage » (v2.9.0), « lag hérité SHARED §6.1 — 4 colonnes en retard ». Le lag = écart entre la version réelle du skill et la version inscrite au PM/SHARED, récurrent car la cascade est manuelle-orchestrée.

**c.5 — Gaps de synchronisation miroir** (constat ce tour) : worklog miroir en retard de 2 tasks (57 vs hôte 58+) ; working tree miroir 296 fichiers modifiés non commités (push réservé propriétaire KO-L009) ; le gap Task 58-G1/Task 59 = fenêtre de perte avérée.

## (d) Tracé du renommage @PM-SKILLS

**Sources** : `scripts/task52-cascade-genplan-v3350.py:80` (« renommage @PM-SKILLS ») · `scripts/task53-restauration-etat-certifie.py:186,190` (« 0 déploiement `@PM-SKILLS/` ») · `scripts/delta-genplan-v3350.json:5-6` (garde post-installation « 0 fichier `PROMPT-MAITRE-*` sous `skills/<skill>/` hors corpus autorisés, 0 déploiement `@PM-SKILLS/` — PM-INSTALL §3.5, v1.9.0 ») · `skills/@historique/README.md` §2 (sceau @historique). **Lecture** : « @PM-SKILLS/ » = l'ancien nom du dossier corpus, renommé `@mon-ecosysteme/` (traces multiples corpus + scripts de cascade). La directive propriétaire « non pas ceux se trouvant dans @PM-SKILLS/ » vise donc le corpus actuel `skills/@mon-ecosysteme/` — la règle canonique G2 ancre cette équivalence.

---

## Synthèse pour G3/G4 (données, pas de conclusions — l'analyse est en G3)

- Le corpus PM (396 Ko, 9 fichiers) vit DANS `skills/` — zone frappée par la volatilité snapshot (c.3).
- La mécanique de régénération existe déjà : `scripts/generer-pm-skill.py` (KO-L004 — base = PM le plus récent + substitutions verrouillées + delta JSON) ; 16 deltas versionnés en font une source de vérité reconstruisible.
- Le coût marginal d'une montée est dominé par la cascade 17 touches (c.1) — indépendant du lieu de stockage du PM.
- La preuve vivante c.3 (corpus perdu, restauration depuis le miroir = ~2 min pipeline + certification) montre que la redondance corpus↔miroir fonctionne MAIS que le working tree non commité est le point de rupture réel (cas v2.10.0).

*Rapport clos — chaque affirmation ci-dessus est vérifiable par les chemins cités (test -e / grep). D601 satisfait.*
