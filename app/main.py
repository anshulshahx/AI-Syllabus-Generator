import requests
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from app.schemas.models import (
    OutcomeRequest, OutcomeResponse,
    SyllabusRequest, SyllabusResponse
)
from app.schemas.review_models import ReviewRequest, ReviewSummary
from app.schemas.programme_models import (
    PEORequest, PEOResponse,
    PORequest, POResponse,
    PSORequest, PSOResponse,
    ProgrammeRequest, ProgrammeResponse
)
from app.generator.llm_client import generate_outcomes
from app.generator.syllabus_generator import generate_syllabus
from app.generator.review_manager import (
    process_reviews, get_all_reviews, get_training_labels
)
from app.generator.programme_generator import (
    generate_peos, generate_pos,
    generate_psos, generate_programme
)
from app.exporter.docx_exporter import export_syllabus_to_docx
from app.schemas.contracts import ALL_CONTRACTS
from app.schemas.validator import run_full_validation
from app.utils.helpers import get_system_stats
from app.config import OLLAMA_BASE_URL, OLLAMA_MODEL

app = FastAPI(
    title="Group 1 - Curriculum AI",
    description="Automated generation of Course Objectives and Learning Outcomes",
    version="2.0.0"
)

@app.get("/")
def root():
    return {"status": "Group 1 API is running", "version": "2.0.0"}

@app.get("/health")
def health():
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}", timeout=5)
        ollama_status = "connected" if response.status_code == 200 else "unreachable"
    except Exception:
        ollama_status = "unreachable"
    return {
        "api":    "running",
        "ollama": ollama_status,
        "model":  OLLAMA_MODEL,
        "version": "2.0.0",
        "new_features": [
            "education_level field (undergraduate/postgraduate/diploma/phd)",
            "programme field (btech/bsc/bcom/ba/mtech/msc/mca/bca/phd/diploma)",
            "year_of_study field (1-6)",
            "custom_prompt field — user custom instructions",
            "regenerate field — force new generation on rejection",
            "topics per unit (SK Verma Sir)",
            "course_outcomes (COs) in syllabus",
            "open_source_resources in syllabus",
            "improved DOCX with COs and topics"
        ]
    }

# ── Generation endpoints ─────────────────────────────────────────
@app.post("/generate/outcomes", response_model=OutcomeResponse)
def generate(request: OutcomeRequest):
    outcomes = generate_outcomes(request)
    return OutcomeResponse(
        course_name    = request.course_name,
        education_level= request.education_level or "undergraduate",
        programme      = request.programme or "btech",
        year_of_study  = request.year_of_study,
        outcomes       = outcomes
    )

@app.post("/generate/syllabus", response_model=SyllabusResponse)
def syllabus(request: SyllabusRequest):
    return generate_syllabus(request)

# ── Export endpoints ─────────────────────────────────────────────
@app.post("/export/docx")
def export_docx(request: SyllabusRequest):
    syllabus_data = generate_syllabus(request)
    if not syllabus_data.units:
        raise HTTPException(status_code=500, detail="Syllabus generation failed")
    file_path = export_syllabus_to_docx(syllabus_data)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=500, detail="DOCX file could not be created")

    prog  = request.programme or "general"
    year  = f"_Year{request.year_of_study}" if request.year_of_study else ""
    fname = f"{request.course_name.replace(' ', '_')}_{prog.upper()}{year}_syllabus.docx"

    return FileResponse(
        path      = file_path,
        filename  = fname,
        media_type= "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

# ── Review endpoints ─────────────────────────────────────────────
@app.post("/review/submit", response_model=ReviewSummary)
def submit_review(request: ReviewRequest):
    return process_reviews(request)

@app.get("/review/all")
def all_reviews():
    return get_all_reviews()

@app.get("/review/training-labels")
def training_labels():
    return get_training_labels()

# ── Programme endpoints ──────────────────────────────────────────
@app.post("/programme/peos", response_model=PEOResponse)
def peos(request: PEORequest):
    return generate_peos(request)

@app.post("/programme/pos", response_model=POResponse)
def pos(request: PORequest):
    return generate_pos(request)

@app.post("/programme/psos", response_model=PSOResponse)
def psos(request: PSORequest):
    return generate_psos(request)

@app.post("/programme/generate-all", response_model=ProgrammeResponse)
def programme_all(request: ProgrammeRequest):
    return generate_programme(request)

# ── Contract endpoints ───────────────────────────────────────────
@app.get("/contracts")
def get_contracts():
    return ALL_CONTRACTS

@app.post("/contracts/validate/{data_type}")
def validate_data(data_type: str, data: dict):
    return run_full_validation(data, data_type)

# ── Stats endpoint ───────────────────────────────────────────────
@app.get("/stats")
def stats():
    return get_system_stats()