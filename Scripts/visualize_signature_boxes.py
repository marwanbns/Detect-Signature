# scripts/annotate_images.py
import cv2
import os
import json
import pytesseract
from pytesseract import Output
import re
from difflib import get_close_matches

def normalize_text(text):
    """ Normalise le texte pour éviter les problèmes d'apostrophes, d'espaces et de casse """
    return re.sub(r"[’']", "'", text).strip().lower()

def find_best_match(word, ocr_words):
    """ Trouve le mot OCR qui correspond le mieux à un mot-clé avec une tolérance """
    matches = get_close_matches(word, ocr_words, n=1, cutoff=0.8)  # Seuil de similarité = 80%
    return matches[0] if matches else None

def highlight_text(image_path, keywords):
    """ Trouve et encadre les mots-clés détectés dans l'image avec OCR et OpenCV """
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # OCR avec coordonnées
    d = pytesseract.image_to_data(gray, output_type=Output.DICT)
    words_detected = [normalize_text(word) for word in d["text"]]

    found = False
    for keyword in keywords:
        norm_keyword = normalize_text(keyword)
        keyword_parts = norm_keyword.split()

        for part in keyword_parts:
            best_match = find_best_match(part, words_detected)
            if best_match:
                idx = words_detected.index(best_match)
                x, y, w, h = d["left"][idx], d["top"][idx], d["width"][idx], d["height"][idx]
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
                found = True

    return img, found

def annotate_images(image_folder, output_folder, signature_data_file):
    """
    Annote les images en encadrant les zones contenant les mots-clés de signature.
    """
    os.makedirs(output_folder, exist_ok=True)

    if not os.path.exists(signature_data_file):
        raise FileNotFoundError(
            f"Fichier {signature_data_file} non trouvé. "
            "Exécute d'abord detect_signature_pages.py"
        )

    # Charger les mots-clés détectés
    with open(signature_data_file, "r", encoding="utf-8") as f:
        signature_keywords = json.load(f)

    # Nettoyer les espaces parasites
    for page in signature_keywords:
        signature_keywords[page] = [" ".join(word.split()) for word in signature_keywords[page]]

    results = {}
    for text_file, keywords in signature_keywords.items():
        image_name = text_file.replace(".txt", ".png")
        image_path = os.path.join(image_folder, image_name)

        if os.path.exists(image_path):
            annotated_img, found = highlight_text(image_path, keywords)
            output_path = os.path.join(output_folder, f"annotated_{image_name}")
            cv2.imwrite(output_path, annotated_img)

            results[image_name] = {
                "keywords": keywords,
                "found": found,
                "output_path": output_path
            }
        else:
            results[image_name] = {"error": "Image non trouvée"}

    print(f"Annotation terminée. Images enregistrées dans '{output_folder}'")
    return results

# Test direct
if __name__ == "__main__":
    IMAGE_FOLDER = "../images"
    OUTPUT_FOLDER = "../annotated_images"
    SIGNATURE_DATA = "../signature_keywords.json"

    annotate_images(IMAGE_FOLDER, OUTPUT_FOLDER, SIGNATURE_DATA)
