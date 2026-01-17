from fastapi import FastAPI, HTTPException

from app.database import init_db
from app.schemas import (
    StudentCreate,
    GroupCreate,
    TransferStudent,
    StudentOut,
    GroupOut,
    StatusResponse,
)
from app import services

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
async def root():
    return {"message": "API is running"}


@app.post("/students", response_model=StudentOut, status_code=201)
async def create_student_endpoint(payload: StudentCreate):
    return services.create_student(student_name=payload.student_name)


@app.get("/students/{student_id}", response_model=StudentOut)
async def get_student_endpoint(student_id: int):
    student = services.get_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.get("/students", response_model=list[StudentOut])
async def list_students_endpoint():
    return services.list_students()


@app.delete("/students/{student_id}", response_model=StatusResponse)
async def delete_student_endpoint(student_id: int):
    ok = services.delete_student(student_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"status": "deleted"}


@app.post("/groups", response_model=GroupOut, status_code=201)
async def create_group_endpoint(payload: GroupCreate):
    return services.create_group(group_number=payload.group_number)


@app.get("/groups/{group_id}", response_model=GroupOut)
async def get_group_endpoint(group_id: int):
    group = services.get_group(group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group


@app.get("/groups", response_model=list[GroupOut])
async def list_groups_endpoint():
    return services.list_groups()


@app.delete("/groups/{group_id}", response_model=StatusResponse)
async def delete_group_endpoint(group_id: int):
    ok = services.delete_group(group_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Group not found")
    return {"status": "deleted"}


@app.post("/groups/{group_id}/students/{student_id}", response_model=StatusResponse)
async def add_student_to_group_endpoint(group_id: int, student_id: int):
    ok = services.add_student_to_group(student_id=student_id, group_id=group_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Student or group not found")
    return {"status": "student_added_to_group"}


@app.delete("/groups/{group_id}/students/{student_id}", response_model=StatusResponse)
async def remove_student_from_group_endpoint(group_id: int, student_id: int):
    ok = services.remove_student_from_group(student_id=student_id, group_id=group_id)
    if not ok:
        raise HTTPException(status_code=400, detail="Student not found or student is not in this group")
    return {"status": "student_removed_from_group"}


@app.get("/groups/{group_id}/students", response_model=list[StudentOut])
async def get_students_in_group_endpoint(group_id: int):
    students = services.get_students_in_group(group_id)
    if students is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return students


@app.post("/students/{student_id}/transfer", response_model=StatusResponse)
async def transfer_student_endpoint(student_id: int, payload: TransferStudent):
    ok = services.transfer_student(
        student_id=student_id,
        from_group_id=payload.from_group_id,
        to_group_id=payload.to_group_id,
    )
    if not ok:
        raise HTTPException(status_code=400, detail="Transfer failed (check ids and current student's group)")
    return {"status": "transferred"}
