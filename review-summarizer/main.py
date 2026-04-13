from src.scraper import scrape_reviews
from src.preprocess import clean_text, chunk_text
from src.llm import analyze_review
from src.utils import extract_product_id, build_review_url, fetch_reviews_api
import pandas as pd
import time
import json


def main():
    user_input = input("🔗 Enter BestBuy Product URL OR Review URL: ").strip()

    # Step 1: Detect source
    if "bazaarvoice" in user_input:
        print("🧠 Detected: Bazaarvoice URL")
        reviews = scrape_reviews(user_input)

    else:
        product_id = extract_product_id(user_input)

        if not product_id:
            print("❌ Invalid product URL")
            return

        print(f"🧠 Extracted Product ID: {product_id}")

        # Step 2: Try Bazaarvoice first
        review_url = build_review_url(product_id)
        print(f"👉 Trying Bazaarvoice: {review_url}")

        reviews = scrape_reviews(review_url)

        # Step 3: Fallback to API
        if not reviews:
            print("⚠️ Bazaarvoice failed. Trying BestBuy API...")
            reviews = fetch_reviews_api(product_id)

    # Step 4: Final fallback
    if not reviews:
        print("\n❌ No reviews found from any source.")
        print("👉 This product may use a protected or unsupported system.")
        return

    print(f"\n✅ Total Reviews Collected: {len(reviews)}")

    # Save raw
    with open("data/raw_reviews.json", "w") as f:
        json.dump(reviews, f, indent=4)

    final_data = []

    for idx, r in enumerate(reviews):
        print(f"\n🔄 Processing review {idx+1}/{len(reviews)}")

        cleaned = clean_text(r["text"])
        chunks = chunk_text(cleaned)

        analysis_parts = []

        for chunk in chunks:
            try:
                result = analyze_review(chunk)
            except Exception as e:
                print("⚠️ API error:", e)
                result = "API FAILED"

            analysis_parts.append(result)
            time.sleep(1)

        final_analysis = " ".join(analysis_parts)

        final_data.append({
            "author": r.get("author", "N/A"),
            "rating": r.get("rating", "N/A"),
            "review": r.get("text", ""),
            "analysis": final_analysis
        })

    df = pd.DataFrame(final_data)
    df.to_csv("data/output.csv", index=False)

    print("\n🎉 DONE! Data saved to data/output.csv")


if __name__ == "__main__":
    main()