# AI-Driven Curriculum Generator (OBE Framework)

A professional-grade backend platform designed to automate and validate academic curricula using **Large Language Models (LLMs)** and **Outcome-Based Education (OBE)** principles.

## 🚀 Key Features
* **Intelligent Syllabus Generation:** Automated unit design and syllabus structuring using local LLMs (Ollama) and the Gemini API.
* **Advanced Rules Engine:** Multi-stage validation logic for measurability, Bloom's Taxonomy verbs, tone consistency, and profanity filtering.
* **Automated Outcome Mapping:** Dynamic generation of Program Educational Objectives (PEOs), Program Outcomes (POs), and Program Specific Outcomes (PSOs).
* **Production-Ready API:** High-performance endpoints built with FastAPI, including comprehensive error handling.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Framework:** FastAPI
* **AI Integration:** Ollama (Local LLM), Google Gemini
* **Validation:** Pydantic Models & Custom Rules Engine
* **Testing:** Pytest & Full Pipeline Integration Suite

## 🧪 Testing & Reliability
This project follows a rigorous testing protocol. The core engine is validated against a **49-point full pipeline integration test**, ensuring:
* ✅ 100% Data contract compliance (JSON Schema).
* ✅ Successful cross-endpoint data flow.
* ✅ Reliable AI output formatting across all generation modules.

## 📦 Installation & Setup
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables in `.env`.
4. Run the server: `uvicorn app.main:app --reload`