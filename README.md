# 📄 PDF Word Extractor (Streamlit App)

This is a free, web-based app that extracts key words from **digital or scanned PDFs**, preserving layout structure, and lets you **view and download results as a collapsible tree**.

## 🚀 Features

- ✅ Accepts both digital and scanned PDFs
- ✅ Automatically detects and handles OCR
- ✅ Filters out: pronouns, adverbs, conjunctions, prepositions, interjections, articles, modals, helping verbs, punctuation
- ✅ Organizes results as Page → Paragraph → Words
- ✅ JSON download of extracted word data
- ✅ 100% Free to run on [Streamlit Cloud](https://streamlit.io/cloud)

## 📦 Setup Instructions

1. **Clone the repository** or create a new repo and add:
    - `app.py` (the main app file)
    - `requirements.txt`
    - `README.md`

2. **Install dependencies locally (optional):**

    ```bash
    pip install -r requirements.txt
    python -m spacy download en_core_web_sm
    ```

3. **Deploy to Streamlit Cloud:**
    - Go to [streamlit.io/cloud](https://streamlit.io/cloud)
    - Connect your GitHub repo
    - Streamlit auto-deploys your app
    - In the Streamlit Cloud shell (first run), run:
      ```bash
      python -m spacy download en_core_web_sm
      ```

4. **Visit your public app link and start uploading PDFs!**
