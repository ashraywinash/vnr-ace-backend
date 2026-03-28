from typing import TypedDict, Optional, List, Dict, Any


class ShortlistingState(TypedDict, total=False):
    user_id: str
    user_role: str
    user_query: str

    jd_text: Optional[str]

    candidates_pool: List[Dict[str, Any]]
    shortlisted_candidates: List[Dict[str, Any]]

    intent: Optional[str]
    clarification_needed: bool
    clarification_question: Optional[str]

    rag_executed: bool

    final_response: Optional[str]

    audit_events: List[Dict[str, Any]]