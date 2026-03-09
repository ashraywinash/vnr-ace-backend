from fastapi import APIRouter
import random

router = APIRouter(prefix="/predictions", tags=["Predictions API"])

@router.get("/placement-percentage")
async def predict_placement_percentage():
    # Mocking statistical prediction
    base_rate = 85.5
    projected = base_rate + random.uniform(-2, 5)
    return {
        "current_rate": base_rate,
        "projected_end_of_year": round(projected, 2),
        "confidence": "80%"
    }

@router.get("/salary-trends")
async def predict_salary_trends():
    return {
        "current_avg": 8.5,
        "next_year_projected": 9.2,
        "trend_direction": "Upward"
    }

@router.get("/unplaced-risk")
async def get_unplaced_risk():
    return [
        {"student_roll": "20BD1A0501", "risk_score": 85, "reason": "Low CGPA, 2 Active Backlogs"},
        {"student_roll": "20BD1A0545", "risk_score": 70, "reason": "No Interships"}
    ]
