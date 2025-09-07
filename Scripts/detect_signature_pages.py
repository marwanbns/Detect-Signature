# scripts/detect_signature_pages.py
import openai
import os
import json

def load_api_key(key_file="key.txt"):
    """Charge la clé API OpenAI depuis un fichier"""
    if not os.path.exists(key_file):
        raise FileNotFoundError(f"Le fichier {key_file} est introuvable. Place-le à la racine du projet.")
    with open(key_file, "r", encoding="utf-8") as f:
        return f.read().strip()

def clean_text(text):
    """ Nettoie le texte en supprimant les espaces parasites et remplaçant les caractères spéciaux. """
    replacements = {
        "’": "'",
        "‘": "'",
        "“": '"',
        "”": '"'
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return " ".join(text.split())  # supprime les espaces multiples

def find_signature_pages_and_keywords(text_folder, output_json, key_file="key.txt"):
    """
    Analyse les textes OCR pour détecter les mots-clés de signature.
    Sauvegarde les résultats dans un fichier JSON.
    Retourne un dict {fichier_txt: [keywords]}.
    """
    openai.api_key = load_api_key(key_file)
    pages_with_signatures = {}

    for text_file in sorted(os.listdir(text_folder)):
        if text_file.endswith(".txt"):
            with open(os.path.join(text_folder, text_file), "r", encoding="utf-8") as f:
                text = f.read()

            prompt = (f"Voici un extrait d'un contrat :\n\n{text}\n\n"
                      "Identifie UNIQUEMENT les mots-clés qui indiquent une zone **obligatoire** de signature "
                      "(c'est-à-dire où les signataires doivent écrire leur nom et signer). "
                      "Ne donne PAS de termes généraux comme 'Agreement', 'signed' ou 'Signatures on Following Page'. "
                      "Si tu es CERTAIN que cette page contient un pavé de signature, retourne le résultat sous forme JSON :\n"
                      "{\"keywords\": [\"mot1\", \"mot2\"]}.\n"
                      "Sinon, retourne {\"keywords\": []}.\n\n"
                      "IMPORTANT : Garde exactement la typographie d'origine du texte. "
                      "N'utilise pas d'apostrophes spéciales (‘’), remplace-les par des apostrophes standards ('). "
                      "Évite également les guillemets spéciaux (“ ”), utilise des guillemets simples ou doubles normaux. "
                      "AUCUN espace supplémentaire ne doit être ajouté ou retiré dans les mots détectés.")

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Tu es un assistant spécialisé dans la détection des pavés de signature. "
                                                  "Tu dois uniquement identifier les mots-clés qui indiquent **clairement** "
                                                  "une zone où une signature est requise (ex : 'Seller's Signature')."},
                    {"role": "user", "content": prompt}
                ]
            )

            try:
                data = json.loads(response["choices"][0]["message"]["content"])
                keywords = [clean_text(k) for k in data.get("keywords", [])]
                if keywords:
                    pages_with_signatures[text_file] = keywords
            except json.JSONDecodeError:
                print(f"Erreur JSON pour {text_file}, réponse inattendue.")

    # Sauvegarde dans un JSON
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(pages_with_signatures, f, indent=4)

    print(f"Détection terminée. Résultats enregistrés dans {output_json}")
    return pages_with_signatures

# Test direct (si on exécute uniquement ce fichier)
if __name__ == "__main__":
    INPUT_TEXTS_DIR = "../extracted_texts"
    OUTPUT_JSON = "../signature_keywords.json"
    results = find_signature_pages_and_keywords(INPUT_TEXTS_DIR, OUTPUT_JSON)
    print("Pages avec signature détectées :", results)
