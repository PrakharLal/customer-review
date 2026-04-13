import streamlit as st
import pandas as pd
from src.preprocess import chunk_text_by_tokens

from src.scraper import scrape_reviews
from src.llm import analyze_overall_reviews
from src.utils import extract_product_id, build_review_url, fetch_reviews_api

# 🎨 PAGE CONFIG
st.set_page_config(page_title="AI Review Analyzer", layout="centered")

# 🔥 CUSTOM CSS (MODERN UI)
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

/* Glass Card Improved */
.glass {
    background: rgba(255, 255, 255, 0.08);
    padding: 30px;
    border-radius: 20px;
    backdrop-filter: blur(15px);
    box-shadow: 0px 8px 40px rgba(0,0,0,0.3);
    margin-top: 30px;
    line-height: 1.7;
}

/* Improve text readability */
.glass p, .glass li {
    font-size: 16px;
    color: #e6e6e6;
}

/* Section headings */
.glass h3 {
    color: #ffffff;
    margin-bottom: 15px;
}

/* Button */
.stButton>button {
    background: linear-gradient(90deg, #ff7e5f, #feb47b);
    border-radius: 12px;
    font-weight: bold;
    padding: 10px 20px;
}

/* Success box */
.stAlert {
    border-radius: 10px;
}
</style>
    
""", unsafe_allow_html=True)


# 🧠 HEADER
st.markdown("<h1>🧠 AI Product Review Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Get intelligent insights from product reviews</p>", unsafe_allow_html=True)

# 🔗 INPUT
user_input = st.text_input("🔗 Enter BestBuy Product URL OR Review URL")

# 🚀 BUTTON
if st.button("🚀 Analyze Product"):

    if not user_input:
        st.error("Please enter a URL")
        st.stop()

    with st.spinner("🔍 Fetching reviews..."):

        if "bazaarvoice" in user_input:
            reviews = scrape_reviews(user_input)
        else:
            product_id = extract_product_id(user_input)

            if not product_id:
                st.error("❌ Invalid URL")
                st.stop()

            review_url = build_review_url(product_id)
            reviews = scrape_reviews(review_url)

            if not reviews:
                st.warning("⚠️ Trying API fallback...")
                reviews = fetch_reviews_api(product_id)

    if not reviews:
        st.error("❌ No reviews found")
        st.stop()

    st.success(f"✅ {len(reviews)} reviews collected")

    # 🔥 LIMIT REVIEWS
    reviews = reviews[:20]


    all_reviews_text = " ".join([r["text"] for r in reviews])
    chunks = chunk_text_by_tokens(all_reviews_text, max_tokens=500)
    all_reviews_text = all_reviews_text[:4000]

    # 🧠 LLM
    with st.spinner("🧠 Generating insights..."):
        
        chunks = chunk_text_by_tokens(all_reviews_text, max_tokens=500)

        analysis_parts = []

        for chunk in chunks:
            result = analyze_overall_reviews(chunk)
            analysis_parts.append(result)

        overall_analysis = " ".join(analysis_parts)

    # 💎 GLASS CARD OUTPUT
    st.markdown('<div class="glass">', unsafe_allow_html=True)

    st.markdown("### 🧠 Overall Product Insights")

# 👇 THIS FIXES MARKDOWN FORMATTING
    st.markdown(overall_analysis)

    st.markdown('</div>', unsafe_allow_html=True)

    # 📥 CSV DOWNLOAD
    df = pd.DataFrame(reviews)
    df["overall_analysis"] = overall_analysis

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download CSV",
        data=csv,
        file_name="reviews_analysis.csv",
        mime="text/csv"
    )