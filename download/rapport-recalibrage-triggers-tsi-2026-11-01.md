# Rapport de livraison — Recalibrage triggers famille TSI (hôte) — suite F-2

**Directive** : `gen-plan : "GO"` (trace 1a197552459ad8f5, session web-4f989063, 2026-11-01) — application du recalibrage des 5 dérives triggers de la famille TSI proposé à la clôture F-2 (Task 29).
**Périmètre** : recalibrage des 5 cases négatives en dérive (vetos croisés V6.1) — les 3 skills concernés sont HÔTE-SEULS (voir §4), donc aucune montée de version, aucune cascade PM/KB/pin.

---

## 1. Les 5 dérives corrigées (vetos croisés — doctrine « termes réservés d'AUTRES skills » du tandem TSI)

| Skill | Case en dérive | Veto appliqué | Règle de périmètre encodée |
|---|---|---|---|
| tsi-architect | « **Valide** ce fichier TSI et liste-moi toutes les erreurs » | `exclusifs: ["valide"]` | validation = tsi-validator (tandem) |
| tsi-architect | « Génère la **documentation** du Freeze Mode… » | `exclusifs: ["documentation"]` | notice/tableaux = midi-doc-expert |
| tsi-validator | « **Conçois** l'architecture d'un nouveau mapping TSI… » | `exclusifs: ["conçois"]` | conception/architecture = tsi-architect (tandem) |
| tsi-validator | « **Documente** ce mapping avec un tableau de référence MIDI » | `exclusifs: ["documente"]` | tableau de référence = midi-doc-expert |
| midi-doc-expert | « **Valide** la conformité de ce TSI au schéma de référence » | `exclusifs: ["valide"]` | validation = tsi-validator |

Cause racine commune : le radical fort `tsi` (nom du skill) déclenche le routage sur TOUTE requête contenant « TSI », y compris les requêtes relevant des skills voisins du tandem. Le veto V6.1 (Task 30 — avant scoring) est le mécanisme prévu pour ce routage croisé. Garde anti-collision : veto PAR CAS — le cas positif 0 de midi-doc-expert (« mapping TSI **validé** », v1.0.0-cal) n'est pas affecté.

## 2. Preuves mécaniques

| Arbitre | Résultat |
|---|---|
| check-triggers-replay ×2 (hôte) | **PASS 483/483** ×2 — tsi-architect 6/6, tsi-validator 6/6, midi-doc-expert 6/6, traduction-zh-fr 8/8 (non-régression F-2) |
| check-triggers-replay (dépôt canonique) | **PASS 827/827** — inchangé (les 3 skills n'y figurent pas, §4) |
| check-ecosysteme-integrity ×2 | **86/86 PASS** (dépôt + hôte) — manifestes écrits |
| verify-cross (dépôt) | 100 %, 0 erreur (Task 29, inchangé) |
| Non-régression | SKILL.md des 3 skills NON touchés (byte-intacts) → zéro bump semver, zéro cascade PM/KB/pin — changement d'evals uniquement (données de calibration, précédent auto-v1-t27) |

## 3. Finding de vol — angle mort du self-healing (3e matérialisation de F-1)

Entre deux messages, `version-management` a de NOUVEAU disparu de l'hôte (3e occurrence du jour) — et cette fois le garde `auto-install-ecosysteme.py` a rendu **« INSTALLE » à tort** : le contrôle double (checker dépôt + byte-identité SHA-256) couvre 7 fichiers critiques qui n'incluent pas ce skill. Réparé manuellement depuis le dépôt (byte-identique, diff -r vide). **Recommandation (sur GO)** : étendre la liste des 7 fichiers critiques du contrôle (b) aux 41 entrées KB versionnées — le contrôle byte-identité généralisé couvrirait tout angle mort de ce type.

## 4. Constat structurel (correction du rapport Task 29 + décision pendante)

Précision honnête par rapport au rapport F-2 (« variantes plateforme ») : **tsi-architect, tsi-validator, midi-doc-expert sont des skills `category: ecosystem` v1.0.0 HÔTE-SEULS** — jamais commités au dépôt, absents de la KB et du corpus integrity ; seule la propagation §0 les compte (« 5 skills hôte-seuls », commit bf44e77). Conséquences :

- le recalibrage de ce rapport est **volatil par construction** (perdu au recyclage du sandbox avec les evals) — la voie durable est l'**inscription des 3 skills + evals recalibrés au dépôt** (arbre, KB, pins ECO_SKILLS, cascade KO-L004 complète) : décision propriétaire, sur GO ;
- tant que les evals n'existent qu'en hôte, le dépôt canonique ne peut pas mesurer ce périmètre (827 cases) — la dérive est invisible côté dépôt, d'où le PASS 827/827 permanent.

## 5. État final

- Famille TSI recalibrée : **18/18 cases OK** (3 skills × 6) — routage croisé du tandem encodé comme données d'evals.
- Corpus hôte : **483/483 PASS ×2** · dépôt : **827/827 PASS** · integrity **86/86 ×2**.
- Commit pathspec strict (worklog Task 30 + présent rapport) — push origin/main = propriétaire (KO-L009 point 5).
- Décisions pendantes (sur GO) : (a) inscription au dépôt des 3 skills TSI hôte-seuls ; (b) extension du contrôle byte-identité du self-healing aux 41 entrées KB ; (c) disque 86 % (surveillance).
