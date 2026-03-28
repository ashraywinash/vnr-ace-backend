from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class IntentOutput(BaseModel):
    intent: str
    clarification_needed: bool = False
    clarification_question: Optional[str] = None


class CandidateScore(BaseModel):
    candidate_id: str
    score: float
    reasoning: str