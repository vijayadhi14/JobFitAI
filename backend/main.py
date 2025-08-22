from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.models.scorer import JobScorer
from backend.utils.pdf_parser import extract_text_from_pdf

# Initialize FastAPI app
app = FastAPI(title="JobFit AI", version="1.0.0")

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load scorer once at startup
scorer = JobScorer()

@app.post("/score")
async def score_resume(
    jd_text: str = Form(..., description="Job description text"),
    resume: UploadFile = File(..., description="Resume PDF file")
):
    """
    Endpoint to score a resume PDF against a JD text.
    Returns final score, component scores, and explanation.
    """
    try:
        pdf_bytes = await resume.read()
        resume_text = extract_text_from_pdf(pdf_bytes)
        result = scorer.score_resume(resume_text, jd_text)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
