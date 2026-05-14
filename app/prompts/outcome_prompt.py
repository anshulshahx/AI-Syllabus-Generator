def build_outcome_prompt(course_name: str, course_description: str, target_bloom_levels: list, n_candidates: int) -> str:
    levels = ", ".join(target_bloom_levels)
    prompt = f"""You are a curriculum designer. Generate exactly {n_candidates} learning outcomes for this course.

Course: {course_name}
Description: {course_description}
Bloom Levels to use: {levels}

Rules:
- Each outcome MUST start with a Bloom action verb
- One verb per outcome only
- Be specific and measurable

You MUST respond with valid JSON only. No explanation. No markdown. Just JSON.

Use exactly this structure:
{{"outcomes": [{{"text": "verb + object here", "bloom_level": "level here", "assessment_suggestion": "how to assess", "confidence_est": 0.9}}]}}

Generate {n_candidates} outcomes now in JSON:"""
    return prompt