import requests
import time
from src.config import MISTRAL_API_KEY, API_URL, MODEL

HEADERS = {
    "Authorization": f"Bearer {MISTRAL_API_KEY}",
    "Content-Type": "application/json"
}



def call_llm(payload, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=15)

            
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]

            
            elif response.status_code == 429:
                print(f"Rate limited... retry {attempt+1}")
                time.sleep(2 * (attempt + 1))  # exponential wait

            
            else:
                print("API Error:", response.text)
                return "LLM analysis failed"

        except requests.exceptions.Timeout:
            print("Request timed out")
        
        except requests.exceptions.ConnectionError:
            print("Connection error")

        except requests.exceptions.RequestException as e:
            print("Request failed:", e)

        # wait before retry
        time.sleep(1)

    return "⚠️ LLM failed after multiple retries"



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

    return call_llm(payload)



def analyze_overall_reviews(all_reviews_text):
    prompt = f"""
    You are an expert product analyst.

    Analyze the following customer reviews and provide:

    1. Overall Sentiment (Positive / Negative / Mixed)
    2. Key Pros (bullet points)
    3. Key Cons (bullet points)
    4. Final Verdict (2-3 lines)

    Reviews:
    {all_reviews_text}
    """

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 400
    }

    return call_llm(payload)