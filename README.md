JobFit AI

JobFit AI is a smart resume scoring application that evaluates resumes against a job description (JD) and provides a professional compatibility score. The app uses NLP techniques, semantic similarity, and keyphrase analysis to help job seekers understand how well their resume matches a target role.

---

- Upload a Resume PDF and input a job description.
- Computes a JobFit score (0-100) using NLP.
- Easy to deploy via FastAPI backend + Streamlit frontend.

---

Project Structure
JobFitAI/
│
├─ backend/
│ ├─ main.py # FastAPI backend
│ ├─ models/
│ │ ├─ extractor.py # Keyphrase extraction
│ │ ├─ scorer.py # Resume scoring logic
│ │ └─ embedder.py # Embedding & semantic similarity
│
├─ frontend/
│ └─ app.py # Streamlit frontend
│
├─ requirements.txt # Python dependencies
└─ README.md

---
Note : Download spacy - 3.8.7 for windows 64 - bit that is given in the repo
