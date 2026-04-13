import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)  # remove extra spaces
    text = re.sub(r'[^a-zA-Z0-9.,!? ]', '', text)  # remove noise
    return text.strip()


def chunk_text(text, max_words=100):
    words = text.split()
    chunks = []

    for i in range(0, len(words), max_words):
        chunk = " ".join(words[i:i + max_words])
        chunks.append(chunk)

    return chunks