from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Annotated
from courses import COURSES
from models import Course


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
def read_current_user(username: Annotated[HTTPBasicCredentials, Depends(authenticate)]):
    return {"username": username}


@admin.post("/add-course/{course_id}")
async def add_course(course_id: int,
                     course: Course,
                     username: Annotated[HTTPBasicCredentials, Depends(authenticate)]
                     ) -> Course:
    if course_id in COURSES:
        raise HTTPException(403, detail="Course already exists")
    COURSES[course_id] = course
    return COURSES[course_id]


@admin.delete("/delete-course/{course_id}")
async def delete_course(course_id: int,
                        username: Annotated[HTTPBasicCredentials, Depends(authenticate)]
                        ) -> Course:
    if course_id in COURSES:
        deleted = COURSES.pop(course_id)
        return deleted
    raise HTTPException(404, detail="Course not found")