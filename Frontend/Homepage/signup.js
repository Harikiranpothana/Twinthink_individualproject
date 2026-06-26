const form = document.getElementById("signupForm");

form.addEventListener("submit", function(event){

    event.preventDefault();

    const fullname = document.getElementById("fullname").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    if(fullname === "" || email === "" || password === "" || confirmPassword === ""){
        alert("Please fill all fields.");
        return;
    }

    if(password !== confirmPassword){
        alert("Passwords do not match.");
        return;
    }

    alert("Account created successfully!");

    // Future Flask Integration
    // window.location.href = "dashboard.html";
});