from pydantic import BaseModel, validator, Field
from typing import List, Optional

VALID_BLOOM_LEVELS = ["remember", "understand", "apply", "analyze", "evaluate", "create"]

class OutcomeRequest(BaseModel):
    course_name: str = Field(..., min_length=3, max_length=100)
    course_description: str = Field(..., min_length=10, max_length=1000)
    target_bloom_levels: Optional[List[str]] = ["remember", "understand", "apply"]
    n_candidates: int = Field(default=3, ge=1, le=10)
    education_level: Optional[str] = "undergraduate"
    programme: Optional[str] = "btech"
    year_of_study: Optional[int] = Field(default=None, ge=1, le=6)
    custom_prompt: Optional[str] = None

    @validator("course_name")
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("course_name cannot be empty")
        return v.strip()

    @validator("target_bloom_levels")
    def valid_bloom_levels(cls, v):
        if v:
            for level in v:
                if level.lower() not in VALID_BLOOM_LEVELS:
                    raise ValueError(f"Invalid bloom level: '{level}'")
        return v

    @validator("course_description")
    def description_not_empty(cls, v):
        if not v.strip():
            raise ValueError("course_description cannot be empty")
        return v.strip()

class OutcomeObject(BaseModel):
    text: str
    bloom_level: str
    assessment_suggestion: str
    confidence_est: float
    flags: List[str] = []
    domain_tags: List[str] = []

class OutcomeResponse(BaseModel):
    course_name: str
    education_level: str = "undergraduate"
    programme: str = "btech"
    year_of_study: Optional[int] = None
    outcomes: List[OutcomeObject]

class SyllabusRequest(BaseModel):
    course_name: str = Field(..., min_length=3, max_length=100)
    course_description: str = Field(..., min_length=10, max_length=1000)
    num_units: int = Field(default=5, ge=1, le=10)
    education_level: Optional[str] = "undergraduate"
    programme: Optional[str] = "btech"
    year_of_study: Optional[int] = Field(default=None, ge=1, le=6)
    semester: Optional[int] = Field(default=None, ge=1, le=12)
    branch: Optional[str] = None
    course_code: Optional[str] = None
    credits: Optional[int] = Field(default=4, ge=1, le=10)
    ltp: Optional[str] = "3:1:0"
    university_name: Optional[str] = "G.B. Pant Institute of Engineering & Technology, Pauri Garhwal"
    custom_prompt: Optional[str] = None
    regenerate: Optional[bool] = False
    rejection_reason: Optional[str] = None

    @validator("course_name")
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("course_name cannot be empty")
        return v.strip()

class UnitObject(BaseModel):
    unit_id: str
    unit_title: str
    topics_paragraph: str
    topics: List[str]
    unit_objectives: List[str]
    unit_outcomes: List[str]
    assessments: List[str]
    readings: List[str]
    hours: Optional[int] = 8

class SyllabusResponse(BaseModel):
    course_name: str
    course_code: Optional[str] = None
    education_level: str
    programme: str
    year_of_study: Optional[int] = None
    semester: Optional[int] = None
    branch: Optional[str] = None
    credits: Optional[int] = 4
    ltp: Optional[str] = "3:1:0"
    university_name: Optional[str] = None
    units: List[UnitObject]
    course_objectives: List[str] = []
    course_outcomes: List[str] = []
    textbooks: List[str] = []
    youtube_resources: List[str] = []
    open_source_resources: List[str] = []