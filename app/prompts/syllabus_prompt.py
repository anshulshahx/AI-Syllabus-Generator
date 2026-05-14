def build_syllabus_prompt(course_name: str, course_description: str, num_units: int) -> str:
    prompt = f"""You are an expert curriculum designer for NBA-accredited engineering colleges.

Generate a complete unit-wise syllabus for:
Course Name: {course_name}
Course Description: {course_description}
Number of Units: {num_units}

STRICT RULES:
1. Generate exactly {num_units} units
2. Each unit must have a clear title
3. Each unit must have exactly 3 objectives starting with Bloom action verbs
4. Each unit must have exactly 2 outcomes starting with Bloom action verbs
5. Each unit must have 2 assessment methods
6. Each unit must have 2 recommended readings
7. Include exactly 3 real textbooks with author, title, publisher, year
8. Include exactly 3 YouTube channels or NPTEL playlists relevant to this course
9. Respond in STRICT JSON only — no markdown, no extra text

Use exactly this JSON structure:
{{
  "course_name": "{course_name}",
  "units": [
    {{
      "unit_id": "U1",
      "unit_title": "title here",
      "unit_objectives": [
        "objective 1 starting with bloom verb",
        "objective 2 starting with bloom verb",
        "objective 3 starting with bloom verb"
      ],
      "unit_outcomes": [
        "outcome 1 starting with bloom verb",
        "outcome 2 starting with bloom verb"
      ],
      "assessments": [
        "assessment method 1",
        "assessment method 2"
      ],
      "readings": [
        "reading 1",
        "reading 2"
      ]
    }}
  ],
  "textbooks": [
    "Author(s), Title, Publisher, Edition, Year",
    "Author(s), Title, Publisher, Edition, Year",
    "Author(s), Title, Publisher, Edition, Year"
  ],
  "youtube_resources": [
    "Channel Name - Description - URL",
    "Channel Name - Description - URL",
    "Channel Name - Description - URL"
  ]
}}

Generate exactly {num_units} units now:"""
    return prompt


def build_textbook_prompt(course_name: str) -> str:
    return f"""List exactly 3 well-known standard textbooks for: {course_name}

Output format (JSON only, no extra text):
{{
  "textbooks": [
    "Author(s), Title, Publisher, Edition, Year",
    "Author(s), Title, Publisher, Edition, Year",
    "Author(s), Title, Publisher, Edition, Year"
  ]
}}"""


def build_youtube_prompt(course_name: str) -> str:
    return f"""Suggest 3 YouTube channels or NPTEL playlists for learning: {course_name}

Use real channels like NPTEL, MIT OpenCourseWare, freeCodeCamp, Neso Academy.

Output format (JSON only, no extra text):
{{
  "youtube_resources": [
    "Channel Name - Description - URL",
    "Channel Name - Description - URL",
    "Channel Name - Description - URL"
  ]
}}"""