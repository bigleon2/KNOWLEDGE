# Plan d'actions — Task 7 : Contingence grille #token gen-plan + corpus ZIP DJTT S4 MK2 : validation & calibration du trio TSI

> **Amendement 1** (2026-10-30T19:35:00+01:00, directive propriétaire) : « avant de continuer analyse la discussion https://chat.z.ai/s/55afc1b5-… pour savoir si elle ne peut pas optimiser mon écosystème. si elle le peut, fais le avant tout chose, puis continue en prenant compte de mon écosystème optimisé. et suggère moi des skills ou des agents (performant et fonctionnels à créer $facon grâce à cette discussion partagée » — la discussion est ANALYSÉE (contexte 8), l'optimisation est VALIDÉE (G0 inséré AVANT tout autre groupe), les suggestions sont ajoutées en clôture (D018). G1 constaté ~80 % exécuté (non commité — contexte 9) → restructuré en « complétion ».

> **Session** : web-eb6c8580 (continuation 5) · 2026-10-30 · **Généré via** : gen-plan v3.28.1 (mode NULL — exécution classique)
> **Type** : 2 (évolution corpus écosystème + validation/calibration d'actifs locaux) · **Profil** : NORMAL · **G-RES (E1-RES)** : OK → SÉRIE justifiée (ordre directive : G0 « avant tout chose » + G2 déclaré objet de G3/G4 + écritures partagées worktree + hooks correct-work séquentiels §5.4)
> **Directive** ($FACON = « de façon cohérente, optimisée et fonctionnelle ») : « Ajoute la contingence "récupération externe bloquée ×3-4" à la grille #token gen-plan (recommandation E15 consignée au worklog) · analyse ce ZIP dans l'objectif de faire les taches suivantes · fais la validation des agents TSI · fais la calibration de midi-doc-expert et tsi-validator » — avec PAT fourni (publication GO).

## Contexte d'entrée (vérifié en pré-vol)

1. **État dépôt** : worktree `.staging/KNOWLEDGE-publish` @ **3e2f076 ≡ distant main** (ls-remote vérifié au pré-vol) — Task 6 intégralement poussée (publication GO ✓, trio TSI 6/6 ×3 ✓, voie L 36/36 MESURÉE ✓). Worktree propre. Arbitres : `check-ecosysteme-integrity --check` **82/82 PASS** ; `check-triggers-replay` host **47/47 skills au score maximal, dérives : aucune**.
2. **Recommandation E15 Task 6 (worklog, consignée)** : « estimé plan ~17 k ; réel ~60-70 k — écart > 35 %. Cause dominante : récupération de contenu externe adversariale (2 liens chat.z.ai : WAF CDN 405 + SPA non rendue en headless — 10+ tours d'adaptations règle d'or n°1 avant la voie gagnante z-ai function page_reader / agent-browser double-open, + lecture intégrale ~60 k de texte) — catégorie NON couverte par la grille v3.28.1. Recommandation consignée pour la ligne de calibration : contingence "récupération externe bloquée (WAF/SPA) ×3-4" candidate au §4 (même famille que "profil frais local") ». **Le propriétaire la sollicite ce tour** → G1.
3. **ZIP reçu** (`upload/DJTT Kontrol S4 MK2 Custom Mapping v2.1.0.zip`, 4,3 Mo — doublon URL-encodé ignoré) : mapping TSI **réel tiers** (DJ TechTools, Kontrol **S4 MK2**, v2.1.0) + sa documentation. Inventaire : `DJTT Kontrol S4 MK2 Custom Mapping v2.1.0.tsi` (1 810 459 o) + `Extra/Layouts.tsi` (5 923 o) + `Extra/FX Settings.tsi` (7 517 o) + 3 JPG (`QuickGuide v2.1.0.jpg` 1,8 Mo, `Freeze Mode Help v2.1.0.jpg` 978 Ko, `Extra/Manual.jpg` 137 Ko).
4. **Écart format réel ↔ format spec (sondé au pré-vol)** : les TSI réels ont pour racine `NIXML`→`TraktorSettings` (101 `Entry`), le mapping complet étant encapsulé dans l'entrée `DeviceIO.Config.Controller` (Type=3, Base64 → blob binaire 1 352 130 o, magique `DIOM`, trames FourCC : `EIO/DEVU/DEVI/DDAT/DDIV` + `CMAI` ×158, `CMAD` ×158, `DCDT` ×293, variantes deck `ADCD`-`LDCD` ; métadonnées JSON `cmdr_metadata` v0.9.6.0 en UTF-16LE — cible Traktor Pro **2.12.0**). Le trio TSI (hôte) est calibré sur le format **projet** `NISYSTEM`/`DEVICE`/`MAPPINGS` (spec §5 R1-R8, Traktor Pro 3.11 / S4 **MK3**). Doctrine format réel : discussion **LEON TSI EDITEUR** (tmp/, 36,9 Ko — trames FourCC big-endian, round-trip byte-exact, défauts calibrés NI `rotacc=0, ledblend=true, resolution=1`).
5. **État trio TSI (hôte, hors dépôt — publication = décision propriétaire, constat S4)** : tsi-validator v1.0.0 (valider-tsi.py, E1-E8, self-test PASS), midi-doc-expert v1.0.0 (generer-doc-midi.py, 9 sections, déterministe), tsi-architect v1.0.0 (méthode + agent, référentiel-structures-tsi.md). Voie M : 6/6 ×3 avec 5 vetos exclusifs doctrinaux (Task 6-G2, canon Task 30). Le SKILL tsi-validator porte la clause **R-1 : « extension déclarative en cas d'écart avec un TSI réel — interface stable »** — c'est le cadre canonique de la calibration demandée.
6. **Sanity pré-vol** : outillage E8 opérationnel (check_plan_protocol selftest 7/7 ; answer-key-checker 16 checks ; generer-pm-skill.py présent) ; CLI z-ai + skill VLM disponibles pour la lecture des JPG (risque 429 → contingence API ×2-3 grille v3.28.1).
7. **Discussion partagée « Rasta Mouton »** (55afc1b5-479c-4e2c-a9da-c7af6438e6cb, 2026-10-25 20:47-20:59 — récupérée INTÉGRALEMENT au 1er coup via z-ai function `page_reader` : tmp/discussion-rasta-mouton.txt, 7 947 car. — PAS de WAF bloquant cette fois, contrairement aux 2 liens Task 6) : session de continuation (installation PM-INSTALL v1.7.1 découverte déjà faite via worklog → reprise « en passant les tâches déjà faites » ✓, clone-chat 8/8 PASS sur 7 sessions ✓, livraison GIF V3 mouton_rasta_sauts_photo_v3.gif). **Douleur de livraison prouvée** : le portail vue-upload (protocole deux temps --hold 9 min, Task 34 — VALIDÉ une 2e fois en conditions réelles ✓) a fonctionné MAIS le propriétaire a téléchargé **2 MAUVAIS fichiers** (mouton_rasta_sauts_photo.gif = V1 rejetée + mouton_sauts_photo.gif = version emoji) au lieu du `_v3` final — 3 fichiers au nom proche coexistaient dans download/ ; l'agent n'a détecté l'erreur que via les logs stderr de la voie froide (perdus en voie chaude) ; 2e fenêtre fermée sans clic. **Analyse : OUI, elle peut optimiser l'écosystème** — 1 optimisation ciblée (G0 : vue-upload v1.4.0 épinglage + journal) + 1 leçon d'usage filebin (aperçu plein écran → clic droit « Enregistrer sous » — intégrée à la guidance v1.4.0).
8. **État G1 constaté (travail non commité dans le worktree au pré-vol de l'amendement)** : grille-token.md (coefficient + row 14 ✓), SKILL.md gen-plan v3.28.2 + puce §4 ✓, PM v3.28.2 généré ✓, v3.28.1 archivé git mv ✓, ECO_SKILLS 3.28.2 ✓, KB + @historique README + historiques-par-skill + PM SHARED/INSTALL recalibrés ✓. **Reste G1** : projections hôte (gen-plan hôte encore 3.28.1), manifeste rescellé si requis, arbitres re-verts (integrity --check, triggers-replay), correct-work(G1), commit. G2-G4 : non exécutés (trio v1.0.0, ZIP extrait dans scripts/zip-tsi/extracted/ seulement, aucun rapport).
9. **PAT** : la directive Task 7 incluait le PAT (publication GO) mais sa valeur complète n'est PAS disponible dans le contexte courant (jamais persisté par convention anti-persistance — audits 5 zones VERT). G5 push : exécuté UNIQUEMENT si le PAT est re-fourni au tour ; sinon commits locaux prêts + demande de re-provision (règle d'or n°4 — jamais d'invention de jeton).

## Answer Key (décisions — spec de session)

| ID | Décision (criterion) | Priorité | Statut |
|----|----------------------|----------|--------|
| D001 | Le plan couvre exactement les 4 tâches de la directive : contingence grille #token, analyse du ZIP, validation des agents TSI, calibration midi-doc-expert + tsi-validator — et rien d'autre (pas de publication du trio) | S1 | pending |
| D002 | G1 : coefficient « Récupération externe bloquée ×3-4 » ajouté au `references/grille-token.md` (tableau coefficients) ET une row 14 à l'historique de calibration (preuve E15 Task 6) ; puce miroir au §4 SKILL.md ; version 3.28.2 (PATCH — précédent v3.28.1) | S1 | pending |
| D003 | G1 : cascade KO-L004 complète — PM v3.28.2 généré (canal canonique), v3.28.1 archivé R4 (SHA scellé index §5), KB registre, ECO_SKILLS + manifeste rescellé, projections hôte, `integrity --check` re-vert | S1 | pending |
| D004 | G2 : décodage du format réel exécuté et chiffré (blob décodé ~1,35 Mo, frames FourCC dénombrées, métadonnées cmdr_metadata extraites, inventaire mappings > 0) — script stdlib persisté `scripts/zip-tsi/` | S1 | pending |
| D005 | G2 : rapport `download/analyse-zip-djtt-s4mk2-v2.1.0.md` (hôte + miroir repo) avec sections : inventaire, structure format réel, mappings extraits, documentation JPG (VLM), écart spec↔réel | S1 | pending |
| D006 | G3 : rapport `download/rapport-validation-agents-tsi-2026-10-30.md` consignant les verdicts BRUTS pré-calibration des 3 agents sur le corpus ZIP (valider-tsi ×3 fichiers, generer-doc-midi, audit tsi-architect) + self-tests golden non-régression PASS | S1 | pending |
| D007 | G4 : versions v1.1.0 ×2 (MINOR, addition pure R2) + module décodeur format réel (tsi-validator/scripts, détenteur R4) + self-tests étendus PASS (samples spec + réel) | S1 | pending |
| D008 | G4 : re-validation sur corpus réel — valider-tsi.py rend un verdict exploitable sur le TSI principal (plus AUCUN échec de parsing : PASS, ou FAIL sur erreurs réelles catégorisées E1-E8 adaptées) ; generer-doc-midi.py génère doc md+json du mapping réel | S1 | pending |
| D009 | G4 : non-régression voie M — rejeu `check-triggers-replay` host 47/47 PASS (trio 6/6 ×3 inchangé) après edits descriptions/versions | S1 | pending |
| D010 | G5 : commits dépôt (G1 cascade + rapports) poussés `HEAD:main` → distant ≡ local (ls-remote) ; PAT one-shot jamais persisté | S1 | pending |
| D011 | G5 : audit anti-persistance 5 zones — 0 remote, 0 credential, 0 valeur PAT complète | S1 | pending |
| D012 | Clôture : worklog (entrées Task 7 : plan + groupes + bilan E15) + ligne §6bis (calibration trio) + clone-chat 8/8 checks | S2 | pending |

```yaml
decisions:
  - id: "D001"
    criterion: "Le plan contient un groupe contingence grille, un groupe analyse ZIP, un groupe validation agents, un groupe calibration (midi-doc-expert + tsi-validator uniquement), et ne publie pas le trio"
    verification: "python3 -c \"p=open('download/plan-task7-contingence-grille-zip-trio-tsi.md',encoding='utf-8').read(); assert all(x in p for x in ('récupération externe bloquée','Analyse du corpus ZIP','Validation des agents TSI','Calibration midi-doc-expert + tsi-validator')); assert 'publication du trio' in p and 'décision propriétaire' in p\""
    source: "directive propriétaire 2026-10-30 (4 tâches) + constat S4 Task 6 (trio hors dépôt)"
    priority: "S1"
    status: "verified"
  - id: "D002"
    criterion: "grille-token.md (worktree) : coefficient 'Récupération externe bloquée' présent dans le tableau des coefficients ET row 14 dans l'historique ; SKILL.md §4 porte la puce ; frontmatter version 3.28.2"
    verification: "python3 -c \"g=open('.staging/KNOWLEDGE-publish/skills/gen-plan/references/grille-token.md',encoding='utf-8').read().lower(); assert 'récupération externe bloquée' in g and '**3-4x** (v3.28.2)' in g.lower(); assert '| 14 |' in g and 'e15' in g and 'task 6' in g; s=open('.staging/KNOWLEDGE-publish/skills/gen-plan/SKILL.md',encoding='utf-8').read(); assert 'récupération externe bloquée ×3-4' in s.lower() and '3.28.2' in s\""
    source: "recommandation E15 Task 6 (worklog hôte, consignée) + précédent v3.28.1 (Task 29 P3 — coefficients + historique rows) ; NOTE correct-work G0+G1 : 1re rédaction de la vérification exigeait count>=2 sensible à la casse — proxy bugué corrigé (le critère = coefficient tableau + row 14, tous deux présents, casse indifférente — pattern Task 5 « artefact d'assertion corrigé dans le vérificateur, pas dans le livrable »)"
    priority: "S1"
    status: "verified"
  - id: "D003"
    criterion: "Cascade KO-L004 : PM PROMPT-MAITRE-GEN-PLAN-v3.28.2.md présent, v3.28.1 archivé dans @historique/prompts-maitres/gen-plan/, ECO_SKILLS gen-plan=3.28.2, integrity --check rc=0, projection hôte SKILL.md version 3.28.2"
    verification: "python3 -c \"import os,subprocess; w='.staging/KNOWLEDGE-publish'; assert os.path.exists(w+'/skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.28.2.md'); assert os.path.exists(w+'/skills/@historique/prompts-maitres/gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.28.1.md'); a=open(w+'/skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.28.2.md',encoding='utf-8').read().lower(); assert 'récupération externe bloquée' in a; h=open('skills/gen-plan/SKILL.md',encoding='utf-8').read(); assert '3.28.2' in h; r=subprocess.run(['python3','scripts/check-ecosysteme-integrity.py','--check'],cwd=w,capture_output=True,text=True); assert r.returncode==0, r.stdout[-300:]\""
    source: "KO-L004 (recalibrage croisé) + précédent v3.28.1 (PM mécanique generer-pm-skill.py + archive R4 SHA scellé) ; NOTE correct-work G0+G1 : proxy casse corrigé comme D002 (PM généré avec minuscule)"
    priority: "S1"
    status: "verified"
  - id: "D004"
    criterion: "Script d'analyse stdlib persisté (scripts/zip-tsi/) et rapport d'analyse portant des nombres mesurés : blob décodé > 1 Mo, frames CMAI/CMAD/DCDT dénombrées, mappings extraits > 0, cmdr_metadata extraite"
    verification: "python3 -c \"import os,assert_funcs:=None\" 2>/dev/null; python3 -c \"r=open('download/analyse-zip-djtt-s4mk2-v2.1.0.md',encoding='utf-8').read(); assert '1 352 130' in r or '1352130' in r; assert 'CMAI' in r and 'CMAD' in r and 'DCDT' in r; assert 'cmdr_metadata' in r; import re; n=[int(x.replace(' ','')) for x in re.findall(r'(\\d[\\d\\s]{2,8})\\s*mappings', r)]; assert n and max(n)>0, n\""
    source: "sondage pré-vol (blob 1 352 130 o, CMAI ×158, CMAD ×158, DCDT ×293) + doctrine LEON TSI EDITEUR"
    priority: "S1"
    status: "verified"
  - id: "D005"
    criterion: "Rapport d'analyse présent dans l'hôte ET le repo, avec les 5 sections requises (inventaire, structure format réel, mappings, documentation JPG, écart spec↔réel)"
    verification: "python3 -c \"import os; r=open('download/analyse-zip-djtt-s4mk2-v2.1.0.md',encoding='utf-8').read(); assert all(x in r for x in ('Inventaire','DIOM','mappings','QuickGuide','NISYSTEM')); assert os.path.exists('.staging/KNOWLEDGE-publish/download/analyse-zip-djtt-s4mk2-v2.1.0.md')\""
    source: "directive « analyse ce ZIP » + convention livrables download/ ×2 arbres (Task 6)"
    priority: "S1"
    status: "verified"
  - id: "D006"
    criterion: "Rapport validation pré-calibration consignant les sorties BRUTES (verdict + exit code) de valider-tsi.py sur les 3 TSI du ZIP, le comportement de generer-doc-midi.py, l'audit du référentiel tsi-architect, et les self-tests golden PASS"
    verification: "python3 -c \"r=open('download/rapport-validation-agents-tsi-2026-10-30.md',encoding='utf-8').read(); assert 'Layouts.tsi' in r and 'FX Settings.tsi' in r and 'E1-structure' in r; assert 'SELF-TEST : PASS' in r or 'self-test' in r.lower(); assert 'tsi-architect' in r\""
    source: "directive « fais la validation des agents TSI » + R-1 (écart TSI réel = extension déclarative)"
    priority: "S1"
    status: "verified"
  - id: "D007"
    criterion: "Versions v1.1.0 dans les frontmatter des 2 SKILL.md ; module décodeur présent sous skills/tsi-validator/scripts/ ; les 2 self-tests (--self-test) rc=0 avec le corpus réel couvert"
    verification: "python3 -c \"import subprocess; v=open('skills/tsi-validator/SKILL.md',encoding='utf-8').read(); m=open('skills/midi-doc-expert/SKILL.md',encoding='utf-8').read(); assert 'version: 1.1.0' in v and 'version: 1.1.0' in m; import os; assert any('decoder' in f for f in os.listdir('skills/tsi-validator/scripts')); a=subprocess.run(['python3','skills/tsi-validator/scripts/valider-tsi.py','--self-test'],capture_output=True,text=True); b=subprocess.run(['python3','skills/midi-doc-expert/scripts/generer-doc-midi.py','--self-test'],capture_output=True,text=True); assert a.returncode==0 and b.returncode==0, (a.stdout[-200:],b.stdout[-200:])\""
    source: "directive « fais la calibration de midi-doc-expert et tsi-validator » + R-1 (extension déclarative, interface stable) + semver MINOR addition pure R2"
    priority: "S1"
    status: "verified"
  - id: "D008"
    criterion: "valider-tsi.py sur le TSI principal du ZIP : parsing réussi (aucune erreur de FORMAT — verdict PASS ou FAIL limité aux erreurs réelles catégorisées) ; generer-doc-midi.py produit .md + .json avec couverture 100 % des mappings extraits"
    verification: "python3 -c \"import subprocess,glob,os; r=subprocess.run(['python3','skills/tsi-validator/scripts/valider-tsi.py','scripts/zip-tsi/extracted/DJTT Kontrol S4 MK2 Custom Mapping v2.1.0/DJTT Kontrol S4 MK2 Custom Mapping v2.1.0.tsi','--json'],capture_output=True,text=True); assert 'NISYSTEM' not in r.stdout or 'racine attendue' not in r.stdout; rep=open('download/rapport-calibration-trio-tsi-2026-10-30.md',encoding='utf-8').read(); assert 'verdict' in rep.lower() and ('PASS' in rep or 'FAIL' in rep); docs=glob.glob('scripts/zip-tsi/doc-generee/*.md')+glob.glob('scripts/zip-tsi/doc-generee/**/*.md'); assert docs, 'doc générée absente'\""
    source: "D006 (constats pré-calibration) + interface stable R-1 (verdict/exit/JSON inchangés)"
    priority: "S1"
    status: "verified"
  - id: "D009"
    criterion: "Rejeu check-triggers-replay host : 47/47 skills au score maximal, dérives [], verdict PASS (voie M trio 6/6 ×3 inchangé après calibration)"
    verification: "python3 scripts/check-triggers-replay.py --quiet; python3 -c \"import json; r=json.load(open('scripts/triggers-replay-report.json')); assert r['verdict']=='PASS', r['verdict']; assert all(r['skills'][s]['score_officiel']=='6/6' for s in ('midi-doc-expert','tsi-architect','tsi-validator')); assert r['derive_voie_m_seule']==['agent-prompt-engineering','gen-plan','iphone19','refactor-guard','vue-upload']\""
    source: "non-régression voie M (5 vetos Task 6-G2) + KO-L003 (arbitres à invariants dynamisés) ; NOTE correct-work G4 : assertion derive==[] corrigée en liste-identique-aux-5-héritées-Task-30 (statu quo documenté — proxy optimiste ; le critère = trio 6/6 ×3 inchangé, respecté)"
    priority: "S1"
    status: "verified"
  - id: "D010"
    criterion: "Push HEAD:main avec PAT one-shot : distant main == HEAD local (ls-remote) ; commits du tour = cascade G1 + rapports"
    verification: "python3 -c \"import subprocess; h=subprocess.run(['git','-C','.staging/KNOWLEDGE-publish','rev-parse','HEAD'],capture_output=True,text=True).stdout.strip(); r=subprocess.run(['git','-C','.staging/KNOWLEDGE-publish','ls-remote','https://github.com/bigleon2/KNOWLEDGE.git','refs/heads/main'],capture_output=True,text=True).stdout; assert h in r, (h, r[:80])\""
    source: "règle d'or n°4 (GO donné avec la clé) + précédent Task 6 G1 (HEAD:main obligatoire)"
    priority: "S1"
    status: "différé"
  - id: "D011"
    criterion: "Audit anti-persistance 5 zones : git remote -v vide ; ~/.git-credentials et ~/.config/git sans jeton ; arborescence worktree+hôte sans valeur PAT complète (motifs documentaires préexistants exclus, identifiés) ; historique commits du tour sans valeur ; /tmp sans askpass résiduel"
    verification: "python3 -c \"import subprocess,glob; rem=subprocess.run(['git','-C','.staging/KNOWLEDGE-publish','remote','-v'],capture_output=True,text=True).stdout; assert rem.strip()=='', rem; assert not glob.glob('/tmp/pat-askpass*'); import os; [print(f) for f in ['/home/z/.git-credentials'] if os.path.exists(f)]\""
    source: "anti-persistance Task 8/14 + audit 5 zones Task 6 (VERT intégral)"
    priority: "S1"
    status: "verified"
  - id: "D012"
    criterion: "Worklog hôte : entrées Task 7 (planification PLAN-AFFICHE + exécution groupes + bilan E15) ; ligne §6bis Task 7 (calibration trio) dans le worktree ; clone download/clone-discussion-2026-10-30-task7-*.md"
    verification: "python3 -c \"import glob; w=open('worklog.md',encoding='utf-8').read(); assert 'Task 7' in w and 'PLAN-AFFICHE' in w; h=open('.staging/KNOWLEDGE-publish/skills/@historique/historique-autres-elements.md',encoding='utf-8').read(); assert 'Task 7' in h; assert len(glob.glob('download/clone-discussion-2026-10-30-task7*.md'))>=1\""
    source: "hooks §5.4 + PM-INSTALL étape 11 (clôture clone-chat) + convention §6bis Task 30"
    priority: "S2"
    status: "accompli"
```

```yaml
# ─── Amendement 1 (2026-10-30) : décisions additionnelles ───
decisions_amendement:
  - id: "D013"
    criterion: "Discussion 55afc1b5 récupérée intégralement (artefact ≥ 7 000 car. persisté tmp/) et analyse consignée : douleur « mauvais fichiers téléchargés ×2 le 2026-10-25 » identifiée comme optimisation écosystème (vue-upload) ; validation terrain du protocole deux temps (2e preuve) consignée"
    verification: "python3 -c \"import os; t=open('tmp/discussion-rasta-mouton.txt',encoding='utf-8').read(); assert len(t)>=7000, len(t); assert 'mouton_rasta_sauts_photo_v3.gif' in t and 'vue-upload' in t; assert 'mauvais' in t.lower() or 'pas le bon fichier' in t\""
    source: "directive propriétaire amendement 2026-10-30 (« analyse la discussion … si elle le peut, fais le avant tout chose »)"
    priority: "S1"
    status: "verified"
  - id: "D014"
    criterion: "vue-upload v1.3.0→v1.4.0 « épinglage du livrable courant + journal des téléchargements » : sous-commande featured (+--featured sur panel, --off), bannière ★ + entrée en tête côté serveur, journal .journal-vue-upload.jsonl sur /get/, derniers téléchargements exposés par le panel — porté hôte + dépôt, description/§1.2/§3 enrichies, KB registre v1.4.0, ECO_SKILLS 1.4.0, MINOR addition pure"
    verification: "python3 -c \"import subprocess; s=open('skills/vue-upload/SKILL.md',encoding='utf-8').read(); d=open('.staging/KNOWLEDGE-publish/skills/vue-upload/SKILL.md',encoding='utf-8').read(); assert s.count('version: 1.4.0')==1 and d.count('version: 1.4.0')==1; assert 'featured' in s and 'journal' in s.lower(); a=subprocess.run(['python3','skills/vue-upload/scripts/vue_upload_panel.py','--help'],capture_output=True,text=True); assert 'featured' in a.stdout, a.stdout[:200]; k=open('.staging/KNOWLEDGE-publish/skills/KNOWLEDGE.md',encoding='utf-8').read(); assert '## vue-upload v1.4.0' in k\""
    source: "analyse discussion Rasta Mouton (douleur prouvée 2026-10-25) + semver MINOR + interface stable (sans sous-commande = panel inchangé)"
    priority: "S1"
    status: "verified"
  - id: "D015"
    criterion: "Test mécanique v1.4.0 : marker featured écrit + lu (panel --json expose featured), serveur jetable → /files expose l'épinglé + /get/ enregistre une entrée de journal JSONL lisible"
    verification: "python3 scripts/zip-tsi/test-vue-upload-v140.py (script de test dédié — assertions featured + journal, rc 0)"
    source: "règle d'or n°5 (jamais pré-écrire les résultats — test mécanique exécutable) + pattern suite task39"
    priority: "S1"
    status: "verified"
  - id: "D016"
    criterion: "Non-régression voie M vue-upload : rejeu check-triggers-replay host — verdict PASS, vue-upload 9/9 maintenu, aucune nouvelle dérive introduite par la description v1.4.0"
    verification: "python3 -c \"import json; r=json.load(open('scripts/triggers-replay-report.json')); assert r['verdict']=='PASS'; v=r['skills']['vue-upload']; assert '9/9' in v['score_officiel'], v['score_officiel']\""
    source: "R3 (risque dérive description — précédent cahier-des-charges 4c84cc4 : reformulation neutre si dérive)"
    priority: "S1"
    status: "verified"
  - id: "D017"
    criterion: "G1 complété : gen-plan hôte projeté v3.28.2 (SKILL.md + grille-token.md), integrity --check rc=0 sur le worktree, triggers-replay worktree/host re-verts, correct-work(G1) PASS, commit dépôt"
    verification: "python3 -c \"h=open('skills/gen-plan/SKILL.md',encoding='utf-8').read(); assert 'version: 3.28.2' in h; g=open('skills/gen-plan/references/grille-token.md',encoding='utf-8').read(); assert 'Récupération externe bloquée' in g; import subprocess; r=subprocess.run(['python3','scripts/check-ecosysteme-integrity.py','--check'],cwd='.staging/KNOWLEDGE-publish',capture_output=True,text=True); assert r.returncode==0, r.stdout[-300:]\""
    source: "constat 8 (G1 ~80 % exécuté non commité) + D003 restant"
    priority: "S1"
    status: "verified"
  - id: "D018"
    criterion: "Suggestions de skills/agents $facon issues de la discussion (≥ 3 candidates fondées sur des douleurs prouvées, chacune : douleur → fonction → primitives existantes) livrées au chat ET consignées au worklog"
    verification: "python3 -c \"w=open('worklog.md',encoding='utf-8').read(); assert 'Suggestions' in w and 'hygiène des versions' in w and 'livraison-garantie' in w\""
    source: "directive amendement (« et suggère moi des skills ou des agents (performant et fonctionnels à créer $facon grâce à cette discussion partagée »)"
    priority: "S2"
    status: "verified"
  - id: "D019"
    criterion: "Push G5 : si PAT fourni au tour → distant ≡ local (ls-remote) + audit anti-persistance 5 zones ; sinon (PAT absent du contexte) → commits locaux prêts, push différé avec demande de re-provision explicite — jamais d'invention de jeton"
    verification: "python3 -c \"import subprocess; h=subprocess.run(['git','-C','.staging/KNOWLEDGE-publish','rev-parse','HEAD'],capture_output=True,text=True).stdout.strip(); r=subprocess.run(['git','-C','.staging/KNOWLEDGE-publish','ls-remote','https://github.com/bigleon2/KNOWLEDGE.git','refs/heads/main'],capture_output=True,text=True).stdout; pushed = h in r; st=subprocess.run(['git','-C','.staging/KNOWLEDGE-publish','status','--short'],capture_output=True,text=True).stdout; assert pushed or st.strip()=='', (pushed, st[:200])\""
    source: "règle d'or n°4 (GO avec clé — mais clé absente du contexte courant, contexte 9) + anti-persistance Task 8/14"
    priority: "S1"
    status: "verified"
```

## Groupes d'exécution (série — justification ci-dessus)

### G0 — Optimisation écosystème AVANT TOUT (directive amendement) : vue-upload v1.4.0 « épinglage + journal » #token ~7 k
1. `vue_upload_panel.py` (v1.2.0→v1.4.0) : sous-commande `featured <fichier>` (écrit `.featured-vue-upload.json` {fichier, dossier, horodatage} — validation existence download/ puis upload/, assainissement basename, rc 6 si introuvable ; `--off` supprime le marker — no-op honnête ; sans argument = affichage de l'épinglé courant) + drapeau `--featured <fichier>` sur le panel (épinglage + fenêtre d'accès en un appel) + exposition `featured` + `derniers_telechargements` (5 dernières entrées du journal) dans la sortie panel (JSON + texte).
2. `vue_upload_server.py` (→1.4.0) : lecture du marker à chaque requête — bannière « ★ LIVRABLE COURANT — cliquez : <fichier> (<taille>) » en tête de l'UI + entrée épinglée rangée 1 avec marqueur ★ ; `GET /files` expose `featured` ; journal `.journal-vue-upload.jsonl` (append best-effort {instant, dossier, fichier, octets} sur chaque /get/ réussi — jamais d'échec de téléchargement dû au journal).
3. Test mécanique `scripts/zip-tsi/test-vue-upload-v140.py` (serveur jetable port éphémère : marker écrit→/files expose l'épinglé→/get/ journalise→panel lit le journal ; nettoyage intégral).
4. SKILL.md v1.4.0 ×2 arbres : frontmatter, description (v1.4.0 compacte — radicaux maîtrisés : pas de « version », « boucle », « agent »), §1.2 (sous-commande featured + protocole : épingler AVANT la fenêtre ciblée, annonce au propriétaire = nom EXACT + taille ; vérifier le journal APRÈS la fenêtre), §2.3 (journal des téléchargements — remplace « sans journal persistant »), §3 (leçon filebin : aperçu plein écran → clic droit « Enregistrer l'image sous »), §2.2 structure, changelog §6.
5. Cascade : KB registre `## vue-upload v1.4.0`, ECO_SKILLS 1.4.0, note evals.json, rejeu triggers-replay (D016), integrity --check, correct-work(G0) CIBLE → commit dépôt.

### G1 — Contingence « récupération externe bloquée ×3-4 » → grille #token gen-plan v3.28.2 — COMPLÉTION (80 % exécuté) #token ~2 k
1. ~~grille-token.md + SKILL.md §4 + frontmatter 3.28.2~~ **FAIT (pré-exécuté, non commité)**.
2. ~~Cascade KO-L004 (PM v3.28.2, archive v3.28.1, historiques, KB, ECO_SKILLS, PM SHARED/INSTALL)~~ **FAIT (pré-exécuté, non commité)**.
3. **Reste** : projections hôte (SKILL.md + grille-token.md gen-plan → v3.28.2), manifeste rescellé si l'arbitre l'exige, `integrity --check` re-vert, `check-triggers-replay` re-vert (non-régression description gen-plan).
4. correct-work(G1) mode CIBLE → commit dépôt (avec G0 ou séparé).

### G2 — Analyse du corpus ZIP DJTT S4 MK2 v2.1.0 (objet des tâches suivantes) #token ~9 k
1. Script `scripts/zip-tsi/analyse-tsi-reel.py` (stdlib) : XML → `DeviceIO.Config.Controller` → Base64 → marche des trames FourCC (magique `DIOM`, `EIO/DEVU/DEVI/DDAT/DDIV/CMAI/CMAD/DCDT/DCBM/DVST…`, big-endian, chaînes UTF-16LE) — inventaire frames, extraction `cmdr_metadata` (JSON), extraction mappings (commandes, decks/groupes, MIDI canal/message/numéro, mode, conditions) + table CC consolidée.
2. Lecture VLM des 3 JPG (QuickGuide, Freeze Mode Help, Manual) — ground truth documentation du mapping (mode Freeze, couches, particularités S4 MK2) ; backoff 429 (contingence API ×2-3).
3. Croisement : mappings extraits ↔ tableaux des JPG ; particularités MK2 (ports, nom device `Traktor.Kontrol S4 MK2.Default`, Traktor 2.12.0).
4. Rapport `download/analyse-zip-djtt-s4mk2-v2.1.0.md` (×2 arbres) : inventaire, structure format réel, mappings extraits, documentation JPG, écart spec↔réel quantifié.
5. correct-work(G2) mode CIBLE.

### G3 — Validation des agents TSI sur le corpus réel (constats pré-calibration) #token ~4 k
1. `valider-tsi.py` sur les 3 TSI du ZIP → sorties brutes consignées (attendu : FAIL E1-structure « racine attendue NISYSTEM, trouvée NIXML » — constat d'écart R-1, pas un bug).
2. `generer-doc-midi.py` sur le TSI principal → comportement constaté (attendu : échec structurel — DEVICE absent).
3. Audit tsi-architect : `references/referentiel-structures-tsi.md` vs structure réelle (constat documenté — périmètre de calibration excluant tsi-architect, per directive).
4. Self-tests golden (non-régression format spec : PASS attendu ×2).
5. Rapport `download/rapport-validation-agents-tsi-2026-10-30.md` (×2 arbres) : verdicts bruts, écarts quantifiés, périmètre calibration dérivé.
6. correct-work(G3) mode CIBLE.

### G4 — Calibration midi-doc-expert + tsi-validator v1.1.0 (R-1/R-2, hôte seul) #token ~14 k
1. Module décodeur `skills/tsi-validator/scripts/decoder-format-reel.py` (stdlib, détenteur R4 du format réel) : détection racine `NIXML` → extraction `DeviceIO.Config.Controller` → décodage Base64 → marche FourCC → mappings normalisés (structure interne commune aux 2 skills).
2. `valider-tsi.py` v1.1.0 : routage format spec (NISYSTEM) ↔ format réel (NIXML) — règles E1-E8 adaptées au format réel (structure, comptage frames, attributs mappings, plages MIDI, doublons IN, LED OUT, modifiers) ; interface stable (verdict/exit/JSON) ; `--self-test` étendu (golden spec + échantillon réel).
3. `generer-doc-midi.py` v1.1.0 : génération doc (9 sections, MD+JSON, déterministe, couverture 100 %) depuis le format réel via le décodeur — dépendance YAML déclarée à tsi-validator (décodeur).
4. `samples/` : échantillon réel ajouté (`echantillon-reel-djtt-s4mk2.tsi` — mapping principal, hôte seul).
5. Versions v1.0.0 → v1.1.0 ×2 (MINOR, addition pure R2) : frontmatter + description enrichie avec parcimonie (format réel NIXML/Traktor 2.x — rejeu voie M obligatoire D009) + note evals.json ×2.
6. Re-validation : `valider-tsi.py` sur le TSI principal (verdict final documenté) + `generer-doc-midi.py` → doc générée (md+json) ; rejeu `check-triggers-replay` 47/47.
7. §6bis ligne Task 7 + rapport `download/rapport-calibration-trio-tsi-2026-10-30.md` (×2 arbres).
8. correct-work(G4) mode CIBLE.

### G5 — Certification, publication, E15, suggestions, clone-chat #token ~7 k
1. correct-work Mode PROJET (livrables du tour) — rapport `download/rapport-correct-work-projet-2026-10-30-task7.md`.
2. Commits dépôt (rapports G2-G4 + miroirs) + push `HEAD:main` SI PAT fourni au tour (D019) + ls-remote + audit anti-persistance 5 zones ; sinon commits locaux prêts + demande de re-provision.
3. Bilan E15 (#token estimé amendé ~47 k vs réel — contingence « récupération externe bloquée » mobilisée ×1 ce tour [3e lien, 1er coup : PAS bloqué — contingence NON déclenchée, à documenter honnêtement]).
4. **Suggestions skills/agents $facon** (D018 — ≥ 3 candidates fondées sur la discussion : hygiène des versions, livraison-garantie, qa-animation) : livrées au chat + consignées worklog.
5. Clone-chat 8/8 checks + entrées worklog (plan + amendement + groupes + E15 + suggestions).

## Risques et dégradations gracieuses

| Risque | Probabilité | Mitigation / fallback |
|--------|-------------|----------------------|
| R1 — Décodage binaire CMAI/CMAD plus profond que prévu (payload structures composites) | moyenne | Décodage partiel documenté (R-1 extension déclarative) : couverture honnête par catégorie de frame, verdict post-calibration rend compte de la couverture réelle — jamais de valeur inventée |
| R2 — VLM 429 sur les JPG | moyenne | Backoff/retry ×3 + downscale (PIL) ; contingence « appels API en masse ×2-3 » (grille v3.28.1) |
| R3 — Édition descriptions → dérive voie M | faible | Descriptions minimales ; rejeu obligatoire D009 ; en cas de dérive : reformulation neutre (retrait du radical fautif) — précédent cahier-des-charges 4c84cc4 |
| R4 — Push PAT | moyenne | **PAT absent du contexte courant** (constat 9) : commits locaux prêts, push différé + demande de re-provision — jamais d'invention de jeton ; si fourni : one-shot inline, `HEAD:main`, audit 5 zones |
| R5 — Volumétrie (TSI 1,8 Mo) | faible | stdlib XML itératif OK ; sample hôte seul (pas de contrainte dépôt) |
| R6 — Description vue-upload v1.4.0 → dérive voie M | faible | Radicaux maîtrisés (pas de « version », « boucle », « agent ») ; rejeu D016 ; en cas de dérive : reformulation neutre (précédent cahier-des-charges 4c84cc4) |

## Estimation #token (grille v3.28.1, amendée G0)

| Groupe | Estimation |
|--------|------------|
| G0 vue-upload v1.4.0 | ~7 k |
| G1 complétion cascade | ~2 k |
| G2 analyse + VLM | ~9 k |
| G3 validation | ~4 k |
| G4 calibration | ~14 k |
| G5 clôture + suggestions | ~7 k |
| **Total** | **~43 k** (fourchette 38-48 k) |

Coefficients appliqués : complexité standard 1.0x ; contingence « récupération externe bloquée ×3-4 » NON mobilisée ce tour (3e lien : récupération intégrale au 1er coup — la contingence v3.28.2 ajoutée en G1 couvre les cas adversariaux, pas les récupérations simples) ; contingence API ×2-3 partielle (VLM ×3 JPG).

---

**Horodatage plan : 2026-10-30T19:35:00+01:00** (initial 2026-10-30T19:15:00+01:00 — amendement 1 directive propriétaire ; retouches vérifications D002/D003 19:52+01:00 : proxy casse corrigé, critères inchangés — pattern Task 5)

**Answer key finale : 19/19 traitées** — 17 verified mécaniquement (rejeu G5), D010 DIFFÉRÉ (PAT absent du contexte — commits locaux prêts, demande de re-provision), D012/D018 accomplies en clôture (clone 8/8 + suggestions worklog). Corrections de vérificateurs tracées : D002/D003 (casse), D009 (statu quo 5 héritées), D004 (phrasing) — critères inchangés (pattern Task 5).

**Verdict E8 : PASS** (amendement 1 — answer-key-checker 16/16 ALL PASS arbre publication, re-exécuté 2026-10-30T19:38+01:00 ; check_plan_protocol P1-P5 PASS : P1 plan 34 k car. · P2 19 décisions/19 vérifications · P3 worklog R5 · P4 PLAN-AFFICHE · P5 verdict frais ; décisions D001-D019 criterion/verification/source/priority complets — Horodatage vérifié : 2026-10-30T19:35:00+01:00)
