import streamlit as st
from docx import Document
import fitz  # PyMuPDF
import io
from gingerit.gingerit import GingerIt

# Replace with your actual Hugging Face API key
HUGGING_FACE_API_KEY = "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"

def summarize_text(text):
    api_url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {"Authorization": f"Bearer {HUGGING_FACE_API_KEY}"}
    payload = {"inputs": text}
    response = requests.post(api_url, headers=headers, json=payload)
    summary = response.json()[0]['summary_text']
    return summary

def suggest_improvements(text):
    parser = GingerIt()
    result = parser.parse(text)
    corrections = result['corrections']
    suggestions = []
    for correction in corrections:
        message = f"{correction['text']} -> {correction['correct']}"
        suggestions.append(message)
    return suggestions

def process_docx(file):
    doc = Document(file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def process_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    full_text = []
    for page in doc:
        full_text.append(page.get_text())
    return '\n'.join(full_text)

def process_txt(file):
    return file.read().decode('utf-8')

st.title("Document Summarizer and Suggestion App")

uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt"])

if uploaded_file:
    if uploaded_file.name.endswith(".docx"):
        text = process_docx(uploaded_file)
    elif uploaded_file.name.endswith(".pdf"):
        text = process_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".txt"):
        text = process_txt(uploaded_file)

    st.subheader("Original Text")
    st.write(text)

    if st.button("Summarize"):
        summary = summarize_text(text)
        st.subheader("Summary")
        st.write(summary)

    if st.button("Suggest Improvements"):
        suggestions = suggest_improvements(text)
        st.subheader("Suggestions")
        for suggestion in suggestions:
            st.write("- " + suggestion)
