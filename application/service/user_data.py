import json

def get_user_data(file_path, user_id):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            user_data = json.load(file)
    except Exception as e:
        print(f"Fehler beim Laden der JSON-Datei: {e}")
        return None

    for user in user_data:
        if user["user_id"] == user_id:
            return user
    
    print(f"Benutzer mit ID {user_id} nicht gefunden.")
    return None
