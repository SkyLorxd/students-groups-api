from pydantic import BaseModel, Field


class StudentCreate(BaseModel):
    student_name: str = Field(..., min_length=1, max_length=200)


class GroupCreate(BaseModel):
    group_number: str = Field(..., min_length=1, max_length=50)


class TransferStudent(BaseModel):
    from_group_id: int = Field(..., ge=10000_000, le=99999999)
    to_group_id: int = Field(..., ge=10000_000, le=99999999)


class StudentOut(BaseModel):
    id: int
    name: str
    group_id: int | None = None


class GroupOut(BaseModel):
    id: int
    group_number: str


class StatusResponse(BaseModel):
    status: str
