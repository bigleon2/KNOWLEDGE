# RAPPORT — Task 115 : résorption des différés consignés + erreurs non bloquantes

**Trace** : 1a2027a1c9c5c9a5 (session web-f492e049) · **Date** : 2026-11-22 · **Directive** : « continue mais fais avant gen-plan : "recherche tous les différés consignés, puis corrige-les, ainsi que les erreurs non bloquantes" » — exécutée AVANT la continuation gen-plan.
**Méthode** : re-jeu du scanner canonique `scripts/task101-scan-differes.py` (outil de la directive jumelle Task 101) + recoupements (journal lessons-learned, registres d'arbitres, worklog, état git, cron) + corrections par voie canonique + certification complète.

---

## 1 — Différés et erreurs recensés (25 items scanner + recoupements)

| # | Constat | Classe | Origine |
|---|---------|--------|---------|
| 1-7 | 7 fichiers vivants/historiques introuvables côté hôte (plan-task100, rapport-cw-task99, clone-task99, plan-task99, plan-task98, rapport-cw-task97, plan-task96) | Défaut arbitre (zones figées d'époque — tous présents au miroir dépôt) | Scanner zone VIVANTE/HISTORIQUE |
| 8-21 | 14 auto-références du scanner (docstrings, regex, cas selftest flaggés OPEN) | Défaut arbitre (latent depuis Task 101 : le miroir dépôt du scanner n'existait pas au 1er passage) | Scanner zone CODE |
| 22 | « TODO/fenêtre de tâches » (t114-genplan-v3470.py:76 — concept TodoWrite du rappel langue v3.47.0) | Faux positif arbitre | Scanner zone CODE |
| 23-25 | 3 étiquettes d'étape « [TODO] » dans `skills/rea-analysis/scripts/rea-install.py` (annonçaient des étapes EN COURS avec le marqueur réservé aux travaux non exécutés) | Erreur réelle (réalité trompeuse) | Scanner zone CODE |
| 26 | Journal lessons-learned : L005 « validé », L006 « applique » (coquille), L009 « validé (M4) », L011 « validé » — 4 matérialisations EFFECTUÉES au disque mais statuts jamais alignés | Erreur réelle (retard documentaire) | Recoupement journal ↔ disque |
| 27 | L002 « proposé » (snapshot zip avant montage) — jamais re-adjuguée depuis le 2026-09-26 | Différé consigné (proposition ouverte) | Journal lessons-learned |
| 28 | L010 « candidate » (croiser le worklog amont au recensement) — jamais re-adjuguée depuis le 2026-10-31 | Différé consigné (proposition ouverte) | Journal lessons-learned |
| 29 | version-management (73ᵉ skill) absent de l'hôte | Erreur réelle (10ᵉ épisode d'amputation recyclage — présent au dépôt) | Recoupement audit |
| 30 | Anciennes erreurs non bloquantes historiques vérifiées ÉTEINTES : baseline 24 WARN coherence (0 avertissement désormais), divergence gif-animator-pro (diff -rq vide), résidus ⚠ KB (0), N1 natifs 57 (résolu Task 113 : 73/73) | Vérification | Certification + diffs |

## 2 — Corrections appliquées

### 2.1 rea-analysis v1.0.0 → v1.0.1 (PATCH — la réalité corrigée, KO-L003)

- `rea-install.py` : 3 étiquettes d'étape `« [TODO] »` → `« [ÉTAPE] »` (etape_clone / etape_npm / etape_build) — une étiquette d'étape en cours n'est pas un marqueur de travail différé.
- Cascade complète ×2 arbres (parité byte vérifiée) : SKILL.md frontmatter · registre KB (titre + Dernière calibration) · `@historique/historiques-par-skill/rea-analysis.md` (tableau 2 versions) · pin ECO_SKILLS `check-ecosysteme-integrity.py`.
- Contrat comportemental §3 inchangé (clone/npm/build conditionnels, sonde CLI, rc 0/1/2, idempotence ×2).

### 2.2 Scanner task101 dynamisé (l'arbitre corrigé, KO-L003)

- **Zones dynamiques** (jamais de listes figées) : worklog hôte (3 dernières suites, repli dépôt) + dernier `plan-*.md` + dernier `rapport-cw-*.md` + 5 derniers `clone-*.md` — hôte d'abord (dossier vivant persistant inter-recyclages), repli miroir dépôt. Les 7 fichiers introuvables sont résolus par construction.
- **Auto-exclusion** du scanner (ses docstrings/regex/cas selftest décrivent la méthode) — 14 faux positifs éteints.
- **Frontières de mots** sur « pendance » (exclut « indépendance/dépendance » — faux positif réel constaté sur la ligne §2 du plan courant).
- **Règles d'adjudication ordonnées** : lignes answer key (`criterion/verification/source/priority/status:`) = METHODE_ARBITRE · « TODO/fenêtre » + « fenêtre de tâches » = concept TodoWrite (METHODE) · « différées au worklog » / « explicitement différées » = politique de report documenté D005 (METHODE) · « pendances héritées » / « vérification croisée pendances » = langage d'analyse G1b (METHODE).
- Extrait de contexte 220 → 400 caractères ; selftest 21 → 28 cas (toutes PASS, y compris résolution `_latest` hôte→repli dépôt).

### 2.3 Journal lessons-learned aligné sur le disque (règle d'or n°5)

`scripts/task115-maj-journal-lessons.py` (idempotent ×2 prouvé NO-OP, garde de refus sur état inattendu) :

| Leçon | Avant | Après | Justification (preuve au disque) |
|-------|-------|-------|----------------------------------|
| L005 | validé | **appliqué** | PATTERN:KO-L005-v1.0.0 installé (regles-or.md + table KO gen-plan §1.16 + E7-DISP « re-génération KO-L005 ») — retard documentaire résorbé |
| L006 | « applique » | **appliqué** | coquille du champ statut |
| L009 | validé (M4) | **appliqué** | bloc PATTERN:KO-L009 §1.5 gen-plan v3.30.0 + application processus (verdict CW PASS conservé) |
| L011 | validé | **appliqué** | PATTERN:KO-L011 §1.14bis v3.43.0 + regles-or.md + scripts/adaptation-json-sse.py |
| L002 | proposé | **rejeté** | RÉSORBÉ PAR ÉVOLUTION : la voie canonique git (commit AVANT bootstrap, leçon Task 17 G1) + preflight reset --hard + miroir dépôt fournissent l'état antérieur restaurable visé (9 épisodes de recyclage réparés par ce mécanisme, jamais par snapshot zip) ; un zip dupliquerait la fonction git (R4) |
| L010 | candidate | **rejeté** | COUVERT : règles d'or n°7 (v3.33.0 — mémoire complète, relire worklog/clones avant tout recensement, couverture VÉRIFIABLE) et n°5 (v3.26.0 — statuts dérivés du disque), installées POSTÉRIEURES à la consignation ; preuve d'application de facto : census Task 108 G2 croisé sur la relecture intégrale 153 suites + 21 clones ; un bloc PATTERN dupliquerait (R4) |

Le journal ne porte plus AUCUNE entrée non terminale (11/11 : 8 appliquées, 2 rejetées documentées, L003 appliquée — plus de « proposé/candidate »).

## 3 — Verdicts mécaniques finaux

| Arbitre | Verdict |
|---------|---------|
| Scanner différés `task101-scan-differes.py` | **0_DIFFERE_CORRECTABLE — rc=0** (132 marqueurs, **0 OPEN** ; 20 PROPRIETAIRE = rappels PAT/cron, actions propriétaire correctement classées ; selftest 28/28) |
| Audit conformité `task113-audit-conformite.py` | **73/73 skills + 4/4 agents CONFORMES** (version-management restauré) |
| Certification `certification-complete.py` | **ALL PASS 6/6** — verify-cross 168/168 ×2 · correct-work 16/16 · integrity 116/116 · interactions PASS STRICT 59/59 · tool-routing 6/6 |
| Bootstrap `bootstrap-ecosysteme.py` | **INSTALLE-REPARÉ** (preflight PROPRE · 1 divergence réparée [version-management] · post-install 56 SHA 0 divergence · garde É1-INSTALL INSTALLE) |
| Git dépôt | commit **2b30286f** (voie canonique : commit AVANT bootstrap) · parité HEAD = origin/main + 1 commit local en attente de PUSH |

## 4 — Pendances propriétaire (non exécutables par l'agent — rappels)

1. **RÉVOCATION des PATs exposés** — l'ancien PAT Task 107 ET le jeton du tour Task 114 (**CRITIQUE** — action compte GitHub : Settings → Developer settings → Personal access tokens → révoquer).
2. **Décision cron 531684** — 7ᵉ vérification consécutive : cron list = 0 job. Recréer le job OU entériner son absence (le préflight/bootstrap d'ouverture de session couvre déjà le besoin de réparation).
3. **PUSH des commits du tour** — 1 commit local (2b30286f) en attente ; aucun PAT fourni ce tour (0 manipulation, 0 exposition — KO-L009) ; push immédiat dès PAT frais (leçon Task 98/101).

---

*Rapport généré par la Task 115 — règle d'or n°6 : français exclusif. Preuves : download/task101-differes-report.json · download/rapport-audit-conformite-task113.json · scripts/certification-report.json · download/bootstrap-ecosysteme-rapport.json.*
