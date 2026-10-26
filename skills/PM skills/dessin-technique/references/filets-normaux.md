# Filets métriques ISO 261 — table de référence (F4 `mesurer_filet.py`)

> **Version** : 1.0.0 (v1.1.0 du skill) — **Date** : 2026-10-18 (Task 10)
> **Nature** : miroir documentaire de la table `TABLE_ISO` intégrée au script
> `scripts/mesurer_filet.py` (source exécutable). Toute évolution = éditer les DEUX
> sources + bump de version du skill (traçabilité R4).

## Protocole photo (conditions contractuelles)

1. Tige/vis **de profil** (axe de la vis horizontal ou vertical dans l'image) ;
2. Pièce de monnaie **posée à côté, même plan**, bien séparée de la tige ;
3. Stries du filet **nettes** (flou acceptable si la périodicité reste visible) ;
4. Zone filetée suffisamment longue (≥ ~10 périodes visibles).

Tolérances attendues : **pas ±10 %** (photo réelle), **Ø majeur ±5 %** ;
scène synthétique : ≤ 5 % (test T5).

## Table ISO 261 (gros + fins courants, M6 → M30)

| Désignation | Ø majeur (mm) | Pas (mm) | Famille |
|-------------|---------------|----------|---------|
| M6x1 | 6 | 1,0 | gros |
| M8x1.25 | 8 | 1,25 | gros |
| M8x1 | 8 | 1,0 | fin |
| M10x1.5 | 10 | 1,5 | gros |
| M10x1.25 | 10 | 1,25 | fin |
| M10x1 | 10 | 1,0 | fin |
| M12x1.75 | 12 | 1,75 | gros |
| M12x1.5 | 12 | 1,5 | fin |
| M12x1.25 | 12 | 1,25 | fin |
| M14x2 | 14 | 2,0 | gros |
| M14x1.5 | 14 | 1,5 | fin |
| M16x2 | 16 | 2,0 | gros |
| M16x1.5 | 16 | 1,5 | fin |
| M18x2.5 | 18 | 2,5 | gros |
| M18x2 | 18 | 2,0 | fin |
| M18x1.5 | 18 | 1,5 | fin |
| M20x2.5 | 20 | 2,5 | gros |
| M20x2 | 20 | 2,0 | fin |
| M20x1.5 | 20 | 1,5 | fin |
| M22x2.5 | 22 | 2,5 | gros |
| M22x2 | 22 | 2,0 | fin |
| M22x1.5 | 22 | 1,5 | fin |
| M24x3 | 24 | 3,0 | gros |
| M24x2 | 24 | 2,0 | fin |
| M26x1.5 | 26 | 1,5 | fin (écrou DKO VOSS 18L) |
| M27x3 | 27 | 3,0 | gros |
| M27x2 | 27 | 2,0 | fin |
| M30x3.5 | 30 | 3,5 | gros |
| M30x2 | 30 | 2,0 | fin |

## Critères de rapprochement (script)

Candidat retenu si : `|Ø_mesuré − Ø_table| / Ø_table ≤ 5 %` **ET**
`|pas_mesuré − pas_table| ≤ max(10 % × pas_table, 0,15 mm)`.
Sortie : liste des candidats triés par score combiné croissant
(`score = écart_Ø_rel + écart_pas/pas_table`) ; `meilleur` = premier.
Aucun candidat → valeurs brutes reportées (« hors table »).
