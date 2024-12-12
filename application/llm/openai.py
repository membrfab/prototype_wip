import markdown

def create_messages(user_query, context, user_data, sources):
    user_context = (
        f"Alter: {user_data['age']}, Geschlecht: {user_data['gender']}, "
        f"Größe: {user_data['height_cm']} cm, Gewicht: {user_data['weight_kg']} kg, "
        f"Fitnessziel: {user_data['fitness_goal']}, Allergien: {', '.join(user_data['allergies'])}, "
        f"Erkrankungen: {', '.join(user_data['medical_conditions'])}.\n\n"
    )
    messages = [
        {
            "role": "system",
            "content": (
                "Du bist ein wissenschaftlicher Ernährungsberater, der auf Grundlage der bereitgestellten wissenschaftlichen Informationen Empfehlungen gibt. "
                "Verlasse dich auf den bereitgestellten wissenschaftlichen Kontext. "
                "Ergänze deine Antworten mit einigen Emojis, um sie freundlicher zu gestalten. Übertreibe nicht"
                "Beziehe dich in deinen Antworten auf die Benutzerinformationen, aber nur wenn sie relevant sind. "
                "Verwende die Benutzerinformationen, um die Antworten zu personalisieren. Antworte aber trotzdem nur anhand des wissenschaftlichen Kontexts. "
                "Falls der Benutzer Allergien oder Erkrankungen hat, berücksichtige diese in deinen Empfehlungen."
                "Antworte in der Sprache, in der die Frage des Benutzers gestellt wurde (Benutzerfrage)."
                "Gib am Schluss immer die Quellen des Kontext in einer Liste an."
            )
        },
        {
            "role": "user",
            "content": f"Benutzerfrage (Antworte in der Sprache dieser Frage): {user_query}\n\nBenutzerinformationen: {user_context}\n\nHier ist der wissenschaftliche Kontext:\n{context} \n\n Quellen: {', '.join(sources)}"
        }
    ]
    return messages


def get_response(user_query, context, openAIclient, user_data, sources):
    messages = create_messages(user_query, context, user_data, sources)
    
    try:
        response = openAIclient.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=500,
            temperature=0.2
        )
        #response_html = markdown.markdown(response.choices[0].message.content)
        response_html = markdown.markdown(
            response.choices[0].message.content,
            extensions=[
                "markdown.extensions.extra",
                "markdown.extensions.admonition",
                "markdown.extensions.nl2br"
            ]
        )

        return response_html
    except Exception as e:
        print(f"Fehler bei der Anfrage an OpenAI: {e}")
        return "Fehler bei der Anfrage."
