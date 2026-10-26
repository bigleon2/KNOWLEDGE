# Scène : CV / Résumé

## Objectif

Générer un CV complet, authentique, bien structuré, ciblé sur un poste et avec une mise en forme Word stable. Doit simultanément répondre aux critères :
- Contenu authentique et crédible, ciblage de poste clair
- Compatible avec les systèmes de suivi des candidatures (ATS), mise en page Word stable
- Structure propre, design visuel professionnel, facile à parcourir

**Priorité d'exécution** (en cas de conflit) : Pertinence du poste > Lisibilité de l'information > Compatibilité ATS > Décoration visuelle

**Interdit** : Produire uniquement des conseils / des fragments / des brouillons inachevés ; fournir des explications de style chat.

→ Profil de police : **B (Visuel)** — voir `references/common-rules.md`
→ Convention de placeholder et interdits universels — voir `references/common-rules.md`

---

## Portée

Par défaut : générer un CV général orienté poste. Passer au CV en anglais, CV académique, format international ou style portfolio uniquement lorsque l'utilisateur le demande explicitement.

---

## Routage de type de CV

Sélection automatique de l'ordre des modules en fonction du profil utilisateur et de la cible :

### CV général (par défaut)
Informations personnelles → Poste ciblé → Résumé de profil (optionnel) : Compétences clés → Expérience professionnelle → Projets → Formation → Certifications / Récompenses

### CV pour jeune diplômé
Informations personnelles → Poste ciblé → Formation → Expérience en stage → Projets → Activités universitaires / Compétitions / Récompenses → Compétences & Certifications

### CV pour poste technique
Informations personnelles → Orientation ciblée → Résumé de profil (optionnel) → Stack technique / Compétences clés → Expérience professionnelle → Projets → Formation → Open Source / Publications / Brevets / Compétitions

### CV académique
Informations personnelles → Axe de recherche / Cible → Formation → Expérience de recherche → Publications / Brevets / Projets / Subventions → Enseignement / Service académique → Récompenses / Compétences / Langues

---

## Règles de traitement des entrées

1. Si l'utilisateur fournit un poste ciblé ou une description de poste (JD) → **doit réorganiser et réécrire le contenu autour des exigences du poste**
2. Si l'utilisateur fournit un brouillon brut → prioriser la restructuration, l'amélioration de la formulation et le réordonnancement des priorités ; ne pas réécrire dans une carrière inconnue
3. **Jamais inventer** d'entreprises, de postes, de diplômes, de projets, de certifications, de récompenses, de publications, de brevets, de résultats de données ou de réalisations
4. Si des données critiques sont manquantes → utiliser des expressions conservatrices ou un placeholder `【Veuillez remplir : ______】` ; jamais inventer de nombres précis
5. Un seul CV doit généralement servir une seule direction de carrière principale

---

## Contraintes de qualité du contenu

### Principes fondamentaux
1. Le CV doit tourner autour du poste ciblé → ne pas répartir équitablement toutes les expériences
2. Les expériences, projets et compétences les plus pertinents doivent être **placés en premier et détaillés**
3. Terminologie, noms d'entreprise, titres de poste, formats de date et noms de compétences doivent être cohérents
4. Doit démontrer : **positionnement personnel → étiquettes de capacité → expérience pertinente → résultats vérifiables**
5. Pas d'accumulation de louanges vagues ; pas d'écriture inspirante ou de vidanges chronologiques

### Normes de rédaction d'expérience

Chaque élément d'expérience doit démontrer : **Action + Objet/Contexte + Méthode + Résultat/Impact**

**Verbes recommandés** : Mené, construit, piloté, optimisé, refactoré, conçu, livré, coordonné, amélioré, réduit, atteint

**Règles** :
- "Responsable de" / "participant à" ne sont pas absolument interdits, mais doivent inclure le périmètre et les résultats
- Chaque élément est concis → une contribution centrale par élément
- Quantifier lorsque possible, mais ne pas forcer la mise en gras de tous les nombres
- L'expérience récente est détaillée ; l'expérience peu pertinente/pas de valeur est compressée ou supprimée
- Ordre chronologique inversé → le plus récent et pertinent en premier
- Développer les 2 expériences les plus récentes ; compresser les plus anciennes

### Résumé de profil / Auto-évaluation
1. Non obligatoire
2. Si inclus, formater comme "Résumé de profil" → **maximum 3-4 lignes**
3. Se concentrer sur : années d'expérience, orientation de carrière, capacités fondamentales, réalisations représentatives, adéquation au poste
4. **Interdit** comme contenu principal : "travailleur acharné", "forte sens des responsabilités", "bon joueur d'équipe", "apprentissage rapide", "personnalité extravertie"

### Vérité & Contrôle des risques
1. Jamais inventer d'expériences, de réalisations, de formation, de récompenses ou de certifications
2. Jamais transformer "participant à" en "mené" sauf si les informations utilisateur le permettent
3. Jamais attribuer entièrement à l'individuel des résultats d'équipe
4. Jamais inventer de revenus, taux de conversion, effectif, budgets ou métriques techniques
5. Si aucune donnée disponible, utiliser des expressions mesurées : "amélioration de l'efficacité de livraison", "raccourcissement du cycle de traitement", "prise en charge du lancement du cœur de métier"

---

## Contrôle de longueur

| Type de candidat | Nombre de pages cible |
|----------------|---------------------|
| Jeune diplômé / <3 ans expérience | **1 page** |
| 3-10 ans expérience | 1-2 pages |
| Cadre supérieur / chercheur / CV académique | Peut dépasser 2 pages, mais doit maintenir une densité d'information |

**Règles de compression** :
- Expériences de plus de 5 ans avec faible pertinence doivent être compressées
- Expériences de plus de 10 ans et non pertinentes peuvent être omises
- Jamais gonfler les expériences peu valorisantes juste pour "paraître complet"

---

## Contraintes ATS & Structure

1. Les informations clés doivent être en texte brut → jamais dépendre d'images, d'icônes, de boîtes de texte ou d'en-têtes/pieds de page pour le contenu clé
2. Pas de graphiques intégrés, d'objets, de SmartArt ou de WordArt
3. Les descriptions d'expérience utilisent des symboles de puces cohérents → pas de numérotation automatique complexe
4. Les puces au sein du même poste doivent être compactes → pas d'excessive ligne blanche

**Équilibre mise en page tableau vs ATS** : Les 3 modèles visuels (A/B/C) utilisent des mises en page basées sur des tableaux pour la qualité visuelle Word. Dans des scénarios ATS stricts (l'utilisateur dit explicitement "priorité ATS"), préférer le Modèle B (mono-colonne) avec réduction de la dépendance aux tableaux. Par défaut : qualité visuelle en priorité.

---

## Nommage des modules

Utiliser uniquement des noms standards, universels, familiers des recruteurs :
- Informations personnelles, Poste ciblé, Résumé de profil, Compétences clés, Expérience professionnelle, Projets, Formation, Certifications, Récompenses, Langues

**Noms fantaisistes interdits** : "Mon parcours de croissance", "Auto-évaluation", "Moments brillants", "Mot de vie"

---

## Prévention des maladies de modèle

1. Ne pas inclure d'étiquettes d'identité non pertinentes (affiliation politique, ville natale, etc.) sauf demande explicite de l'utilisateur
2. Ne pas placer les modules de faible priorité (loisirs, langues, traits de personnalité) avant l'expérience professionnelle
3. Ne pas combiner lettre de motivation et CV dans un seul document (sauf demande explicite de l'utilisateur)
4. Ne pas laisser le modèle écraser les informations personnelles réelles
5. Ne pas laisser l'"auto-évaluation" occuper la zone d'or de la page (devrait venir après compétences/expérience clés)

---## Sélection de modèle

Trois modèles sont fournis, sélectionnés automatiquement en fonction des besoins de l'utilisateur :

| Modèle | Mise en page | Idéal pour | Style de couleur |
|--------|--------------|------------|------------------|
| A | Barre latérale gauche + corps droit | Usage général, postes techniques | Barre latérale gris foncé + barres de titre bleues |
| B | Bannière d'en-tête sombre + colonne unique | Contenu important / candidats seniors | En-tête bleu fondu + soulignements de titre |
| C | Barre latérale gauche + titres à ligne verticale | International / bilingue / entreprises étrangères | Barre latérale bleue + titres avec bordure gauche |

**Logique de sélection :**
- Par défaut : Modèle A
- Beaucoup de contenu (prévu > 1 page) → Modèle B (pas de barre latérale, meilleure utilisation de l'espace)
- L'utilisateur demande explicitement du bilingue / anglais → Modèle C

### Suggestions de couleurs par secteur

| Orientation de carrière | Arrière-plan barre latérale | Couleur d'accent | Modèle recommandé |
|------------------------|----------------------------|-----------------|-------------------|
| Tech / Internet | `#1A1F36` (bleu violet profond) | `#667eea` (améthyste) | A ou C |
| Finance / Conseil | `#0F2027` (bleu mer profond) | `#D4AF37` (doré) | A ou B |
| Design / Créatif | `#2D1B30` (violet profond) | `#f5576c` (corail rose) | A ou C |
| Éducation / Formation | `#1A3A3A` (vert foncé) | `#3CB4A0` (menthe verte) | A |
| Médical / Santé | `#0E2030` (cyan foncé) | `#3888A8` (bleu médical) | B |
| Général / Par défaut | `#303030` (neutre sombre chaud) | `#B89870` (accent chaud) | A |

Lorsque le secteur n'est pas spécifié, utilisez la palette neutre chaude par défaut. Cela correspond aux directives de profil visuel neutre-chaude dans `design-system.md`.

## Règles clés

- **Pas de page de couverture / PAS DE SOMMAIRE**
- **Cible : 1 page** (2 pages max pour les postes seniors)
- **Espacement compact** : `line: 276` (1.15x)
- Tous les modèles utilisent des **titres de section bilingues** (par exemple, "Work Experience 工作经历")

---

## Modèle A : Barre latérale gauche + barres de titre colorées

### Palette de couleurs
```js
const S = {
  bg: "3B4F5C",      // arrière-plan barre latérale (gris-bleu foncé)
  text: "D8E2E8",    // texte barre latérale
  label: "8BA0AD",   // texte secondaire barre latérale
  accent: "2F97B8",  // couleur d'accentuation (bleu-cyan)
  title: "1A2D38",   // titre corps
  body: "2C3E4A",    // contenu corps
  sec: "6B8592",     // informations secondaires (dates etc.)
};
```

### Structure de mise en page
```
┌──────────┬──────────────────────┐
│ [Photo]  │ ██ Profile ██        │  ← Barre de titre bleue
│          │ Texte du résumé...   │
│ Nom      │                      │
│ Fonction │ ██ Work Experience ██│
│          │ Société  Rôle  Date  │
│ ──────── │ ▸ Réalisation...     │
│ Info     │ ▸ Réalisation...     │
│ de base  │                      │
│          │ ██ Projects ██       │
│ ──────── │ ...                  │
│ Contact  │                      │
│          │ ██ Education ██      │
│ ──────── │ ...                  │
| Compétences |                      │
| Java ●●●●○│                     │
| Go   ●●●○○│                     │
│          │                      │
│ ──────── │                      │
| Certifs  │                      │
└──────────┴──────────────────────┘
     30%             70%
```

### Notes de mise en œuvre

**Configuration de la page :**
```js
page: { margin: { top: 0, bottom: 0, left: 0, right: 0 } }
// Utiliser Table pour simuler les colonnes : columnWidths: [3400, 8506]
// ⚠️ La hauteur de ligne doit utiliser "exact" avec marge de sécurité pour éviter le débordement
// Hauteur de ligne : height: { value: 16038, rule: "exact" }
// 16038 = 16838(hauteur A4) - 1200(marge de sécurité pour compatibilité multi-moteurs)
```

**Ordre des éléments de la barre latérale :**
1. Espace photo (rectangle + bordure, largeur 2400 DXA, hauteur 1800)
2. Nom (32pt gras blanc SimHei) + Fonction (18pt accent)
3. Info de base (date de naissance / diplôme / école)
4. Info de contact (téléphone / email / adresse)
5. Évaluations de compétences (nom + évaluation ●○, 5 niveaux chacun)
6. Liste des certificats

**Titres de section côté droit (style barre colorée) :**
```js
// Barre pleine largeur + texte chinois blanc + texte anglais plus clair
new Table({ columnWidths:[7600], rows:[new TableRow({ children:[
  new TableCell({
    shading: { fill: S.accent, type: ShadingType.CLEAR },
    margins: { top:40, bottom:40, left:200, right:100 },
    children: [new Paragraph({ children: [
      new TextRun({ text: "Work Experience  ", size:22, bold:true, color:"FFFFFF", font:"SimHei" }),
      new TextRun({ text: "Experience", size:18, color:"C8E8F0", font:"Times New Roman", italics:true }),
    ] })],
  })
] })] });
```

**Format d'entrée d'expérience :**
```js
// Ligne 1 : Société(gras) + Fonction(accent) + Date(aligné à droite)
new Paragraph({
  tabStops: [{ type: TabStopType.RIGHT, position: 7200 }],
  children: [
    new TextRun({ text: "Nom de l'entreprise", size:22, bold:true, color:S.title }),
    new TextRun({ text: "    Intitulé du poste", size:20, color:S.accent }),
    new TextRun({ text: "\t2023.06 — Présent", size:17, color:S.sec }),
  ]
});
// Ligne 2+ : ▸ puces
```

---

## Modèle B : Bannière d'en-tête sombre + colonne unique

### Palette de couleurs
```js
const C = {
  dark: "1A3352",    // arrière-plan en-tête (bleu foncé)
  accent: "2980B9",  // couleur d'accent
  title: "1A2636",   // titre
  body: "2C3E50",    // texte corps
  sec: "6B8599",     // informations secondaires
  light: "E8EFF5",   // arrière-plan clair
};
```

### Structure de mise en page
```
┌────────────────────────────────┐
│ ██████████████████████████████ │  ← Bannière d'arrière-plan bleu foncé
│ █  Nom    Fonction            █ │    Contient nom / fonction /
│ █  Téléphone | Email | Localité █ │    contact / info de base /
│ █  DN | Diplôme | École        █ │    date de naissance / diplôme / école
│ ██████████████████████████████ │
│                                │
│ Profile                        │  ← Titre souligné
│ ─────────────────────────────  │
│ Texte du résumé...             │
│                                │
│ Work Experience                │
│ ─────────────────────────────  │
│ Société | Rôle        Date     │
│ • Réalisation...               │
│ ...                            │
│                                │
│ Skills                         │
│ ─────────────────────────────  │
| Programmation ●●●●○  Java/Go/...│  ← Évaluation + détails
└────────────────────────────────┘
```

### Notes de mise en œuvre

**Bannière d'en-tête :**
```js
// Tableau une ligne une colonne, arrière-plan sombre, hauteur 2400 DXA
new Table({ columnWidths:[11906], rows:[new TableRow({
  height: { value:2400, rule:"exact" },
  children:[new TableCell({
    shading: { fill: C.dark },
    margins: { top:300, bottom:200, left:800, right:800 },
    verticalAlign: VerticalAlign.TOP, // Jamais utiliser CENTER dans les lignes de hauteur exacte (incompatible WPS)
    children: [
      // Ligne 1 : Nom(48pt blanc) + Fonction
      // Ligne 2 : Téléphone | Email | Localité
      // Ligne 3 : DN | Diplôme | École
    ]
  })]
})] });
```

**Titres de section (style souligné) :**
```js
new Paragraph({
  borders: { bottom: { style: BorderStyle.SINGLE, size: 2, color: C.accent } },
  children: [
    new TextRun({ text: "Work Experience", size:24, bold:true, color:C.accent, font:"SimHei" }),
    new TextRun({ text: "  Experience", size:18, color:C.sec, italics:true }),
  ]
});
```

**Affichage des compétences (évaluation + détails) :**
```js
// Nom(gras) + évaluation ●○ + liste d'outils spécifiques
new Paragraph({ children: [
  new TextRun({ text: "Programming  ", size:19, bold:true, color:C.title }),
  new TextRun({ text: "●●●●○  ", size:13, color:C.accent }),
  new TextRun({ text: "Java / Go / Python / TypeScript", size:18, color:C.sec }),
] });
```

---## Template C : Barre latérale bleue + Titres avec ligne verticale

### Palette de couleurs
```js
const C = {
  side: "4A7C8F",     // arrière-plan de la barre latérale (bleu-turquoise)
  text: "FFFFFF",     // texte de la barre latérale
  label: "A0C4D0",   // texte secondaire de la barre latérale
  accent: "357A8F",   // couleur d'accentuation
  dot: "2F8FAD",      // couleur de remplissage des points de compétences
  dotDim: "B8D4DE",   // couleur vide des points de compétences
  title: "1A3040",    // titre du corps
  body: "2C4050",     // contenu du corps
  sec: "6B8A98",      // informations secondaires
};
```

### Éléments spécifiques à la barre latérale

**Espace réservé pour photo circulaire :**
```js
new Paragraph({ alignment: AlignmentType.CENTER,
  children: [new TextRun({ text: "◯", size:80, color:C.label })]
});
```

**Matrice de compétence linguistique :**
```js
"Anglais  ● ● ● ● ○"
"Japonais ● ● ○ ○ ○"
```

**Titres de section côté droit (style bordure gauche) :**
```js
new Paragraph({
  borders: { left: { style: BorderStyle.SINGLE, size:8, color:C.accent, space:8 } },
  indent: { left: 120 },
  children: [
    new TextRun({ text: "Expérience professionnelle", size:24, bold:true, color:C.title, font:"SimHei" }),
    new TextRun({ text: "  Expérience", size:18, color:C.sec, italics:true }),
  ]
});
```

**Format d'entrée d'expérience (diffère de A) :**
```js
// Ligne 1 : Nom de l'entreprise (gras)
// Ligne 2 : Rôle (couleur d'accentuation) + Date
// Ligne 3+ : ▸ puces
```

---

## Règles universelles

### Spécifications de police
| Élément | Police | Taille | Style |
|---------|--------|--------|-------|
| Nom (barre latérale) | SimHei | 32pt (size:64) | Gras, blanc |
| Nom (en-tête) | SimHei | 24pt (size:48) | Gras, blanc |
| Titre de section | SimHei | 11pt (size:22) | Gras |
| Entreprise / École | Microsoft YaHei | 11pt (size:22) | Gras |
| Titre de fonction | Microsoft YaHei | 10pt (size:20) | couleur d'accentuation |
| Période | Microsoft YaHei | 8.5pt (size:17) | couleur secondaire |
| Description en puces | Microsoft YaHei | 9.5pt (size:19) | couleur du corps |
| Points de compétences | Par défaut | 6.5pt (size:13) | accent / couleurDim |

### Symboles de puce
- Template A / C : `▸` (petit triangle)
- Template B : `•` (point rond)

### Règles d'évaluation des compétences
- 1–5 niveaux utilisant des points ● remplis et ○ vides
- Une compétence par ligne, nom à gauche, points à droite
- Couleur du point rempli : accent ; couleur du point vide : couleurDim

### Logique de correspondance JD
Lorsque l'utilisateur fournit une description de poste :
1. Extraire les exigences clés (compétences, expérience, éducation)
2. Prioriser les éléments d'expérience correspondants en haut
3. Intégrer naturellement les mots-clés JD dans les descriptions
4. Mettre en évidence les compétences pertinentes

### Gestion multi-pages

- 1 page de contenu : Templates barre latérale (A/C) ou template mono-colonne (B)
- Plus de 1 page : Préférer Template B ; si utilisation de A/C, passer la page 2 en mise en page pleine largeur avec une barre de nom en haut (Nom | Titre)

⚠️ **Les CV multi-pages doivent utiliser une structure multi-sections :**

La page 1 et la page 2 doivent être des **sections différentes** pour un contrôle indépendant des marges et de la mise en page :

```js
sections: [
  {
    // Section page 1 — marge 0 (la mise en page barre latérale a besoin de pleine page)
    properties: { page: { margin: { top: 0, bottom: 0, left: 0, right: 0 } } },
    children: [page1Table],
  },
  {
    // Section page 2 — marges normales avec barre d'en-tête
    properties: { page: { margin: { top: 800, bottom: 600, left: 800, right: 800 } } },
    children: [pageHeader(name, title), ...page2Content],
  },
]
```

⚠️ **Gestion multi-pages du Template B :**

La bannière d'en-tête du Template B utilise une simulation de Tableau :
1. La `columnWidths` de la bannière doit être égale à la **largeur de la zone de contenu de la page** (pageWidth - marginLeft - marginRight), pas la pleine largeur de page
2. Si la bannière a besoin d'une pleine largeur de page → définir la marge de la section page 1 à 0, columnWidths de la bannière à 11906
3. Page 2+ doivent être des sections indépendantes, margin.top ≥ 800

⚠️ **Règles d'espacement en haut de la page 2+ (obligatoire) :**

1. **La marge page.top doit être ≥ 800 twips** (~1.4 cm), jamais 0
2. **La page 2+ a besoin d'une barre d'info d'en-tête :** barre concise `Nom | Titre`, hauteur ~400–600 twips, séparée du corps par un arrière-plan clair ou une ligne du bas
3. **Espacement de 200–300 twips entre la barre d'en-tête et le contenu du corps**
4. **Interdit : le contenu touchant très haut de la page 2**

```js
// Barre d'en-tête concise pour page 2+
function pageHeader(name, title) {
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    borders: { top: NB, left: NB, right: NB, insideHorizontal: NB, insideVertical: NB,
               bottom: { style: BorderStyle.SINGLE, size: 1, color: "D0D0D0" } },
    rows: [new TableRow({
      cantSplit: true,
      height: { value: 500, rule: "atLeast" },
      children: [new TableCell({
        margins: { top: 60, bottom: 60, left: 200, right: 200 },
        borders: { top: NB, left: NB, right: NB, bottom: NB },
        children: [new Paragraph({
          children: [
            new TextRun({ text: name, size: 20, bold: true, color: S.title || C.title }),
            new TextRun({ text: `  |  ${title}`, size: 18, color: S.sec || C.sec }),
          ]
        })],
      })],
    })],
  });
}
```

---

## Contrôles de qualité spécifiques à la scène

En plus des contrôles universels (voir `references/common-rules.md`) :

### Format
- [ ] Tient sur 1 page (senior ≤ 2 pages)
- [ ] **Taux de remplissage mono-page ≥ 85%** (espace blanc en bas ≤ 15%, ~2500 twips)
- [ ] Les titres de section sont bilingues
- [ ] Les points d'évaluation des compétences sont corrects (●○)
- [ ] L'expérience est en ordre chronologique inversé
- [ ] Pas de page de couverture, pas de sommaire
- [ ] Espacement des lignes 1.15x (line: 276)
- [ ] Pas de pages blanches supplémentaires
- [ ] **La hauteur de ligne de tableau utilise `rule: "exact"` avec valeur ≤ 16038** (empêcher le débordement de pages blanches)
- [ ] **Multi-page : la page 2+ a une barre d'info d'en-tête + espacement en haut approprié**

### Contenu
- [ ] Clair et organisé autour de la position cible
- [ ] Pas d'auto-évaluations vagues ("travailleur", "responsable", "joueur d'équipe")
- [ ] Pas de données fabriquées ou de résultats exagérés
- [ ] L'expérience la plus pertinente est placée en premier et détaillée
- [ ] Chaque puce démontre action + objet + méthode + résultat
- [ ] Pas de blocs narratifs longs / phrases excessivement longues / déséquilibre de densité d'information
- [ ] Les noms de module sont standardisés
- [ ] Les informations de contact sont en texte brut, bien positionnées
- [ ] La zone d'en-tête forme le centre visuel
- [ ] L'expérience professionnelle et les projets forment le corps principal visuel
- [ ] Le nombre de pages correspond au niveau de seniorité du candidat

### Règles de remplissage mono-page

Les CV mono-page doivent utiliser pleinement l'espace de la page — **un grand espace blanc en bas est interdit :**

1. Si le contenu est insuffisant → **agrandir proactivement :**
   - Ajouter des détails de projet, mots-clés de compétences, données de réalisation
   - Ajouter des modules supplémentaires : résumé de profil, intérêts, récompenses
2. Utiliser l'espacement de section (`spacing.before/after`) pour **répartir le contenu uniformément**
3. Templates barre latérale (A/C) : la hauteur de la barre latérale devrait approcher la pleine page
   - Si le contenu de la barre latérale est clairsemé, augmenter l'espacement des éléments
   - Ou ajouter des modules supplémentaires : "Langues", "Intérêts"
4. Évaluation : après génération, vérifier la position du dernier élément de contenu ; si >2500 twips du bas de page, ajuster
