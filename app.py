import streamlit as st
import os
import docx
import PyMuPDF
import nltk
from transformers import pipeline

# Download the necessary NLTK resources
nltk.download('punkt')

# Set the page configuration
st.set_page_config(page_title="Document Summarizer", page_icon=":books:")

# Create the Streamlit app
st.title("Document Summarizer")

# File upload section
st.subheader("Upload a Document")
uploaded_file = st.file_uploader("Choose a file", type=["docx", "pdf", "txt"])

if uploaded_file is not None:
    # Save the uploaded file to disk
    file_path = os.path.join("uploads", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Process the document based on the file type
    if uploaded_file.name.endswith(".docx"):
        doc = docx.Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    elif uploaded_file.name.endswith(".pdf"):
        doc = PyMuPDF.Document(file_path)
        text = "\n".join([page.get_text() for page in doc])
    elif uploaded_file.name.endswith(".txt"):
        with open(file_path, "r") as f:
            text = f.read()

    # Summarize the text using the Hugging Face Transformers library
    summarizer = pipeline("summarization")
    summary = summarizer(text, max_length=200, min_length=50, do_sample=False)[0]["summary_text"]

    # Provide suggestions based on the document type
    st.subheader("Document Summary")
    st.write(summary)

    st.subheader("Suggestions")
    if uploaded_file.name.endswith(".docx"):
        st.write("- Consider using more concise language and shorter sentences.")
        st.write("- Ensure that the document is well-structured with clear headings and subheadings.")
    elif uploaded_file.name.endswith(".pdf"):
        st.write("- Check for any inconsistencies in formatting and layout.")
        st.write("- Ensure that the document is easy to navigate and understand.")
    elif uploaded_file.name.endswith(".txt"):
        st.write("- Consider adding formatting and structure to improve readability.")
        st.write("- Ensure that the document is free of spelling and grammatical errors.")
