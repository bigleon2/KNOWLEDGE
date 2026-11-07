# Plan d'actions — Task 9 : Push différé D010 (Task 8) avec PAT + résumé PDF Premium des skills créés et optimisés dans la discussion

> **Session** : web-eb6c8580 (continuation 7) · 2026-10-31 · **Généré via** : gen-plan v3.28.2 (mode NULL — exécution classique)
> **Type** : 2 (publication dépôt + document de synthèse) · **Profil** : NORMAL · **G-RES (E1-RES)** : OK → SÉRIE justifiée (le PDF documente le résultat du push — dépendance d'information G1→G2 ; écritures partagées worklog/download ×2 arbres ; commit de clôture unique)
> **Directive** : « utilise ma clé [PAT], puis fais moi un résumé (en version PDF Premium) des skills qui ont créés et optimisés dans cette discussion » — ① PAT re-fourni → push différé D010 des 5 commits Task 8 (fallback D019 levé, règle d'or n°4 : jeton one-shot, jamais persisté, jamais échoé) ; ② résumé PDF Premium des skills créés et optimisés au fil de la session web-eb6c8580 (Tasks 1-8, 2026-10-25 → 2026-10-31), contenu dérivé intégralement du worklog (règle d'or n°5 — chiffres mécaniques, jamais inventés).

> **Verdict E8 : PASS** — answer-key-checker 16/16 ALL PASS (pré-exécution) ; statuts answer key « pending » au départ (règle d'or n°5 — alignement sur preuve mécanique en clôture) ; vérifications YAML exécutables (syntaxe validée). **Horodatage vérifié : 2026-10-31T04:12:00+08:00**.
> **Horodatage plan : 2026-10-31T04:12:00+08:00** (anti-verdict-périmé, convention E7-DISP — re-validé à chaque écriture).

## Contexte d'entrée (vérifié en pré-vol E1-RES)

1. **État dépôt** : Task 8 clôturé 10/10 (9 verified + 1 accompli) — worktree publication `.staging/KNOWLEDGE-publish` propre @ **f24953d**, distant main = **03cdb0f** (ls-remote public vérifié à l'instant). **5 commits en attente de push** : 9548c5b (G1 vue-upload v1.5.0) · 191f52e (G2 livraison-garantie v1.0.0) · d4847ad (G3 gif-animator-pro v2.1.0) · 3b16c25 (G4 registre+certification) · f24953d (G5 clôture).
2. **Arbitres** : integrity 84/84 ×2 arbres · replay 48/48 (dérivées aucune) · correct-work 16/16 · answer-key 16/16 (état de sortie Task 8, worklog fait foi) ; arbitres E8 de ce cycle opérationnels (check_plan_protocol selftest, answer-key-checker 16 checks).
3. **PAT** : fourni ce tour par le propriétaire — usage one-shot au moment du push (pattern officiel D010 : fichier jeton `/tmp/kp` umask 077, consommation via `$(cat /tmp/kp)` dans l'URL push — la valeur n'apparaît dans aucune commande affichée, détruit immédiatement après), puis audit anti-persistance 5 zones (`scripts/task7-audit-d011.py`, ré-exécution post-push).
4. **Périmètre du résumé PDF** : session web-eb6c8580 = « cette discussion » (worklog Tasks 1-8) — **création** : livraison-garantie v1.0.0 ; **optimisations** : vue-upload v1.3.0→v1.4.0→v1.5.0, gif-animator-pro→v2.1.0 (qa-animation), midi-doc-expert→v1.1.0, tsi-validator→v1.1.0, cahier-des-charges→v2.0.2 (M4 + voie L MESURÉE), gen-plan v3.28.0→v3.28.2, vetos doctrinaux trio TSI (6/6 ×3). Contenu strictement dérivé du worklog + plans + rapports existants.
5. **Convention PDF** : les PDF sont commités dans `download/` du dépôt (précédents : rapport-consolide-genplan-T1-T2-T3.pdf…) → le résumé sera généré côté hôte `download/` (livrable propriétaire) ET projeté dans le worktree (commit de clôture).
6. **Sanity pré-vol** : zéro appel API externe requis ; Pillow/pymupdf disponibles ; `tool-results/` (artefacts de lecture runtime) NON commités.

## Answer Key (décisions — spec de session)

| ID | Décision (criterion) | Priorité | Statut |
|----|----------------------|----------|--------|
| D001 | Push D010 exécuté : distant main 03cdb0f → f24953d (les 5 commits Task 8), `HEAD:main` (jamais `main` — branche locale divergente), ls-remote vérifié AVANT (≡ 03cdb0f) et APRÈS (≡ HEAD worktree) | S1 | verified |
| D002 | PAT one-shot jamais persisté : fichier jeton /tmp/kp umask 077 détruit après usage, AUCUNE valeur complète dans remotes/credentials/worklog/plan/PDF/scripts, aucun `git config` d'authentification | S1 | verified |
| D003 | Audit anti-persistance 5 zones VERT post-push (scripts/task7-audit-d011.py ré-exécuté : remotes ×2, credentials, arborescence, historique poussé, /tmp) | S1 | verified |
| D004 | Résumé PDF Premium généré : `download/resume-skills-discussion-web-eb6c8580.pdf` — français, ligne Report (ReportLab + couverture HTML/Playwright html2poster.js), métadonnées complètes, pdf_qa.py PASS/WARN justifié, contrôle visuel pdftoppm | S1 | verified |
| D005 | Contenu PDF dérivé intégralement du worklog (règle d'or n°5) : création livraison-garantie v1.0.0 + optimisations vue-upload v1.4.0/v1.5.0, gif-animator-pro v2.1.0 (qa-animation), midi-doc-expert/tsi-validator v1.1.0, cahier-des-charges v2.0.2, gen-plan v3.28.2, vetos trio TSI — avec les chiffres mécaniques réels (tests 31/17/13 checks, replay 48/48, integrity 84/84, voie L F1 1.0, 5 626 mappings décodés) et la chaîne de livraison intégrée | S1 | verified |
| D006 | Clôture : worklog Task 9 (pré-vol, plan, groupes, E15) ×2 arbres, statuts answer key alignés sur preuve mécanique, PDF projeté worktree, commits hôte + worktree, push final de clôture, ls-remote ≡ HEAD | S2 | verified |
| D007 | Bilan E15 #token consigné (estimé vs réel, causes, recommandation éventuelle) | S2 | accompli |

```yaml
decisions:
  - id: "D001"
    criterion: "Distant main = f24953d après push (5 commits Task 8 publiés), préalable vérifié = 03cdb0f, forme HEAD:main"
    verification: "python3 -c \"import subprocess; out=subprocess.run(['git','-C','.staging/KNOWLEDGE-publish','ls-remote','https://github.com/bigleon2/KNOWLEDGE.git','refs/heads/main'],capture_output=True,text=True).stdout; assert out.startswith('f24953d'), out\""
    source: "directive « utilise ma clé » + pattern officiel D010 (worklog Task 7 clôture) + règle d'or n°4"
    priority: "S1"
    status: "verified"
  - id: "D002"
    criterion: "Zéro persistance du PAT : /tmp/kp détruit, aucun remote URL authentifié, aucune valeur complète (>= 40 car. après préfixe) dans les 2 arbres, le worklog et le plan"
    verification: "python3 scripts/task7-audit-d011.py"
    source: "convention anti-persistance Task 8/14 + D011 Task 7 (pattern réutilisé tel quel)"
    priority: "S1"
    status: "verified"
  - id: "D003"
    criterion: "Audit 5 zones VERT intégral re-exécuté APRÈS le push (zones 1-5)"
    verification: "python3 scripts/task7-audit-d011.py 2>&1 | grep -c VERT"
    source: "D011 Task 7 — audit re-joué post-push"
    priority: "S1"
    status: "verified"
  - id: "D004"
    criterion: "Le PDF existe (>= 5 pages, taille > 50 Ko), métadonnées Title/Author/Creator/Subject présentes, textes français corrects (accents rendus)"
    verification: "python3 -c \"import os, subprocess; from pypdf import PdfReader; p='download/resume-skills-discussion-web-eb6c8580.pdf'; r=PdfReader(p); assert os.path.getsize(p)>50000; assert len(r.pages)>=5; m=r.metadata; assert m.title and m.author; t=subprocess.run(['pdftotext','-f','1','-l','1',p,'-'],capture_output=True,text=True).stdout.lower(); assert 'skills' in t, 'couverture sans le mot skills'\""
    source: "directive « résumé (en version PDF Premium) » + skill pdf (ligne Report) + checklist qualité"
    priority: "S1"
    status: "verified"
  - id: "D005"
    criterion: "Le texte du PDF mentionne les 7 skills/versions clés avec leurs chiffres mécaniques : livraison-garantie v1.0.0, vue-upload v1.5.0 (31 checks), gif-animator-pro v2.1.0 (13 checks), midi-doc-expert v1.1.0, tsi-validator v1.1.0 (5 626 mappings), cahier-des-charges v2.0.2 (F1 1.0), replay 48/48"
    verification: "python3 -c \"import subprocess; t=subprocess.run(['pdftotext','download/resume-skills-discussion-web-eb6c8580.pdf','-'],capture_output=True,text=True).stdout.replace('\\xa0',' '); req=['livraison-garantie','v1.5.0','v2.1.0','v1.1.0','v2.0.2','48/48','5 626']; missing=[k for k in req if k not in t]; assert not missing, missing\""
    source: "règle d'or n°5 (chiffres dérivés d'artefacts vérifiables — worklog Tasks 5-8) + directive « skills qui ont créés et optimisés »"
    priority: "S1"
    status: "verified"
  - id: "D006"
    criterion: "Clôture complète : entrée worklog Task 9 dans les 2 arbres, statuts plan alignés (aucun pending restant), PDF présent ×2 arbres, commits hôte + worktree, push clôture exécuté, ls-remote ≡ HEAD"
    verification: "python3 -c \"import subprocess; w='.staging/KNOWLEDGE-publish'; c=open('download/plan-task9-push-d010-resume-pdf-premium.md',encoding='utf-8').read(); assert 'status: \\\"pending\\\"' not in c, 'statuts non alignés'; assert subprocess.run(['git','-C',w,'status','--porcelain'],capture_output=True,text=True).stdout.strip()=='', 'worktree sale'; out=subprocess.run(['git','-C',w,'ls-remote','https://github.com/bigleon2/KNOWLEDGE.git','refs/heads/main'],capture_output=True,text=True).stdout; head=subprocess.run(['git','-C',w,'rev-parse','--short=7','HEAD'],capture_output=True,text=True).stdout.strip(); assert out.startswith(head), (out, head)\""
    source: "règle d'or n°5 (statuts alignés sur preuve) + pattern clôture Task 7 (commit de clôture poussé)"
    priority: "S2"
    status: "verified"
  - id: "D007"
    criterion: "Bilan E15 présent dans l'entrée worklog Task 9 (estimé vs réel, causes dominantes, recommandation candidate éventuelle)"
    verification: "grep -c 'E15' worklog.md"
    source: "grille #token v3.28.2 §4 + §1.14 gen-plan"
    priority: "S2"
    status: "accompli"
```

## Groupes d'exécution (série justifiée — dépendance d'information G1→G2, écritures partagées, commit de clôture unique)

| Groupe | Contenu | Livrables | Hook |
|--------|---------|-----------|------|
| **G1** | Push D010 Task 8 | ls-remote avant (≡ 03cdb0f) · push `HEAD:main` via jeton /tmp/kp (umask 077, détruit) · ls-remote après (≡ f24953d) · audit anti-persistance 5 zones · consignation worklog (bloc clôture Task 8 D010, ×2 arbres) | correct-work(G1) CIBLE |
| **G2** | Résumé PDF Premium | lecture briefs pdf (report.md + fichiers référencés) · palette.cascade · couverture HTML (cover.md, html2poster.js + cover_validate.js) · corps ReportLab · fusion pypdf · pdf_qa.py + contrôle visuel | correct-work(G2) CIBLE |
| **G3** | Clôture | statuts answer key alignés · worklog Task 9 (E15) ×2 arbres · PDF projeté worktree · commits hôte + worktree · push clôture · ls-remote ≡ HEAD | correct-work(G3) CIBLE |

## Estimation #token (grille v3.28.2)

- **Estimé** : ~27 k (G1 4 k · G2 18 k · G3 5 k) — plage 22-34 k.
- **Facteurs** : push = procédure officielle re-jouée (coût faible) ; PDF = ligne Report complète (lecture briefs + références typesetting ~12 k, génération + itérations QA ~6 k) ; clôture standard ×2 arbres.
- **Contingences** : échec pdf_qa → itération correctrice (+3 k) ; rejet push (non-fast-forward) → diagnostic avant toute force (+2 k, jamais de --force) ; PAT refusé (révoqué) → commits locaux conservés + demande de re-provision (fallback D019).

## Règles de session (rappel)

- Règle d'or n°4 : PAT one-shot au push — jamais persisté, jamais échoé dans les commandes affichées (consommation via `$(cat /tmp/kp)`), détruit après ; rappel révocation/rotation au propriétaire en clôture.
- Règle d'or n°5 : statuts answer key « pending » au départ — JAMAIS pré-écrits ; alignés sur preuve mécanique à la clôture ; chiffres du PDF dérivés du worklog uniquement.
- R2 : aucune modification des livrables Task 8 (skills, tests, registre) — ce cycle publie et documente, il n'édite pas le corpus.
