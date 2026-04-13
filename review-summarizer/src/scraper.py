import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_reviews(url):
    print("🌐 Fetching page...")

    response = requests.get(url, headers=HEADERS, timeout=10)

    if response.status_code != 200:
        raise Exception(f"Failed: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")

    reviews = []

    # ✅ Correct container
    review_blocks = soup.select(".BVRRContentReview")

    print(f"🔍 Found {len(review_blocks)} reviews")

    for r in review_blocks:
        try:
            text = r.select_one(".BVRRReviewText").get_text(strip=True)
            rating = r.select_one(".BVRRRatingNumber").get_text(strip=True)
            author = r.select_one(".BVRRNickname").get_text(strip=True)

            reviews.append({
                "text": text,
                "rating": rating,
                "author": author
            })

        except Exception as e:
            print("Skipping:", e)

    return reviews