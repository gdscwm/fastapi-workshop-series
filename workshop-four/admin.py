from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Annotated
from models import Course, CourseEnrollment
from courses import COURSES


admin = APIRouter()

security = HTTPBasic()


def authenticate(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    if not (credentials.username == "admin") or not (credentials.password == "password"):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@admin.get("/users/me")
async def read_current_user(username: Annotated[str, Depends(authenticate)]):
    return {"username": username}


@admin.post("/add-course/{course_id}")
async def add_course(course_id: int, course: Course, username: Annotated[str, Depends(authenticate)]) -> Course:
    if course_id in COURSES:
        raise HTTPException(403, detail="Course already exists")
    # show by accessing indiv params first, then with dict() method
    # COURSES[course_id] = {"name": course.name,
    #                       "professor": course.professor,
    #                       "current_enr": course.current_enr,
    #                       "max_enr":  course.max_enr,
    #                       "time": course.time}
    COURSES[course_id] = course
    return COURSES[course_id]


@admin.delete("/delete-course/{course_id}")
async def remove_course(course_id: int) -> Course:
    deleted = COURSES.pop(course_id)
    return deleted


@admin.get("/get-course/{course_id}/enrollment")
async def get_enrolled_data(course_id: int) -> CourseEnrollment:
    return COURSES[course_id]


#unfinished ignore this
@admin.put("/course/{course_id}/update", response_model=Course)
async def update_course_data(course_id: int, course_data: Course):
    if course_id in COURSES:
        COURSES[course_id] = course_data