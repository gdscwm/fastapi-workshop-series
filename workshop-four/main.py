from fastapi import FastAPI, Path, Query, HTTPException
from typing import Optional

from starlette.middleware.cors import CORSMiddleware

from admin import admin
from courses import COURSES
from models import Time, Course

my_courses = {}

my_times = {}

# create an instance of FastAPI
app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

app.include_router(admin, tags=["admin"])

"""""""""""""""""""""""""""""""""""""""""""""""""""
Workshop 1
"""""""""""""""""""""""""""""""""""""""""""""""""""


@app.get("/")
async def root():
    # return "Hello world"
    return {"message": "Hello world"}


# continue: run app
# pause here for line-by-line explanation, show can make path anything
# pause here for explanation of path operations
# pause here for JSON explanation, uncomment first return


# let's get into the seriesss
@app.get("/course/{course_id}")  # pause here for path param explanation
# begin with only course_id: int, then add = Path
async def get_course(course_id: int = Path(description="ID of the class you'd like to get",
                                           ge=1)):  # note that param must match path param, explain type hint & automatic fastapi type checking
    return COURSES[course_id]


"""""""""""""""""""""""""""""""""""""""""""""""""""
Workshop 2
"""""""""""""""""""""""""""""""""""""""""""""""""""


# show using API to update data with post
@app.put("/class/{course_id}/enroll")
async def enroll(course_id: int):
    course = COURSES[course_id]
    # v2 after next two endpoints
    if course["current_enr"] >= course["max_enr"]:
        raise HTTPException(403, detail="Class is full")
    course["current_enr"] += 1
    enrolled = f"{course['current_enr']}/{course['max_enr']}"
    return {"enrolled": enrolled}


# workshop 4
@app.delete("/class/{course_id}/enroll")
async def unenroll(course_id: int):
    return


# show query params - get a course by its name
@app.get("/course-name")
async def get_course(name: str):
    for course_id in COURSES:
        print(COURSES[course_id])
        if COURSES[course_id]["name"] == name:
            return COURSES[course_id]
    return {"course": "not found"}
    # raise HTTPException(404, detail="Course not found")


# show how this works with url -- enter 127.0.0.1/course-name?name=Data%20Visualization


# list courses
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


# now edit enroll endpoint to have if full, show error logic


# DIY endpoint - guide em thru it
@app.get("/course-by-prof/{prof}")
async def get_prof_courses(prof: str, open: bool):
    prof_courses = {}
    for course_id in COURSES:
        if COURSES[course_id]["professor"] == prof:
            if not open:
                prof_courses[course_id] = COURSES[course_id]
            elif open and COURSES[course_id]["current_enr"] < COURSES[course_id]["max_enr"]:
                prof_courses[course_id] = COURSES[course_id]
    if len(prof_courses) == 0:
        raise HTTPException(404, detail="No courses taught by this professor.")
    return prof_courses


"""""""""""""""""""""""""""""""""""""""""""""""""""
Workshop 3
"""""""""""""""""""""""""""""""""""""""""""""""""""


@app.get("/{course_id}/time")
async def get_course_times(course_id: int) -> Time:
    course = COURSES[course_id]
    if course:
        pass
