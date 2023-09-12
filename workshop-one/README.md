# Workshop One: Hello, world!
## What is an API?
An API (Application Programming Interface) allows different applications to talk to each other. Think of an API like a waiter in a restaurant: the waiter takes your order,
sends it to the kitchen, waits for the kitchen to make your order, then the waiter brings it back to you.
In the same way, an API takes a request from an application and sends it to a server. The server then processes the request and sents the data back to the application. 
Now that the API has done its job, the application can interpret the data and present it to the user. 

## What is FastAPI?
TODO

## Let's make an API!
### Setup
1. Open up your command line (if you're using Mac/Linux, this will be Terminal, if you're on Windows, use Powershell) and enter the following commands:

TODO FINISH SETUP

pip install fastapi
pip install uvicorn
If that doesn’t work, try these for both fastapi and uvicorn:
pip3 install fastapi
python -m pip install fastapi
python3 -m pip install fastapi
If it still doesn’t work, raise your hand and someone will come help you
Open up your favorite IDE (place to write code)
If you don’t have one, VSCode is free
Create a new file main.py
If you’re using VSCode, install the Python package

### Hello, world!
In your main.py, copy this code:
```
from fastapi import FastAPI     # note the capitalization!

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello world"}
```
Now in your terminal, run this command:
```
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
- **GET**: read data (aka user input)
- **POST**: create data
- **PUT**: update data
- **DELETE**: delete data


#### A quick note on JSON
In our function above, we return a Python dictionary. (Python dictionaries are used to store data as key/value pairs, written as {key:value}. If you access a key in a dictionary, it returns its value.)
This dictionary is automatically converted by FastAPI into JSON. JSON is the standard way to send and receive information from an endpoint, because it makes the information easy to understand and access,
as we'll see later in this workshop.

### TODO TITLE OF SECTION FOR GETTING INTO THE SERIES
TODO ADD CODE
#### Path parameters
TODO DEFINE



### Sources
https://www.educative.io/blog/python-fastapi-tutorial

https://www.datacamp.com/tutorial/introduction-fastapi-tutorial

https://www.youtube.com/watch?v=-ykeT6kk4bk

https://fastapi.tiangolo.com/
