from database.retriever import query_chromadb, extract_contexts_from_results
from llm.openai import get_response
from service.user_data import get_user_data

### Koordiniert die Abfrage an ChromaDB und die Verarbeitung der Antwort durch OpenAI.
def process_user_query(user_query, chromaDBclient, openAIclient, collection_name, user_id):

    # Benutzerdaten laden
    user_data = get_user_data("data/users/users.json", user_id)

    # ChromaDB abfragen
    results = query_chromadb(user_query, chromaDBclient, collection_name, user_data)
    if not results:
        return "Keine relevanten Ergebnisse gefunden.", []

    # Kontext und Quellen extrahieren
    contexts, sources = extract_contexts_from_results(results)
    if not contexts:
        return "Keine relevanten Ergebnisse gefunden.", sources

    # Kontext zusammenfügen
    flat_context = "\n".join(contexts)

    # OpenAI-Response abrufen
    response = get_response(user_query, flat_context, openAIclient, user_data, sources)
    return response, sources
