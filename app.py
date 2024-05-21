import streamlit as st
import docx
import PyPDF2
import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

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
        full_text.append(page.extract_text())  # Changed from extractText() to extract_text()
    return '\n'.join(full_text)

def generate_summary(text, sentence_count=SENTENCES_COUNT):
    parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)
    summarizer = LsaSummarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    summary = summarizer(parser.document, sentence_count)
    return ' '.join([str(sentence) for sentence in summary])

def main():
    st.title("Document Summary Generator")
    st.write("Upload a .docx or .pdf file and get a summary!")

    file = st.file_uploader("Upload file", type=['docx', 'pdf'])

    if file is not None:
        file_extension = file.name.split('.')[-1]

        if file_extension == 'docx':
            text = extract_text_from_docx(file)
        elif file_extension == 'pdf':
            text = extract_text_from_pdf(file)
        else:
            st.error("Unsupported file format. Only docx and pdf files are supported.")
            return

        summary = generate_summary(text)
        st.subheader("Summary:")
        st.write(summary)

if __name__ == "__main__":
    main()
