// =========================
// TwinThink Settings Engine
// =========================

// Get elements
const saveBtn = document.querySelector(".save-btn");
const selects = document.querySelectorAll("select");

// Status box (right panel)
const statusBox = document.querySelector(".status-box");

// =========================
// LOAD SAVED SETTINGS
// =========================
window.addEventListener("load", () => {
  selects.forEach((select) => {
    const savedValue = localStorage.getItem(select.previousElementSibling.innerText);
    if (savedValue) {
      select.value = savedValue;
    }
  });

  updateStatus("Settings Loaded");
});

// =========================
// SAVE SETTINGS
// =========================
if (saveBtn) {
  saveBtn.addEventListener("click", () => {
    selects.forEach((select) => {
      const key = select.previousElementSibling.innerText;
      const value = select.value;

      localStorage.setItem(key, value);
    });

    updateStatus("Configuration Saved ✔");
    flashButton();
  });
}

// =========================
// STATUS UPDATE FUNCTION
// =========================
function updateStatus(message) {
  if (!statusBox) return;

  const statusLine = document.createElement("p");
  statusLine.textContent = `⚡ ${message}`;

  statusBox.appendChild(statusLine);

  // keep only last 4 logs
  const logs = statusBox.querySelectorAll("p");
  if (logs.length > 4) {
    logs[0].remove();
  }
}

// =========================
// BUTTON ANIMATION FEEDBACK
// =========================
function flashButton() {
  saveBtn.innerText = "Saved ✔";

  setTimeout(() => {
    saveBtn.innerText = "Save Configuration";
  }, 1500);
}

// =========================
// OPTIONAL: LIVE DETECTION
// =========================
selects.forEach((select) => {
  select.addEventListener("change", () => {
    updateStatus(`${select.previousElementSibling.innerText} changed`);
  });
});