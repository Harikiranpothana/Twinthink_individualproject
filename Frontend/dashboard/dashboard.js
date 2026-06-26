document.addEventListener("DOMContentLoaded", function () {

  const ctx = document.getElementById("chart");

  if (!ctx) {
    console.error("❌ Canvas with id 'chart' not found!");
    return;
  }

  new Chart(ctx, {
    type: "line",
    data: {
      labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
      datasets: [{
        label: "Questions Asked",
        data: [12, 19, 10, 15, 22, 18, 25],
        borderColor: "#06B6D4",
        backgroundColor: "rgba(6, 182, 212, 0.2)",
        tension: 0.4,
        fill: true
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          labels: {
            color: "#ffffff"
          }
        }
      },
      scales: {
        x: {
          ticks: { color: "#ffffff" }
        },
        y: {
          ticks: { color: "#ffffff" }
        }
      }
    }
  });

});