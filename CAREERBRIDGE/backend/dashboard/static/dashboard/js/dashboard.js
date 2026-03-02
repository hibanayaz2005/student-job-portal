document.addEventListener('DOMContentLoaded', function () {
  function initChart(canvasId, type, bgColors) {
    const el = document.getElementById(canvasId);
    if (!el) return;
    const labels = JSON.parse(el.getAttribute('data-labels') || '[]');
    const values = JSON.parse(el.getAttribute('data-values') || '[]');

    new Chart(el, {
      type: type,
      data: {
        labels: labels,
        datasets: [{
          data: values,
          backgroundColor: bgColors || ['#2563eb', '#06b6d4', '#f97316', '#10b981'],
          borderWidth: 0
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { position: 'bottom' } }
      }
    });
  }

  initChart('rolesChart', 'doughnut');
  initChart('jobsChart', 'bar', ['#4f46e5', '#06b6d4', '#f43f5e']);
});
