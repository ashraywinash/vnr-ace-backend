# ace_graphs/admissions_graph.py

import os
import re
from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional
from core.llm import call_llm

# ---------------------------
#   State Definition
# ---------------------------

class AdmissionsState(TypedDict):
    message: str
    reply: Optional[str]
    route: Optional[str]      # e.g., 'department_query', 'faq'
    dept_route: Optional[str] # specific department key

# ---------------------------
#   Load Department Data
# ---------------------------

DEPARTMENTS_DATA = {}
DEPT_DIR = "data/departments"

def sanitize_key(name):
    """Sanitizes file names to be used as graph node keys."""
    # Remove extension, lower case, replace non-alphanumeric with underscore
    name = os.path.splitext(name)[0]
    # Replace common separators with space then sanitize
    name = name.replace("&", " and ").replace(",", " ")
    key = re.sub(r'[^a-zA-Z0-9]', '_', name).lower()
    # Collapse multiple underscores
    key = re.sub(r'_+', '_', key)
    return key.strip('_')

if os.path.exists(DEPT_DIR):
    for filename in os.listdir(DEPT_DIR):
        if filename.endswith(".txt"):
            filepath = os.path.join(DEPT_DIR, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    key = sanitize_key(filename)
                    DEPARTMENTS_DATA[key] = {
                        "name": os.path.splitext(filename)[0],
                        "content": content
                    }
            except Exception as e:
                print(f"Error reading {filename}: {e}")

# ---------------------------
#   AGENTS
# ---------------------------

async def public_supervisor_agent(state: AdmissionsState):
    """
    This supervisor decides which agent should handle the message.
    """

    dept_list = ", ".join([info['name'] for info in DEPARTMENTS_DATA.values()])

    prompt = f"""
    You are the PUBLIC SUPERVISOR AGENT for VNR-ACE Admissions.

    Classify the following user message into EXACTLY one route:
    - faq: For general questions about admissions (eligibility, dates, fees) OR PLACEMENTS (job statistics, recruiters, highest package).
    - application_tracking: For questions about application status.
    - department_query: For questions about specific departments (e.g., {dept_list}) or courses.
    - admin_action: For admin-specific tasks.
    - unknown

    User message: {state['message']}

    Return ONLY the route name.
    """

    route = (await call_llm(prompt)).strip().lower()
    print(f"DEBUG: Supervisor Route Raw: {route}")

    if route not in ["faq", "application_tracking", "department_query", "admin_action"]:
        route = "faq"

    return {"route": route}


async def faq_agent(state: AdmissionsState):
    # If it's a general question about admissions, we can also use the 'admissions' department data if available
    admissions_context = ""
    if "admissions" in DEPARTMENTS_DATA:
        admissions_context = f"\nUse this background context if relevant:\n{DEPARTMENTS_DATA['admissions']['content']}\n"

    prompt = f"""
    You are the VNR-ACE Admissions FAQ Agent.
    Answer clearly and concisely.

    {admissions_context}

    Student question:
    {state['message']}
    
    IMPORTANT: Your scope is strictly limited to Admissions FAQs. If the question is outside of this scope, respond exactly with: 'I cannot handle this request, out of boundary. Please ask something related to Admissions.'
    """

    answer = await call_llm(prompt)
    return {"reply": answer}


async def tracking_agent(state: AdmissionsState):
    prompt = f"""
    You are the Application Tracking Agent for VNR-ACE.

    The user is asking about application status.

    Provide a helpful response.
    
    IMPORTANT: Your scope is strictly limited to Application Tracking. If the user asks anything outside of this scope, you MUST immediately respond exactly with: 'I cannot handle this request, out of boundary. Please ask something related to Application Tracking.'
    """

    answer = await call_llm(prompt)
    return {"reply": answer}


async def department_router_agent(state: AdmissionsState):
    dept_options = "\n".join([f"- {key}: {info['name']}" for key, info in DEPARTMENTS_DATA.items()])
    
    prompt = f"""
    You are the DEPARTMENT ROUTING AGENT for VNR-ACE.
    You help route the user to the correct Department Head.

    User query:
    {state['message']}

    Determine which department this message belongs to from the following list:
    {dept_options}
    - placements: Placement details, Training, T&P, Companies, Job Statistics
    - not_department

    Abbreviations Mapping (Reference):
    - CSE: Department of CSE&CSBS
    - ECE: Electronics & Communication Engineering
    - IT: Department of Information Technolog
    - EEE: Electrical & Electronics Engineering
    - EIE: Electronics Instrumentation Engineering
    - AI&DS: Artificial Intelligence & Data Science
    - CSBS: Department of CSE&CSBS

    Instructions:
    1. Select the most relevant department key.
    2. If the query mentions a specific department, its abbreviation, or its courses, pick that department.
    3. If the user asks about placements generally, return 'placements'.
    4. Return ONLY the department key (the string before the colon) and nothing else.
    """

    dept_key = (await call_llm(prompt)).strip().lower()
    print(f"DEBUG: Dept Router Raw: {dept_key}")
    
    # Try to find any known key in the response if it's too long
    matched_key = "not_department"
    if dept_key in DEPARTMENTS_DATA or dept_key == "placements":
        matched_key = dept_key
    else:
        # Check if any key exists as a word in the response
        words = re.split(r'[^a-zA-Z0-9_]', dept_key)
        for key in list(DEPARTMENTS_DATA.keys()) + ["placements"]:
            if key in words or key in dept_key:
                matched_key = key
                break
    
    if matched_key == "placements":
        print(f"DEBUG: Matched Placements")
        return {"dept_route": "placements"} # This will need a node or handling
    
    if matched_key in DEPARTMENTS_DATA:
        print(f"DEBUG: Matched Key: {matched_key}")
        return {"dept_route": matched_key}
    
    print(f"DEBUG: No Match for Key: {dept_key}")
    return {"dept_route": "not_department", "reply": "I'm sorry, I couldn't identify a specific department for your query. Please visit our website for more details."}


async def admin_agent(state: AdmissionsState):
    prompt = f"""
    You are the ADMIN SUPPORT AGENT for VNR-ACE Admissions.
    You ONLY assist administrators in performing tasks related to applications.

    Admin message:
    {state['message']}

    Provide a structured, useful response.
    
    IMPORTANT: Your scope is strictly limited to Admin Actions for Admissions. If the user asks anything outside of this scope, you MUST immediately respond exactly with: 'I cannot handle this request, out of boundary. Please ask something related to Admin Actions.'
    """

    answer = await call_llm(prompt)
    return {"reply": answer}


def create_department_agent(dept_key):
    dept_info = DEPARTMENTS_DATA[dept_key]
    dept_content = dept_info['content']
    dept_name = dept_info['name']

    async def department_agent(state: AdmissionsState):
        prompt = f"""
        You are the Head of the department: {dept_name} at VNRVJIET. 
        You have end-to-end knowledge about your department based on the following data:

        ---
        {dept_content}
        ---

        User Question: {state['message']}

        Instructions:
        1. Answer the user's question as the Head of Department. 
        2. Answer exclusively based on the provided data.
        3. If the answer is not in the data or if you are unsure, do NOT hallucinate. Instead, reply exactly with: "I can't confirm, visit website for more accurate details."
        4. Be professional, concise, and helpful.
        """
        answer = await call_llm(prompt)
        return {"reply": answer}
    
    return department_agent


# ---------------------------
#   GRAPH DEFINITION
# ---------------------------

builder = StateGraph(AdmissionsState)

builder.add_node("supervisor", public_supervisor_agent)
builder.add_node("faq", faq_agent)
builder.add_node("application_tracking", tracking_agent)
builder.add_node("department_router", department_router_agent)
builder.add_node("admin_action", admin_agent)

# Add department nodes dynamically
for dept_key in DEPARTMENTS_DATA.keys():
    builder.add_node(f"dept_{dept_key}", create_department_agent(dept_key))

# supervisor is entry
builder.set_entry_point("supervisor")

# Main routing logic
builder.add_conditional_edges(
    "supervisor",
    lambda state: state["route"],
    {
        "faq": "faq",
        "application_tracking": "application_tracking",
        "department_query": "department_router",
        "admin_action": "admin_action",
    },
)

# Department routing logic
dept_routing_map = {key: f"dept_{key}" for key in DEPARTMENTS_DATA.keys()}
dept_routing_map["not_department"] = END

builder.add_conditional_edges(
    "department_router",
    lambda state: state.get("dept_route", "not_department"),
    dept_routing_map
)

# Terminal nodes
builder.add_edge("faq", END)
builder.add_edge("application_tracking", END)
builder.add_edge("admin_action", END)

for dept_key in DEPARTMENTS_DATA.keys():
    builder.add_edge(f"dept_{dept_key}", END)

admissions_graph = builder.compile()

