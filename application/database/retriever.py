def query_chromadb(query_text, chromaDBclient, collection_name, n_results=5):
    try:
        # Zugriff auf die entsprechende Sammlung
        collection = chromaDBclient.get_collection(collection_name)
        results = collection.query(query_texts=[query_text], n_results=n_results)
        return results
    except Exception as e:
        print(f"Fehler bei der Abfrage von ChromaDB: {e}")
        return None

def extract_contexts_from_results(results):
    if not results or "documents" not in results or "metadatas" not in results:
        return [], []

    contexts = []
    sources = set()

    for outer_idx, docs in enumerate(results["documents"]):
        for inner_idx, doc in enumerate(docs):
            # Extrahiere zugehörige Metadaten
            metadata_list = results["metadatas"][outer_idx]
            if len(metadata_list) > inner_idx:
                metadata = metadata_list[inner_idx]
                source_file = metadata.get("source_file", "Unbekannt")
                sources.add(source_file)
            contexts.append(doc)
    
    return contexts, list(sources)
