import os
import openai
from dotenv import load_dotenv
from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer
import nest_asyncio
from llama_parse import LlamaParse

def config():
    # Umgebungsvariablen laden
    load_dotenv()

    # OpenAI-Client initialisieren
    openAIclient = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))

    # Parser konfigurieren
    parser = LlamaParse(
        input_value="application/json",
        parsing_instructions="Remove all irrelevant information from the scientific papers and only keep the main content. Especially remove the bibliography.",
        languages=["en, de"],
    )

    # Pfade definieren
    root = os.path.dirname(os.path.abspath(os.path.join(os.path.dirname(__file__))))
    pdf_path = os.path.join(root, "data/raw")
    json_path = os.path.join(root, "data/parsed")
    embeddings_path = os.path.join(root, "data/embeddings")
    sections_path = os.path.join(root, "data/sections")

    # ChromaDB-Client initialisieren
    collection_name = "nutrition_papers"
    chromaDBclient = PersistentClient(path=embeddings_path)

    # SentenceTransformer-Modell initialisieren
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Event-Loop anpassen
    nest_asyncio.apply()

    return openAIclient, chromaDBclient, model, parser, pdf_path, json_path, collection_name, sections_path
