# Workshop Two: Query Parameters

Let's review from workshop one:
- What is an API?
- What is JSON?
- What are the four main types of path operations, and what do they do?
- What does the command `uvicorn main:app --reload` do?

If you missed workshop one, go into the `workshop-one` directory in this repository and follow the steps to get FastAPI 
set up on your system.

## Wrapping up path parameters
### PUT endpoint
Dana Willner is the best professor ever, and I really want to enroll in her class. How can I do that?

We're going to use a `PUT` endpoint to update our dummy data. Copy this code into your `main.py`:
```python
@app.put("/class/{course_id}/enroll")
async def enroll(course_id: int):
    course = COURSES[course_id]
    course["current_enr"] += 1
    enrolled = f"{course['current_enr']}/{course['max_enr']}"
    return {"enrolled": enrolled}
```
What are we doing here? 
* `course = COURSES[course_id]` Use the `course_id` param to get the desired course (in dictionary form) from `COURSES`
* `course["current_enr"] += 1` Get the value of the course's `current_enr`, and add 1 to it
* `enrolled = f"{course['current_enr']}/{course['max_enr']}"` Craft a string to show the ratio of students enrolled to 
max number of students that can enroll in the course. (`f""` is just an easy way to pass variables into a string without concatenation.)
* `return {"enrolled": enrolled}` Return the enrollment count in dictionary form

Try it out in the docs!

Then go back to our `GET` endpoint and check the course again -- under `current_enr`, the value should now be 1.

### Optional Extension #1
___
Before we add more data to our `COURSES`, we may want to add some object-oriented design to aid us. For example,
creating a `Course` class may be useful, because all entries in `COURSES` have course names, professors, etc.

We'll get more into classes next work shop, but now it might be useful to have a class definition that looks like this:
```python
class Course:
   def __init__(self, [any params this class should know]):
      self.field = param
      ...
```
Our new `COURSES` dictionary should look something like:
```python
COURSES = {
    1: Course("Data Viz", "Dana Willner", etc.)
    ...
}
```
Or you could define your courses prior to the dictionary definition.  
Some things to think about:
1. Do we need the `COURSES` dictionary anymore? Or could we make the `course_id` an attribute of the `Course` class?
2. How do we need to update how we access and change `course` information in the endpoint functions in `main.py`?
___
## Query Parameters
First, we're going to expand our fake course database to have a little more to work with. Copy the dictionary below to the top of
your main.py, replacing the old dictionary:
```python
COURSES = {
    1: {
        "name": "Data Visualization",
        "professor": "Dana Willner",
        "current_enr": 34,
        "max_enr": 35,
    },
    2: {
        "name": "Data Structures",
        "professor": "Jim Deverick",
        "current_enr": 35,
        "max_enr": 35,
    },
    3: {
        "name": "Computational Problem Solving",
        "professor": "Timothy Davis",
        "current_enr": 30,
        "max_enr": 35,
    },
    4: {
        "name": "Intro to Data Science",
        "professor": "Dana Willner",
        "current_enr": 36,
        "max_enr": 35,
    }
}
```

### Optional extension #2
___
If you get here before the rest of the workshop -- Let's move this dictionary into a separate location, so `main.py` 
only has FastAPI endpoints. Decluttering your code as you go is good practice. 
1. Create a new python file in the same directory as `main.py`
2. Copy over the `COURSES` dictionary into your new file
3. Import the `COURSES` dictionary from your new file
___
Sweet! Now let's hit our new database with some API requests.

### What's a query parameter?

Query parameters are like more flexible path parameters. Any parameters you add to your function that are not defined as
path parameters (i.e. with curly brackets in the path) are interpreted as **query parameters**. Since they're not a fixed
part of the path, they can be optional and have default values.

`www.google.com/search?q=why+is+fastapi+great` <-- real example of a query parameter in action

Say we know the name of the course we want to get, but we don't know its id. We can use a query parameter to get the
course by its name instead. Copy this into your `main.py`:

``` python
@app.get("/course-name")
async def get_course(name: str):
    for course_id in COURSES:
        if COURSES[course_id]["name"] == name:
            return COURSES[course_id]
    return {"course": "not found"}
```

Notice that we don't have curly brackets in the path, but we still have a parameter passed into the function. This is 
the query parameter.

We add a query parameter to a URL with a question mark, after the path, like this:

`/path?query=value_to_pass_in`

If we were trying to find the information for "Data Visualization", we would visit
[http://127.0.0.1:8000/course-name?name=Data%20Visualization](http://127.0.0.1:8000/course-name?name=Data%20Visualization).
- The URL has the path we defined in our decorator, `/course-name`
- It's followed by a question mark to denote the query parameter
- The query name `name` is given
- `name` is set equal to `Data Visualization`, the course we're trying to get. (Note that since you can't have spaces in
URLs, they're notated as `%20`. Try typing in the URL with a space instead -- your browser will automatically convert
it to `%20`.)
- 
### Optional Extension #3
___
What else can you think of that we could `PUT` or `POST` to this "database" of courses? Could we update multiple fields
at once (e.g. update `professor` and `max_enr` in the same endpoint)? What if we wanted to create an entirely new class
entry in the `COURSES` "database"? 
1. Create a new endpoint to accomplish one of the tasks above, or come up with your own task!
    - Remember: Use `PUT` if you're updating existing data, and use `POST` if you're creating new data.
2. Think about what parameters you need, and how you want to pass them:
    - Should they be query or path params? Does it matter?
    - If you're updating data, you probably want corresponding params. If you're creating an entirely new class entry, 
   what params do you need?
3. Add some error handling to your endpoint! Let's assume for now we only want one class per name. You could also check 
if the class is over-enrolled.

___

### Optional and default values
We could have easily written the above function with a path parameter. What really makes query parameters useful and 
unique is that they can be made optional, or have default values assigned to them. This means that we can write one
endpoint to perform multiple functions for us.

Say we want to list all the courses in our course list, with the option to filter by whether the course is available
(not full) or not. 

We can use a query parameter `available` as that filter. By default, `available` is `False`, so our endpoint will return
all courses in the list. But, if we set it to `true`, our endpoint will only show courses whose `current_enr` is less
than its `max_enr`.

```python
from typing import Optional

# your other code here ...

@app.get("/list-courses")
async def list_courses(available: Optional[bool] = False):
    if available:
        available_courses = {}
        for course_id in COURSES:
            if COURSES[course_id]["current_enr"] < COURSES[course_id]["max_enr"]:
                available_courses[course_id] = COURSES[course_id]
        return available_courses
    return COURSES
```

Since we set a default value for `available`, the parameter is **optional**, i.e., we don't have to pass in a value for 
it ourselves.

We can also add documentation the way we did with path parameters. Replace your function declaration with this, and then
take a look at how the docs change:

```python
# notice that where we define the default value changes
async def list_courses(available: Optional[bool] = Query(default=False, description="True to show only classes with "
                                                                        "available seats. False to show all classes.")):
```
## Status Codes and Error Responses
So far, we've handled errors by just returning a fake JSONified error message, like in our `get_course` by name method:

```python
@app.get("/course-name")
async def get_course(name: str):
    for course_id in COURSES:
        if COURSES[course_id]["name"] == name:
            return COURSES[course_id]
    return {"course": "not found"}
```

This sort of works, as long as we're in the docs. But in the real world, you'd want to let the client using your API
know when something goes wrong. To do this, we can throw an **HTTP exception**, which changes the HTTP status code of 
the response. We can also add a detailed error response to go along with it. Common HTTP exceptions include:
- `200: OK`
- `404: Not Found`
- `403: Forbidden`
- `500: Internal Server Error`
- and [more](https://icecreamcode.org/posts/fastapi/http-exceptions/)

Let's add an HTTP exception to the `get_course` by name method.
```python
@app.get("/course-name")
async def get_course(name: str):
    for course_id in COURSES:
        if COURSES[course_id]["name"] == name:
            return COURSES[course_id]
    raise HTTPException(404, detail="Course not found")     # line changed here
```

Check out how this changes things in the docs.

Where else can we add HTTP exceptions? What error codes should we use?

## Try it yourself!
Write an endpoint that returns all courses taught by a professor, and can filter them by availability. (Hint: you will 
use **both** a path parameter and query parameter here!) Include an error response if there are no courses taught by the
professor.

```python
@app.[???]("/[???]")
async def get_prof_courses([???], [???]):
    # fill in here
```


### Sources
https://www.youtube.com/watch?v=-ykeT6kk4bk 

https://fastapi.tiangolo.com/

https://icecreamcode.org/posts/fastapi/http-exceptions/
