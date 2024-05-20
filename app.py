import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import PyPDF2
import docx

# Function to preprocess text
def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()
    return text

# Function to calculate TF-IDF vectors
def calculate_tfidf_vectors(documents):
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
    return tfidf_matrix

# Function to read text from PDF
def read_pdf(file):
    pdf_reader = PyPDF2.PdfFileReader(file)
    text = ""
    for page_num in range(pdf_reader.numPages):
        page = pdf_reader.getPage(page_num)
        text += page.extractText()
    return text

# Function to read text from DOCX
def read_docx(file):
    doc = docx.Document(file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text
    return text

# Function to summarize document
def summarize_document(document, num_sentences=2):
    # Preprocess the document
    processed_document = preprocess_text(document)
    # Calculate TF-IDF vectors
    tfidf_matrix = calculate_tfidf_vectors([processed_document,])
    # Calculate cosine similarity between sentences and document
    cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)
    # Get top N similar sentences
    sentence_scores = list(cosine_similarities.argsort()[0][-num_sentences:])
    # Extract and return summary
    summary = ' '.join([sentences[i] for i in sentence_scores])
    return summary

# Define the Streamlit app
def main():
    st.title("Document Summarizer")
    
    # File upload widget
    uploaded_file = st.file_uploader("Upload a document", type=["txt", "pdf", "docx"])
    
    # Summarize the document when uploaded
    if uploaded_file is not None:
        # Read the uploaded file based on file type
        if uploaded_file.type == "text/plain":  # For text files
            raw_text = uploaded_file.read().decode("utf-8")
        elif uploaded_file.type == "application/pdf":  # For PDF files
            raw_text = read_pdf(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":  # For DOCX files
            raw_text = read_docx(uploaded_file)
        
        # Process the document and generate summary
        summary = summarize_document(raw_text)
        
        # Display the summary
        st.subheader("Summary")
        st.write(summary)

# Entry point of the app
if __name__ == "__main__":
    main()
