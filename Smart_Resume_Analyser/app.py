# If you see import errors, install missing packages:
# pip install streamlit python-dotenv PyPDF2
import os
import streamlit as st
from dotenv import load_dotenv
from gemini_api import get_gemini_response
from pdf_utils import input_pdf_setup
from display_utils import display_gemini_response

# Load environment variables
load_dotenv()

def handle_job_description_and_resume(input_text, uploaded_file, prompt, submit_button, highlight_percentage=False):
    if not input_text or not input_text.strip():
        st.error("Job description is required to calculate the percentage match, identify missing keywords, and provide final thoughts. Please enter a job description above.")
        return

    if submit_button:
        if uploaded_file is not None:
            pdf_text = input_pdf_setup(uploaded_file)
            if pdf_text:
                response = get_gemini_response(input_text, pdf_text, prompt)
                st.subheader("The Response is")
                display_gemini_response(response, highlight_percentage=highlight_percentage)
            else:
                st.error("Error extracting text from PDF.")
        else:
            st.write("Please upload the resume.")

# Streamlit App
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")

# Input for job description
input_text = st.text_area("Job Description: ", key="input")

# File uploader for resume (PDF)
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

# Buttons to submit
submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage Match")

# Prompts
input_prompt1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description.
Please share your professional evaluation on whether the candidate's profile aligns with the role.
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality.
Your task is to evaluate the resume against the provided job description.
Give me the percentage of match if the resume matches the job description. First, the output should come as a percentage,
then keywords missing, and last, final thoughts.
"""

# Check for 'Tell Me About the Resume' button submission
if submit1:
    handle_job_description_and_resume(input_text, uploaded_file, input_prompt1, submit1)

# Check for 'Percentage Match' button submission
elif submit3:
    handle_job_description_and_resume(input_text, uploaded_file, input_prompt3, submit3, highlight_percentage=True)
