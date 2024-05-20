import streamlit as st
from transformers import T5ForConditionalGeneration, T5Tokenizer
import pdfplumber
from docx import Document

# Load model and tokenizer
model_name = "t5-small"
model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name)

def summarize(text):
    inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        return text

def extract_text_from_docx(file):
    doc = Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text
    return text

# Streamlit app
st.title('Document Summarization')

# File upload
uploaded_file = st.file_uploader("Upload a DOCX or PDF file", type=["docx", "pdf"])

if uploaded_file is not None:
    file_type = uploaded_file.type.split('/')[1]
    if file_type == "docx":
        text = extract_text_from_docx(uploaded_file)
    elif file_type == "pdf":
        text = extract_text_from_pdf(uploaded_file)

    st.write("### Original Text:")
    st.write(text)

    if st.button('Summarize'):
        summary = summarize(text)
        st.write("### Summary:")
        st.write(summary)
