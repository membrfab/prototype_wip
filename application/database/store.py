import os
from llama_index.core import SimpleDirectoryReader
from service.text import split_document

### Sammlung löschen und neu erstellen
def setup_collection(chromaDBclient, collection_name):
    collections = chromaDBclient.list_collections()
    collection_names = [coll.name for coll in collections]
    if collection_name in collection_names:
        chromaDBclient.delete_collection(collection_name)
    return chromaDBclient.create_collection(name=collection_name)

### Thematische Gruppierung über das gesamte Dokument
def store_documents(documents, source_file, model, collection):
    # Kombiniere alle Seiteninhalte
    full_text = " ".join([page.text for page in documents])

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
                metadatas={"section_id": section_idx, "source_file": source_file, "grouped": True},
                ids=f"{source_file}_grouped_section_{section_idx}",
                embeddings=embedding
            )
            print("\nAbschnitt gespeichert.")
            print("\n---------------------------------------------------------")


### Ordner verarbeiten
def process_folder(folder_path, collection_name, model, chromaDBclient):
    collection = chromaDBclient.get_collection(collection_name)
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            print("\n---------------------------------------------------------")
            print(f"Lade Datei: {file_name}")
            print("---------------------------------------------------------")

            try:
                # Dokumente laden
                reader = SimpleDirectoryReader(input_files=[file_path])
                documents = reader.load_data()

                # Thematische Gruppierung speichern
                store_documents(documents, file_name, model, collection)

            except Exception as e:
                print(f"Fehler bei der Verarbeitung von {file_name}: {e}")
