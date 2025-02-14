<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Switch Monitoring Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; }
        table { width: 80%; margin: auto; border-collapse: collapse; }
        th, td { padding: 10px; border: 1px solid #ccc; text-align: left; }
        th { background-color: #333; color: white; }
        .up { color: green; font-weight: bold; }
        .down { color: red; font-weight: bold; }
        .controls { margin-bottom: 20px; }
    </style>
</head>
<body>
    <h2>Cisco Switch Monitoring Dashboard</h2>

    <div class="controls">
        <form action="/control" method="POST">
            <button type="submit" name="start">Start</button>
            <button type="submit" name="stop">Stop</button>
            <label for="interval">Check Interval:</label>
            <select name="interval" id="interval" onchange="this.form.submit()">
                <option value="5" {% if check_interval == 5 %}selected{% endif %}>5 min</option>
                <option value="10" {% if check_interval == 10 %}selected{% endif %}>10 min</option>
                <option value="20" {% if check_interval == 20 %}selected{% endif %}>20 min</option>
            </select>
        </form>
    </div>

    <table>
        <tr>
            <th>Name</th>
            <th>IP Address</th>
            <th>Status</th>
            <th>Timestamp</th>
        </tr>
        {% for row in data %}
        <tr>
            <td>{{ row.name }}</td>
            <td>{{ row.ip }}</td>
            <td class="{{ 'up' if row.status == 'UP' else 'down' }}">{{ row.status }}</td>
            <td>{{ row.timestamp }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
