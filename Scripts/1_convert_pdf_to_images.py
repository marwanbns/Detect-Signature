from pdf2image import convert_from_path
import os

# Dossier contenant les PDF
pdf_folder = "../contratpdf"
output_folder = "../images"

# Assurer que le dossier des images existe
os.makedirs(output_folder, exist_ok=True)

def pdf_to_images(pdf_path, output_folder):
    images = convert_from_path(pdf_path, dpi=300)
    image_paths = []
    
    for i, img in enumerate(images):
        img_path = os.path.join(output_folder, f"{os.path.basename(pdf_path).replace('.pdf', '')}_page_{i+1}.png")
        img.save(img_path, "PNG")
        image_paths.append(img_path)

    return image_paths

# Convertir tous les PDF du dossier
pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]
for pdf_file in pdf_files:
    pdf_path = os.path.join(pdf_folder, pdf_file)
    print(f"📄 Conversion de {pdf_file} en images...")
    pdf_to_images(pdf_path, output_folder)

print("Conversion terminée ! Images enregistrées dans 'images/'")