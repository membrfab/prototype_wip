from flask import Flask, request, jsonify
from flask_cors import CORS
from config import initialize_clients
from database.store import setup_collection, process_folder
from service.user_query import process_user_query

# Source-Pfad
import_path = "../data/import"

# Store-Pfad
storage_path = "../data/storage"

# Flask-App initialisieren
app = Flask(__name__)
CORS(app)

# Initialisierung
print("Initialisiere Clients...")
openAIclient, chromaDBclient, model = initialize_clients(storage_path)

# Dokumente verarbeiten (einmal beim Start des Servers)
print("Verarbeite Dokumente...")
collection_name = "nutrition_facts"
setup_collection(chromaDBclient, collection_name)
process_folder(import_path, collection_name, model, chromaDBclient)
print("Dokumente erfolgreich verarbeitet.")

# Endpoint für Benutzerabfragen
@app.route('/query', methods=['POST'])
def query_endpoint():
    data = request.json  # JSON-Daten aus der Anfrage lesen
    user_query = data.get("user_query", "")

    if not user_query:
        return jsonify({"error": "Die Anfrage darf nicht leer sein"}), 400

    # Benutzeranfrage verarbeiten
    response, sources = process_user_query(user_query, chromaDBclient, openAIclient)

    # Antwort und Quellen zurückgeben
    return jsonify({
        "response": response,
        "sources": sources
    })

# Flask-Server starten
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
