# agents/classwork/faculty_timetable_enquiry/utils.py

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def make_audit_event(
    event_type: str,
    user_id: str,
    agent_name: str,
    details: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    return {
        "timestamp": utc_now_iso(),
        "event_type": event_type,
        "user_id": user_id,
        "agent_name": agent_name,
        "details": details or {},
    }


def normalize_text(text: str) -> str:
    if not text:
        return ""
    return " ".join(text.strip().lower().split())


def trim_memory(memory: List[Dict[str, Any]], max_items: int = 20) -> List[Dict[str, Any]]:
    return memory[-max_items:]


def compact_rows(rows: List[Dict[str, Any]], limit: int = 10) -> List[Dict[str, Any]]:
    return rows[:limit]