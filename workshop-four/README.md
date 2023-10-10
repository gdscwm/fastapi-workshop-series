# Workshop 4: 

In case you missed the first workshop, look
[here](https://github.com/gdscwm/fastapi-workshop-series/tree/main/workshop-one#setup)
for setup instructions to get FastAPI up and running.

## What is a frontend?
The frontend is what the user interacts with! This includes
* The user interface (UI)
* The page layout
* Styling/coloration
* Frontend functionality (e.g. what happens when you click a button)

## What tools are used to build frontends?
There are many frameworks for building frontends, like Angular and React. 
For this tutorial, we'll avoid installations and stick to the basics.
* HTML
* CSS
* JavaScript

## Creating the frontend
1. Create a new file in your `fastapi-workshop-series` directory, called `frontend.html`. Depending on your IDE, it might generate some sample HTML code for you. Just so we all have the same starting point, begin with the code below in your HTML file.
```angular2html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Course Registration</title>
</head>
<body>

</body>
</html>
```
2. Now we have a bare bones webpage, but nothing in the `<body>`, so nothing will actually show up when we open it. Lets add a simple title to the page:
```angular2html
<div>
    <div id="register">
        <h2>Course Registration</h2>
    </div>
</div>
```
3. Open the webpage in your browser. Again, your IDE may offer to do it for you, but if not, from your terminal you can run 
```
open frontend.html
```
You should now see a very simple web page titled `Course Registration` in your web browser!

## Styling the frontend
Now we'll add a bit of styling using CSS. 
1. Create a new file `frontend.css` and add a link to it in `frontend.html`, such that your `<head>` section looks like this:
```angular2html
<head>
    <meta charset="UTF-8">
    <title>Course Registration</title>
    <link rel="stylesheet" type="text/css" href="frontend.css"/>
</head>
```
2. Add the following code to `frontend.css` to style our page title a bit!
```css
body {
    font-family: sans-serif;
    padding: 1rem 2rem;
    display: flex;
    gap: 4rem;
}

body > div {
flex-basis: 50%;
}

h2 {
    font-weight: bold;
    font-size: 2em;
}
```
Now when you reload the webpage, you should see some changes, like a different font and font size!

Now that we've got a basic webpage and styling, let's add some more components!

## Adding a frontend component
To add frontend components, we need to go back to our HTML file. This page will simulate registering for courses, so we want to add some features that allow users to do just that!
1. One tool that might be useful would be a list of all the courses in our course list. Let's add a placeholder for our courses by including another `<div>` below our `Course Registration` div. Add the code below so the `<body>` section now looks like:
```angular2html
<div>
    <div id="register">
        <h2>Course Registration</h2>
    </div>
</div>

<div>
    <h2>All Courses</h2>
    <label>
        Display only open courses?
        <input type="checkbox" onclick=""/>
    </label>
    <div class="class-list" id="class-list"></div>
</div>
```

2. Let's add some spacing to our class-list as well -- add the following code to your CSS file:
```css
.class-list {
    padding: 1rem 0;
}

.class-list > div {
    margin-bottom: 2rem;
}
```
Note that we included a checkbox on our page, but it doesn't actually do anything yet because we haven't specified an `onclick` function.

So how do we actually get data on courses from our FastAPI "database"?

We first need to make sure our FastAPI server is actually running, and ready to accept requests from our webpage!
In your `main.py`, add the following import:
```python
from starlette.middleware.cors import CORSMiddleware
```

And the following code block: 
```python
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])
```

This will allow our python database to accept requests!


With your virtual environment activated, run `uvicorn main:app --reload` to start the FastAPI server. You should be able to see the endpoints we've written in the past three workshops at [localhost:8000/docs](localhost:8000/docs).


## Getting data from our endpoints
With our database up and running, we now want our HTML frontend to be able to get data from our Python backend. For that, we use JavaScript!
1. In `fastapi-workshop-series`, create a new file `scripts.js` and add the following code:
```javascript
// List of all courses
const courses = [];

document.addEventListener("DOMContentLoaded", async () => {
    // Make a request for which classes are currently open
    const response = await fetch("http://localhost:8000/list-courses");
    const data = await response.json();

    // Take the courses returned by the endpoint and turn them into something we can actually use
    for (const [id, course] of Object.entries(data)) {
        courses.push({...course, id: id})
    }
    
    render();
})
```
This creates a list `courses` to hold the information on all courses. Then, we send a get request to _our_ FastAPI endpoint `list-courses`, which we store in `courses`!
2. Now we have the data, we need some way to display it. First, let's add this function to nicely display information from a given course:
```javascript
function returnCourseDiv(course) {
    const entry = document.createElement("div");
    entry.append(Object.assign(document.createElement("h3"), {textContent: course.name}));
    entry.append(Object.assign(document.createElement("p"), {textContent: course.professor}));
    entry.append(Object.assign(document.createElement("p"),
        {
            textContent: `Currently registered: ${course.current_enr}/${course.max_enr} 
        ${course.current_enr < course.max_enr ? "" : "FULL"}`
        }));
    return entry;
}
```
3. Next, let's write a function that will call `returnCourseDiv` for each course we get from the database:
```javascript
function render() {

    // Populate the course list with all the courses listed in the backend
    const list = document.getElementById("class-list");
    // Clear the current list before using append
    list.innerHTML = "";
    courses.forEach((course) => {
        list.append(returnCourseDiv(course));
    })
}
```
4. Finally, we need to call `render();` at the end of our EventListener function where we first populate `courses`!
5. To make sure our HTML page can use the JavaScript functions, we need to include one line at the end of our HTML body:
```angular2html
<script src="scripts.js" defer></script>
```

Now, when you reload your webpage, you should see all courses displayed!

## Registering for a course
Now that we know all the courses we can choose from, what if we want to register for one?
1. First, we need to add some HTML components so users can register. Add the code below to the `register` `<div>`
```angular2html
<div class="form">
    <label for="class-select">
        Select class to register for:
    </label>
    <select id="class-select">
    </select>
    <button onclick="enroll()" id="register">Register</button>
</div>
<p id="error" class="error-text"></p>
```
2. You'll notice that our dropdown to register has no classes in it! We need to add some javascript pull the classes from the backend and inject them into our dropdown.
3. First, we need to define some variables to store our courses -- add the code below to the top of your JS file.
```javascript
// List of courses the user is enrolled in
const enrolledCourses = [];

// Holds error message for any issues with enrolling
let enrollmentError = " ";
```
4. Then, in our render function, we want to actually display the courses in our `<select>` HTML element. Add the code below to the `render` function:
```javascript
// Populate the select with courses the user has not already registered for
const select = document.getElementById("class-select");

// Reset the currently selected item
select.selectedIndex = -1;

// Clear the current contents of the select
select.innerHTML = " ";
```

Now, when we go to our webpage, our dropdown should be populated with the courses we see on the right!

But, when we click register, nothing happens! This is because we haven't defined a function `enroll`. We'll do that again with JavaScript.

5. Define a function `enroll` in `scripts.js` that contains the following code: 
```javascript
// Enroll in a course
async function enroll() {
    
    // Get the ID of the course the user wants to register in
    const courseId = document.getElementById("class-select").value;

    // Make a request to enroll in the class
    const response = await fetch(`http://localhost:8000/class/${courseId}/enroll`, {method: "PUT"});

    // Check that the request to enroll was successful
    if (response.ok) {
        // Reset the error message
        enrollmentError = "";

        const enrolled = courses.find((course) => course.id === courseId)
        // Increment the enrollment by 1 since the user just enrolled
        enrolled.current_enr += 1;

        // Add the course to the user's list of courses
        enrolledCourses.push(enrolled);
    } else {
        const error = await response.json();
        enrollmentError = error.detail;
    }

    // Re-render the interface
    render();
}
```

Now, when we click register on a course that isn't at capacity, we should see the number of students on the right increase by 1!

6. Finally, in our `enroll` function, we defined an error message `enrollmentError` for when we can't register for a class, but we're not displaying it anywhere. We have an html element with the id `error` where we could display it. Now, when we call render, we want to disaplay our error.
```javascript
    // Render the error text
    document.getElementById("error").innerText = enrollmentError;
```

Now, when we try and enroll in a class at capacity, we should see an error message saying we can't register!

7. Let's add some simple styling to that error message so it pops! Add the following to your CSS file:
```css
.error-text {
    color: red;
    white-space: pre;
    height: 1.5rem;
}
```

## Display a user's courses
Finally, the user may want to see the different classes that they've registered for. 
1. Once again, we'll need to add an HTML element to display this data. Add the following code _below_ the `register div`
```angular2html
<div>
    <h3>Currently Registered Classes</h3>
    <p>You are currently registered for <span id="registered">0</span> courses</p>
    <div class="class-list" id="registered-class-list"></div>
</div>
```

When you reload the webpage, you should see these new HTML elements appear. But, when we register for a course, we don't see any change in the HTML -- let's add some Javascript!
2. Add the following code to the `render` function so we populate the course the user has registered for each time the webpage loads:
```javascript
// Populate the list of registered courses
const registeredList = document.getElementById("registered-class-list");

// Remove any of the current options in the list
registeredList.innerHTML = "";

// Create an entry for every class the user is registered in
enrolledCourses.forEach((course) => {
    registeredList.append(returnCourseDiv(course));
})

// Update the number of enrolled courses to match the number of courses the user is in
document.getElementById("registered").innerText = enrolledCourses.length;

```

Now, when you register for a course, you should be able to see the number of courses increase, and a description of the course appear on the left hand side!
