from pydantic import BaseModel, Field
from typing import Optional


class Time(BaseModel):
    days: str = Field(description="Course meeting days", pattern="^[MTWRF]+$")
    start: int
    end: int


class Course(BaseModel):
    name: str
    professor: str
    current_enr: Optional[int] = 0
    max_enr: int
    time: Time


