# Règles Communes

Règles partagées référencées par tous les fichiers de scène. Les substitutions spécifiques à la scène prévalent.

## Mise en Page par Défaut

A4 portrait. Sauf indication contraire de la scène, utiliser :

| Propriété | Valeur | Twips |
|----------|-------|-------|
| Largeur de page | 21.0 cm | 11906 |
| Hauteur de page | 29.7 cm | 16838 |
| Marge supérieure | 2.54 cm | 1440 |
| Marge inférieure | 2.54 cm | 1440 |
| Marge gauche | 3.0 cm | 1701 |
| Marge droite | 2.5 cm | 1417 |

```js
page: {
  size: { width: 11906, height: 16838, orientation: PageOrientation.PORTRAIT },
  margin: { top: 1440, bottom: 1440, left: 1701, right: 1417 },
}
```

**Substitutions de scène :**
- **Document officiel (GB/T 9704 en-tête rouge) :** sup 2098, inf 1984, gauche 1588, droite 1474
- **Examen :** sup/inf 1134 (2 cm), gauche/droite 1134 (2 cm)

## Spécifications de Police par Défaut

Deux profils de police existent. Chaque scène déclare quel profil elle utilise.

### Profil A : Formel (rapport, académique, contrat, document-officiel, examen)

| Élément | Police CN | Police EN | Taille | Notes |
|---------|---------|---------|------|-------|
| H1 | SimHei | Times New Roman | 16 pt (size: 32) | Gras, centré |
| H2 | SimHei | Times New Roman | 15 pt (size: 30) | Gras |
| H3 | SimHei | Times New Roman | 14 pt (size: 28) | Gras |
| Corps | SimSun | Times New Roman | 12 pt (size: 24) | |
| Légende | SimSun | Times New Roman | 10.5 pt (size: 21) | |

- Couleur du texte : toujours **noir pur `"000000"`** (jamais bleu-gris foncé)
- Retrait de première ligne : **480 twips** (2 caractères à SimSun 12pt)
- Espacement entre lignes : **312** (1.3x).
- **Routage des couleurs pour les documents non-rapport** : Lorsque le document est un texte court (essai, évaluation, lettre, discours, candidature, réflexion, etc.) plutôt qu'un rapport structuré/whitepaper/proposition/délivrance de conseil, la couleur de titre DOIT utiliser le noir pur `"000000"` au lieu de `palette.primary`. Les titres colorés sont réservés aux documents ayant besoin d'une identité de marque/professionnelle (rapports avec couvertures, whitepapers, propositions, livrables de conseil).

### Profil B : Visuel (CV, rédaction publicitaire)

| Élément | Police CN | Police EN | Taille |
|---------|---------|---------|------|
| Nom/Titre | Microsoft YaHei | Calibri | Variable |
| Corps | Microsoft YaHei | Calibri | 10–11 pt |
| Légende | Microsoft YaHei | Calibri | 9 pt |

- Retrait de première ligne : **420 twips** (2 caractères à YaHei)
- Couleur : selon la palette du système de design

### Substitution de Police pour Document Officiel (GB/T 9704)

Lorsque `needsRedHeader() = true` :

| Élément | Police | Taille |
|---------|------|------|
| Nom de l'organisation en-tête rouge | STXiaoBiaoSong (ou SimSun gras) | 26 pt (size: 52) |
| Titre | STXiaoBiaoSong (ou SimHei) | 22 pt (size: 44) |
| Corps | FangSong | 16 pt (size: 32) |
| Titre de section | FangSong_GB2312 gras (ou HeiTi) | 16 pt (size: 32) |

- Espacement entre lignes : **560** (28 pt fixe)
- Retrait de première ligne : **640 twips** (2 caractères à FangSong 16pt)

## Référence de Taille de Police Chinoise

| Nom | Points | Demi-points (size:) |
|------|--------|---------------------|
| Chu Hao (initial) | 42 | 84 |
| Xiao Chu | 36 | 72 |
| Yi Hao (1er) | 26 | 52 |
| Xiao Yi | 24 | 48 |
| Er Hao (2ème) | 22 | 44 |
| Xiao Er | 18 | 36 |
| San Hao (3ème) | 16 | 32 |
| Xiao San | 15 | 30 |
| Si Hao (4ème) | 14 | 28 |
| Xiao Si | 12 | 24 |
| Wu Hao (5ème) | 10.5 | 21 |
| Xiao Wu | 9 | 18 |
| Liu Hao (6ème) | 7.5 | 15 |

## Convention d'Espace Réservé

Lorsque des informations requises manquent, utiliser des espaces réservés standardisés afin que les utilisateurs puissent Rechercher & Remplacer dans Word.

**Format :** Toujours utiliser des crochets pleine-largeur `【 】`.

| Type | Format | Exemple |
|------|--------|---------|
| Champ général | `【nom du champ】` | Nom : 【nom de l'entreprise】 |
| Montant monétaire | `【RMB en lettres : yuan (minuscule : ¥)】` | Montant : 【RMB en lettres】 |
| Champ date | `【____/____/____】` | Date de signature : 【____/____/____】 |
| Long texte | `【Veuillez remplir : ______】` | Critères de livraison : 【Veuillez remplir : ______】 |
| Référence de pièce jointe | `【Voir Annexe 1 : ______】` | |

**Règles :**
1. Le format d'espace réservé doit être cohérent dans tout le document
2. Chaque espace réservé doit spécifier exactement ce qui est nécessaire (jamais utiliser "TBD" ou "à compléter" vague)
3. Jamais coder en dur des faits critiques non confirmés ; utiliser un espace réservé à la place
4. Jamais utiliser d'expressions négligées comme "à affiner", "omis", "rempli par l'utilisateur plus tard"

## Prévention des Orphelins de Titre (Toutes Scènes)

Les titres de corps (H1/H2/H3) et les titres de couverture doivent éviter de laisser 1-2 caractères seuls sur la dernière ligne. Cette règle s'applique à TOUS les types de documents.

**Pour les titres de couverture :** Toujours utiliser `calcTitleLayout()` + `splitTitleLines()` depuis `design-system.md` — ceux-ci gèrent automatiquement la prévention des orphelins (fusionnent les dernières lignes de ≤2 caractères dans la ligne précédente).

**Pour les titres de corps (H1/H2/H3) :** Lorsqu'un texte de titre est suffisamment long pour revenir à la ligne, appliquer la même logique `splitTitleLines()`. Si le titre causerait un orphelin d'un seul caractère dans le retour à la ligne automatique de Word, diviser manuellement en plusieurs éléments `TextRun` avec un `Break` (saut de ligne doux) à une limite sémantique.

```js
const { Break } = require("docx");

// Vérifier si le titre nécessite un saut de ligne manuel pour éviter l'orphelin
function buildHeadingRuns(text, maxCharsPerLine, runProps) {
  // Si le texte tient en une ligne, aucune action nécessaire
  if (text.length <= maxCharsPerLine) {
    return [new TextRun({ text, ...runProps })];
  }
  // Utiliser splitTitleLines pour trouver les points de rupture sémantiques
  const lines = splitTitleLines(text, maxCharsPerLine);
  const runs = [];
  for (let i = 0; i < lines.length; i++) {
    if (i > 0) runs.push(new TextRun({ break: 1, ...runProps, text: "" })); // saut de ligne doux
    runs.push(new TextRun({ text: lines[i], ...runProps }));
  }
  return runs;
}
```

**Estimation pour maxCharsPerLine :** Pour les titres centrés, estimer la largeur disponible = largeur de page - marge gauche - marge droite. Pour SimHei à une taille pt donnée, chaque caractère CJK ≈ pt × 20 twips de largeur. Diviser la largeur disponible par la largeur du caractère pour obtenir `maxCharsPerLine`.

---

## Prévention des Valeurs Undefined / Null (Obligatoire)

Le code généré DOIT se protéger contre l'affichage littéral de `undefined`, `null`, `NaN`, ou chaînes vides pour tout champ de texte visible. Ceci est une **exigence stricte** — ces valeurs sont jamais acceptables dans un document livré.

```js
// ✅ OBLIGATOIRE : Helper de texte sécurisé — utiliser pour TOUS les valeurs de texte utilisateur
function safeText(value, placeholder) {
  if (value === undefined || value === null || value === "" || String(value) === "NaN" || String(value) === "undefined") {
    return placeholder || "【Veuillez remplir】";
  }
  return String(value);
}

// Utilisation :
new TextRun({ text: safeText(config.contact, "【Personne contact】") })
new TextRun({ text: safeText(row.phone, "【Numéro de téléphone】") })
```

**Règles :**
1. Chaque `TextRun` affichant des données fournies par l'utilisateur ou dérivées de la configuration DOIT utiliser `safeText()` ou une protection équivalente
2. Si un champ est optionnel et non fourni, utiliser l'espace réservé `【Veuillez remplir : nom_champ】` (crochets pleine-largeur)
3. Cellules de tableau avec données manquantes : afficher `【Veuillez remplir】`, jamais laisser comme chaîne vide ou undefined
4. Ceci s'applique à TOUS les scènes — contrats, rapports, académique, examens, etc.

---## WPS / Office Word Compatibility (Obligatoire)

Les fichiers .docx générés doivent s'afficher de manière cohérente dans Microsoft Office Word et WPS Office. Les fonctionnalités OOXML suivantes présentent des problèmes de compatibilité connus — à éviter ou à utiliser avec prudence.

### Fonctionnalités à ÉVITER (risque de incompatibilité élevé)

| Fonctionnalité | Problème | Alternative |
|---------|-------|------------|
| **Lignes décoratives en texte** (par exemple, `───`, `━━━`, `═══`, `——————`) | Les lignes dessinées avec des caractères dépendent des métriques de police et du moteur de rendu — elles apparaissent de largeurs longueurs différentes dans MS Office vs WPS, souvent tronquées ou mal alignées. Elles ne peuvent pas s'étendre sur une largeur contrôlée. | **Utilisez toujours des bordures de paragraphe** (`border.top`, `border.bottom`) pour les lignes décoratives horizontales. Les bordures de paragraphe s'affichent de manière cohérente entre les moteurs et respectent le retrait pour un contrôle de largeur précis. Voir la recette R2 pour une mise en œuvre correcte. |
| **Bordures de table par défaut sur les tables d'enveloppe de couverture** (oubli de `allNoBorders`) | Les bordures de table par défaut de docx-js sont `single/auto/sz=4`. Sur l'enveloppe de couverture haute de 16838, ces bordures ajoutent environ 8 twips de hauteur supplémentaire par bord. MS Office inclut l'épaisseur de la bordure dans le calcul de la hauteur, provoquant un débordement de contenu de quelques twips → **page 2 blanche**. WPS est plus tolérant et peut absorber le débordement. | **Toute table d'enveloppe de couverture DOIT explicitement définir `borders: allNoBorders`** (les 6 positions de bordure = AUCUNE). Ne jamais se fier aux valeurs par défaut. Définissez la constante `allNoBorders` et utilisez-la de manière cohérente. |
| `verticalAlign: "center"` ou `"bottom"` dans TableRow de hauteur exacte | WPS ignore l'alignement vertical dans les lignes de hauteur exacte ; le contenu peut être coupé ou décalé | Utilisez `verticalAlign: "top"` + `spacing.before` pour positionner le contenu. Évitez `margins.top`/`margins.bottom` dans les cellules de hauteur exacte — elles réduisent la hauteur disponible de manière imprévisible entre les moteurs |
| `characterSpacing` (grandes valeurs) | WPS rend différemment de Word ; l'espacement des lettres peut s'effondrer ou se dilater | Gardez `characterSpacing` ≤ 80 ; pour les étiquettes anglaises de couverture, testez les deux moteurs de rendu |
| `margins.top`/`margins.bottom` à l'intérieur de cellules de hauteur exacte | MS Office et WPS calculent la hauteur restante différemment lorsque les marges de cellule sont présentes | Utilisez `spacing.before` sur le premier paragraphe pour le positionnement vertical ; n'utilisez que `margins.left`/`margins.right` |
| Tables complexes imbriquées à l'intérieur de cellules de hauteur exacte | Le calcul de hauteur de WPS diffère de Word ; le contenu peut déborder ou être coupé | Enveloppez tout dans une seule cellule externe 16838 (architecture R1). Les tables imbriquées à l'intérieur sont acceptables lorsque l'enveloppe externe fournit une sécurité |
| Police de grande taille sans `spacing.line` explicite | Le paragraphe hérite d'un petit espacement de ligne du document par défaut (par exemple, 560tw pour le corps) ; police plus haute que la hauteur de ligne → partie supérieure des caractères coupée | Définissez toujours `spacing: { line: fontPt * 23, lineRule: "atLeast" }` sur les paragraphes avec une taille de police > texte du corps |
| `ShadingType.SOLID` | WPS affiche du noir uni au lieu de la couleur prévue | Utilisez toujours `ShadingType.CLEAR` |
| XML brut OOXML pour les colonnes (`w:cols`) | Le rendu des colonnes de WPS peut différer | N'utilisez que lorsque nécessaire explicitement (examens A3) ; testez la sortie |
| `titlePage: true` avec en-têtes/pieds de page complexes | WPS peut ne pas supprimer correctement l'en-tête/pied de page de la première page | Utilisez des sections séparées au lieu du drapeau titlePage |
| Tabulations pour l'alignement | La largeur de tabulation de WPS peut différer de celle de Word | Utilisez des Tables sans bordure pour l'alignement à la place |

### Fonctionnalités SÛRES (rendu cohérent)

| Fonctionnalité | Notes |
|---------|-------|
| Tables sans bordure pour la mise en page | Les deux moteurs gèrent bien |
| `ShadingType.CLEAR` avec couleur de remplissage | Cohérent |
| `rule: "exact"` sur TableRow à un seul niveau | Fonctionne dans les deux (à éviter avec les Tables imbriquées) |
| Bordures de paragraphe (gauche, bas, etc.) | Cohérent |
| `spacing.before` / `spacing.after` | Cohérent |
| Polices standard (SimHei, SimSun, YaHei, TNR, Calibri) | Disponibles sur les deux plateformes |
| `PageBreak` à l'intérieur d'un Paragraphe | Cohérent |
| Sauts de section (`SectionType.NEXT_PAGE`) | Cohérent |

### Contrôles de Compatibilité Obligatoires (Post-Génération)

Ajoutez à l'auto-contrôle qualité :
- [ ] Aucun `ShadingType.SOLID` n'est utilisé (dans tout le codebase)
- [ ] Aucun `verticalAlign: "center"` ou `"bottom"` dans les lignes de hauteur exacte
- [ ] Aucun alignement par tabulation pour les informations du parti ou l'alignement des données (utilisez des Tables)
- [ ] Les couvertures utilisent l'architecture d'enveloppe externe 16838 (modèle R1) avec `spacing.before` pour le positionnement ; aucun `margins.top`/`margins.bottom` dans les cellules de hauteur exacte
- [ ] **La marge de section de couverture = `{ top: 0, bottom: 0, left: 0, right: 0 }`** — des marges non nulles font que l'enveloppe se réduit en s'éloignant des bords de la page
- [ ] **La ligne d'enveloppe de couverture a `height: { value: 16838, rule: "exact" }`** — sans cela, le contenu déborde ou laisse des espaces blancs
- [ ] **La couverture est dans une section séparée du contenu du corps** — couverture et corps ne doivent pas partager de section
- [ ] **La table d'enveloppe de couverture utilise `allNoBorders` explicite** — ne jamais se fier aux bordures de table par défaut (provoque une page 2 blanche dans MS Office)
- [ ] **Aucune ligne décorative en texte** (`───`, `━━━`, `═══`, `——————`) — utilisez des bordures de paragraphe à la place
- [ ] Les valeurs `characterSpacing` ≤ 80 partout
- [ ] SOMMAIRE : suivez la liste de contrôle de `references/toc.md` (style de titre, élément TableOfContents, PageBreak, script de post-traitement)
- [ ] Toutes les tables utilisent `WidthType.PERCENTAGE` pour les largeurs de colonne (bug tblGrid de WPS ; si DXA est inévitable, définissez `columnWidths` explicitement)

```js
// ✅ Correct — largeurs en pourcentage, compatible WPS
new Table({
  width: { size: 100, type: WidthType.PERCENTAGE },
  rows: [new TableRow({ children: [
    new TableCell({ width: { size: 30, type: WidthType.PERCENTAGE }, children: [...] }),
    new TableCell({ width: { size: 70, type: WidthType.PERCENTAGE }, children: [...] }),
  ]})],
});

// ❌ FAUX — largeurs DXA provoquent un tblGrid mismatch dans WPS (tous gridCol=100)
new TableCell({ width: { size: 3000, type: WidthType.DXA }, ... })
```

---

## Interdictions Universelles

Celles-ci s'appliquent à TOUS les scénarios. Les fichiers de scénario peuvent ajouter des interdictions spécifiques au scénario.

1. **Aucune structure uniquement en contours** — produisez toujours un document complet et fini
2. **Aucune sortie de style conversationnel** — le document ne doit pas ressembler à une conversation ou une explication
3. **Aucun faux SOMMAIRE / numéros de page / en-têtes** — utilisez les structures docx-js appropriées
4. **Aucune ligne blanche excessive** pour remplir la mise en page
5. **Aucun formatage sale** — aucune annotation parasite, fragment de modèle, hyperlien cassé, marqueurs illisibles
6. **Aucun placeholder négligent** — "TBD", "omis", "略 (lüè)", "à affiner" sont interdits ; utilisez des placeholders `【】` appropriés
7. **Aucune donnée fabriquée** — n'inventez pas de statistiques, citations, références juridiques ou faits pour paraître professionnel
8. **Aucune numérotation/titres incohérents** — un système de numérotation par document, sans saut de niveau
9. **Aucun artéfact Markdown** — aucun `#`, `**`, marqueurs de liste `-`, `>` citations en bloc et **aucune syntaxe de tableau Markdown** (`| col1 | col2 |`, `|---|---|`) dans le docx final. Toute donnée tabulaire DOIT être rendue comme un objet `Table` docx approprié — jamais comme des lignes de texte délimitées par des pipes. Ceci s'applique à TOUS les scénarios y compris les tableaux de données d'examens, statistiques de rapport et tables de résultats académiques.
10. **Aucun document en liste à puces** — le texte du corps doit être des paragraphes appropriés, pas des puces interminables## Format de Lettre / Correspondance (Universel)

Lors de la génération de tout document de type lettre (lettre d'invitation, lettre de remerciement, lettre de motivation, lettre de recommandation, dissertation en anglais au format lettre, etc.), les règles de mise en page suivantes s'appliquent quelle que soit la scène :

1. **La formule de politesse et le nom de l'expéditeur DOIVENT être alignés à droite** — par exemple, "Yours sincerely,", "Best regards,", "Yours,", et le nom de l'expéditeur en dessous doivent utiliser `alignment: AlignmentType.RIGHT`
2. **Date** — si placée en haut de la lettre, alignée à droite ; si en bas, alignée à droite avec la formule de politesse
3. **Formule d'appel** ("Dear Mr. Smith," / "Dear Mike,") — alignée à gauche, suivie d'une ligne vide ou de `spacing.after`
4. **Paragraphes du corps** — alignés à gauche (anglais) ou justifiés (chinois coréen japonais), avec un `spacing.after` approprié entre les paragraphes

```js
// ✅ Correct — formule de politesse et nom de l'expéditeur alignés à droite
new Paragraph({ alignment: AlignmentType.RIGHT, spacing: { before: 400 },
  children: [new TextRun({ text: "Yours sincerely,", size: 24 })] }),
new Paragraph({ alignment: AlignmentType.RIGHT,
  children: [new TextRun({ text: "Li Hua", size: 24 })] }),

// ❌ FAUX — formule de politesse alignée à gauche (par défaut)
new Paragraph({
  children: [new TextRun({ text: "Yours sincerely," })] }),
```

## Auto-contrôle Qualité (Universel)

→ Voir **SKILL.md § Post-Génération — Vérification en Deux Couches** pour la liste de contrôle complète.

Les fichiers de scène ajoutent des vérifications spécifiques à la scène par-dessus cette liste de contrôle universelle.

## Priorité d'Exécution

Lorsque les règles entrent en conflit, suivre cet ordre de priorité (le plus élevé en premier) :

1. **Modèle fourni par l'utilisateur ou instructions explicites** — écrasent toujours les valeurs par défaut
2. **Règles spécifiques à la scène** — écrasent les règles communes et les valeurs par défaut du système de design
3. **Règles communes** (ce fichier) — écrasent les valeurs par défaut esthétiques du système de design
4. **Valeurs par défaut du système de design** — esthétique de base

## Recettes de Couverture

Voir `references/design-system.md` pour les 7 recettes de couverture validées (R1–R7) et 14 palettes de couleurs.

Sélection de la recette de couverture : `selectCoverRecipe(docType, industry, titleLength)` — définie dans `references/design-system.md` (source autoritaire).

---

## Règles de Mise en Page du Titre de Couverture (Obligatoire)

Ces règles s'appliquent à TOUTES les recettes de couverture (R1–R7). Elles empêchent les problèmes de qualité de couverture les plus courants : débordement du titre, contenu qui déborde sur la page 2, et sauts de ligne au milieu de mots.

### Règle 1 : Toujours utiliser `calcTitleLayout()`

Toute couverture DOIT appeler `calcTitleLayout(title, availableWidth)` depuis `design-system.md` pour déterminer :
- **Taille de police** (calculée dynamiquement, jamais codée en dur au-dessus de 40pt)
- **Sauts de ligne** (sémantiques, jamais au milieu de mots)

**Interdit :** Passer le titre complet comme un seul long TextRun et laisser Word faire le retour automatique. Cela provoque des sauts de ligne incontrôlés à des positions de caractères arbitraires.

### Règle 2 : Pas de lignes orphelines d'un seul caractère

Si la dernière ligne d'un titre ne contient que 1-2 caractères, la fusionner avec la ligne précédente. La fonction `splitTitleLines()` gère cela automatiquement.

### Règle 3 : Pas de césures de mots pour le texte CJK

Les sauts de ligne doivent se produire aux limites sémantiques : après des particules (par exemple, de/yu/he/ji/zhi), de la ponctuation, des connecteurs, des espaces ou des underscores. Jamais séparer un terme composé (par exemple, un terme de 4 caractères comme une spécification de gestion ne doit pas être divisé en 3+1 caractères).

Pour les titres mixtes chinois+anglais (par exemple, "Jiyu Transformer jiegou de..." — "Basé sur l'architecture Transformer..."), utiliser `estimateTextWidth()` au lieu du nombre de caractères pour le calcul des sauts de ligne. Les caractères chinois sont environ 2× plus larges que les caractères anglais à la même taille de police.

### Règle 4 : Maximum 3 lignes de titre sur la couverture

Les titres de couverture ne doivent pas dépasser 3 lignes. Si le titre est trop long, réduire la taille de police (jusqu'à un minimum de 24pt) avant d'ajouter plus de lignes. S'il dépasse toujours 3 lignes à 24pt, forcer 3 lignes avec des longueurs de ligne plus longues.

### Règle 5 : Toujours utiliser `calcCoverSpacing()` pour l'espacement

Les valeurs d'espacement (`spacing.before`) dans les éléments de couverture doivent être calculées dynamiquement, pas codées en dur. Des valeurs fixes comme `before: 4500` supposent une longueur de titre spécifique et provoqueront un débordement avec des titres plus longs.

### Règle 6 : Validation du budget de hauteur de couverture

Avant la génération, vérifier que la hauteur totale du contenu reste dans les 15638 twips (hauteur de page 16838 moins une marge de sécurité de 1200 twips — MS Office rend les polices grandes plus hautes que calculées). Chaque recette dans `design-system.md` inclut des annotations de budget de hauteur — vérifier pendant la génération.

### Règle 7 : Tableau de méta-informations R5 (couvertures académiques)

La méta-information académique de couverture DOIT utiliser un tableau à 2 colonnes avec des largeurs en pourcentage SEULEMENT (PAS en DXA — WPS ne fonctionne pas avec les largeurs DXA) :
- **Largeur du tableau** : adaptative 55–75% de la page, calculée par `calcR5MetaLayout()` dans `design-system.md`. Le tableau est centré via `alignment: CENTER`.
- **Colonne d'étiquettes** : adaptative 25–45% de la largeur du tableau, **alignée à GAUCHE**, texte d'étiquette simple + "：". PAS de remplissage d'espace pleine largeur, PAS d'alignement à droite, PAS d'alignement distribué.
- **Colonne de valeurs** : pourcentage restant, **alignée à GAUCHE**, `bottom border single sz=4` = soulignement de longueur fixe (même longueur pour toutes les lignes quelle que soit la longueur du texte de valeur).
- **Bordures de la colonne d'étiquettes** : aucune (PAS de bordure inférieure sur les cellules d'étiquette).
- ⚠️ N'utilisez PAS de largeurs DXA, de remplissage d'espace pleine largeur (`\u3000`), de colonnes d'espacement ou de tabulations — ces éléments rendent de manière incohérente entre MS Office et WPS.

### Règle 8 : Les paragraphes avec une grande police DOIVENT définir un espacement de ligne explicite

Lorsqu'un paragraphe utilise une taille de police plus grande que le texte du corps du document (par exemple, les titres de couverture à 36pt+), il DOIT définir un `spacing.line` explicite pour éviter le rognage. Sans cela, le paragraphe hérite de l'espacement de ligne par défaut du document/style (souvent 560 twips pour le texte du corps), qui est plus petit que la hauteur de police → le haut des caractères est rogné.

**Formule :** `spacing.line = Math.ceil(fontPt * 23)` avec `lineRule: "atLeast"`

**Exemple :** Un titre de 36pt a besoin de `spacing: { line: 828, lineRule: "atLeast" }`. Sans cela, l'héritage `line=560` rogne les 160 twips supérieurs du texte.

Cela s'applique à TOUS les paragraphes à grande police (titres de couverture, titres de chapitre, texte décoratif), pas seulement aux couvertures.

### Règle 9 : Chaque TextRun sur un arrière-plan coloré DOIT définir une `color` explicite

⚠️ **CRUCIAL :** Lorsqu'un TextRun se à l'intérieur d'une cellule/zone avec un arrière-plan foncé ou coloré (ombrage), il DOIT définir explicitement la propriété `color`. Omettre `color` met par défaut à noir (`#000000`), qui est invisible sur les arrière-plans foncés.

**Erreur courante :** Sous-titre ou méta-texte sur les blocs de couverture foncée R1/R2/R4 sans `color` → apparaît comme texte noir invisible sur fond sombre.

**Règle :** Pour tout TextRun à l'intérieur d'une cellule ombrée :
- Utiliser `P.cover.titleColor` pour le texte du titre
- Utiliser `P.cover.subtitleColor` pour le texte du sous-titre
- Utiliser `P.cover.metaColor` pour le texte de méta-information
- Utiliser `P.cover.footerColor` pour le texte de pied de page
- **JAMAIS** se fier à la couleur par défaut lorsque l'arrière-plan n'est pas blanc

### Règle 10 : Imbrication de l'API de numérotation de page et numérotation en 3 sections

⚠️ **CRUCIAL :** Les paramètres de numérotation de page DOIVENT être imbriqués dans `page.pageNumbers` :

```js
// ❌ FAUX — docx-js ignore les pageNumberStart/pageNumberFormatType de niveau supérieur
properties: { pageNumberStart: 1, pageNumberFormatType: NumberFormat.DECIMAL }

// ✅ CORRECT
properties: { page: { pageNumbers: { start: 1, formatType: NumberFormat.DECIMAL } } }
```

**Numérotation de page standard (convention en 5 zones) :**

Tous les documents multi-sections DOIVENT suivre ce schéma de numérotation de page en cinq zones, sauf si l'utilisateur le demande explicitement autrement.

| Zone | Section | pageNumbers | Footer instrText | Notes |
|------|---------|-------------|-----------------|-------|
| 1. Couverture | Page de titre | Aucune (pas de pied de page) | — | Toujours page logique 1, mais le numéro est **masqué** |
| 2. Matière préliminaire | Résumé, Table des matières, Préface | `{ start: 1, formatType: UPPER_ROMAN }` | `PAGE \* ROMAN \* MERGEFORMAT` | Séquence indépendante de chiffres romains (i, ii, iii…) |
| 3. Corps | Contenu principal | `{ start: 1, formatType: DECIMAL }` | `PAGE \* arabic \* MERGEFORMAT` | **Réinitialisé à 1** |
| 4. Annexe | Annexes (A, B, C…) | Continue le corps (pas de réinitialisation) | Même que le corps | Pas de saut de section nécessaire sauf en-têtes différents requis |
| 5. Références | Bibliographie | Continue le corps (pas de réinitialisation) | Même que le corps | Si le corps se termine à la p.42, les références continuent à la p.43 |

**Règles clés :**
0. **JAMAIS utiliser le format dénominateur "Page X de Y".** Le pied de page ne doit afficher que le numéro de page actuel (par exemple, `1`, `2`, `iii`). NE PAS afficher le nombre total de pages. Aucun `Page 3 of 12`, aucun `3 / 12`, aucun `di3 ye/gong 12 ye`. Juste le numéro seul. `PageNumber.TOTAL_PAGES` / `NUMPAGES` est **INTERDIT** dans les pieds de page.
1. **La couverture est toujours la page 1 en interne** mais le numéro de page n'est jamais affiché. Supprimer le pied de page dans la section couverture.
2. **La matière préliminaire utilise des chiffres romains indépendants** commençant à `i`. Cette séquence est séparée du corps.
3. **Le corps est réinitialisé à 1 arabe.** La première page du contenu principal est toujours la page `1`.
4. **L'annexe et les références continuent la séquence du corps.** Pas de réinitialisation entre corps → annexe → références.
5. **Documents sans matière préliminaire** passent la zone 2 (couverture masquée, corps commence à 1 arabe).
6. **Documents sans couverture** commencent le corps (ou matière préliminaire) directement à la page 1.
7. **Documents courts (≤3 pages)** : simple numérotation arabe 1, 2, 3 tout au long, pas de distinction couverture/matière préliminaire.
8. **Documents d'une seule page** (certificats, lettres) : aucune numérotation de page du tout.

**Implémentation docx-js en 3 sections (pour les documents avec table des matières) :**

Au minimum, implémenter les zones 1–3 comme des sections docx séparées :

```js
// Section 1 : Couverture — pas de numéro de page
properties: { page: { /* pas de pageNumbers */ } }
// Pas de enfants de pied de page, ou pied de page vide

// Section 2 : Matière préliminaire — chiffres romains
properties: { page: { pageNumbers: { start: 1, formatType: NumberFormat.UPPER_ROMAN } } }
// Pied de page : PAGE \* ROMAN \* MERGEFORMAT

// Section 3 : Corps — arabe, réinitialisé à 1
properties: { page: { pageNumbers: { start: 1, formatType: NumberFormat.DECIMAL } } }
// Pied de page : PAGE \* arabic \* MERGEFORMAT

// Annexe et Références : même section que le corps (continue la numérotation)
// Créer une nouvelle section seulement si un contenu d'en-tête/pied de page différent est nécessaire
```

**Post-traitement requis** (compatibilité WPS) :
1. Supprimer `<w:pgNumType/>` vide du XML de la section couverture
2. Corriger le pied de page instrText : remplacer `PAGE` nu par `PAGE \* ROMAN` ou `PAGE \* arabic` spécifique au format

Voir `toc.md` § API de Numérotation de Page pour les détails complets.
