import requests
import json
import os
from datetime import datetime
from app.config import OLLAMA_BASE_URL, OLLAMA_MODEL
from app.prompts.syllabus_prompt import build_syllabus_prompt, build_regenerate_prompt
from app.schemas.models import SyllabusRequest, UnitObject, SyllabusResponse
from app.rules.engine import load_bloom_verbs

bloom_verbs = load_bloom_verbs()
OUTPUTS_DIR = "outputs"

def save_syllabus_to_file(data: dict, course_name: str):
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = course_name.replace(" ", "_")
    filename  = f"{OUTPUTS_DIR}/syllabus_{safe_name}_{timestamp}.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved: {filename}")
    return filename

def validate_bloom_start(text: str) -> str:
    if not text or not text.strip():
        return text
    words      = text.strip().split()
    first_word = words[0].lower().rstrip(".,;:")
    all_verbs  = [v for verbs in bloom_verbs.values() for v in verbs]
    if first_word not in all_verbs:
        return f"[VERB_WARNING] {text}"
    return text

def call_ollama(prompt: str, timeout: int = 600) -> str:
    print(f"Calling Ollama (timeout={timeout}s)...")
    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False, "format": "json"},
        timeout=timeout
    )
    if response.status_code != 200:
        raise Exception(f"Ollama HTTP {response.status_code}: {response.text[:200]}")
    raw  = response.json()
    text = raw.get("response", "").strip()
    if not text:
        raise Exception("Ollama returned empty response")
    if "```" in text:
        for part in text.split("```"):
            if "{" in part:
                text = part.lstrip("json").strip()
                break
    return text.strip()

def parse_syllabus(parsed: dict, request: SyllabusRequest) -> SyllabusResponse:
    units = []
    for unit in parsed.get("units", []):
        objectives = [validate_bloom_start(o) for o in unit.get("unit_objectives", [])]
        outcomes   = [validate_bloom_start(o) for o in unit.get("unit_outcomes",   [])]
        units.append(UnitObject(
            unit_id          = unit.get("unit_id",          f"UNIT {len(units)+1}"),
            unit_title       = unit.get("unit_title",       ""),
            hours            = int(unit.get("hours",        8)),
            topics_paragraph = unit.get("topics_paragraph", ""),
            topics           = unit.get("topics",           []),
            unit_objectives  = objectives,
            unit_outcomes    = outcomes,
            assessments      = unit.get("assessments",      []),
            readings         = unit.get("readings",         [])
        ))
    return SyllabusResponse(
        course_name           = request.course_name,
        course_code           = parsed.get("course_code") or request.course_code,
        education_level       = request.education_level   or "undergraduate",
        programme             = request.programme         or "btech",
        year_of_study         = request.year_of_study,
        semester              = request.semester,
        branch                = request.branch,
        credits               = request.credits           or 4,
        ltp                   = request.ltp               or "3:1:0",
        university_name       = request.university_name,
        units                 = units,
        course_objectives     = parsed.get("course_objectives",    []),
        course_outcomes       = parsed.get("course_outcomes",      []),
        textbooks             = parsed.get("textbooks",            []),
        youtube_resources     = parsed.get("youtube_resources",    []),
        open_source_resources = parsed.get("open_source_resources",[])
    )

def generate_syllabus(request: SyllabusRequest) -> SyllabusResponse:
    print(f"\n{'='*55}")
    print(f"Course:    {request.course_name}")
    print(f"Programme: {request.programme} | {request.education_level}")
    print(f"Year: {request.year_of_study} | Sem: {request.semester} | Units: {request.num_units}")
    print(f"Regenerate: {request.regenerate}")
    print(f"{'='*55}")
    try:
        if request.regenerate:
            prompt = build_regenerate_prompt(
                request.course_name, request.course_description,
                request.num_units,
                request.education_level   or "undergraduate",
                request.programme         or "btech",
                request.year_of_study, request.semester, request.branch,
                request.credits or 4, request.ltp or "3:1:0",
                request.rejection_reason, request.custom_prompt
            )
        else:
            prompt = build_syllabus_prompt(
                request.course_name, request.course_description,
                request.num_units,
                request.education_level   or "undergraduate",
                request.programme         or "btech",
                request.year_of_study, request.semester, request.branch,
                request.credits or 4, request.ltp or "3:1:0",
                request.custom_prompt
            )
        timeout = 300 + (request.num_units * 120)
        print(f"Timeout: {timeout}s for {request.num_units} units")
        text   = call_ollama(prompt, timeout=timeout)
        parsed = json.loads(text)
        result = parse_syllabus(parsed, request)
        print(f"Units: {len(result.units)} | COs: {len(result.course_outcomes)}")
        if len(result.units) == 0:
            raise Exception("No units parsed")
        save_syllabus_to_file({
            "course_name":          request.course_name,
            "course_code":          result.course_code,
            "education_level":      request.education_level,
            "programme":            request.programme,
            "year_of_study":        request.year_of_study,
            "semester":             request.semester,
            "branch":               request.branch,
            "credits":              request.credits,
            "ltp":                  request.ltp,
            "regenerated":          request.regenerate,
            "generated_at":         datetime.now().isoformat(),
            "units":                [u.dict() for u in result.units],
            "course_objectives":    result.course_objectives,
            "course_outcomes":      result.course_outcomes,
            "textbooks":            result.textbooks,
            "youtube_resources":    result.youtube_resources,
            "open_source_resources":result.open_source_resources,
        }, request.course_name)
        return result
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return SyllabusResponse(
            course_name=request.course_name,
            education_level=request.education_level or "undergraduate",
            programme=request.programme or "btech",
            units=[], course_objectives=[], course_outcomes=[]
        )