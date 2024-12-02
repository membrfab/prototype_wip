import os
import json
from llama_index.core import SimpleDirectoryReader
from service.chunking import split_document

### Sammlung löschen und neu erstellen
def setup_collection(chromaDBclient, collection_name):
    collections = chromaDBclient.list_collections()
    collection_names = [coll.name for coll in collections]
    if collection_name in collection_names:
        chromaDBclient.delete_collection(collection_name)

    # Speichern    
    collection = chromaDBclient.create_collection(name=collection_name)
    return collection

### Dokumente aus JSON-Dateien speichern
def store_documents(json_path, model, collection):
    try:
        # Überprüfen, ob der Import-Pfad existiert
        if not os.path.exists(json_path):
            print(f"Der Pfad {json_path} existiert nicht.")
            return

        # JSON-Dateien im Verzeichnis verarbeiten
        for file_name in os.listdir(json_path):
            file_path = os.path.join(json_path, file_name)
            if os.path.isfile(file_path) and file_name.endswith(".json"):
                print(f"\n---------------------------------------------------------")
                print(f"Verarbeite Datei: {file_name}")
                print("---------------------------------------------------------")

                try:
                    # JSON-Datei laden
                    with open(file_path, "r", encoding="utf-8") as json_file:
                        documents = json.load(json_file)

                    # Kombiniere alle Texte aus der JSON-Datei
                    full_text = " ".join([doc["text"] for doc in documents if "text" in doc])

                    # Thematische Gruppierung anwenden
                    grouped_sections = split_document(full_text)

                    # Abschnitte thematisch speichern
                    for section_idx, section in enumerate(grouped_sections):
                        print(f"Section {section_idx}:")
                        print("---------------------------------------------------------\n")
                        print(section)
                        if section.strip():
                            embedding = model.encode(section)
                            collection.add(
                                documents=section,
                                metadatas={"section_id": section_idx, "source_file": file_name, "grouped": True},
                                ids=f"{file_name}_grouped_section_{section_idx}",
                                embeddings=embedding
                            )
                            print("\nAbschnitt gespeichert.")
                            print("\n---------------------------------------------------------")

                except Exception as e:
                    print(f"Fehler beim Verarbeiten der Datei {file_name}: {e}")

    except Exception as e:
        print(f"Fehler beim Verarbeiten des Ordners {json_path}: {e}")
