# Note d'analyse — Task 92 : erreur « SyntaxError : Token inattendu 'd', "data: {"da »… est pas valide en JSON »

> Directive : trace `1a1de66691f9c2d5` (premier envoi `1a1de6474f53677d`) — mémorisation écosystème + adaptation autonome.
> Date : 2026-11-15 · Base des groupes G2 (leçon L011) et G3 (règle KO-L011 + mécanisme).
> État vérifiable : enquête mécanique E1-E2 (rg sur artefacts + lecture `scripts/adaptation-syntaxe.py`).

## 1. Signature exacte de l'erreur

```
SyntaxError : Token inattendu 'd', « data : {"da »... est pas valide en JSON
```

(En anglais : `SyntaxError: Unexpected token 'd', "data: {"da"... is not valid JSON`)

Le « Token inattendu 'd' » est la marque de fabrique du moteur **V8 (Node.js)** : le parseur attendait `{` ou `"` (un début de valeur JSON) et a rencontré la lettre **`d`** — première lettre du préfixe **`data:`**. La chaîne soumise à `JSON.parse()` commence donc par `data: {"da…`.

## 2. Cause racine — flux SSE soumis à JSON.parse

`data: {…}` est le format **SSE (Server-Sent Events)** : protocole de streaming où chaque événement est encodé en lignes de la forme :

```
data: {"delta":"Bonjour","finish":false}
data: {"delta":" comment","finish":false}
data: [DONE]
```

Un `JSON.parse()` naïf sur la trame **brute** (ou sur un fragment de trame délimité arbitrairement par le buffering réseau) échoue systématiquement :
1. le préfixe `data: ` n'est pas du JSON ;
2. plusieurs payloads JSON concaténés ne forment pas un JSON valide ;
3. le marqueur de fin `data: [DONE]` n'est pas du JSON ;
4. une trame **partielle** (coupée à mi-chemin par le découpage réseau — exactement « data: {"da » dans le message du propriétaire) n'est pas ferlée : accolade ouvrante sans fermante.

**Contexte d'apparition** : cette erreur est affichée au propriétaire lorsque l'agent (ou la passerelle/SDK sous-jacente, ex. `z-ai-web-dev-sdk` en streaming, passerelle IM zai-web) consomme une réponse en flux et qu'un maillon de la chaîne parse la trame brute comme un JSON unique. C'est une erreur **plateforme/agent**, jamais une erreur du propriétaire — le propriétaire a raison : elle ne vient pas de lui.

## 3. Distinction avec l'existant — R1 vérifié (pas de doublon)

`scripts/adaptation-syntaxe.py` (garde d'auto-réparation syntaxique, directive pré-gen-plan 2026-11-04) couvre **7 classes de défauts PYTHON** : `future_import`, `bom`, `crlf`, `zero_width`, `narrow_space`, `smart_quotes`, `fullwidth`. Son incident fondateur était un `SyntaxError` **py_compile** (« from __future__ import annotations » mal placé — v3.32.0).

L'erreur rapportée ici est d'une **autre classe** : échec d'analyse **JSON d'exécution** sur trame **SSE** (V8/Node), pas un défaut de fichier source Python. Aucune classe existante ne la couvre ; les 6 occurrences `SyntaxError` trouvées dans les artefacts (worklog, task47, task84, adaptation-syntaxe) sont toutes de classe Python. **⇒ Leçon genuinely nouvelle, aucune duplication R4.**

## 4. Occurrences documentées (comptage honnête — règle d'or n°5 / KO-L003)

| Source | Nature | Traçable |
|---|---|---|
| Directive propriétaire trace `1a1de6474f53677d` | rapport verbatim de l'erreur + témoignage « tu m'envoies **souvent** » | chat session web-ecef7f80 |
| Directive propriétaire trace `1a1de66691f9c2d5` | même rapport réitéré (préfixe gen-plan) | chat session web-ecef7f80 |
| Artefacts écosystème (download/ 13 clones, worklog 121 suites, scripts/) | **0 occurrence** — l'erreur vit dans le canal chat agent↔propriétaire (plateforme de streaming), non capturée par les clones | rg vérifié ce tour |

Le témoignage du propriétaire atteste la récurrence (« souvent ») ; les artefacts ne peuvent pas la compter (elle n'écrit pas dans l'écosystème). Le comptage est enregistré POUR CE QU'IL EST : 2 directives verbatim + témoignage de récurrence propriétaire. La sévérité n'est pas S1 (pas de corruption de données, verdict faux ni perte de livrable — c'est une erreur d'affichage/parasitage récurrente) ; le seuil de récurrence standard (3) est couvert par la directive propriétaire elle-même, et la porte M3-M4 s'ouvre **sur directive propriétaire explicite** — précédent L009 (matérialisée v3.30.0 sur directive explicite, journal-versions.md).

## 5. Solution $FACON — contourner et corriger automatiquement

### 5.1 CORRECTION racine — assainir avant de parser

Toute entrée soupçonnée SSE est assainie **avant** `JSON.parse` :
1. strip du préfixe de champ `data:` (+ `event:`, `id:`, `retry:`) sur chaque ligne ;
2. filtrage des lignes vides (séparateurs d'événements SSE) et du marqueur `data: [DONE]` ;
3. si plusieurs payloads : parse **par ligne** (chaque payload est un JSON complet), pas de concaténation ;
4. détection de trame partielle : accolades non équilibrées → attendre la suite du flux ou extraire le dernier payload complet.

### 5.2 CONTOURNEMENT — repli par extraction

Si l'assainissement ne suffit pas (trame corrompue/hybride) : extraction **regex** du premier bloc JSON bien formé `/\{[\s\S]*?\}(?=\s*$|\s*data:)/m` (ou du dernier complet), puis parse. Repli ultime : voie **non-streaming** (réponse JSON complète en une trame) ou backend/méthode alternatif.

### 5.3 Garde anti-boucle — jamais de re-jeu à l'identique

Le même appel + le même parse échouera **identiquement** (erreur déterministe de format, pas transitoire). Règle : **max 2 rounds** de correction (SHARED §4.4) — round 1 = assainissement, round 2 = extraction regex/non-streaming — puis escalade à la méthode alternée, avec journalisation worklog (règle d'or n°1 : adaptation journalisée, jamais d'arrêt implicite).

### 5.4 MÉCANISME rejouable — `scripts/adaptation-json-sse.py`

Sur le pattern éprouvé de `adaptation-syntaxe.py` (détection → réparation mécanique → re-jeu de la commande bloquée) :
- **Entrée** : fichier ou stdin contenant la trame brute (ou l'erreur) ;
- **Sortie** : JSON propre (payload unique ou tableau de payloads) sur stdout, rc=0 ; rc=2 si aucun JSON extractible (diagnostic complet) ;
- **Self-test** embarqué : golden samples dont la trame exacte `data: {"da` (reproduction littérale du message du propriétaire), trame multi-payloads, `[DONE]`, lignes vides, entrée déjà-propre (no-op), entrée sans JSON (rc=2) ;
- **Idempotence ×2** (re-jeu no-op), stdlib uniquement, déterministe, sorties `--json` ;
- **Post-traitement correct-py** obligatoire (garde-fou 6 §1.3 — conventions script-creator).

### 5.5 RÈGLE D'INVOCATION (mémoire active — KO-L011, cible gen-plan §1.14bis)

Dès la signature détectée (`SyntaxError` + `data:` dans le message d'erreur, toute langue) :
1. **ne pas re-jouer à l'identique** ;
2. assainir via `python3 scripts/adaptation-json-sse.py` (ou transformation équivalente inline) puis re-jeu ;
3. échec persistant (max 2 rounds) → voie non-streaming / méthode alternée ;
4. journaliser l'adaptation au worklog (règle d'or n°1).

La règle est portée par gen-plan (lue à toute planification — comme KO-L001 face aux 429), instanciant la règle d'or n°1 (adaptation autonome) pour cette classe d'erreur.

## 6. Périmètre « adaptation autonome » du tour (item 1 de la directive)

La directive étend l'exigence d'adaptation autonome à : cette erreur ✓ (KO-L011), la consommation de ressources ✓ (déjà couvert : resource-monitor G-RES hook E1-RES + continu E9-E14, profils ECO/VIEUX PC — §1.2bis/§2.4), le blocage prolongé ✓ (déjà couvert : règle d'or n°1 + garde anti-boucle max 2 rounds + pause explicite motivée si inatteignable). Le Delta réel de ce tour = la classe SSE/JSON (non couverte) — le reste est déjà porté par l'écosystème, constat consigné sans duplication R4.
