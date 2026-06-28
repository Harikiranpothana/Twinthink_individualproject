// =============================
// TwinThink Login System
// =============================

const form = document.querySelector("form");

if (form) {

    form.addEventListener("submit", async function (event) {

        event.preventDefault();

        const email = document
            .querySelector('input[type="email"]')
            .value
            .trim();

        const password = document
            .querySelector('input[type="password"]')
            .value
            .trim();

        if (!email || !password) {
            alert("Please fill in all fields.");
            return;
        }

        try {

            const response = await fetch(
                "http://127.0.0.1:5000/login",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        email: email,
                        password: password
                    })
                }
            );

            const data = await response.json();

            if (data.status === "success") {

                // Save login session
                localStorage.setItem(
                    "isLoggedIn",
                    "true"
                );

                localStorage.setItem(
                    "user",
                    JSON.stringify(data.user)
                );

                // Button feedback
                const btn = form.querySelector("button");

                if (btn) {
                    btn.innerText = "Redirecting...";
                    btn.disabled = true;
                }

                // Redirect to dashboard
                setTimeout(() => {

                    window.location.href =
                        "../dashboard/dashboard.html";

                }, 500);

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