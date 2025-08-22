import streamlit as st
import requests

# Backend API URL (adjust if deployed elsewhere)
API_URL = "http://localhost:8000/score"

st.set_page_config(page_title="JobFit AI", layout="wide")
st.title("JobFit AI 🌟")
st.markdown(
    "Upload a resume PDF and paste the job description to get a compatibility score and professional message."
)

# Job Description input
jd_text = st.text_area("Paste Job Description Here:", height=200)

# Resume file upload
resume_file = st.file_uploader("Upload Resume (PDF):", type=["pdf"])

if st.button("Score Resume"):
    if not jd_text:
        st.warning("Please enter the Job Description text.")
    elif not resume_file:
        st.warning("Please upload a resume PDF.")
    else:
        with st.spinner("Scoring resume..."):
            files = {"resume": (resume_file.name, resume_file.getvalue())}
            data = {"jd_text": jd_text}
            try:
                response = requests.post(API_URL, files=files, data=data)
                result = response.json()
                
                if "error" in result:
                    st.error(f"Error: {result['error']}")
                else:
                    # Display final score
                    st.success(f"✅ JobFit Score: {result['final_score']} / 100")
                    
                    # Display professional message
                    st.subheader("Message:")
                    st.write(result["message"])
            except Exception as e:
                st.error(f"Failed to connect to backend: {e}")
