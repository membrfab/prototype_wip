from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

def split_document(content, n_topics=3):
    try:
        # Text in größere Abschnitte aufteilen
        paragraphs = content.split("\n\n")
        if len(paragraphs) < 4:
            paragraphs = content.split("\n")

        vectorizer = CountVectorizer(max_features=1000)
        X = vectorizer.fit_transform(paragraphs)

        # LDA-Themenmodell
        lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
        lda.fit(X)

        # Themenzuweisungen
        topics = lda.transform(X)
        sections = []
        current_section = []
        current_topic = topics[0].argmax()

        # Toleranzschwelle für Themenwechsel
        for idx, topic_dist in enumerate(topics):
            topic = topic_dist.argmax()
            if abs(topic_dist[topic] - topic_dist[current_topic]) > 0.2:  # Toleranz 20%
                sections.append(" ".join(current_section))
                current_section = []
                current_topic = topic
            current_section.append(paragraphs[idx])

        if current_section:
            sections.append(" ".join(current_section))

        # Nachträgliche Zusammenführung kleiner Abschnitte
        MIN_SECTION_LENGTH = 150 
        merged_sections = []
        current_section = []

        for section in sections:
            current_section.append(section)
            if len(" ".join(current_section).split()) > MIN_SECTION_LENGTH:
                merged_sections.append(" ".join(current_section))
                current_section = []

        if current_section:
            merged_sections.append(" ".join(current_section))

        return merged_sections
    except Exception as e:
        print(f"Fehler bei der thematischen Segmentierung: {e}")
        return []
