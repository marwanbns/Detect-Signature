# scripts/extract_text_with_ocr.py
import pytesseract
from PIL import Image
import os

def extract_text_from_images(image_folder, output_folder):
    """
    Extrait le texte d'un dossier d'images avec OCR (Tesseract).
    Sauvegarde chaque texte dans un fichier .txt.
    Retourne un dict {image_path: texte}.
    """
    os.makedirs(output_folder, exist_ok=True)
    extracted_texts = {}

    for img_file in sorted(os.listdir(image_folder)):
        if img_file.endswith(".png"):
            img_path = os.path.join(image_folder, img_file)
            text = pytesseract.image_to_string(Image.open(img_path))

            text_file_path = os.path.join(output_folder, f"{img_file.replace('.png', '')}.txt")
            with open(text_file_path, "w", encoding="utf-8") as f:
                f.write(text)

            extracted_texts[img_path] = text

    print(f"Extraction OCR terminée. Textes enregistrés dans '{output_folder}'")
    return extracted_texts

# Test direct (si on exécute uniquement ce fichier)
if __name__ == "__main__":
    INPUT_IMAGES_DIR = "../images"
    OUTPUT_TEXTS_DIR = "../extracted_texts"
    texts = extract_text_from_images(INPUT_IMAGES_DIR, OUTPUT_TEXTS_DIR)
    print(f"Nombre de fichiers traités : {len(texts)}")
