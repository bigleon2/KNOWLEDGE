---
name: audio-metadata
version: 1.0.0
category: metier
language: fr
description: >
  Gestion avancée des métadonnées audio — Extraction, normalisation, conversion  de tags ID3v2, MP4, FLAC, Vorbis. Supporte les formats DJ (MP3, FLAC, WAV, AIFF, M4A). Use when the user needs to manage audio metadata, extract tags, or normalize  metadata across a collection.
  
tags: []
dependencies: []
date: 2026-06-21
description-fr: Gestion avancée des métadonnées audio — Extraction, normalisation, conversion de tags ID3v2, MP4, FLAC, Vorbis. Supporte les formats DJ (MP3, FLAC, WAV, AIFF, M4A). Utiliser quand l'utilisateur a besoin de gérer des métadonnées audio, extraire des tags, ou normaliser les métadonnées d'une collection.
---

# audio-metadata

## Description

Skill de gestion avancée des métadonnées audio pour DJ et production musicale.

## Capacités

### 1. Extraction de Métadonnées
- Lecture de tous les formats de tags (ID3v1, ID3v2, MP4, FLAC, Vorbis)
- Extraction BPM, clé, genre, artiste, titre, album
- Extraction de couvertures d'album (pochettes)
- Extraction de commentaires et notes

### 2. Normalisation
- Standardisation des formats de tags
- Correction des encodages de caractères (UTF-8)
- Normalisation des noms d'artistes et titres
- Standardisation des genres musicaux

### 3. Conversion de Formats
- Conversion ID3v1 → ID3v2
- Conversion MP4 → ID3v2
- Conversion FLAC → Vorbis
- Préservation des métadonnées lors de la conversion

### 4. Écriture de Métadonnées
- Écriture de tags dans tous les formats
- Ajout de couvertures d'album
- Ajout de commentaires et notes
- Mise à jour batch de métadonnées

### 5. Analyse et Rapport
- Génération de rapports de métadonnées
- Détection de métadonnées manquantes
- Statistiques de collection (genres, années, BPM)
- Export en CSV/JSON/PDF

## Bibliothèques Python Utilisées

### mutagen
```python
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TBPM

# Lecture
audio = MP3('track.mp3', ID3=ID3)
title = audio.tags['TIT2'].text[0]
artist = audio.tags['TPE1'].text[0]
bpm = audio.tags['TBPM'].text[0]

# Écriture
audio.tags.add(TIT2(encoding=3, text='Nouveau Titre'))
audio.save()
```

### eyed3
```python
import eyed3

# Lecture
audiofile = eyed3.load('track.mp3')
tag = audiofile.tag
print(tag.title, tag.artist, tag.album)

# Écriture
tag.title = 'Nouveau Titre'
tag.artist = 'Nouvel Artiste'
tag.save()
```

### tinytag
```python
from tinytag import TinyTag

# Lecture rapide
tag = TinyTag.get('track.mp3')
print(tag.title, tag.artist, tag.album, tag.duration)
```

## Scripts Python Typiques

### Script 1 : Extraction de Toutes les Métadonnées
```python
#!/usr/bin/env python3
"""Extraction complète des métadonnées d'une collection"""
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from pathlib import Path
import json

def extract_metadata(directory):
    """Extrait toutes les métadonnées d'une collection"""
    results = []
    
    for audio_file in Path(directory).glob('*.*'):
        if audio_file.suffix == '.mp3':
            try:
                audio = MP3(audio_file)
                metadata = {
                    'file': audio_file.name,
                    'title': audio.tags.get('TIT2', [''])[0] if audio.tags else '',
                    'artist': audio.tags.get('TPE1', [''])[0] if audio.tags else '',
                    'album': audio.tags.get('TALB', [''])[0] if audio.tags else '',
                    'bpm': audio.tags.get('TBPM', [''])[0] if audio.tags else '',
                    'duration': audio.info.length
                }
                results.append(metadata)
            except Exception as e:
                print(f"Erreur {audio_file}: {e}")
        
        elif audio_file.suffix == '.flac':
            try:
                audio = FLAC(audio_file)
                metadata = {
                    'file': audio_file.name,
                    'title': audio.get('title', [''])[0],
                    'artist': audio.get('artist', [''])[0],
                    'album': audio.get('album', [''])[0],
                    'bpm': audio.get('bpm', [''])[0],
                    'duration': audio.info.length
                }
                results.append(metadata)
            except Exception as e:
                print(f"Erreur {audio_file}: {e}")
    
    return results

if __name__ == '__main__':
    metadata = extract_metadata('/home/z/music/traktor')
    
    # Export JSON
    with open('metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Extrait {len(metadata)} fichiers")
```

### Script 2 : Normalisation des Métadonnées
```python
#!/usr/bin/env python3
"""Normalisation des métadonnées d'une collection"""
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from pathlib import Path

def normalize_metadata(directory):
    """Normalise les métadonnées (UTF-8, formatage)"""
    for audio_file in Path(directory).glob('*.mp3'):
        try:
            audio = MP3(audio_file, ID3=ID3)
            
            # Normaliser les titres
            if 'TIT2' in audio.tags:
                title = audio.tags['TIT2'].text[0]
                # Supprimer les espaces multiples
                title = ' '.join(title.split())
                # Capitalisation
                title = title.title()
                audio.tags['TIT2'].text = [title]
            
            # Normaliser les artistes
            if 'TPE1' in audio.tags:
                artist = audio.tags['TPE1'].text[0]
                artist = ' '.join(artist.split())
                audio.tags['TPE1'].text = [artist]
            
            # Sauvegarder avec UTF-8
            audio.save(v2_version=4)
            
        except Exception as e:
            print(f"Erreur {audio_file}: {e}")

if __name__ == '__main__':
    normalize_metadata('/home/z/music/traktor')
    print("Normalisation terminée")
```

### Script 3 : Rapport de Métadonnées Manquantes
```python
#!/usr/bin/env python3
"""Rapport des métadonnées manquantes"""
from mutagen.mp3 import MP3
from pathlib import Path

def report_missing_metadata(directory):
    """Génère un rapport des métadonnées manquantes"""
    missing = []
    
    for audio_file in Path(directory).glob('*.mp3'):
        try:
            audio = MP3(audio_file)
            tags = audio.tags
            
            missing_fields = []
            
            if not tags or 'TIT2' not in tags:
                missing_fields.append('title')
            if not tags or 'TPE1' not in tags:
                missing_fields.append('artist')
            if not tags or 'TALB' not in tags:
                missing_fields.append('album')
            if not tags or 'TBPM' not in tags:
                missing_fields.append('bpm')
            
            if missing_fields:
                missing.append({
                    'file': audio_file.name,
                    'missing': missing_fields
                })
        
        except Exception as e:
            print(f"Erreur {audio_file}: {e}")
    
    return missing

if __name__ == '__main__':
    missing = report_missing_metadata('/home/z/music/traktor')
    
    print(f"Fichiers avec métadonnées manquantes : {len(missing)}")
    for item in missing[:10]:
        print(f"  {item['file']}: {', '.join(item['missing'])}")
```

## Intégration avec Autres Skills

- **auto-tagger** : Utilise les scripts d'extraction de métadonnées
- **traktor-automation** : Intégration avec TRAKTOR
- **pdf-expert** : Génération de rapports
- **python-executor** : Exécution des scripts

## Cas d'Usage

1. "Extrais toutes les métadonnées de ma collection"
2. "Normalise les tags de mes fichiers MP3"
3. "Trouve les fichiers sans BPM"
4. "Converti les tags ID3v1 en ID3v2"
5. "Génère un rapport des métadonnées manquantes"

## Déclenches

- "extrais les métadonnées"
- "normalise les tags"
- "gestion métadonnées audio"
- "rapport métadonnées"
- "conversion tags"

---

**Skill créé le 2026-06-21 pour François — DJ TRAKTOR**