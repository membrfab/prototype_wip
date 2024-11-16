import os
import openai
from dotenv import load_dotenv
from chromadb import Client
from sentence_transformers import SentenceTransformer
import nest_asyncio

def initialize_clients():
    # Umgebungsvariablen laden
    load_dotenv()

    # OpenAI-Client initialisieren
    openAIclient = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))

    # ChromaDB-Client initialisieren
    chromaDBclient = Client()

    # SentenceTransformer-Modell initialisieren
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Event-Loop anpassen
    nest_asyncio.apply()

    return openAIclient, chromaDBclient, model
