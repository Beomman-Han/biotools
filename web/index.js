// Get submit button object
const submit_btn = document.querySelector(".content #submit");

// Event handler for click at SUBMIT button
function submit() {
    const input = document.querySelector(".content textarea");
    console.log(input.value);
}

// Add event handler
submit_btn.addEventListener('click', submit);
