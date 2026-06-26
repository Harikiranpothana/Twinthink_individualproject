function sendMessage() {
  const input = document.getElementById("userInput");
  const chatBox = document.getElementById("chatBox");

  const message = input.value.trim();
  if (!message) return;

  // USER MESSAGE
  const userDiv = document.createElement("div");
  userDiv.className = "user-msg";
  userDiv.innerText = message;
  chatBox.appendChild(userDiv);

  // BOT TYPING EFFECT
  const botDiv = document.createElement("div");
  botDiv.className = "bot-msg";
  botDiv.innerText = "Thinking...";

  chatBox.appendChild(botDiv);

  // AUTO SCROLL
  chatBox.scrollTop = chatBox.scrollHeight;

  input.value = "";

  // SIMULATED RESPONSE (replace later with Flask + RAG)
  setTimeout(() => {
    botDiv.innerText =
      "This is a placeholder response. Your RAG backend will generate real answers here.";
    chatBox.scrollTop = chatBox.scrollHeight;
  }, 800);
}