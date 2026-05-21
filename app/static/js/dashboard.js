/**
 * Sentilytics — Dashboard JavaScript
 * Handles Chart.js initialization and interactive features.
 */

// ==========================================
// Chart: Actual vs Predicted
// ==========================================
function initActualVsPredChart(data) {
    const ctx = document.getElementById('actualVsPredChart');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.dates,
            datasets: [
                {
                    label: 'Actual Close',
                    data: data.actual,
                    borderColor: '#4361ee',
                    backgroundColor: 'rgba(67,97,238,0.06)',
                    fill: true,
                    tension: 0.3,
                    pointRadius: 1.5,
                    pointHoverRadius: 5,
                    borderWidth: 2.5,
                    order: 1,
                },
                {
                    label: 'Predicted Close',
                    data: data.predicted,
                    borderColor: '#fd7e14',
                    backgroundColor: 'transparent',
                    fill: false,
                    tension: 0.3,
                    pointRadius: 1.5,
                    pointHoverRadius: 5,
                    borderWidth: 2.5,
                    borderDash: [5, 3],
                    order: 0,
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 16,
                        font: { size: 12, family: "'Inter', sans-serif" }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(30,41,59,0.95)',
                    titleFont: { size: 12 },
                    bodyFont: { size: 12 },
                    padding: 12,
                    cornerRadius: 8,
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ': Rp ' +
                                   context.parsed.y.toLocaleString('id-ID', {maximumFractionDigits: 0});
                        }
                    }
                }
            },
            scales: {
                y: {
                    grid: { color: 'rgba(0,0,0,0.04)' },
                    ticks: {
                        callback: function(value) {
                            return 'Rp ' + value.toLocaleString('id-ID');
                        },
                        font: { size: 11 }
                    }
                },
                x: {
                    grid: { display: false },
                    ticks: {
                        maxTicksLimit: 12,
                        font: { size: 11 }
                    }
                }
            }
        }
    });
}

// ==========================================
// Chart: Forecast H+7
// ==========================================
function initForecastChart(data) {
    const ctx = document.getElementById('forecastChart');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.steps,
            datasets: [{
                label: 'Forecast Close',
                data: data.predicted,
                borderColor: '#7b2ff7',
                backgroundColor: 'rgba(123,47,247,0.08)',
                fill: true,
                tension: 0.3,
                pointRadius: 6,
                pointBackgroundColor: '#7b2ff7',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                borderWidth: 3,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 16,
                        font: { size: 12, family: "'Inter', sans-serif" }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(30,41,59,0.95)',
                    padding: 12,
                    cornerRadius: 8,
                    callbacks: {
                        label: function(context) {
                            return 'Predicted: Rp ' +
                                   context.parsed.y.toLocaleString('id-ID', {maximumFractionDigits: 0});
                        }
                    }
                }
            },
            scales: {
                y: {
                    grid: { color: 'rgba(0,0,0,0.04)' },
                    ticks: {
                        callback: function(value) {
                            return 'Rp ' + value.toLocaleString('id-ID');
                        },
                        font: { size: 11 }
                    }
                },
                x: {
                    grid: { display: false },
                    ticks: { font: { size: 11 } }
                }
            }
        }
    });
}
