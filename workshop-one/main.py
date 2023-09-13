from fastapi import FastAPI, Path

app = FastAPI()

COURSES = {
    1: {
        "name": "Data Visualization",
        "professor": "Dana Willner",
        "current_enr": 0,
        "max_enr": 35,
    }
}


@app.get("/")
async def root():
    return {"message": "Hello world"}


@app.get("/course/{course_id}")
async def get_course(course_id: int = Path(description="ID of the course to get", ge=1)):
    return COURSES[course_id]
