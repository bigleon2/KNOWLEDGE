#!/usr/bin/env python3
"""
extract_pdf.py — Extraction PDF via PyMuPDF (fitz)

Ce script effectue l'extraction BRUTE du PDF. Il est MODE-AGNOSTIC :
il ne gère ni les modes (qwen/glm/multi/pipeline), ni le menu
décisionnel, ni la normalisation du contenu. Ces responsabilités
incombent au LLM lors de l'étape de traitement.

Capacités d'extraction :
  1. Extraction structurée (texte, blocs logiques, coordonnées)
  2. Gestion des tableaux (via page.find_tables() de PyMuPDF)
  3. Gestion des images (métadonnées + BBox, extraction optionnelle)
  4. Détection OCR (heuristique : ratio texte/images)
  5. Extraction fine (liens, signets, métadonnées, polices/tailles/couleurs)
  6. Détection en-têtes/pieds de page répétitifs (pour nettoyage RAG)

Limites connues :
  - Pas d'OCR réel (détection uniquement). L'OCR avancé et les marqueurs
    [[? mot]] sont gérés par le LLM en mode pipeline/normalisation.
  - Les polices sont extraites comme données brutes pour le LLM, pas
    utilisées algorithmiquement pour la détection de structure.
  - Les images sont décrites en métadonnées (BBox, dimensions).
    Utiliser --extract-images pour les extraire sur disque.

Usage :
  python extract_pdf.py --input file.pdf --output dir/
  python extract_pdf.py --input file.pdf --output dir/ --full
  python extract_pdf.py --input file.pdf --output dir/ --links --bookmarks --fonts
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict


def extract_links(doc) -> list:
    """Extrait tous les liens hypertexte du PDF (URL + texte d'ancre + page)."""
    links = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        page_links = page.get_links()
        for link in page_links:
            if link.get("uri"):
                anchor_text = ""
                try:
                    rect = fitz.Rect(link["from"])
                    blocks = page.get_text("blocks")
                    for block in blocks:
                        if block[6] == 0:
                            block_rect = fitz.Rect(block[0], block[1], block[2], block[3])
                            if rect.intersects(block_rect):
                                anchor_text += block[4].strip() + " "
                except Exception:
                    pass

                links.append({
                    "text": anchor_text.strip() or link.get("uri", ""),
                    "url": link["uri"],
                    "page": page_num + 1
                })
    return links


def extract_bookmarks(doc) -> list:
    """Extrait les signets/TOC intégrés du PDF."""
    toc = doc.get_toc()
    bookmarks = []
    for entry in toc:
        level, title, page = entry
        bookmarks.append({
            "heading": title,
            "level": level,
            "page": page
        })
    return bookmarks


def extract_fonts(doc) -> list:
    """
    Analyse les polices, tailles et couleurs utilisées dans le document.
    Les données sont extraites pour être exploitées par le LLM lors de
    la détection de structure (mode pipeline), pas pour un traitement
    algorithmique par le script.
    """
    font_info = defaultdict(lambda: {"count": 0, "sizes": set(), "colors": set()})
    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict", flags=11)["blocks"]
        for block in blocks:
            if block["type"] == 0:
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        font_name = span.get("font", "inconnu")
                        font_size = round(span.get("size", 0), 1)
                        color = span.get("color", 0)
                        color_hex = f"#{color:06x}" if color else "#000000"
                        font_info[font_name]["count"] += 1
                        font_info[font_name]["sizes"].add(font_size)
                        font_info[font_name]["colors"].add(color_hex)

    result = []
    for name, info in font_info.items():
        result.append({
            "font": name,
            "occurrences": info["count"],
            "sizes": sorted(list(info["sizes"])),
            "colors": sorted(list(info["colors"]))
        })
    return sorted(result, key=lambda x: x["occurrences"], reverse=True)


def detect_headers_footers(pages_data: list, threshold: float = 0.7) -> dict:
    """
    Détecte les en-têtes et pieds de page répétitifs pour nettoyage RAG.
    Seuil de détection : une ligne est considérée comme répétitive si
    elle apparaît sur >= threshold % des pages (par défaut 70 %).
    """
    if len(pages_data) < 3:
        return {"header_patterns": [], "footer_patterns": []}

    first_lines = []
    last_lines = []
    for page in pages_data:
        lines = [l.strip() for l in page["text"].split("\n") if l.strip()]
        if lines:
            first_lines.append(lines[0])
        if len(lines) > 1:
            last_lines.append(lines[-1])

    header_patterns = _find_repeated_patterns(first_lines, threshold)
    footer_patterns = _find_repeated_patterns(last_lines, threshold)

    return {
        "header_patterns": header_patterns,
        "footer_patterns": footer_patterns
    }


def _find_repeated_patterns(lines: list, threshold: float) -> list:
    """Trouve les lignes répétées au-dessus du seuil."""
    if not lines:
        return []
    counts = defaultdict(int)
    for line in lines:
        normalized = re.sub(r'\d+', 'X', line.strip())
        if normalized:
            counts[normalized] += 1

    total = len(lines)
    patterns = []
    for pattern, count in counts.items():
        if count / total >= threshold and count >= 2:
            patterns.append({
                "pattern": pattern,
                "occurrences": count,
                "coverage": round(count / total * 100, 1)
            })
    return sorted(patterns, key=lambda x: x["occurrences"], reverse=True)


def _normalize_pdf_date(raw_date: str) -> str:
    """
    Normalise une date PDF vers le format YYYY-MM-DD.
    Les métadonnées PDF utilisent le format "D:YYYYMMDDHHmmSS+TZ'".
    """
    if not raw_date:
        return "NON PRÉSENT DANS LE DOCUMENT"
    cleaned = raw_date.replace("D:", "")
    if len(cleaned) >= 8 and cleaned[:8].isdigit():
        return f"{cleaned[:4]}-{cleaned[4:6]}-{cleaned[6:8]}"
    return cleaned[:10] if len(cleaned) >= 10 else "NON PRÉSENT DANS LE DOCUMENT"


def _extract_tables_from_page(page) -> list:
    """
    Extrait les tableaux d'une page via page.find_tables() de PyMuPDF.
    Chaque tableau est converti en liste de listes (lignes × colonnes).
    """
    tables = []
    try:
        found = page.find_tables()
        for table in found:
            rows = []
            for row in table.extract():
                # Nettoyer les cellules None
                cleaned = [str(cell).strip() if cell is not None else "" for cell in row]
                rows.append(cleaned)
            if rows:
                tables.append({"data": rows, "bbox": list(table.bbox)})
    except Exception:
        pass
    return tables


def extract_pdf(input_path: str, output_dir: str,
                full: bool = False,
                extract_links_flag: bool = False,
                extract_bookmarks_flag: bool = False,
                extract_fonts_flag: bool = False,
                rag_cleanup: bool = False,
                extract_images_flag: bool = False) -> dict:
    """
    Extrait le texte et les métadonnées d'un PDF via PyMuPDF.

    Ce script est MODE-AGNOSTIC. Il produit les données brutes que le LLM
    normalisera selon le mode choisi (qwen/glm/multi/pipeline).

    Retourne les métadonnées extraites ou signale une erreur.
    """
    try:
        global fitz
        import fitz  # PyMuPDF
    except ImportError:
        print("ERREUR: PyMuPDF (fitz) non installé. Exécutez : pip install PyMuPDF")
        sys.exit(1)

    if not os.path.isfile(input_path):
        print(f"ERREUR: Fichier introuvable : {input_path}")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    # --- Ouverture du document ---
    try:
        doc = fitz.open(input_path)
    except Exception as e:
        print(f"DOCUMENT CORROMPU : impossible d'ouvrir le fichier. {e}")
        sys.exit(1)

    # --- Vérification PDF protégé (P2) ---
    if doc.is_encrypted:
        print("DOCUMENT PROTÉGÉ — extraction impossible")
        metadata_error = {
            "error": "DOCUMENT PROTÉGÉ — extraction impossible",
            "input": input_path,
            "hint": "Fournissez un PDF non protégé."
        }
        meta_path = os.path.join(output_dir, "document_metadata.json")
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(metadata_error, f, ensure_ascii=False, indent=2)
        doc.close()
        return metadata_error

    if len(doc) == 0:
        print("DOCUMENT VIDE : 0 page")
        metadata_error = {
            "error": "DOCUMENT VIDE — extraction impossible",
            "input": input_path,
            "page_count": 0,
            "hint": "Le fichier PDF ne contient aucune page."
        }
        meta_path = os.path.join(output_dir, "document_metadata.json")
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(metadata_error, f, ensure_ascii=False, indent=2)
        doc.close()
        return metadata_error

    # --- Métadonnées ---
    raw_meta = doc.metadata or {}
    metadata = {
        "title": raw_meta.get("title", "") or "NON PRÉSENT DANS LE DOCUMENT",
        "authors": (
            [a.strip() for a in raw_meta.get("author", "").split(";") if a.strip()]
            if raw_meta.get("author")
            else []
        ),
        "dates": {
            "created": _normalize_pdf_date(raw_meta.get("creationDate", "")),
            "modified": _normalize_pdf_date(raw_meta.get("modDate", "")),
        },
        "version": raw_meta.get("format", "NON PRÉSENT DANS LE DOCUMENT"),
        "page_count": len(doc),
        "language": raw_meta.get("language", "NON PRÉSENT DANS LE DOCUMENT"),
        "source_type": "pdf",
        "ocr": False,
        "ocr_quality": "NON APPLICABLE",
        "ocr_notes": "NON APPLICABLE",
        "producer": raw_meta.get("producer", "NON PRÉSENT DANS LE DOCUMENT"),
        "creator": raw_meta.get("creator", "NON PRÉSENT DANS LE DOCUMENT"),
        "encryption": False,
    }

    # --- Extraction par page (avec protection contre corruption — P10) ---
    total_text_length = 0
    pages_data = []
    corrupted_pages = []

    for page_num in range(len(doc)):
        try:
            page = doc[page_num]

            # Texte
            text = page.get_text("text")

            # Images avec BBox
            images = page.get_images(full=True)
            images_with_bbox = []
            for img_index, img in enumerate(images):
                xref = img[0]
                try:
                    base_image = doc.extract_image(xref)
                    img_rects = page.get_image_rects(xref)
                    bbox = None
                    if img_rects:
                        r = img_rects[0]
                        bbox = [r.x0, r.y0, r.x1, r.y1]
                    images_with_bbox.append({
                        "xref": xref,
                        "index": img_index,
                        "bbox": bbox,
                        "width": base_image.get("width", 0),
                        "height": base_image.get("height", 0),
                        "ext": base_image.get("ext", ""),
                    })
                except Exception:
                    images_with_bbox.append({
                        "xref": xref,
                        "index": img_index,
                        "bbox": None,
                    })

            # Blocs de texte avec coordonnées
            blocks = page.get_text("blocks")

            # Détecter si la page est principalement des images (scannée)
            # Seuil : < 50 caractères de texte ET au moins 1 image
            text_length = len(text.strip())
            has_images = len(images) > 0
            is_image_heavy = has_images and text_length < 50

            total_text_length += text_length

            # Tableaux via page.find_tables() (P9)
            tables = _extract_tables_from_page(page)

            # Extraction des blocs avec coordonnées
            text_blocks = []
            for block in blocks:
                if block[6] == 0:
                    text_blocks.append({
                        "x0": round(block[0], 2),
                        "y0": round(block[1], 2),
                        "x1": round(block[2], 2),
                        "y1": round(block[3], 2),
                        "text": block[4].strip(),
                        "block_no": block[5],
                    })

            page_info = {
                "page": page_num + 1,
                "text": text,
                "text_length": text_length,
                "image_count": len(images),
                "images_with_bbox": images_with_bbox,
                "is_image_heavy": is_image_heavy,
                "tables": tables,
                "text_blocks": text_blocks,
            }
            pages_data.append(page_info)

        except Exception as e:
            corrupted_pages.append(page_num + 1)
            pages_data.append({
                "page": page_num + 1,
                "text": f"PAGE CORROMPUE: {e}",
                "text_length": 0,
                "image_count": 0,
                "images_with_bbox": [],
                "is_image_heavy": False,
                "tables": [],
                "text_blocks": [],
                "error": str(e),
            })

    if corrupted_pages:
        print(f"ATTENTION : pages corrompues détectées : {corrupted_pages}")

    # --- Détection OCR (heuristique uniquement) ---
    avg_text_per_page = total_text_length / max(len(doc), 1)
    image_heavy_pages = sum(1 for p in pages_data if p.get("is_image_heavy", False))
    if avg_text_per_page < 100 and image_heavy_pages > len(doc) * 0.5:
        metadata["ocr"] = True
        metadata["ocr_quality"] = "NON ÉVALUÉE — détection heuristique uniquement"
        metadata["ocr_notes"] = (
            f"Document probablement scanné. {image_heavy_pages}/{len(doc)} pages "
            "à dominante image. L'OCR réel et les marqueurs [[? mot]] sont gérés "
            "par le LLM en mode pipeline/normalisation."
        )

    # --- Liens ---
    links = []
    if extract_links_flag or full:
        links = extract_links(doc)

    # --- Signets ---
    bookmarks = []
    if extract_bookmarks_flag or full:
        bookmarks = extract_bookmarks(doc)

    # --- Polices ---
    fonts = []
    if extract_fonts_flag or full:
        fonts = extract_fonts(doc)

    # --- Nettoyage RAG ---
    headers_footers = {"header_patterns": [], "footer_patterns": []}
    if rag_cleanup or full:
        headers_footers = detect_headers_footers(pages_data)

    page_count = len(doc)

    # --- Extraction images sur disque (optionnel) — AVANT doc.close() ---
    extracted_images = []
    if extract_images_flag:
        img_dir = os.path.join(output_dir, "images")
        os.makedirs(img_dir, exist_ok=True)
        img_count = 0
        for p in pages_data:
            for img_info in p.get("images_with_bbox", []):
                try:
                    xref = img_info.get("xref")
                    if xref is None:
                        continue
                    img_bytes = doc.extract_image(xref)
                    if img_bytes and img_bytes.get("image"):
                        ext = img_info.get("ext", "png")
                        img_filename = f"page{p['page']}_img{img_info.get('index', 0)}.{ext}"
                        img_path = os.path.join(img_dir, img_filename)
                        with open(img_path, "wb") as img_f:
                            img_f.write(img_bytes["image"])
                        img_count += 1
                        extracted_images.append(img_filename)
                except Exception:
                    pass
        if img_count > 0:
            print(f"  -> {img_dir}/ ({img_count} images extraites)")

    doc.close()

    # ============================================================
    # SORTIE FICHIERS — Toujours créer TOUS les fichiers (P3, P4)
    # ============================================================

    # --- Fichier 1 : texte brut (page par page) ---
    raw_text_path = os.path.join(output_dir, "document_raw.txt")
    with open(raw_text_path, "w", encoding="utf-8") as f:
        for page in pages_data:
            if page.get("error"):
                f.write(f"{'='*60}\n")
                f.write(f"PAGE {page['page']} — CORROMPUE\n")
                f.write(f"{'='*60}\n\n")
                f.write(f"ERREUR: {page['error']}\n\n")
                continue
            f.write(f"{'='*60}\n")
            f.write(f"PAGE {page['page']}\n")
            f.write(f"{'='*60}\n\n")
            f.write(page["text"])
            if page.get("tables"):
                f.write(f"\n\n--- TABLEAUX DÉTECTÉS SUR CETTE PAGE ---\n")
                for i, table in enumerate(page["tables"], 1):
                    if isinstance(table, dict) and "data" in table:
                        for row in table["data"]:
                            f.write(" | ".join(row) + "\n")
                        f.write("\n")
            f.write("\n")

    # --- Fichier 2 : métadonnées JSON ---
    meta_path = os.path.join(output_dir, "document_metadata.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    # --- Fichier 3 : détail pages JSON ---
    pages_path = os.path.join(output_dir, "document_pages.json")
    pages_output = []
    for p in pages_data:
        pages_output.append({
            "page": p["page"],
            "text": p["text"],
            "text_length": p["text_length"],
            "image_count": p["image_count"],
            "images_with_bbox": p["images_with_bbox"],
            "is_image_heavy": p["is_image_heavy"],
            "tables": p["tables"],
            "text_blocks": p["text_blocks"],
        })
    with open(pages_path, "w", encoding="utf-8") as f:
        json.dump(pages_output, f, ensure_ascii=False, indent=2)

    # --- Fichier 4 : liens JSON (TOUJOURS créé si --full ou --links) ---
    links_path = os.path.join(output_dir, "document_links.json")
    with open(links_path, "w", encoding="utf-8") as f:
        json.dump(links, f, ensure_ascii=False, indent=2)

    # --- Fichier 5 : signets JSON (TOUJOURS créé si --full ou --bookmarks) ---
    bookmarks_path = os.path.join(output_dir, "document_bookmarks.json")
    with open(bookmarks_path, "w", encoding="utf-8") as f:
        json.dump(bookmarks, f, ensure_ascii=False, indent=2)

    # --- Fichier 6 : polices JSON (TOUJOURS créé si --full ou --fonts) ---
    fonts_path = os.path.join(output_dir, "document_fonts.json")
    with open(fonts_path, "w", encoding="utf-8") as f:
        json.dump(fonts, f, ensure_ascii=False, indent=2)

    # --- Fichier 7 : en-têtes/pieds JSON (TOUJOURS créé si --full ou --rag-cleanup) ---
    hf_path = os.path.join(output_dir, "document_headers_footers.json")
    with open(hf_path, "w", encoding="utf-8") as f:
        json.dump(headers_footers, f, ensure_ascii=False, indent=2)

    # --- Extraction images : déjà effectuée AVANT doc.close() (voir plus haut) ---

    # --- Résumé ---
    print(f"Extraction terminée : {page_count} pages traitées")
    if corrupted_pages:
        print(f"  ATTENTION : pages corrompues : {corrupted_pages}")
    print(f"  -> {raw_text_path}")
    print(f"  -> {meta_path}")
    print(f"  -> {pages_path}")
    if extract_links_flag or full:
        print(f"  -> {links_path} ({len(links)} liens)")
    if extract_bookmarks_flag or full:
        print(f"  -> {bookmarks_path} ({len(bookmarks)} signets)")
    if extract_fonts_flag or full:
        print(f"  -> {fonts_path} ({len(fonts)} polices)")
    if rag_cleanup or full:
        h_count = len(headers_footers.get("header_patterns", []))
        f_count = len(headers_footers.get("footer_patterns", []))
        print(f"  -> {hf_path} ({h_count} en-têtes, {f_count} pieds de page détectés)")
    if metadata["ocr"]:
        print(f"  ATTENTION : Document probablement scanné (OCR recommandé)")

    return metadata


def main():
    parser = argparse.ArgumentParser(
        description="Extraction PDF via PyMuPDF (mode-agnostic). "
                    "Produit les données brutes pour normalisation par le LLM."
    )
    parser.add_argument("--input", "-i", required=True, help="Chemin du fichier PDF")
    parser.add_argument("--output", "-o", required=True, help="Répertoire de sortie")
    parser.add_argument("--full", action="store_true",
                        help="Active toutes les capacités d'extraction")
    parser.add_argument("--links", action="store_true",
                        help="Extraction des liens hypertexte")
    parser.add_argument("--bookmarks", action="store_true",
                        help="Extraction des signets PDF (TOC intégré)")
    parser.add_argument("--fonts", action="store_true",
                        help="Analyse des polices, tailles et couleurs")
    parser.add_argument("--rag-cleanup", action="store_true",
                        help="Détection en-têtes/pieds de page pour nettoyage RAG")
    parser.add_argument("--extract-images", action="store_true",
                        help="Extraire les images sur disque dans un sous-dossier images/")
    args = parser.parse_args()

    extract_pdf(
        input_path=args.input,
        output_dir=args.output,
        full=args.full,
        extract_links_flag=args.links,
        extract_bookmarks_flag=args.bookmarks,
        extract_fonts_flag=args.fonts,
        rag_cleanup=args.rag_cleanup,
        extract_images_flag=args.extract_images,
    )


if __name__ == "__main__":
    main()
