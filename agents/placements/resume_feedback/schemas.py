# agents/placements/resume_feedback/schemas.py

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field


class ScopeClassifierOutput(BaseModel):
    label: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    reason: str


class IntentClassifierOutput(BaseModel):
    intent: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    clarification_needed: bool = False
    clarification_question: Optional[str] = None


class ResumeFollowupAnswerOutput(BaseModel):
    answer: str


class StructuredResumeAnalysis(BaseModel):
    summary: str
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    missing_elements: List[str] = Field(default_factory=list)
    improvement_suggestions: List[str] = Field(default_factory=list)
    ats_notes: List[str] = Field(default_factory=list)
    section_feedback: Dict[str, Any] = Field(default_factory=dict)
    score_breakdown: Dict[str, Any] = Field(default_factory=dict)