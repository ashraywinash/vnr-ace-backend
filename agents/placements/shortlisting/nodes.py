from .constants import *
from .prompts import *
from .schemas import IntentOutput
from .utils import make_event


def access_node(state):
    if state["user_role"] not in ALLOWED_ROLES:
        state["final_response"] = STANDARD_MESSAGES["access_denied"]
        return state
    return state


def intent_node(state, llm):
    result: IntentOutput = llm.invoke_structured(
        INTENT_PROMPT,
        state["user_query"],
        IntentOutput
    )
    state["intent"] = result.intent
    state["clarification_needed"] = result.clarification_needed
    state["clarification_question"] = result.clarification_question
    return state


def clarification_node(state):
    state["final_response"] = state["clarification_question"]
    return state


def rag_shortlisting_node(state, rag_service=None):
    """
    This will call your RAG later
    """
    if not state.get("jd_text"):
        state["final_response"] = STANDARD_MESSAGES["no_jd"]
        return state

    # MOCK OUTPUT
    candidates = [
        {"id": "s1", "score": 8.7, "reason": "Strong ML + projects"},
        {"id": "s2", "score": 7.9, "reason": "Good DSA but less projects"},
        {"id": "s3", "score": 6.5, "reason": "Basic skills only"},
    ]

    state["shortlisted_candidates"] = candidates
    state["rag_executed"] = True
    return state


def response_node(state):
    candidates = state.get("shortlisted_candidates", [])

    if not candidates:
        state["final_response"] = STANDARD_MESSAGES["no_candidates"]
        return state

    state["final_response"] = f"Top Candidates:\n{candidates}"
    return state