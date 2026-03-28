# agents/placements/shortlisting/utils.py

from datetime import datetime, timezone
from typing import Dict, Any


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def make_event(event_type, user_id, agent, details=None):
    return {
        "timestamp": utc_now(),
        "event_type": event_type,
        "user_id": user_id,
        "agent_name": agent,
        "details": details or {},
    }
