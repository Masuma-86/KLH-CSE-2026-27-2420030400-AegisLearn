from enum import Enum
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field


class BloomLevel(str, Enum):
    REMEMBERING = "remembering"
    UNDERSTANDING = "understanding"
    APPLYING = "applying"
    ANALYZING = "analyzing"
    EVALUATING = "evaluating"
    CREATING = "creating"


class LearningStyle(str, Enum):
    VISUAL = "visual"
    VERBAL = "verbal"
    ACTIVE = "active"
    INTUITIVE = "intuitive"
    STANDARD = "standard"


class MasteryLevels(BaseModel):
    remembering: float = Field(default=50.0, ge=0.0, le=100.0)
    understanding: float = Field(default=50.0, ge=0.0, le=100.0)
    applying: float = Field(default=50.0, ge=0.0, le=100.0)
    analyzing: float = Field(default=50.0, ge=0.0, le=100.0)
    evaluating: float = Field(default=50.0, ge=0.0, le=100.0)
    creating: float = Field(default=50.0, ge=0.0, le=100.0)

    def get_average(self) -> float:
        scores = [
            self.remembering,
            self.understanding,
            self.applying,
            self.analyzing,
            self.evaluating,
            self.creating,
        ]
        return round(sum(scores) / len(scores), 2)


class StudentProfile(BaseModel):
    id: str
    name: str
    grade_level: str = "College"
    focus_subject: str = "Biology"
    streak: int = 1
    study_hours: float = 0.0
    mastery_levels: MasteryLevels = Field(default_factory=MasteryLevels)
    preferred_style: LearningStyle = LearningStyle.STANDARD


class RagChunk(BaseModel):
    id: str
    chapter_id: str
    title: str
    content: str
    source_citation: str
    similarity_score: Optional[float] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class DocumentIngestRequest(BaseModel):
    chapter_id: str
    title: str
    text_content: str
    source_citation: str = "Custom Upload"
    chunk_size: int = 350
    chunk_overlap: int = 50


class SearchRequest(BaseModel):
    query: str
    chapter_id: Optional[str] = None
    top_k: int = 3
    min_similarity: float = 0.05


class SearchResponse(BaseModel):
    query: str
    total_chunks_matched: int
    chunks: List[RagChunk]


class StudyGuideRequest(BaseModel):
    student_id: str
    chapter_id: str
    topic_query: str
    bloom_level: Optional[BloomLevel] = None
    learning_style: Optional[LearningStyle] = None
    top_k_chunks: int = 3


class StudyGuideResponse(BaseModel):
    student_id: str
    chapter_id: str
    topic_query: str
    target_bloom_level: BloomLevel
    applied_style: LearningStyle
    pedagogical_prompt: str
    grounded_context: List[RagChunk]
    generated_content: str
    hallucination_risk_score: float
    citations: List[str]


class QuizQuestion(BaseModel):
    id: str
    bloom_level: BloomLevel
    prompt: str
    options: List[str]
    correct_option_index: int
    explanation: str
    concept_tested: str


class QuizGenerateRequest(BaseModel):
    chapter_id: str
    topic: str
    num_questions: int = 3
    target_bloom_level: Optional[BloomLevel] = None


class QuizGenerateResponse(BaseModel):
    chapter_id: str
    topic: str
    questions: List[QuizQuestion]


class QuizSubmission(BaseModel):
    student_id: str
    question_id: str
    selected_option_index: int
    time_taken_seconds: float = 30.0


class QuizFeedbackResponse(BaseModel):
    question_id: str
    is_correct: bool
    correct_option_index: int
    explanation: str
    updated_mastery: MasteryLevels
    recommended_next_bloom: BloomLevel


class CitationMap(BaseModel):
    sentence: str
    matched_chunk_id: str
    grounding_confidence: float


class XaiExplainRequest(BaseModel):
    generated_text: str
    retrieved_chunk_ids: List[str]


class XaiExplainResponse(BaseModel):
    overall_grounding_score: float
    sentence_citations: List[CitationMap]
    key_contributing_concepts: List[str]
    transparency_summary: str
