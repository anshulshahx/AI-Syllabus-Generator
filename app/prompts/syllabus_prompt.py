def get_programme_context(programme: str) -> str:
    contexts = {
        "btech":   "B.Tech Engineering following AICTE/NBA guidelines",
        "bsc":     "B.Sc Science following UGC guidelines",
        "bcom":    "B.Com Commerce following UGC guidelines",
        "ba":      "B.A Arts following UGC guidelines",
        "mtech":   "M.Tech Post-graduate Engineering following AICTE guidelines",
        "msc":     "M.Sc Post-graduate Science following UGC guidelines",
        "mca":     "MCA Computer Applications following AICTE guidelines",
        "bca":     "BCA Computer Applications undergraduate",
        "mcom":    "M.Com Post-graduate Commerce following UGC guidelines",
        "phd":     "PhD Doctoral level research curriculum",
        "diploma": "Diploma Technical curriculum following AICTE guidelines",
        "mbbs":    "MBBS Medical curriculum following MCI guidelines",
        "mba":     "MBA Business Administration following AICTE guidelines",
        "llb":     "LLB Law following BCI guidelines",
        "bed":     "B.Ed Education following NCTE guidelines",
        "barch":   "B.Arch Architecture following CoA guidelines",
    }
    return contexts.get(programme.lower(), "Standard university curriculum")


def build_syllabus_prompt(
    course_name: str,
    course_description: str,
    num_units: int,
    education_level: str = "undergraduate",
    programme: str = "btech",
    year_of_study: int = None,
    semester: int = None,
    branch: str = None,
    credits: int = 4,
    ltp: str = "3:1:0",
    custom_prompt: str = None
) -> str:

    year_text   = f"Year {year_of_study}" if year_of_study else "Not specified"
    sem_text    = f"Semester {semester}"  if semester      else "Not specified"
    branch_text = branch                  if branch        else "General"
    custom_text = f"\nADDITIONAL USER INSTRUCTIONS: {custom_prompt}" if custom_prompt else ""
    prog_ctx    = get_programme_context(programme)

    return f"""You are an expert curriculum designer for {prog_ctx}.

Generate a complete syllabus in the EXACT FORMAT used by Indian technical universities (UTU, VTU, AKTU, Anna University).

COURSE DETAILS:
Course Name: {course_name}
Course Description: {course_description}
Programme: {programme.upper()}
Education Level: {education_level}
Year of Study: {year_text}
Semester: {sem_text}
Branch: {branch_text}
Credits: {credits}
L:T:P: {ltp}
Number of Modules/Units: {num_units}
{custom_text}

STRICT RULES:
1. Generate exactly {num_units} units/modules
2. topics_paragraph MUST be a single flowing paragraph of comma-separated subtopics ending with period and hours like "(8 hours)" — exactly like UTU/VTU syllabus format
3. Generate exactly 5 COURSE OBJECTIVES — broad statements of what the course intends
4. Generate exactly 5 COURSE OUTCOMES labeled CO1 to CO5 — what students can do AFTER the course
5. Each unit has 3 unit objectives (CSOs) starting with Bloom action verbs
6. Each unit has 2 unit outcomes starting with Bloom action verbs
7. Each unit has 2 assessment methods
8. Each unit has 2 readings
9. Textbooks must be REAL published books with author, title, publisher, edition, year
10. YouTube resources must be REAL channels like NPTEL, MIT OCW, freeCodeCamp, Neso Academy
11. Open source resources must be REAL — GitHub repos, Coursera, edX, documentation sites
12. Difficulty MUST match {programme.upper()} {education_level} {year_text} {sem_text}
13. RESPOND IN STRICT JSON ONLY — no markdown, no explanation

JSON FORMAT:
{{
  "course_name": "{course_name}",
  "course_code": "realistic course code like CST-003",
  "education_level": "{education_level}",
  "programme": "{programme}",
  "year_of_study": {year_of_study if year_of_study else "null"},
  "semester": {semester if semester else "null"},
  "branch": "{branch_text}",
  "credits": {credits},
  "ltp": "{ltp}",
  "course_objectives": [
    "The idea of ... and their applications.",
    "To understand ...",
    "To evaluate ...",
    "To apply ...",
    "To acquaint students with ..."
  ],
  "course_outcomes": [
    "CO1: Remember the concept of ... and apply in solving real life problems.",
    "CO2: Apply the concept of ... to evaluate problems.",
    "CO3: Understand ... and solve related problems.",
    "CO4: Design and implement ... for given specifications.",
    "CO5: Evaluate ... and select appropriate methods."
  ],
  "units": [
    {{
      "unit_id": "UNIT 1",
      "unit_title": "TITLE IN CAPS",
      "hours": 8,
      "topics_paragraph": "Subtopic1, Subtopic2, Subtopic3, Subtopic4, Subtopic5, Subtopic6, Subtopic7, Subtopic8. (8 hours)",
      "topics": ["Subtopic1","Subtopic2","Subtopic3","Subtopic4","Subtopic5","Subtopic6","Subtopic7","Subtopic8"],
      "unit_objectives": [
        "Understand the fundamentals of ...",
        "Apply ... to solve ...",
        "Analyze ... to evaluate ..."
      ],
      "unit_outcomes": [
        "Apply knowledge of ... to ...",
        "Design ... using ..."
      ],
      "assessments": ["Quiz on ...", "Assignment on ..."],
      "readings": ["Chapter X of Textbook 1", "Chapter Y of Textbook 2"]
    }}
  ],
  "textbooks": [
    "1. Author, Title, Publisher, Edition, Year",
    "2. Author, Title, Publisher, Edition, Year",
    "3. Author, Title, Publisher, Edition, Year",
    "4. Author, Title, Publisher, Edition, Year",
    "5. Author, Title, Publisher, Edition, Year"
  ],
  "youtube_resources": [
    "NPTEL - Course Name - https://nptel.ac.in/...",
    "Channel Name - Topic - URL",
    "Channel Name - Topic - URL"
  ],
  "open_source_resources": [
    "Resource Name - Description - URL",
    "Resource Name - Description - URL",
    "Resource Name - Description - URL"
  ]
}}

Generate exactly {num_units} units for {programme.upper()} {education_level} {year_text} {sem_text} now:"""


def build_regenerate_prompt(
    course_name: str,
    course_description: str,
    num_units: int,
    education_level: str,
    programme: str,
    year_of_study: int = None,
    semester: int = None,
    branch: str = None,
    credits: int = 4,
    ltp: str = "3:1:0",
    rejection_reason: str = None,
    custom_prompt: str = None
) -> str:
    reason = f"REJECTION REASON: {rejection_reason}" if rejection_reason else "User was not satisfied"
    custom = f"USER INSTRUCTIONS: {custom_prompt}" if custom_prompt else ""
    base   = build_syllabus_prompt(
        course_name, course_description, num_units,
        education_level, programme, year_of_study,
        semester, branch, credits, ltp, custom_prompt
    )
    return f"""IMPORTANT: The user REJECTED the previous syllabus for "{course_name}".
{reason}
{custom}

Generate a COMPLETELY DIFFERENT improved version:
- Different unit titles and topic coverage
- Different Bloom verbs
- More specific measurable outcomes
- Reorganized topic sequence

{base}"""


def build_outcome_prompt(
    course_name: str,
    course_description: str,
    target_bloom_levels: list,
    n_candidates: int,
    education_level: str = "undergraduate",
    programme: str = "btech",
    year_of_study: int = None,
    custom_prompt: str = None
) -> str:
    levels      = ", ".join(target_bloom_levels)
    year_text   = f"Year {year_of_study}" if year_of_study else ""
    custom_text = f"\nADDITIONAL INSTRUCTIONS: {custom_prompt}" if custom_prompt else ""

    return f"""You are a curriculum designer for {programme.upper()} {education_level} {year_text}.

Generate exactly {n_candidates} Course Outcomes (COs) for:
Course: {course_name}
Description: {course_description}
Bloom Levels: {levels}
Programme: {programme.upper()} {education_level} {year_text}
{custom_text}

Rules:
- Each outcome MUST start with a Bloom action verb from: {levels}
- One verb per outcome only — no compound verbs
- Be specific and measurable
- Match difficulty to {programme.upper()} {education_level}
- VALID JSON ONLY. No explanation. No markdown.

Format:
{{"outcomes":[{{"text":"verb + outcome","bloom_level":"level","assessment_suggestion":"how to assess","confidence_est":0.9}}]}}

Generate {n_candidates} outcomes now:"""