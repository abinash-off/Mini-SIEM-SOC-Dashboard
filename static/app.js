let severityChart;

async function loadStats() {
    const response = await fetch('/api/stats');
    const data = await response.json();
    document.getElementById('totalEvents').textContent = data.total_events;
    document.getElementById('totalAlerts').textContent = data.total_alerts;
    document.getElementById('criticalAlerts').textContent = data.critical_alerts;
    document.getElementById('highAlerts').textContent = data.high_alerts;
    loadChart(data);
}

function loadChart(data) {
    const ctx = document.getElementById('severityChart');
    if (severityChart) severityChart.destroy();
    severityChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Critical', 'High', 'Medium', 'Low'],
            datasets: [{
                label: 'Alerts',
                data: [data.critical_alerts, data.high_alerts, data.medium_alerts, data.low_alerts]
            }]
        },
        options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true, ticks: { precision: 0 } } } }
    });
}

async function loadAlerts() {
    const response = await fetch('/api/alerts');
    const alerts = await response.json();
    const table = document.getElementById('alertTable');
    table.innerHTML = '';
    alerts.forEach(alert => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${alert.id}</td>
            <td>${escapeHTML(alert.timestamp)}</td>
            <td>${escapeHTML(alert.alert_type)}</td>
            <td class="severity ${escapeHTML(alert.severity)}">${escapeHTML(alert.severity)}</td>
            <td>${escapeHTML(alert.source_ip || '-')}</td>
            <td>${escapeHTML(alert.mitre_id || '-')}</td>
            <td>${escapeHTML(alert.status)}</td>`;
        table.appendChild(row);
    });
}

async function loadEvents() {
    const response = await fetch('/api/events');
    const events = await response.json();
    const table = document.getElementById('eventTable');
    table.innerHTML = '';
    events.forEach(event => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${event.id}</td>
            <td>${escapeHTML(event.timestamp)}</td>
            <td>${escapeHTML(event.source)}</td>
            <td>${escapeHTML(event.source_ip || '-')}</td>
            <td>${escapeHTML(event.username || '-')}</td>
            <td>${escapeHTML(event.event_type)}</td>
            <td>${escapeHTML(event.message || '-')}</td>`;
        table.appendChild(row);
    });
}

function escapeHTML(value) {
    const div = document.createElement('div');
    div.textContent = String(value);
    return div.innerHTML;
}

async function refreshDashboard() {
    try {
        await Promise.all([loadStats(), loadAlerts(), loadEvents()]);
    } catch (error) {
        console.error('Dashboard refresh failed:', error);
    }
}

refreshDashboard();
setInterval(refreshDashboard, 10000);
