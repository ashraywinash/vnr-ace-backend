# agents/classwork/mail_automation/state.py

from typing import TypedDict, Optional, List, Dict, Any


class MailAutomationState(TypedDict, total=False):
    # identity
    user_id: str
    user_name: str
    user_role: str

    # conversation
    conversation_id: str
    user_query: str
    messages: List[Dict[str, str]]
    memory: List[Dict[str, Any]]

    # guardrails
    access_granted: bool
    safe_language: bool
    exploit_detected: bool
    in_scope: bool
    rejection_reason: Optional[str]

    # intent
    intent: Optional[str]
    interpreted_entities: Dict[str, Any]
    clarification_needed: bool
    clarification_question: Optional[str]

    # email draft
    recipients: List[str]
    recipient_type: Optional[str]   # section / faculty / custom
    subject: Optional[str]
    body: Optional[str]
    attachments: List[str]

    # approval
    approval_required: bool
    approval_status: Optional[str]
    human_approved: Optional[bool]
    approval_notes: Optional[str]
    waiting_for_human: bool

    # execution
    email_sent: bool
    send_status: Optional[str]

    # response
    final_response: Optional[str]

    # logs
    audit_events: List[Dict[str, Any]]