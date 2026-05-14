def build_peo_prompt(programme_name: str, programme_description: str, n_peos: int) -> str:
    return f"""You are an expert in NBA/ABET accreditation and Outcome-Based Education.

Generate exactly {n_peos} Program Educational Objectives (PEOs) for:
Programme: {programme_name}
Description: {programme_description}

RULES:
- PEOs describe what graduates will achieve 3-5 years after graduation
- Each PEO must be broad, long-term, and career-oriented
- Start each PEO with action words like "Graduates will", "Alumni will"
- Must align with NBA accreditation standards
- Respond in STRICT JSON only

JSON structure:
{{
  "peos": [
    {{
      "peo_id": "PEO1",
      "text": "Graduates will ...",
      "focus_area": "Industry/Research/Entrepreneurship/Society"
    }}
  ]
}}

Generate exactly {n_peos} PEOs now:"""


def build_po_prompt(programme_name: str, programme_description: str) -> str:
    return f"""You are an NBA/ABET accreditation expert.

Generate the 12 standard Program Outcomes (POs) for:
Programme: {programme_name}
Description: {programme_description}

RULES:
- Use the standard NBA 12 POs as reference
- Each PO must be specific and measurable
- Start with action verbs
- Respond in STRICT JSON only

JSON structure:
{{
  "pos": [
    {{
      "po_id": "PO1",
      "title": "Engineering Knowledge",
      "text": "Apply knowledge of mathematics, science and engineering fundamentals"
    }}
  ]
}}

Generate all 12 standard POs now:"""


def build_pso_prompt(programme_name: str, course_list: list, n_psos: int) -> str:
    courses = ", ".join(course_list) if course_list else "core programme courses"
    return f"""You are an NBA accreditation curriculum expert.

Generate exactly {n_psos} Program Specific Outcomes (PSOs) for:
Programme: {programme_name}
Core Courses: {courses}

RULES:
- PSOs are specific to this programme — not generic
- Must reflect domain-specific skills students will demonstrate at graduation
- Start with action verbs (Apply, Design, Develop, Analyze...)
- Must be measurable and assessable
- Respond in STRICT JSON only

JSON structure:
{{
  "psos": [
    {{
      "pso_id": "PSO1",
      "text": "Apply ... to ...",
      "domain": "specific domain area"
    }}
  ]
}}

Generate exactly {n_psos} PSOs now:"""