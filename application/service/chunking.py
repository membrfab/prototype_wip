import os
import json
from pydantic import BaseModel
from typing import List

# Pydantic-Klassen für die Antwortstruktur
class Section(BaseModel):
    content: str
    tags: List[str]

class DocumentSections(BaseModel):
    sections: List[Section]

# service/chunking.py
def split_document(json_path, openAIclient, output_dir, context_size=2):
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
                print(f"Verarbeite Datei: {json_path}/{file_name}")
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

                        try:
                            print(f"\nSeite {i + 1} von {total_pages} wird durch OpenAI in Abschnitte aufgeteilt...\n")
                            completion = openAIclient.beta.chat.completions.parse(
                                model="gpt-4o-mini",
                                messages=[
                                    {
                                        "role": "system",
                                        "content": (
                                            "You are an expert in text segmentation. Your task is to divide the text into meaningful sections without altering or adding any information.\n"
                                            "The following requirements must be strictly adhered to:\n"
                                            "1. The original language of the text must remain unchanged under any circumstances.\n"
                                            "   - Texts in German must remain in German.\n"
                                            "   - Texts in English must remain in English.\n"
                                            "   - Any translation, whether intentional or unintentional, is an error.\n"
                                            "2. Remove and ignore irrelevant information, such as:\n"
                                            "   - Metadata (e.g., page numbers, footnotes),\n"
                                            "   - Bibliographies, references, appendices\n"
                                            "   - Content unrelated to nutrition, health, or related fields.\n"
                                            "3. The main content of the text must remain unchanged.\n"
                                            "4. Each section must be thematically coherent and:\n"
                                            "   - At least 200 characters long (unless the section ends logically earlier).\n"
                                            "   - No longer than 1500 characters.\n"
                                            "   - Include at least 5 tags describing the most important themes of the section.\n"
                                            "5. After segmentation, verify that the language is in the same language as the original text.\n"
                                            "6. Remove any sections explicitly labeled as bibliographies, references, or similar. Do not generate or include any new information for these sections."
                                            "7. Do not generate or invent any new content under any circumstances. If a bibliography or reference section is found, remove it entirely."
                                        )
                                    },
                                    {"role": "user", "content": page_context},
                                ],
                                response_format=DocumentSections,
                                temperature=0.0
                            )

                            structured_data = completion.choices[0].message.parsed

                            for section in structured_data.sections:
                                results.append({
                                    "section": section_id,
                                    "content": section.content,
                                    "tags": section.tags
                                })
                                section_id += 1

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
