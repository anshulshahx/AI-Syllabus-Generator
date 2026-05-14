from pydantic import BaseModel, validator, Field
from typing import List, Optional

VALID_BLOOM_LEVELS = ["remember", "understand", "apply", "analyze", "evaluate", "create"]

# ── Outcome Models ───────────────────────────────────────────────
class OutcomeRequest(BaseModel):
    course_name: str = Field(..., min_length=3, max_length=100)
    course_description: str = Field(..., min_length=10, max_length=1000)
    target_bloom_levels: Optional[List[str]] = ["remember", "understand", "apply"]
    n_candidates: int = Field(default=3, ge=1, le=10)

    @validator("course_name")
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("course_name cannot be empty or whitespace")
        return v.strip()

    @validator("target_bloom_levels")
    def valid_bloom_levels(cls, v):
        if v:
            for level in v:
                if level.lower() not in VALID_BLOOM_LEVELS:
                    raise ValueError(f"Invalid bloom level: '{level}'. Must be one of {VALID_BLOOM_LEVELS}")
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
    outcomes: List[OutcomeObject]

# ── Syllabus Models ──────────────────────────────────────────────
class SyllabusRequest(BaseModel):
    course_name: str = Field(..., min_length=3, max_length=100)
    course_description: str = Field(..., min_length=10, max_length=1000)
    num_units: int = Field(default=5, ge=1, le=10)

    @validator("course_name")
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("course_name cannot be empty")
        return v.strip()

class UnitObject(BaseModel):
    unit_id: str
    unit_title: str
    unit_objectives: List[str]
    unit_outcomes: List[str]
    assessments: List[str]
    readings: List[str]

class SyllabusResponse(BaseModel):
    course_name: str
    units: List[UnitObject]
    textbooks: List[str] = []
    youtube_resources: List[str] = []