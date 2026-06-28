// =============================
// TwinThink Signup System
// =============================

const form = document.querySelector("form");

if (form) {

    form.addEventListener("submit", async function (event) {

        event.preventDefault();

        const username = document
            .querySelector('input[type="text"]')
            .value
            .trim();

        const email = document
            .querySelector('input[type="email"]')
            .value
            .trim();

        const password = document
            .querySelectorAll('input[type="password"]')[0]
            .value
            .trim();

        const confirmPassword = document
            .querySelectorAll('input[type="password"]')[1]
            .value
            .trim();

        // Validation
        if (!username || !email || !password || !confirmPassword) {

            alert("Please fill in all fields.");
            return;
        }

        if (password !== confirmPassword) {

            alert("Passwords do not match.");
            return;
        }

        try {

            const response = await fetch(
                "http://127.0.0.1:5000/signup",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        username: username,
                        email: email,
                        password: password
                    })
                }
            );

            const data = await response.json();

            if (data.status === "success") {

                alert("Account created successfully!");

                // Redirect to Login Page
                window.location.href = "login.html";

            } else {

                alert(data.message);

            }

        } catch (error) {

            console.error(error);

            alert(
                "Unable to connect to server. Make sure backend is running."
            );

        }

    });

}