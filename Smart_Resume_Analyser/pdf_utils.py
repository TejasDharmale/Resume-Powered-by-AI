import io
import PyPDF2
import streamlit as st

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        try:
            pdf_bytes = uploaded_file.read()
            with io.BytesIO(pdf_bytes) as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
        except Exception as e:
            st.error(f"Error processing PDF: {e}")
            return None
    else:
        raise FileNotFoundError("No file uploaded") 