import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from config import config
from service.user_query import process_user_query
from database.store import setup_collection, store_documents

# Initialisierung
print("Initialisiere Clients & Starte Webserver...")
openAIclient, chromaDBclient, model, parser, pdf_path, json_path, collection_name, sections_path = config()

# Dokumente in ChromaDB speichern
setup_collection(chromaDBclient, collection_name, model)
store_documents(sections_path, pdf_path, model, chromaDBclient.get_collection(collection_name))
print("Dokumente erfolgreich in ChromaDB gespeichert.")
print("\nDokumente erfolgreich verarbeitet.")

######################
### Flask-Server  ###
######################
# Flask-App initialisieren
app = Flask(__name__)
CORS(app)

# Endpoint für Benutzerabfragen
@app.route('/query', methods=['POST'])
def query_endpoint():
    data = request.json  # JSON-Daten aus der Anfrage lesen
    user_query = data.get("user_query", "")

    if not user_query:
        return jsonify({"error": "Die Anfrage darf nicht leer sein"}), 400

    # Benutzeranfrage verarbeiten
    response, sources = process_user_query(user_query, chromaDBclient, openAIclient, collection_name, user_id=1)

    # Antwort und Quellen zurückgeben
    return jsonify({
        "response": response,
        "sources": sources
    })

@app.route('/')
def home():
    return "Service is running!"

# Flask-Server starten
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    print(f"Starting Flask server on port {port}")
    app.run(host='0.0.0.0', port=port)