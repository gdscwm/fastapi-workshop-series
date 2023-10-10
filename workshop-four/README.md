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
    <h2>Course Registration</h2>
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
    <h2>Course Registration</h2>
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
Note that we included a checkbox on our page, but it doesn't actually do anything yet because we haven't specified an `onclick` function.

So how do we actually get data on courses from our FastAPI "database"?

We first need to make sure our FastAPI server is actually running!
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

Now, when you reload your webpage, you should see all courses displayed!
