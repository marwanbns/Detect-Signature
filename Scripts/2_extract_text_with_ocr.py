import pytesseract
from PIL import Image
import os

# Dossiers
image_folder = "../images"
output_folder = "../extracted_texts"

# Assurer que le dossier de texte existe
os.makedirs(output_folder, exist_ok=True)

def extract_text_from_images(image_folder):
    extracted_texts = {}

    for img_file in sorted(os.listdir(image_folder)):
        if img_file.endswith(".png"):
            img_path = os.path.join(image_folder, img_file)
            text = pytesseract.image_to_string(Image.open(img_path))

            text_file_path = os.path.join(output_folder, f"{img_file.replace('.png', '')}.txt")
            with open(text_file_path, "w", encoding="utf-8") as f:
                f.write(text)

            extracted_texts[img_path] = text

    return extracted_texts

texts = extract_text_from_images(image_folder)
print("Extraction OCR terminée ! Textes enregistrés dans 'extracted_texts/'")