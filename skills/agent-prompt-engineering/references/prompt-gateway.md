# Prompt-Gateway — spécification intégrale du mode M5 (agent-prompt-engineering v1.1.0)

> Référence intégrale du §1.6 du SKILL.md (progressive disclosure R1 — le SKILL.md porte le résumé, le présent fichier l'intégral).
> Directive propriétaire 2026-11-21 (Task 112 G1) : « fais en sorte que mon écosystème l'exécute automatiquement de façon autonome lorsque j'envoie à mon IA un prompt qui n'est ni court et ni simple à exécuter. Ce skill doit automatiquement analyser mon prompt, évaluer sa complexité, puis le retranscrire $FACON et l'envoyer en version compréhensible, explicite et structurée à mon IA. »
> Précision propriétaire 2026-11-21 (trace 1a1fc7b1728869e9) : « je précise que agent-prompt-engineering doit être exécuté à chaque fois que j'envoie un prompt à mon IA » — le déclenchement est INCONDITIONNEL ; la complexité route la profondeur, pas l'exécution.
> Glossaire : $FACON = « de façon cohérente, optimisée et fonctionnelle » · $FACON2 = « (cohérent, optimisé et fonctionnel) » (registre alias-eco).

## §1 — Objet et positionnement

Le mode PROMPT-GATEWAY (M5) fait d'agent-prompt-engineering la **porte d'entrée SYSTÉMATIQUE des prompts** de l'écosystème. Il ne remplace ni gen-plan (planification des tâches), ni l'orchestrateur ULTRA (routage entre PMs) : il s'intercale ENTRE le message du propriétaire et l'exécution, **à CHAQUE prompt**, pour garantir que l'IA reçoive une entrée sans ambiguïté.

Le déclenchement est AUTOMATIQUE ET INCONDITIONNEL (description de routage du SKILL.md + §A — précision propriétaire trace 1a1fc7b1728869e9) : aucune mention explicite du skill n'est requise dans le prompt du propriétaire ; les phases A-B (analyse + évaluation de complexité) s'exécutent sur TOUT prompt ; les phases C-D (retranscription + envoi structuré) uniquement sur verdict COMPLEXE (≥ 2/5 critères).

## §2 — Phase A : analyse du prompt

Inventaire exhaustif AVANT tout jugement :

1. **Métriques brutes** : nombre de mots, de paragraphes, de verbes d'action conjugués à l'impératif, de sous-instructions imbriquées (guillemets, accolades, listes).
2. **Étapes** : explicites (numérotées, « puis », « ensuite », « dans l'ordre ») et implicites (« fais de même » = rejouer la procédure citée).
3. **Dépendances** : ordre contraignant entre étapes (B exige la sortie de A), parallélisation possible, ressources partagées.
4. **Livrables** : fichiers attendus (noms, formats), messages, verdicts, plans.
5. **Références externes** : URLs, chemins de fichiers, noms de skills/agents, numéros de version, citations imbriquées.
6. **Ambiguïtés et implicites** : pronoms sans antécédent unique, expressions référentielles (« la même chose », « comme précédemment »), termes à désambiguïser.
7. **Contraintes** : langue, ordre imposé, conditions (« si c'est le cas alors »), limites (« max 2 rounds »).

Sortie : fiche d'analyse compacte (le propriétaire n'a pas besoin de la voir en entier — elle alimente la phase B).

## §3 — Phase B : évaluation de complexité (grille GO/NO-GO)

Cinq critères indépendants (grille §1.6 du SKILL.md). Règle de décision :

- **≥ 2 critères COMPLEXE → GO** (phases C-D exécutées) ;
- **≤ 1 critère COMPLEXE → NO-GO** (prompt passé tel quel à l'IA, aucune transformation, journalisation worklog du verdict).

Règle d'indécision : un critère indécidable compte COMPLEXE (prudence — mieux vaut structurer à tort que rater une exécution).

## §4 — Phase C : retranscription $FACON

### §4.1 Gabarit de sortie (version compréhensible, explicite et structurée)

```markdown
### Prompt retranscrit $FACON2 — [titre court dérivé de l'objectif]

**Objectif** : [une phrase — ce que le propriétaire veut obtenir, in fine]

**Contexte** : [faits, état, sessions/fichiers/URLs cités — seulement ce qui conditionne l'exécution]

**Contraintes** : [langue, ordre imposé, formats, limites, conditions]

**Étapes ordonnées** :
1. [étape — verbe d'action + objet + sortie attendue]
2. […]

**Dépendances** : [B après A ; C et D parallélisables ; …]

**Livrables** : [fichiers/messages/verdicts, avec noms et formats]

**Critères d'acceptation** : [comment le propriétaire jugera que c'est réussi]
```

### §4.2 Règles de retranscription

1. **Zéro perte sémantique** : tout nom propre, URL, chiffre, version, chemin, contrainte et condition de l'original figure dans la retranscription. Vérification point par point avant la phase D (liste de contrôle : chaque sous-instruction de l'original → au moins une ligne du gabarit).
2. **Zéro ajout d'intention** : la retranscription explicite l'intention du propriétaire, elle ne l'invente jamais. Les interprétations nécessaires à la désambiguïsation sont marquées « [interprétation : …] ».
3. **Doublons dédupliqués** (R4) : une demande répétée à l'identique dans le prompt original n'apparaît qu'une fois, avec mention « (cité ×N dans l'original) ».
4. **Langue** : la retranscription est en français (règle d'or n°6) ; les artefacts techniques cités verbatim (chemins, commandes, identifiants, extraits de code) conservent leur forme d'origine.
5. **Économie** : le gabarit reste plus court que l'original quand l'original est verbeux ; il peut être plus long quand l'original était dense et implicite — la clarté prime, jamais le gonflement.

## §5 — Phase D : envoi à l'IA

1. Le bloc « Prompt retranscrit $FACON2 » est affiché au propriétaire en tête d'exécution (transparence — le propriétaire voit l'entrée réelle de son IA).
2. La version structurée devient l'entrée d'exécution (les étapes, dépendances et critères d'acceptation alimentent directement la planification aval — gen-plan E1 s'il y a lieu).
3. L'original est conservé en citation (provenance) — aucune exécution sur une interprétation non tracée.
4. Journalisation worklog R5 : verdict de complexité (critères GO/NO-GO), #token original → #token retranscrit, décisions d'interprétation.

## §6 — Exemples

### §6.1 GO — prompt complexe (le présent cas d'école, trace 1a1fc6f31a7bf61d)

Original (extrait) : « fais dans l'ordre les étapes suivantes : "{ - installe mon écosystème… et lorsque l'installation sera terminée, prend en compte mon skill gen-plan fraichement installé pour générer le plan d'actions des étapes suivantes : "{ - gen-plan (step) : … }" » — imbrication de guillemets multiples, ordre contraignant (installation AVANT plan), livrables multiples, dépendance explicite entre blocs.

Critères : longueur COMPLEXE · étapes COMPLEXE · ambiguïté COMPLEXE (« fais de même » à désambiguïser par référence au paragraphe précédent) · livrables COMPLEXE · contexte COMPLEXE → **GO (5/5)**.

Retranscription : objectif = exécuter la chaîne complète (installer → planifier → tester/optimmiser 10 skills → correct-work ×2 → clone-chat) ; contexte = écosystème Knowledge, dépôt bigleon2/KNOWLEDGE, pins a5daa964/aaac4fa1 ; contraintes = ordre strict des étapes, mode step sans validation, français ; étapes = 1. installation bootstrap canonique 2. plan gen-plan 3. tests/optims G1-G8 4. correct-work --bloc 5. tests conditionnels G10-G12 6. correct-work --bloc 7. clone-chat ; dépendances = 1 avant 2, 2 avant 3, 3 avant 4… ; livrables = écosystème installé certifié, plan, skills optimisés, rapports, clone ; critères = certification ALL PASS, answer key D001-D011 verified, verdicts correct-work PASS.

### §6.2 NO-GO — prompt court et simple (le skill s'exécute, la retranscription est omise)

Original : « quelle heure est-il ? » — 4 mots, 0 action-outil, réponse immédiate, autosuffisant → 0 critère COMPLEXE → **NO-GO** : phases A-B exécutées (analyse + verdict COURT/SIMPLE journalisé), passage direct SANS retranscription — le déclenchement du skill a bien eu lieu (inconditionnel), seule la profondeur est réduite.

## §7 — Tests et garde de non-régression

- `evals/trigger_evals.json` porte les cas de routage (positifs : prompts complexes avec imbrication/ordre/livrables ET cas triviaux à déclenchement garanti par arbitrages voie L documentés — précision propriétaire trace 1a1fc7b1728869e9, cache `scripts/voie-l-cache.json` ; négatifs : requêtes du périmètre réservé d'autres skills — doctrine V6.1/V6.2) — l'arbitre `scripts/check-triggers-replay.py` doit rester PASS (0 dérive) à toute évolution du présent skill.
- `evals/evals.json` porte le scénario de retranscription (id 6 — APE-prompt-gateway).
- Toute évolution du gabarit §4.1 = montée de version PATCH (recalibrage croisé KO-L004 : KB, arbitres, certification).
