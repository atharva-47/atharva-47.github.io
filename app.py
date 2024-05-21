import streamlit as st
import docx
import PyPDF2
from gensim.summarization import summarize

def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def extract_text_from_pdf(pdf_file):
    with open(pdf_file, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        full_text = []
        for page_num in range(reader.numPages):
            page = reader.getPage(page_num)
            full_text.append(page.extractText())
    return '\n'.join(full_text)

def generate_summary(text, ratio=0.2):
    return summarize(text, ratio=ratio)

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
