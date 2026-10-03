# verification-protocol.md — Protocole de vérification Second Opinion (mode AVEUGLE)

Version : 1.0.0 · Créé : phase N20 (session B12-r41) · Restauré : B13-r5 (trace `1a0dfca3a0ffe13d`, post-wipe inter-sessions — reconstitué d'après la spécification N20 du worklog et le mode AVEUGLE installé dans correct-work v2.6.0 ; le contenu exact d'origine est perdu au wipe).

<!-- PATTERN:VERIFICATION-PROTOCOL-v1.0.0 -->

## §0 — Contexte Système (SHARED v1.6.0)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case | semver | #token | {{VARIABLE}} | @mon-ecosysteme/ (exception)
> Règle Zéro : skills auto-contenus, registre KB source de vérité, cross-references bidirectionnelles.

## §1 — Le protocole Second Opinion

### §1.1 Problème

Un vérificateur qui connaît le raisonnement de construction du livrable hérite de ses angles morts : il retrouve naturellement le chemin emprunté et confirme les mêmes choix (biais de confirmation). Une vérification menée « dans le contexte » valide l'intention, pas le résultat.

### §1.2 Solution — la vérification aveugle

La Second Opinion est une re-vérification menée **sans le contexte de construction** : un arbitre (ou une instance de vérification dédiée) reprend le livrable à froid, avec uniquement les inputs filtrés (§2), et reformule indépendamment les verdicts. Elle est déclenchée par correct-work au hook « 2nd opinion agent-driven » (Étape 5) : tout FAIL ou divergence détectée entraîne une re-vérification aveugle, dans la limite de 2 rounds (SHARED §4.4 — garde anti-boucle).

## §2 — Inputs filtrés (ce que la Second Opinion voit)

| Voit | Ne voit PAS |
|------|-------------|
| Le livrable final (fichiers, rapports, artefacts) | **Historique de construction** (raisonnements, itérations, tentatives abandonnées) |
| Les exigences/critères d'acceptation | Les justifications de l'auteur du livrable |
| Les conventions de référence (SHARED, PM) | Les interprétations intermédiaires qui ont conduit au résultat |
| Les arbitrages mécaniques (SHA, comptages) | Les verdicts préliminaires de la vérification « dans le contexte » |

L'instance de vérification aveugle reformule ses critères AVANT de lire le livrable (answer key pré-écrite quand disponible), puis confronte ses conclusions aux résultats sans les modifier a posteriori.

## §3 — Les 4 étapes du protocole

| Étape | Action | Sortie |
|-------|--------|--------|
| 1 | **Cadrage à froid** : reformuler les exigences à partir des seuls inputs filtrés | critères indépendants |
| 2 | **Vérification aveugle** : auditer le livrable sans le contexte de construction | verdicts indépendants |
| 3 | **Confrontation** : comparer aux verdicts initiaux ; toute divergence est un signal S1/S2 à documenter | matrice de divergence |
| 4 | **Décision** : divergence confirmée → correction obligatoire + re-verdict (max 2 rounds) ; convergence → verdict final consolidé | verdict + worklog |

## §4 — Intégration correct-work

- **Mode AVEUGLE** (correct-work v2.6.0, §1.2/§10.4) : `correct-work(aveugle)` force l'application du présent protocole sur la cible.
- **Hook 2nd opinion agent-driven** (Étape 5) : FAIL ou divergence → re-vérification aveugle ; convergence requise pour tout verdict final ; max 2 rounds (garde anti-boucle SHARED §4.4).
- **Journalisation** : chaque round (inputs fournis, verdicts, divergences) est tracé au worklog — jamais d'édition silencieuse.

## §5 — Garde-fous

1. Les inputs filtrés sont construits AVANT le cadrage à froid (sinon le contexte s'y infiltre).
2. L'instance aveugle ne consulte ni le worklog de construction ni les justifications de l'auteur.
3. Toute divergence est documentée même si elle est résolue (matrice conservée).
4. La Second Opinion ne remplace pas la vérification standard (correct-work 5 étapes) : elle la double sur demande ou sur divergence.

<!-- FIN-PATTERN:VERIFICATION-PROTOCOL-v1.0.0 -->

## §6 — Provenance

- **v1.0.0 — 2026-09-19 (phase N20, session B12-r41)** : création d'après `propositions-qwen.md` (pattern Second Opinion) — hook agent-driven ajouté à correct-work Étape 5, mode AVEUGLE matérialisé.
- **2026-09-26 (B13-r5, trace `1a0dfca3a0ffe13d`)** : restauration post-wipe inter-sessions — reconstitution conforme au mode AVEUGLE installé et à la spécification N20 (worklog) ; le fichier d'origine est perdu.
