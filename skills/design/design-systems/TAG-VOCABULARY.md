# Vocabulaire contrôlé des tags de marque

Les entrées `brand_inspiration` de `index.json` utilisent le vocabulaire contrôlé suivant pour un étiquetage multidimensionnel. **Pour ajouter ou modifier un tag de marque,
le terme doit être choisi dans cette table**, afin d'éviter l'éclatement en synonymes (comme « minimaliste / épuré / minimal ») qui provoquerait des ratés d'appariement lors de la recherche.

Le vocabulaire est dérivé du contenu réel des DESIGN.md des 89 marques, et aligné sur la conception
des dimensions du `template.json` de `deck-templates`.

---

## `industry` (secteur, tableau, ≥1)
IA · outils développeur · productivité/collaboration · finance/paiement · automobile · luxe · social/communication ·
e-commerce/retail · médias/édition · infrastructure/entreprise · électronique grand public/tech ·
contenu/outils créatifs · mobilité/vie locale · télécoms · documentation/éducation

## `product_type` (forme du produit, tableau, ≥1)
SaaS · site vitrine/page marketing · plateforme développeur · app grand public · plateforme de contenu ·
e-commerce/transaction · page de marque · page de lancement produit · site de documentation · portfolio/personnel

## `mood` (tempérament émotionnel, tableau, ≥2)
minimaliste · retenu · précision/ingénierie · technophile · luxueux · théâtral · dark natif · image d'abord ·
éditorial/magazine · chaleureux · accessible/amical · énergique/lumineux · contenu d'abord · corporate/digne de confiance ·
atmosphère en dégradés · illustration riche · rétro/espiègle · futuriste/science-fiction

Notes (distinctions de synonymes conservées volontairement, non fusionnées) :
- `minimaliste` = soustraction structurelle ; `retenu` = calme, sans éclat. Les deux peuvent coexister ou apparaître seuls.
- `précision/ingénierie` = visuel calibré avec exactitude ; `technophile` = tempérament code/développeur.

## Dimensions à valeur unique
- `formality` (niveau de formalité) : high / medium / low
- `density` (densité d'information) : high / medium / low
- `scheme` (clair/obscur) : light / dark / both
- `era` (époques) : rétro / moderne / futur

## Champs en langage naturel
- `best_for` : contextes les plus adaptés (une phrase)
- `avoid_for` : contextes inadaptés (une phrase)

---

## Usage en recherche
Filtrer `index.json` selon les dimensions du besoin → présélectionner des marques candidates → ne lire que les `DESIGN.md` des marques retenues pour obtenir les tokens complets et les règles.
Les dimensions de type tableau supportent le plusieurs-à-plusieurs : une marque peut correspondre à plusieurs valeurs d'une même dimension (ex. Stripe appartient à la fois à finance/paiement et à outils développeur).
