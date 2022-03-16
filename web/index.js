// Get 'SUBMIT' button object
const submit_btn = document.querySelector(".content #submit");

// Event handler for click at SUBMIT button
function submit() {
    const input = document.querySelector(".content textarea");
    console.log(input.value);
}
// Add event handler
submit_btn.addEventListener('click', submit);

// Get 'CLEAR' button object
const clear_btn = document.querySelector(".content #clear");

// Event handler
function clear() {
    const input = document.querySelector(".content textarea");
    input.value = "";
}
// Add event handler
clear_btn.addEventListener('click', clear);