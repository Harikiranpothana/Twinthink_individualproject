// =============================
// TwinThink Chat System
// =============================

console.log("Chat JS Loaded Successfully");

// Detect page refresh
window.addEventListener("beforeunload", () => {
    console.log("PAGE IS RELOADING");
});


// ======================================
// LOAD OLD CHAT HISTORY FROM DATABASE
// ======================================
window.onload = async function () {

    const chatBox = document.getElementById("chatBox");

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/chat-history"
        );

        const data = await response.json();

        console.log("Chat History:", data);

        if (
            data.status === "success" &&
            data.history.length > 0
        ) {

            // Remove default welcome message
            chatBox.innerHTML = "";

            data.history.forEach(chat => {

                // User message
                const userDiv = document.createElement("div");
                userDiv.className = "user-msg";
                userDiv.innerText = chat.question;

                chatBox.appendChild(userDiv);

                // Bot message
                const botDiv = document.createElement("div");
                botDiv.className = "bot-msg";
                botDiv.innerText = chat.answer;

                chatBox.appendChild(botDiv);
            });

            chatBox.scrollTop = chatBox.scrollHeight;
        }

    } catch (error) {

        console.error(
            "Unable to load chat history:",
            error
        );
    }
};


// =============================
// SEND MESSAGE FUNCTION
// =============================
async function sendMessage() {

    console.log("Send button clicked");

    const input = document.getElementById("userInput");
    const chatBox = document.getElementById("chatBox");

    const message = input.value.trim();

    if (!message) return;

    // -------------------------
    // USER MESSAGE
    // -------------------------
    const userDiv = document.createElement("div");
    userDiv.className = "user-msg";
    userDiv.innerText = message;

    chatBox.appendChild(userDiv);

    // Clear input
    input.value = "";

    // -------------------------
    // BOT THINKING MESSAGE
    // -------------------------
    const botDiv = document.createElement("div");
    botDiv.className = "bot-msg";
    botDiv.innerText = "Thinking...";

    chatBox.appendChild(botDiv);

    chatBox.scrollTop = chatBox.scrollHeight;

    try {

        // Send question to backend
        const response = await fetch(
            "http://127.0.0.1:5000/ask",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    question: message
                })
            }
        );

        const data = await response.json();

        console.log("Backend Response:", data);

        // Display answer
        if (data.status === "success") {

            botDiv.innerText =
                data.answer || "No answer available.";

        } else {

            botDiv.innerText =
                data.message || "Something went wrong.";
        }

    } catch (error) {

        console.error("Error:", error);

        botDiv.innerText =
            "Unable to connect to TwinThink backend.";
    }

    chatBox.scrollTop = chatBox.scrollHeight;
}


// =============================
// ENTER KEY SUPPORT
// =============================
document
    .getElementById("userInput")
    .addEventListener("keydown", function (event) {

        if (event.key === "Enter") {

            event.preventDefault();
            sendMessage();
        }

    });