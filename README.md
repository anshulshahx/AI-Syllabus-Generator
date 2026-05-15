# Group 1 — Curriculum AI Platform

> AI-Driven Platform for Outcome-Based Curriculum Design & Sequencing

![Python](https://img.shields.io/badge/Python-3.14-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green) ![Ollama](https://img.shields.io/badge/Ollama-llama3.1:8b-orange) ![Tests](https://img.shields.io/badge/Tests-167%2F167-brightgreen)

---

## What This Does

Group 1 is the **LLM Generation Layer** of a larger 3-group OBE curriculum platform. It automatically generates accreditation-ready curriculum artifacts using a locally hosted LLM (Ollama llama3.1:8b) and a deterministic 8-rule validation engine.

**Every output is:**
- Validated against Bloom's Taxonomy
- Checked for measurability, bias, profanity and academic tone
- Deduplicated and domain-tagged
- Saved as structured JSON ready for Group 2 (Mapping) and Group 3 (UI)

---

## Quick Start

### Prerequisites
- Python 3.x
- [Ollama](https://ollama.com/download) installed with `llama3.1:8b` model

### Installation

```powershell
# Clone or navigate to project
cd "C:\Users\ASUS\Desktop\final yr Project"

# Install dependencies
pip install -r requirements.txt

# Pull the LLM model
ollama pull llama3.1:8b
```

### Running

```powershell
# Terminal 1 — Ollama runs automatically in background
# If needed: ollama serve

# Terminal 2 — Start the API
python -m uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for interactive API documentation.

---

## API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | Health check |
| GET | `/health` | Detailed status + Ollama connection |
| POST | `/generate/outcomes` | AI learning outcomes with rules engine |
| POST | `/generate/syllabus` | Full unit syllabus with textbooks & YouTube |
| POST | `/export/docx` | Download syllabus as Word document |
| POST | `/review/submit` | Faculty accept / reject / edit outcomes |
| GET | `/review/all` | All stored faculty reviews |
| GET | `/review/training-labels` | BERT training labels for Group 2 |
| POST | `/programme/peos` | Program Educational Objectives |
| POST | `/programme/pos` | All 12 standard NBA Program Outcomes |
| POST | `/programme/psos` | Programme Specific Outcomes |
| POST | `/programme/generate-all` | PEOs + POs + PSOs in one call |
| GET | `/contracts` | Official JSON data contracts |
| GET | `/stats` | System usage statistics |

---

## Example Usage

### Generate Learning Outcomes
```json
POST /generate/outcomes
{
  "course_name": "Data Structures",
  "course_description": "Arrays, linked lists, trees, graphs and sorting algorithms",
  "target_bloom_levels": ["apply", "analyze"],
  "n_candidates": 3
}
```

### Generate Full Syllabus
```json
POST /generate/syllabus
{
  "course_name": "Machine Learning",
  "course_description": "Supervised learning, neural networks, regression and classification",
  "num_units": 5
}
```

### Generate All Programme Outcomes
```json
POST /programme/generate-all
{
  "programme_name": "B.Tech Computer Science Engineering",
  "programme_description": "Four year undergraduate programme in computer science",
  "course_list": ["Data Structures", "Machine Learning", "Computer Networks"],
  "n_peos": 5,
  "n_psos": 3
}
```

---

## The 8-Rule Validation Engine

Every AI-generated outcome passes through all 8 rules before reaching the user:

| # | Rule | Type | Description |
|---|------|------|-------------|
| 1 | Bloom Verb Check | ERROR | First word must be a valid Bloom taxonomy action verb |
| 2 | Measurability | ERROR | No compound verbs like "understand and apply" |
| 3 | Deduplication | REMOVE | Jaccard similarity > 0.8 removes duplicate outcomes |
| 4 | Domain Tagging | TAG | Extracts technical keywords into domain_tags |
| 5 | Length Check | ERROR | Outcome must be 8-30 words |
| 6 | Profanity Filter | ERROR | 20-word inappropriate language blacklist |
| 7 | Bias Filter | WARNING | Gendered and ability-biased language detection |
| 8 | Academic Tone | WARNING | Informal language detection |

---

## Project Structure

```
final yr Project/
├── app/
│   ├── main.py                      # 14 API endpoints
│   ├── config.py                    # Ollama configuration
│   ├── prompts/                     # LLM prompt builders
│   ├── rules/engine.py              # 8-rule validation engine
│   ├── generator/                   # LLM clients + review manager
│   ├── schemas/                     # Pydantic models + contracts
│   ├── exporter/                    # DOCX Word export
│   └── utils/                       # Logging + helpers
├── data/bloom_verbs.json            # Bloom taxonomy verb lists
├── feedback/reviews.json            # Faculty review logs
├── outputs/                         # Generated JSON outputs
├── tests/
│   ├── test_engine.py               # 35 rules engine tests
│   ├── test_pipeline.py             # 49 integration tests
│   ├── test_contracts.py            # 24 contract tests
│   ├── test_30_courses.py           # 30 course benchmark
│   └── test_polish.py               # 29 polish tests
└── requirements.txt
```

---

## Test Results

```
Rules Engine Tests:      35/35  ✅
Pipeline Integration:    49/49  ✅
JSON Contracts:          24/24  ✅
30 Course Benchmark:     30/30  ✅
Polish & Bug Fix:        29/29  ✅
─────────────────────────────────
TOTAL:                  167/167 ✅
```

Run all tests:
```powershell
python tests/test_engine.py
python tests/test_pipeline.py
python tests/test_contracts.py
python tests/test_30_courses.py
python tests/test_polish.py
```

---

## Data Contracts

All outputs follow strict JSON schemas defined in `app/schemas/contracts.py`.
Export the contracts for Group 2 and Group 3 integration:

```
GET /contracts
```

Contracts defined:
- `OutcomeObject` — individual AI-generated outcome
- `CourseUnits` — full course with unit syllabus
- `MappingResponse` — Group 2 CO-to-PO mapping format
- `TrainingLabel` — BERT retraining labels
- `Programme` — PEOs + POs + PSOs

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM | Ollama + LLaMA 3.1 8B (local, free) |
| API Framework | FastAPI + Uvicorn |
| Validation | Pydantic v2 |
| NLP | Custom rules engine + Bloom taxonomy |
| Export | python-docx |
| Testing | Custom test runner |
| OS | Windows 11 / PowerShell |

---

## Integration with Other Groups

**→ Group 2 (Semantic Mapping)**
- Consumes `POST /generate/outcomes` output
- Uses `GET /review/training-labels` for BERT retraining
- Uses `GET /contracts` for OutcomeObject and MappingResponse schemas

**→ Group 3 (UI Platform)**
- Consumes all generation endpoints
- Uses `POST /review/submit` for faculty review UI
- Uses `GET /contracts` for CourseUnits schema

---

## Authors

Group 1 — Final Year Project 2026  
Department of Computer Science & Engineering