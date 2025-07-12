import openai
import os
import json

# Charger la clé API depuis key.txt
openai.api_key = open("key.txt", "r").read().strip('\n')

# Dossier contenant les textes extraits des images OCR
text_folder = "../extracted_texts"
output_json = "../signature_keywords.json"

def clean_text(text):
    """ Nettoie le texte en supprimant les espaces parasites et en remplaçant les caractères spéciaux. """
    replacements = {
        "’": "'",
        "‘": "'",
        "“": '"',
        "”": '"'
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    # **Suppression des espaces inutiles**
    text = " ".join(text.split())  # Supprime les espaces inutiles
    return text

def find_signature_pages_and_keywords(text_folder):
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
                      "{{\"keywords\": [\"mot1\", \"mot2\"]}}.\n"
                      "Sinon, retourne {{\"keywords\": []}}.\n\n"
                      "IMPORTANT : Garde exactement la typographie d'origine du texte. "
                      "N'utilise pas d'apostrophes spéciales (‘’), remplace-les par des apostrophes standards ('). "
                      "Évite également les guillemets spéciaux (“ ”), utilise des guillemets simples ou doubles normaux. "
                      "AUCUN espace supplémentaire ne doit être ajouté ou retiré dans les mots détectés.")

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "system", "content": "Tu es un assistant spécialisé dans la détection des pavés de signature. "
                                                        "Tu dois uniquement identifier les mots-clés qui indiquent **clairement** "
                                                        "une zone où une signature est requise (ex : 'Seller's Signature', 'Purchaser's Signature'). "
                                                        "Évite les termes vagues ou généraux. "
                                                        "Garde la typographie EXACTEMENT comme elle apparaît dans l'extrait."},
                          {"role": "user", "content": prompt}]
            )

            try:
                data = json.loads(response["choices"][0]["message"]["content"])
                keywords = [clean_text(k) for k in data.get("keywords", [])]

                # Si des mots-clés pertinents sont trouvés, on les enregistre
                if keywords:
                    pages_with_signatures[text_file] = keywords  

            except json.JSONDecodeError:
                print(f"⚠️ Erreur JSON pour {text_file}, réponse inattendue.")

    return pages_with_signatures

# Exécuter l'analyse
signature_data = find_signature_pages_and_keywords(text_folder)

# Afficher les résultats
print("Pages avec signature détectées :")
for page, keywords in signature_data.items():
    print(f"- {page} : {keywords}")

# Sauvegarde des mots-clés détectés dans un fichier JSON
with open(output_json, "w", encoding="utf-8") as f:
    json.dump(signature_data, f, indent=4)

print(f"Données enregistrées dans {output_json}")