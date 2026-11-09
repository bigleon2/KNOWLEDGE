# Clone de discussion — Task 60 : PM-skill (D604 VALIDÉE) + correct-work v2.11.0 — 2026-11-07

> **Session** : web-c30e6506 · **Skill porteur** : gen-plan v3.35.2 (mode NULL — dérogation porte D604) · **Clone-chat** : v2.0.2 (format canon 7+1 étapes, condensé — le détail intégral vit au `worklog.md` et aux livrables cités)
> **Reprise** : une session héritière repart du §3 (décisions), vérifie le §5 (état disque) et lit le plan `download/plan-task60-ordre-directive-4-2-3-1.md`.

## §1 Contexte d'ouverture

Pile de directives intégrée (règle d'or n°3), ordre explicite (4)→(2)→(3)→(1) : recherche historique « n'invente jamais » → règle canonique « mon skill X = forme installée racine » → idée PM-skill (précisée E13-3 : PM éphémère MD extrait des SKILL.md, usage IA externe, proposition + validation propriétaire avant intégration) → correct-work v2.10.0 optimisée en v2.11.0 (DERNIÈRE action). État d'ouverture : corpus + 15ᵉ disparition version-management restaurés par pipeline (v2.10.0 Task 59 perdue au recyclage — jamais journalisée ni syncée ; survivant : plan-task59).

## §2 Chaîne d'exécution (G1→G5)

- **G1 (D601)** — inventaire historique exhaustif ancré disque : 12 versions correct-work + contrat v2.10.0 reconstitué + métriques (17 touches/montée, 13 montées/2 sem, lags ×4+, 16ᵉ disparition vm) + renommage @PM-SKILLS.
- **G2 (D602)** — SHARED v1.7.27 : règle canonique de désambiguïsation (§0/§1.2) + propagation 68 skills/150 scripts/2 agents.
- **G3-SG1 (D603)** — analyse $FACON : verdict portabilité AUGMENTE (couverture ×17, coût 0, lag 0, volatilité absorbée, R4 respecté) / remplacement corpus NE PAS APPLIQUER ; proposition « couche additive, corpus intact » (5 ajouts : injection §0, livraison vue-upload, préservation corpus, SHA-256, mode d'emploi IA).
- **G3-SG1b (D603b)** — tests comparatifs (E13-4) : harnais 24 tests, prototype embarqué en bac à sable — **16 PASS · 1 FAIL [défaut réel de l'actuel : PM gen-plan corpus non auto-portant] · 7 FACT** ; futur : 68/68, auto-portants, 0,4 ms/skill, régénération 1 ms, bump 1 ms.
- **ARRÊT PORTE PROPRIÉTAIRE D604** — présentation : analyse + tests + réponse à la question « la future version est mieux ? » (oui sur tous les critères de portabilité mesurés, complément — pas remplacement).
- **G3-SG2 (D604 VALIDÉE)** — directive verbatim « je valide ta proposition, tu peux l'exécuter $FACON pour me générer $FACON un écosystème $FACON2 » → intégration complète : skill `pm-skill` v1.0.0 + `scripts/generer-pm-ephemere.py` (self-test ST1-ST11 11/11 ×2, auto-application prouvée) + evals 4+3 vetos + KB 53e + pin + @historique + miroir bbff275. Incidents n°5 : 16ᵉ disparition vm auto-réparée (garde Task 56) + rescellement piliers.
- **G4 (D605/D606)** — correct-work v2.9.0→v2.11.0 : §1.5bis correctifs mode STEP (contrat v2.10.0 ré-intégré, lignage honnête) + matrice best-of §12 (13 lignes) + plancher gen-plan >=3.22.0 + arbitre 16/16 ×2 + cascade KO-L004 complète (PM 802 L, delta v2110, SHARED v1.7.28 [drifts §6.1 résorbés], PM-INSTALL v1.9.4, ULTRA dé-figé, v2.9.0 archivé R4, miroir 5544734). Incidents n°6 : 17ᵉ disparition vm auto-réparée + rescellement corrigé. **Preuve lag 0** : `PM-ephemere-correct-work-v2.11.0.md` généré immédiatement, featured ★.
- **G5 (D607)** — clôture : correct-work (projet) --bloc **PASS 5/5** + rapport final + présent clone.

## §3 Décisions (answer key D601-D607 — toutes done)

1. **D601** inventaire sourcé · **D602** règle canonique SHARED — faits.
2. **D603** verdict AUGMENTE (portabilité) + proposition couche additive — validée.
3. **D603b** tests comparatifs : futur domine tous les critères de portabilité ; ne remplace pas l'archive corpus (C7).
4. **D604 PORTE PROPRIÉTAIRE FRANCHIE** (validation explicite) → intégration pm-skill v1.0.0.
5. **D605/D606** correct-work v2.11.0 + cascade complète — best-of 12 versions + §1.5bis.
6. **D607** clôture --bloc PASS 5/5.

## §3.5 Context Drift

Aucun drift de langue (règle d'or n°6 tenue — français intégral). Dérives d'état absorbées : 6 manifestations de volatilité (2 auto-réparations autonomes garde Task 56, 1 perte ciblée plan réécrite, 1 rescellement corrigé) — toutes journalisées règle d'or n°1. Le mode NULL a tenu SAUF la porte D604 (arrêt bloquant respecté, dérogation documentée).

## §4 Artefacts (tous vérifiables sur disque)

`download/` : inventaire-historique-task60.md · analyse-idee-pm-skill.md · rapport-tests-task60.md (+ tests-task60/) · rapport-final-task60.md · PM-ephemere-pm-skill-v1.0.0.md · PM-ephemere-correct-work-v2.11.0.md (★) · plan-task60-ordre-directive-4-2-3-1.md. `skills/` : pm-skill/ (SKILL.md + evals/) · correct-work/SKILL.md v2.11.0 · @mon-ecosysteme/ (PM v2.11.0, SHARED v1.7.28, PM-INSTALL v1.9.4) · @historique/historiques-par-skill/{pm-skill,correct-work}.md · KNOWLEDGE.md (53 entrées). `scripts/` : generer-pm-ephemere.py · delta-correctwork-v2110.json · check-ecosysteme-integrity.py (pin 53) · ecosysteme-integrity.json · gen-ultra-maitre.py (dé-figé). Worklog : chaîne G1→G5 complète + incidents ×6.

## §5 État disque final (règle d'or n°5 — vérifiable)

integrity **110/110 ×2** · verify-correct-work **16/16 ×2** · verify-cross **100 %** · pm-skill self-test **11/11 ×2** · corpus 9 fichiers · miroir bbff275 + 5544734 (push KO-L009 différé). Versions : gen-plan 3.35.2 · correct-work 2.11.0 · clone-chat 2.0.2 · refactor-guard 1.8.1 · SHARED 1.7.28 · PM-INSTALL 1.9.4 · pm-skill 1.0.0.

## §6 Reprise pour session héritière

1. Vérifier É1-INSTALL (ensure-installed --check) — la volatilité L55-3 est la cause racine documentée (17 disparitions vm à ce jour, 2 auto-réparations ce tour).
2. Pendances §5 du plan : Task 58 G2/G3 (dessin-technique v1.3.0, clôture 58) · push distant KNOWLEDGE (GO propriétaire) · rotation PAT · F1 Traktor · F3 P1b.
3. Usage pm-skill : `PM-skill(<nom-du-skill>)` → `download/PM-ephemere-<skill>-v<version>.md` → coller comme prompt système dans l'IA de votre choix.

*Clone scellé — aucune information de ce fichier ne contredit l'état du disque (règle d'or n°5).*
