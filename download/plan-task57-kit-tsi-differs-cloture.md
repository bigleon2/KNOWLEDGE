# Plan d'actions Task 57 — Kit de correction TSI (F1/F2/F4) · différés agent-actionnables · clôture

**Générateur** : skill `gen-plan` v3.35.2 (mode **NULL** — demande propriétaire : « continue mais avant gen-plan : vérifie que tu as finis tes correctifs des actions que tu étais en train de faire » → vérification FAITE en préalable, puis continuation classique sans portes de confirmation, clause mode NULL v3.21.0).
**Session** : web-c30e6506 (continuation) · **Date** : 2026-11-06 · **Exécution** : G1 ∥ G2 (preuve d'indépendance — aucune écriture partagée), G3 séquentiel, `correct-work (projet) --bloc` en fin de chaîne.

---

## §0 État d'ouverture (E1-RES — dérivé du disque, règle d'or n°5)

| Vérification préalable | Résultat |
|---|---|
| É1-INSTALL `ensure-installed.py` | **INSTALLE-REPARÉ** rc=0 — `version-management` restauré (12ᵉ matérialisation, 3ᵉ preuve vivante de la garde auto-réparante en production) → re-jeux ×2 : **INSTALLE** (idempotent, 0 manquant, KB 52 entrées) |
| Garde post-coupure (règle d'or n°9 — arbitre integrity) | **108/108 PASS ×2** (manifeste `scripts/ecosysteme-integrity.json`) |
| Collecte G-RES (resource-monitor) | **OK → PARALLELE** (disque 7,5 Go libres, mémoire 2,65 Go, charge 0.0) |
| coherence interactions | **53 PASS / 23 WARN / 0 FAIL** (baseline Task 55/56) |
| verify-correct-work | **16/16 PASS** |
| Miroir local `KNOWLEDGE-repo/` | **59a5805, porcelain 0** (état de clôture Task 56 inchangé — push = GO propriétaire) |
| **Vérification demandée par le propriétaire ce tour** | **CORRECTIFS TASK 56 TERMINÉS** — constat disque : skills/ 73 entrées (gen-plan v3.35.2, correct-work v2.9.0, clone-chat v2.0.2, @mon-ecosysteme 7 PMs, KNOWLEDGE.md 52 entrées, version-management v1.2.0) · chaîne G1→G6 close · 6 livrables Task 56 présents dans `download/` · worklog complet |
| ZIP propriétaire | `upload/mes-mappings-tsi-actuels.zip` — 6 TSI analysés Task 56 G2 (rapport JSON rejouable + rapport Markdown) |

**Failles G2 héritées (rapport `download/rapport-g2-analyse-zip-s4mk2.md`)** : F1 divergence mapping embarqué Settings (15 assignations) ≠ « Mon Mapping (Aout 2024) » (31) · F2 « Mapping Juin 2024-2025.tsi » = préférences, nom trompeur · F3 couverture P1b 0/22 (décision propriétaire) · F4 doublon Aout 2023 ≡ Novembre 2023.

**Différés §5 hérités (Tasks 55-56)** : branche test/compilation-windows@04accb8 (**bloquée 403 PAT — propriétaire**) · plancher inter-scripts→dessin-technique ≥1.3.0 (**insatisfaisable, installé 1.1.1 — décision propriétaire**) · précision verdicts orchestrateur-tsi (**agent-actionnable**) · indentation registre alias (**agent-actionnable**).

---

## §1 Objectif (éléments restants de la discussion — règle d'or n°7)

Demande du tour : « continue mais avant gen-plan : vérifie que tu as finis tes correctifs… » → **vérification FAITE** (tableau §0 : terminés). La continuation traite les pendances restantes de la mission racine (« corrige $FACON les failles de mon écosystème afin de l'optimiser $FACON pour qu'il ait un fonctionnement $FACON2 » — expansions alias-eco : $FACON = « de façon cohérente, optimisée et fonctionnelle », $FACON2 = « (cohérent, optimisé et fonctionnel) ») :

1. **Failles mappings G2 actionnables** : F1 (guide d'import ordonné), F2 (renommage), F4 (hygiène doublon) — F3 reste décision propriétaire.
2. **Différés agent-actionnables (2/4)** : précision verdicts orchestrateur-tsi, indentation registre alias.
3. **Clôture** : correct-work (projet) --bloc + rapport final + RAPPELS OBLIGATOIRES propriétaire + clone-chat.

**Intégration E13 (règle d'or n°3 — directive propriétaire gen-plan (step) en cours d'exécution)** : (a) vérification que le plan est bien une génération gen-plan → **preuve faite, aucun bug** (D013) ; (b) explication des 4 différés demandée → **livrée au chat** (D014) ; l'exécution se poursuit en mode step (correct-work(groupe) après chaque groupe, correct-work(projet) --bloc en fin de chaîne).

---

## Answer key (hook E1)

```yaml
decisions:
  - id: "D001"
    libelle: "Plan Task 57 généré via gen-plan v3.35.2 mode NULL, validé E8, affiché au chat"
    criterion: "Le plan est écrit dans download/, validé E8 (P1-P5), affiché (PLAN-AFFICHE)"
    verification: "python3 skills/gen-plan/scripts/check_plan_protocol.py --plan download/plan-task57-kit-tsi-differs-cloture.md --worklog worklog.md → PASS 5/5"
    source: "Demande propriétaire (« continue mais avant gen-plan : {vérification correctifs} »)"
    priority: S1
    status: pending
  - id: "D002"
    libelle: "Vérification des correctifs Task 56 demandée par le propriétaire : TERMINÉS — constat mécanique sur disque"
    criterion: "Chaque correctif en cours au moment du message cité est vérifié existant : skills restaurés, vm v1.2.0, batterie arbitres, miroir 59a5805, livrables Task 56"
    verification: "Tableau §0 (constat disque du tour) + re-jeux garde INSTALLE ×2 + integrity 108/108 ×2 affichés au chat"
    source: "Message propriétaire citant le constat des absences (skills/ 66 entrées, vm/gen-plan/correct-work manquants)"
    priority: S1
    status: pending
  - id: "D003"
    libelle: "Kit de correction TSI : copie renommée « Préférences Juin 2024-2025.tsi » (F2) — nom de fichier + nom interne si pertinent"
    criterion: "Le fichier trompeur « Mapping Juin 2024-2025.tsi » (préférences) est fourni en copie au nom correct ; l'original n'est jamais modifié (non-destructif)"
    verification: "Fichier présent dans download/kit-correction-tsi/ ; contenu byte-identique à l'original hormis le renommage documenté ; verdict tsi-validator conforme à l'original"
    source: "Faille F2 rapport G2 Task 56 (recommandation : renommer les exports)"
    priority: S1
    status: pending
  - id: "D004"
    libelle: "Guide d'import ordonné Traktor (F1) : Settings d'abord, puis ré-import « Mon Mapping (Aout 2024).tsi »"
    criterion: "Guide pas-à-pas dans le kit ; PAS de chirurgie TSI sur les Settings (risque de corruption des préférences propriétaire — décision motivée : la procédure 2 imports est celle recommandée par le rapport G2)"
    verification: "README-import.md dans download/kit-correction-tsi/ avec l'ordre exact, les fichiers sources et l'explication de la divergence 15≠31"
    source: "Faille F1 rapport G2 Task 56 (la plus actionnable)"
    priority: S1
    status: pending
  - id: "D005"
    libelle: "Hygiène doublon (F4) : Aout 2023 ≡ Novembre 2023 — conservation désignée"
    criterion: "Le kit documente le doublon bref (hash identique ou verdict ≡) et désigne « Mapping TRAKTOR _ KONTROL S4 MK2 Novembre 2023.tsi » comme copie conservée (nom le plus explicite), Aout 2023 comme doublon à archiver"
    verification: "Section hygiène dans le rapport du kit, appuyée sur les verdicts tsi-validator des deux fichiers"
    source: "Faille F4 rapport G2 Task 56 (doublon d'export)"
    priority: S2
    status: pending
  - id: "D006"
    libelle: "Validation tsi-validator v1.3.0 de chaque fichier du kit"
    criterion: "Chaque fichier du kit reçoit un verdict mécanique (PASS/PRÉFÉRENCES/FAIL) ; les verdicts sont conformes aux originaux (le renommage ne change pas la structure)"
    verification: "Tableau avant/après dans le rapport du kit ; tout écart de verdict est documenté et investigué"
    source: "Garde obligatoire du tandem tsi-architect (jamais de mapping livré sans verdict PASS)"
    priority: S1
    status: pending
  - id: "D007"
    libelle: "Différé résolu : précision des verdicts orchestrateur-tsi (bump mineur)"
    criterion: "La section verdicts/agrégation de orchestrateur-tsi est précisée (qualification par membre, agrégation « pire des membres », traçabilité), bump 1.1.0→1.1.1, inscription KB, sync miroir"
    verification: "SKILL.md orchestrateur-tsi v1.1.1 + section KB recalée + integrity re-pass 108/108 + verify-correct-work PASS"
    source: "Finding S4 correct-work --bloc Task 55 (2×S4 différés : précision verdicts orchestrateur-tsi)"
    priority: S2
    status: pending
  - id: "D008"
    libelle: "Différé résolu : indentation du registre alias normalisée"
    criterion: "aliases.json ré-écrit avec indentation cohérente (json.dump indent=2), données strictement identiques (diff sémantique vide), idempotent ×2"
    verification: "Re-jeu ×2 stable ; python3 -c json.load → valide ; comparaison structurelle avant/après = 0 différence"
    source: "Finding S4 correct-work --bloc Task 55 (indentation registre alias)"
    priority: S2
    status: pending
  - id: "D009"
    libelle: "Parallélisation G1 ∥ G2 (philosophie #4 v3.32.0 — preuve d'indépendance)"
    criterion: "G1 (kit TSI, écritures dans download/kit-correction-tsi/ uniquement) et G2 (skills + @historique, écritures dans skills/ et miroir uniquement) n'ont aucune écriture partagée ni dépendance d'ordre"
    verification: "Journalisation worklog de l'exécution en vagues ; G3 démarre après complétion G1+G2"
    source: "Philosophie #4 gen-plan §1.7 (parallélisation par défaut des tâches ET des commandes)"
    priority: S2
    status: pending
  - id: "D010"
    libelle: "correct-work (projet) --bloc sur périmètre Task 57 : 3 blocs (B1 kit / B2 différés / B3 clôture)"
    criterion: "Mode bloc par bloc exécuté en fin de chaîne ; verdict global = pire des blocs ; findings corrigés en vol (max 2 rounds)"
    verification: "Rapport correct-work --bloc Task 57 dans download/ ; 3× PASS → global PASS"
    source: "Protocole mode step Task 56 (G3) reconduit en clôture"
    priority: S1
    status: pending
  - id: "D011"
    libelle: "Rapport final + RAPPELS OBLIGATOIRES propriétaire (KO-L009 point 5, D009 Task 56 reconduit)"
    criterion: "Rapport final Task 57 (couverture des demandes, état final dérivé du disque) + rappels : rotation PAT K1/K2 + GHORG_GITHUB_TOKEN (12ᵉ+ expositions — inclut le déblocage 403 de la branche test/compilation-windows) · GO push 59a5805 · F1 import Traktor côté propriétaire · F3 décision complément P1b · plancher dessin-technique ≥1.3.0"
    verification: "download/rapport-final-task57.md présent ; section rappels en tête ; worklog clôturé"
    source: "Pendances propriétaire consignées Task 56 (rapport final §3)"
    priority: S1
    status: pending
  - id: "D012"
    libelle: "clone-chat scellé + worklog Task 57 complet (R5)"
    criterion: "Clone de discussion auto-suffisant dans download/ ; entrée worklog Task 57 (contexte, décisions, artefacts, état, pendances)"
    verification: "Fichier clone présent + entrée worklog vérifiable"
    source: "Étape 4 de la demande d'origine (clone-chat) — reconduite en clôture de chaque tâche"
    priority: S1
    status: pending
  - id: "D013"
    libelle: "[E13 — intégrée en cours d'exécution, directive propriétaire gen-plan (step)] Vérification que le plan a bien été généré via le skill gen-plan — si ce n'est pas le cas, corriger le bug et régénérer"
    criterion: "Preuve mécanique que le plan Task 57 est une génération gen-plan v3.35.2 (en-tête Générateur, answer key, worklog R5, PLAN-AFFICHE, arbitre PASS)"
    verification: "Re-jeu check_plan_protocol.py → PASS 5/5 ; en-tête « Générateur : skill gen-plan v3.35.2 » ; entrée worklog « plan généré via gen-plan » — AUCUN bug constaté, pas de re-génération nécessaire"
    source: "Demande propriétaire gen-plan (step) du 2026-11-06 (tour courant)"
    priority: S1
    status: verified
  - id: "D014"
    libelle: "[E13 — intégrée en cours d'exécution] Explication livrée au propriétaire des 4 différés (branche compilation-windows, plancher dessin-technique, précision orchestrateur-tsi, indentation registre alias)"
    criterion: "Réponse en français au chat expliquant chaque différé : nature, cause du report, qui peut le résoudre (agent vs propriétaire), état actuel"
    verification: "Bloc explicatif au chat + statuts actualisés (2/4 résolus Task 57 [orchestrateur-tsi v1.1.1, alias déjà conforme] ; 1 propriétaire-bloqué [403 PAT] ; 1 décision propriétaire [plancher])"
    source: "Demande propriétaire gen-plan (step) du 2026-11-06 : « que veux-tu dire lorsque tu me dis 'Différés inchangés…' »"
    priority: S1
    status: verified
```

---

## §2 Groupes et tâches

### G1 — Kit de correction TSI (F1+F2+F4) — ∥ G2
- **SG1.1** Extraction fraîche du ZIP vers `tmp/zip-task57/` ; copie de travail des 3 fichiers utiles ; renommage F2 (« Préférences Juin 2024-2025.tsi ») ; rédaction `README-import.md` (F1 — ordre d'import, explication divergence 15≠31, tableau des 6 fichiers) ; note hygiène F4.
- **SG1.2** Validation tsi-validator v1.3.0 × fichiers du kit + originaux de référence (tableau avant/après).
- **SG1.3** Rapport `download/rapport-kit-correction-tsi.md` (verdicts, instructions, hygiène).

### G2 — Différés agent-actionnables — ∥ G1
- **SG2.1** orchestrateur-tsi : lecture SKILL.md v1.1.0, précision de la section verdicts (qualification par membre, agrégation pire-des-membres, traçabilité), bump 1.1.1, §0 conservé, KB recalée, sync miroir, re-certification.
- **SG2.2** aliases.json : normalisation indentation (json.dump indent=2, ensure_ascii=False), diff sémantique vide prouvé, idempotence ×2, sync miroir si modifié.

### G3 — Clôture (après G1+G2)
- **SG3.1** correct-work (projet) --bloc : B1 (kit) / B2 (différés) / B3 (clôture).
- **SG3.2** Rapport final `download/rapport-final-task57.md` + RAPPELS OBLIGATOIRES + worklog.
- **SG3.3** clone-chat scellé `download/clone-discussion-2026-11-06-task57.md`.

---

## §3 Budget #token (E4) et profil (E6)

~35 k#token (G1 ~12 k · G2 ~8 k · G3 ~15 k) × 1,3 pire cas ≈ **46 k**. Profil **NORMAL / PARALLELE** (G-RES OK). Skills mobilisés (E5) : tsi-architect v1.2.0 (méthode), tsi-validator v1.3.0 (arbitre), correct-work v2.9.0 (--bloc), clone-chat v2.0.2, knowledge-observer (leçons E15), gen-plan v3.35.2 (porteur).

## §4 Risques et adaptations (règle d'or n°1)

- Recyclage sandbox en cours de chaîne → reprise E1-RES (garde auto-réparante — preuves vivantes ×3).
- Renommage TSI → validation avant/après par l'arbitre ; original jamais modifié (non-destructif).
- Bump orchestrateur-tsi → cascade conformité KO-L004 (KB + miroir + integrity re-pass) avant de poursuivre.

## §5 Hors périmètre (différés/propriétaire — inchangés sauf traitement ci-dessus)

F3 complément couverture P1b (décision propriétaire) · branche test/compilation-windows@04accb8 (403 PAT — propriétaire) · plancher dessin-technique ≥1.3.0 (décision propriétaire) · push distant (GO propriétaire — KO-L009 point 5).

---

## Hooks de validation (E8)

Horodatage plan : 2026-11-06T21:31:00Z

Verdict E8 : PASS (P1 plan présent · P2 answer key 12 décisions/12 vérifications · P3 worklog R5 · P4 PLAN-AFFICHE · P5 frais — Horodatage vérifié : 2026-11-06T21:31:00Z)
