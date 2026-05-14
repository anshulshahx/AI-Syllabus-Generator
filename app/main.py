import requests
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from app.schemas.models import (
    OutcomeRequest, OutcomeResponse,
    SyllabusRequest, SyllabusResponse
)
from app.generator.llm_client import generate_outcomes
from app.generator.syllabus_generator import generate_syllabus
from app.exporter.docx_exporter import export_syllabus_to_docx
from app.config import OLLAMA_BASE_URL, OLLAMA_MODEL

app = FastAPI(
    title="Group 1 - Curriculum AI",
    description="Automated generation of Course Objectives and Learning Outcomes",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"status": "Group 1 API is running"}

@app.get("/health")
def health():
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}", timeout=5)
        ollama_status = "connected" if response.status_code == 200 else "unreachable"
    except Exception:
        ollama_status = "unreachable"
    return {
        "api": "running",
        "ollama": ollama_status,
        "model": OLLAMA_MODEL,
        "endpoints": [
            "GET  /",
            "GET  /health",
            "POST /generate/outcomes",
            "POST /generate/syllabus",
            "POST /export/docx"
        ]
    }

@app.post("/generate/outcomes", response_model=OutcomeResponse)
def generate(request: OutcomeRequest):
    outcomes = generate_outcomes(request)
    return OutcomeResponse(
        course_name=request.course_name,
        outcomes=outcomes
    )

@app.post("/generate/syllabus", response_model=SyllabusResponse)
def syllabus(request: SyllabusRequest):
    return generate_syllabus(request)

@app.post("/export/docx")
def export_docx(request: SyllabusRequest):
    # Generate syllabus first then export to docx
    syllabus_data = generate_syllabus(request)

    if not syllabus_data.units:
        raise HTTPException(
            status_code=500,
            detail="Syllabus generation failed — no units returned"
        )

    file_path = export_syllabus_to_docx(syllabus_data)

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=500,
            detail="DOCX file could not be created"
        )

    return FileResponse(
        path=file_path,
        filename=f"{request.course_name.replace(' ', '_')}_syllabus.docx",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )