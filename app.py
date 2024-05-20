import streamlit as st
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

# Define the Streamlit app
def main():
    st.title("Document Summarizer")
    
    # File upload widget
    uploaded_file = st.file_uploader("Upload a document", type=["pdf", "docx", "txt"])
    
    # Summarize the document when uploaded
    if uploaded_file is not None:
        # Read the uploaded file based on file type
        raw_text = uploaded_file.read().decode("utf-8")
        
        # Parse the text and generate summary using LSA algorithm
        parser = PlaintextParser.from_string(raw_text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, 2)  # Adjust the number of sentences in the summary
        
        # Display the summary
        st.subheader("Summary")
        st.write(" ".join(str(sentence) for sentence in summary))

# Entry point of the app
if __name__ == "__main__":
    main()
