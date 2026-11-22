# ANALYSE — Intégration des déclencheurs skills/agents dans gen-plan (Task 114)

**Trace** : 1a2025197d2a0e9d (session web-f492e049) · **Date** : 2026-11-22 · **Verdict** : idée JUDICIEUSE dans sa variante scriptée, DÉGRADANTE dans sa variante incrustée
**Livrables liés** : `skills/gen-plan/scripts/routage-skills-agents.py` v1.0.0 · gen-plan v3.47.0 (§0 rappel langue, §1.16 É5-ROUTAGE, §1.17, §2.2, §3, §4) · `ensure-installed.py` garde réinjection plateforme · cascade KO-L004 complète (certification ALL PASS 6/6)

---

## 1 — La demande et les trois options possibles

Le propriétaire demande : (a) intégrer les déclencheurs des skills et des agents de
l'écosystème dans le corps de gen-plan ; (b) forcer gen-plan à utiliser ces
déclencheurs quand la situation adéquate se présente ; (c) si l'utilisation des agents
n'est justifiée que dans des cas complexes, intégrer un script qui orchestre cette
prise de décision. Trois implantations sont possibles ; elles ont été mesurées sur
l'arbre réel (73 skills installés, 4 agents) avant décision.

## 2 — Mesures (arbre réel, 2026-11-22)

| Mesure | Valeur | Source |
|--------|--------|--------|
| Poids gen-plan avant | 35 702 o (34,9 Kio) | `wc -c` |
| Catalogue complet des déclencheurs (descriptions + read_when des 72 skills scannés) | **102 620 o (100,2 Kio)** | script de routage (scan frontmatters installés) |
| Option A — gen-plan après incrustation | **139,1 Kio → 2,3× le seuil CRITIQUE (60 Kio)** de l'arbitre poids-chargement | calcul |
| Option C — gen-plan après intégration scriptée | **39 788 o (38,9 Kio, +3,99 Kio, +11,4 %)** — reste LOURD, sous le seuil CRITIQUE | `wc -c` |
| Durée murale du script de routage (×4 tâches variées) | **41-46 ms** (moyenne 44 ms, cible < 1 s) | `time.perf_counter` subprocess |
| Sortie JSON consignée | **2 251 o (~2,2 Kio)** par plan | `download/routage-dernier.json` |
| Selftest script | **9/9 PASS** | `--selftest` |

## 3 — Analyse des trois options

### Option A — incrustation du catalogue complet (rejetée : DÉGRADE)

Copier les déclencheurs des 72 skills + 4 agents dans le corps de gen-plan coûte
+100,2 Kio : gen-plan franchit 139,1 Kio, soit 2,3× le seuil CRITIQUE de l'arbitre
poids-chargement (E5-POIDS, ≥ 60 Kio). gen-plan étant chargé à CHAQUE session de
planification, la dégradation frappe toute session, même triviale — l'inverse de
l'objectif d'automatisation. Deuxième dégradation, structurelle : R4 (jamais
dupliquer) est violé — les déclencheurs vivent DÉJÀ dans les frontmatters installés
(description + read_when, convention Task 28) et dans le registre KB ; toute copie
créerait une dérive silencieuse à chaque édition d'un skill, avec une cascade
KO-L004 (recalibrage gen-plan) à répéter pour CHAQUE montée de version des ~73
skills — une dette de maintenance récurrente et un risque de routage sur données
périmées.

### Option B — table compacte statique dans gen-plan (rejetée : sous-optimal)

Une ligne par skill (~6-8 Kio) réduirait le surcoût, mais resterait une DUPLICATION :
même lag, même cascade KO-L004, même perte de garantie que l'option A en plus petit.
Aucun avantage sur l'option C ; rejetée.

### Option C — routage mécanique à l'exécution (RETENUE : OPTIMISE)

gen-plan intègre un **hook É5-ROUTAGE** (§1.16) qui exécute à E5 et E7 le script
`routage-skills-agents.py` : celui-ci lit les frontmatters INSTALLÉS (source unique —
zéro duplication, zéro lag, zéro cascade), score chaque skill (description ×2,
read_when ×3 — le contrat de déclenchement Task 28), rend un **verdict de complexité
5 critères** et porte-garde les **agents** : recommandés uniquement si verdict
COMPLEXE (≥ 2/5 critères — grille alignée sur le PROMPT-GATEWAY agent-prompt-engineering
§1.6), conformément au point (c) de la demande. Coûts réels : +3,99 Kio dans le corps
de gen-plan (une fois), ~300 #token et 44 ms par plan, sortie JSON ~2,2 Kio.
Économie nette par rapport à l'option A : **~96 Kio de charge évitée à chaque session**,
plus la suppression de la dette de recalibrage croisé.

### Verdict sur la consommation de tokens

| Option | Coût session (gen-plan) | Coût par plan | Duplication/lag | Verdict |
|--------|-------------------------|---------------|-----------------|---------|
| A — incrustation | +100,2 Kio (CRITIQUE ×2,3) | 0 | oui — cascade KO-L004 ×73 skills | DÉGRADE |
| B — table statique | +6-8 Kio | 0 | oui — lag silencieux | sous-optimal |
| **C — script exécution (retenue)** | **+3,99 Kio (une fois)** | **~300 #token, 44 ms** | **non — source unique** | **OPTIMISE** |

## 4 — Comment gen-plan est « forcé » d'utiliser ses déclencheurs

Le forçage est réalisé par trois mécanismes complémentaires (additions pures,
non-régression des déclencheurs existants — arbitre check-triggers-replay PASS) :

1. **Hook É5-ROUTAGE §1.16** — prescription d'exécution du script à E5 (sélection)
   et E7 (plan — section « Routage »), sortie consignée `download/routage-dernier.json`
   (preuve vérifiable, règle d'or n°5) ;
2. **Porte d'agents §1.17** — la délégation d'agent est SUBORDONNÉE au verdict
   COMPLEXE du script (matrice dynamique R4 : les objectifs .agent sont lus à
   l'exécution, jamais copiés dans le corps) ;
3. **Rappel permanent langue (§0, v3.47.0)** — directive 1a2025ce4a6ed095 : à chaque
   exécution de gen-plan, rappel du FRANÇAIS exclusif avec le propriétaire
   (dérive chinois constatée au tour précédent, corrigée et journalisée au worklog ;
   durcissement : correction immédiate + worklog + rappel permanent).

## 5 — Extension du système décisionnel à d'autres skills/agents

Analyse des interactions demandée par le propriétaire (« ce système pourrait-il être
à d'autres skills ou agents selon leurs interactions avec le reste de mon
écosystème ? ») :

| Élément | Interaction avec le système décisionnel | Décision |
|---------|-----------------------------------------|----------|
| **orchestrateur-tsi** (2ᵉ orchestrateur) | Route la famille TSI par micro-spécifications de mission DÉJÀ mécaniques (concevoir→valider→documenter) ; le script générique le recommande déjà (preuve : score 13 sur la tâche d'audit — test F) | **Aucune modification** — ajouter le scoreur générique dupliquerait son routage de domaine (R4) ; il reste une CIBLE du routage gen-plan |
| **4 agents (.agent)** | Cibles du routage (matrice dynamique §1.17 lisant leurs objectifs) — jamais routeurs | **Aucune modification** (déjà intégrés) |
| **skills-inventory** | Périmètre inventaire/listing ; le script de routage COMPLÈTE (trouve pour une tâche) sans chevaucher | **Aucune modification** — complémentarité documentée ici |
| **correct-work / arbitres** | Consommateurs de verdicts, pas de routage | **Aucune modification** |
| **gen-plan** | Détenteur du hook | **Modifié (v3.47.0)** |

**Conclusion d'extension** : le système décisionnel est pertinent UNIQUEMENT pour les
ORCHESTRATEURS de skills/agents. L'écosystème en compte exactement deux : gen-plan
(modifié ce tour) et orchestrateur-tsi (mécanisme de domaine propre déjà suffisant —
modification non justifiée, justification documentée ci-dessus). Aucune autre
modification n'est nécessaire ; le script reste réutilisable tel quel par tout futur
orchestrateur (chemin canonique `skills/gen-plan/scripts/routage-skills-agents.py`,
interface `--tache --format json`).

## 6 — Garde associée : réinjection plateforme (ensure-installed.py)

Constat du tour : la plateforme réinjecte ses skills natifs au démarrage de session —
les 17 SKILL.md français (Task 113) sont écrasés et les 4 dossiers majuscules
ASR/LLM/TTS/VLM recréés ; l'audit passait de 73/73 à 60/77 entre deux tours.
La garde Task 114 étend `ensure-installed.py --check` : détection par signature native
(clawdbot ou absence de §0 « Contexte Système »), réparation depuis le miroir
(règle d'or n°4), suppression des dossiers majuscules SOUS garde d'archive R4
byte-identité (jamais de destruction sans preuve). Testé en conditions réelles :
`INSTALLE-RÉPARÉ` (13 restaurations + 4 suppressions) → `INSTALLE` idempotent ×2.

## 7 — Non-régression et certification

Arbitres re-jeu après intégration : verify-cross 168/168 · verify-correct-work 16/16 ·
check-ecosysteme-integrity 116/116 · interactions PASS STRICT 59/59 ·
check-tool-routing 7/7 · **certification ALL PASS 6/6** · bootstrap VERDICT GLOBAL
INSTALLE · audit conformité 73/73 skills + 4/4 agents · check-triggers-replay PASS.
Cascade KO-L004 complète : PM v3.47.0 généré mécaniquement, KB, pin ECO_SKILLS ×2
arbres, evals sync, propagation §0 (SHARED v1.7.45) ×2 arbres, archive v2.5 rescellée
×2 arbres.
