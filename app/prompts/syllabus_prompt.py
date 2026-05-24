# ── NBA 12 POs — Indian Universities ────────────────────────────
NBA_12_POS_TEXT = """PO1:  Engineering Knowledge — Apply mathematics, science, engineering fundamentals and specialization to solve complex engineering problems
PO2:  Problem Analysis — Identify, formulate, research literature and analyze complex engineering problems using principles of mathematics, natural sciences and engineering
PO3:  Design/Development of Solutions — Design solutions for complex engineering problems considering public health, safety, cultural, societal and environmental considerations
PO4:  Conduct Investigations of Complex Problems — Use research-based knowledge and methods including design of experiments, analysis, interpretation of data for complex problems
PO5:  Modern Tool Usage — Create, select and apply appropriate techniques, resources and modern engineering tools including IT tools for complex engineering activities
PO6:  The Engineer and Society — Apply contextual knowledge to assess societal, health, safety, legal and cultural issues and professional engineering responsibilities
PO7:  Environment and Sustainability — Understand the impact of professional engineering solutions in societal and environmental contexts and demonstrate knowledge for sustainable development
PO8:  Ethics — Apply ethical principles and commit to professional ethics, responsibilities and norms of engineering practice
PO9:  Individual and Team Work — Function effectively as an individual and as a member or leader in diverse teams in multidisciplinary settings
PO10: Communication — Communicate effectively on complex engineering activities — reports, effective presentations, give and receive clear instructions
PO11: Project Management and Finance — Demonstrate knowledge and understanding of engineering management and financial principles and apply these to one's own work
PO12: Life Long Learning — Recognize the need for and have the preparation and ability to engage in independent and lifelong learning"""


def get_programme_context(programme: str) -> str:
    contexts = {
        "btech":   "B.Tech Engineering — AICTE approved, NBA accredited, 4-year UG programme",
        "bsc":     "B.Sc Science — UGC-LOCF compliant, 3-year UG programme",
        "bcom":    "B.Com Commerce — UGC-LOCF compliant, 3-year UG programme",
        "ba":      "B.A Arts — UGC-LOCF compliant, 3-year UG programme",
        "mtech":   "M.Tech Post-graduate Engineering — AICTE approved, NBA accredited",
        "msc":     "M.Sc Post-graduate Science — UGC compliant",
        "mca":     "MCA — AICTE approved, NBA accredited, 3-year PG programme",
        "bca":     "BCA — UGC compliant, 3-year UG programme",
        "mcom":    "M.Com Post-graduate Commerce — UGC compliant",
        "phd":     "PhD — UGC compliant doctoral programme",
        "diploma": "Diploma — AICTE approved, State Board of Technical Education affiliated",
        "mbbs":    "MBBS — NMC/MCI approved medical programme",
        "mba":     "MBA — AICTE approved business programme",
        "llb":     "LLB — BCI approved law programme",
        "bed":     "B.Ed — NCTE approved teacher education programme",
        "barch":   "B.Arch — CoA approved architecture programme",
    }
    return contexts.get(programme.lower(), "UGC/AICTE approved university programme")


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

    year_text     = f"Year {year_of_study}" if year_of_study else "Not specified"
    sem_text      = f"Semester {semester}"  if semester      else "Not specified"
    branch_text   = branch                  if branch        else "General"
    custom_text   = f"\nADDITIONAL INSTRUCTIONS: {custom_prompt}" if custom_prompt else ""
    prog_ctx      = get_programme_context(programme)
    total_hours   = num_units * 8
    total_lectures = num_units * 9

    return f"""You are an expert Indian university curriculum designer strictly following NBA GAPC v4.0, AICTE, UGC-LOCF, NAAC and IQAC Outcome Based Education (OBE) framework for Indian universities.

Generate a complete DETAILED OBE-compliant syllabus exactly as required by Indian university NBA course files.

COURSE DETAILS:
Course Name: {course_name}
Course Description: {course_description}
Programme: {programme.upper()} — {prog_ctx}
Education Level: {education_level}
Year of Study: {year_text}
Semester: {sem_text}
Branch: {branch_text}
Credits: {credits}
L:T:P: {ltp}
Total Contact Hours: {total_hours} hours ({num_units} units × 8 hours)
Total Lectures: {total_lectures} lectures ({num_units} units × 9 lectures)
Standards: NBA GAPC v4.0, AICTE, UGC-LOCF, NAAC, IQAC, Bloom's Taxonomy
{custom_text}

NBA 12 PROGRAMME OUTCOMES (PO1-PO12) — Indian Standard:
{NBA_12_POS_TEXT}

INDIAN UNIVERSITY EXAM PATTERN:
Internal Assessment: 30 marks total
  — Unit Tests (2 tests): 20 marks
  — Assignments: 5 marks
  — Attendance: 5 marks
End Semester Examination: 70 marks
Total: 100 marks

NBA ATTAINMENT LEVELS (Indian Standard):
Level 3: 80% or more students score above 60% threshold
Level 2: 70-79% students score above 60% threshold
Level 1: 60-69% students score above 60% threshold
Level 0: Less than 60% students score above threshold

CO ATTAINMENT FORMULA: CO Attainment = (Direct Assessment × 0.8) + (Indirect Assessment × 0.2)
PO ATTAINMENT FORMULA: PO Attainment = Σ(CO_Attainment × CO-PO_Strength) / Σ(CO-PO_Strength)

STRICT RULES — ALL MANDATORY FOR INDIAN NBA COMPLIANCE:
1. Generate exactly {num_units} units of 8 hours each — total {total_hours} contact hours
2. Each unit MUST have minimum 12-15 DETAILED specific subtopics — NO vague general topics
3. topics_paragraph must be a DETAILED flowing comma-separated paragraph ending with (8 hours)
4. Generate exactly 5 COURSE OBJECTIVES — broad teaching intentions following UGC-LOCF format
5. Generate exactly 5 COURSE OUTCOMES CO1 to CO5 each with ALL fields:
   a. Bloom taxonomy action verb at start
   b. Bloom level declared (Remember/Understand/Apply/Analyze/Evaluate/Create)
   c. Bloom level number (L1/L2/L3/L4/L5/L6)
   d. Minimum 2 POs mapped from NBA 12 POs above
   e. Correlation strength per PO: 3=High 2=Medium 1=Low
   f. Minimum 1 PSO mapped
   g. Attainment target: 60% of students score above 60%
   h. Attainment level: 1 (initial target for new course)
   i. Direct assessment: Unit Test, Assignment, End Sem Exam mapped to marks
   j. Indirect assessment: Course End Survey
6. Generate COMPLETE CO-PO matrix — 5 COs × 12 POs — values 0/1/2/3
7. Generate COMPLETE CO-PSO matrix — 5 COs × 3 PSOs — values 0/1/2/3
8. Each unit must declare satisfied_cos — which COs it covers
9. Each unit must have:
   - 3 Course Specific Objectives with Bloom verb + level
   - 2 Course Specific Outcomes mapped to COs
   - Assessments mapped to specific COs and marks
   - 2 readings with chapter and textbook reference
   - lecture_plan: how 9 lectures are distributed in this unit
10. Include CQI plan — what action if CO attainment below target
11. Include 5 real textbooks modern editions 2015 onwards
12. Include 3 YouTube or NPTEL resources
13. Include 3 open source resources
14. Difficulty must match {programme.upper()} {education_level} {year_text}
15. lesson_plan_note: total {total_lectures} lectures in {num_units} units
16. naac_iqac_note: include NAAC and IQAC compliance statement
17. RESPOND IN STRICT JSON ONLY — no markdown no extra text

JSON FORMAT — exact structure required:
{{
  "course_name": "{course_name}",
  "course_code": "realistic Indian university code like PHY-101 or CS-301",
  "education_level": "{education_level}",
  "programme": "{programme}",
  "year_of_study": {year_of_study if year_of_study else "null"},
  "semester": {semester if semester else "null"},
  "branch": "{branch_text}",
  "credits": {credits},
  "ltp": "{ltp}",
  "total_hours": {total_hours},
  "total_lectures": {total_lectures},
  "standards": "NBA GAPC v4.0, AICTE, UGC-LOCF, NAAC, IQAC, Bloom's Taxonomy",
  "course_objectives": [
    "To understand the fundamental principles and concepts of ...",
    "To apply the theoretical knowledge of ... to solve practical problems",
    "To analyze ... using standard methods and techniques",
    "To evaluate ... for practical engineering/science applications",
    "To develop problem solving skills in ..."
  ],
  "course_outcomes": [
    {{
      "co_id": "CO1",
      "text": "Bloom verb + specific measurable outcome statement",
      "bloom_level": "Remember",
      "bloom_verb": "Define",
      "bloom_level_number": "L1",
      "mapped_pos": ["PO1", "PO2"],
      "po_correlation": {{"PO1": 3, "PO2": 2, "PO3": 0, "PO4": 0, "PO5": 0, "PO6": 0, "PO7": 0, "PO8": 0, "PO9": 0, "PO10": 0, "PO11": 0, "PO12": 1}},
      "mapped_psos": ["PSO1"],
      "pso_correlation": {{"PSO1": 3, "PSO2": 1, "PSO3": 0}},
      "attainment_target": "60% of students score above 60% marks",
      "attainment_level": 1,
      "direct_assessment": ["Unit Test I (20 marks)", "Assignment I (5 marks)"],
      "indirect_assessment": ["Course End Survey"],
      "unit_test_marks": 20,
      "assignment_marks": 5,
      "end_sem_marks": 70
    }},
    {{
      "co_id": "CO2",
      "text": "Bloom verb + specific measurable outcome statement",
      "bloom_level": "Understand",
      "bloom_verb": "Explain",
      "bloom_level_number": "L2",
      "mapped_pos": ["PO1", "PO3"],
      "po_correlation": {{"PO1": 2, "PO2": 0, "PO3": 3, "PO4": 0, "PO5": 0, "PO6": 0, "PO7": 0, "PO8": 0, "PO9": 0, "PO10": 0, "PO11": 0, "PO12": 1}},
      "mapped_psos": ["PSO1", "PSO2"],
      "pso_correlation": {{"PSO1": 2, "PSO2": 3, "PSO3": 0}},
      "attainment_target": "60% of students score above 60% marks",
      "attainment_level": 1,
      "direct_assessment": ["Unit Test I (20 marks)", "End Semester Exam (70 marks)"],
      "indirect_assessment": ["Course End Survey"],
      "unit_test_marks": 20,
      "assignment_marks": 5,
      "end_sem_marks": 70
    }},
    {{
      "co_id": "CO3",
      "text": "Bloom verb + specific measurable outcome statement",
      "bloom_level": "Apply",
      "bloom_verb": "Solve",
      "bloom_level_number": "L3",
      "mapped_pos": ["PO2", "PO3"],
      "po_correlation": {{"PO1": 0, "PO2": 3, "PO3": 2, "PO4": 0, "PO5": 1, "PO6": 0, "PO7": 0, "PO8": 0, "PO9": 0, "PO10": 0, "PO11": 0, "PO12": 0}},
      "mapped_psos": ["PSO2"],
      "pso_correlation": {{"PSO1": 1, "PSO2": 3, "PSO3": 2}},
      "attainment_target": "60% of students score above 60% marks",
      "attainment_level": 1,
      "direct_assessment": ["Unit Test II (20 marks)", "Assignment II (5 marks)", "End Semester Exam (70 marks)"],
      "indirect_assessment": ["Course End Survey"],
      "unit_test_marks": 20,
      "assignment_marks": 5,
      "end_sem_marks": 70
    }},
    {{
      "co_id": "CO4",
      "text": "Bloom verb + specific measurable outcome statement",
      "bloom_level": "Analyze",
      "bloom_verb": "Analyze",
      "bloom_level_number": "L4",
      "mapped_pos": ["PO2", "PO4"],
      "po_correlation": {{"PO1": 0, "PO2": 2, "PO3": 0, "PO4": 3, "PO5": 0, "PO6": 0, "PO7": 0, "PO8": 0, "PO9": 0, "PO10": 0, "PO11": 0, "PO12": 0}},
      "mapped_psos": ["PSO2", "PSO3"],
      "pso_correlation": {{"PSO1": 0, "PSO2": 2, "PSO3": 3}},
      "attainment_target": "60% of students score above 60% marks",
      "attainment_level": 1,
      "direct_assessment": ["Unit Test II (20 marks)", "End Semester Exam (70 marks)"],
      "indirect_assessment": ["Exit Survey"],
      "unit_test_marks": 20,
      "assignment_marks": 5,
      "end_sem_marks": 70
    }},
    {{
      "co_id": "CO5",
      "text": "Bloom verb + specific measurable outcome statement",
      "bloom_level": "Evaluate",
      "bloom_verb": "Evaluate",
      "bloom_level_number": "L5",
      "mapped_pos": ["PO3", "PO11", "PO12"],
      "po_correlation": {{"PO1": 0, "PO2": 0, "PO3": 2, "PO4": 0, "PO5": 0, "PO6": 0, "PO7": 0, "PO8": 0, "PO9": 0, "PO10": 0, "PO11": 2, "PO12": 3}},
      "mapped_psos": ["PSO3"],
      "pso_correlation": {{"PSO1": 0, "PSO2": 1, "PSO3": 3}},
      "attainment_target": "60% of students score above 60% marks",
      "attainment_level": 1,
      "direct_assessment": ["Assignment II (5 marks)", "End Semester Exam (70 marks)"],
      "indirect_assessment": ["Alumni Feedback Survey", "Course End Survey"],
      "unit_test_marks": 20,
      "assignment_marks": 5,
      "end_sem_marks": 70
    }}
  ],
  "co_po_matrix": {{
    "CO1": {{"PO1": 3, "PO2": 2, "PO3": 0, "PO4": 0, "PO5": 0, "PO6": 0, "PO7": 0, "PO8": 0, "PO9": 0, "PO10": 0, "PO11": 0, "PO12": 1}},
    "CO2": {{"PO1": 2, "PO2": 0, "PO3": 3, "PO4": 0, "PO5": 0, "PO6": 0, "PO7": 0, "PO8": 0, "PO9": 0, "PO10": 0, "PO11": 0, "PO12": 1}},
    "CO3": {{"PO1": 0, "PO2": 3, "PO3": 2, "PO4": 0, "PO5": 1, "PO6": 0, "PO7": 0, "PO8": 0, "PO9": 0, "PO10": 0, "PO11": 0, "PO12": 0}},
    "CO4": {{"PO1": 0, "PO2": 2, "PO3": 0, "PO4": 3, "PO5": 0, "PO6": 0, "PO7": 0, "PO8": 0, "PO9": 0, "PO10": 0, "PO11": 0, "PO12": 0}},
    "CO5": {{"PO1": 0, "PO2": 0, "PO3": 2, "PO4": 0, "PO5": 0, "PO6": 0, "PO7": 0, "PO8": 0, "PO9": 0, "PO10": 0, "PO11": 2, "PO12": 3}}
  }},
  "co_pso_matrix": {{
    "CO1": {{"PSO1": 3, "PSO2": 1, "PSO3": 0}},
    "CO2": {{"PSO1": 2, "PSO2": 3, "PSO3": 0}},
    "CO3": {{"PSO1": 1, "PSO2": 3, "PSO3": 2}},
    "CO4": {{"PSO1": 0, "PSO2": 2, "PSO3": 3}},
    "CO5": {{"PSO1": 0, "PSO2": 1, "PSO3": 3}}
  }},
  "exam_pattern": {{
    "internal_assessment": 30,
    "end_semester_exam": 70,
    "total": 100,
    "internal_breakdown": {{
      "unit_tests_2_tests": 20,
      "assignments": 5,
      "attendance": 5
    }}
  }},
  "attainment_formula": "CO Attainment = (Direct Assessment × 0.8) + (Indirect Assessment × 0.2)",
  "attainment_levels": {{
    "Level 3": "80% or more students score above 60% threshold",
    "Level 2": "70-79% students score above 60% threshold",
    "Level 1": "60-69% students score above 60% threshold",
    "Level 0": "Less than 60% students score above threshold"
  }},
  "po_attainment_formula": "PO Attainment = Σ(CO_Attainment × CO-PO_Strength) / Σ(CO-PO_Strength)",
  "cqi_plan": "1. Review CO attainment every semester end. 2. If any CO attainment < Level 1 (below 60%): redesign assessment, add remedial classes, change teaching method. 3. Document Action Taken Report (ATR) for each low attainment CO. 4. Present in IQAC meeting for approval. 5. Re-measure next semester to verify improvement.",
  "lesson_plan_note": "Total {total_lectures} lectures planned: {num_units} units × 9 lectures per unit. Lecture plan submitted separately as per NAAC requirements.",
  "naac_iqac_note": "This syllabus is prepared as per NBA GAPC v4.0, NAAC SSR criteria 1.1.2 and IQAC guidelines for Outcome Based Education in Indian higher education institutions.",
  "units": [
    {{
      "unit_id": "UNIT 1",
      "unit_title": "TITLE IN CAPS",
      "hours": 8,
      "satisfied_cos": ["CO1", "CO2"],
      "lecture_plan": "Lectures 1-2: Introduction and basics. Lectures 3-5: Core concepts. Lectures 6-7: Applications. Lecture 8-9: Problems and revision.",
      "topics_paragraph": "Subtopic1, Subtopic2, Subtopic3, Subtopic4, Subtopic5, Subtopic6, Subtopic7, Subtopic8, Subtopic9, Subtopic10, Subtopic11, Subtopic12, Subtopic13, Subtopic14, Subtopic15. (8 hours)",
      "topics": [
        "Subtopic1", "Subtopic2", "Subtopic3", "Subtopic4", "Subtopic5",
        "Subtopic6", "Subtopic7", "Subtopic8", "Subtopic9", "Subtopic10",
        "Subtopic11", "Subtopic12", "Subtopic13", "Subtopic14", "Subtopic15"
      ],
      "unit_objectives": [
        "Remember (Bloom L1): Define and list the fundamental concepts of ...",
        "Understand (Bloom L2): Explain and describe the working principles of ...",
        "Apply (Bloom L3): Solve numerical problems related to ... using standard formulas"
      ],
      "unit_outcomes": [
        "Students will be able to apply knowledge of ... to solve problems (maps to CO1)",
        "Students will be able to analyze ... and determine ... (maps to CO2)"
      ],
      "assessments": [
        "Unit Test I — Questions from this unit — mapped to CO1 and CO2 (20 marks)",
        "Assignment I — Numerical problems from this unit — mapped to CO1 (5 marks)"
      ],
      "readings": [
        "Chapter X: Title — Author, Textbook Name, Edition, Year",
        "Chapter Y: Title — Author, Textbook Name, Edition, Year"
      ]
    }}
  ],
  "textbooks": [
    "1. Author Surname, First Name, Title of Book, Publisher, Edition, Year",
    "2. Author Surname, First Name, Title of Book, Publisher, Edition, Year",
    "3. Author Surname, First Name, Title of Book, Publisher, Edition, Year",
    "4. Author Surname, First Name, Title of Book, Publisher, Edition, Year",
    "5. Author Surname, First Name, Title of Book, Publisher, Edition, Year"
  ],
  "youtube_resources": [
    "NPTEL - Course Name - Prof. Name - IIT/IISc - https://nptel.ac.in/courses/...",
    "MIT OpenCourseWare - Topic Name - https://ocw.mit.edu/...",
    "Khan Academy - Topic Name - https://www.khanacademy.org/..."
  ],
  "open_source_resources": [
    "PhET Interactive Simulations - University of Colorado - https://phet.colorado.edu",
    "MIT OpenCourseWare - Free Course Materials - https://ocw.mit.edu",
    "NPTEL SWAYAM - Free Online Courses - https://swayam.gov.in"
  ]
}}

Generate exactly {num_units} FULLY DETAILED OBE-COMPLIANT units following Indian university NBA GAPC v4.0 standards now:"""


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
    reason = f"REJECTION REASON: {rejection_reason}" if rejection_reason else "User not satisfied"
    custom = f"USER INSTRUCTIONS: {custom_prompt}" if custom_prompt else ""
    base   = build_syllabus_prompt(
        course_name, course_description, num_units,
        education_level, programme, year_of_study,
        semester, branch, credits, ltp, custom_prompt
    )
    return f"""IMPORTANT: User REJECTED the previous syllabus for "{course_name}".
{reason}
{custom}

Generate a COMPLETELY DIFFERENT improved version:
- Different unit titles and topic coverage
- More detailed subtopics minimum 12-15 per unit
- Better CO-PO mapping justification
- Different Bloom verb distribution across COs

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

    return f"""You are an Indian university curriculum designer following NBA GAPC v4.0 and AICTE OBE framework.

Generate exactly {n_candidates} Course Outcomes (COs) for:
Course: {course_name}
Description: {course_description}
Bloom Levels to use: {levels}
Programme: {programme.upper()} {education_level} {year_text}
{custom_text}

Rules:
- Each CO MUST start with a valid Bloom action verb from: {levels}
- One verb per CO — no compound verbs like understand and apply
- Be specific, measurable and achievable
- Match difficulty to {programme.upper()} {education_level}
- VALID JSON ONLY — no explanation no markdown

Format:
{{"outcomes":[{{"text":"verb + outcome","bloom_level":"level","assessment_suggestion":"assessment method","confidence_est":0.9}}]}}

Generate {n_candidates} outcomes now:"""