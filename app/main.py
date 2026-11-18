from pathlib import Path
from typing import List
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from fastapi import FastAPI, File, Form, HTTPException, UploadFile

from app.ranker import rank_resumes
from app.resume_parser import extract_text

app = FastAPI(
    title="AI Resume Screening System",
    description=(
        "Upload a job description and resumes to rank candidates "
        "using TF-IDF and cosine similarity."
    ),
    version="1.0.0"
)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

SUPPORTED_FORMATS = {".pdf", ".docx", ".txt"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB per resume


@app.get("/")
async def home():
    return FileResponse("app/templates/index.html")


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/screen-resumes")
async def screen_resumes(
    job_description: str = Form(...),
    files: List[UploadFile] = File(...)
):
    """Extract resume text, calculate similarity, and return ranked results."""
    if not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty.")

    if not files:
        raise HTTPException(status_code=400, detail="Upload at least one resume.")

    resumes = []

    for uploaded_file in files:
        filename = uploaded_file.filename or "unnamed_resume"
        extension = Path(filename).suffix.lower()

        try:
            if extension not in SUPPORTED_FORMATS:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported file format: {filename}. Use PDF, DOCX, or TXT."
                )

            content = await uploaded_file.read()

            if not content:
                raise HTTPException(
                    status_code=400,
                    detail=f"{filename} is empty."
                )

            if len(content) > MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=400,
                    detail=f"{filename} exceeds the 5 MB file size limit."
                )

            try:
                resume_text = extract_text(content, filename)
            except ValueError as error:
                raise HTTPException(status_code=400, detail=f"{filename}: {error}")

            resumes.append({"filename": filename, "text": resume_text})

        finally:
            await uploaded_file.close()

    try:
        ranked_candidates = rank_resumes(job_description, resumes)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    return {
        "message": "Resume screening completed successfully.",
        "total_resumes_processed": len(ranked_candidates),
        "ranking_method": "TF-IDF + Cosine Similarity",
        "results": ranked_candidates
    }
