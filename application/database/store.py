import os
import json
from llama_index.core import SimpleDirectoryReader
from service.chunking import split_document

### Sammlung löschen und neu erstellen
def setup_collection(chromaDBclient, collection_name, model):
    # Liste vorhandener Collections abrufen
    collections = chromaDBclient.list_collections()
    collection_names = [coll.name for coll in collections]
    
    # Collection löschen, falls vorhanden
    if collection_name in collection_names:
        print(f"Lösche bestehende Collection: {collection_name}...")
        chromaDBclient.delete_collection(collection_name)
        print(f"Collection '{collection_name}' erfolgreich gelöscht.")
    
    # Überprüfen der Embedding-Dimension des Modells
    embedding_dim = len(model.encode("Test"))
    print(f"Verwendete Embedding-Dimension des Modells: {embedding_dim}")
    
    # Neue Collection erstellen
    print(f"Erstelle neue Collection: '{collection_name}'...")
    collection = chromaDBclient.create_collection(name=collection_name)
    print(f"Neue Collection '{collection_name}' wurde erfolgreich erstellt.")
    
    return collection

### Dokumente aus JSON-Dateien speichern
def store_documents(sections_path, pdf_path, model, collection):
    if not os.path.exists(sections_path):
        print(f"Der Pfad {sections_path} existiert nicht.")
        return

    for file_name in os.listdir(sections_path):
        file_path = os.path.join(sections_path, file_name)
        if os.path.isfile(file_path) and file_name.endswith(".json"):
            print(f"\n---------------------------------------------------------")
            print(f"Verarbeite Datei: {sections_path}/{file_name}")
            print("---------------------------------------------------------")
            try:
                with open(file_path, "r", encoding="utf-8") as json_file:
                    grouped_sections = json.load(json_file)
                
                # Name der zugehörigen PDF-Datei ermitteln
                pdf_file = os.path.join(pdf_path, os.path.splitext(file_name)[0] + ".pdf")
                if not os.path.exists(pdf_file):
                    print(f"Zu JSON {file_name} passende PDF {pdf_file} nicht gefunden.")
                    pdf_file = None

                for section in grouped_sections:
                    section_id = section.get("section")
                    section_content = section.get("content", "").strip()
                    section_tags = section.get("tags", [])

                    if not section_content:
                        print(f"Leerer Inhalt in Abschnitt {section_id} von Datei {file_name}.")
                        continue
                    
                    print(f"Speichere Abschnitt {section_id} mit Tags: {section_tags}.")
                    embedding = model.encode(section_content)
                    
                    collection.add(
                        documents=section_content,
                        metadatas={
                            "section_id": section_id,
                            "source_file": file_name,
                            "tags": ", ".join(section_tags),
                            "original_pdf": pdf_file
                        },
                        ids=f"{file_name}_section_{section_id}",
                        embeddings=embedding
                    )
                    print(f"Abschnitt {section_id} gespeichert. \n")
            except Exception as e:
                print(f"Fehler beim Verarbeiten der Datei {file_name}: {e}")
