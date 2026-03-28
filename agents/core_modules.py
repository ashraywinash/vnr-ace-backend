# agents/core_modules.py

from typing import Any, Dict, List, Optional
from core.llm import groq_llm
from core.db import engine
from sqlalchemy import text
import json
import asyncio

class LLMService:
    """
    Concrete implementation of the agent's LLM interface.
    """
    def __init__(self):
        self.llm = groq_llm

    def invoke_structured(self, system_prompt: str, user_prompt: str, schema: Any) -> Any:
        """
        Uses with_structured_output if the schema is a Pydantic model.
        """
        structured_llm = self.llm.with_structured_output(schema)
        return structured_llm.invoke([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ])

    def invoke_text(self, system_prompt: str, user_prompt: str) -> str:
        """
        Generic text-in, text-out call.
        """
        response = self.llm.invoke([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ])
        return response.content

class AuditRepo:
    """
    Persists agent events to the audit_logs table.
    """
    def __init__(self):
        self.engine = engine

    async def persist_events(self, events: List[Dict[str, Any]]) -> None:
        if not events:
            return
        
        async with self.engine.begin() as conn:
            for event in events:
                # Map event keys to audit_log columns
                query = text("""
                    INSERT INTO audit_logs (event_type, user_id, agent_name, details)
                    VALUES (:event_type, :user_id, :agent_name, :details)
                """)
                await conn.execute(query, {
                    "event_type": event.get("event_type", "info"),
                    "user_id": event.get("user_id"),
                    "agent_name": event.get("agent_name", "unknown"),
                    "details": json.dumps(event.get("details", {}))
                })

    def persist(self, events: List[Dict[str, Any]]) -> None:
        """Synchronous wrapper for persist_events if needed by some nodes."""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If we are in an async loop, we should ideally use await
                # But if a node is sync, this is a fallback.
                loop.create_task(self.persist_events(events))
            else:
                loop.run_until_complete(self.persist_events(events))
        except Exception as e:
            print(f"Error persisting audit logs: {e}")

class EmailService:
    """
    Mock email service for mail_automation agent.
    """
    def send_email(self, recipients: List[str], subject: str, body: str) -> bool:
        print(f"DEBUG: Sending email to {recipients} | Subject: {subject}")
        # In a real app, use smtplib or an API like SendGrid
        return True

class SQLRepo:
    """
    Executes SQL queries for the faculty_timetable_enquiry agent.
    """
    def __init__(self):
        self.engine = engine

    async def execute_query(self, sql: str) -> List[Dict[str, Any]]:
        async with self.engine.connect() as conn:
            result = await conn.execute(text(sql))
            return [dict(row) for row in result.mappings().all()]

class AnalyticsRepo:
    """
    Placeholder for chart_generator analytics data.
    """
    def get_base_dataframe(self) -> Any:
        import pandas as pd
        # Return a mock or real DB-backed dataframe
        return pd.DataFrame([
            {"department": "CSE", "month": "Jan", "placements_count": 12, "avg_package": 8.1, "offers_count": 15, "company": "A"},
            {"department": "ECE", "month": "Jan", "placements_count": 9, "avg_package": 6.9, "offers_count": 10, "company": "A"},
        ])

class DashboardRepo:
    """
    Placeholder for live_dashboard data.
    """
    def get_dashboard_data(self) -> Dict[str, Any]:
        return {
            "stats": {"total_placements": 156, "avg_package": 12.5},
            "recent_activity": []
        }

class ResumeCacheRepo:
    """
    Placeholder for resume_feedback caching.
    """
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        return None
    def put(self, key: str, analysis: Dict[str, Any], metadata: Dict[str, Any]) -> None:
        pass
