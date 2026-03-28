# agents/placements/resume_feedback/utils.py

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import hashlib


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


def trim_memory(memory: List[Dict[str, Any]], max_items: int = 20) -> List[Dict[str, Any]]:
    return memory[-max_items:]


def build_cache_key(user_id: str, resume_id: str | None, resume_text: str | None) -> str:
    base = f"{user_id}::{resume_id or ''}::{resume_text or ''}"
    return hashlib.sha256(base.encode("utf-8")).hexdigest()