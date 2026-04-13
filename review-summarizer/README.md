🧠 AI Product Review Analyzer

A Python-based application that extracts customer reviews from e-commerce product pages and uses an LLM to generate meaningful insights such as sentiment, key pros/cons, and an overall product verdict.


-----------------------------------------------------------------------------------------------------------------------

🚀 Overview

When buying a product online, going through hundreds of reviews can be overwhelming. This project simplifies that process by automatically collecting reviews and summarizing them into clear, actionable insights using an LLM.

The application takes a product URL, extracts reviews, processes the text, and generates an overall analysis — all in a clean Streamlit interface.


-----------------------------------------------------------------------------------------------------------------------

✨ Features
	•	🔗 Accepts product URLs (BestBuy supported)
	•	🌐 Scrapes customer reviews along with metadata (author, rating)
	•	🧹 Cleans and preprocesses raw text
	•	📦 Handles long inputs using token-based chunking
	•	🤖 Uses Mistral AI (OpenAI-compatible API) for analysis
	•	📊 Generates:
		    Overall sentiment
            Key pros
            Key cons
            Final verdict
	•	📥 Exports results as CSV
	•	⚠️ Includes error handling for network issues and API failures

-----------------------------------------------------------------------------------------------------------------------

🛠️ Tech Stack
	•	Python
	•	requests, BeautifulSoup
	•	pandas
	•	Streamlit
	•	Mistral AI API
	•	tiktoken
	•	python-dotenv

------------------------------------------------------------------------------------------------------------------------

🧩 Project Structure
review-summarizer/
│
├── src/
│   ├── scraper.py        # Review scraping logic
│   ├── preprocess.py     # Cleaning + token chunking
│   ├── llm.py            # LLM interaction (Mistral API)
│   ├── utils.py          # URL parsing + helpers
│   └── config.py         # API config
│
├── data/
│   └── output.csv        # Generated results
│
├── app.py                # Streamlit UI
├── requirements.txt
├── README.md
└── .env                  # API keys


----------------------------------------------------------------------------------------------------------

🔗 Example Product URL

https://bestbuy.ugc.bazaarvoice.com/3545syn/6535928/syndicatedreviews.htm?sourcename=lg



----------------------------------------------------------------------------------------------------------

🧠 How It Works
	1.	Extract product ID from URL
	2.	Attempt to fetch reviews via Bazaarvoice
	3.	Fallback to alternative method if needed
	4.	Clean and preprocess text
	5.	Split into token-safe chunks
	6.	Send to LLM for analysis
	7.	Merge results into a final summary
	8.	Display insights + export CSV

----------------------------------------------------------------------------------------------------------

⚠️ Limitations
	•	Not all products expose reviews via Bazaarvoice
	•	Some review sections are dynamically loaded and cannot be scraped using simple requests
	•	API rate limits may slow down processing
	•	LLM output may vary slightly due to model behavior

----------------------------------------------------------------------------------------------------------

## ⚙️ How to Run

Follow these steps to run the application locally:


1. Clone the repository:

git clone <your-repo-link>
cd review-summarizer

2. Create and activate virtual environment:

python3 -m venv venv
source venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

4. Set up environment variables

MISTRAL_API_KEY=your_api_key_here

5. Run the Streamlit app

streamlit run app.py

6. Use the application
	•	Paste a BestBuy product URL (preferably LG products)
	•	Click “Analyze Product”
	•	View AI-generated insights
	•	Download results as CSV


📄 Output

The application generates:
	•	Overall sentiment analysis
	•	Key pros and cons
	•	Final verdict
	•	Downloadable CSV with reviews + analysis



⚠️ Notes
	•	Bazaarvoice-supported products work best
	•	Some products may not expose reviews via scraping
	•	Processing time depends on API response speed