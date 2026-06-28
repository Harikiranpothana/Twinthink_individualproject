let memoryView;
let timelineView;

let memories = [];

/* ====================================
   INIT SAFE CONTAINERS
==================================== */
document.addEventListener("DOMContentLoaded", () => {

    memoryView = document.querySelector(".memory-view");
    timelineView = document.getElementById("timeline");

    if (!memoryView || !timelineView) {
        console.error("❌ Missing .memory-view or #timeline in HTML");
        return;
    }

    loadMemories();

    const searchInput = document.getElementById("searchInput");

    if (searchInput) {
        searchInput.addEventListener("input", (e) => {
            searchMemory(e.target.value);
        });
    }
});


/* ====================================
   LOAD FROM BACKEND
==================================== */
async function loadMemories() {

    try {

        const response = await fetch("http://127.0.0.1:5000/memory-timeline");

        if (!response.ok) {
            throw new Error("Failed to fetch timeline");
        }

        const data = await response.json();

        const timeline = data.timeline || [];

        // clear UI
        memoryView.innerHTML = "";
        timelineView.innerHTML = "<h3>Memory Timeline</h3>";

        if (timeline.length === 0) {
            memoryView.innerHTML = `
                <div class="memory-card">
                    <h3>No Memories Found</h3>
                    <p>No memory timeline available yet.</p>
                </div>
            `;
            return;
        }

        memories = timeline.map((item, index) => ({
            id: index + 1,
            title: item.event_type || "Memory",
            content: item.event_text || "No content available",
            time: item.timestamp || "Unknown time"
        }));

        renderUI(memories);

    } catch (error) {

        console.error("Unable to load memories:", error);

        memoryView.innerHTML = `
            <div class="memory-card">
                <h3>Error</h3>
                <p>Unable to connect to backend.</p>
            </div>
        `;
    }
}


/* ====================================
   RENDER BOTH SIDES
==================================== */
function renderUI(data) {

    memoryView.innerHTML = "";
    timelineView.innerHTML = "<h3>Memory Timeline</h3>";

    data.forEach(mem => {

        // LEFT TIMELINE
        const t = document.createElement("div");
        t.className = "item";
        t.innerHTML = `
            <span>${mem.title}</span>
            <p>${mem.content}</p>
        `;
        timelineView.appendChild(t);

        // CENTER MEMORY CARD
        const card = document.createElement("div");
        card.className = "memory-card";
        card.innerHTML = `
            <h3>${mem.title}</h3>
            <p>${mem.content}</p>
            <small>${mem.time}</small>
        `;

        memoryView.appendChild(card);
    });
}


/* ====================================
   SEARCH MEMORY
==================================== */
function searchMemory(query = "") {

    const q = query.toLowerCase().trim();

    const filtered = memories.filter(mem =>
        (mem.title || "").toLowerCase().includes(q) ||
        (mem.content || "").toLowerCase().includes(q)
    );

    renderUI(filtered);
}


/* ====================================
   WHAT HAVE I FORGOTTEN?
==================================== */
function showForgotten() {

    if (!memories.length) {
        alert("No memories available.");
        return;
    }

    const forgotten =
        memories[Math.floor(Math.random() * memories.length)];

    alert(
        `⚠ TwinThink Insight:\n\nYou may want to revisit:\n${forgotten.content}`
    );
}