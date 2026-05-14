import requests
import json
import os
from datetime import datetime
from app.config import OLLAMA_BASE_URL, OLLAMA_MODEL
from app.prompts.syllabus_prompt import build_syllabus_prompt
from app.schemas.models import SyllabusRequest, UnitObject, SyllabusResponse
from app.rules.engine import check_bloom_verb, load_bloom_verbs

bloom_verbs = load_bloom_verbs()
OUTPUTS_DIR = "outputs"

def save_syllabus_to_file(data: dict, course_name: str):
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = course_name.replace(" ", "_")
    filename  = f"{OUTPUTS_DIR}/syllabus_{safe_name}_{timestamp}.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved syllabus to {filename}")
    return filename

def validate_bloom_start(text: str) -> str:
    words = text.strip().split()
    if not words:
        return text
    first_word = words[0].lower().rstrip(".,;:")
    all_verbs  = []
    for verbs in bloom_verbs.values():
        all_verbs.extend(verbs)
    if first_word not in all_verbs:
        return f"[VERB_WARNING] {text}"
    return text

def call_ollama(prompt: str, timeout: int = 300) -> str:
    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json={
            "model":  OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        },
        timeout=timeout
    )
    if response.status_code != 200:
        raise Exception(f"Ollama error: {response.text}")
    raw  = response.json()
    text = raw.get("response", "").strip()
    if "```" in text:
        for part in text.split("```"):
            if "{" in part:
                text = part.lstrip("json").strip()
                break
    return text.strip()

def generate_syllabus(request: SyllabusRequest) -> SyllabusResponse:
    print(f"\nGenerating syllabus for: {request.course_name}")

    try:
        # ── Main syllabus generation ──
        prompt = build_syllabus_prompt(
            course_name=request.course_name,
            course_description=request.course_description,
            num_units=request.num_units
        )

        text   = call_ollama(prompt, timeout=300)
        parsed = json.loads(text)
        units  = []

        for unit in parsed.get("units", []):
            objectives = [validate_bloom_start(o) for o in unit.get("unit_objectives", [])]
            outcomes   = [validate_bloom_start(o) for o in unit.get("unit_outcomes",   [])]
            units.append(UnitObject(
                unit_id         = unit.get("unit_id",    f"U{len(units)+1}"),
                unit_title      = unit.get("unit_title", ""),
                unit_objectives = objectives,
                unit_outcomes   = outcomes,
                assessments     = unit.get("assessments", []),
                readings        = unit.get("readings",    [])
            ))

        textbooks        = parsed.get("textbooks",        [])
        youtube_resources = parsed.get("youtube_resources", [])

        print(f"Generated {len(units)} units")
        print(f"Textbooks: {len(textbooks)}")
        print(f"YouTube resources: {len(youtube_resources)}")

        # ── Save to file ──
        result = SyllabusResponse(
            course_name       = request.course_name,
            units             = units,
            textbooks         = textbooks,
            youtube_resources = youtube_resources
        )

        save_syllabus_to_file({
            "course_name":       request.course_name,
            "generated_at":      datetime.now().isoformat(),
            "num_units":         len(units),
            "units":             [u.dict() for u in units],
            "textbooks":         textbooks,
            "youtube_resources": youtube_resources
        }, request.course_name)

        return result

    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
        return SyllabusResponse(course_name=request.course_name, units=[])
    except Exception as e:
        print(f"Error: {e}")
        return SyllabusResponse(course_name=request.course_name, units=[])