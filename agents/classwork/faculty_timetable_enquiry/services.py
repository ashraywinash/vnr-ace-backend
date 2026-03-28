# agents/classwork/faculty_timetable_enquiry/services.py

from __future__ import annotations

from typing import Any, Dict, List


class LLMService:
    def __init__(self, llm: Any):
        self.llm = llm

    def invoke_structured(self, system_prompt: str, user_prompt: str, schema: Any) -> Any:
        raise NotImplementedError("Wire this to your structured-output LLM stack.")

    def invoke_text(self, system_prompt: str, user_prompt: str) -> str:
        raise NotImplementedError("Wire this to your text LLM stack.")


class AuditLogRepository:
    def __init__(self, db_client: Any):
        self.db_client = db_client

    def persist_events(self, events: List[Dict[str, Any]]) -> None:
        if not events:
            return
        pass


class ReadOnlySQLRepository:
    """
    Replace with SQLAlchemy / psycopg / Supabase RPC / direct Postgres adapter.
    Must execute SELECT-only statements with bound parameters.
    """

    def __init__(self, db_client: Any):
        self.db_client = db_client

    def execute_read_only(self, sql_query: str, sql_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        # implement with a safe read-only DB user
        raise NotImplementedError("Wire this to your DB execution layer.")
        