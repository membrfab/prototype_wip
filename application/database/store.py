import os
from llama_index.core import SimpleDirectoryReader
from service.text import split_document

def setup_collection(chromaDBclient, collection_name):
    # Sammlung löschen und neu erstellen
    collections = chromaDBclient.list_collections()
    collection_names = [coll.name for coll in collections]
    if collection_name in collection_names:
        chromaDBclient.delete_collection(collection_name)
    return chromaDBclient.create_collection(name=collection_name)

def store_documents(documents, source_file, model, collection):
    for idx, document in enumerate(documents):
        content = document.text
        doc_id = f"{source_file}_page_{idx}"
        sections = split_document(content)
        for section_idx, section in enumerate(sections):
            if section.strip():
                embedding = model.encode(section)
                collection.add(
                    documents=section,
                    metadatas={"section_id": section_idx, "page_id": doc_id, "source_file": source_file},
                    ids=f"{doc_id}_section_{section_idx}",
                    embeddings=embedding
                )
    print(f"Dokumente aus {source_file} gespeichert.")

def process_folder(folder_path, collection_name, model, chromaDBclient):
    collection = chromaDBclient.get_collection(collection_name)
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            print(f"Verarbeite Datei: {file_name}")
            try:
                reader = SimpleDirectoryReader(input_files=[file_path])
                documents = reader.load_data()
                store_documents(documents, file_name, model, collection)
            except Exception as e:
                print(f"Fehler bei der Verarbeitung von {file_name}: {e}")
