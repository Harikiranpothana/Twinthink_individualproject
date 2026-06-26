// 
// TwinThink Login System (Fixed)
// 

const form = document.querySelector("form");

form.addEventListener("submit", function (event) {
  event.preventDefault();

  const email = document.querySelector('input[type="email"]').value.trim();
  const password = document.querySelector('input[type="password"]').value.trim();

  if (!email || !password) {
    alert("Please fill in all fields.");
    return;
  }

  // TEMP AUTH (replace later with backend API)
  if (email === "email@example.com" && password === "1234") {

    // Save session
    localStorage.setItem("isLoggedIn", "true");
    localStorage.setItem("userEmail", email);

    // UI feedback (NON-blocking)
    const btn = form.querySelector("button");
    if (btn) {
      btn.innerText = "Redirecting...";
      btn.disabled = true;
    }

    // Smooth redirect
    setTimeout(() => {
      window.location.href = "../dashboard/dashboard.html";
    }, 400);

  } else {
    alert("Invalid credentials");
  }
});