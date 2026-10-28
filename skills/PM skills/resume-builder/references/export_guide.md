# Guide d'export de CV

## Combinaisons recommandées

- **Pour les candidatures principales** : docx (format directement reçu par les RH) + pdf (version finale, pour éviter les problèmes de mise en page)
- **Sauvegarde** : md (pour ses propres itérations, à mettre sur GitHub)

## Export docx (par défaut)

Appeler la compétence docx. Priorité des modèles :
1. Modèle fourni par l'utilisateur → utiliser celui de l'utilisateur
2. `assets/resume_template.docx` existe → utiliser celui de cette compétence
3. Aucun des deux → utiliser le style par défaut de la compétence docx (attention à contrôler la police, l'interligne, les marges)

Paramètres de style (par défaut recommandé) :
- Police chinoise : Source Han Serif / SimSun / Microsoft YaHei (probablement présente sur l'ordinateur du RH)
- Police latine : Arial / Helvetica / Calibri
- Taille de police : corps 10.5~11pt, titres 12~14pt, nom 16~18pt
- Interligne : 1.15~1.3
- Marges : haut/bas 1.5cm, gauche/droite 1.8cm
- Couleur : entièrement noir + une couleur d'accentuation à faible saturation (bleu foncé / gris foncé)

## Export pdf

**Recommandé** : docx → conversion en pdf via libreoffice headless

```bash
libreoffice --headless --convert-to pdf <input.docx> --outdir <out_dir>
```

**Non recommandé** : dessiner directement depuis zéro avec reportlab / weasyprint, résultat moche et problèmes de police fréquents.

## Export markdown

Le plus simple et direct : nom de fichier recommandé `resume_<nom en pinyin>_<YYYYMM>.md`, par exemple `resume_zhangsan_202605.md`.

## Suggestions de nommage de fichier

Le nom de fichier lors des candidatures est extrêmement important (beaucoup de RH recherchent directement par nom de fichier) :

`<Nom>_<Poste visé>_<X années d'expérience>.<ext>`

Ex : `Zhang_San_Directeur_Produit_Senior_5ans.pdf`

Ne pas nommer `final.pdf`, `final_v2.pdf` ou `version-modifiee.docx`, les RH trouveront cela non professionnel.

## Nettoyage des métadonnées (pdf)

Appeler la compétence pdf pour nettoyer les métadonnées (auteur, outil de création), pour éviter de révéler l'origine du modèle Word original (certains modèles laissent des marques comme "Modèle de CV WPS v3.2").

## Confidentialité & Sécurité

- Le CV **ne contient pas par défaut le numéro d'identité, l'adresse personnelle, les contacts d'urgence**
- Ajouter uniquement si spécifiquement requis pour des postes particuliers (banque / fonction publique / entreprises d'État)
- Si le CV téléchargé par l'utilisateur contient ces informations, **les supprimer activement et alerter l'utilisateur** lors de l'export d'une nouvelle version.
