# agents/classwork/mail_automation/schemas.py

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class IntentOutput(BaseModel):
    intent: str
    interpreted_entities: Dict[str, Any] = Field(default_factory=dict)
    clarification_needed: bool = False
    clarification_question: Optional[str] = None


class EmailDraftOutput(BaseModel):
    recipients: List[str]
    subject: str
    body: str