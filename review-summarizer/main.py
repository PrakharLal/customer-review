from src.scraper import scrape_reviews
from src.preprocess import clean_text, chunk_text
from src.llm import analyze_review
import pandas as pd
import time

URL = "https://bestbuy.ugc.bazaarvoice.com/3545syn/11690692/syndicatedreviews.htm?sourcename=lg"
def main():
    reviews = scrape_reviews(URL)

    final_data = []

    for r in reviews:
        cleaned = clean_text(r["text"])
        chunks = chunk_text(cleaned)

        analysis_parts = []

        for chunk in chunks:
            result = analyze_review(chunk)
            analysis_parts.append(result)
            time.sleep(1)  # avoid rate limit

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