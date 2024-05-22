import streamlit as st
import docx
import PyPDF2
import nltk
import re

# Download the 'punkt' data
nltk.download('punkt')

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
    return text

def parse_extracted_text(extracted_text):
    # Split the text into lines
    lines = extracted_text.split('\n')
    
    # Initialize lists to store the structured data
    structured_data = []

    # Initialize temporary variables to store data for each row
    temp_row = {}

    # Define a pattern to identify lines that start with a number (indicating a new data row)
    pattern = re.compile(r'^\d{1,2}\.\s')

    for line in lines:
        if pattern.match(line):
            # If the line starts with a number, it indicates the start of a new row
            if temp_row:
                # Append the previous row to the structured data list
                structured_data.append(temp_row)
                temp_row = {}
            # Extract the number (if needed) and the rest of the line
            parts = line.split(maxsplit=1)
            temp_row['number'] = parts[0]
            temp_row['text'] = parts[1] if len(parts) > 1 else ''
        else:
            # If the line does not start with a number, it is a continuation of the previous row's text
            if 'text' in temp_row:
                temp_row['text'] += ' ' + line
            else:
                temp_row['text'] = line

    # Append the last row to the structured data list if it exists
    if temp_row:
        structured_data.append(temp_row)
    
    return structured_data

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

        clean_text_content = clean_text(text)
        
        # Print or log the cleaned text for debugging
        st.text_area("Extracted Text", clean_text_content, height=200)
        
        # Parse the extracted text into structured data
        structured_data = parse_extracted_text(clean_text_content)
        
        st.subheader("Structured Data:")
        for data in structured_data:
            st.write(data)

if __name__ == "__main__":
    main()
