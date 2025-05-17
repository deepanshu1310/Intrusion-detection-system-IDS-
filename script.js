$(document).ready(function() {
    $.get('/alerts', function(data) {
        const alertsList = $('#alert-list');
        alertsList.empty();
        data.forEach(function(ip) {
            alertsList.append(`<li>${ip}</li>`);
        });
    });

    $.get('/data', function(data) {
        const tableBody = $('#ip-table');
        tableBody.empty();
        Object.keys(data).forEach(function(ip) {
            const row = `<tr>
                <td>${ip}</td>
                <td>${data[ip].count}</td>
                <td>${data[ip].last_seen}</td>
                <td>${data[ip].location}</td>
                <td>${data[ip].org}</td>
            </tr>`;
            tableBody.append(row);
        });
    });

    $.get('/data', function(data) {
        const ctx = $('#barChart')[0].getContext('2d');
        const ipCounts = Object.values(data).map(info => info.count);
        const ipLabels = Object.keys(data);
        const chartData = {
            labels: ipLabels,
            datasets: [{
                label: 'IP Hits',
                data: ipCounts,
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        };
        const options = {
            responsive: true,
            scales: {
                x: { beginAtZero: true }
            }
        };
        new Chart(ctx, {
            type: 'bar',
            data: chartData,
            options: options
        });
    });
});
