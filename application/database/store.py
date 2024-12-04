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
def store_documents(sections_path, model, collection):
    """
    Verarbeitet JSON-Dokumente aus einem Verzeichnis und speichert thematisch gruppierte Abschnitte.
    """
    try:
        # Überprüfen, ob der Import-Pfad existiert
        if not os.path.exists(sections_path):
            print(f"Der Pfad {sections_path} existiert nicht.")
            return

        # JSON-Dateien im Verzeichnis verarbeiten
        for file_name in os.listdir(sections_path):
            file_path = os.path.join(sections_path, file_name)
            if os.path.isfile(file_path) and file_name.endswith(".json"):
                print(f"\n---------------------------------------------------------")
                print(f"Verarbeite Datei: {sections_path}/{file_name}")
                print("---------------------------------------------------------")

                try:
                    # JSON-Datei laden
                    with open(file_path, "r", encoding="utf-8") as json_file:
                        grouped_sections = json.load(json_file)

                    # Abschnitte thematisch speichern
                    for section in grouped_sections:
                        section_id = section.get("section", None)
                        section_content = " ".join(section.get("content", []))
                        section_tags = section.get("tags", [])

                        print(f"Section {section_id}:")
                        print("---------------------------------------------------------\n")
                        print(section_content)
                        print(f"\nTags: {section_tags}")

                        if section_content.strip():
                            embedding = model.encode(section_content)
                            collection.add(
                                documents=section_content,
                                metadatas={
                                    "section_id": section_id,
                                    "source_file": file_name,
                                    "tags": ", ".join(section_tags)
                                },
                                ids=f"{file_name}_section_{section_id}",
                                embeddings=embedding
                            )
                            print("\nAbschnitt gespeichert.")
                            print("---------------------------------------------------------")

                except Exception as e:
                    print(f"Fehler beim Verarbeiten der Datei {file_name}: {e}")

    except Exception as e:
        print(f"Fehler beim Verarbeiten des Ordners {sections_path}: {e}")