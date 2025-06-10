import streamlit as st
import fitz  # PyMuPDF for PDF text extraction
import openai
import os

# Load API key securely from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def get_summary_from_openai(raw_text):
    prompt = f"""
    You are a legal assistant. Summarize the following Georgia crash report.
    Include:
    - Date of incident
    - Location
    - Drivers and vehicles involved (name, DOB, car make/model/year)
    - Injuries reported
    - Vehicle damage
    - Fault determination
    - Citation(s) issued
    - A clear, short narrative of the crash

    Use bullet points. Be professional and neutral.

    Report:
    {raw_text}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a legal assistant AI."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response["choices"][0]["message"]["content"].strip()

st.set_page_config(page_title="Crash Report Summarizer", layout="centered")
st.title("🚗 Georgia Crash Report Analyzer")
st.write("Upload a police crash report PDF and get a professional summary.")

uploaded_file = st.file_uploader("Upload PDF Report", type="pdf")

if uploaded_file:
    with st.spinner("Processing crash report..."):
        raw_text = extract_text_from_pdf(uploaded_file)
        summary = get_summary_from_openai(raw_text)

        st.success("Crash report summarized!")
        st.subheader("📋 Summary")
        st.text_area("Summary Output", summary, height=400)
        st.download_button("📥 Download Summary", summary, file_name="crash_summary.txt")
