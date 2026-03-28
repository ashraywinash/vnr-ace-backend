import os
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from sqlalchemy import select, func, desc
from core.db import get_db
from models.placement import Placement
from models.student import Student
from models.company import Company
from models.offer import Offer

router = APIRouter(prefix="/charts", tags=["Charts API"])

@router.get("/placement-trend")
async def get_placement_trend(db: Session = Depends(get_db)):
    # Group by year or month of placement_date. Let's assume year for trend.
    # Note: SQLite date functions differ from Postgres.
    # We will do a generic approach fetching dates and grouping in Python for safety
    # or use SQLAlchemy func.date_trunc if strictly Postgres.
    
    placements = db.execute(select(Placement.placement_date)).scalars().all()
    
    trends = {}
    for p_date in placements:
        if p_date:
            year = p_date.year
            trends[year] = trends.get(year, 0) + 1
            
    # Format for chart:
    result = [{"year": str(y), "count": count} for y, count in sorted(trends.items())]
    return result

@router.get("/branch-wise")
async def get_branch_wise_stats(db: Session = Depends(get_db)):
    # Total students per branch vs Placed per branch
    branches_query = select(Student.branch, func.count(Student.id)).group_by(Student.branch)
    total_by_branch = dict(db.execute(branches_query).all())
    
    placed_query = select(Student.branch, func.count(Student.id)).join(Placement).group_by(Student.branch)
    placed_by_branch = dict(db.execute(placed_query).all())
    
    result = []
    for branch, total in total_by_branch.items():
        if not branch:
            continue
        placed = placed_by_branch.get(branch, 0)
        percentage = round((placed / total * 100), 2) if total > 0 else 0
        result.append({
            "branch": branch,
            "total": total,
            "placed": placed,
            "percentage": percentage
        })
    
    return result

@router.get("/salary-distribution")
async def get_salary_distribution(db: Session = Depends(get_db)):
    # Group into buckets: < 5, 5-10, 10-15, > 15
    salaries = db.execute(select(Placement.ctc_lpa)).scalars().all()
    buckets = {"< 5 LPA": 0, "5 - 10 LPA": 0, "10 - 15 LPA": 0, "> 15 LPA": 0}
    
    for s in salaries:
        if s is None:
            continue
        if s < 5:
            buckets["< 5 LPA"] += 1
        elif s < 10:
            buckets["5 - 10 LPA"] += 1
        elif s < 15:
            buckets["10 - 15 LPA"] += 1
        else:
            buckets["> 15 LPA"] += 1
            
    return [{"bucket": k, "count": v} for k, v in buckets.items()]

@router.get("/company-wise")
async def get_company_wise_stats(db: Session = Depends(get_db)):
    # Top hiring companies
    query = select(Company.name, func.count(Placement.id)).join(Placement).group_by(Company.name).order_by(desc(func.count(Placement.id))).limit(10)
    data = db.execute(query).all()
    
    return [{"company": row[0], "hires": row[1]} for row in data]

@router.get("/minor-degree")
async def get_minor_degree_stats(db: Session = Depends(get_db)):
    # Impact of minor degree on placements
    with_minor = db.execute(select(func.count(Student.id)).filter(Student.minor_degree != None)).scalar() or 0
    with_minor_placed = db.execute(select(func.count(Student.id)).join(Placement).filter(Student.minor_degree != None)).scalar() or 0
    
    without_minor = db.execute(select(func.count(Student.id)).filter(Student.minor_degree == None)).scalar() or 0
    without_minor_placed = db.execute(select(func.count(Student.id)).join(Placement).filter(Student.minor_degree == None)).scalar() or 0
    
    return {
        "with_minor": {"total": with_minor, "placed": with_minor_placed},
        "without_minor": {"total": without_minor, "placed": without_minor_placed}
    }

@router.get("/multiple-offers")
async def get_multiple_offers(db: Session = Depends(get_db)):
    # Students with > 1 offer
    query = select(Offer.student_id, func.count(Offer.id)).group_by(Offer.student_id).having(func.count(Offer.id) > 1)
    multiple_offer_students = db.execute(query).all()
    count = len(multiple_offer_students)
    
    return {"students_with_multiple_offers": count}

class ChartQueryRequest(BaseModel):
    query: str

CHART_PROMPT = """
You are an intelligent router for a placement dashboard. The user is asking for a specific chart or data visualization.
Match the user's query to one of the following available chart identifiers:
- placement-trend : Shows the trend of placements over years/months.
- branch-wise : Shows total vs placed students and percentage per branch.
- salary-distribution : Shows how salaries are distributed into buckets (<5, 5-10, 10-15, >15 LPA).
- company-wise : Shows the top hiring companies and placement counts.
- minor-degree : Shows the impact of having a minor degree on placements.
- multiple-offers : Shows the count of students with multiple offers.

If the user's query matches one of these, reply with ONLY the exact identifier name from the list above. Do not include quotes, periods, or formatting.
If the query does not match any of these charts, reply with ONLY the word: unknown

User Query: {query}
"""

async def _process_dynamic_chart(query: str, db: Session):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="LLM API Key missing")
        
    llm = ChatGroq(model="llama3-8b-8192", temperature=0)
    prompt_template = PromptTemplate(template=CHART_PROMPT, input_variables=["query"])
    chain = prompt_template | llm
    
    try:
        response = await chain.ainvoke({"query": query})
        identifier = response.content.strip().lower()
        
        if identifier == "placement-trend":
            data = await get_placement_trend(db)
            return {"chart": "placement-trend", "data": data}
        elif identifier == "branch-wise":
            data = await get_branch_wise_stats(db)
            return {"chart": "branch-wise", "data": data}
        elif identifier == "salary-distribution":
            data = await get_salary_distribution(db)
            return {"chart": "salary-distribution", "data": data}
        elif identifier == "company-wise":
            data = await get_company_wise_stats(db)
            return {"chart": "company-wise", "data": data}
        elif identifier == "minor-degree":
            data = await get_minor_degree_stats(db)
            return {"chart": "minor-degree", "data": data}
        elif identifier == "multiple-offers":
            data = await get_multiple_offers(db)
            return {"chart": "multiple-offers", "data": data}
        else:
            return {"error": "Could not identify a matching chart.", "chart": "unknown"}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dynamic")
async def get_dynamic_chart(query: str, db: Session = Depends(get_db)):
    """
    Identify and return chart data based on a natural language text query (GET).
    """
    return await _process_dynamic_chart(query, db)

@router.post("/dynamic")
async def generate_dynamic_chart(request: ChartQueryRequest, db: Session = Depends(get_db)):
    """
    Identify and return chart data based on a natural language text query (POST).
    """
    return await _process_dynamic_chart(request.query, db)
