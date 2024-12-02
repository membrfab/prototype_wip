from database.retriever import query_chromadb, extract_contexts_from_results
from llm.openai import get_response

### Koordiniert die Abfrage an ChromaDB und die Verarbeitung der Antwort durch OpenAI.
def process_user_query(user_query, chromaDBclient, openAIclient, collection_name):
    # ChromaDB abfragen
    results = query_chromadb(user_query, chromaDBclient, collection_name)
    if not results:
        return "Keine relevanten Ergebnisse gefunden.", []

    # Kontext und Quellen extrahieren
    contexts, sources = extract_contexts_from_results(results)
    if not contexts:
        return "Keine relevanten Ergebnisse gefunden.", sources

    # Kontext zusammenfügen
    flat_context = "\n".join(contexts)

    # OpenAI-Response abrufen
    response = get_response(user_query, flat_context, openAIclient)
    return response, sources
