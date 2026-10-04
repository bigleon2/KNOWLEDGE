# Rapport correct-work (mode PROJET) — Task 23 : routage découverte, installation minimale, auto-réinstallation, francisation

**Date** : 2026-10-03 · **Session** : web-bbbeab47 · **Skill** : correct-work v2.7.0 (couplage §1.5 : gen-plan obligatoire — plan `download/plan-task23-routage-install-minimale-francisation.md`, answer key D001-D008, vérifiée 16/16 par answer-key-checker).

**Mode** : PROJET (v2.7.0, Étapes 1-5) · **Cible** : écosystème local `/home/z/my-project/ecosystem` (corpus + formes installées + outillage) — couche Task 23.

## Étape 1 — Plan de session (E7)

Plan Task 23 en 5 actions (fraîcheur, routage découverte, installation minimale, auto-réinstallation, francisation idempotente) + phases C (exécution), D (re-certification), E (clôture). Décisions D001-D008 toutes vérifiables mécaniquement, marquées `verified` après exécution.

## Étape 2 — Vérification des livrables (faits de matérialisation, KO-L007)

1. **Fraîcheur (D001)** : écosystème installé à la dernière version locale (HEAD a7ca9de au démarrage) — réinstallation non requise, preuve `ensure-installed.py --check` = INSTALLE (rc=0).
2. **Routage découverte (D004)** : gen-plan v3.19.0 §1.16 — skills-inventory PRIORITAIRE (scanner mesuré : 73 skills, 73 descriptions, 14 catégories, zéro API), fallback skill-finder-cn avec contrôle cybersécurité audit-provenance obligatoire avant adoption ; comparaison de performances MÉMORISÉE au KB (décision D004 Task 23).
3. **Installation minimale (D005)** : PM-INSTALL v1.3.1→v1.4.0 (§2bis) ; fermeture mécanique dérivée par `task23-install-minimale.py` — 23 skills, empreinte c6212e1e stable ×2 (idempotent), gain **60,8 Mo (96,7 %)**, arbre élagué `ecosystem-minimale/` matérialisé ; corpus et archive intacts (COMPLET demeure le défaut).
4. **Auto-réinstallation (D006)** : `ensure-installed.py` (--check rc=0/1, --reinstall clone éphémère sans persistance de jeton, no-op si installé) branché au hook É1-INSTALL de gen-plan §1.16.
5. **Francisation (D002/D003/D007)** : audit corrigé (élisions FR — leçon KO : le compteur naïf surestime l'anglais) → 26 cibles réelles sur 103 éléments actifs ; noyau réécrit (skill-creator EN→FR v1.1.0 — V6 maintenu 8/8 ; version-management ZH→FR v1.1.0 — V6 3/8 inchangé, C006 voie L inchangée) + 16 fichiers tiers + skill-finder-cn (version+§0 installés, inscrit ECO_SKILLS n°27) ; 13 fichiers déjà-FR confirmés (faux positifs) ; identifiants/structure/blocs de code préservés (hashes vérifiés par les agents, frontmatter validé YAML) ; CJK résiduels = données d'exemple verbatim (aminer-daily-paper, get-fortune-analysis — consignés).
6. **Propagation des liés (directive « mise à jour des éléments liés »)** : KB miroir ×3 + entrée skill-finder-cn + décision Task 23 ; 7 citations vives « gen-plan v3.18.0 » → v3.19.0 (context/fleet/graph/harness/loop/memory/spec engineering) ; ECO_SKILLS ×3 + skill-finder-cn ; frontmatters tiers complétés (67 : version semver 3-part, catégorie scanner, tags neutres radical-du-nom) ; check 11c-adjacent dynamisé (compte KB = len(ECO_SKILLS), KO-L004) ; garde R2 dynamisée dans interactions (résolution PM famille — le PM corpus v3.18.0 antérieur à l'installé v3.19.0 est toléré et journalisé, PM-INSTALL §3.2) ; ULTRA régénéré (SHA 7774994a, --check no-op) ; archive rescellée round-trip 26/26.

## Étape 3 — Certification (E8)

**6/6 arbitres PASS** (agrégateur certification-complete.py : PASS AVEC RÉSERVES, 4 avertissements, 0 échec) — integrity 58/58 ; verify-cross 98,8 % (0 erreur, warnings uniquement) ; interactions PASS AVEC RÉSERVES ; answer-key ALL PASS ; V6 18/26 (8 dérivants consignés, ZÉRO régression post-francisation) ; check-tool-routing PASS (N1 70 skills conformes, N2 ×5) ; harnais voie M stable. **Idempotence** : installation ×2 empreinte fe1b6975 stable ; fermeture minimale ×2 empreinte c6212e1e stable ; complétion frontmatters ×2 = 0 modification au second passage.

## Étape 4 — Constats

- **S3 (hérité)** : fullstack-dev baseline-pending — inchangé, hors périmètre.
- **S4 (cosmétique)** : drift de modes 100644→100755 + artefacts .next/dev — hors périmètre sémantique (garde numstat 0/0).
- **Réserves nouvelles** : (R1) baselines voie L des 2 équipés francisés (skill-creator, version-management) → re-mesure armée au prochain QUOTA_OK (R3, zéro fabrication — la voie M mécanique est déjà re-verdictée) ; (R2) PM-MAITRE-GEN-PLAN corpus v3.18.0 antérieur à l'installé v3.19.0 — toléré par la garde R2 dynamisée, écart KO-L004 journalisé ; (R3) francisation des CJK de données d'exemple (2 fichiers) non effectuée — identifiants/paramètres d'API verbatim.

## Résumé (problèmes / corrections)

**Problèmes trouvés et corrigés à la source (KO-L003)** : (1) compte KB figé « 26 » dans l'intégrité → dynamisé sur `len(ECO_SKILLS)` ; (2) résolution du PM gen-plan par nom EXACT (crash si l'installé devance le corpus) → garde R2 dynamisée dans interactions (PM famille le plus récent, antérieur toléré + journalisé, postérieur = FAIL) ; (3) extraction semver avalant le point final (« 3.18.0. ») → regex bornée ; (4) ~67 frontmatters tiers incomplets (version/category/tags, défauts préexistants révélés par N1) → complétion mécanique idempotente ; (5) 7 citations vives gen-plan v3.18.0 devenues stale après la montée v3.19.0 → propagation ; (6) ULTRA en dérive après édition du corpus → régénéré (SHA 7774994a) + archive rescellée 26/26 ; (7) KB : bullet Task 22 affirmait « PUSH exécuté » (faux — armé, en attente de jeton) → corrigé.

## Étape 5 — Verdict

**Verdict** : **PASS AVEC RÉSERVES** — les 5 actions de la directive sont matérialisées, certifiées 6/6, idempotentes ; les réserves sont documentées, armées et réversibles (aucune fabrication, KO-L003 respecté : 3 défauts d'arbitres corrigés à la source — compte KB figé, résolution PM exacte, extraction semver à point final avalé).
