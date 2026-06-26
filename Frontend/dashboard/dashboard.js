// TwinThink Dashboard Engine (STABLE FINAL VERSION)

document.addEventListener("DOMContentLoaded", function () {

  // ================= LOGIN CHECK =================
  const isLoggedIn = localStorage.getItem("isLoggedIn");

  if (isLoggedIn !== "true") {
    window.location.href = "../homepage/login.html";
    return;
  }

  // ================= CHART INIT =================
  const canvas = document.getElementById("chart");

  if (!canvas) {
    console.error("Chart canvas not found");
    return;
  }

  const ctx = canvas.getContext("2d");

  // IMPORTANT FIX: destroy if reloaded
  if (window.dashboardChart) {
    window.dashboardChart.destroy();
  }

  window.dashboardChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
      datasets: [{
        label: "Questions Asked",
        data: [12, 19, 10, 15, 22, 18, 25],
        borderColor: "#06B6D4",
        backgroundColor: "rgba(6, 182, 212, 0.2)",
        borderWidth: 2,
        pointRadius: 4,
        tension: 0.4,
        fill: true
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
          ticks: { color: "#ffffff" },
          grid: { color: "rgba(255,255,255,0.08)" }
        },
        y: {
          ticks: { color: "#ffffff" },
          grid: { color: "rgba(255,255,255,0.08)" }
        }
      }
    }
  });

});