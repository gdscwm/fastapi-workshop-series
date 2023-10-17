from fastapi import FastAPI, Path, Query, HTTPException
from starlette.middleware.cors import CORSMiddleware
from typing import Optional
from courses import COURSES
from admin import admin

app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

app.include_router(admin, tags=["admin"])

my_courses= {}

my_times={}


@app.get("/")
async def root():
    return {"message": "Hello world"}


@app.get("/course/{course_id}")
async def get_course(course_id: int = Path(description="ID of the course to get", ge=1)):
    return COURSES[course_id]


@app.put("/class/{course_id}/enroll")
async def enroll(course_id: int):
    course = COURSES[course_id]
    if course["current_enr"] >= course["max_enr"]:
        raise HTTPException(403, detail="Class is full")
    course["current_enr"] += 1
    enrolled = f"{course['current_enr']}/{course['max_enr']}"
    return {"enrolled": enrolled}


@app.get("/course-name")
async def get_course(name: str):
    for course_id in COURSES:
        if COURSES[course_id]["name"] == name:
            return COURSES[course_id]
    raise HTTPException(404, detail="Course not found")


@app.get("/list-courses")
async def list_courses(available: Optional[bool] = Query(default=False, description="True to show only classes with "
                                                                        "available seats. False to show all classes.")):
    if available:
        available_courses = {}
        for course_id in COURSES:
            if COURSES[course_id]["current_enr"] < COURSES[course_id]["max_enr"]:
                available_courses[course_id] = COURSES[course_id]
        return available_courses
    return COURSES


@app.get("/get-prof-courses/{prof}")
async def get_prof_courses(prof: str, available: Optional[bool] = False):
    prof_courses = {}
    for course_id in COURSES:
        if COURSES[course_id]["professor"] == prof:
            if not available:
                prof_courses[course_id] = COURSES[course_id]
            if available and COURSES[course_id]["current_enr"] < COURSES[course_id]["max_enr"]:
                prof_courses[course_id] = COURSES[course_id]
    if len(prof_courses) == 0:
        raise HTTPException(404, "No courses taught by this professor found")
    return prof_courses