# CLONE DE DISCUSSION — Task 48 : écosystème personnel + iphone19 pixel binning + photos 1944

> **Date du clone** : 2026-10-21
> **Source** : Discussion entre le propriétaire (bigleon2) et Super Z (assistant Z.ai) — session web-38713acd (suite)
> **Sessions couvertes** : discussion courante (directive 2026-10-21) — 6 entrées worklog Task 48, héritage Tasks 41-47
> **Version clone-chat** : 2.0.1

---

## §0 — RÈGLE ZÉRO — CONTEXTE PERDU

Les fichiers des sessions précédentes n'existent pas dans cette nouvelle session.
Tu dois **reconstruire** l'intégralité du contexte à partir de ce document.
Ne jamais utiliser le verbe « conserver » — tout est à recréer.

Contexte matériel cible : assistant Z.ai sur /home/z/my-project (profil local de l'écosystème Knowledge personnel du propriétaire — dépôt GitHub bigleon2/KNOWLEDGE, clone certifié local tmp/KNOWLEDGE-repo) ; SDK z-ai-web-dev-sdk (bun, module /home/z/.bun/install/global/node_modules/z-ai-web-dev-sdk/dist/index.js) ; Python 3.12 + PIL ; garde É1-INSTALL (réinstallation auto post-wipe).

---

## §1 — CHRONOLOGIE DE LA DISCUSSION

### §1.0 Héritage — chaîne de clonage

Lignée : sessions Tasks 41-47 (2026-10-08 → 2026-10-20) couvertes par le worklog `worklog.md` (aucun clone-chat antérieur matérialisé — ceci est le PREMIER clone de la lignée) : migration iphone18 (Task 41), tests PA-TEST-001 à 005 (Tasks 42-46), skills photo au dépôt (Task 44), mission 7 étapes (Task 45), nouvelle tentative 17_max + comparaisons (Task 46), migration ANTICIPÉE iphone19 v0.9.0 + installation écosystème + PA-TEST-005 + comparaison copines (Task 47). État de départ connu : dépôt GitHub à jour @ e62f354 (3 skills photo 17 v1.0.0 / 18 v1.0.0 / 19 v0.9.0 + PMs @photos + KB 36). La présente discussion ajoute 6 entrées worklog (Task 48 : installation+G1, G2, G3, G4, G5, G6).

### §1.1 Résumé global

Directive propriétaire ordonnée du 2026-10-21 : (étape 1) réinstaller l'écosystème personnel sur le profil local depuis le PM-INSTALL b75a620 (post-wipe inter-sessions : gen-plan/ et correct-work/ avaient disparu), puis gen-plan(step) pour : vérifier que iphone19 émule le pixel binning (article Frandroid), produire la comparaison enrichie du rendu 19 pour « les potos », adapter les 3 skills aux photos de 1944, tester robustement les 3 skills sur « libération après guerre », comparer les 3 rendus, exécuter correct-work(projet) puis clone-chat. Livrables clés : iphone19 v0.10.0 (R19 émulation pixel binning 16-en-1 — Sony Lytia 901 200 MP → 12,5 MP), extension 1944 des 3 skills (v1.1.0 / v1.1.0 / v0.11.0 — ère 40s, grain préservé, monochrome natif, aucune colorisation), rendus PA-TEST-006 (potos, QC 13/13) et PA-TEST-007 (libération ×3 skills : QC 11/11, 12/12 après 1 itération anti-colorisation, 13/13), 2 comparaisons enrichies, archivage R4 @historique/photos/, certification 6/6 arbitres, correct-work(projet) 25/25. Évolution : de la vérification d'une rumeur à une montée en version complète des 3 skills métier + validation empirique sur photo historique réelle. État final : écosystème certifié, 3 skills photo bumpés et testés, dépôt prêt à pousser (D010).

### §1.2 Table des sessions

| # | Date | Thème | Livrables principaux |
|---|------|-------|---------------------|
| T48-1 | 2026-10-21 | Réinstallation écosystème (étape 1) + gen-plan plan + G1/S1 pixel binning | task48-install-ecosysteme.py (PASS), recalibrage KO-L004 (ECO_SKILLS 36), rescellage archive v2.3, certification 6/6 ; plan Task 48 (YAML+MD, answer key D001-D011, E8 25/25) ; iphone19 v0.10.0 (R19 + QC 13), audit 44/44, rapport-S1, CW G1 21/21 |
| T48-2 | 2026-10-21 | G2/S2 — rendu 19 potos + comparaison enrichie | PA-TEST-006-1 (QC 13/13 après requalification motivée par arbitrage pleine image), comparaison-les-potos-5-versions.png + rapport, CW G2 21/21 ; commit 29e2de1 |
| T48-3 | 2026-10-21 | G3/S3 — extension 1944 des 3 skills | PMs v2.1/v1.1/v0.11.0 (note §1, ère 40s, §6.6), skills v1.1.0/v1.1.0/v0.11.0, @historique/photos/ (4 versions scellées), recalibrage croisé, audit 74/74, re-certification 6/6, CW G3 21/21 ; commit 3245b27 |
| T48-4 | 2026-10-21 | G4/S4+S5 — test robuste libération ×3 + comparaison | PA-TEST-007-1/2/3 (QC 11/11 ; 12/12 après it. 1/2 anti-colorisation ; 13/13), comparaison-liberation-apres-guerre-cote-a-cote.png, 2 rapports, CW G4 32/32 ; commit 54aecf8 |
| T48-5 | 2026-10-21 | G5/S6 — correct-work (projet) | 25/25 PASS (C01-C25) après mise en rejouabilité des vérificateurs (audit --old/--new refs git) ; commit 7fd432e |
| T48-6 | 2026-10-21 | G6/S7 — clone-chat + clôture dépôt | Le présent clone + push final D010 |

### §1.3 Détail par session

**T48-1 (installation + G1)** : réinstallation profil COMPLET post-wipe (§3.4) via task48-install-ecosysteme.py — certification initiale 4/6 → 3 correctifs (ECO_SKILLS 35→36 iphone19 omis en Task 47, bidirectionnalité skill-creator↔iphone19, rescellage archive v2.3 : la KB pilier avait divergé) → 6/6. gen-plan v3.23.1 mode (step) : plan + answer key D001-D011 persistés avant action (E8 25/25). S1 : article Frandroid relu 2× (200 MP Sony Lytia 901, 16-en-1 → 12,5 MP, 1/1,12″, DCS, 2027) ; constat honnête : v0.9.0 n'émulait PAS (exclusion §4.4 « rumeur unique ») → bump v0.10.0 : R19 (ajout pur), QC 13 (ajout pur), propagations §0/§3/§5/§6.1/§6.10/§7/§8/§11/§12, coquille §6.9 corrigée ; projection + evals + KB + ECO_SKILLS + README @photos (ligne iphone19, oubli Task 47 résorbé) ; audit 44/44 ; CW CIBLE 21/21.

**T48-2 (G2)** : campagne PA-20261021-006 — leçon PA-TEST-005 appliquée d'emblée (recette conservatrice it.2 + expression R19) : 2 appels, zéro itération, QC 12/13 directs → KO unique critère 5 (lisibilité inscription t-shirt) tranché par PROTOCOLE VARIANCE-VISION : arbitrage pleine image confiance haute (inscription identique, netteté excellente ×1,9) → requalification motivée 13/13. Comparaison enrichie 5 versions + guide (même format D7 copines). CW 21/21 (2 faux positifs anti-persistance levés : chaînes de recherche nues dans les vérificateurs).

**T48-3 (G3)** : audit du chemin restauration → 3 bumps chirurgicaux en ajout pur (note §1 années 1940 : grain authentique ≠ bruit, dégâts A10, tonalité A8, monochrome natif, aucune colorisation — G3/règle 7 ; ère 40s table §6.5 ; extension §6.6 1930-1950 : monochrome, tonalité restaurée sans HDR, grain préservé par défaut, dégâts P1, détails uniquement depuis l'existant — drapeaux/inscriptions/uniformes/armes/foule, netteté honnête) ; archivage R4 : création @historique/photos/ (4 versions extraites git byte-identiques, INDEX.md SHA-256) ; recalibrage croisé KO-L004 (KB 3 entrées + ECO_SKILLS + README @photos règle 1 réalignée sur la pratique + README @historique) ; projections régénérées VERBATIM (417/431/463 lignes) ; audit 74/74 ; rescellage + re-certification 6/6 ; CW 21/21.

**T48-4 (G4)** : analyse dédiée de « libération après guerre » (828×550, tirage argentique N&B août 1944 — B6 exhaustif verrouillé : camion, drapeaux tricolore + US, casques, carabine, foule, haussmannien). 3 chaînes indépendantes : 17 → 11/11 zéro it. ; 18 → v1 REJETÉE (colorisation complète : drapeaux peints, camion vert olive, grain écrasé, 4/12 divergences majeures) → CONSTAT SYSTÉMIQUE mesuré PIL : l'étage P1-P6 colorise 3/3 (saturations 23-29, même avec consigne renforcée) ; l'étage RENDU restaure le monochrome → it.1/2 : 12/12 fidèle ; 19 → 13/13 zéro it. (binning sans écraser le grain). P0 intacts. Comparaison enrichie (panneaux 3:2, panneau P1-P6 désaturé mécaniquement et étiqueté honnêtement). CW 32/32.

**T48-5 (G5)** : correct-work(projet) C01-C25 — 1re passe 23/25 : 2 KO de REJOUABILITÉ des vérificateurs (audit v0.10.0 rejoué contre le PM courant v0.11.0 ; scans anti-persistance mutuels) → corrections (audit paramétré --old/--new refs git, exclusions unifiées task48-cw-*, motif de JETON réel github_pat_<20+ car. — la chaîne documentaire nue du rapport Task 47 n'est pas un jeton) → re-jeux G1-G4 PASS + **25/25 PASS**. Réserve : push différé à G6.

**T48-6 (G6)** : exécution du skill clone-chat v2.0.1 (le présent document, 7+1 étapes, 8 checks) + clôture dépôt : commit final + PUSH GitHub (D010, PAT éphémère jamais persisté).

---

## §2 — ÉCOSYSTÈME DE SKILLS

### §2.1 Skills créés ou modifiés

#### iphone19 v0.11.0 [ANTICIPÉE] (skill) — PM `skills/@photos/iphone19-photos.md` v0.11.0
- **Description** : pipeline CPE « iPhone 19 Pro Max » génération ANTICIPÉE 2027 ; v0.10.0 = émulation pixel binning R19 (directive propriétaire, Frandroid 27/03/2026) ; v0.11.0 = extension 1944.
- **Catégorie** : métier | **Langue** : fr
- **Spécification fonctionnelle** : grille ANALYSE-v2 (A1-A10, B1-B6 verrouillé, C1-C3) + note années 1940 ; moteur R1-R19 (R19 : pixel binning 16-en-1 — capteur 200 MP → sortie 12,5 MP équivalente, SNR/lumière/crop-zoom, [RUMEUR] DCS via Frandroid) ; pipeline P0-P8/P8b ; QC 13 critères (13 = binning respectée sans lissage plastique ni altération des sujets) ; presets §6 (défaut iphone19_max, ère 40s §6.5, restauration §6.6 extension 1930-1950) ; squelette §6.10 iphone20 INACTIF ; commandes §13 (preset:iphone20 refusé).
- **Spécification technique** : projection VERBATIM du PM (byte-identité R2, jamais édité) ; scripts/editer-image.mjs (contournement SDK base64) ; evals 8+8 (moteur R1-R19).
- **Relations** : dépend de skill-creator (conventions), VLM + image-edit (plateforme) ; lignage : v0.9.0 (migration Task 47) → v0.10.0 (pixel binning Task 48 G1) → v0.11.0 (1944 Task 48 G3) ; v0.9.0 et v0.10.0 scellées @historique/photos/.

#### iphone18 v1.1.0 (skill) — PM `skills/@photos/iphone18-photos.md` v1.1
- **Description** : pipeline CPE « iPhone 18 Pro Max » génération CONFIRMÉE ; v1.1 = extension 1944 (même package que 19, sans R19 ; garde R18 ouverture variable, QC 12).
- **Relations** : v1.0 scellée @historique/photos/ ; testée PA-TEST-007 (QC 12/12 après it. anti-colorisation).

#### iphone17 v1.1.0 (skill) — PM `skills/@photos/iphone17-photos.md` v2.1
- **Description** : pipeline CPE « iPhone 17 Pro Max » PÉRIMÈTRE D'ÉPOQUE (génération archivée au plan générationnel) ; v2.1 = extension 1944 (sans R18/R19 ; QC 11 ; R1-R17).
- **Relations** : v2.0 scellée @historique/photos/ ; testée PA-TEST-007 (QC 11/11 zéro itération).

#### Écosystème (profil local, réinstallation)
- gen-plan v3.23.1, correct-work v2.7.0, clone-chat v2.0.1 ( fraîchement installés, exécutés) ; certification 6/6 arbitres (verify-cross 108/108 ×2, verify-correct-work 16/16, check-ecosysteme-integrity 76/76, interactions 50/51 [1 WARN hérité toléré], check-tool-routing 6/6) ; archive d'intégrité v2.3 rescellée 2× (corpus 9 + piliers 6) ; ECO_SKILLS 36 (17 1.1.0, 18 1.1.0, 19 0.11.0).

### §2.2 Scripts créés ou modifiés (tous dans `scripts/`, versionnés au dépôt)

| Script | Rôle | Points clés |
|---|---|---|
| task48-install-ecosysteme.py | Réinstallation profil COMPLET (phases A-E) | idempotent, rapport JSON, certification |
| task48-rescellage-archive.py | Rescelleur archive v2.3 | corpus 9 + piliers 6, round-trip byte-identique, garde .bak |
| task48-validate-plan.py | E8 validation plan + answer key | 25/25 |
| task48-ip19-v010-projection.py | Régénération projection 19 v0.10.0 | frontmatter + §0 + lignage + corps PM verbatim |
| task48-audit-ip19-v010.py | Auto-audit bump v0.10.0 | 44/44 ; **paramétrable --old/--new (refs git) — rejouable** |
| task48-cw-g{1..4}.py, task48-cw-projet.py | correct-work CIBLE par groupe + PROJET | 21/21, 21/21, 21/21, 32/32 ; projet 25/25 |
| task48-pa006-{p1,rendu}-potos.txt, task48-pa006-qc.mjs, task48-pa006-arbitrage{,-crop}.mjs/py, -arbitrage-full.mjs | Campagne PA-TEST-006 (potos v0.10.0) | QC 13, protocole variance-vision |
| task48-comparaison-potos.py | Composite 5 versions potos | PIL pur, 2208×1204 |
| task48-historique-photos.py | Archivage R4 @historique/photos/ | extraction git, INDEX SHA-256 |
| task48-v1944-projections.py | Régénération 3 projections (1944) | 417/431/463 lignes |
| task48-recalibrage-1944.py | Recalibrage croisé KB/ECO_SKILLS/READMEs | 20 remplacements chirurgicaux assertés count==1 |
| task48-audit-1944.py | Auto-audit 3 bumps 1944 | 74/74 |
| task48-pa007-analyse.mjs | Analyse ANALYSE-v2 libération | B6 exhaustif |
| task48-pa007-p1.txt, -p1-r19.txt, **-p1-monochrome.txt**, -rendu-{17,18,19}.txt | Instructions de génération | la version -monochrome est la référence anti-colorisation |
| task48-pa007-qc.mjs | QC par skill (11/12/13 critères) | B6 libération + contexte 1944 |
| task48-comparaison-liberation.py | Composite libération | panneaux 3:2 720×480, P1-P6 désaturé mécanique |
| task48-plan-directive.yaml, -plan-PA-20261021-00{6,7}.yaml | Plans (règle 3 : persistés avant action) | answer key, ordre, invariants |

### §2.3 Artefacts produits (download/, non versionnés au dépôt sauf rapports)

| Fichier | Taille | Description |
|---------|--------|-------------|
| PA-TEST-006-1-iphone19-max.png + intermédiaire + candidat | ~75-86 Ko | Rendu 19 v0.10.0 « les potos » (QC 13/13) |
| comparaison-les-potos-cote-a-cote-5-versions.png | 2208×1204 | 5 versions + guide |
| PA-TEST-007-{1,2,3}-iphone1{7,8,9}-max.png (+ intermédiaires + candidats) | ~114-133 Ko | Rendus libération (QC 11/12/13) |
| comparaison-liberation-apres-guerre-cote-a-cote.png | 2208×1084 | 5 panneaux 3:2 + guide 1944 |
| rapport-S1-verification-pixel-binning.md | ~5 Ko | Vérification + table article→implémentation |
| rapport-comparaison-potos.md, rapport-PA-TEST-007.md, rapport-comparaison-liberation.md | ~5-7 Ko | Rapports gabarit §8 |
| rapport-installation-ecosysteme-task48.json, rapport-cw-projet-task48.json | JSON | Preuves PASS |
| plan-task48-directive.md | ~4 Ko | Plan conventionnel (routage normatif) |
| skills/@historique/photos/ (dépôt) | 4 PMs + INDEX.md | Archive R4 scellée |

### §2.4 Historique des interactions (KB)

gen-plan v3.23.1 mode (step) —invoque→ correct-work v2.7.0 (CIBLE ×4 groupes puis PROJET 25/25) —utilise→ skills iphone17/18/19 (campagnes PA-TEST-006/007 via image-edit/VLM plateforme) ; gen-plan —routage→ skill-creator (skills), agent-creator (PMs), script-creator (scripts), script-mon-ecosysteme-infrastructure (déploiement), knowledge-observer (leçons), clone-chat v2.0.1 (archivage — le présent document) ; certification-complete.py (6 arbitres) à l'installation et post-G3.

---

## §3 — DÉCISIONS CLÉS

### §3.1 Décisions de l'utilisateur

| # | Décision | Contexte | Conséquence |
|---|----------|----------|-------------|
| 1 | Ordre imposé : installer l'écosystème PUIS gen-plan(step) | PM-INSTALL b75a620 cité comme source unique | Réinstallation post-wipe + plan régénéré via gen-plan fraîchement installé (règle d'or n°2) |
| 2 | « Vérifie que mon skill iphone19 émule bien la technique pixel binning » (frandroid) | Article 27/03/2026 : 200 MP Sony Lytia 901, 16-en-1 → 12,5 MP | Constat honnête (v0.9.0 n'émulait pas — exclusion §4.4 rumeur unique) + corrective v0.10.0 : R19, QC 13, statut [RUMEUR] conservé (2e publication DCS) |
| 3 | « La réponse à la dernière question du skill sera "sans modification, ni retouches" » (potos, libération ×3) | Contrainte zéro-retouche pré-décidée | Recettes conservatrices, aucune retouche, itérations QC uniquement sur fidélité |
| 4 | « Fais en sorte que mes skills 17/18/19 puissent traiter fonctionnellement et de façon optimisée les photos prises en 1944 » | Photo « libération après guerre » fournie | Extension 1944 en ajout pur (note §1, ère 40s, §6.6) + bumps MINOR ×3 + archivage R4 |
| 5 | « Effectue un test robuste » sur la photo 1944 | Photo inédite | Campagne PA-TEST-007 : 3 chaînes indépendantes, QC par skill, P0 intacts |
| 6 | « Exécute correct-work (projet) puis clone-chat » | Clôture écosystème | 25/25 PASS + présent clone |

### §3.2 Bugs corrigés

| # | Bug | Cause | Fix | Résultat |
|---|-----|-------|-----|----------|
| 1 | Certification 4/6 à la réinstallation | ECO_SKILLS 35 vs KB 36 (recalibrage omis Task 47 D3) + asymétrie skill-creator↔iphone19 + archive divergente (pilier KB) | Recalibrage + bidirectionnalité + rescellage v2.3 | 6/6 arbitres PASS |
| 2 | 18_max libération colorisé (drapeaux bleu-blanc-rouge, camion vert olive) | Biais du modèle de génération : scène iconique « Libération » → souvenir couleur ; l'étage P1-P6 colorise systématiquement (3/3, saturations 23-29) même avec consigne renforcée | Itération 1/2 : rejeu P1 renforcé + rendu conservateur (l'étage rendu RESTAURE le monochrome) | v2 : QC 12/12 fidèle, saturation 0.10 ; recette consignée : P1 → rendu conservateur monochrome |
| 3 | KO QC critère 5 (inscription t-shirt, PA-TEST-006) | Variance vision en grille globale | Protocole Groupe F : arbitrage ciblé pleine image (confiance haute : inscription identique, netteté excellente) | Requalification motivée 13/13 |
| 4 | Vérificateurs non rejouables (CW projet 23/25) | Audits point-in-time rejoués contre l'état courant (v0.11.0) ; scans anti-persistance se détectant mutuellement | Audit paramétré --old/--new (refs git) ; exclusions unifiées task48-cw-* ; motif de jeton RÉEL (github_pat_<20+ car. — la chaîne documentaire nue n'est pas un jeton, précédent Task 47 D5) | G1-G4 re-jeux PASS + CW projet 25/25 |
| 5 | Divers scripts : bugs mécaniques | Mode bits 644→755 (bruit git, restauré) ; course d'écriture Write/Bash ; « canvas » npm absent (→ PIL) ; JSON analyse avec sauts de ligne bruts (extraction textuelle) ; motifs d'audit (R17/R18 en gras, split '-v') | Corrections ciblées à chaque fois | Tous résolus en séance |

### §3.3 Conventions établies

| Convention | Règle | Exemple |
|------------|-------|---------|
| Archivage PMs @photos | Toute évolution = bump versionné dans le fichier vivant (changelog + note rétroactive §11 + auto-audit) + archivage de la version supplantée dans @historique/photos/ (extraction git byte-identique, SHA-256 scellé INDEX.md) + table §2 README | iphone18-photos-v1.0.md scellé au bump v1.1 |
| Sourcing rumeur photo | Une fuite exclue (« rumeur unique ») peut être intégrée en ÉMULATION sur directive propriétaire dès qu'une 2e publication la relaie — statut [RUMEUR] conservé, re-ancrage prévu à la confirmation | R19 pixel binning (DCS via Frandroid) |
| Photos 1944 (§6.6) | Monochrome natif (aucune colorisation — G3), grain argentique préservé par défaut (A3 « grain » ≠ bruit), tonalité restaurée sans HDR, dégâts en P1, détails uniquement depuis l'existant, netteté honnête | « libération après guerre » |
| Rejouabilité des vérificateurs | Tout audit/CW de session doit être rejouable : comparaisons par refs git (--old/--new), jamais contre l'état courant implicite ; scans anti-persistance par motif de jeton réel, vérificateurs exclus | task48-audit-ip19-v010.py --old e62f354 --new 29e2de1 |

### §3.4 Données de calibration

- Certifications : installation 6/6 (76/76 intégrité, 50/51 interactions — 1 WARN hérité toléré, 108/108 verify-cross ×2, 16/16, 6/6 routage) ; re-certification post-G3 identique.
- QC campagne : PA-TEST-006 13/13 (12 directs + 1 requalifié) ; PA-TEST-007 : 11/11 (0 it.), 12/12 (1/2 it.), 13/13 (0 it.) — fidélité zéro divergence ×4 sorties.
- Saturations mesurées (libération) : original 0.01 ; intermédiaires P1 23-29 (colorisés 3/3) ; finaux 0.16 / 0.10 / 0.48.
- Auto-audits : v0.10.0 44/44 ; bumps 1944 74/74. CW : 21/21, 21/21, 21/21, 32/32, projet 25/25.
- Dépôt : 4 commits Task 48 (29e2de1, 3245b27, 54aecf8, 7fd432e) + clôture ; KB 37 lignes « ## X v » (36 entrées arbitre).

### §3.5 Évolutions de contexte (Context Drift)

Cette section trace chaque fois que le contexte a **changé** durant la discussion.

**5 types de drift** :

| Type | Définition |
|------|----------|
| INVERSION | Décision renversée (A accepté → A refusé) |
| MODIFICATION | Décision ajustée (paramètre X → Y) |
| CORRECTION | Spécification ou décision erronée corrigée |
| ENRICHISSEMENT | Décision complétée (ajout d'un élément nouveau) |
| RECALIBRAGE | Paramètre ajusté (seuil, ratio, estimation recalibré) |

**Table des drifts** :

| # | Type | Avant | Après | Session | Ligne worklog | Raison |
|---|------|-------|-------|---------|---------------|--------|
| 1 | ENRICHISSEMENT | iphone19 v0.9.0 : 200 MP exclu (« rumeur unique », citation contexte seul) | v0.10.0 : R19 émulation pixel binning 16-en-1 intégrée (2e publication Frandroid + directive propriétaire) | T48-1 | G1 | Directive « vérifie que mon skill émule le pixel binning » |
| 2 | RECALIBRAGE | QC iphone19 = 12 critères | QC = 13 critères (binning respectée) | T48-1 | G1 | Propagation §11d de R19 |
| 3 | ENRICHISSEMENT | Ères §6.5 : 70s → 2010s ; restauration générique | Ères : **40s** → 2010s + extension §6.6 années 1930-1950 (monochrome, grain, aucune colorisation) | T48-3 | G3 | Directive « photos prises en 1944 » |
| 4 | MODIFICATION | Directive Task 47 : D1-D8 (push/install/migration/test/cw/push/comparaison) | Directive Task 48 : S1-S7 (pixel binning, comparaisons, 1944, correct-work, clone-chat — sans étapes push explicites, clôture D010 par précédent) | T48-1 | plan | Nouveau message ordonné du propriétaire (2026-10-21) |
| 5 | CORRECTION | En-tête §6.9 dupliqué (hérité migration v0.9.0) | En-tête unique (coquille documentée, précédent « pitié → piqué ») | T48-1 | G1 | Hygiène documentaire au bump |
| 6 | MODIFICATION | README @photos règle 1 : « jamais édités en place » (ambigu pour les bumps) | Pratique codifiée : bump versionné + changelog + archivage @historique/photos + table §2 | T48-3 | G3 | Aligner la règle sur la pratique établie (R4) |
| 7 | CORRECTION | Vérificateurs point-in-time (non rejouables après évolution) | Audits --old/--new refs git, exclusions unifiées, motif jeton réel | T48-5 | G5 | CW projet 23/25 → 25/25 |
| 8 | ENRICHISSEMENT | Plan PA-TEST-006 : rendu 19 potos à régénérer | Leçon systématique : scène iconique → étage P1 colorise ; recette = rendu conservateur monochrome en garant du livrable | T48-4 | G4 | Échec 18 v1 + mesure PIL 3/3 |

---

## §4 — INSTRUCTIONS D'UTILISATION

### Comment utiliser ce clone
1. Ouvrir une nouvelle session avec un assistant IA
2. Coller le contenu de ce fichier
3. Dire : « Exécute le clone de discussion »
4. L'assistant recrée le contexte et peut poursuivre le travail

### Ce que l'assistant doit faire
1. Lire §0 (Règle zéro) — tout est à reconstruire
2. Vérifier l'état de départ : clone certifié tmp/KNOWLEDGE-repo (git log : 4+ commits Task 48 poussés sur origin/main bigleon2/KNOWLEDGE), profil local skills/ (garde É1-INSTALL : `python3 skills/gen-plan/scripts/ensure-installed.py --check`), certification (`python3 scripts/certification-complete.py` — attendu 6/6, 1 WARN hérité toléré)
3. Les fichiers sources de vérité vivent dans le dépôt (PMs @photos v2.1/v1.1/v0.11.0, skills 17 v1.1.0/18 v1.1.0/19 v0.11.0, @historique/photos/, KB 36) — les reconstruire par sync dépôt→profil si wipe (task48-install-ecosysteme.py est idempotent)
4. Appliquer les décisions et conventions de §3 (notamment : archivage @historique/photos, sourcing rumeur, photos 1944, rejouabilité)
5. Les recettes de génération critiques sont dans `scripts/task48-pa007-p1-monochrome.txt` (instruction technique anti-colorisation de référence — en cas de régénération sur photo 1944, la passer à l'étage P1 PUIS impérativement l'étage rendu conservateur monochrome) et `scripts/task48-pa007-rendu-{17,18,19}.txt` (rendus par génération)
6. Se positionner à l'état exact de la fin : directive S1-S7 intégralement exécutée, dépôt poussé (D010)

### Fichiers à reconstruire en priorité
1. **skills/@photos/iphone19-photos.md v0.11.0** — PM courant génération 19 (R19 + 1944)
2. **skills/@photos/iphone18-photos.md v1.1 / iphone17-photos.md v2.1** — PMs génération confirmée / archivée
3. **scripts/task48-pa007-p1-monochrome.txt + rendu-19.txt** — recettes génération 1944 de référence (in extenso au dépôt)
4. **scripts/check-ecosysteme-integrity.py** — arbitre ECO_SKILLS (36, versions 1.1.0/1.1.0/0.11.0)
5. **skills/KNOWLEDGE.md** — registre KB (36 entrées)

---

## §5 — AUTO-CLONAGE

Ce clone est auto-référentiel. À la fin de la nouvelle session :
1. Exécuter le skill `clone-chat` sur la discussion en cours
2. Le nouveau clone contiendra : tout le contexte de ce clone (discussion originale) + tout le nouveau contexte de la discussion en cours
3. Le nouveau clone remplace ce fichier
4. Le clone « grandit » à chaque session sans perdre l'historique

**Mécanisme** : les sections §1-§3 (incluant §3.5 Context Drift) sont enrichies avec les nouvelles sessions. Les sections §0, §4-§5 sont régénérées à l'identique (auto-référentielles).
