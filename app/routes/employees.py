from fastapi import APIRouter, HTTPException, status, Body
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List
from ..models import EmployeeModel
from ..database import db
from bson import ObjectId

router = APIRouter()

@router.post("/", response_description="Add new employee", response_model=EmployeeModel, status_code=status.HTTP_201_CREATED, response_model_by_alias=True)
async def create_employee(employee: EmployeeModel = Body(...)):
    # Check for duplicate employee_id
    existing_employee = await db["employees"].find_one({"employee_id": employee.employee_id})
    if existing_employee:
        raise HTTPException(status_code=400, detail="Employee with this ID already exists")
    
    # Check for duplicate email
    existing_email = await db["employees"].find_one({"email": employee.email})
    if existing_email:
        raise HTTPException(status_code=400, detail="Employee with this email already exists")

    employee = jsonable_encoder(employee, exclude={"id"})
    new_employee = await db["employees"].insert_one(employee)
    created_employee = await db["employees"].find_one({"_id": new_employee.inserted_id})
    return created_employee

@router.get("/", response_description="List all employees", response_model=List[EmployeeModel], response_model_by_alias=True)
async def list_employees():
    employees = await db["employees"].find().to_list(1000)
    return employees

@router.delete("/{id}", response_description="Delete an employee", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(id: str):
    try:
        delete_result = await db["employees"].delete_one({"_id": ObjectId(id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    if delete_result.deleted_count == 1:
        return

    raise HTTPException(status_code=404, detail=f"Employee {id} not found")

@router.put("/{id}", response_description="Update an employee", response_model=EmployeeModel, response_model_by_alias=True)
async def update_employee(id: str, employee: EmployeeModel = Body(...)):
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    # Check if employee exists
    existing_employee = await db["employees"].find_one({"_id": oid})
    if not existing_employee:
        raise HTTPException(status_code=404, detail=f"Employee {id} not found")

    # If updating employee_id, check for duplicates (excluding self)
    if employee.employee_id != existing_employee["employee_id"]:
        dup_id = await db["employees"].find_one({"employee_id": employee.employee_id, "_id": {"$ne": oid}})
        if dup_id:
             raise HTTPException(status_code=400, detail="Employee with this ID already exists")

    # If updating email, check for duplicates (excluding self)
    if employee.email != existing_employee["email"]:
        dup_email = await db["employees"].find_one({"email": employee.email, "_id": {"$ne": oid}})
        if dup_email:
             raise HTTPException(status_code=400, detail="Employee with this email already exists")

    employee_data = jsonable_encoder(employee, exclude={"id", "created_at"}) # Exclude creation time update usually
    
    update_result = await db["employees"].update_one(
        {"_id": oid},
        {"$set": employee_data}
    )

    if update_result.modified_count == 1:
        updated_employee = await db["employees"].find_one({"_id": oid})
        return updated_employee

    return existing_employee # Return existing if no changes made
