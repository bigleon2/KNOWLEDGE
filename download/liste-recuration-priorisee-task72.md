# Liste priorisée des prochaines re-curations progressive disclosure — Task 72 G3 (D008)

**Date : 2026-11-08** · Session : web-ecef7f80 · Plan : download/plan-task72-recuration-genplan-adequation-liste-skill-recuration.md (rév. 3) · Précédent accompli : gen-plan v3.38.0→v3.39.0 (104,0→29,9 Kio, −71,2 % — G1, commit dépôt 5646e96)
Méthode : mesure mécanique (poids-chargement.py ×2 idempotent — mesures identiques), croisement disque (échantillon 5/5 PASS), classification gouvernance (KB + ECO_SKILLS), multicritère (gain #token × risque dépendants × stabilité × fréquence), cartographie sèche SANS ÉCRITURE du candidat n°1 écosystème.

## 1. État mesuré (T3.1 — arbitre poids-chargement.py, re-jeu ×2 identique)

**70 skills : 28 OK · 33 intermédiaires · 9 LOURD · 0 CRITIQUE** (seuils : OK < 12 / LOURD ≥ 30 / CRITIQUE ≥ 60 Kio — le CRITIQUE unique de l'écosystème, gen-plan, est résorbé en G1).

## 2. Tableau trié par priorité (T3.3 — multicritère)

| Rang | Skill | SKILL.md | #token | Dépendants KB | Gouvernance | Gain estimé* | Risque | Justification du rang |
|---|---|---|---|---|---|---|---|---|
| **1** | **version-management** | 46,1 Kio | 11 811 | 0 | écosystème (KB v1.3.0, ECO_SKILLS) | ~55-60 % → ~18-22 Kio | faible (0 dépendant) + contrainte miroir | Plus lourd skill écosystème stable ; top-8 sections = 26,2 Kio déplaçables (§1.3 structure 5,8 Kio · §3.4 send_file 5,6 · §3.1 points d'entrée 3,5 · §6 aide-mémoire 3,0 · §8 résorption 2,3 · §1.2 chemins 2,2 · §5 meta.json 1,6) ; **contrainte spécifique : 6ᵉ disparition le 2026-11-08 (volatilité plateforme) — la re-curation DOIT être synchronisée hôte + miroir dans la même passe (l'auto-réparation restaure depuis le miroir)** |
| **2** | **iphone19** | 50,0 Kio | 12 793 | 0 | écosystème (KB v0.11.0, ECO_SKILLS) | ~50-60 % → ~20-25 Kio | faible (0 dépendant) + évolution active | Plus lourd écosystème toutes générations ; top-8 = 24,1 Kio dont **changelogs 4,9 Kio = archive pure (meilleurs candidats R4, zéro perte fonctionnelle)** ; §2 moteur R1-R19 (5,1 Kio) + §0 rôle (4,5) + §11 auto-audit (2,8) + presets (2,6) ; à re-curer AVANT la montée v1.0.0 prévue (éviter le double churn) |
| **3** | **iphone18** | 40,4 Kio | 10 348 | 0 | écosystème (KB v1.1.0) | ~50-55 % | faible | Génération courante CONFIRMÉE, structure sœur d'iphone19 — mutualisation des gabarits de re-curation (même cartographie) |
| **4** | **skill-creator** | 40,4 Kio | 10 330 | **12 — NOYAU** | écosystème (KB v1.1.0) | ~50 % | **élevé (rayon d'explosion 12 skills)** | Chargé par 12 dépendants — gain réel le plus élevé en usage cumulé, mais protocole renforcé obligatoire (golden master + evals + sweep 12 citations) ; à exécuter APRÈS validation du skill re-curation (G4/G5) sur les candidats 1-3 |
| **5** | **web-reader** | 31,3 Kio | 8 021 | 0 | écosystème (KB v1.0.0) | ~45-50 % | faible | Juste au-dessus du seuil LOURD ; gain modéré |
| **6** | **cahier-des-charges** | 30,8 Kio | 7 895 | 0 | écosystème (KB v2.0.2) | ~35-45 % | faible | Déjà partiellement décentralisé (4 fichiers references/ = 34,2 Kio existants) — gains résiduels moindres, structure à compléter |
| **7** | **iphone17** | 34,2 Kio | 8 753 | 0 | écosystème (KB v1.1.0) | ~50 % | faible | Génération supersédée (18/19 actives) — usage rare ; poids sous contrôle, priorité basse malgré la taille |
| **8** | **pdf** | 58,3 Kio | 14 927 | 1 | **PLATEFORME (hors KB/ECO_SKILLS)** | ~55-65 % → ~21-26 Kio | **gouvernance : hors écosystème** | Plus lourd skill du profil ; cartographie sèche disponible (46 sections : routing matrix 4,4 Kio · tooling reference ~7 Kio · file map 3,1 · engine selection 3,1 · quality checklists ~4 Kio) ; **hors gouvernance écosystème (pas d'entrée KB, pas de cascade KO-L004, risque de régression silencieuse au cycle plateforme suivant) — re-curation locale POSSIBLE mais sur décision explicite du propriétaire** |
| **9** | **pptx** | 39,5 Kio | 10 100 | 0 | **PLATEFORME (hors KB/ECO_SKILLS)** | ~50 % | gouvernance : hors écosystème | Même classe que pdf — poids sous le seuil de pdf, même réserve de gouvernance |

\* Gain estimé = réduction du poids de chargement PAR DÉFAUT (SKILL.md) par déplacement R4 byte-identité vers references/ + résumés opérationnels inline — méthode validée sur gen-plan (−71,2 % mesurés).

## 3. Cartographie sèche du candidat n°1 écosystème — version-management (T3.4, SANS ÉCRITURE)

- **État** : 47 244 octets (46,1 Kio) / 632 lignes / 38 sections / **0 fichier references/** (tout inline) / 32 fences (délimiteurs R4 exploitables).
- **Blocs déplaçables identifiés (par taille)** : §1.3 Règles de structure des fichiers (5 822 o) · §3.4 Sortie dans le flux send_file (5 597 o) · §3.1 Points d'entrée d'édition (3 532 o) · §6 Aide-mémoire des opérations (3 035 o) · §8 Résorption structurelle Task 69 (2 264 o) · §1.2 Contrôle des chemins (2 204 o) · §5 Structure meta.json (1 630 o) = **~23,1 Kio déplaçables (50 %)**.
- **Faisabilité** : élevée — sections délimitées par headers + fences ; contrats à préserver : déclencheurs §A/read_when + description frontmatter (baseline golden master PRE, même mécanique que T1.1.0) ; **contrainte miroir** : la disparition récurrente (6ᵉ occurrence ce jour, auto-réparée INSTALLE-REPARÉ depuis le miroir) impose la sync hôte↔dépôt dans la même passe + re-certification integrity.
- **Gain projeté** : 46,1 → ~19-23 Kio (verdict OK/INTERMÉDIAIRE attendu) ; ≈ 9 000 #token économisés par chargement par défaut.
- **Sûreté (tests avant re-curation — directive complémentaire 1)** : protocole-test.py en phase PRE (baseline golden master → GO/NO-GO) puis POST (cohérent/optimisé/fonctionnel maintenu) — le skill re-curation (G4) sera l'exécutant canonique.

## 4. Preuves de test (règle d'or n°5)

- T3.1 : poids-chargement.py --json ×2 → **mesures byte-identiques** (cmp OK) — stats : 70/28/33/9/0.
- T3.2 : croisement disque échantillon 5 (pdf, iphone19, version-management, cahier-des-charges, gen-plan) → **5/5 PASS** (tailles disque == rapport, tolérance 0,15 Kio d'arrondi).
- T3.3 : dépendants KB extraits mécaniquement de skills/KNOWLEDGE.md (regex « Dépend de ») ; gouvernance par entrée KB (## <skill> v<x.y.z>) + registre ECO_SKILLS de check-ecosysteme-integrity.py.
- T3.4 : cartographie par headers ^#{2,3} — aucune écriture sur les fichiers cartographiés (test de sûreté).

## 5. Recommandation

Poursuivre l'application du chantier R1 dans l'ordre 1→7 (écosystème d'abord, périphérie avant noyau : version-management → iphone19 → iphone18 → [validation G4/G5] → skill-creator → web-reader → cahier-des-charges → iphone17). Les candidats plateforme (pdf, pptx) restent à la décision du propriétaire (gain réel mais hors gouvernance/pérennité écosystème). Chaque re-curation DOIT passer par le protocole « tests avant re-curation » (PRE GO/NO-GO → re-curation → POST) du skill re-curation créé en G4 — c'est l'objet même de ce skill.

**Décision couverte : D008 ✓ (présent livrable).**
