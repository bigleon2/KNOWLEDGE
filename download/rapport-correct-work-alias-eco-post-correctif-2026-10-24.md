# Rapport correct-work post-correctif — alias-eco (mode CIBLE)

## Métadonnées
- **Date** : 2026-10-24 · **Mode** : CIBLE · **Version correct-work** : 2.8.0
- **Cible** : alias-eco v1.1.0 (2 réserves S3 du rapport 2026-10-24 — correction Task 25bis, plan `download/plan-task25-correction-reserves-alias-eco.md`)

## Vérification des corrections

| Réserve | Correction appliquée | Preuve mécanique | Statut |
|---------|---------------------|------------------|--------|
| R1 — trigger_evals 5/8 (3 faux positifs négatifs) | Description Optimization v1.1.0 : clause d'exclusion reformulée sans radicaux étrangers (« chaque compétence sœur couvre son propre domaine ») ; cascade KO-L004 (KB en-tête, format-alias §4, script docstring/source, journal @historique créé, parité profil local) | replay re-joué : **alias-eco 8/8, ok=true, 0 cas échoué** ; radicaux polluants restants : **AUCUN** ; dérives globales 20 → 19 (0 nouvelle) | ✅ CLOSE |
| R2 — registre @Alias absent au profil local | Projection conforme pipeline étape 7 (« Registre : sync @historique/@Alias/ — registre vivant ») | sha256 dépôt == local (33016333…) ×2 idempotent ; `--resolve "de $ECO-LEON, installation $OPT-TRIO"` → « de mon écosystème personnel » + signalement explicite de l'alias inconnu (rc=1) | ✅ CLOSE |

## Contrôles de non-régression

| Contrôle | Résultat |
|----------|----------|
| py_compile alias-manager.py ×2 (dépôt + profil) | PASS |
| alias-manager.py --selftest | **15/15 PASS** |
| Frontmatter YAML ×2 | OK — v1.1.0 |
| verify-cross (dépôt) | **111/111 PASS** — 0 warning, 0 erreur |
| evals canoniques (5 + 8) | OK — inchangés (le corpus officiel n'a PAS été touché : correction à la racine, pas sur le test) |
| Parité dépôt ↔ profil local (×4 : SKILL, format-alias, script, journal) | OK byte-identique |
| Règle d'or n°2 | 0 commit, 0 push — modifications tracées au git status (6 M + 4 ??), publication au GO |

## Résumé
- **Problèmes trouvés** : 0 nouveau
- **Corrections appliquées** : 2 (R1, R2) — validées mécaniquement
- **Problèmes restants** : 0
- **Verdict** : **PASS** (les 2 réserves S3 sont closes ; le verdict replFail global du replay — 19 dérives restantes dont les 3 iphone arbitrées Task 25 G2 — demeure « FAIL informatif » hors périmètre alias-eco)
