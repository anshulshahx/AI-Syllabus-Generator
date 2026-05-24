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
    from app.schemas.models import COObject

    # Parse units
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
            satisfied_cos    = unit.get("satisfied_cos",    []),
            assessments      = unit.get("assessments",      []),
            readings         = unit.get("readings",         []),
            lecture_plan     = unit.get("lecture_plan",     "")
        ))

    # Parse COs — full Indian NBA format
    raw_cos    = parsed.get("course_outcomes", [])
    co_objects = []
    co_texts   = []

    for co in raw_cos:
        if isinstance(co, dict):
            co_obj = COObject(
                co_id               = co.get("co_id",               "CO"),
                text                = co.get("text",                ""),
                bloom_level         = co.get("bloom_level",         ""),
                bloom_verb          = co.get("bloom_verb",          ""),
                bloom_level_number  = co.get("bloom_level_number",  ""),
                mapped_pos          = co.get("mapped_pos",          []),
                po_correlation      = co.get("po_correlation",      {}),
                mapped_psos         = co.get("mapped_psos",         []),
                pso_correlation     = co.get("pso_correlation",     {}),
                attainment_target   = co.get("attainment_target",   "60% of students score above 60%"),
                attainment_level    = int(co.get("attainment_level", 1)),
                direct_assessment   = co.get("direct_assessment",   []),
                indirect_assessment = co.get("indirect_assessment", []),
                unit_test_marks     = int(co.get("unit_test_marks", 20)),
                assignment_marks    = int(co.get("assignment_marks", 5)),
                end_sem_marks       = int(co.get("end_sem_marks",   70))
            )
            co_objects.append(co_obj)

            # Build readable text
            bloom_num = co.get("bloom_level_number", "")
            pos_text  = ", ".join([
                f"{po}({co.get('po_correlation',{}).get(po,'?')})"
                for po in co.get("mapped_pos", [])
            ])
            pso_text  = ", ".join([
                f"{pso}({co.get('pso_correlation',{}).get(pso,'?')})"
                for pso in co.get("mapped_psos", [])
            ])
            co_texts.append(
                f"{co.get('co_id')}: {co.get('text')} "
                f"[Bloom: {co.get('bloom_level')} {bloom_num}] "
                f"[POs: {pos_text}] [PSOs: {pso_text}] "
                f"[Attainment Target: {co.get('attainment_target','')}]"
            )
        else:
            co_texts.append(str(co))

    # Build exam pattern
    exam_pattern = parsed.get("exam_pattern", {
        "internal_assessment": 30,
        "end_semester_exam": 70,
        "total": 100,
        "internal_breakdown": {
            "unit_tests_2_tests": 20,
            "assignments": 5,
            "attendance": 5
        }
    })

    return SyllabusResponse(
        course_name           = request.course_name,
        course_code           = parsed.get("course_code")     or request.course_code,
        education_level       = request.education_level       or "undergraduate",
        programme             = request.programme             or "btech",
        year_of_study         = request.year_of_study,
        semester              = request.semester,
        branch                = request.branch,
        credits               = request.credits               or 4,
        ltp                   = request.ltp                   or "3:1:0",
        university_name       = request.university_name,
        standards             = parsed.get("standards",       "NBA GAPC v4.0, AICTE, UGC-LOCF, NAAC, IQAC, Bloom's Taxonomy"),
        total_hours           = parsed.get("total_hours"),
        total_lectures        = parsed.get("total_lectures"),
        units                 = units,
        course_objectives     = parsed.get("course_objectives",    []),
        course_outcomes       = co_objects,
        course_outcomes_text  = co_texts,
        co_po_matrix          = parsed.get("co_po_matrix",         {}),
        co_pso_matrix         = parsed.get("co_pso_matrix",        {}),
        exam_pattern          = exam_pattern,
        attainment_formula    = parsed.get("attainment_formula",   "CO Attainment = (Direct × 0.8) + (Indirect × 0.2)"),
        attainment_levels     = parsed.get("attainment_levels",    {}),
        po_attainment_formula = parsed.get("po_attainment_formula","PO Attainment = Σ(CO_Attainment × CO-PO_Strength) / Σ(CO-PO_Strength)"),
        cqi_plan              = parsed.get("cqi_plan"),
        lesson_plan_note      = parsed.get("lesson_plan_note"),
        naac_iqac_note        = parsed.get("naac_iqac_note"),
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