# Workshop Three: Pydantic Models and Authentication

In case you missed the first workshop, look 
[here](https://github.com/gdscwm/fastapi-workshop-series/tree/main/workshop-one#setup) 
for setup instructions to get FastAPI up and running.

Let's review from our first two workshops:
- What is FastAPI?
- What is a path parameter? What does it look like?
- What is a query parameter? How is it different from a path parameter? What does it look like?

## Cleaning moment
Let's clean up our directory structure real quick to make our life easier as our API gets more complex.

In your `fastapi-workshop-series` directory, create a new file called `courses.py`. Copy this into it (it's the same 
course list we've been using, but with additional time data):
```python
COURSES = {
    1: {
        "name": "Data Visualization",
        "professor": "Dana Willner",
        "current_enr": 34,
        "max_enr": 35,
        "time": {
            "days": "TR",
            "start": 1100,
            "end": 1220
        }
    },
    2: {
        "name": "Data Structures",
        "professor": "Jim Deverick",
        "current_enr": 35,
        "max_enr": 35,
        "time": {
            "days": "TR",
            "start": 1330,
            "end": 1650
        }
    },
    3: {
        "name": "Computational Problem Solving",
        "professor": "Timothy Davis",
        "current_enr": 30,
        "max_enr": 35,
        "time": {
            "days": "TR",
            "start": 1100,
            "end": 1220
        }
    },
    4: {
        "name": "Intro Data Science",
        "professor": "Dana Willner",
        "current_enr": 36,
        "max_enr": 35,
        "time": {
            "days": "MWF",
            "start": 900,
            "end": 950
        }
    },
}
```

Now remove our old `COURSES` dictionary from `main.py` and add this line to the top :
```python
from courses import COURSES
```
This will just make our `main` a little less cluttered.

Create two new files in the same directory: `admin.py` and `models.py`. We'll be writing most of our code for this 
workshop in there.

## Routing
We now have a file admin.py, which we're going to write some API endpoints in. But, we don't want to create a whole 
nother API just for admin functions. We want some way to link it to the existing `app` instance of FastAPI in `main`.
To do this, we can use a **router**.

In `admin.py`, add the following code:
```python
from fastapi import APIRouter


admin = APIRouter()     # note how we declare this!
```
How do you think this will change how we write path operations in `admin.py?`

Now in `main.py`, add this:
```python
from admin import admin
#...

app = FastAPI()     # this was already here

app.include_router(admin, tags=["admin"])   # this tag will make for easy organization in the docs
```


## Pydantic models: Making 'em
A **request body** is data sent from the client to the API. A **response body** is what the API sends back to the 
client. APIs always provide a response, but we don't always need to send a request body.

When we do send request bodies, we typically do so using **Pydantic models**. Pydantic is a Python library used for data
parsing and validation. We're going to use it to be able to add and remove data from our course list, get some return 
type validation, and more.

In `models.py`, first import BaseModel from pydantic, then declare our new `Course` data model as a class that inherits 
from BaseModel:
```python
from pydantic import BaseModel
from typing import Optional


class Course(BaseModel):
    name: str
    professor: str
    current_enr: Optional[int] = 0
    max_enr: int
    time: dict
```
The variables defined under the model are called **attributes**.  Notice how all the attributes of the class here are 
the same as the ones in our course list. 

We define types for the attributes the way we can with path and query parameters. If you go to the FastAPI 
[docs](http://127.0.0.1:8000/docs) and scroll to the bottom, under `Schemas`, you can see our new `Course` model with 
documentation on all its attributes. Notice how the `time` attribute is of type `object`. That's not very useful, 
especially since we know that `time` will always have three attributes: `days`, `start`, and `end`. Wouldn't it be nice
if we could define that within the attribute?

Turns out, we can! With Pydantic models, you can use a model itself as a type. We can simply create a new `Time` model
for `Course` to use.
```python
from pydantic import BaseModel
from typing import Optional


class Time(BaseModel):
    days: str
    start: int
    end: int


class Course(BaseModel):
    name: str
    professor: str
    current_enr: Optional[int] = 0
    max_enr: int
    time: Time      # change down here!
```
Wow! So clean!

We can also add metadata and restrictions to attributes with `Field`, exactly the same way we did with `Query` and 
`Path`. Let's add some to `days` in our `time` model.
```python
from pydantic import BaseModel, Field   # new import
#...

class Time(BaseModel):
    days: str = Field(description="Course meeting days", pattern="^[MTWRF]+$")
    start: int
    end: int
```
We added a description to let us know what `days` represents, and a restriction on the characters `days` can be with
`pattern`. `pattern` uses something called a **regular expression**, a super powerful tool for string matching. All you
need to know for now is that `pattern="^[MTWRF]+$"` will accept only strings made up of the characters `M`, `T`, `W`, `R`, 
and `F`.

### Optional excursion: everyone loves regular expressions!
___
Regular expressions are a super powerful tool for string matching. They use certain **metacharacters** as special rules 
to describe what is and isn't allowed in a string. In the regular expression above, we used the metacharacters
- `^` assert the start of a line (this ensures no characters other than MTWRF will sneak in before our `days` string)
- `$` assert the end of a line (same as above, no non-weekday characters at the end)
- `[]` match a single character within the brackets
- `+` match one or more of the preceding character(s)

So, `^[MTWRF]+$` means a string must contain one or more repetitions of one or more of the characters `M`, `T`, `W`, 
`R`, and `F`, and no other characters.

There's a slight problem: this regular expression matches repetitions of the same character, like "MM", or "WFW". How 
can you rewrite the regular expression to not accept character repetitions?

[Here](https://www.keycdn.com/support/regex-cheat-sheet) is a metacharacter cheat sheet, 
and [here](https://regex101.com/) is a great place to test your regular expressions.
---

## Pydantic models: Using 'em
### Request Body
If a parameter is not present in the path, and it uses a Pydantic BaseModel, FastAPI interprets it as a request body. In
`admin.py`, let's try it out by writing an endpoint to create a new course using our new `Course` model.

```python
from fastapi import APIRouter, HTTPException    # added import here
from courses import COURSES     # import our course list
from models import Course       # import our Course Pydantic model


admin = APIRouter()


@admin.post('/add-course/{course_id}')       # note how we use @admin here since that's the name of our router
async def add_course(course_id: int, course: Course):
    if course_id in COURSES:
        raise HTTPException(403, detail="Course already exists")
    COURSES[course_id] = {"name": course.name, 
                          "professor": course.professor, 
                          "current_enr": course.current_enr,
                          "max_enr":  course.max_enr, 
                          "time": course.time}
    return COURSES[course_id]
```
Take a look at the docs. FastAPI will automatically show you what data needs to be entered in the request body. The body
of the function creates a new entry in our course list and assigns each field to the corresponding attribute in the 
`Course` data we wrote in our request body.

But that's a little complicated. Instead, we can assign the `COURSES` entry to the `Course` object, and FastAPI is smart
enough to convert all the attributes to JSON for us.

```python
@admin.post('/add-course/{course_id}')
async def add_course(course_id: int, course: Course):
    if course_id in COURSES:
        raise HTTPException(403, detail="Course already exists")
    COURSES[course_id] = course
    return COURSES[course_id]
```
With this, we can also use .{attribute} to access parts of a course instead of indexing with ["{attribute}"].

### Optional excursion: Can I see some ID?
___
We don't necessarily want to keep track of what course ids haven't yet been used in our course list, but we also want 
the option of putting in whatever unused id we want.

1. Edit the endpoint to make `course_id` optional. What needs to change?
2. Write some code to assign the course to the next available id in the list if one isn't provided. (Hint: count up the
number of entries in `COURSES`, then add 1.)
___

### Response Model – Return Type
You can also use Pydantic models to define a return type. In Python, we define return types with an arrow `->` in the 
function declaration, like this:
```python
def get_num_cats() -> int:
    return num_cats
```
The number of cats will obviously be an integer, and we can validate that by adding a return type.

Similarly, we can define a return type as a response model to validate the returned data. If the response body from
FastAPI isn't the model we expect (e.g. it's missing a field), that means something went wrong with our app. In that 
case, FastAPI will return a server error instead of returning incorrect data.

What endpoints do we have that should return course data as a `Course` type? `add_course`, for one. We can define the 
return type like this:

```python
@admin.post("/course/{course_id}")
async def add_course(course_id: int, course: Course) -> Course:   # change this line
    if course_id in COURSES:
        raise HTTPException(403, detail="Course already exists")
    COURSES[course_id] = course
    return COURSES[course_id]
```
If we look at the docs before reloading, we can see FastAPI tells us a successful response for `add_course` is just a
`"string"`. Now if we reload with our return type changes above, the successful response field becomes much more 
informative, because it's expecting a `Course` type to be returned.

Where else can we define the return type?

### Optional excursion: please don't let this course I need to graduate be full
___
Another reason we use Pydantic models as return types is to limit and filter the output data, which is especially useful
for security.

Say we only wanted to know the enrollment stats of a course. We could create a new model that only includes the course name and enrollment data, 
and uses that as the return type in an endpoint.

1. Create a new Pydantic model `CourseEnrollment` in `models.py` that only includes the fields `"name"`, 
`"current_enr"`, and `"max_enr"`.
2. Write a new endpoint `get_enrolled_data` in `main.py` that takes a course id as a parameter and returns type
`CourseEnrollment`. Hint: the body of your function should simply return the data from `COURSES` indexed by the course id
3. Look at the docs! What data is returned?
___


## Authentication
We don't want just anyone editing the course list, that'd be mayhem. We need to only allow admins the privilege to add
courses to the course list. We can do so using some simple authentication using FastAPI's security package.

In `admin.py`:
```python
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Annotated                # if you're running Python 3.9+, use this import
from typing_extensions import Annotated     # if you're running Python 3.6+, use this import
# more imports...


admin = APIRouter()

security = HTTPBasic()      # create a "security scheme"


@admin.get("/users/me")
def read_current_user(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    return {"username": credentials.username, "password": credentials.password}
```
`credentials` is type `HTTPBasicCredentials`, which includes a username and password. But note that it's `Annotated`,
which lets us add some metadata to it. In this case, we're using `security` as a **dependency** for `credentials`. In
other words, `credentials` has to follow all the rules set by our security scheme. These rules say that if you want to
hit this endpoint, you have to provide some log in information: a username and password. That log in information is 
stored in `HTTPBasicCredentials`.

Right now, this is super insecure. If you try to "execute" this endpoint in the docs, it'll take any username and 
password you give it as valid authentication. We can make it a little more secure by adding an authentication function
that will check to see if the credentials provided are correct.

```python
def authenticate(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    if not (credentials.username == "admin") or not (credentials.password == "password"):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
```

Now anytime we need authentication for an endpoint, we should use `authenticate` as a dependency instead of `security`
to make sure the proper credentials were given.
```python
@admin.get("/users/me")
# note how we use username instead of credentials because authenticate returns a username
async def read_current_user(username: Annotated[str, Depends(authenticate)]):
    return {"username": username}
```

Let's add the same authentication to `add_course`:
```python
@admin.post("/course/{course_id}")
async def add_course(course_id: int, 
                     course: Course, 
                     username: Annotated[str, Depends(authenticate)]   # change here
                     ) -> Course:
    if course_id in COURSES:
        raise HTTPException(403, detail="Course already exists")
    COURSES[course_id] = course
    return COURSES[course_id]
```


## DIY endpoint!
Write an endpoint in `admin.py` to delete a course from our course list. It should require authentication and return a
`Course` object.

___
### Sources

https://progressivecoder.com/a-guide-to-fastapi-request-body-using-pydantic-basemodel/

https://docs.pydantic.dev/latest/concepts/models/

https://fastapi.tiangolo.com/
