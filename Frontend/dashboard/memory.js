const memoryView = document.querySelector(".memory-view");

let memories = [
  {
    id: 1,
    title: "RAG Explanation",
    content: "Retrieval Augmented Generation combines search + LLM reasoning..."
  },
  {
    id: 2,
    title: "Transformer Basics",
    content: "Self-attention mechanism allows context-based token learning..."
  },
  {
    id: 3,
    title: "AI Notes Summary",
    content: "Key concepts from uploaded PDF extracted and stored..."
  }
];

/* =========================
   RENDER ENGINE (OPTIMIZED)
========================= */
function renderMemories(data) {
  // clear previous safely
  const existing = document.querySelectorAll(".memory-card");
  existing.forEach(el => el.remove());

  // empty state handling
  if (data.length === 0) {
    const empty = document.createElement("div");
    empty.className = "memory-card";
    empty.innerHTML = `<h3>No Memories Found</h3><p>Try a different search.</p>`;
    memoryView.appendChild(empty);
    return;
  }

  // render cards
  data.forEach(mem => {
    const card = document.createElement("div");
    card.className = "memory-card";

    card.innerHTML = `
      <h3>${mem.title}</h3>
      <p>${mem.content}</p>
    `;

    memoryView.appendChild(card);
  });
}

/* =========================
   SEARCH ENGINE (REAL-TIME READY)
========================= */
function searchMemory(query = "") {
  const q = query.toLowerCase().trim();

  const filtered = memories.filter(mem =>
    mem.title.toLowerCase().includes(q) ||
    mem.content.toLowerCase().includes(q)
  );

  renderMemories(filtered);
}

/* =========================
   ADD MEMORY (BACKEND READY)
========================= */
function addMemory(title, content) {
  const newMemory = {
    id: Date.now(),
    title,
    content
  };

  memories.unshift(newMemory);
  renderMemories(memories);

  // 🔥 Backend hook (Flask / RAG ready)
  /*
  fetch("/add-memory", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(newMemory)
  });
  */
}

/* =========================
   AI "WHAT YOU FORGOT"
========================= */
function showForgotten() {
  const forgotten = memories[Math.floor(Math.random() * memories.length)];

  alert(`⚠ AI Insight:
You may need to revise: ${forgotten.title}`);
}

/* =========================
   LIVE SEARCH INPUT (IMPORTANT)
========================= */
document.addEventListener("DOMContentLoaded", () => {
  renderMemories(memories);

  const searchInput = document.getElementById("searchInput");

  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      searchMemory(e.target.value);
    });
  }
});