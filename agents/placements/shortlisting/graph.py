from langgraph.graph import StateGraph, END
from .state import ShortlistingState
from .nodes import *


def build_shortlisting_graph(llm, rag_service=None):
    g = StateGraph(ShortlistingState)

    g.add_node("access", access_node)
    g.add_node("intent", lambda s: intent_node(s, llm))
    g.add_node("clarification", clarification_node)
    g.add_node("rag", lambda s: rag_shortlisting_node(s, rag_service))
    g.add_node("response", response_node)

    g.set_entry_point("access")

    g.add_edge("access", "intent")
    g.add_conditional_edges("intent", lambda s: "clarification" if s["clarification_needed"] else "rag")
    g.add_edge("rag", "response")
    g.add_edge("clarification", END)
    g.add_edge("response", END)

    return g.compile()