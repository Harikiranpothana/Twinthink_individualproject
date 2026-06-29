// =======================================
// TwinThink Dashboard Engine
// =======================================

document.addEventListener("DOMContentLoaded", () => {

    // =======================================
    // LOGIN CHECK
    // =======================================
    const isLoggedIn = localStorage.getItem("isLoggedIn");

    if (isLoggedIn !== "true") {
        window.location.href = "../homepage/login.html";
        return;
    }

    // Load everything
    loadDashboardStats();
    loadActivityFeed();
});


// =======================================
// LOAD DASHBOARD STATISTICS
// =======================================
async function loadDashboardStats() {

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/dashboard"
        );

        const data = await response.json();

        console.log("Dashboard Data:", data);

        if (data.status === "success") {

            document.getElementById("totalDocs").innerText =
                data.stats.total_documents || 0;

            document.getElementById("totalQueries").innerText =
                data.stats.total_queries || 0;

            document.getElementById("totalChats").innerText =
                data.stats.total_chats || 0;

            document.getElementById("totalUsers").innerText =
                data.stats.total_users || 0;


            // Build chart
            createChart(
                data.stats.total_documents,
                data.stats.total_queries,
                data.stats.total_chats,
                data.stats.total_users
            );
        }

    }

    catch (error) {

        console.error("Dashboard Error:", error);
    }
}


// =======================================
// LOAD RECENT ACTIVITIES
// =======================================
async function loadActivityFeed() {

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/memory-timeline"
        );

        const data = await response.json();

        const activityFeed =
            document.getElementById("activityFeed");

        const forgottenList =
            document.getElementById("forgottenList");

        activityFeed.innerHTML = "";
        forgottenList.innerHTML = "";

        if (!data.timeline || data.timeline.length === 0) {

            activityFeed.innerHTML =
                "<li>No activity found.</li>";

            forgottenList.innerHTML =
                "<li>No memories available.</li>";

            return;
        }

        // Show latest 5 activities
        const recent = data.timeline.slice(0, 5);

        recent.forEach(item => {

            const li = document.createElement("li");

            li.innerText = item.event_text;

            activityFeed.appendChild(li);
        });

        // Show random forgotten memories
        const forgotten =
            data.timeline.slice(0, 3);

        forgotten.forEach(item => {

            const li = document.createElement("li");

            li.innerText = item.event_text;

            forgottenList.appendChild(li);
        });

    }

    catch (error) {

        console.error(
            "Activity Feed Error:",
            error
        );
    }
}


// =======================================
// CREATE ANALYTICS CHART
// =======================================
function createChart(
    documents,
    queries,
    chats,
    users
) {

    const canvas =
        document.getElementById("chart");

    if (!canvas) return;

    const ctx = canvas.getContext("2d");

    // Destroy previous chart if exists
    if (window.dashboardChart) {

        window.dashboardChart.destroy();
    }

    window.dashboardChart = new Chart(ctx, {

        type: "bar",

        data: {

            labels: [
                "Documents",
                "Queries",
                "Chats",
                "Users"
            ],

            datasets: [{
                label: "TwinThink Analytics",

                data: [
                    documents,
                    queries,
                    chats,
                    users
                ],

                backgroundColor: [
                    "#06B6D4",
                    "#8B5CF6",
                    "#10B981",
                    "#F59E0B"
                ],

                borderWidth: 1
            }]
        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {
                    labels: {
                        color: "#ffffff"
                    }
                }
            },

            scales: {

                x: {

                    ticks: {
                        color: "#ffffff"
                    },

                    grid: {
                        color: "rgba(255,255,255,0.08)"
                    }
                },

                y: {

                    beginAtZero: true,

                    ticks: {
                        color: "#ffffff"
                    },

                    grid: {
                        color: "rgba(255,255,255,0.08)"
                    }
                }
            }
        }
    });
}