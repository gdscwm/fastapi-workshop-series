from models import Course

COURSES = {
    1: {
        "name": "Data Visualization",
        "professor": "Dana Willner",
        "current_enr": 34,
        "max_enr": 35,
        "time": {
            "days": "W",
            "start": 0,
            "end": 0
        }
    },
    2: {
        "name": "Data Structures",
        "professor": "Jim Deverick",
        "current_enr": 35,
        "max_enr": 35,
        "time": {
            "days": "W",
            "start": 0,
            "end": 0
        }
    },
    3: {
        "name": "Computational Problem Solving",
        "professor": "Timothy Davis",
        "current_enr": 30,
        "max_enr": 35,
        "time": {
            "days": "W",
            "start": 0,
            "end": 0
        }
    },
    4: {
        "name": "Intro Data Science",
        "professor": "Dana Willner",
        "current_enr": 36,
        "max_enr": 35,
        "time": {
            "days": "W",
            "start": 0,
            "end": 0
        }
    },
}

# include time: slot, to have days of the week. something like
# "time": {
#     "Monday": [12:30, 14:00]
# }