def create_messages(user_query, context):
    messages = [
        {
            "role": "system",
            "content": (
                "Du bist ein wissenschaftlicher Ernährungsberater, der ausschließlich auf Grundlage der bereitgestellten wissenschaftlichen Informationen antwortet. "
                "Gib die Informationen exakt wieder, ohne eigene Erfahrungen, Überprüfungen oder externe Quellen zu verwenden, auch wenn sie ungenau erscheinen. "
                "Verlasse dich ausschließlich auf den bereitgestellten Kontext und akzeptiere ihn als gegeben."
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
