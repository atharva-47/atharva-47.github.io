import streamlit as st
import fitz  # PyMuPDF
from transformers import pipeline
import docx2txt

# Load summarization pipeline
summarizer = pipeline("summarization")

# Function to summarize text
def summarize_text(text, max_length=150, min_length=30):
    # Split text into chunks if it's too long for the model
    num_iters = len(text) // 1000 + 1
    summarized_text = ""
    for i in range(num_iters):
        start = i * 1000
        end = (i + 1) * 1000
        summary = summarizer(text[start:end], max_length=max_length, min_length=min_length, do_sample=False)
        summarized_text += summary[0]['summary_text'] + " "
    return summarized_text

# Streamlit UI
st.title("Document Summarizer")

uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt"])

if uploaded_file is not None:
    # Read the file
    if uploaded_file.type == "application/pdf":
        # Extract text from PDF
        pdf_reader = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in pdf_reader:
            text += page.get_text()
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        text = docx2txt.process(uploaded_file)
    else:
        text = uploaded_file.read().decode("utf-8")

    # Display the original document
    st.subheader("Original Document")
    st.write(text)

    # Summarize the document
    summary = summarize_text(text)

    # Display the summary
    st.subheader("Summary")
    st.write(summary)
