def query_chromadb(query_text, chromaDBclient, collection_name, user_data, n_results=8):
    try:
        # Benutzerinformationen in den Abfragetext einbinden
        user_context = (
            f"Geschlecht: {user_data['gender']}, "
            f"Fitnessziel: {user_data['fitness_goal']}, Allergien: {', '.join(user_data['allergies'])}, "
            f"Erkrankungen: {', '.join(user_data['medical_conditions'])}.\n\n"
        )
        query_text = f"Frage: {query_text} Benutzerinformationen: {user_context}"

        # ChromaDB-Abfrage ausführen
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
                source_file = metadata.get("original_pdf", "Unbekannt")
                sources.add(source_file)
            contexts.append(doc)
    
    return contexts, list(sources)
