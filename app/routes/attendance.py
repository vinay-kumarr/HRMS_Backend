from fastapi import APIRouter, HTTPException, status, Body
from fastapi.encoders import jsonable_encoder
from typing import List
from ..models import AttendanceModel
from ..database import db

router = APIRouter()

@router.post("/", response_description="Mark attendance", response_model=AttendanceModel, status_code=status.HTTP_201_CREATED, response_model_by_alias=True)
async def mark_attendance(attendance: AttendanceModel = Body(...)):
    # Verify employee exists
    employee = await db["employees"].find_one({"employee_id": attendance.employee_id})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Check if attendance already marked for this date
    existing_attendance = await db["attendance"].find_one({
        "employee_id": attendance.employee_id, 
        "date": attendance.date
    })
    
    if existing_attendance:
         # Update existing? Or Error? Requirement says "Mark attendance", usually implies creating. 
         # We can just update it or return error. Let's update it for better UX.
         await db["attendance"].update_one(
             {"_id": existing_attendance["_id"]},
             {"$set": {"status": attendance.status}}
         )
         updated_attendance = await db["attendance"].find_one({"_id": existing_attendance["_id"]})
         return updated_attendance

    attendance = jsonable_encoder(attendance, exclude={"id"})
    new_attendance = await db["attendance"].insert_one(attendance)
    created_attendance = await db["attendance"].find_one({"_id": new_attendance.inserted_id})
    return created_attendance

@router.get("/{employee_id}", response_description="List attendance records", response_model=List[AttendanceModel], response_model_by_alias=True)
async def list_attendance(employee_id: str):
    attendance_records = await db["attendance"].find({"employee_id": employee_id}).to_list(1000)
    return attendance_records
