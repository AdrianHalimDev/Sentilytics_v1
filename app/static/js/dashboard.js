/**
 * Sentilytics — Dashboard JavaScript
 * Interactive charts with zoom/pan and train/test split annotation.
 *
 * Controls:
 *   🖱️ Scroll       → Zoom in/out (x-axis)
 *   🖱️ Drag         → Pan left/right
 *   Double-click    → Reset zoom
 *   ↺ Button        → Reset zoom
 */

// Chart instances (stored for reset)
let actualVsPredChartInstance = null;
let forecastChartInstance = null;

// ==========================================
// Shared zoom/pan plugin config
// ==========================================
function makeZoomConfig(resetBtnId) {
    return {
        pan: { enabled: true, mode: 'x', threshold: 5 },
        zoom: {
            wheel: { enabled: true },
            pinch: { enabled: true },
            mode: 'x',
            onZoomComplete({ chart }) {
                const btn = document.getElementById(resetBtnId);
                if (btn) btn.style.display = 'inline-flex';
            }
        },
        limits: { x: { minRange: 5 } }
    };
}

// ==========================================
// Chart: Actual vs Predicted (Full Range)
// ==========================================
function initActualVsPredChart(data) {
    const ctx = document.getElementById('actualVsPredChart');
    if (!ctx) return;

    // Build annotation for train/test split line
    const annotations = {};
    if (data.split_index != null && data.split_date) {
        annotations.splitLine = {
            type: 'line',
            xMin: data.split_index,
            xMax: data.split_index,
            borderColor: 'rgba(220, 53, 69, 0.7)',
            borderWidth: 2,
            borderDash: [6, 4],
            label: {
                display: true,
                content: '← Train | Test →',
                position: 'start',
                backgroundColor: 'rgba(220,53,69,0.85)',
                color: '#fff',
                font: { size: 11, weight: 'bold' },
                padding: { x: 8, y: 4 },
                borderRadius: 4,
            }
        };
    }

    actualVsPredChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.dates,
            datasets: [
                {
                    label: 'Actual Close (Historis)',
                    data: data.actual,
                    borderColor: '#4361ee',
                    backgroundColor: 'rgba(67,97,238,0.05)',
                    fill: true,
                    tension: 0.3,
                    pointRadius: 0,
                    pointHoverRadius: 5,
                    borderWidth: 2,
                    order: 1,
                },
                {
                    label: 'Predicted Close (Test Set)',
                    data: data.predicted,
                    borderColor: '#fd7e14',
                    backgroundColor: 'transparent',
                    fill: false,
                    tension: 0.3,
                    pointRadius: 0,
                    pointHoverRadius: 5,
                    borderWidth: 2.5,
                    borderDash: [5, 3],
                    spanGaps: false,   // don't connect across nulls
                    order: 0,
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { mode: 'index', intersect: false },
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
                    filter: function(item) {
                        return item.parsed.y !== null;
                    },
                    callbacks: {
                        label: function(context) {
                            if (context.parsed.y === null) return null;
                            return context.dataset.label + ': Rp ' +
                                   context.parsed.y.toLocaleString('id-ID', { maximumFractionDigits: 0 });
                        }
                    }
                },
                annotation: { annotations },
                zoom: makeZoomConfig('resetZoomBtn_actualVsPredChart'),
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
                    ticks: { maxTicksLimit: 14, font: { size: 10 } }
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

    forecastChartInstance = new Chart(ctx, {
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
                pointRadius: 7,
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
                                   context.parsed.y.toLocaleString('id-ID', { maximumFractionDigits: 0 });
                        }
                    }
                },
                zoom: makeZoomConfig('resetZoomBtn_forecastChart'),
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

// ==========================================
// Reset zoom helpers
// ==========================================
function resetActualVsPredZoom() {
    if (actualVsPredChartInstance) {
        actualVsPredChartInstance.resetZoom();
        const btn = document.getElementById('resetZoomBtn_actualVsPredChart');
        if (btn) btn.style.display = 'none';
    }
}

function resetForecastZoom() {
    if (forecastChartInstance) {
        forecastChartInstance.resetZoom();
        const btn = document.getElementById('resetZoomBtn_forecastChart');
        if (btn) btn.style.display = 'none';
    }
}
