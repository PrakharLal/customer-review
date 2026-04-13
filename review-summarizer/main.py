from src.scraper import scrape_reviews
from src.preprocess import clean_text, chunk_text
from src.llm import analyze_review
import pandas as pd
import time
import json
import re


def extract_product_id(url):
    match = re.search(r'/(\d+)\.p', url)
    if match:
        return match.group(1)
    return None


def build_review_url(product_id):
    return f"https://bestbuy.ugc.bazaarvoice.com/3545syn/{product_id}/syndicatedreviews.htm?sourcename=lg"


def main():
    # 🔥 Take user input INSIDE main (clean design)
    user_input = input("🔗 Enter BestBuy Product URL OR Review URL: ").strip()

    # Case 1: Direct review URL
    if "bazaarvoice" in user_input:
        review_url = user_input

    # Case 2: Product URL
    else:
        product_id = extract_product_id(user_input)

        if not product_id:
            print("❌ Invalid product URL")
            return

        review_url = build_review_url(product_id)

    print(f"\n👉 Using Review URL: {review_url}")

    # 🔥 Use correct variable here
    reviews = scrape_reviews(review_url)

    if not reviews:
        print("❌ No reviews found. Exiting...")
        return

    # Save raw data
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
            time.sleep(1)  # rate limit safety

        final_analysis = " ".join(analysis_parts)

        final_data.append({
            "author": r["author"],
            "rating": r["rating"],
            "review": r["text"],
            "analysis": final_analysis
        })

    df = pd.DataFrame(final_data)
    df.to_csv("data/output.csv", index=False)

    print("\n✅ Data saved to data/output.csv")


if __name__ == "__main__":
    main()