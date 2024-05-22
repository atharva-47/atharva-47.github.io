import streamlit as st
import docx
import PyPDF2
import nltk
import re
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from langdetect import detect

# Download the 'punkt' data
nltk.download('punkt')

LANGUAGE = "english"
SENTENCES_COUNT = 10

def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    full_text = []
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        full_text.append(page.extract_text())
    return '\n'.join(full_text)

def clean_text(text):
    # Remove non-ASCII characters
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    # Normalize whitespace: convert multiple spaces, newlines, or tabs to a single space
    text = re.sub(r'\s+', ' ', text)
    # Remove leading and trailing whitespace
    text = text.strip()
    # Filter out non-English text
    text = filter_non_english(text)
    return text

def filter_non_english(text):
    filtered_text = ""
    lines = text.split("\n")
    for line in lines:
        # Check if the line contains English text
        if len(line) > 0 and detect(line) == 'en':
            filtered_text += line + "\n"
    return filtered_text

def generate_summary(text, sentence_count=SENTENCES_COUNT):
    parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)
    summarizer = LsaSummarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    summary = summarizer(parser.document, sentence_count)
    return ' '.join([str(sentence) for sentence in summary])

def summarize_page(page_text):
    return page_text[:50] + '...'

def main():
    st.title("Document Summary Generator")
    st.write("Upload a .docx or .pdf file and get a summary!")

    file = st.file_uploader("Upload file", type=['docx', 'pdf'])

    generate_page_summary = st.checkbox('Generate Page-wise Summary')

    if file is not None:
        file_extension = file.name.split('.')[-1]

        if file_extension == 'docx':
            text = extract_text_from_docx(file)
        elif file_extension == 'pdf':
            text = extract_text_from_pdf(file)
        else:
            st.error("Unsupported file format. Only docx and pdf files are supported.")
            return

        clean_text_content = clean_text(text)
        
        # Print or log the cleaned text for debugging
        st.text_area("Extracted Text", clean_text_content, height=200)
        
        if generate_page_summary:
            pages = clean_text_content.split('\n')
            for i, page in enumerate(pages):
                summary = summarize_page(page)
                st.write(f'**Page {i+1} Summary:**\n{summary}')
        else:
            summary = generate_summary(clean_text_content)
            st.subheader("Summary:")
            st.write(summary)

if __name__ == "__main__":
    main()
