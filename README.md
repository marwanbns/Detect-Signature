# Détection de pavés de signature dans les contrats PDF
**Description**
Ce projet permet d’analyser automatiquement des contrats PDF afin de :

**Convertir** le PDF en images page par page

**Extraire** le texte avec OCR (Tesseract)

**Détecter** les zones de signature obligatoires grâce à l’IA (OpenAI GPT)

**Annoter** les images avec des rectangles autour des zones détectées

**Prévisualiser** et parcourir les images annotées via une interface graphique (Tkinter)

**Objectif** : automatiser l’identification et la visualisation des pavés de signature dans des documents légaux.

## Installation
1. Cloner le projet
git clone <url_du_repo>
cd <nom_du_repo>

2. Créer un environnement virtuel
conda create -n signature-detect python=3.10
conda activate signature-detect

3. Installer les dépendances
pip install -r requirements.txt

4. Clé API OpenAI
"sk-xxxxxxxxxxxxx"

## Arborescence
```
.
├── key.txt
├── main.py
├── scripts/
│   ├── convert_pdf_to_images.py
│   ├── extract_text_with_ocr.py
│   ├── detect_signature_pages.py
│   └── visualize_signature_boxes.py
├── inputs/
│   └── pdf/
├── outputs/
│   ├── images/
│   ├── extracted_texts/
│   ├── annotated_images/
│   └── signature_keywords.json
└── requirements.txt
```

## Utilisation
1.Lancer l'application

```
python main.py
```

2.Interface Tkinter :

    1. Convert PDF -> Images : transformation PDF en PNG

    2. Extraire texte avec OCR : extraction de texte brut

    3. Détecter pavés de signature : analyse via OpenAI

    4. Annoter les images : rectangles sur les zones trouvées

    5. Prévisualiser images : naviguer entre toutes les pages annotées

## Auteur
Projet développé par Marwan bns