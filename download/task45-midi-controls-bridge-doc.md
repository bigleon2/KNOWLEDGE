# MIDI Controls bridge — délégation par deck (Traktor 3.11.1 / Kontrol S4 MK2)

## 1. Introduction

Ce document décrit en détail le fonctionnement du mapping MIDI « MIDI Controls bridge — délégation par deck (Traktor 3.11.1 / Kontrol S4 MK2) » pour le contrôleur **Traktor Kontrol S4 MK2** sous **TRAKTOR PRO 3.11**. Il est généré automatiquement par le skill midi-doc-expert à partir du fichier de mapping source, puis validé mécaniquement (couverture complète). Le vocabulaire MIDI utilisé — note (message NOTE), CC (Control Change, message de commande continue), canal (CHANNEL, voie MIDI 0-15) et mode (Interaction Mode : Direct, Toggle, Increment…) — est défini à sa première occurrence afin d'être accessible sans prérequis.

## 2. Vue d'ensemble du mapping

Le device « Traktor Kontrol S4 MK2 » dialogue avec Traktor via les ports Traktor Kontrol S4 MK2 In (entrée) et Traktor Kontrol S4 MK2 Out (sortie), avec pour cible de deck Focus. Le mapping compte **56 affectations** : 48 entrées (commandes) et 8 sorties (retours d'état LED). Aucune couche logique (mapping mono-couche).

**Bridge MIDI Controls détecté** : ce mapping exploite les commandes génériques Global > MIDI Controls (MIDI Button/Knob/Fader, IDs 850-873 — Interaktiv Audio, https://interaktivaudio.com/traktor-commands, CC BY 4.0) comme relais : 8 boutons, 8 knobs, 8 faders. Le pont fonctionne en deux étages : l'étage 1 (canal 0) reçoit le MIDI du contrôleur externe vers les commandes génériques ; l'étage 2 (canal 1 — bus virtuel des MIDI Controls) délègue ces mêmes événements aux commandes de deck réelles, en réplique du pattern « In | Deck X | Direct | X.Filter » de l'Assignment Table, selon la convention 1-4 = deck gauche / 5-8 = deck droit (looprituals.de).

## 3. Activation / Désactivation

Ce mapping n'utilise pas de couche logique conditionnée : toutes les commandes sont actives en permanence.

## 4. Contrôle des Slices

Aucune affectation de slices conditionnée dans ce mapping (pas de couche FREEZE).

## 5. Réglages avancés

Le contrôle « Bridge entrée — MIDI Button 1 (CC80) » (CC 80, canal 0, mode Direct) attaque la commande générique **MIDI Button 1** (relais bridge). Le mode Direct transmet la valeur absolue du contrôle (0-127). Actif en couche BASE.

Le contrôle « Bridge entrée — MIDI Button 2 (CC81) » (CC 81, canal 0, mode Direct) attaque la commande générique **MIDI Button 2** (relais bridge). Le mode Direct transmet la valeur absolue du contrôle (0-127). Actif en couche BASE.

Le contrôle « Bridge entrée — MIDI Button 3 (CC82) » (CC 82, canal 0, mode Direct) attaque la commande générique **MIDI Button 3** (relais bridge). Le mode Direct transmet la valeur absolue du contrôle (0-127). Actif en couche BASE.

Le contrôle « Bridge entrée — MIDI Button 4 (CC83) » (CC 83, canal 0, mode Direct) attaque la commande générique **MIDI Button 4** (relais bridge). Le mode Direct transmet la valeur absolue du contrôle (0-127). Actif en couche BASE.

Le bouton « Bridge entrée — MIDI Button 5 (CC84) » (CC 84, canal 0, mode Toggle) commute **MIDI Button 5**. Le mode Toggle bascule l'état (on/off) à chaque appui. Actif en couche BASE.

Le bouton « Bridge entrée — MIDI Button 6 (CC85) » (CC 85, canal 0, mode Toggle) commute **MIDI Button 6**. Le mode Toggle bascule l'état (on/off) à chaque appui. Actif en couche BASE.

Le bouton « Bridge entrée — MIDI Button 7 (CC86) » (CC 86, canal 0, mode Toggle) commute **MIDI Button 7**. Le mode Toggle bascule l'état (on/off) à chaque appui. Actif en couche BASE.

Le bouton « Bridge entrée — MIDI Button 8 (CC87) » (CC 87, canal 0, mode Toggle) commute **MIDI Button 8**. Le mode Toggle bascule l'état (on/off) à chaque appui. Actif en couche BASE.

Le contrôle « Bridge entrée — MIDI Knob 1 (CC88) » (CC 88, canal 0, mode Direct) attaque la commande générique **MIDI Knob 1** (relais bridge). Le mode Direct transmet la valeur absolue du contrôle (0-127). Actif en couche BASE.

Le contrôle « Bridge entrée — MIDI Knob 2 (CC89) » (CC 89, canal 0, mode Direct) attaque la commande générique **MIDI Knob 2** (relais bridge). Le mode Direct transmet la valeur absolue du contrôle (0-127). Actif en couche BASE.

Le contrôle « Bridge entrée — MIDI Knob 3 (CC90) » (CC 90, canal 0, mode Direct) attaque la commande générique **MIDI Knob 3** (relais bridge). Le mode Direct transmet la valeur absolue du contrôle (0-127). Actif en couche BASE.

Le contrôle « Bridge entrée — MIDI Knob 4 (CC91) » (CC 91, canal 0, mode Direct) attaque la commande générique **MIDI Knob 4** (relais bridge). Le mode Direct transmet la valeur absolue du contrôle (0-127). Actif en couche BASE.

Le contrôle « Bridge entrée — MIDI Knob 5 (CC92) » (CC 92, canal 0, mode Direct) attaque la commande générique **MIDI Knob 5** (relais bridge). Le mode Direct transmet la valeur absolue du contrôle (0-127). Actif en couche BASE.

Le contrôle « Bridge entrée — MIDI Knob 6 (CC93) » (CC 93, canal 0, mode Direct) attaque la commande générique **MIDI Knob 6** (relais bridge). Le mode Direct transmet la valeur absolue du contrôle (0-127). Actif en couche BASE.

Le contrôle « Bridge entrée — MIDI Knob 7 (CC94) » (CC 94, canal 0, mode Direct) attaque la commande générique **MIDI Knob 7** (relais bridge). Le mode Direct transmet la valeur absolue du contrôle (0-127). Actif en couche BASE.

Le contrôle « Bridge entrée — MIDI Knob 8 (CC95) » (CC 95, canal 0, mode Direct) attaque la commande générique **MIDI Knob 8** (relais bridge). Le mode Direct transmet la valeur absolue du contrôle (0-127). Actif en couche BASE.

Le contrôle « Bridge entrée — MIDI Fader 1 (CC96) » (CC 96, canal 0, mode Direct) attaque la commande générique **MIDI Fader 1** (relais bridge). Le mode Direct transmet la valeur absolue du contrôle (0-127). Actif en couche BASE.

Le contrôle « Bridge entrée — MIDI Fader 2 (CC97) » (CC 97, canal 0, mode Direct) attaque la commande générique **MIDI Fader 2** (relais bridge). Le mode Direct transmet la valeur absolue du contrôle (0-127). Actif en couche BASE.

Le contrôle « Bridge entrée — MIDI Fader 3 (CC98) » (CC 98, canal 0, mode Direct) attaque la commande générique **MIDI Fader 3** (relais bridge). Le mode Direct transmet la valeur absolue du contrôle (0-127). Actif en couche BASE.

Le contrôle « Bridge entrée — MIDI Fader 4 (CC99) » (CC 99, canal 0, mode Direct) attaque la commande générique **MIDI Fader 4** (relais bridge). Le mode Direct transmet la valeur absolue du contrôle (0-127). Actif en couche BASE.

Le contrôle « Bridge entrée — MIDI Fader 5 (CC100) » (CC 100, canal 0, mode Direct) attaque la commande générique **MIDI Fader 5** (relais bridge). Le mode Direct transmet la valeur absolue du contrôle (0-127). Actif en couche BASE.

Le contrôle « Bridge entrée — MIDI Fader 6 (CC101) » (CC 101, canal 0, mode Direct) attaque la commande générique **MIDI Fader 6** (relais bridge). Le mode Direct transmet la valeur absolue du contrôle (0-127). Actif en couche BASE.

Le contrôle « Bridge entrée — MIDI Fader 7 (CC102) » (CC 102, canal 0, mode Direct) attaque la commande générique **MIDI Fader 7** (relais bridge). Le mode Direct transmet la valeur absolue du contrôle (0-127). Actif en couche BASE.

Le contrôle « Bridge entrée — MIDI Fader 8 (CC103) » (CC 103, canal 0, mode Direct) attaque la commande générique **MIDI Fader 8** (relais bridge). Le mode Direct transmet la valeur absolue du contrôle (0-127). Actif en couche BASE.

Le contrôle « Délégation Mixer FX Adjust — Deck A (A.Filter) ← MIDI Button 1 » (CC 80, canal 1, mode Direct) ajuste **Mixer FX Adjust** en valeur absolue (mode Direct, 0-127). Actif en couche BASE.

Le contrôle « Délégation Mixer FX Adjust — Deck B (B.Filter) ← MIDI Button 2 » (CC 81, canal 1, mode Direct) ajuste **Mixer FX Adjust** en valeur absolue (mode Direct, 0-127). Actif en couche BASE.

Le contrôle « Délégation Mixer FX Adjust — Deck C (C.Filter) ← MIDI Button 3 » (CC 82, canal 1, mode Direct) ajuste **Mixer FX Adjust** en valeur absolue (mode Direct, 0-127). Actif en couche BASE.

Le contrôle « Délégation Mixer FX Adjust — Deck D (D.Filter) ← MIDI Button 4 » (CC 83, canal 1, mode Direct) ajuste **Mixer FX Adjust** en valeur absolue (mode Direct, 0-127). Actif en couche BASE.

Le bouton « Délégation Mixer FX On — Deck A (A.MixerFX On) ← MIDI Button 5 » (CC 84, canal 1, mode Toggle) commute **Mixer FX On**. Le mode Toggle bascule l'état (on/off) à chaque appui. Actif en couche BASE.

Le bouton « Délégation Mixer FX On — Deck B (B.MixerFX On) ← MIDI Button 6 » (CC 85, canal 1, mode Toggle) commute **Mixer FX On**. Le mode Toggle bascule l'état (on/off) à chaque appui. Actif en couche BASE.

Le bouton « Délégation Mixer FX On — Deck C (C.MixerFX On) ← MIDI Button 7 » (CC 86, canal 1, mode Toggle) commute **Mixer FX On**. Le mode Toggle bascule l'état (on/off) à chaque appui. Actif en couche BASE.

Le bouton « Délégation Mixer FX On — Deck D (D.MixerFX On) ← MIDI Button 8 » (CC 87, canal 1, mode Toggle) commute **Mixer FX On**. Le mode Toggle bascule l'état (on/off) à chaque appui. Actif en couche BASE.

Le contrôle « Délégation Low Adjust — Deck A (A.Low) ← MIDI Knob 1 » (CC 88, canal 1, mode Direct) ajuste **Low Adjust** en valeur absolue (mode Direct, 0-127). Actif en couche BASE.

Le contrôle « Délégation High Adjust — Deck A (A.High) ← MIDI Knob 2 » (CC 89, canal 1, mode Direct) ajuste **High Adjust** en valeur absolue (mode Direct, 0-127). Actif en couche BASE.

Le contrôle « Délégation Low Adjust — Deck C (C.Low) ← MIDI Knob 3 » (CC 90, canal 1, mode Direct) ajuste **Low Adjust** en valeur absolue (mode Direct, 0-127). Actif en couche BASE.

Le contrôle « Délégation High Adjust — Deck C (C.High) ← MIDI Knob 4 » (CC 91, canal 1, mode Direct) ajuste **High Adjust** en valeur absolue (mode Direct, 0-127). Actif en couche BASE.

Le contrôle « Délégation Low Adjust — Deck B (B.Low) ← MIDI Knob 5 » (CC 92, canal 1, mode Direct) ajuste **Low Adjust** en valeur absolue (mode Direct, 0-127). Actif en couche BASE.

Le contrôle « Délégation High Adjust — Deck B (B.High) ← MIDI Knob 6 » (CC 93, canal 1, mode Direct) ajuste **High Adjust** en valeur absolue (mode Direct, 0-127). Actif en couche BASE.

Le contrôle « Délégation Low Adjust — Deck D (D.Low) ← MIDI Knob 7 » (CC 94, canal 1, mode Direct) ajuste **Low Adjust** en valeur absolue (mode Direct, 0-127). Actif en couche BASE.

Le contrôle « Délégation High Adjust — Deck D (D.High) ← MIDI Knob 8 » (CC 95, canal 1, mode Direct) ajuste **High Adjust** en valeur absolue (mode Direct, 0-127). Actif en couche BASE.

Le contrôle « Délégation Tempo Adjust — Deck A (A.Tempo) ← MIDI Fader 1 » (CC 96, canal 1, mode Direct) ajuste **Tempo Adjust** en valeur absolue (mode Direct, 0-127). Actif en couche BASE.

Le contrôle « Délégation Volume Adjust — Deck A (A.Volume) ← MIDI Fader 2 » (CC 97, canal 1, mode Direct) ajuste **Volume Adjust** en valeur absolue (mode Direct, 0-127). Actif en couche BASE.

Le contrôle « Délégation Tempo Adjust — Deck C (C.Tempo) ← MIDI Fader 3 » (CC 98, canal 1, mode Direct) ajuste **Tempo Adjust** en valeur absolue (mode Direct, 0-127). Actif en couche BASE.

Le contrôle « Délégation Volume Adjust — Deck C (C.Volume) ← MIDI Fader 4 » (CC 99, canal 1, mode Direct) ajuste **Volume Adjust** en valeur absolue (mode Direct, 0-127). Actif en couche BASE.

Le contrôle « Délégation Tempo Adjust — Deck B (B.Tempo) ← MIDI Fader 5 » (CC 100, canal 1, mode Direct) ajuste **Tempo Adjust** en valeur absolue (mode Direct, 0-127). Actif en couche BASE.

Le contrôle « Délégation Volume Adjust — Deck B (B.Volume) ← MIDI Fader 6 » (CC 101, canal 1, mode Direct) ajuste **Volume Adjust** en valeur absolue (mode Direct, 0-127). Actif en couche BASE.

Le contrôle « Délégation Tempo Adjust — Deck D (D.Tempo) ← MIDI Fader 7 » (CC 102, canal 1, mode Direct) ajuste **Tempo Adjust** en valeur absolue (mode Direct, 0-127). Actif en couche BASE.

Le contrôle « Délégation Volume Adjust — Deck D (D.Volume) ← MIDI Fader 8 » (CC 103, canal 1, mode Direct) ajuste **Volume Adjust** en valeur absolue (mode Direct, 0-127). Actif en couche BASE.

## 6. Tableau de Référence MIDI

| Affectation | Groupe | Commande | Sens | Message MIDI | Canal | Mode | Couche |
|---|---|---|---|---|---|---|---|
| Délégation High Adjust — Deck A (A.High) ← MIDI Knob 2 | Deck A | High Adjust | IN | CC 89 | ch 1 | Direct | BASE |
| Délégation Low Adjust — Deck A (A.Low) ← MIDI Knob 1 | Deck A | Low Adjust | IN | CC 88 | ch 1 | Direct | BASE |
| Délégation Mixer FX Adjust — Deck A (A.Filter) ← MIDI Button 1 | Deck A | Mixer FX Adjust | IN | CC 80 | ch 1 | Direct | BASE |
| Délégation Mixer FX On — Deck A (A.MixerFX On) ← MIDI Button 5 | Deck A | Mixer FX On | IN | CC 84 | ch 1 | Toggle | BASE |
| Délégation Tempo Adjust — Deck A (A.Tempo) ← MIDI Fader 1 | Deck A | Tempo Adjust | IN | CC 96 | ch 1 | Direct | BASE |
| Délégation Volume Adjust — Deck A (A.Volume) ← MIDI Fader 2 | Deck A | Volume Adjust | IN | CC 97 | ch 1 | Direct | BASE |
| Délégation High Adjust — Deck B (B.High) ← MIDI Knob 6 | Deck B | High Adjust | IN | CC 93 | ch 1 | Direct | BASE |
| Délégation Low Adjust — Deck B (B.Low) ← MIDI Knob 5 | Deck B | Low Adjust | IN | CC 92 | ch 1 | Direct | BASE |
| Délégation Mixer FX Adjust — Deck B (B.Filter) ← MIDI Button 2 | Deck B | Mixer FX Adjust | IN | CC 81 | ch 1 | Direct | BASE |
| Délégation Mixer FX On — Deck B (B.MixerFX On) ← MIDI Button 6 | Deck B | Mixer FX On | IN | CC 85 | ch 1 | Toggle | BASE |
| Délégation Tempo Adjust — Deck B (B.Tempo) ← MIDI Fader 5 | Deck B | Tempo Adjust | IN | CC 100 | ch 1 | Direct | BASE |
| Délégation Volume Adjust — Deck B (B.Volume) ← MIDI Fader 6 | Deck B | Volume Adjust | IN | CC 101 | ch 1 | Direct | BASE |
| Délégation High Adjust — Deck C (C.High) ← MIDI Knob 4 | Deck C | High Adjust | IN | CC 91 | ch 1 | Direct | BASE |
| Délégation Low Adjust — Deck C (C.Low) ← MIDI Knob 3 | Deck C | Low Adjust | IN | CC 90 | ch 1 | Direct | BASE |
| Délégation Mixer FX Adjust — Deck C (C.Filter) ← MIDI Button 3 | Deck C | Mixer FX Adjust | IN | CC 82 | ch 1 | Direct | BASE |
| Délégation Mixer FX On — Deck C (C.MixerFX On) ← MIDI Button 7 | Deck C | Mixer FX On | IN | CC 86 | ch 1 | Toggle | BASE |
| Délégation Tempo Adjust — Deck C (C.Tempo) ← MIDI Fader 3 | Deck C | Tempo Adjust | IN | CC 98 | ch 1 | Direct | BASE |
| Délégation Volume Adjust — Deck C (C.Volume) ← MIDI Fader 4 | Deck C | Volume Adjust | IN | CC 99 | ch 1 | Direct | BASE |
| Délégation High Adjust — Deck D (D.High) ← MIDI Knob 8 | Deck D | High Adjust | IN | CC 95 | ch 1 | Direct | BASE |
| Délégation Low Adjust — Deck D (D.Low) ← MIDI Knob 7 | Deck D | Low Adjust | IN | CC 94 | ch 1 | Direct | BASE |
| Délégation Mixer FX Adjust — Deck D (D.Filter) ← MIDI Button 4 | Deck D | Mixer FX Adjust | IN | CC 83 | ch 1 | Direct | BASE |
| Délégation Mixer FX On — Deck D (D.MixerFX On) ← MIDI Button 8 | Deck D | Mixer FX On | IN | CC 87 | ch 1 | Toggle | BASE |
| Délégation Tempo Adjust — Deck D (D.Tempo) ← MIDI Fader 7 | Deck D | Tempo Adjust | IN | CC 102 | ch 1 | Direct | BASE |
| Délégation Volume Adjust — Deck D (D.Volume) ← MIDI Fader 8 | Deck D | Volume Adjust | IN | CC 103 | ch 1 | Direct | BASE |
| Bridge entrée — MIDI Button 1 (CC80) | Global | MIDI Button 1 | IN | CC 80 | ch 0 | Direct | BASE |
| Bridge entrée — MIDI Button 2 (CC81) | Global | MIDI Button 2 | IN | CC 81 | ch 0 | Direct | BASE |
| Bridge entrée — MIDI Button 3 (CC82) | Global | MIDI Button 3 | IN | CC 82 | ch 0 | Direct | BASE |
| Bridge entrée — MIDI Button 4 (CC83) | Global | MIDI Button 4 | IN | CC 83 | ch 0 | Direct | BASE |
| Bridge entrée — MIDI Button 5 (CC84) | Global | MIDI Button 5 | IN | CC 84 | ch 0 | Toggle | BASE |
| Bridge entrée — MIDI Button 6 (CC85) | Global | MIDI Button 6 | IN | CC 85 | ch 0 | Toggle | BASE |
| Bridge entrée — MIDI Button 7 (CC86) | Global | MIDI Button 7 | IN | CC 86 | ch 0 | Toggle | BASE |
| Bridge entrée — MIDI Button 8 (CC87) | Global | MIDI Button 8 | IN | CC 87 | ch 0 | Toggle | BASE |
| Bridge entrée — MIDI Fader 1 (CC96) | Global | MIDI Fader 1 | IN | CC 96 | ch 0 | Direct | BASE |
| Bridge entrée — MIDI Fader 2 (CC97) | Global | MIDI Fader 2 | IN | CC 97 | ch 0 | Direct | BASE |
| Bridge entrée — MIDI Fader 3 (CC98) | Global | MIDI Fader 3 | IN | CC 98 | ch 0 | Direct | BASE |
| Bridge entrée — MIDI Fader 4 (CC99) | Global | MIDI Fader 4 | IN | CC 99 | ch 0 | Direct | BASE |
| Bridge entrée — MIDI Fader 5 (CC100) | Global | MIDI Fader 5 | IN | CC 100 | ch 0 | Direct | BASE |
| Bridge entrée — MIDI Fader 6 (CC101) | Global | MIDI Fader 6 | IN | CC 101 | ch 0 | Direct | BASE |
| Bridge entrée — MIDI Fader 7 (CC102) | Global | MIDI Fader 7 | IN | CC 102 | ch 0 | Direct | BASE |
| Bridge entrée — MIDI Fader 8 (CC103) | Global | MIDI Fader 8 | IN | CC 103 | ch 0 | Direct | BASE |
| Bridge entrée — MIDI Knob 1 (CC88) | Global | MIDI Knob 1 | IN | CC 88 | ch 0 | Direct | BASE |
| Bridge entrée — MIDI Knob 2 (CC89) | Global | MIDI Knob 2 | IN | CC 89 | ch 0 | Direct | BASE |
| Bridge entrée — MIDI Knob 3 (CC90) | Global | MIDI Knob 3 | IN | CC 90 | ch 0 | Direct | BASE |
| Bridge entrée — MIDI Knob 4 (CC91) | Global | MIDI Knob 4 | IN | CC 91 | ch 0 | Direct | BASE |
| Bridge entrée — MIDI Knob 5 (CC92) | Global | MIDI Knob 5 | IN | CC 92 | ch 0 | Direct | BASE |
| Bridge entrée — MIDI Knob 6 (CC93) | Global | MIDI Knob 6 | IN | CC 93 | ch 0 | Direct | BASE |
| Bridge entrée — MIDI Knob 7 (CC94) | Global | MIDI Knob 7 | IN | CC 94 | ch 0 | Direct | BASE |
| Bridge entrée — MIDI Knob 8 (CC95) | Global | MIDI Knob 8 | IN | CC 95 | ch 0 | Direct | BASE |
| LED retour — MIDI Button 1 | Global | MIDI Button 1 | OUT | — | ch — | — | BASE |
| LED retour — MIDI Button 2 | Global | MIDI Button 2 | OUT | — | ch — | — | BASE |
| LED retour — MIDI Button 3 | Global | MIDI Button 3 | OUT | — | ch — | — | BASE |
| LED retour — MIDI Button 4 | Global | MIDI Button 4 | OUT | — | ch — | — | BASE |
| LED retour — MIDI Button 5 | Global | MIDI Button 5 | OUT | — | ch — | — | BASE |
| LED retour — MIDI Button 6 | Global | MIDI Button 6 | OUT | — | ch — | — | BASE |
| LED retour — MIDI Button 7 | Global | MIDI Button 7 | OUT | — | ch — | — | BASE |
| LED retour — MIDI Button 8 | Global | MIDI Button 8 | OUT | — | ch — | — | BASE |

## 7. Modes de sortie

Les sorties (TYPE=OUT, 8 affectation(s)) restituent l'état logiciel sur les LED du contrôleur : chaque LED porte son numéro de note, ses valeurs ON (allumée) et OFF (éteinte), et le mode Output (émission d'état). Les LED conditionnées ne s'allument que dans leur couche.

## 8. États des LED

- **LED retour — MIDI Button 1** — note 80 : OFF (0) par défaut, ON (127) lorsque l'état porté par « MIDI Button 1 » est actif.
- **LED retour — MIDI Button 2** — note 81 : OFF (0) par défaut, ON (127) lorsque l'état porté par « MIDI Button 2 » est actif.
- **LED retour — MIDI Button 3** — note 82 : OFF (0) par défaut, ON (127) lorsque l'état porté par « MIDI Button 3 » est actif.
- **LED retour — MIDI Button 4** — note 83 : OFF (0) par défaut, ON (127) lorsque l'état porté par « MIDI Button 4 » est actif.
- **LED retour — MIDI Button 5** — note 84 : OFF (0) par défaut, ON (127) lorsque l'état porté par « MIDI Button 5 » est actif.
- **LED retour — MIDI Button 6** — note 85 : OFF (0) par défaut, ON (127) lorsque l'état porté par « MIDI Button 6 » est actif.
- **LED retour — MIDI Button 7** — note 86 : OFF (0) par défaut, ON (127) lorsque l'état porté par « MIDI Button 7 » est actif.
- **LED retour — MIDI Button 8** — note 87 : OFF (0) par défaut, ON (127) lorsque l'état porté par « MIDI Button 8 » est actif.

## 9. Annexes

Calibration : les numéros MIDI proviennent du référentiel de référence du projet (statut « à calibrer », R-1/R-2 — spec §8) ; ils sont remplaçables par les valeurs d'un TSI réel sans changement de pipeline. 
Sources : articles Native Instruments (Controller Manager, Generic MIDI), reverse-engineering public du format TSI (IvanZ 2014), mappings TSI tiers documentés (cible S4 MK2, analyse DJTT v2.1.0), documentation PyMuPDF/pymupdf4llm (chaîne PDF aval). Format PDF : généré en aval via le skill plateforme pdf.
