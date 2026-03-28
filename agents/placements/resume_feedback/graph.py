# agents/placements/resume_feedback/graph.py

from __future__ import annotations

from typing import Any
from langgraph.graph import StateGraph, END

from .state import ResumeFeedbackState
from .nodes import (
    access_control_node,
    language_guardrail_node,
    scope_classifier_node,
    intent_classifier_node,
    clarification_node,
    cache_lookup_node,
    rag_analysis_node,
    initial_analysis_response_node,
    followup_answer_node,
    memory_update_node,
    persist_audit_logs_node,
)


def build_resume_feedback_graph(
    llm_service: Any = None,
    rag_service: Any = None,
    cache_repo: Any = None,
    audit_repo: Any = None,
):
    builder = StateGraph(ResumeFeedbackState)

    builder.add_node("access_control", access_control_node)
    builder.add_node("language_guardrail", language_guardrail_node)
    builder.add_node(
        "scope_classifier",
        lambda state: scope_classifier_node(state, llm_service=llm_service),
    )
    builder.add_node(
        "intent_classifier",
        lambda state: intent_classifier_node(state, llm_service=llm_service),
    )
    builder.add_node("clarification", clarification_node)
    builder.add_node(
        "cache_lookup",
        lambda state: cache_lookup_node(state, cache_repo=cache_repo),
    )
    builder.add_node(
        "rag_analysis",
        lambda state: rag_analysis_node(state, rag_service=rag_service, cache_repo=cache_repo),
    )
    builder.add_node("initial_analysis_response", initial_analysis_response_node)
    builder.add_node(
        "followup_answer",
        lambda state: followup_answer_node(state, llm_service=llm_service),
    )
    builder.add_node("memory_update", memory_update_node)
    builder.add_node(
        "persist_audit_logs",
        lambda state: persist_audit_logs_node(state, audit_repo=audit_repo),
    )

    builder.set_entry_point("access_control")

    def route_after_access(state):
        return "language_guardrail" if state.get("access_granted") else "persist_audit_logs"

    def route_after_language(state):
        return "scope_classifier" if state.get("safe_language") else "persist_audit_logs"

    def route_after_scope(state):
        return "intent_classifier" if state.get("in_scope") else "persist_audit_logs"

    def route_after_intent(state):
        return "clarification" if state.get("clarification_needed") else "cache_lookup"

    def route_after_rag(state):
        if state.get("intent") == "analyze_resume":
            return "initial_analysis_response"
        return "followup_answer"

    builder.add_conditional_edges("access_control", route_after_access)
    builder.add_conditional_edges("language_guardrail", route_after_language)
    builder.add_conditional_edges("scope_classifier", route_after_scope)
    builder.add_conditional_edges("intent_classifier", route_after_intent)
    builder.add_edge("cache_lookup", "rag_analysis")
    builder.add_conditional_edges("rag_analysis", route_after_rag)
    builder.add_edge("initial_analysis_response", "memory_update")
    builder.add_edge("followup_answer", "memory_update")
    builder.add_edge("clarification", "persist_audit_logs")
    builder.add_edge("memory_update", "persist_audit_logs")
    builder.add_edge("persist_audit_logs", END)

    return builder.compile()