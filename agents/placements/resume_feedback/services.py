# agents/placements/resume_feedback/services.py

from __future__ import annotations
from typing import Any, Dict, List, Optional


class LLMService:
    def __init__(self, llm: Any):
        self.llm = llm

    def invoke_structured(self, system_prompt: str, user_prompt: str, schema: Any) -> Any:
        raise NotImplementedError

    def invoke_text(self, system_prompt: str, user_prompt: str) -> str:
        raise NotImplementedError


class ResumeAnalysisCacheRepository:
    """
    Back by DB / Redis / document store.
    """

    def get(self, cache_key: str) -> Optional[Dict[str, Any]]:
        raise NotImplementedError

    def put(self, cache_key: str, analysis: Dict[str, Any], metadata: Dict[str, Any]) -> None:
        raise NotImplementedError


class ResumeRAGService:
    """
    Wrap your existing RAG pipeline here.
    For now we only define the contract.
    """

    def analyze_resume(self, resume_text: str | None, resume_path: str | None) -> Dict[str, Any]:
        """
        Return structured analysis dict compatible with StructuredResumeAnalysis.
        """
        # Placeholder implementation contract
        raise NotImplementedError


class AuditLogRepository:
    def __init__(self, db_client: Any):
        self.db_client = db_client

    def persist_events(self, events: List[Dict[str, Any]]) -> None:
        if not events:
            return
        pass