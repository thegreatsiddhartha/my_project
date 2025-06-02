import streamlit as st
import pdfplumber
from pdf2image import convert_from_bytes
import pytesseract
import spacy
import subprocess
import sys
import json
from io import BytesIO
from PIL import Image

# 📦 Load or download SpaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

EXCLUDE_POS = {
    "PRON", "ADV", "CCONJ", "SCONJ", "ADP",
    "INTJ", "DET", "AUX", "PART", "PUNCT"
}

# 📄 Extract text from digital or scanned PDF
def extract_text_from_pdf(uploaded_file):
    layout = {}
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            has_text = any(p.extract_text() for p in pdf.pages)
            if has_text:
                for i, page in enumerate(pdf.pages, start=1):
                    lines = page.extract_text().split('\n') if page.extract_text() else []
                    layout[f"Page {i}"] = {
                        f"Paragraph {j+1}": line
                        for j, line in enumerate(lines)
                        if line.strip()
                    }
                return layout, "digital"
    except Exception:
        pass  # fallback to OCR

    # OCR fallback
    uploaded_file.seek(0)
    images = convert_from_bytes(uploaded_file.read(), dpi=300)
    for i, img in enumerate(images, start=1):
        text = pytesseract.image_to_string(img)
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        layout[f"Page {i}"] = {
            f"Paragraph {j+1}": para
            for j, para in enumerate(paragraphs)
        }
    return layout, "scanned"

# 🧠 Filter valid words using POS tagging
def filter_valid_words(text):
    doc = nlp(text)
    return sorted(set([
        token.text.lower()
        for token in doc
        if token.pos_ not in EXCLUDE_POS and token.is_alpha and not token.is_stop
    ]))

# 🌲 Build nested tree structure
def build_word_tree(raw_layout):
    tree = {}
    for page, paragraphs in raw_layout.items():
        tree[page] = {}
        for para_id, para_text in paragraphs.items():
            words = filter_valid_words(para_text)
            if words:
                tree[page][para_id] = words
    return tree

# 📚 Display tree view
def display_tree_view(tree_data):
    if not tree_data:
        st.warning("No valid words found in this PDF.")
        return
    for page, paragraphs in tree_data.items():
        with st.expander(page):
            for para, words in paragraphs.items():
                with st.expander(para):
                    st.write(", ".join(words))

# 📥 JSON download button
def render_download_button(data):
    json_str = json.dumps(data, indent=2)
    st.download_button(
        "📥 Download JSON",
        json_str,
        file_name="filtered_words.json",
        mime="application/json"
    )

# 🚀 Streamlit UI
st.set_page_config(page_title="PDF Word Extractor", layout="wide")
st.title("📄 PDF Word Extractor")
st.markdown("Upload a PDF (digital or scanned), extract important words, and download the result as JSON.")

pdf_file = st.file_uploader("Upload PDF File", type=["pdf"])

if pdf_file:
    with st.spinner("Processing PDF..."):
        layout_data, source_type = extract_text_from_pdf(pdf_file)
        word_tree = build_word_tree(layout_data)

    st.success(f"Processed as a {source_type.upper()} PDF")

    st.subheader("📚 Collapsible Tree View")
    display_tree_view(word_tree)

    st.subheader("📥 Download Extracted Data")
    render_download_button(word_tree)
else:
    st.info("Upload a PDF file to begin.")

