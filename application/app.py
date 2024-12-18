from flask import Flask, request, jsonify
from flask_cors import CORS
from config import config
from service.user_query import process_user_query

# Initialisierung
print("Initialisiere Clients & Starte Webserver...")
openAIclient, chromaDBclient, model, parser, pdf_path, json_path, collection_name, sections_path = config()

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
    response, sources = process_user_query(user_query, chromaDBclient, openAIclient, collection_name, user_id=2)

    # Antwort und Quellen zurückgeben
    return jsonify({
        "response": response,
        "sources": sources
    })

# Flask-Server starten
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
