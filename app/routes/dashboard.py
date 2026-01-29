from fastapi import APIRouter
from datetime import datetime, date
from ..database import db

router = APIRouter()

@router.get("/stats", tags=["Dashboard"])
async def get_dashboard_stats():
    today = date.today().isoformat() # YYYY-MM-DD
    print(f"Dashboard Stats Query for Date: {today}")

    total_employees = await db["employees"].count_documents({})
    
    present_today = await db["attendance"].count_documents({
        "date": today,
        "status": "Present"
    })
    print(f"Present count: {present_today}")
    
    absent_today = await db["attendance"].count_documents({
        "date": today,
        "status": "Absent"
    })
    print(f"Absent count: {absent_today}")
    
    return {
        "total_employees": total_employees,
        "present_today": present_today,
        "absent_today": absent_today
    }
