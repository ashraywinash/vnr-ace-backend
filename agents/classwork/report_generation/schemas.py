# agents/classwork/report_generation/schemas.py

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class PlannerOutput(BaseModel):
    interpreted_intent: str = Field(..., description="Short intent label")
    report_type: str = Field(..., description="One of the allowed report types")
    filters: Dict[str, Any] = Field(default_factory=dict, description="Structured filters")
    required_datasets: List[str] = Field(default_factory=list, description="Dataset names needed")
    export_format: str = Field(default="xlsx", description="Requested export format")
    clarification_needed: bool = Field(default=False)
    clarification_question: Optional[str] = None


class ScopeClassifierOutput(BaseModel):
    label: str = Field(..., description="in_scope or out_of_scope")
    confidence: float = Field(..., ge=0.0, le=1.0)
    reason: str = Field(..., description="Why this classification was chosen")