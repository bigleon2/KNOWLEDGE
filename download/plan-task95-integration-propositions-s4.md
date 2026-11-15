# Plan — Task 95 : intégration des 3 propositions S4 + tests $FACON2 + correct-work --bloc + clone-chat

**Directive propriétaire** trace `1a1ded2a59319bb9` (reformulée `1a1dee6f8511bee1`) — gen-plan mode step
**Référentiel à l'ouverture** : HEAD `5e7508b` (Task 94 CLOSE, poussé — 0 unpushed) · SHARED v1.7.38 · PM-INSTALL v1.9.15 · gen-plan v3.43.0 · harnais re-curation v1.2.2 · extrait §0 PM-INSTALL **v1.7.17 (figé — 21 versions de retard)**
**Baseline prélevée** (`scripts/task95-baseline.json`, médiane ×3, AVANT toute modification) : gen-ultra --check 25,6 ms (rc 1 — dérive pré-existante : ULTRA Task 92 capturé version-management absent, « — » vs 1.3.0 restauré É1-INSTALL) · generer-pm --check 22,3 ms · verify-cross 31,7/32,2 ms · verify-correct-work 21,2 ms · integrity 40,8 ms · interactions 138,6 ms · tool-routing 894,7 ms · propagate 55,7 ms (0 chgt) · cache-verdicts selftest 280,3 ms (12/12)

---

## G1 — S4-1 (finding R2) : dynamiser le littéral harnais dans gen-ultra-maitre.py
- Nouvelle fonction `harness_version()` : lit la version réelle de `skills/re-curation/scripts/protocole-test.py` (docstring, repli « ? » si absent) — KO-L003, même mécanique que `frontmatter_version()`
- ROUTING ligne 56 : littéral « v1.2.1 » → marqueur « v{HV} » substitué à build() ; régénération ULTRA (résorbe AUSSI la dérive pré-existante version-management)
- Idempotence ×2 : `--check` rc 0 après régénération

## G2 — S4-2 (finding R3) : étendre generer-pm-skill.py au bloc CONTEXTE SYSTÈME
- **Cœur** : bloc §0 de PM-INSTALL désormais DÉRIVÉ du SHARED vivant — span verrouillé §0→§1.3 (Règle Zéro + principes fondamentaux [dont langue FR + référence canonique] + §1.1 variables 4/4 + §1.2 conventions complètes), en-tête « (Extrait SHARED v{vivante}) » — remplace le digest figé v1.7.17
- **Classe de drift éteinte** (3 instances découvertes à l'enquête) : (a) §0 figé v1.7.17, (b) étiquette §A.3 stale « v1.9.4, 2026-11-07 », (c) colonne §6.1 SHARED ligne PM-INSTALL stale « v1.8.0 »
- **Mécanique** : `recalibrage()` étendu (toute montée de famille rafraîchit §0 + étiquette §A.3 + ligne §6.1) + NOUVEAU mode `--refresh-ctx` (rafraîchissement SOLO sans montée — NO-OP si déjà frais, idempotence ×2) + `generate_famille()` substitue l'en-tête §0 des PMs de famille à la prochaine montée (contenu L2 = spécification historique, consigné)
- **Versions** : PM-INSTALL v1.9.15→**v1.9.16** (PATCH recalibrage) · SHARED v1.7.38→**v1.7.39** (PATCH référence §6.1) — précédents mécaniques bump_patch
- **Cascade KO-L004** : propagation §0 v1.7.39 (propagateur canonique v2.1.1, dérivation dynamique) → ULTRA régénéré ×2 → archive rescellée (task21-f2 idempotent) → integrity

## G3 — S4-3 (finding R4) : doctrine cache-verdicts codifiée
- Docstring `cache-verdicts.py` : domaine d'usage PERTINENT = boucles intra-exécution (campagnes task71/73/84) · NON-PERTINENT = arbitrage de certification (« un verdict figé n'est JAMAIS une preuve en soi » — mesures Task 91 G2 citées : integrity 0,045 s · verify-cross 0,03 s · interactions 0,146 s) · câblage exhaustif des graders fréquents (F-71-4) = NON-PERTINENT (valeur faible + risque sémantique)
- KB Décisions : entrée Task 95 (3 propositions S4 intégrées, formes retenues)

## G4 — Tests $FACON2 : fonctionnels + performances (objectif OPTIMISATION)
- `scripts/task95-tests-s4.py` (déjà écrit, baseline prélevée) : **T01-T18** fonctionnels (littéral retiré, ULTRA dynamique, byte-identité extrait/span, versions, étiquette §A.3, ligne §6.1, NO-OP refresh, 0 stale v1.7.38, interactions STRICT, integrity, selftest 12/12, doctrine, certification ×5) + **P-gardes** (arbitres < +30 % — aucun code arbitre modifié ; gen-ultra < +50 ms — coût dérivation) + comparaisons avant/après + tailles (impact #token documenté) + rapport `download/rapport-tests-task95.md`
- Analyse d'influence : extract §0 lu à l'installation uniquement ; 261 en-têtes longueur constante ; arbitres non modifiés ; ULTRA taille constante

## G5 — correct-work (projet) --bloc
- Vérification bloc par bloc, verdict par bloc (B1-B4) — rapport download/

## G6 — clone-chat + finalisation
- Clone scellé 8/8 S1-S8 (étape 11 PM-INSTALL — lignée Task 72→95) + miroirs download/ + worklog hôte/dépôt + arbitres AU VERT + commit « Task 95 CLOSE » + PUSH (19ᵉ exposition PAT — rotation recommandée) + résumé concis

---

## Answer key (preuves vérifiables par décision)

| ID | Décision | Preuve mécanique |
|----|----------|------------------|
| D001 | S4-1 : DYNAMISATION retenue (pas recalibrage 1 ligne) | gen-ultra-maitre.py sans littéral « v1.2.1 » + ULTRA cite v1.2.2 (T01-T03) |
| D002 | S4-2 : extrait = span §0→§1.3 du SHARED vivant (complet, pas digest partiel) | byte-identité bloc PM-INSTALL ↔ span SHARED (T05) |
| D003 | S4-2 classe : étiquette §A.3 + colonne §6.1 incluses (2 drifts adjacents découverts enquête) | « Instantané courant (v1.9.16, 2026-11-15) » + «\| v1.9.16 \| » (T08-T09) |
| D004 | S4-2 mécanique : recalibrage étendu + --refresh-ctx NO-OP-si-frais + en-tête §0 PMs famille à la prochaine montée | rejeu --refresh-ctx NO-OP (T10) + --check familles rc 0 (T11) |
| D005 | Versions : PM-INSTALL v1.9.16 + SHARED v1.7.39 (PATCH mécaniques, précédents bump_patch) | en-têtes + lignes d'historique (T06-T07) |
| D006 | S4-3 : doctrine codifiée dans l'outil (pas câblage) — F-71-4 classé NON-PERTINENT | marqueurs doctrine dans cache-verdicts.py + selftest 12/12 (T15-T16) + KB Décisions |
| D007 | Cascade : propagation v1.7.39 + ULTRA ×2 + archive rescellée + integrity | 0 stale v1.7.38 + interactions STRICT + integrity PASS (T12-T14, T17) |
| D008 | Dérive ULTRA pré-existante (version-management « — ») diagnostiquée et résorbée par la régénération | diff baseline (5 lignes) + T03 rc 0 |
| D009 | Tests $FACON2 = baseline AVANT + T01-T18 + P-gardes APRÈS, rapport dédié | rapport-tests-task95.md |
| D010 | correct-work --bloc B1-B4 + clone-chat 8/8 + commit + PUSH | rapports + worklog suite 132+ |

*Plan Task 95 — gen-plan mode step v3.43.0, enquête E1-E2 terminée (12 lectures de code), baseline prélevée avant toute écriture.*
