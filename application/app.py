from flask import Flask, request, jsonify
from flask_cors import CORS
from config import config
from database.store import setup_collection, store_documents
from service.parser import parse_documents
from service.user_query import process_user_query
from service.chunking import split_document

#############################
### Dokumente verarbeiten ###
#############################
# Initialisierung
print("Initialisiere...")
openAIclient, chromaDBclient, model, parser, pdf_path, json_path, collection_name, sections_path = config()

# Dokumente verarbeiten (einmal beim Start des Servers)
print("Verarbeite Dokumente...")

# Dokumente parsen
parse_documents(pdf_path, json_path, parser)
print("Dokumente erfolgreich geparset und als JSON gespeichert.")

# Dokumente in Abschnitte unterteilen
split_document(json_path, openAIclient, sections_path)
print("Dokumente erfolgreich in Abschnitte unterteilt.")

# Dokumente in ChromaDB speichern
setup_collection(chromaDBclient, collection_name)
store_documents(sections_path, model, chromaDBclient.get_collection(collection_name))
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
    response, sources = process_user_query(user_query, chromaDBclient, openAIclient, collection_name)

    # Antwort und Quellen zurückgeben
    return jsonify({
        "response": response,
        "sources": sources
    })

# Flask-Server starten
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
