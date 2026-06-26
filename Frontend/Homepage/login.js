// Select the login form
const form = document.querySelector("form");

form.addEventListener("submit", function(event) {

    // Prevent page refresh
    event.preventDefault();

    // Get input values
    const email = document.querySelector('input[type="email"]').value.trim();
    const password = document.querySelector('input[type="password"]').value.trim();

    // Basic validation
    if (email === "" || password === "") {
        alert("Please fill in all fields.");
        return;
    }

    // Temporary success message
    alert("Login Successful!");

    // Future: Redirect to dashboard
    // window.location.href = "dashboard.html";
});