# Group 1 — AI-Driven OBE Curriculum Platform

> Automated generation of PEOs, POs, PSOs, Course Outcomes and Syllabi using Local LLM (Ollama)

![Python](https://img.shields.io/badge/Python-3.14-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)
![Ollama](https://img.shields.io/badge/Ollama-llama3.1:8b-orange)
![Tests](https://img.shields.io/badge/Tests-158%2F158-brightgreen)
![Version](https://img.shields.io/badge/Version-2.0.0-purple)

---

## Project Overview

Group 1 is the **LLM Generation Layer** of a 3-group AI-driven Outcome-Based Education (OBE)
platform built for G.B. Pant Institute of Engineering & Technology, Pauri Garhwal.

It automatically generates accreditation-ready curriculum artifacts using a locally hosted
LLM (Ollama llama3.1:8b) and a deterministic 8-rule validation engine — with zero cloud
dependency and zero API cost.

---

## Institution

**G.B. Pant Institute of Engineering & Technology, Pauri Garhwal**
B.Tech CSE (AI & ML) | VIII Semester | AIP-109 | 2026

---

## Team

| Member | Role |
|--------|------|
| Member 1 | LLM Integration + Rules Engine |
| Member 2 | Syllabus Generator + DOCX Exporter |
| Member 3 | Programme Generator + Review System |
| Member 4 | API Design + Testing + Contracts |

---

## Quick Start

### Prerequisites
- Python 3.x
- [Ollama](https://ollama.com/download) installed

### Installation

```powershell
cd "C:\Users\ASUS\Desktop\final yr Project"
pip install -r requirements.txt
ollama pull llama3.1:8b
```

### Run

```powershell
# Terminal 1
ollama serve

# Terminal 2
python -m uvicorn app.main:app --reload
```

Open: `http://127.0.0.1:8000/docs`

---

## API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | Health check |
| GET | `/health` | Ollama status + endpoint list |
| POST | `/generate/outcomes` | AI course outcomes with rules engine |
| POST | `/generate/syllabus` | Full unit syllabus with textbooks and YouTube |
| POST | `/export/docx` | Download syllabus as Word document |
| POST | `/review/submit` | Faculty accept / reject / edit outcomes |
| GET | `/review/all` | All stored faculty reviews |
| GET | `/review/training-labels` | BERT training labels for Group 2 |
| POST | `/programme/peos` | Generate Program Educational Objectives |
| POST | `/programme/pos` | Generate all 12 NBA Program Outcomes |
| POST | `/programme/psos` | Generate Programme Specific Outcomes |
| POST | `/programme/generate-all` | PEOs + POs + PSOs in one call |

---

## Features

### SK Verma Sir Requirements
- Education level field (undergraduate / postgraduate / diploma / PhD)
- Programme field (BTech / BSc / BCom / BA / MTech / MCA / MBA etc.)
- Year of study (Year 1 to Year 6)
- Semester field
- Course Objectives (5 numbered)
- Course Outcomes CO1–CO5
- Topics per unit in paragraph format (UTU style)
- 5 reference textbooks
- YouTube and NPTEL resources
- Open source resources
- DOCX download in UTU format with red footer bar

### Jayant Sir Requirements
- `regenerate: true` — force completely new generation
- `rejection_reason` — tell LLM why previous was rejected
- `custom_prompt` — user gives extra instructions to LLM

### Supported Programmes
BTech, BSc, BCom, BA, MTech, MSc, MCA, BCA, MCom,
MBA, LLB, BEd, BArch, MBBS, Diploma, PhD

---

## The 8-Rule Validation Engine

Every AI-generated outcome passes all 8 rules before reaching the user:

| Rule | Name | Type |
|------|------|------|
| 1 | Bloom Verb Check | ERROR |
| 2 | Measurability (no compound verbs) | ERROR |
| 3 | Deduplication (Jaccard > 0.8) | REMOVE |
| 4 | Domain Tagging | TAG |
| 5 | Length Check (8–30 words) | ERROR |
| 6 | Profanity Filter | ERROR |
| 7 | Bias Filter | WARNING |
| 8 | Academic Tone | WARNING |

---

## Project Structure
final yr Project/
├── app/
│   ├── main.py                      # 12 API endpoints
│   ├── config.py                    # Ollama config
│   ├── exporter/
│   │   ├── init.py
│   │   └── docx_exporter.py         # UTU format DOCX
│   ├── generator/
│   │   ├── init.py
│   │   ├── llm_client.py            # Outcome generation
│   │   ├── syllabus_generator.py    # Syllabus generation
│   │   ├── programme_generator.py   # PEO/PO/PSO generation
│   │   └── review_manager.py        # Faculty review system
│   ├── prompts/
│   │   ├── init.py
│   │   ├── outcome_prompt.py        # Outcome prompt builder
│   │   ├── syllabus_prompt.py       # Syllabus prompt builder
│   │   └── peo_prompt.py            # PEO/PO/PSO prompts
│   ├── rules/
│   │   ├── init.py
│   │   └── engine.py                # 8-rule validation engine
│   ├── schemas/
│   │   ├── init.py
│   │   ├── models.py                # Pydantic models
│   │   ├── review_models.py         # Review models
│   │   ├── programme_models.py      # Programme models
│   │   ├── contracts.py             # JSON data contracts
│   │   └── validator.py             # Schema validators
│   └── utils/
│       ├── init.py
│       └── helpers.py               # Logging + file helpers
├── data/
│   └── bloom_verbs.json             # 6 levels, 80+ verbs
├── feedback/
│   └── reviews.json                 # Faculty review logs
├── outputs/                         # Generated JSON files
│   └── exports/                     # Generated DOCX files
├── logs/
│   └── app.log                      # Application logs
├── tests/
│   ├── test_engine.py               # 35 rules engine tests
│   ├── test_pipeline.py             # 40 integration tests
│   ├── test_contracts.py            # 24 contract tests
│   ├── test_30_courses.py           # 30 course benchmark
│   └── test_polish.py               # 29 polish tests
├── requirements.txt
└── README.md

---

## Test Results
Rules Engine Tests      35/35  ✅
Pipeline Integration    40/40  ✅
JSON Contracts          24/24  ✅
30 Course Benchmark     30/30  ✅
Polish & Bug Fix        29/29  ✅
─────────────────────────────────
TOTAL                  158/158 ✅

Run all tests:

```powershell
python tests/test_engine.py
python tests/test_pipeline.py
python tests/test_contracts.py
python tests/test_30_courses.py
python tests/test_polish.py
```

---

## Sample API Requests

### Generate Outcomes
```json
POST /generate/outcomes
{
  "course_name": "Data Structures",
  "course_description": "Arrays, linked lists, trees, graphs and sorting algorithms",
  "target_bloom_levels": ["apply", "analyze"],
  "n_candidates": 3,
  "education_level": "undergraduate",
  "programme": "btech",
  "year_of_study": 2
}
```

### Generate Syllabus
```json
POST /generate/syllabus
{
  "course_name": "Machine Learning",
  "course_description": "Supervised learning, neural networks, regression and classification",
  "num_units": 5,
  "education_level": "undergraduate",
  "programme": "btech",
  "year_of_study": 3,
  "semester": 5,
  "branch": "Computer Science and Engineering AI and ML",
  "credits": 4,
  "ltp": "3:1:0",
  "university_name": "G.B. Pant Institute of Engineering and Technology, Pauri Garhwal"
}
```

### Regenerate (user rejected previous)
```json
POST /generate/syllabus
{
  "course_name": "Data Structures",
  "course_description": "Arrays, linked lists, trees and graphs",
  "num_units": 3,
  "programme": "btech",
  "year_of_study": 2,
  "regenerate": true,
  "rejection_reason": "Too theoretical, need more practical examples",
  "custom_prompt": "Focus on implementation and real world applications"
}
```

### Generate All Programme Artifacts
```json
POST /programme/generate-all
{
  "programme_name": "B.Tech Computer Science Engineering AI and ML",
  "programme_description": "Four year undergraduate programme covering AI, ML, data structures and networks",
  "course_list": ["Data Structures", "Machine Learning", "Computer Networks"],
  "n_peos": 5,
  "n_psos": 3
}
```

---

## Data Contracts for Group 2 and Group 3
GET /contracts

Contracts:
- `OutcomeObject` — AI-generated outcome with bloom level, flags, domain tags
- `CourseUnits` — full syllabus with unit-wise breakdown
- `MappingResponse` — Group 2 CO-to-PO mapping format
- `TrainingLabel` — BERT retraining labels from faculty reviews
- `Programme` — PEOs + POs + PSOs

---

## Integration Points

### Group 2 (Semantic Mapping)
- Consumes `POST /generate/outcomes` — gets COs with bloom levels and domain tags
- Consumes `GET /review/training-labels` — gets BERT retraining data
- Consumes `GET /contracts` — gets OutcomeObject and MappingResponse schemas

### Group 3 (React UI)
- Consumes all generation endpoints
- Consumes `POST /review/submit` — faculty review interface
- Consumes `POST /export/docx` — DOCX download
- Consumes `GET /contracts` — gets CourseUnits schema

---

## Technology Stack

| Layer | Technology |
|-------|-----------|
| LLM | Ollama + LLaMA 3.1 8B (local, free) |
| API | FastAPI + Uvicorn |
| Validation | Pydantic v2 |
| Rules Engine | Custom 8-rule deterministic engine |
| NLP | Bloom taxonomy + Jaccard similarity |
| Export | python-docx (UTU format) |
| Security | CORS + GZip + Rate limiting |
| OS | Windows 11 / PowerShell |

---

## Requirements
fastapi
uvicorn
pydantic
requests
python-docx

Install:
```powershell
pip install fastapi uvicorn pydantic requests python-docx
```

---

## Version History

| Version | Changes |
|---------|---------|
| 1.0.0 | Basic outcome generation + rules engine |
| 1.5.0 | Syllabus generator + DOCX export |
| 1.8.0 | Human review system + training labels |
| 2.0.0 | Programme generator + multi-programme support + security + optimization |

---

*Final Year Project 2026 | G.B. Pant Institute of Engineering & Technology | B.Tech CSE AI & ML*
