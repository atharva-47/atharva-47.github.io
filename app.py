import streamlit as st
from transformers import T5ForConditionalGeneration, T5Tokenizer

# Load model and tokenizer
model_name = "t5-small"
model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name)

def summarize(text):
    inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

# Streamlit app
st.title('Document Summarization')
text = st.text_area("Enter text to summarize", height=200)
if st.button('Summarize'):
    summary = summarize(text)
    st.write('Summary:', summary)
