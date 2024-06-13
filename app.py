import streamlit as st
from docx import Document
import fitz  # PyMuPDF
import os

def summarize_text(text):
    # Implement a simple summarizer
    return ' '.join(text.split()[:50])  # Example: First 50 words

def suggest_improvements(text):
    # Implement a simple suggestion engine
    return ["Consider simplifying complex sentences.", "Check for passive voice usage."]

def process_docx(file):
    doc = Document(file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def process_pdf(file):
    doc = fitz.open(file)
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

    summary = summarize_text(text)
    st.subheader("Summary")
    st.write(summary)

    suggestions = suggest_improvements(text)
    st.subheader("Suggestions")
    for suggestion in suggestions:
        st.write("- " + suggestion)
