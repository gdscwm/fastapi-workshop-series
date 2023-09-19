# Workshop One: Hello, world!
## What is an API?
An API (Application Programming Interface) allows different applications to talk to each other. Think of an API like a waiter in a restaurant: the waiter takes your order,
sends it to the kitchen, waits for the kitchen to make your order, then the waiter brings it back to you.
In the same way, an API takes a request from an application and sends it to a server. The server then processes the request and sents the data back to the application. 
Now that the API has done its job, the application can interpret the data and present it to the user. 

## What is FastAPI?
It's a high-performance, super fast Python framework that integrates multiple powerful Python packages to simplify 
data access. It also just all around makes your life so much easier, and makes building APIs painless. Data is
automatically transformed to and from Python objects so you can simply code Python. Arguably the best part: it
creates automatic interactive documentation for your code.
## Setup
1. Create a directory for your code by opening the command line (if you're using Mac/Linux, open Terminal, if you're on Windows, use Powershell)
and enter the following commands:
```
mkdir fastapi-workshop-series
cd fastapi-workshop-series
```
You should now be in the directory `fastapi-workshop-series`.  
\
2. Now we want to create a virtual environment in the `fastapi-workshop-series` directory. Run the following commands:
```
python3 --version
```
We want to see a version greater than or equal to 3.7. If you don't have this, please raise your hand.
```
python3 -m venv [venvname]
```
Where you replace `[venvname]` with what you want your virtual environment to be called. _We strongly recommend calling it `.venv.`_  
\
3. Activate your virtual environment with the following command:
```
source [venvname]/bin/activate
```
So if you named your virtual environment `.venv`, the full command will look like:
```
source .venv/bin/activate
```
If this command does not work for you, refer to [the python documentation](https://docs.python.org/3/library/venv.html#how-venvs-work) for further options, and raise your hand.  
\
4. Confirm that things are set up correctly using the following command:
```
pip list
```
you should see two packages: `pip` and `setuptools`. If you see these packages, you're ready to move onto package installation!


## Package installation
1. Open up your command line (if you're using Mac/Linux, this will be Terminal, if you're on Windows, use Powershell)
and enter the following commands:
```commandline
pip install fastapi
pip install uvicorn
```
If that doesn’t work, try these variations for both fastapi and uvicorn:

`pip3 install fastapi`

`python -m pip install fastapi`

`python3 -m pip3 install fastapi`

If it still doesn’t work, raise your hand and someone will come help you out.

2. Open up your favorite IDE (place to write code). If you don’t have one, we recommend PyCharm.
3. Create a new file `main.py`. If you’re using VSCode, install the Python package.

### Hello, world!
In your main.py, copy this code:
```python
from fastapi import FastAPI     # note the capitalization!

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello world"}
```
Now in your terminal, run this command:
```commandline
uvicorn main:app --reload
```
Note: if this doesn't work and you're in your system terminal, try running it in your IDE's built-in terminal.

Let's break down this command:
* `main` refers to the file name
* `app` refers to object of FastAPI created inside our `main.py` file
* `--reload` tells uvicorn to automatically restart the server when it detects changes in `main.py`

Now, go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/). You should see a `{"message":"Hello world"}` -- exactly what we returned from our FastAPI endpoint!

Let's break down our `main.py` code, line by line.
* `from fastapi import FastAPI` We import FastAPI, which is a Python class that provides all the functionality for the API.
* `app = FastAPI()` We create an instance of the class FastAPI and name it app. This is the app referred to by uvicorn in the above command.
* `@app.get("/")` This is a **path operation decorator**. GET is a type of **path operation** (more on those below).
What's inside the parentheses is our **path**, which is what gets typed into the URL.
* `async def root():` We define the function that will execute whenever someone visits the above path.
* `return {"message": "Hello world"}` We return a response to the client whenever the route is accessed.

### Path Operations
There are many different path operations, but the vast majority of the time, you use these four:
- **GET**: read data
- **POST**: create data
- **PUT**: update data
- **DELETE**: delete data


#### A quick note on JSON
In our function above, we return a Python dictionary. (Python dictionaries are used to store data as key/value pairs, written as {key:value}. If you access a key in a dictionary, it returns its value.)
This dictionary is automatically converted by FastAPI into JSON. JSON is the standard way to send and receive information from an endpoint, because it makes the information easy to understand and access,
as we'll see later in this workshop.

### The docs
Go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). 
These are the FastAPI docs. FastAPI automatically generates interactive documentation for your code, which is one of the biggest draws to using it.

There should be one `GET` endpoint in there right now for our "Hello World" function we wrote. Click on it to expand, click the `Try it out` button
in the top right, and click `Execute`. Under "Response body", you should see the same `{"message": "Hello world"}`. We use the docs because they're 
easier to understand, and offer more information when something goes wrong.

# Let's make an API!
Add this to the top of your file, right below the import statements:
```python
COURSES = {
    1: {
        "name": "Data Visualization",
        "professor": "Dana Willner",
        "current_enr": 0,
        "max_enr": 35
    },
}
```
We'll use this as some dummy data to simulate the data in the opencourselist. 

## Path parameters

Copy this endpoint below your `root` endpoint:
```python
@app.get("/course/{course_id}")
async def get_course(course_id: int):
    return COURSES[course_id]
```
This endpoint uses a **path parameter**. The path parameter is enclosed in {curly braces}, and always has a matching
function parameter. Whatever you pass in as a parameter to the function is added to the URL path in place of the path 
parameter. This simplifies the API by allowing it to use the same endpoint for a bunch of different items. 

Let's look at what this endpoint is doing. We're using a `GET` method, so we're reading data. We restrict `course_id` 
to be an int, so FastAPI will automatically type check the input and make sure the user inputs an integer. Then we return
the course from `COURSES` corresponding to the course id we passed in.

Go to the FastAPI docs, and under the `course/{course_id}` endpoint, "try it out" and enter `1` next to `course_id`. 
It returns the entry in the dummy course data we added!

Try out some other values. What information does FastAPI give you when you put in a different integer? A string?

There's a bunch of cool things FastAPI will do for you to make your life easier. In path parameters, it can add 
validation and metadata to the parameter, like the int type checking we saw above. You can do more using the `Path` function.

Add `Path` to your list of imports from `fastapi` at the top, like so:
```python
from fastapi import FastAPI, Path
```
and change this line to add path validation:
```python
async def get_course(course_id: int = Path(description="ID of the class you'd like to get", ge=1)):
```
Go back into your FastAPI docs, and see that the description now pops up next to the `course_id` variable.
`ge` means you must enter an integer greater than or equal to one. 

What happens if you enter 0? What if you go to [http://127.0.0.1:8000/course/0](http://127.0.0.1:8000/course/0)?

# This is where we stopped. We'll go over the code below in Workshop Two.

#### PUT endpoint
Dana Willner is the best professor ever, and I really want to enroll in her class. How can I do that?

We're going to use a `PUT` endpoint to update our dummy data. Copy this code into your main.py:
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
* `course["current_enr"] += 1` Get the value of the courses `current_enr`, and add 1 to it
* `enrolled = f"{course['current_enr']}/{course['max_enr']}"` Craft a string to show the ratio of students enrolled to 
max number of students that can enroll in the course. (`f""` is just an easy way to pass variables into a string without concatenation.)
* `return {"enrolled": enrolled}` Return the enrollment count in dictionary form

Try it out in the docs!

Then go back to our `GET` endpoint and check the course again -- under `current_enr`, the value should now be 1.


### Sources
https://www.educative.io/blog/python-fastapi-tutorial

https://www.datacamp.com/tutorial/introduction-fastapi-tutorial

https://www.youtube.com/watch?v=-ykeT6kk4bk 

https://fastapi.tiangolo.com/
