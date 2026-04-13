import os
from dotenv import load_dotenv

load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

if not MISTRAL_API_KEY:
    raise ValueError("❌ MISTRAL_API_KEY not found in .env")

API_URL = "https://api.mistral.ai/v1/chat/completions"
MODEL = "mistral-small"
MAX_TOKENS = 200