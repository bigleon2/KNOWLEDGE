# Rapport de livraison — Task 31 : (a) inscription des 3 skills TSI au dépôt + (b) self-healing généralisé

**Directive** : `gen-plan : "{"- (a) : effectue l'inscription des 3 skills TSI au dépôt (cascade complète). - (b) : effectue l'extension du contrôle byte-identité du self-healing aux 41 entrées KB.}"` (trace 1a1975c9a4c7fa31, session web-4f989063, 2026-11-01).

---

## (a) Inscription des 3 skills TSI — cascade complète

| Élément | Détail |
|---|---|
| Copie host→repo | tsi-architect (5 fichiers), tsi-validator (6), midi-doc-expert (5) — `diff -r` vide ×3 (byte-identité) ; blocs §0 SHARED v1.7.17 déjà présents (propagation no-op idempotent — vérification canonique propagate-context.py) |
| KB | 3 entrées v1.0.0 (template SHARED §2.2 : Category / Description / Dépend de / Utilisé par / Dernière calibration / Statut) — lignage honnête : « créé hors dépôt, copie byte-identique, aucune revendication rétroactive » (doctrine Task 27) ; réciproque gen-plan « Utilisé par » complétée ×3 |
| Pin ECO_SKILLS | `tsi-architect`/`tsi-validator`/`midi-doc-expert` = "1.0.0" (44e-46e entrées versionnées, provenance en commentaire) |
| historiques-par-skill | 3 journaux v1.0.0 créés (`@historique/historiques-par-skill/`, hôte + dépôt) — 0 version archivée, révisions documentaires Task 30/31 consignées |
| Archive v2.3 | re-scellée (corpus 9 + piliers 6 byte-identiques, round-trip vérifié) + sync hôte→dépôt |

**Preuves (a)** : replay dépôt **PASS 845/845** (TSI 6/6 ×3 intégrés — +18 cases, n_skills 109) · verify-cross **100 %, 0 erreur** · integrity **92/92 PASS ×2** (dépôt + hôte — le total passe 86→92 avec les 3 pins + 3 entrées KB dynamisées) · replay hôte PASS 483/483 (non-régression).

**Finding en vol (consigné)** : l'invocation `propagate-context.py --help` a déclenché une vraie passe (le script ne protège pas ses arguments) — effet : normalisation canonique §0 v1.7.16→v1.7.17 sur 4 fichiers agents (2 skills + 2 PM) — bénigne, même normalisation que le commit bf44e77, conservée avec provenance. Recommandation : garder `--help` hors grammaire du script.

## (b) Extension du contrôle byte-identité du self-healing

`auto-install-ecosysteme.py` étendu (pivot 7 fichiers **+ SKILL.md de TOUTES les entrées KB versionnées, dérivé dynamiquement** du dépôt KB — regex identique à l'arbitre integrity, KO-L003 jamais figé ; toute future entrée KB est couverte sans édition du script) :

| Preuve | Résultat |
|---|---|
| Selftest | **5/5 PASS** (48 fichiers critiques uniques au dépôt, liste KB dynamique 45, défaut synthétique 48/48 détecté, verdicts déterministes) |
| **Test réel sur état cassé VIVANT** | version-management avait de nouveau disparu de l'hôte (4e matérialisation du jour) → le garde étendu a détecté `skills/version-management/SKILL.md (hôte absent)` — l'angle mort exact qui rendait « INSTALLE » à tort ×3 — et a exécuté le pipeline canonique : **REINSTALLE rc=0, 0 défaut après** |
| Idempotence ×2 | INSTALLE, actions [] — no-op ×2 |
| Cohérence | integrity 92/92 ×2 après réparation ; replay hôte 483/483 |

## État final

- Dépôt : **+16 fichiers** (3 skills) + KB/pins/historiques/garde étendu — commit pathspec strict, push origin/main = propriétaire (KO-L009 point 5).
- Les 3 skills TSI sont désormais couverts par : KB, pin integrity, replay triggers (dépôt), historiques-par-skill, contrôle byte-identité du self-healing — et **survivent au recyclage du sandbox** (réinstallés par le pipeline depuis le dépôt, recalibrage Task 30 inclus).
- Pendantes : disque 86 % (surveillance) ; garde `--help` du propagateur (note).
