# @photos/ — Prompts maîtres de la famille photo « iPhone »

> **Version** : 1.0.0
> **Date** : 2026-10-20 (Task 44, session web-38713acd — directive propriétaire « pousse les skills photo vers le dépôt KNOWLEDGE distant »)
> **Nature** : dossier non-skill (convention SHARED §1.2 v1.6.8 : préfixe `@` = dossier non-skill en tête du listing `skills/`, précédent `@historique/`) — collection de prompts maîtres **métier**, sans SKILL.md ni entrée registre KB.

## 1. Objet

Ce dossier conserve la famille des prompts maîtres d'amélioration photo « qualité iPhone » — générée, migrée et testée empiriquement hors écosystème (sessions web-38713acd, Tasks 41-42, 2026-10-08/09), publiée ici pour survivre aux wipes inter-sessions (le dépôt = source de vérité, précédent dessin-technique Task 8 : « le skill survit aux wipes — clone → pipeline → hôte »).

## 2. Contenu

| Fichier | Rôle | Statut |
|---------|------|--------|
| `iphone18-photos.md` | PROMPT MAÎTRE — pipeline d'amélioration photo « iPhone 18 Pro Max, qualité max » + rendus d'époques + posters (preset défaut `iphone18_max`, règle R18 ouverture variable simulée ƒ/1.48–ƒ/4.0, QC 12, squelette §6.10 `iphone19` [SPÉCULATIF] INACTIF) | **v1.1 COURANT** — extension 1944 le 2026-10-21 (Task 48) ; v1.0 scellée `@historique/photos/` ; tests PA-TEST-001 (QC 12/12) + PA-TEST-002 (QC 12/12 ×2) |
| `iphone19-photos.md` | PROMPT MAÎTRE — génération suivante (iPhone 19 Pro Max, **ANTICIPÉE 2027** — preset défaut `iphone19_max`, R18 ouverture variable, **R19 émulation pixel binning 16-en-1** [RUMEUR — DCS via Frandroid 27/03/2026], QC 13, squelette §6.10 `iphone20` INACTIF) | **v0.11.0 ANTICIPÉE (parallèle)** — migration v0.9.0 (Task 47) + pixel binning R19 v0.10.0 (Task 48) + extension 1944 v0.11.0 (Task 48 : ère 40s, grain N&B, chemin §6.6) ; v0.9.0/v0.10.0 scellées `@historique/photos/` ; tests PA-TEST-005 (QC 12/12 ×2) + PA-TEST-006 (QC 13/13) |
| `iphone17-photos.md` | PROMPT MAÎTRE — génération précédente (iPhone 17 Pro Max) | **v2.1 ARCHIVÉE (génération)** — extension 1944 le 2026-10-21 (Task 48) ; v2.0 scellée `@historique/photos/` ; génération supersédée par `iphone18-photos` (règle §6.10 activée : keynote 9/9/2026) ; tests PA-TEST-003 (QC 11/11 sortie 1) + PA-TEST-004 (QC arbitré) |
| `iphone-photos-migration.md` | PROMPT MAÎTRE MONOLITHE — procédure de migration générationnelle (iphone17 → iphone18, réutilisable pour iphone18 → iphone19) | **v1.0 RÉUTILISABLE** — exécuté de bout en bout (Task 41, checkpoints G-M1/G-M3/G-M5, auto-audit A1-A8 100 %) |

## 3. Règles

1. **Byte-identité (R2)** : fichiers publiés byte-identiques aux livrables audités (SHA-256 vérifié au push ; archive `iphone18.zip`, Task 42) — jamais édités sans procédure ; toute évolution = **bump versionné dans le fichier vivant** (changelog + note rétroactive §11 + auto-audit) + **archivage de la version supplantée dans `@historique/photos/`** (extraction git byte-identique, SHA-256 scellé dans son INDEX.md — établi Task 48) + mise à jour de la table §2. L'état git du dépôt fait foi de la chaîne byte-identité complète.
2. **Version courante unique** : une seule génération « COURANT » à la fois ; la génération précédente est conservée ici marquée ARCHIVÉ (le lignage des générations vit dans le §6.10 de chaque PM — source de vérité).
3. **Hors registre KB à l'origine** : ces PMs métier n'étaient pas inscrits au registre `skills/KNOWLEDGE.md` à la publication (décision Task 44) ; l'inscription est intervenue depuis (Task 45c pour iphone17/iphone18, Task 47 pour iphone19 — les skills projetés `skills/iphone17|18|19/` sont inscrits, ECO_SKILLS 36 ; les PMs `@photos/` restent des sources de lignage hors registre).
4. **Restauration** : `git clone` du dépôt → les fichiers sont directement utilisables (auto-porteurs, mode data-driven : Analyse → Décision → Plan → Exécution → QC → Question utilisateur).

## 4. Provenance

- **Génération iphone18** : Task 41 (session web-38713acd) — prompt maître `iphone-photos-migration.md` exécuté Phases 0→6, livrable v1.0 auto-audité 100 % (A1→A8, 4 itérations, zéro régression G1-G7/B6/R1-R17/QC 1-11 vs source v2.0).
- **Test empirique** : Task 42 — PA-TEST-001 sur photo réelle, pipeline §1→§9 exécuté de bout en bout, QC 12/12 PASS, R18 validée fonctionnellement, validation propriétaire sans réserve (§9 = « non »).
- **Remise** : archive `iphone18.zip` (9 fichiers, incluant ces 3 PMs) remise au propriétaire via le portail vue-upload (Task 43).
- **Publication** : Task 44 (2026-10-20) — push au dépôt distant sur clone frais (main b75a620), dossier `skills/@photos/` créé, byte-identité SHA-256 prouvée, registre KB volontairement non modifié (règle §3.3).
