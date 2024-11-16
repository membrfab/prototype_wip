def create_messages(user_query, context):
    messages = [
        {
            "role": "system",
            "content": (
                "Du bist ein wissenschaftlicher Ernährungsberater. "
                "Beantworte Fragen des Nutzers ausschließlich basierend auf dem bereitgestellten Kontext. "
                "Nutze keine externen Quellen oder eigenes Wissen."
            )
        },
        {
            "role": "user",
            "content": f"Hier ist der Kontext:\n{context}\n\nFrage: {user_query}"
        }
    ]
    return messages

def get_response(user_query, context, openAIclient):
    messages = create_messages(user_query, context)
    
    try:
        response = openAIclient.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=200,
            temperature=0.5
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Fehler bei der Anfrage an OpenAI: {e}")
        return "Fehler bei der Anfrage."
