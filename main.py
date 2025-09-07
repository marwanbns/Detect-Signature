# main.py
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import scripts.convert_pdf_to_images as pdf2img
import scripts.extract_text_with_ocr as ocr
import scripts.detect_signature_pages as detect
import scripts.visualize_signature_boxes as annotate

# Dossiers d’E/S
INPUT_PDF_DIR = "inputs/pdf"
OUTPUT_IMAGES_DIR = "outputs/images"
OUTPUT_TEXTS_DIR = "outputs/extracted_texts"
OUTPUT_ANNOTATED_DIR = "outputs/annotated_images"
OUTPUT_SIGNATURE_JSON = "outputs/signature_keywords.json"

# Création des dossiers si absents
for d in [INPUT_PDF_DIR, OUTPUT_IMAGES_DIR, OUTPUT_TEXTS_DIR, OUTPUT_ANNOTATED_DIR]:
    os.makedirs(d, exist_ok=True)

def run_convert():
    pdf_files = filedialog.askopenfilenames(
        initialdir=INPUT_PDF_DIR,
        filetypes=[("PDF files", "*.pdf")]
    )
    if not pdf_files:
        return
    for pdf in pdf_files:
        pdf2img.pdf_to_images(pdf, OUTPUT_IMAGES_DIR)
    messagebox.showinfo("Succès", "Conversion PDF → Images terminée !")

def run_ocr():
    ocr.extract_text_from_images(OUTPUT_IMAGES_DIR, OUTPUT_TEXTS_DIR)
    messagebox.showinfo("Succès", "Extraction OCR terminée !")

def run_detect():
    signature_data = detect.find_signature_pages_and_keywords(
        text_folder=OUTPUT_TEXTS_DIR,
        output_json=OUTPUT_SIGNATURE_JSON
    )
    if signature_data:
        messagebox.showinfo("Succès", "Détection des pavés de signature terminée !")
    else:
        messagebox.showwarning("Avertissement", "Aucun pavé de signature détecté.")

def run_annotate():
    results = annotate.annotate_images(
        image_folder=OUTPUT_IMAGES_DIR,
        output_folder=OUTPUT_ANNOTATED_DIR,
        signature_data_file=OUTPUT_SIGNATURE_JSON
    )
    if results:
        messagebox.showinfo("Succès", "Annotation terminée !")
    else:
        messagebox.showwarning("Avertissement", "Aucune image annotée.")

# --- Prévisualisation avec navigation ---
def run_preview():
    # On regarde d'abord dans les images annotées
    files = sorted([os.path.join(OUTPUT_ANNOTATED_DIR, f) for f in os.listdir(OUTPUT_ANNOTATED_DIR) if f.endswith(".png")])
    if not files:
        # Sinon on prend les images brutes
        files = sorted([os.path.join(OUTPUT_IMAGES_DIR, f) for f in os.listdir(OUTPUT_IMAGES_DIR) if f.endswith(".png")])

    if not files:
        messagebox.showwarning("Avertissement", "Aucune image à prévisualiser.")
        return

    # Nouvelle fenêtre
    preview = tk.Toplevel(root)
    preview.title("Prévisualisation des images")
    preview.geometry("800x600")

    img_label = tk.Label(preview)
    img_label.pack(expand=True)

    # Index de l'image courante
    state = {"index": 0}

    def show_image(idx):
        try:
            img = Image.open(files[idx])
            img.thumbnail((750, 550))
            img_tk = ImageTk.PhotoImage(img)
            img_label.config(image=img_tk)
            img_label.image = img_tk
            preview.title(f"Prévisualisation - {os.path.basename(files[idx])}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'afficher l'image : {e}")

    def prev_image():
        if state["index"] > 0:
            state["index"] -= 1
            show_image(state["index"])

    def next_image():
        if state["index"] < len(files) - 1:
            state["index"] += 1
            show_image(state["index"])

    # Boutons navigation
    nav_frame = tk.Frame(preview)
    nav_frame.pack(pady=10)

    btn_prev = tk.Button(nav_frame, text="⏮ Précédent", command=prev_image)
    btn_prev.pack(side="left", padx=10)

    btn_next = tk.Button(nav_frame, text="Suivant ⏭", command=next_image)
    btn_next.pack(side="left", padx=10)

    # Afficher la première image
    show_image(0)

# --- Interface Tkinter ---
root = tk.Tk()
root.title("Détection de pavés de signature")
root.geometry("500x350")

label = tk.Label(root, text="Bienvenue dans le détecteur de pavés de signature", font=("Arial", 14))
label.pack(pady=20)

btn1 = tk.Button(root, text="1. Convert PDF → Images", command=run_convert, width=30)
btn1.pack(pady=5)

btn2 = tk.Button(root, text="2. Extraire texte avec OCR", command=run_ocr, width=30)
btn2.pack(pady=5)

btn3 = tk.Button(root, text="3. Détecter pavés de signature", command=run_detect, width=30)
btn3.pack(pady=5)

btn4 = tk.Button(root, text="4. Annoter les images", command=run_annotate, width=30)
btn4.pack(pady=5)

btn5 = tk.Button(root, text="5. Prévisualiser images", command=run_preview, width=30)
btn5.pack(pady=5)

root.mainloop()
