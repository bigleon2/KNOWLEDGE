# Plan d'actions — Task 8 : Création $facon des 3 skills suggérés (vue-upload v1.5.0 « hygiène des versions » · livraison-garantie v1.0.0 · qa-animation sur gif-animator-pro v2.1.0)

> **Session** : web-eb6c8580 (continuation 6) · 2026-10-31 · **Généré via** : gen-plan v3.28.2 (mode NULL — exécution classique)
> **Type** : 2 (évolution corpus écosystème — création de skills) · **Profil** : NORMAL · **G-RES (E1-RES)** : OK → SÉRIE justifiée (dépendance G1→G2 [livraison-garantie exige vue-upload >= 1.5.0], écritures partagées KB/worktree/ECO_SKILLS, hooks correct-work séquentiels §5.4)
> **Directive** ($FACON = « de façon cohérente, optimisée et fonctionnelle » — définition Task 7, worklog) : « crée $facon ces trois skills (cohérents, optimisés et fonctionnels) » — les trois skills = suggestions D018 du worklog Task 7 (issues de la discussion « Rasta Mouton » 55afc1b5, fondées sur douleurs prouvées) : ① vue-upload v1.5.0 « hygiène des versions », ② skill livraison-garantie (delivery-warden), ③ extension qa-animation à gif-animator-pro.

> **Verdict E8 : PASS** — answer-key-checker 16/16 ALL PASS (re-jeux pré-exécution ET post-écriture) ; check_plan_protocol P1-P5 ; answer key re-jouée mécaniquement 10/10 PASS en clôture (scripts/task8/re-jeu-answer-key.py — Horodatage vérifié : 2026-10-31T03:40:16+08:00). **PLAN-AFFICHE** (2026-10-31, session web-eb6c8580).
> **Horodatage plan : 2026-10-31T03:40:16+08:00** (anti-verdict-périmé, convention E7-DISP — re-validé à chaque écriture).

## Contexte d'entrée (vérifié en pré-vol E1-RES)

1. **État dépôt** : Task 7 clôturé 19/19 — push D010 EXÉCUTÉ (distant main **03cdb0f** ≡ worktree `.staging/KNOWLEDGE-publish` ≡ miroir hôte, ls-remote vérifié ; audit D011 5 zones VERT). Worktree propre @ 03cdb0f.
2. **Arbitres pré-vol** : `check-ecosysteme-integrity --check` **82/82 PASS** ; `check-triggers-replay` host **47/47 skills au score maximal** — dérivées voie-M-seule = 5 héritées Task 30 (agent-prompt-engineering, gen-plan, iphone19, refactor-guard, vue-upload), aucune nouvelle.
3. **Fondement des 3 skills (douleurs prouvées, discussion Rasta Mouton 2026-10-25)** : ① 3 fichiers au nom proche coexistaient dans download/ (V1 rejetée + version emoji + _v3 finale) → 2 MAUVAIS fichiers téléchargés — l'épinglage v1.4.0 corrige l'affichage, PAS la coexistence ; ② la QA du GIF fut visuelle à chaque itération (3 versions) alors que chaque critère de rejet était vérifiable mécaniquement ; ③ la séquence de livraison = 4 tours entièrement manuels, détection du mauvais fichier par chance (logs stderr voie froide).
4. **État des cibles (lus intégralement au pré-vol)** : vue-upload v1.4.0 — registre KB « ## vue-upload v1.4.0 », ECO_SKILLS 1.4.0, panel 752 L (featured/share/push/doctor, parseur tolérant) + serveur 374 L (UI DM-1, /files featured, journal) ; test mécanique v1.4.0 : `scripts/zip-tsi/test-vue-upload-v140.py` (16 checks, ne passe PAS par push → auto-archive v1.5.0 sans impact). gif-animator-pro : skill standalone v2 (frontmatter name/description/license SANS version, hors registre KB/ECO_SKILLS), moteur `gif_sprite_gif_pro.py` (Pillow — v11.3.0 disponible). livraison-garantie : inexistant (création from scratch).
5. **Décision de cadrage gif-animator-pro (D005)** : statu quo registre ASSUMÉ — le skill reste hors KB/ECO_SKILLS (D018 ne demande pas l'inscription ; cohérence préservée : frontmatter `version: 2.1.0` ajouté + provenance documentée dans son SKILL.md ; l'intégrité n'itère que les clés ECO_SKILLS et les entrées KB — aucun impact).
6. **Coût de livraison imposé par la douleur** : livraison-garantie dépend de vue-upload >= 1.5.0 (réutilisation des primitives R4 : import module panel — start_inprocess/lit_journal/lit_featured/sanitize_name — zéro duplication), d'où la série G1→G2.
7. **PAT** : non fourni ce tour (jamais persisté par convention anti-persistance — audits 5 zones VERT Task 7). Publication = commits locaux (worktree publication + hôte main état session), **push DIFFÉRÉ** — exécutable UNIQUEMENT si le PAT est re-fourni (règle d'or n°4 — jamais d'invention de jeton ; demande de re-provision en clôture).
8. **Sanity pré-vol** : arbitres E8 opérationnels (check_plan_protocol selftest ; answer-key-checker 16 checks) ; AUCUN appel API externe prévu (VLM non requis — zéro risque 429) ; tests mécaniques ×3 sous `scripts/task8/`.

## Answer Key (décisions — spec de session)

| ID | Décision (criterion) | Priorité | Statut |
|----|----------------------|----------|--------|
| D001 | Le plan couvre exactement les 3 skills D018 — vue-upload v1.5.0 « hygiène des versions », création livraison-garantie v1.0.0, extension qa-animation à gif-animator-pro v2.1.0 — et rien d'autre (pas d'inscription gif-animator-pro au registre, pas de 4e skill) | S1 | verified |
| D002 | G1 vue-upload v1.5.0 (MINOR addition pure R2) : détection de familles de versions (radical commun après purge des motifs _vN/V1/final/nouvelle/copie/(N)) ; sous-commande `versions` (listing familles multi-versions + suspects nom proche [1er token commun] + archive, JSON+texte) ; push archive AUTOMATIQUEMENT les versions exactes supersédées vers `<dir>/archive/` (drapeau --no-archive pour désactiver, no-op honnête si aucune, épinglé conservé signalé) ; panel expose `versions` + `versions_archivees` ; UI serveur : section repliée `<details>` « versions archivées » (affichage seul, sans lien — anti-mauvais-clic) | S1 | verified |
| D003 | G1 non-régression R2 : sans sous-commande = panel v1.1.0 inchangé ; sous-commandes featured/share/doctor inchangées ; codes retour 0/2/3/4/5/6 préservés ; marker featured + journal inchangés ; re-jeu test v1.4.0 (16 checks) PASS après édition | S1 | verified |
| D004 | G2 livraison-garantie v1.0.0 (création via skill-creator, dépendance YAML vue-upload >=1.5.0) : SKILL.md canonique (§0 SHARED, §A déclencheurs, §1-§3, read_when, evals) + `scripts/livraison_garantie.py` — orchestrateur boucle fermée : identifier le livrable (famille nom proche signalée) → épingler AVANT la fenêtre → démarrer le portail (primitives importées vue-upload) → surveiller le journal (position de départ = lignes pré-fenêtre) → arrêt mécanique à la 1re télécommande de la cible (CONFIRME, arrêt anticipé) ou à l'expiration (PARTIEL si mauvais fichier pris / AUCUN sinon) → guidance mécanique (re-ciblage/share) | S1 | verified |
| D005 | G3 gif-animator-pro v2.1.0 : `scripts/qa_animation.py` (Pillow) — contrôles déterministes des livrables animés : frames, boucle (loop infinie ou valeur), dimensions, poids, palette dominante (échantillon), durées/frame (uniformité), mouvement (bbox de différence) — référentiel JSON optionnel (frames/dimensions/boucle/poids_max/palette_dominante/durée/mouvement attendus) ; critères subjectifs DÉCLARÉS non vérifiés (honnêteté R3 — ex. « peau trop verte », « yeux au menton » : jamais simulés mécaniquement) ; verdict PASS/FAIL par contrôle, rc 0/1/6 | S1 | verified |
| D006 | Registre (G4) : ECO_SKILLS vue-upload=1.5.0 + livraison-garantie=1.0.0 (nouvelle clé) ; KB : entrée « ## vue-upload v1.5.0 » (description étendue + calibration) + entrée « ## livraison-garantie v1.0.0 » (création) + réciproque « Utilisé par » de gen-plan/vue-upload cohérente ; integrity --check ALL PASS ×2 arbres (compte KB = len(ECO_SKILLS) dynamique — KO-L003) | S1 | verified |
| D007 | RésCellage archive v2.3 ×2 arbres (corpus 9 + 6 piliers byte-identiques, extras homologues/ conservés) + projections hôte↔worktree (worktree = vérité de publication — Task 7) | S1 | verified |
| D008 | Non-régression voie M : re-jeu check-triggers-replay — verdict PASS, TOUS les skills au score maximal (livraison-garantie incluse si scannée), dérivées = liste héritée 5 Task 30 EXACTEMENT (aucune nouvelle) ; calibration veto/trigger_evals si une dérive apparaît | S1 | verified |
| D009 | Publication : commits locaux (worktree publication/p0-session-web-eb6c8580 — un par groupe G1/G2/G3/G4 ; hôte main = état session : worklog, plan, scripts/task8) ; distant main INCHANGÉ @ 03cdb0f (push DIFFÉRÉ — PAT non fourni) ; demande de re-provision en clôture | S1 | verified |
| D010 | Clôture : worklog Task 8 (pré-vol, plan, groupes, hooks, E15) + bilan E15 #token (estimé vs réel, causes, recommandation éventuelle) + statuts plan alignés + answer-key-checker re-vert | S2 | accompli |

```yaml
decisions:
  - id: "D001"
    criterion: "Les 3 artefacts existent en fin de cycle — SKILL.md vue-upload en 1.5.0, skills/livraison-garantie/ complet, skills/gif-animator-pro/scripts/qa_animation.py — et aucun 4e skill n'est créé"
    verification: "python3 -c \"import os,re; v=open('skills/vue-upload/SKILL.md',encoding='utf-8').read(); assert re.search(r'^version: 1\\.5\\.0', v, re.M); assert os.path.isfile('skills/livraison-garantie/SKILL.md'); assert os.path.isfile('skills/gif-animator-pro/scripts/qa_animation.py'); assert 'version: 2.1.0' in open('skills/gif-animator-pro/SKILL.md',encoding='utf-8').read(); assert not os.path.exists('skills/livraison-garantie/scripts/duplique_vue_upload.py')\""
    source: "directive « crée $facon ces trois skills » + suggestions D018 (worklog Task 7)"
    priority: "S1"
    status: "verified"
  - id: "D002"
    criterion: "vue-upload v1.5.0 : sous-commande versions opérationnelle, push archive les versions exactes supersédées vers download/archive/ (no-op honnête si aucune, --no-archive supporté), panel expose versions/versions_archivees, UI serveur porte la section repliée — prouvé par le test mécanique v1.5.0 (>= 14 checks PASS dont scénario 3-fichiers : push _v3 → V1 archivée, suspect nom proche signalé, _v3 seule en listing)"
    verification: "python3 scripts/task8/test-vue-upload-v150.py"
    source: "D018-1 (worklog Task 7) — douleur 3-fichiers-au-nom-proche du 2026-10-25 ; $FACON : MINOR sur le détenteur naturel R4"
    priority: "S1"
    status: "verified"
  - id: "D003"
    criterion: "Non-régression v1.4.0 : le test v1.4.0 existant passe INTÉGRALEMENT après les éditions v1.5.0 (16 checks), codes retour et protocoles featured/journal inchangés"
    verification: "python3 scripts/zip-tsi/test-vue-upload-v140.py"
    source: "R2 (addition pure) + précédent Task 7 G0 (régression Task 33 15/15 vérifiée au bump v1.2.0)"
    priority: "S1"
    status: "verified"
  - id: "D004"
    criterion: "livraison-garantie v1.0.0 : SKILL.md canonique (frontmatter version/dépendance vue-upload >=1.5.0, §0 SHARED, §A, §1-§3) + orchestrateur avec verdicts mécaniques CONFIRME (arrêt anticipé dès téléchargement de la cible), PARTIEL (mauvais fichier listé), AUCUN, rc 6 si livrable absent — prouvé par test mécanique (>= 10 checks PASS, portail réel in-process + /get simulés)"
    verification: "python3 scripts/task8/test-livraison-garantie.py"
    source: "D018-2 (worklog Task 7) — séquence de livraison 4 tours manuels du 2026-10-25 ; R4 : réutilisation primitives vue-upload, zéro duplication"
    priority: "S1"
    status: "verified"
  - id: "D005"
    criterion: "qa_animation.py : GIF conforme au référentiel → rc 0 verdict PASS ; référentiel violé (frames/dimensions/poids) → rc 1 avec contrôles FAIL nominatifs ; non-GIF → rc 6 ; les critères subjectifs sont LISTÉS comme non vérifiés (jamais simulés) — prouvé par test mécanique (>= 10 checks PASS dont un GIF réellement généré par gif_sprite_gif_pro.py)"
    verification: "python3 scripts/task8/test-qa-animation.py"
    source: "D018-3 (worklog Task 7) — QA visuelle à chaque itération du GIF mouton rasta (3 versions) ; honnêteté R3"
    priority: "S1"
    status: "verified"
  - id: "D006"
    criterion: "Registre cohérent : ECO_SKILLS vue-upload=1.5.0 et livraison-garantie=1.0.0 ; KB porte '## vue-upload v1.5.0' et '## livraison-garantie v1.0.0' (entrées versionnées) ; integrity --check rc=0 sur l'HÔTE et le WORKTREE"
    verification: "python3 -c \"import subprocess,sys; a=open('skills/vue-upload/SKILL.md',encoding='utf-8').read(); assert 'version: 1.5.0' in a; assert 'version: 1.0.0' in open('skills/livraison-garantie/SKILL.md',encoding='utf-8').read(); r1=subprocess.run(['python3','scripts/check-ecosysteme-integrity.py','--check'],capture_output=True,text=True); r2=subprocess.run(['python3','scripts/check-ecosysteme-integrity.py','--check'],cwd='.staging/KNOWLEDGE-publish',capture_output=True,text=True); assert r1.returncode==0, r1.stdout[-400:]; assert r2.returncode==0, r2.stdout[-400:]\""
    source: "Règle Zéro (registre KB source de vérité, cross-references bidirectionnelles) + KO-L003 (arbitres dynamiques — jamais la réalité figée)"
    priority: "S1"
    status: "verified"
  - id: "D007"
    criterion: "Projections ×2 arbres byte-identiques sur les fichiers édités + archive v2.3 rescellée ×2 (corpus + piliers) — integrity ×2 ALL PASS le prouve (check 1-2)"
    verification: "python3 -c \"import subprocess; r1=subprocess.run(['python3','scripts/check-ecosysteme-integrity.py','--check'],capture_output=True,text=True); r2=subprocess.run(['python3','scripts/check-ecosysteme-integrity.py','--check'],cwd='.staging/KNOWLEDGE-publish',capture_output=True,text=True); assert '82/82' in r1.stdout or '0 FAIL' in r1.stdout, r1.stdout[-300:]; assert r2.returncode==0, r2.stdout[-300:]\""
    source: "canon F5 v2.3 (Task 48) + pattern Task 7 (task7-g0g1-projections-rescellage.py — worktree = vérité de publication)"
    priority: "S1"
    status: "verified"
  - id: "D008"
    criterion: "Replay voie M post-édition : verdict PASS, tous les skills au score maximal, dérivées voie-M-seule = liste héritée EXACTE (agent-prompt-engineering, gen-plan, iphone19, refactor-guard, vue-upload) — aucune nouvelle dérive"
    verification: "python3 scripts/check-triggers-replay.py --quiet && python3 -c \"import json; r=json.load(open('scripts/triggers-replay-report.json')); assert r['verdict']=='PASS', r['verdict']; heritee={'agent-prompt-engineering','gen-plan','iphone19','refactor-guard','vue-upload'}; assert set(r['derive_voie_m_seule'])==heritee, r['derive_voie_m_seule']\""
    source: "D009 Task 7 (derive==[] corrigée en liste-identique-aux-5-héritées — statu quo documenté) + KO-L003"
    priority: "S1"
    status: "verified"
  - id: "D009"
    criterion: "Commits locaux propres (worktree publication : 4 commits de groupes ; hôte main : 1 commit état session) ; working trees propres ; ls-remote distant = 03cdb0f (push DIFFÉRÉ — PAT absent)"
    verification: "python3 -c \"import subprocess; w='.staging/KNOWLEDGE-publish'; assert subprocess.run(['git','-C',w,'status','--porcelain'],capture_output=True,text=True).stdout.strip()=='', 'worktree sale'; assert subprocess.run(['git','-C',w,'ls-remote','https://github.com/bigleon2/KNOWLEDGE.git','refs/heads/main'],capture_output=True,text=True).stdout.startswith('03cdb0f'), 'distant != 03cdb0f'\""
    source: "règle d'or n°4 (publication au GO seulement — PAT one-shot, jamais inventé) + fallback D019 Task 7 (pattern identique)"
    priority: "S1"
    status: "verified"
  - id: "D010"
    criterion: "Clôture documentée : worklog Task 8 (pré-vol, plan + verdict E8, groupes, hooks correct-work, arbitres, commits, E15 estimé-vs-réel) + statuts answer key alignés (tous verified/accompli) + answer-key-checker re-vert"
    verification: "python3 scripts/answer-key-checker.py 2>&1 | tail -2 && grep -c 'status: \"verified\"\\|status: \"accompli\"' download/plan-task8-trois-skills-facon.md"
    source: "règle d'or n°5 (jamais pré-écrire les résultats) + bilan E15 (§1.14 gen-plan)"
    priority: "S2"
    status: "accompli"
```

## Groupes d'exécution (série justifiée — dépendance G1→G2, écritures partagées, hooks séquentiels)

| Groupe | Contenu | Livrables | Hook |
|--------|---------|-----------|------|
| **G1** | vue-upload **v1.5.0** « hygiène des versions » | panel (detect_versions, cmd_versions, push auto-archive, VERSION/USAGE) · serveur (_listing versions_archivees + `<details>` UI, marqueur 1.5.0) · SKILL.md (frontmatter/description/§A/§1.2/§2.2/§2.3) · evals VU-7/VU-8 · test `scripts/task8/test-vue-upload-v150.py` (>=14 checks) | correct-work(G1) CIBLE |
| **G2** | **livraison-garantie v1.0.0** (création) | SKILL.md canonique · scripts/livraison_garantie.py (boucle fermée, primitives importées vue-upload) · evals + trigger_evals · test `scripts/task8/test-livraison-garantie.py` (>=10 checks) | correct-work(G2) CIBLE |
| **G3** | gif-animator-pro **v2.1.0** + **qa-animation** | scripts/qa_animation.py · SKILL.md (frontmatter version + section qa-animation + déclencheurs) · test `scripts/task8/test-qa-animation.py` (>=10 checks, GIF généré par le moteur réel) | correct-work(G3) CIBLE |
| **G4** | Projections + registre + certification | ECO_SKILLS (1.5.0 + livraison-garantie 1.0.0) · KB (bump vue-upload + entrée livraison-garantie + réciproques) · projections ×2 arbres + rescellage v2.3 ×2 · arbitres (integrity ×2, replay, verify-correct-work, check-tool-routing, verify-cross si requis) · commits publication (G1-G4) | correct-work(G4) CIBLE |
| **G5** | Clôture | commit hôte main (worklog, plan aligné, scripts/task8) · E15 · demande re-provision PAT | — |

## Estimation #token (grille v3.28.2)

- **Estimé** : ~49 k (G1 14 k · G2 12 k · G3 9 k · G4 9 k · G5 5 k) — plage 42-58 k.
- **Facteurs** : 5 groupes en série (dépendance G1→G2) ; édition multi-fichiers ×3 skills avec tests mécaniques ×3 (boucle d'itération incluse) ; arbitres ×5 en G4 ; AUCUN appel API externe (pas de contingence réseau) ; cascade registre standard (KO-L004 : ECO_SKILLS + KB ×2 arbres).
- **Contingences** : replay en dérive sur description éditée → calibration trigger_evals/vetos (prévue D008, +3 k) ; échec de boucle serveur en test (port occupé) → ports libres dynamiques (déjà le pattern v1.4.0).

## Règles de session (rappel)

- Règle d'or n°5 : statuts answer key « à faire » au départ — JAMAIS pré-écrits ; alignés sur preuve à la clôture.
- Règle d'or n°4 : publication au GO seulement — PAT absent → push DIFFÉRÉ, demande de re-provision.
- R2 : additions pures aux comportements existants (panel sans sous-commande inchangé, codes retour préservés).
- R4 : zéro duplication — livraison-garantie RÉUTILISE les primitives vue-upload (import module) ; serveur liste archive/ (listing simple, pas la logique familles).
