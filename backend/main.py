from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.models.scorer import JobScorer
from backend.utils.pdf_parser import extract_text_from_pdf
import asyncio

app = FastAPI(title="JobFit AI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scorer = JobScorer()

@app.post("/score")
async def score_resume(
    jdtext: str = Form(...),
    resume: UploadFile = File(...)
):
    try:
        pdf_bytes = await resume.read()
        loop = asyncio.get_running_loop()
        resumetext = await loop.run_in_executor(None, extract_text_from_pdf, pdf_bytes)
        score_result = await loop.run_in_executor(None, scorer.score_resume, resumetext, jdtext)
        return JSONResponse(content=score_result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
