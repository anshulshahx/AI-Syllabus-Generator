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

Generate a complete syllabus in the EXACT FORMAT used by Indian technical universities.

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
Number of Units: {num_units}
{custom_text}

STRICT RULES:
1. Generate exactly {num_units} units
2. topics_paragraph must be comma-separated subtopics as one flowing paragraph ending with (8 hours)
3. Generate exactly 5 COURSE OBJECTIVES
4. Generate exactly 5 COURSE OUTCOMES labeled CO1 to CO5
5. Each unit has 3 unit objectives starting with Bloom verbs
6. Each unit has 2 unit outcomes starting with Bloom verbs
7. Each unit has 2 assessments
8. Each unit has 2 readings
9. Include 5 real textbooks with author, title, publisher, edition, year
10. Include 3 YouTube or NPTEL resources
11. Include 3 open source resources
12. Difficulty MUST match {programme.upper()} {education_level} {year_text}
13. RESPOND IN STRICT JSON ONLY

JSON FORMAT:
{{
  "course_name": "{course_name}",
  "course_code": "realistic code like CST-003",
  "education_level": "{education_level}",
  "programme": "{programme}",
  "year_of_study": {year_of_study if year_of_study else "null"},
  "semester": {semester if semester else "null"},
  "branch": "{branch_text}",
  "credits": {credits},
  "ltp": "{ltp}",
  "course_objectives": [
    "Objective 1",
    "Objective 2",
    "Objective 3",
    "Objective 4",
    "Objective 5"
  ],
  "course_outcomes": [
    "CO1: verb + outcome",
    "CO2: verb + outcome",
    "CO3: verb + outcome",
    "CO4: verb + outcome",
    "CO5: verb + outcome"
  ],
  "units": [
    {{
      "unit_id": "UNIT 1",
      "unit_title": "TITLE IN CAPS",
      "hours": 8,
      "topics_paragraph": "Topic1, Topic2, Topic3, Topic4, Topic5, Topic6, Topic7, Topic8. (8 hours)",
      "topics": ["Topic1","Topic2","Topic3","Topic4","Topic5","Topic6","Topic7","Topic8"],
      "unit_objectives": [
        "Understand ...",
        "Apply ...",
        "Analyze ..."
      ],
      "unit_outcomes": [
        "Apply knowledge of ...",
        "Design ... using ..."
      ],
      "assessments": ["Quiz on ...", "Assignment on ..."],
      "readings": ["Chapter X ...", "Chapter Y ..."]
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
    "NPTEL - Course Name - URL",
    "Channel - Topic - URL",
    "Channel - Topic - URL"
  ],
  "open_source_resources": [
    "Resource - Description - URL",
    "Resource - Description - URL",
    "Resource - Description - URL"
  ]
}}

Generate exactly {num_units} units now:"""


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

Generate a COMPLETELY DIFFERENT improved version with:
- Different unit titles and topic coverage
- Different Bloom verbs
- More specific measurable outcomes
- Reorganized topic sequence

{base}"""