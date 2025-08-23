import streamlit as st
import requests

API_URL = "http://localhost:8000/score"

st.set_page_config(page_title="JobFit AI", layout="wide")

st.title("JobFit AI 🌟")
st.markdown("Upload your resume PDF and paste the job description to get a match score.")

jd_text = st.text_area("Paste Job Description Here", height=200)
resume_file = st.file_uploader("Upload Resume PDF", type=["pdf"])

if st.button("Score Resume"):
    if not jd_text.strip():
        st.warning("Please enter the Job Description text.")
    elif resume_file is None:
        st.warning("Please upload a resume PDF.")
    else:
        with st.spinner("Analyzing resume..."):
            try:
                files = {"resume": (resume_file.name, resume_file.getvalue())}
                data = {"jdtext": jd_text}
                response = requests.post(API_URL, files=files, data=data)
                response.raise_for_status()
                result = response.json()
                st.success(f"JobFit Score: {result['final_score']} / 100")
                st.write(f"Status: {result['status']}")
            except requests.exceptions.RequestException as e:
                st.error(f"API request failed: {e}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")
