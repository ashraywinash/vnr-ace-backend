# agents/classwork/faculty_timetable_enquiry/graph.py

from __future__ import annotations

from typing import Any
from langgraph.graph import StateGraph, END

from .state import FacultyTimetableEnquiryState
from .nodes import (
    access_control_node,
    language_guardrail_node,
    scope_classifier_node,
    intent_classifier_node,
    clarification_node,
    sql_generation_node,
    sql_safety_validation_node,
    sql_execution_node,
    answer_formatter_node,
    memory_update_node,
    persist_audit_logs_node,
)


def build_faculty_timetable_enquiry_graph(
    llm_service: Any = None,
    sql_repo: Any = None,
    audit_repo: Any = None,
):
    builder = StateGraph(FacultyTimetableEnquiryState)

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
        "sql_generation",
        lambda state: sql_generation_node(state, llm_service=llm_service),
    )
    builder.add_node("sql_safety_validation", sql_safety_validation_node)
    builder.add_node(
        "sql_execution",
        lambda state: sql_execution_node(state, sql_repo=sql_repo),
    )
    builder.add_node(
        "answer_formatter",
        lambda state: answer_formatter_node(state, llm_service=llm_service),
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
        return "clarification" if state.get("clarification_needed") else "sql_generation"

    def route_after_sql_validation(state):
        return "sql_execution" if state.get("sql_safe") else "persist_audit_logs"

    builder.add_conditional_edges("access_control", route_after_access)
    builder.add_conditional_edges("language_guardrail", route_after_language)
    builder.add_conditional_edges("scope_classifier", route_after_scope)
    builder.add_conditional_edges("intent_classifier", route_after_intent)
    builder.add_edge("sql_generation", "sql_safety_validation")
    builder.add_conditional_edges("sql_safety_validation", route_after_sql_validation)
    builder.add_edge("sql_execution", "answer_formatter")
    builder.add_edge("answer_formatter", "memory_update")
    builder.add_edge("memory_update", "persist_audit_logs")
    builder.add_edge("clarification", "persist_audit_logs")
    builder.add_edge("persist_audit_logs", END)

    return builder.compile()