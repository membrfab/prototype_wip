import os
import json
from llama_index.core import SimpleDirectoryReader

def parse_documents(pdf_path, json_path, parser):
    # Sicherstellen, dass der Export-Pfad existiert
    os.makedirs(json_path, exist_ok=True)

    for file_name in os.listdir(pdf_path):
        file_path = os.path.join(pdf_path, file_name)
        if os.path.isfile(file_path):
            print(f"Lade Datei: {file_name}")

            try:
                # Dokumente laden
                documents = SimpleDirectoryReader(input_files=[file_path]).load_data()
                
                # JSON-Datei speichern
                output_file = os.path.join(json_path, f"{os.path.splitext(file_name)[0]}.json")
                with open(output_file, "w", encoding="utf-8") as json_file:
                    json.dump([doc.__dict__ for doc in documents], json_file, ensure_ascii=False, indent=4)

                print(f"Erfolgreich gespeichert in: {output_file}\n")

            except Exception as e:
                print(f"Fehler bei der Verarbeitung von {file_name}: {e}")
