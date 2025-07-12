import cv2
import os
import json
import pytesseract
from pytesseract import Output
import re
from difflib import get_close_matches

# Dossiers
image_folder = "../images"
output_folder = "../annotated_images"
signature_data_file = "../signature_keywords.json"

# Assurer que le dossier de sortie existe
os.makedirs(output_folder, exist_ok=True)

# Charger les mots-clés détectés et supprimer les espaces parasites
if os.path.exists(signature_data_file):
    with open(signature_data_file, "r", encoding="utf-8") as f:
        signature_keywords = json.load(f)

    #On supprime les espaces inutiles
    for page in signature_keywords:
        signature_keywords[page] = [" ".join(word.split()) for word in signature_keywords[page]]
else:
    print("Fichier signature_keywords.json non trouvé. Exécute `3_detect_signature_pages.py` d'abord.")
    exit()

def normalize_text(text):
    """ Normalise le texte pour éviter les problèmes d'apostrophes, d'espaces et de casse """
    return re.sub(r"[’']", "'", text).strip().lower()

def find_best_match(word, ocr_words):
    """ Trouve le mot OCR qui correspond le mieux à un mot-clé avec une tolérance """
    matches = get_close_matches(word, ocr_words, n=1, cutoff=0.8)  # Seuil de similarité de 80%
    return matches[0] if matches else None

def highlight_text(image_path, keywords):
    """ Trouve et encadre les mots-clés détectés dans l'image avec OCR et OpenCV """
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # On utilise l'OCR avec extraction des coordonnées
    d = pytesseract.image_to_data(gray, output_type=Output.DICT)

    # On normalise les mots de l'OCR pour correspondance plus souple
    words_detected = [normalize_text(word) for word in d["text"]]

    found = False

    for keyword in keywords:
        norm_keyword = normalize_text(keyword)
        keyword_parts = norm_keyword.split()
        print("Keyword :",keyword)
        print("Keyword_parts:",keyword_parts)

        for part in keyword_parts:
            best_match = find_best_match(part, words_detected)

            if best_match:
                idx = words_detected.index(best_match)
                x, y, w, h = d["left"][idx], d["top"][idx], d["width"][idx], d["height"][idx]
                # On dessine un rectangle pour chaque mots
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
                found = True

    if not found:
        print(f"Aucun mot-clé trouvé dans {image_path}")

    return img

# Nettoyage des espaces parasites dans les mots-clés avant l'annotation
for page in signature_keywords:
    signature_keywords[page] = [" ".join(word.split()) for word in signature_keywords[page]]

# Annoter les images
for text_file, keywords in signature_keywords.items():
    image_name = text_file.replace(".txt", ".png")
    image_path = os.path.join(image_folder, image_name)

    if os.path.exists(image_path):
        print(f"Traitement de {image_name} avec les mots-clés {keywords}...")

        # Mettre en évidence les signatures détectées
        annotated_img = highlight_text(image_path, keywords)

        # Sauvegarder l'image annotée
        output_path = os.path.join(output_folder, f"annotated_{image_name}")
        cv2.imwrite(output_path, annotated_img)
        print(f"Image annotée sauvegardée : {output_path}")

    else:
        print(f"Image {image_name} non trouvée dans {image_folder}")

print("Annotation terminée !")