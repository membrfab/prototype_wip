### Teilt den Text in Abschnitte auf
def split_document(content):
    paragraphs = content.split("\n\n")  # Doppelter Zeilenumbruch
    return [p.strip() for p in paragraphs if p.strip()]
