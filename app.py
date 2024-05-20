import streamlit as st
from gensim.summarization import summarize

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
        
        # Generate summary using TextRank algorithm
        summary = summarize(raw_text)
        
        # Display the summary
        st.subheader("Summary")
        st.write(summary)

# Entry point of the app
if __name__ == "__main__":
    main()
