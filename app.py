import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.tokenize import sent_tokenize
import PyPDF2
import docx

# Download NLTK resources
nltk.download('punkt')

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
    # Split document into sentences
    sentences = sent_tokenize(document)
    # Preprocess the sentences
    processed_sentences = [preprocess_text(sentence) for sentence in sentences]
    # Calculate TF-IDF vectors
    tfidf_matrix = calculate_tfidf_vectors(processed_sentences)
    # Calculate cosine similarity between sentences
    sentence_similarity = cosine_similarity(tfidf_matrix, tfidf_matrix)
    # Average similarity scores for each sentence
    avg_similarity = sentence_similarity.mean(axis=1)
    # Sort sentences by their average similarity scores
    ranked_sentences = [sentences[i] for i in avg_similarity.argsort()[::-1]]
    # Extract top N sentences as summary
    summary = ' '.join(ranked_sentences[:num_sentences])
    return summary

# Define the Streamlit app
def main():
    st.title("Document Summarizer")
    
    # File upload widget
    uploaded_file = st.file_uploader("Upload a document", type=["pdf", "docx", "txt"])
    
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
