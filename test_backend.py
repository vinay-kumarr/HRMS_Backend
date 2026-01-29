import requests
import sys

BASE_URL = "http://localhost:8001"

def test_backend():
    print("--- Starting Backend Test ---")
    
    # 1. Create Employee
    print("\n1. Testing Create Employee...")
    employee_data = {
        "employee_id": "TEST_BE_001",
        "full_name": "Backend Test User",
        "email": "betest@example.com",
        "department": "QA"
    }
    try:
        res = requests.post(f"{BASE_URL}/employees/", json=employee_data)
        if res.status_code == 201:
            emp_id = res.json().get("_id")
            print(f"PASS: Employee Created with ID: {emp_id}")
        elif res.status_code == 400 and "already exists" in res.text:
             print("NOTE: Employee already exists. Fetching existing ID...")
             # cleanup first
             all_emps = requests.get(f"{BASE_URL}/employees/").json()
             target = next((e for e in all_emps if e["employee_id"] == "TEST_BE_001"), None)
             if target:
                 requests.delete(f"{BASE_URL}/employees/{target['_id']}")
                 print("Cleaned up existing. Retrying create...")
                 res = requests.post(f"{BASE_URL}/employees/", json=employee_data)
                 emp_id = res.json().get("_id")
                 print(f"PASS: Employee Created with ID: {emp_id}")
        else:
            print(f"FAIL: Status {res.status_code}, Response: {res.text}")
            return
    except Exception as e:
        print(f"FAIL: Exception {e}")
        return

    # 2. Get Employee List
    print("\n2. Testing Get Employees...")
    res = requests.get(f"{BASE_URL}/employees/")
    if res.status_code == 200:
        emps = res.json()
        print(f"PASS: Found {len(emps)} employees")
        # Verify our user is there
        found = any(e["_id"] == emp_id for e in emps)
        if found: print("PASS: Created employee found in list")
        else: print("FAIL: Created employee NOT found in list")
    else:
        print(f"FAIL: Status {res.status_code}")

    # 3. Mark Attendance
    print("\n3. Testing Mark Attendance...")
    attendance_data = {
        "employee_id": "TEST_BE_001", # Using string ID as per model logic
        "date": "2023-10-27",
        "status": "Present"
    }
    res = requests.post(f"{BASE_URL}/attendance/", json=attendance_data)
    if res.status_code == 201:
        print(f"PASS: Attendance marked. Response: {res.json()}")
    elif res.status_code == 200:
        print(f"PASS: Attendance updated. Response: {res.json()}")
    else:
        print(f"FAIL: Status {res.status_code}, Response: {res.text}")

    # 4. Get Attendance
    print("\n4. Testing Get Attendance...")
    res = requests.get(f"{BASE_URL}/attendance/TEST_BE_001")
    if res.status_code == 200:
        recs = res.json()
        print(f"PASS: Found {len(recs)} records for user")
        if len(recs) > 0 and recs[0]["status"] == "Present":
            print("PASS: Verified record content")
        else:
             print("FAIL: Record content mismatch or empty")
    else:
        print(f"FAIL: Status {res.status_code}")

    # 5. Delete Employee
    print("\n5. Testing Delete Employee...")
    res = requests.delete(f"{BASE_URL}/employees/{emp_id}")
    if res.status_code == 204:
        print("PASS: Employee deleted")
        # Verify gone
        verify = requests.get(f"{BASE_URL}/employees/")
        found = any(e["_id"] == emp_id for e in verify.json())
        if not found: print("PASS: Confirmed deletion")
        else: print("FAIL: Employee still exists in list")
    else:
        print(f"FAIL: Status {res.status_code}, Response: {res.text}")

if __name__ == "__main__":
    test_backend()
