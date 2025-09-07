# scripts/convert_pdf_to_images.py
from pdf2image import convert_from_path
import os

def pdf_to_images(pdf_path, output_folder):
    """
    Convertit un fichier PDF en une liste d'images PNG.
    Retourne les chemins des images générées.
    """
    os.makedirs(output_folder, exist_ok=True)
    poppler_path = os.path.abspath("poppler-24.08.0/Library/bin")
    os.environ["PATH"] += os.pathsep + poppler_path
    images = convert_from_path(pdf_path, dpi=300, poppler_path=poppler_path)
    image_paths = []
    
    for i, img in enumerate(images):
        img_name = f"{os.path.basename(pdf_path).replace('.pdf', '')}_page_{i+1}.png"
        img_path = os.path.join(output_folder, img_name)
        img.save(img_path, "PNG")
        image_paths.append(img_path)

    return image_paths

def convert_all_pdfs(pdf_folder, output_folder):
    """
    Convertit tous les PDF d'un dossier en images.
    Retourne un dictionnaire {pdf_file: [image_paths]}.
    """
    os.makedirs(output_folder, exist_ok=True)
    results = {}
    
    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]
    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_folder, pdf_file)
        print(f"📄 Conversion de {pdf_file} en images...")
        results[pdf_file] = pdf_to_images(pdf_path, output_folder)

    print(f"Conversion terminée ! Images enregistrées dans '{output_folder}'")
    return results

# Permet de tester directement ce script si on l'exécute seul
if __name__ == "__main__":
    INPUT_PDF_DIR = "../contratpdf"
    OUTPUT_IMAGES_DIR = "../images"
    convert_all_pdfs(INPUT_PDF_DIR, OUTPUT_IMAGES_DIR)
