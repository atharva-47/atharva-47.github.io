import streamlit as st
import requests

# Define the TextAnalysis API key
API_KEY = "your_api_key_here"

# Define the TextAnalysis Summarization API endpoint
SUMMARIZATION_API_URL = "https://api.textanalysis.ai/text-summarizer"

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
        
        # Make request to the Summarization API
        data = {
            "text": raw_text,
            "sentences_count": 2  # Adjust this parameter as needed
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        response = requests.post(SUMMARIZATION_API_URL, json=data, headers=headers)
        
        # Check if request was successful
        if response.status_code == 200:
            # Get the summary from the response
            summary = response.json().get("summary")
            
            # Display the summary
            st.subheader("Summary")
            st.write(summary)
        else:
            st.error("Failed to summarize the document. Please try again.")

# Entry point of the app
if __name__ == "__main__":
    main()
