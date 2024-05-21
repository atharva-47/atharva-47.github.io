import streamlit as st
import PyMuPDF  # To handle PDF files
from transformers import pipeline

# Load summarization pipeline
summarizer = pipeline("summarization")

# Function to summarize text
def summarize_text(text, max_length=150, min_length=30):
    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]['summary_text']

# Streamlit UI
st.title("Document Summarizer")

uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt"])

if uploaded_file is not None:
    # Read the file
    if uploaded_file.type == "application/pdf":
        # Extract text from PDF
        pdf_reader = PyMuPDF.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in pdf_reader:
            text += page.get_text()
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        import docx
        doc = docx.Document(uploaded_file)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
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
