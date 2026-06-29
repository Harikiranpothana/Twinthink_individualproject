// ====================================
// TwinThink Memory System
// ====================================

let memoryView;
let timelineView;

let memories = [];


// ====================================
// INITIALIZE PAGE
// ====================================
document.addEventListener("DOMContentLoaded", () => {

    console.log("Memory JS Loaded Successfully");

    memoryView = document.querySelector(".memory-view");
    timelineView = document.getElementById("timeline");

    if (!memoryView || !timelineView) {

        console.error("❌ Missing .memory-view or #timeline in HTML");
        return;
    }

    loadMemories();
});


// ====================================
// LOAD MEMORIES FROM BACKEND
// ====================================
async function loadMemories() {

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/memory-timeline"
        );

        if (!response.ok) {
            throw new Error("Failed to fetch memories");
        }

        const data = await response.json();

        console.log("Memory API Response:", data);

        const timeline = data.timeline || [];

        // IMPORTANT FIX
        memories = timeline.map((item, index) => ({

            id: index + 1,

            title:
                item.event_type
                    ? item.event_type.toUpperCase()
                    : "MEMORY",

            content:
                item.event_text || "No content available",

            time:
                item.timestamp
                    ? new Date(item.timestamp).toLocaleString()
                    : "Unknown time"

        }));

        renderUI(memories);

    }

    catch (error) {

        console.error("Unable to load memories:", error);

        memoryView.innerHTML = `
            <div class="memory-card">
                <h3>Error</h3>
                <p>Unable to connect to backend.</p>
            </div>
        `;
    }
}


// ====================================
// RENDER TIMELINE + MEMORY CARDS
// ====================================
function renderUI(data) {

    // Reset Timeline
    timelineView.innerHTML = `
        <h3>Memory Timeline</h3>
    `;

    // Reset Center Panel
    memoryView.innerHTML = `
        <div class="search-box">
            <input
                type="text"
                id="searchInput"
                placeholder="Search memories..."
            >
        </div>

        <h2>Stored Memories</h2>
    `;

    // Reattach Search Listener
    const searchInput =
        memoryView.querySelector("#searchInput");

    if (searchInput) {

        searchInput.addEventListener("input", (e) => {

            searchMemory(e.target.value);

        });
    }

    // Empty State
    if (data.length === 0) {

        memoryView.innerHTML += `
            <div class="memory-card">
                <h3>No Memories Found</h3>
                <p>No memories available.</p>
            </div>
        `;

        return;
    }

    // Render Memories
    data.forEach(mem => {

        // LEFT TIMELINE
        const timelineItem =
            document.createElement("div");

        timelineItem.className = "item";

        timelineItem.innerHTML = `
            <span>${mem.time}</span>
            <p>${mem.content}</p>
        `;

        timelineView.appendChild(timelineItem);

        // CENTER MEMORY CARD
        const card =
            document.createElement("div");

        card.className = "memory-card";

        card.innerHTML = `
            <h3>${mem.title}</h3>
            <p>${mem.content}</p>
            <small>${mem.time}</small>
        `;

        memoryView.appendChild(card);

    });
}


// ====================================
// SEARCH MEMORY
// ====================================
function searchMemory(query = "") {

    const q = query.toLowerCase().trim();

    const filtered = memories.filter(mem =>

        mem.title.toLowerCase().includes(q) ||

        mem.content.toLowerCase().includes(q)

    );

    renderUI(filtered);
}


// ====================================
// ADD MEMORY
// ====================================
function addMemory() {

    alert(
        "Feature coming soon: Add custom memories."
    );
}


// ====================================
// SUMMARIZE ALL
// ====================================
function summarizeAll() {

    alert(
        `TwinThink Summary:\n\nTotal Memories: ${memories.length}`
    );
}


// ====================================
// WHAT HAVE I FORGOTTEN
// ====================================
function whatForgot() {

    if (memories.length === 0) {

        alert("No memories available.");
        return;
    }

    const forgotten =
        memories[
            Math.floor(
                Math.random() * memories.length
            )
        ];

    alert(
        `⚠ TwinThink Insight:\n\nYou may want to revisit:\n\n${forgotten.content}`
    );
}