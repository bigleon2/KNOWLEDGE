# Rapport d'adéquation gen-plan ↔ écosystème — Task 72 G2 (D007)

**Date : 2026-11-08** · Session : web-ecef7f80 · Plan : download/plan-task72-recuration-genplan-adequation-liste-skill-recuration.md (rév. 3, 15 décisions) · gen-plan **v3.39.0** (post-re-curation R1 + fenêtre native AFFICHE-PLAN)
Arbitre de traçabilité : règle d'or n°5 — tout verdict cité est issu d'une exécution mécanique de la présente session (horodatées au worklog suites 36-38).

## 1. T2.1 — Batterie d'arbitres écosystème (×3 exécutions ce jour : cascade + re-jeu ×2 + trace G2)

| Arbitre | Verdict | Durée (trace G2) | Détail |
|---|---|---|---|
| check-ecosysteme-integrity.py | **110/110 PASS, 0 FAIL** | 48 ms | ECO_SKILLS gen-plan 3.39.0 vérifié ; archive round-trip v2.3 corpus 9/9 + piliers 6/6 byte-identiques (re-scellée SHA dbe21285…) |
| test-coherence-interactions.py | **54 PASS / 1 WARN / 0 FAIL — PASS AVEC RÉSERVES** | 121 ms | WARN unique = B1 « historique v3.11.0 + PEK — artefact historique propriétaire » (légitime, hérité, non bloquant — même classe que la cascade v3.38.0) ; recalibrage 3ᵉ éd. documenté dans l'arbitre (plage PM 1200-1900 L — KO-L003 : v3.39.0 = 1 770 L, intégraux in extenso §9.7-§9.10) |
| verify-correct-work.py (vcw) | **16/16 ALL PASS** | 30 ms | 16 checks canoniques du skill correct-work |
| verify-cross.py | **100,0 % — 0 erreur, 0 avertissement** | 34 ms | Cross-references KB × dépendances |

## 2. T2.2 — Selftests des scripts gen-plan + écosystème

| Script | Selftest | Verdict |
|---|---|---|
| skills/gen-plan/scripts/check_plan_protocol.py | --selftest | **OK (7/7)** — dont « idempotence ×2 → PASS stable » |
| scripts/poids-chargement.py | --selftest | **10/10 PASS** (dont T10 idempotence) |
| scripts/cache-verdicts.py | --selftest | **12/12 PASS** (dont T12 stats) |
| skills/gen-plan/scripts/ensure-installed.py | --check | **rc=0 INSTALLE** (après auto-réparation version-management 6ᵉ disparition — INSTALLE-REPARÉ, garde Task 56) |

## 3. T2.3 — Evals de non-régression (contrats D005)

- evals/evals.json : **9 cas** (schéma skill-creator), JSON valide.
- evals/trigger_evals.json : **15 cas** (13 + verbatim « met à jour » + négatif hors périmètre — v3.37.1), JSON valide.
- **Byte-identité baseline golden master** (scripts/task72-baseline-verifier.py --verifier, harnais v2) : §A déclencheurs verbatim + glossaire $FACON/$FACON2 + §0 Contexte Système (étiquette SHARED normalisée — preuve modulo-étiquette SHA bb8fe775… consignée au baseline JSON) + read_when + evals ×2 + comptages canoniques §A == baseline T1.1.0 — **VERDICT POST : PASS** (×2 re-jeu).
- Interprétation : la re-curation (9 blocs déplacés R4 + résumés nouveaux + fenêtre native) n'a modifié AUCUN contrat de déclenchement — la non-régression triggers (précédent Task 61 F-V1-1) est préservée.

## 4. T2.4 — Verdict poids post-re-curation + couverture PM

**Poids (arbitre officiel scripts/poids-chargement.py v1.0.0, seuils OK < 12 / LOURD ≥ 30 / CRITIQUE ≥ 60 Kio)** :

- gen-plan **v3.39.0 : SKILL.md 29,9 Kio ≈ 7 667 #token · references/ 156,0 Kio / 15 fichiers · total 185,9 Kio — verdict INTERMÉDIAIRE, rang 10** (avant v3.38.0 : 104,0 Kio ≈ 26 616 #token, CRITIQUE rang 1) — réduction **−71,2 %** du poids de chargement par défaut.
- Bilan écosystème : **70 skills — 28 OK · 33 intermédiaires · 9 LOURD · 0 CRITIQUE** (avant : 1 CRITIQUE).
- Lecture ciblée = état par défaut du skill lui-même (description frontmatter + E5-POIDS) ; intégraux en references/ chargés à la demande.

**Couverture PM (générateur mécanique KO-L004)** :

- PM v3.39.0 (211 054 octets / 1 770 lignes) : **« [OK] couverture gen-plan : toutes les sections SKILL.md représentées dans le PM »** — la classe WARN §1.13 (« sections SKILL.md absentes du PM », faux positif hérité Task 21 documenté en v3.37.2) est **résorbée par construction** : les résumés compacts §1.8/§1.9/§1.12/§1.16 du PM sont les miroirs exacts des sections SKILL.md, intégraux in extenso §9.7-§9.10.
- Aucune duplication intra-PM (fenêtres 1024 octets — même mécanique que D004) ; generer-pm-skill.py --check : **COHERENT ×4 familles** (gen-plan 3.39.0, correct-work 2.11.0, clone-chat 2.0.2, refactor-guard 1.8.1).
- SHARED v1.7.34 / PM-INSTALL v1.9.10 recalibrés mécaniquement ; propagation §0 v1.7.34 (69 skills + 173 scripts + 2 agents, contenu stable au re-jeu — 0 divergence SHA).

## 5. T2.5 — Synthèse honnête

**Verdict d'adéquation : PASS AVEC RÉSERVES (1 WARN légitime hérité, 0 FAIL)** — le skill gen-plan v3.39.0 est en adéquation mécanique complète avec l'écosystème :

1. **Conforme** : 4/4 arbitres au vert (dont coherence 0 FAIL), 4/4 selftests, contrats triggers byte-identiques, poids sous le seuil LOURD, PM couvrant, cascade KO-L004 complète et synchronisée (commit dépôt 5646e96).
2. **Réserve WARN B1 (coherence)** : artefact historique propriétaire (historique B1 v3.11.0 + PEK non cloné au worklog de session) — légitime, documenté, hors périmètre gen-plan.
3. **Constats S3-class résorbés en cours de route (transparents)** : (a) recalibrage KO-L003 de la plage de lignes PM dans l'arbitre coherence (la re-curation fait légitimement grandir le PM in extenso — 1 770 L) ; (b) harnais v2 du baseline verifier (étiquette SHARED du §0 normalisée — preuve modulo-étiquette) ; (c) re-scellement archive v2.3 (le task42-resceller pointait un clone périmé — voie ré-écrite task72-resceller-archive.py, mêmes conventions) ; (d) lag d'en-tête historiques-par-skill (v3.37.1 → v3.39.0) et arborescence README corpus (v3.35.2 → v3.39.0) résorbés.
4. **Pendance (hors périmètre G2, D013)** : PUSH des commits (Task 70-71 + 5646e96) par le propriétaire uniquement, après révocation du PAT exposé (KO-L009).

**Décisions couvertes** : D007 ✓ (présent rapport) · contributions D001-D006 + D015 (G1, rapportées au worklog suite 37).
