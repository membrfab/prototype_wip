import os
import json

# service/chunking.py
def split_document(json_path, openAIclient, output_dir, context_size=3):
    """
    Teilt Dokumente in Abschnitte mit optionaler Speicherung in separaten JSON-Dateien.
    """
    try:
        # Überprüfen, ob der Import-Pfad existiert
        if not os.path.exists(json_path):
            print(f"Der Pfad {json_path} existiert nicht.")
            return

        # Ergebnisverzeichnis erstellen, falls nicht vorhanden
        os.makedirs(output_dir, exist_ok=True)

        # JSON-Dateien im Verzeichnis verarbeiten
        for file_name in os.listdir(json_path):
            file_path = os.path.join(json_path, file_name)
            output_file = os.path.join(output_dir, f"{file_name}")

            if os.path.isfile(file_path) and file_name.endswith(".json"):
                print(f"\n---------------------------------------------------------")
                print(f"Verarbeite Datei: {file_name}")
                print("---------------------------------------------------------")

                try:
                    # JSON-Datei laden
                    with open(file_path, "r", encoding="utf-8") as json_file:
                        document = json.load(json_file)

                    # Dokument in Seiten aufteilen
                    pages = [doc["text"] for doc in document if "text" in doc]
                    total_pages = len(pages)
                    results = []
                    section_id = 1

                    for i in range(total_pages):
                        current_text = pages[i]
                        context_before = pages[i - 1].split("\n")[-context_size:] if i > 0 else []
                        context_after = pages[i + 1].split("\n")[:context_size] if i < total_pages - 1 else []
                        page_context = "\n".join(context_before + [current_text] + context_after).strip()

                        print(page_context)
                        # OpenAI API-Aufruf
                        try:
                            print(f"\nSeite {i + 1} von {total_pages} wird durch OpenAI in Abschnitte aufgeteilt...\n")
                            response = openAIclient.chat.completions.create(
                                model="gpt-4",
                                messages=[
                                    {
                                        "role": "system",
                                        "content": (
                                            "Du bist ein Experte für Textanalyse. Deine Aufgabe ist es, den folgenden wissenschaftlichen Text zum Thema Ernährung in sinnvolle Abschnitte zu unterteilen. "
                                            "Jeder Abschnitt sollte eine logische, thematische Einheit darstellen und mindestens 300 Zeichen lang sein, es sei denn, der Abschnitt endet natürlich oder logisch. "
                                            "Abschnitte sollen nicht willkürlich geteilt werden und thematisch zusammenhängende Teile umfassen. "
                                            "Stelle sicher, dass Abschnitte inhaltlich vollständig sind und keine wichtigen Informationen abgeschnitten werden. "
                                            "Gib die Ergebnisse im JSON-Format als Liste aus, wobei jedes Listenelement ein Wörterbuch mit den folgenden Schlüsseln ist:\n\n"
                                            "- `content`: Der vollständige Text des Abschnitts.\n"
                                            "- `tags`: Eine Liste von genau 5 prägnanten Schlagwörtern, die den Abschnitt zusammenfassen und beschreiben.\n\n"
                                            "Beispiele für die JSON-Ausgabe:\n"
                                            "[\n"
                                            "  {\n"
                                            "    \"content\": \"Dieser Abschnitt behandelt die grundlegenden Prinzipien der Ernährung und ihre Bedeutung für die Gesundheit...\",\n"
                                            "    \"tags\": [\"Ernährung\", \"Gesundheit\", \"Nährstoffe\", \"Diät\", \"Wissenschaft\"]\n"
                                            "  },\n"
                                            "  {\n"
                                            "    \"content\": \"Dieser Abschnitt erklärt die Methode der Licht-Diät und ihre Vorteile...\",\n"
                                            "    \"tags\": [\"Licht-Diät\", \"Photosynthese\", \"Sonnenlicht\", \"Energie\", \"Regeneration\"]\n"
                                            "  }\n"
                                            "]\n\n"
                                            "Wichtig: Achte darauf, dass die Abschnitte thematisch sinnvoll sind, inhaltlich nicht verändert werden und die Ausgabe vollständig im JSON-Format vorliegt."
                                        ),
                                    },
                                    {"role": "user", "content": page_context},
                                ],
                                max_tokens=3000,
                                temperature=0.2,
                            )
                            # Verarbeiten der Antwort
                            if response.choices:
                                structured_data = json.loads(response.choices[0].message.content)
                                print(structured_data)

                                for section in structured_data:
                                    print(section)
                                    results.append({
                                        "section": section_id,
                                        "content": [section["content"]],
                                        "tags": section["tags"]
                                    })
                                    section_id += 1
                            else:
                                print(f"Keine gültigen Antworten in der API-Response für Seite {i + 1}.")

                        except Exception as e:
                            print(f"Fehler bei Seite {i + 1}: {e}")
                            continue

                    # Ergebnisse speichern
                    with open(output_file, "w", encoding="utf-8") as file:
                        json.dump(results, file, ensure_ascii=False, indent=4)
                        print(f"Ergebnisse gespeichert in {output_file}")

                except Exception as e:
                    print(f"Fehler beim Verarbeiten der Datei {file_name}: {e}")

    except Exception as e:
        print(f"Fehler bei split_document: {e}")
