import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.tokenize import sent_tokenize

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

# Function to summarize document
def summarize_document(document, num_sentences=2):
    # Split document into sentences
    sentences = sent_tokenize(document)
    # Preprocess the document
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
    
    # Paragraph input widget
    paragraph = st.text_area("Enter paragraph")
    
    # Summarize the paragraph when input is provided
    if paragraph:
        # Process the paragraph and generate summary
        summary = summarize_document(paragraph)
        
        # Display the summary
        st.subheader("Summary")
        st.write(summary)

# Entry point of the app
if __name__ == "__main__":
    main()
