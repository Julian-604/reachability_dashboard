import curses
import time
import subprocess
import mysql.connector
import configparser
from flask import Flask, render_template

# Load configuration from file
config = configparser.ConfigParser()
config.read('config.ini')

DB_CONFIG = {
    "host": config.get("mysql", "host"),
    "user": config.get("mysql", "user"),
    "password": config.get("mysql", "password"),
    "database": config.get("mysql", "database")
}

# Flask app for web dashboard
app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# Load switches from a text file
def load_switches(file_path):
    switches = []
    with open(file_path, "r") as file:
        for line in file:
            parts = line.strip().split(",")
            if len(parts) == 2:
                switches.append({"ip": parts[0], "name": parts[1]})
    return switches

switches = load_switches("switches.txt")

def ping(ip):
    """Ping the given IP address and return True if reachable, False otherwise."""
    result = subprocess.run(["ping", "-c", "1", "-W", "1", ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result.returncode == 0

def log_status(ip, name, status):
    """Logs switch status changes to MySQL."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO switch_status (ip, name, status, timestamp)
            VALUES (%s, %s, %s, NOW())
        """, (ip, name, status))
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def display(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(1)   # Make getch non-blocking
    stdscr.timeout(1000)  # Refresh every second
    status = {}
    last_down = {}
    blink = {}
    down_time = {}

    while True:
        stdscr.clear()
        stdscr.addstr(0, 2, "Live Cisco Switch Monitoring", curses.A_BOLD)
        stdscr.addstr(1, 0, "=" * 80)
        stdscr.addstr(2, 2, "Reachable Devices", curses.A_UNDERLINE)
        stdscr.addstr(2, 40, "Unreachable Devices", curses.A_UNDERLINE)
        
        up_row = 3
        down_row = 3
        
        for switch in switches:
            ip = switch["ip"]
            name = switch["name"]
            reachable = ping(ip)
            
            if not reachable:
                if ip not in last_down:
                    last_down[ip] = time.time()
                    log_status(ip, name, "DOWN")
                blink[ip] = (time.time() - last_down[ip]) < 30  # Blink for 30 seconds
                status[ip] = "DOWN"
                down_time[ip] = time.strftime('%H:%M:%S', time.localtime(last_down[ip]))
            else:
                if status.get(ip) == "DOWN":  # Only log transition to UP
                    log_status(ip, name, "UP")
                status[ip] = "UP"
                if ip in last_down:
                    del last_down[ip]
                if ip in blink:
                    del blink[ip]
                if ip in down_time:
                    del down_time[ip]

            color = curses.color_pair(1) if status[ip] == "UP" else curses.color_pair(2)
            if blink.get(ip, False):
                color = curses.color_pair(3)
            
            if status[ip] == "UP":
                stdscr.addstr(up_row, 2, f"{name} ({ip})", color)
                up_row += 1
            else:
                stdscr.addstr(down_row, 40, f"{name} ({ip}) - Down Since: {down_time[ip]}", color)
                down_row += 1
        
        stdscr.refresh()
        if stdscr.getch() == ord('q'):
            break

@app.route('/')
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM switch_status ORDER BY timestamp DESC LIMIT 100")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('dashboard.html', data=data)

def main():
    curses.wrapper(lambda stdscr: setup_colors(stdscr) or display(stdscr))

def setup_colors(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # UP - Green
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # DOWN - Red
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Blinking DOWN

if __name__ == "__main__":
    main()
    app.run(host="0.0.0.0", port=5000, debug=True)
