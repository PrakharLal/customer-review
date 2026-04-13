import requests
from src.config import MISTRAL_API_KEY, API_URL, MODEL

HEADERS = {
    "Authorization": f"Bearer {MISTRAL_API_KEY}",
    "Content-Type": "application/json"
}

def analyze_review(text):
    prompt = f"""
    Analyze the following product review:

    1. Sentiment (Positive / Negative / Neutral)
    2. Short summary (1-2 lines)

    Review:
    {text}
    """

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 150
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)

    if response.status_code != 200:
        raise Exception(f"API Error: {response.text}")

    data = response.json()
    return data["choices"][0]["message"]["content"]