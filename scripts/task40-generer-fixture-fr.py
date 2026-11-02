#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.18)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

"""task40-generer-fixture-fr.py — Régénère la fixture « Mapping Speech-fr.pdf » (batterie analyse-doc-s4mk2 v1.2.0).

Contexte Task 40 (G1/SG1.2) : la fixture historique (traduction française de
« Mapping Speech.pdf », PDFium 2026, consignée SKILL.md §Échantillon secondaire) a
été perdue au recyclage du sandbox — aucun script persisté n'existait (lacune Task
34, résorbée ici). Le ZIP propriétaire re-uploadé ne contient que 2 PDF ; TF-07/08/09
en exigent 3. Ce script régénère la traduction française via la chaîne PyMuPDF
(même famille que la chaîne PDF du skill midi-doc-expert — R4) : structure PDF
simple, flux non compressés + ToUnicode bfchar lisibles par analyser-pdf-mk2.py.

Traduction fidèle (Drew, 2018) — termes DJ techniques conservés en anglais
(mapping, shift, deck, button, knob, modifier, FX) conformément au pivot lexical
du module de cohérence coherence-non-tsi-mk2.py.

Conventions script-creator : stdlib + pymupdf (chaîne plateforme), idempotent ×2
(fitz.Story + métadonnées sans date volatile — re-jeu byte-identique vérifié).
"""
import hashlib
from pathlib import Path

import fitz  # PyMuPDF

DEPUIS = Path("/home/z/my-project/scripts/zip-tsi/extracted-drew/"
              "Kontrol S4  [DREW's MAPPING] - FX4(JogWheel ) + Mode Freeze + Etc")
CIBLE = DEPUIS / "Mapping Speech-fr.pdf"

PARAGRAPHES = [
    "Voici mon cadeau aux utilisateurs de Traktor Pro 2 / S4. En tant que DJ adulte débutant et plein d'ambition, j'ai trouvé mon Traktor Pro 2 / S4 chez Guitar Center. Je l'ai acheté et je me suis bien amusé avec le mapping par défaut. Je l'ai trouvé assez facile à utiliser, et j'aime vraiment l'interface utilisateur. Il manque quelques fonctions tactiles, mais l'affichage est propre, facile à comprendre et professionnel. C'est aussi vrai du mapping par défaut du S4 MKII : le contrôleur est propre, facile à comprendre et professionnel. Certaines capacités manquent, et on découvre que le problème ne vient pas du matériel. Alors, naturellement, j'ai décidé de programmer mon propre mapping. Et là, la vraie fête a commencé !!!",
    "Au début, j'ai fait beaucoup de choses pour apprendre Traktor et la programmation d'un contrôleur. J'ai fait des recherches, regardé des vidéos YouTube, utilisé des recherches web ciblées. J'ai essayé certains des mappings disponibles que j'ai pu trouver (principalement via DJ Tech Tools. Mec ! J'adore ce site !). J'ai eu mes épreuves et mes tribulations, tant personnelles que liées à Traktor, mais j'ai continué de travailler à la compréhension du controller editor intégré à Traktor Pro 2 lui-même. Je donne le meilleur de ma motivation depuis plus de 4 ans maintenant. À ce stade, j'avoue que je ne comprends pas comment Native Instruments peut attendre de ses utilisateurs moyens qu'ils deviennent des DJ Traktor professionnels alors qu'ils se battent avec son logiciel. Je peux seulement espérer que Traktor 3 a fait du chemin.",
    "Après quelques échecs à construire un système complet de contrôle par shift dans un mapping de Pro 2, j'ai enfin compris ce que je devais faire. Il y a eu de nombreux sacrifices par rapport à ce que je voulais dans mon mapping, et quelques leçons apprises. J'ai créé ce système de contrôle par shift en monopolisant 3 modifiers complets : un modifier pour chaque côté du contrôleur, et un troisième pour les relier entre eux. J'ai un peu l'impression d'avoir triché le système, comme si on ne devait pas pouvoir programmer le contrôleur pour qu'il soit aussi fonctionnel. (Désolé de le dire, mais j'ai l'impression que Native Instruments essayait un peu de brider mon imagination.) Avec mon mapping, le contrôleur peut maintenant se trouver dans 12 états différents. Cela signifie que chaque button et chaque knob peut avoir plus de 12 fonctions différentes. OH ! Chaque knob, à l'exception d'un seul : le maudit knob de volume principal. Franchement ? Bref, je ne peux pas vous dire à quel point j'étais heureux quand ça a enfin fonctionné pour moi. Et bonus : ceci est le user mapping (par opposition au midi mapping). C'est un départ propre, il ne se bat pas avec le mapping par défaut. Peu m'importe les messages d'erreur tant que le mapping fait ce qu'il doit. Si vous êtes perdus, vous pouvez appuyer sur un button shift et revenir aux contrôles principaux du deck (deck A/C ou deck B/D). Attention : si vous n'êtes pas perdus, appuyer sur shift vous ramènera quand même aux contrôles principaux du deck. Vous pouvez disposer d'un contrôleur entier supplémentaire au toucher de 2 buttons (Shift + Browse sur le S4).",
    "En tant que source d'inspiration naturelle, je peux vous dire que je travaille sur un mapping capable de contrôler tous les decks sélectionnés en même temps. (Si tous les decks sont sélectionnés et que vous appuyez sur play, tous les decks se mettent en lecture.) Je ne suis pas vraiment pressé de dévoiler celui-là. Honnêtement, je ne libère celui-ci que parce qu'il risque d'être dépassé, et par générosité de caractère. Personne ne me paie pour ça. Peut-être que quelque chose en sortira.",
    "Je dois rendre à nouveau hommage à DJ Tech Tools. Ean, tu sembles vraiment cool mon vieux. Merci ! J'ai beaucoup appris de tes mappings déroutants mais de tes vidéos géniales ! Je dois aussi créditer Scamo, Jay Dizzle, Koolie's Combos. J'ai pillé des informations dans vos mappings pour programmer certaines des fonctions FX. Je suis sûr qu'il y en a eu d'autres en chemin. Merci à tous ! Merci à vous, Native Instruments ! Je n'aurais rien pu faire sans vous. J'espère que vous saurez mieux intégrer Maschine et Traktor. S'il vous plaît, s'il vous plaît, s'il vous plaît ! Comme le fromage suisse et le jambon au miel sur un cracker. Pour un cracker. Hé ! On est ce qu'on mange, non ? Salut à mon pote TJ Brown. Il monte, celui-là !",
    "HÉ ! Regardez-moi ça ! Je suis allé jusqu'à faire un tableur (spreadsheet) pour lister ce qui a été programmé. Si vous regardez de près, il serait facile de comprendre comment l'enrichir ou modifier ce qui s'y trouve. Je pense que tout est correct, mais pardon si quelque chose ne l'est pas tout à fait. Si vous apprenez le mapping, je suggère de garder le controller editor ouvert pour voir les modifiers changer. Cela aide à comprendre ce qui se passe.",
    "Note finale. Elle est plutôt importante, je suppose. J'ai transformé le button play de droite en button shift, et le button shift de droite en button play. J'espère que cela n'embrouillera personne. L'idée est d'écarter votre main droite du chemin de votre autre main droite.",
    "Je suis à l'écoute si quelqu'un a des mappings à modifier et à partager. J'espère que cela aidera beaucoup de gens avec Traktor.",
    "Oh ! Qu'est-ce que vous dites ? D'autres suggestions ? J'utilise Windows. Je peux comprendre pourquoi les DJ sur Mac n'aiment pas ça, mais je n'aime simplement pas Mac. J'aime bien le mac and cheese, par contre. L'écran tactile c'est sympa, mais Traktor n'a que des fonctions tactiles basiques. Xotopad fonctionne plutôt bien. Je trouve que ces tables sur ce contrôleur Ion DJ sont plutôt chouettes. C'est le contrôleur de mixage le plus simple et le meilleur que je connaisse. Il s'est adapté à Traktor à merveille. Midi-ox, et loopB1. Edjing est amusant sur mon écran tactile. Génial pour les débutants qui veulent juste jouer. Je dois filer, et j'espère que vous passerez tous une excellente journée !",
    "Drew",
]

HTML = ('<html><head><meta charset="utf-8"><style>'
        'body { font-family: sans-serif; font-size: 11px; }'
        'h1 { font-size: 14px; text-align: center; }'
        'p { text-align: justify; margin: 0 0 7px 0; }'
        'p.sig { text-align: right; font-style: italic; }'
        '</style></head><body><h1>Mapping Speech — traduction française</h1>'
        + "".join(f"<p class='sig'>{p}</p>" if p == "Drew" else f"<p>{p}</p>" for p in PARAGRAPHES)
        + "</body></html>")

MARGE = 62  # points (~22 mm)
RECT = fitz.Rect(MARGE, MARGE, 595 - MARGE, 842 - MARGE)  # A4


def generer(sortie: Path) -> bytes:
    story = fitz.Story(html=HTML, user_css=None, em=1)
    writer = fitz.DocumentWriter(str(sortie))
    suite = True
    while suite:
        dev = writer.begin_page(fitz.paper_rect("a4"))
        suite, _ = story.place(RECT)
        story.draw(dev)
        writer.end_page()
    writer.close()
    # métadonnées propres + normalisation déterministe (aucune date volatile)
    doc = fitz.open(str(sortie))
    doc.set_metadata({
        "title": "Mapping Speech - traduction française",
        "author": "Drew (auteur original) - traduction française",
        "subject": "Fixture batterie analyse-doc-s4mk2 (traduction française du récit DREW)",
        "creator": "Task 40 - régénération fixture (PyMuPDF Story)",
        "producer": "Task 40 - chaîne PyMuPDF",
    })
    octets = doc.tobytes(garbage=3, deflate=False)  # flux non compressés (lisibles par analyser-pdf-mk2.py)
    doc.close()
    # trailer /ID aléatoire → ID déterministe dérivé du contenu (idempotence byte-identique)
    import re
    m = re.search(rb"/ID\[<([0-9A-F]+)><([0-9A-F]+)>\]", octets)
    if m:
        empreinte = hashlib.sha256(octets[:m.start()] + octets[m.end():]).hexdigest()[:32].upper().encode()
        octets = octets[:m.start()] + b"/ID[<" + empreinte + b"><" + empreinte + b">]" + octets[m.end():]
    sortie.write_bytes(octets)
    return octets


def main() -> int:
    avant = hashlib.sha256(CIBLE.read_bytes()).hexdigest() if CIBLE.exists() else None
    octets = generer(CIBLE)
    apres = hashlib.sha256(octets).hexdigest()
    print(f"fixture générée : {CIBLE.name} ({len(octets)} octets, sha256 {apres[:16]}…)")
    print(f"idempotence : {'BYTE-IDENTIQUE' if avant == apres else 'DIVERGENT (avant ' + (avant or '—')[:16] + '…)'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
