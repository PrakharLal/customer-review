import re
import requests


def extract_product_id(url):
    # Works for numeric + alphanumeric IDs
    match = re.search(r'/([A-Za-z0-9]+)(?:\.p)?$', url)
    return match.group(1) if match else None


def build_review_url(product_id):
    return f"https://bestbuy.ugc.bazaarvoice.com/3545syn/{product_id}/syndicatedreviews.htm?sourcename=lg"


def fetch_reviews_api(product_id):
    print("🌐 Fetching from BestBuy API...")

    try:
        url = f"https://api.bestbuy.com/v1/reviews(productId={product_id})?format=json&apiKey=YOUR_API_KEY"

        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            print("❌ API request failed")
            return []

        data = response.json()

        reviews = []

        for r in data.get("reviews", []):
            reviews.append({
                "text": r.get("comment"),
                "rating": r.get("rating"),
                "author": r.get("reviewer", {}).get("name")
            })

        return reviews

    except Exception as e:
        print("⚠️ API error:", e)
        return []