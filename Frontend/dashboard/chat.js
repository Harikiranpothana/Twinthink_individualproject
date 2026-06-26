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

  // BOT RESPONSE (DUMMY FOR NOW)
  const botDiv = document.createElement("div");
  botDiv.className = "bot-msg";
  botDiv.innerText = "Thinking... (RAG response will come here later)";
  
  chatBox.appendChild(botDiv);

  input.value = "";

  chatBox.scrollTop = chatBox.scrollHeight;
}