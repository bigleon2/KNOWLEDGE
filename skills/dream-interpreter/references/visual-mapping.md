# Correspondance images du rêve → éléments visuels

## Émotion → palette de couleurs

| Valeur mood | Émotion | Couleur dominante | Couleur d'appui | Fond |
|---------|------|------|------|------|
| anxious | anxiété/peur | #2D1B69 violet profond | #1A1A2E bleu sombre | dégradé sombre |
| peaceful | calme/heureux | #F4D35E jaune chaud | #83C5BE vert tendre | dégradé clair |
| sad | tristesse/abattement | #4A6FA5 bleu gris | #2D3142 gris profond | dégradé froid |
| surreal | fantastique/absurde | #FF006E rose néon | #8338EC violet électrique | fond sombre + touches néon |
| exciting | excitation/stimulation | #FF6B35 rouge orangé | #FFD700 or | dégradé chaud |
| nostalgic | nostalgie/tendresse | #DDA15E ambre | #BC6C25 brun chaud | dégradé en lumière douce |

## Image → élément visuel

Chaque élément visuel correspond à un module de dessin p5.js.

### Éléments naturels

| Mots-clés d'image | Valeur visual_element | Rendu p5.js |
|-----------|-------------------|------------|
| eau, mer, rivière, lac, nage | water_ripple | ondulations sinusoïdales diffuses depuis le bas |
| pluie | rain_drops | fines lignes de particules tombant du haut |
| feu, combustion | fire_particles | particules orange-rouge s'élevant |
| vent, tempête | wind_lines | écoulement de courbes horizontales |
| ciel étoilé, nuit | starfield | petits points lumineux scintillant aléatoirement |
| lune | moon_glow | halo circulaire pulsant lentement |
| soleil, lumière | sun_rays | rayons en éventail |
| forêt, arbres | tree_silhouettes | silhouettes d'arbres en pied de cadre |
| fleurs, jardin | floating_petals | formes de pétales tombant lentement |

### Espace / architecture

| Mots-clés d'image | Valeur visual_element | Rendu p5.js |
|-----------|-------------------|------------|
| tour, immeuble, high-rise | building | silhouette architecturale en lignes géométriques |
| pièce, intérieur | room_frame | cadre de pièce en traits en perspective |
| porte | door_shape | contour de porte au centre, ouverte/fermée possible |
| escaliers, marches | stairs | lignes de marches en progression |
| labyrinthe, couloir | maze_lines | tracés générés aléatoirement |
| pont | bridge_arc | silhouette de pont en arc |

### Actions / états

| Mots-clés d'image | Valeur visual_element | Rendu p5.js |
|-----------|-------------------|------------|
| chute, tomber | falling_particles | particules en accélération descendante |
| voler, flotter | rising_particles | particules en ascension lente |
| poursuite, fuite | speed_lines | lignes horizontales à grande vitesse |
| enfermé, encerclé | cage_lines | lignes d'enceinte se resserrant |
| être perdu | scattered_dots | points lumineux dérivant au hasard |

### Personnages / créatures

| Mots-clés d'image | Valeur visual_element | Rendu p5.js |
|-----------|-------------------|------------|
| personne, silhouette humaine | human_silhouette | silhouette humaine abstraite en fondu |
| foule | crowd_dots | petits cercles s'agrégeant et se dispersant |
| serpent | snake_curve | courbe en S ondulant lentement |
| chat/chien/animal | animal_shape | contour animalier stylisé |
| oiseau/créature volante | bird_flight | silhouette en V traversant l'écran |
| poisson/créature aquatique | fish_swim | ellipses glissant entre les ondulations |

### Ambiances

| Mots-clés d'image | Valeur visual_element | Rendu p5.js |
|-----------|-------------------|------------|
| obscurité, visibilité faible | dark_bg | faible luminosité globale + taches floues |
| flou, brume | blur_lights | points lumineux flous gaussiens |
| scintillement, instabilité | flicker_effect | luminosité globale fluctuant aléatoirement |
| rotation, vertige | spiral_motion | particules en mouvement spiralé |
| silence, vide | minimal_space | vastes espaces vides + très peu d'éléments |

## Règles de correspondance

1. Extraire de la description du rêve toutes les images identifiables
2. Chaque image correspond à un visual_element
3. Le tableau visual_elements compte au maximum 5 éléments (pour éviter une image surchargée)
4. Prioriser les images liées à l'intrigue principale
5. Inclure au minimum 1 élément d'ambiance
6. Le mood retient l'émotion la plus forte du rêve, color_scheme correspond au mood
