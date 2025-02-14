### **Frontend, Ubuntu Server, and MySQL Setup Guide**

#### **1️⃣ Frontend (Flask + HTML Dashboard)**
You'll need a simple HTML template (`dashboard.html`) to display switch statuses.

#### 📌 **Create a Templates Folder**
Inside your script directory, create a `templates` folder and add `dashboard.html`:

📄 **`templates/dashboard.html`**
```html
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
    </style>
</head>
<body>
    <h2>Cisco Switch Monitoring Dashboard</h2>
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
```

📌 **Now, when you visit `http://your-server-ip:5000`, it will show the switch status.**

---

#### **2️⃣ Ubuntu Server Setup**
📌 **Install Dependencies**
Run these commands on your Ubuntu server:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv mysql-server -y
pip install flask mysql-connector-python
```

📌 **Start MySQL & Secure Installation**
```bash
sudo systemctl start mysql
sudo mysql_secure_installation
```
Follow the prompts to set a root password and secure MySQL.

---

#### **3️⃣ MySQL Database & Indexing**
📌 **Log in to MySQL**
```bash
mysql -u root -p
```
📌 **Create Database & Table**
```sql
CREATE DATABASE switch_monitor;
USE switch_monitor;

CREATE TABLE switch_status (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ip VARCHAR(15) NOT NULL,
    name VARCHAR(50) NOT NULL,
    status ENUM('UP', 'DOWN') NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```
📌 **Add Index for Faster Queries**
```sql
CREATE INDEX idx_ip ON switch_status(ip);
CREATE INDEX idx_timestamp ON switch_status(timestamp);
```
📌 **Create a MySQL User**
```sql
CREATE USER 'monitor_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON switch_monitor.* TO 'monitor_user'@'localhost';
FLUSH PRIVILEGES;
```

📌 **Update `config.ini`**
Create a `config.ini` file in your script directory:
```
[mysql]
host = localhost
user = monitor_user
password = your_password
database = switch_monitor
```

---

#### **4️⃣ Running the Script**
📌 **Start the Script**
```bash
python3 script.py
```
Then, visit `http://your-server-ip:5000` to see the web dashboard.

📌 **Run as a Background Service (Optional)**
```bash
nohup python3 script.py > output.log 2>&1 &
```

---

### ✅ **Now, you have:**
✔ A **Web Dashboard** to view switch statuses.  
✔ **Efficient MySQL queries** with indexing.  
✔ A **fully configured Ubuntu server** running MySQL and Flask.  

Let me know if you need any improvements! 🚀
