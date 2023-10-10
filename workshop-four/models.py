from pydantic import BaseModel, Field
from typing import Optional


class Time(BaseModel):
    days: str = Field(description="days of week", pattern="^[MTWRF]+$")
    #start: int = Field(pattern="[0-2][0-9](00|30)$")
    start: int
    end: int


class Course(BaseModel):
    name: str
    professor: str
    current_enr: Optional[int] = 0
    max_enr: int
    time: Time


class CourseEnrollment(BaseModel):
    name: str
    current_enr: Optional[int] = 0
    max_enr: int


