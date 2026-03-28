from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from core.db import get_db
from core.deps import role_required
from sqlalchemy import select
from core.auth import get_current_user
from core.guardrails import check_input_guardrail, check_output_guardrail
from models.company_prep import CompanyPrepQuestion
from ace_graphs import placements_graph
# Import all graphs dynamically or by name
from ace_graphs.placements_graph import (
    dashboard_graph, resume_graph, prep_graph, 
    shortlisting_graph, tracking_graph, notification_graph
)
from ace_graphs.tp_admin_graph import tp_admin_agent

# New Agents
from agents.placements.graphs import (
    chart_generator_graph,
    live_dashboard_graph,
    resume_feedback_graph,
    shortlisting_graph
)

router = APIRouter(prefix="/placements", tags=["Placements"])

# Map graph_id to actual graph object
GRAPH_MAP = {
    "dashboard": dashboard_graph,
    "resume": resume_graph,
    "prep": prep_graph,
    "shortlisting": shortlisting_graph,
    "tracking": tracking_graph,
    "notification": notification_graph,
}

@router.get("/admin")
async def admin_access(user = Depends(role_required("admin"))):
    return {"message": "Placements Admin Access", "user": user.email}

@router.post("/admin/process-emails")
async def process_emails():
    """
    Triggers the autonomous T&P Admin Agent to process pending emails.
    """
    initial_state = {"messages": []}
    
    # Run graph asynchronously
    result = await tp_admin_agent.ainvoke(initial_state)
    
    # Extract the last AI message as the summary
    final_message = result.get("messages", [])[-1].content if result.get("messages") else "No result."
    
    return {
        "status": "success",
        "summary": final_message
    }

@router.get("/student")
async def student_access(user = Depends(role_required("student"))):
    return {"message": "Placements Student Access", "user": user.email}

@router.post("/chat/{graph_id}")
async def placements_chat(
    graph_id: str,
    body: dict,
    # current_user=Depends(get_current_user), # Bypassing for testing
    # db: AsyncSession = Depends(get_db)
):
    """
    Invokes the specific graph identified by graph_id.
    """
    if graph_id not in GRAPH_MAP:
        raise HTTPException(status_code=404, detail="Graph not found")
        
    target_graph = GRAPH_MAP[graph_id]

    message = body.get("message")
    if not message:
        # Default message if none provided (some widgets might just be 'triggers')
        message = "trigger"

    # Input Guardrail
    if message != "trigger" and not await check_input_guardrail(message):
        return {
            "reply": "I cannot process this request as it contains inappropriate or abusive language.",
            "graph": graph_id,
            "blocked": True
        }

    # Mock user for testing
    current_user_id = 999
    current_user_role = "student"

    # Prepare graph state
    initial_state = {
        "user_id": current_user_id,
        "role": current_user_role, 
        "message": message,
        "intent": graph_id, # Intent is implicit in the endpoint
        "authorized": False, 
        "response": None,
        "validation_status": None
    }

    # Run graph
    result = await target_graph.ainvoke(initial_state)
    reply = result.get("response")

    # Output Guardrail
    if reply and message != "trigger" and not await check_output_guardrail(reply, message):
        return {
            "reply": "I cannot provide a response to this request as it violates safety guidelines or contains sensitive information.",
            "graph": graph_id,
            "blocked": True
        }

    return {
        "reply": reply,
        "graph": graph_id
    }

# ---------------------------
#   NEW FEATURE ENDPOINTS
# ---------------------------

@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """
    Mock resume analysis endpoint.
    In reality, this would extract text and send to LLM.
    """
    return {
        "filename": file.filename,
        "analysis": "Resume Analysis Successful.\n\nStrengths: Good project diversity.\nWeaknesses: Formatting could be cleaner.\nScore: 8/10"
    }

@router.get("/dashboard-stats")
async def get_dashboard_stats():
    """
    Returns mock live data for the dashboard.
    """
    return {
        "stats": [
            {"label": "Total Placements", "value": "156", "trend": 18},
            {"label": "Avg Package", "value": "10-15 LPA", "trend": 5},
            {"label": "Active Offers", "value": "34", "trend": -2},
            {"label": "Placement Rate", "value": "92%", "trend": 1},
        ],
        "recent_placements": [
            {"name": "John Doe", "branch": "CSE", "company": "TechCorp", "package": "12 LPA"},
            {"name": "Jane Smith", "branch": "IT", "company": "Global Sol", "package": "10 LPA"},
            {"name": "Alice Brown", "branch": "ECE", "company": "Hardware Inc", "package": "8 LPA"},
        ]
    }

@router.get("/companies")
async def get_companies():
    return ["Google", "Microsoft", "Amazon", "TCS", "Infosys", "Wipro", "Accenture"]

@router.post("/shortlist")
async def shortlist_students(
    jd: str = Form(...),
    min_gpa: float = Form(None),
    branch: str = Form(None)
):
    """
    Mock shortlisting logic based on JD and criteria.
    """
    # Mock result list
    all_students = [
        {"id": 1, "name": "Student A", "gpa": 9.0, "branch": "CSE", "match": "95%"},
        {"id": 2, "name": "Student B", "gpa": 8.5, "branch": "IT", "match": "88%"},
        {"id": 3, "name": "Student C", "gpa": 7.5, "branch": "ECE", "match": "70%"},
        {"id": 4, "name": "Student D", "gpa": 8.8, "branch": "CSE", "match": "90%"},
    ]
    
    # Simple filtering
    filtered = []
    for s in all_students:
        if min_gpa and s["gpa"] < min_gpa:
            continue
        if branch and branch.lower() not in s["branch"].lower() and branch.lower() != "all":
            continue
        filtered.append(s)
        
    return {"matches": filtered}

@router.get("/prep/previous-questions")
async def get_previous_questions(company_name: str, db: AsyncSession = Depends(get_db)):
    """
    Fetch previous year interview experiences and questions for a specific company.
    """
    stmt = select(CompanyPrepQuestion).where(
        CompanyPrepQuestion.company_name.ilike(company_name)
    )
    result = await db.execute(stmt)
    record = result.scalars().first()
    
    if not record:
        raise HTTPException(status_code=404, detail="No previous questions found for this company")
        
    return {
        "company": record.company_name,
        "experiences": record.experiences or [],
        "questions": record.questions or []
    }

@router.post("/prep/company-questions")
async def get_company_questions(body: dict):
    """
    Generate top 20 company-specific interview questions.
    """
    company_name = body.get("company_name")
    if not company_name:
        raise HTTPException(status_code=400, detail="company_name is required")
    
    job_role = body.get("job_role", "Software Engineer")
    message = f"{company_name} {job_role}"

    # Input Guardrail
    if not await check_input_guardrail(message):
        raise HTTPException(status_code=400, detail="Input contains inappropriate or abusive language.")

    # Prepare state for prep_graph
    initial_state = {
        "user_id": 999,
        "role": "student",
        "message": message,
        "intent": "prep",
        "authorized": False,
        "response": None,
        "validation_status": None,
        "company_name": company_name,
        "job_role": job_role
    }
    
    try:
        # Run prep graph
        result = await prep_graph.ainvoke(initial_state)
        reply = result.get("response")
        
        # Output Guardrail
        if reply and not await check_output_guardrail(reply, message):
            raise HTTPException(status_code=500, detail="Generated output violated output safety guardrails.")
        
        return {
            "company": result.get("company_name"),
            "role": result.get("job_role"),
            "questions": result.get("questions", []),
            "formatted_response": result.get("response"),
            "context_loaded": bool(result.get("company_context", {}).get("company_info")),
            "web_search_results": len(result.get("search_results", []))
        }
    except Exception as e:
        print(f"Error generating company questions: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing questions: {str(e)}"
        )


# ---------------------------
#   NEW AGENT ENDPOINTS
# ---------------------------

@router.post("/chart-generator")
async def chart_generator(body: dict, current_user=Depends(role_required("admin"))):
    """
    Agent for generating placement charts and visualizations.
    """
    query = body.get("message")
    if not query:
        raise HTTPException(status_code=400, detail="Message required")

    initial_state = {
        "user_query": query,
        "user_role": "admin",
        "user_id": current_user.id,
        "memory": body.get("memory", []),
        "audit_events": []
    }
    
    result = await chart_generator_graph.ainvoke(initial_state)
    return {
        "reply": result.get("final_response"),
        "chart_path": result.get("chart_path"),
        "chart_type": result.get("chart_type"),
        "memory": result.get("memory")
    }

@router.post("/live-dashboard")
async def live_dashboard(body: dict, current_user=Depends(get_current_user)):
    """
    Agent for interacting with the live placement dashboard.
    """
    query = body.get("message", "load_dashboard")
    initial_state = {
        "user_query": query,
        "user_role": current_user.role_id,
        "user_id": current_user.id,
        "memory": body.get("memory", []),
        "audit_events": []
    }
    
    result = await live_dashboard_graph.ainvoke(initial_state)
    return {
        "reply": result.get("final_response"),
        "dashboard_data": result.get("dashboard_data"),
        "memory": result.get("memory")
    }

@router.post("/resume-feedback")
async def resume_feedback(body: dict, current_user=Depends(get_current_user)):
    """
    Agent for analyzing resumes and providing feedback.
    """
    query = body.get("message")
    if not query:
        raise HTTPException(status_code=400, detail="Message required")

    initial_state = {
        "user_query": query,
        "user_role": current_user.role_id,
        "user_id": current_user.id,
        "resume_text": body.get("resume_text"),
        "resume_id": body.get("resume_id"),
        "memory": body.get("memory", []),
        "audit_events": []
    }
    
    result = await resume_feedback_graph.ainvoke(initial_state)
    return {
        "reply": result.get("final_response"),
        "analysis": result.get("structured_analysis"),
        "memory": result.get("memory")
    }

@router.post("/shortlisting-agent")
async def shortlisting_agent_endpoint(body: dict, current_user=Depends(role_required("admin"))):
    """
    Agent for shortlisting students based on JD and criteria.
    """
    query = body.get("message")
    if not query:
        raise HTTPException(status_code=400, detail="Message required")

    initial_state = {
        "user_query": query,
        "user_role": "admin",
        "user_id": current_user.id,
        "jd_text": body.get("jd_text"),
        "audit_events": []
    }
    
    result = await shortlisting_graph.ainvoke(initial_state)
    return {
        "reply": result.get("final_response"),
        "shortlisted_students": result.get("shortlisted_students")
    }
