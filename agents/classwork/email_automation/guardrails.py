# agents/classwork/mail_automation/guardrails.py

from typing import Tuple
from .constants import ALLOWED_ROLES

UNSAFE_PATTERNS = {
    "hack", "bypass", "jailbreak", "drop table", "exploit"
}


def check_access(role: str) -> Tuple[bool, str | None]:
    if role.lower() in ALLOWED_ROLES:
        return True, None
    return False, "access_denied"


def check_language(query: str) -> Tuple[bool, bool, str | None]:
    q = query.lower()
    for p in UNSAFE_PATTERNS:
        if p in q:
            return False, True, "exploit"
    return True, False, None