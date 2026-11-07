# Historique par skill — pm-skill

> **Version** : 1.0.0 — **Date** : 2026-11-07 (Task 60 G3-SG2, session web-c30e6506 — porte propriétaire D604 VALIDÉE : directive verbatim « je valide ta proposition, tu peux l'exécuter $FACON pour me générer $FACON un écosystème $FACON2 »)
> **Version vivante (corpus)** : v1.0.0 — `skills/pm-skill/SKILL.md` (sa spécification fait foi)
> **Versions archivées** : 0 (le skill est né v1.0.0)
> **Provenance** : skill créé DANS le dépôt (Task 60 G3-SG2) — forme de production du prototype embarqué testé par `scripts/task60-tests-comparatifs.py` (D603b : 16 PASS · 1 FAIL [défaut réel de l'écosystème actuel — PM gen-plan corpus non auto-portant] · 7 FACT ; tests B1-B7 verts). Extension unique vs prototype testé : section HISTORIQUE CONDENSÉ (proposition §3 validée). Lignage honnête : l'analyse D603 (`download/analyse-idee-pm-skill.md`) et les tests D603b (`download/rapport-tests-task60.md`) précèdent la validation propriétaire.

## Famille PM-SKILL — 2 versions (skill : pm-skill)

**Rôle** : Portabilité universelle — génération à la demande de prompts maîtres ÉPHÉMÈRES auto-portants (MD) depuis les SKILL.md vivants de la racine skills/, pour usage IA externe (coller comme prompt système). Couche ADDITIVE : corpus `@mon-ecosysteme/` intact (KO-L004 continue pour les 4 familles).

| Version | Date | Améliorations implantées | Avantage par rapport à la version précédente |
|---------|------|--------------------------|----------------------------------------------|
| v1.0.0 | 2026-11-07 | Création (Task 60 G3-SG2, D604 VALIDÉE — analyse D603 verdict « AUGMENTE » + tests D603b 16 PASS/7 FACT) : SKILL.md + bras `scripts/generer-pm-ephemere.py` (Python stdlib — projection auto-portante : en-tête provenance + SHA-256 source + mode d'emploi IA externe + mission verbatim + corps SKILL.md [§0 Contexte Système embarqué] + relations frontmatter + historique condensé @historique ; --generate/--check/--list/--self-test ST1-ST11 ; codes retour 0/1/2/3 ; déterminisme ×2 byte-identique ; zéro invention KO-L003 ; 0 octet d'état — sorties download/ uniquement) + evals (4 positifs + 3 négatifs vetos croisés) + entrée KB + pin ECO_SKILLS | — (point de départ : la portabilité IA externe passe de 4 familles/68 skills à 68/68, coût d'état 17 touches → 0, lag impossible par construction) |
| v1.0.1 | 2026-11-07 | Task 61 G3 (correct-work --bloc findings F1/F2 résorbés — bidirectionnalité SHARED §3.2) : frontmatter dependencies += correct-work >= v2.4.0 (certification post-intégration — arbitres integrity/verify-cross rejoués après création, usage réel confirmé §7) + réciproque KB gen-plan « Utilisé par » += pm-skill (F1, côté gen-plan) + KB pm-skill « Dépend de » += correct-work (F2) ; PATCH addition pure | La relation de certification pm-skill→correct-work est déclarée structurellement (frontmatter + KB) — la bidirectionnalité KB est complète — **VERSION VIVANTE (skill installé)** |
| v1.0.2 | 2026-11-07 | Task 67 G4 (résorption F-67-2 — directive bloc n°3, 25 WARN coherence) : frontmatter dependencies += vue-upload >= v1.5.0 (livraison du PM éphémère : push/featured ★, share vérifié SHA-256) — direction sémantique corrigée : pm-skill DÉPEND de vue-upload (canal de diffusion), l'ancienne mention « Utilisé par » de pm-skill listant vue-upload était inversée ; réciproque ajoutée à vue-upload « Utilisé par » += pm-skill ; PATCH addition pure | La chaîne de livraison du PM éphémère est déclarée dans le bon sens (pm-skill → vue-upload) avec réciproque — le graphe KB est bidirectionnel — **VERSION VIVANTE (skill installé)** |

Révisions documentaires de la famille (sans changement de version du skill) : néant.
Fichiers archivés de la famille : néant (0 fichier).
