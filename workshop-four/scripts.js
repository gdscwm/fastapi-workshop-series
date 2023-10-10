// List of all courses
const courses = [];

// List of courses the user is enrolled in
const enrolledCourses = [];

// Holds error message for any issues with enrolling
let enrollmentError = " ";

// If only open classes are being displayed
let onlyOpen = false;

// Runs when the document successfully loads
document.addEventListener("DOMContentLoaded", async () => {
    // Make a request for which classes are currently open
    const response = await fetch("http://localhost:8000/list-courses");
    const data = await response.json();

    // Take the courses returned by the endpoint and turn them into something we can actually use
    for (const [id, course] of Object.entries(data)) {
        courses.push({...course, id: id})
    }

    // Render the interface
    render();
})

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

// Toggle between displaying only open courses and all courses
function toggleVisibleCourses() {
    onlyOpen = !onlyOpen;

    // Re-render the interface
    render();
}

// Return a div element that nicely displays a class
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

// Re-render data
function render() {
    // Filter the course list to only display the courses the user has requested (either open or all)
    const filtered = courses.filter((course) =>
        !(onlyOpen && course.current_enr >= course.max_enr)
    )

    // Populate the select with courses the user has not already registered for
    const select = document.getElementById("class-select");
    // Reset the currently selected item
    select.selectedIndex = -1;
    // Clear the current contents of the select
    select.innerHTML = " ";

    // List all courses that the user has
    const open = filtered.filter((course) => !enrolledCourses.includes(course));
    open.forEach((course) => {
        select.append(new Option(course.name, course.id))
    });

    // If there are no classes that can be registered for, disable the register button
    document.getElementById("register").disabled = open.length === 0;

    // Populate the course list with all the courses listed in the backend
    const list = document.getElementById("class-list");
    // Clear the current list before using append
    list.innerHTML = "";
    filtered.forEach((course) => {
        list.append(returnCourseDiv(course));
    })

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

    // Render the error text
    document.getElementById("error").innerText = enrollmentError;
}