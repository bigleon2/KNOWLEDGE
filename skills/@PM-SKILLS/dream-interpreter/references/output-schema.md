# Schéma JSON de sortie

Format JSON complet du résultat d'interprétation. Le frontend rend selon ce format la "carte d'interprétation du rêve"。

## Structure complète

```json
{
  "dream_summary": "string — résumé du rêve en une phrase (20 caractères max)",
  "keywords": ["string — mots-clés du rêve, 3-6"],
  "mood": "string — classification d'humeur, valeurs d'énumération ci-dessous",
  "color_scheme": "string — nom du schéma de couleurs, correspond à mood",
  "visual_elements": ["string — identifiants d'éléments visuels, 5 max, voir visual-mapping.md"],
  "interpretations": {
    "zhouGong": {
      "icon": "🔮",
      "title": "Interprétation des rêves selon Zhou Gong",
      "content": "string — interprétation principale, 100-200 caractères",
      "fortune": "string — verdict de fortune : grand auspice/auspice/neutre/neutre-inauspice/inauspice",
      "advice": "string — conseil en une phrase, format prescriptions/interdictions"
    },
    "freud": {
      "icon": "🧠",
      "title": "Analyse psychologique",
      "content": "string — analyse psychologique, 100-200 caractères",
      "insight": "string — insight clé en une phrase",
      "advice": "string — un conseil concret d'auto-prise en charge"
    },
    "cyber": {
      "icon": "🌀",
      "title": "Mage cyber",
      "content": "string — interprétation cyber, 100-200 caractères",
      "prediction": "string — une prophétie délirante",
      "advice": "string — un conseil d'action drôle mais concret"
    }
  },
  "overall_advice": "string — conseil global, 1-2 phrases, ton neutre",
  "shareable_text": "string — texte partageable avec emoji, adapté aux Moments, 50 caractères max"
}
```

## mood valeurs d'énumération

| Valeur | Signification |
|----|------|
| anxious | anxiété, peur, tension |
| peaceful | calme, beauté, confort |
| sad | tristesse, perte, regret |
| surreal | fantastique, absurde, surréaliste |
| exciting | excitation, adrénaline, aventure |
| nostalgic | nostalgie, douceur, manque |

## color_scheme correspondance avec mood

mood et color_scheme ont la même valeur. Le frontend prend les couleurs de color_scheme depuis la palette de visual-mapping.md selon sa valeur.

## Exigences de sortie

1. JSON doit être valide, directement JSON.parse
2. Utiliser ```json pour envelopper
3. aucun champ string ne doit être vide
4. keywords : tableau de 3-6 éléments
5. visual_elements : tableau de 1-5 éléments
6. les content des trois interpretation gardent des longueurs proches (tous 100-200 caractères)
7. shareable_text doit être amusant, donner envie de partager
