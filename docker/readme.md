Here's a **Dockerfile** to containerize your Cisco Switch Monitoring app. It includes:  

✅ **Ubuntu 22-based image**  
✅ **Python environment setup**  
✅ **Flask & SNMP dependencies**  
✅ **Exposes Flask on port 5000**  

---

### **📄 Dockerfile**
```dockerfile
# Use Ubuntu 22 as the base image
FROM ubuntu:22.04

# Set environment variables to avoid interactive prompts during install
ENV DEBIAN_FRONTEND=noninteractive

# Update and install required packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    libsnmp-dev \
    snmp \
    snmp-mibs-downloader \
    mysql-client \
    && apt-get clean

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 5000

# Command to run the script
CMD ["python3", "script.py"]
```

---

### **📄 `requirements.txt` (Add this file)**
```txt
Flask
pysnmp
mysql-connector-python
curses
configparser
```

---

### **🚀 How to Build & Run the Docker Container**
1️⃣ **Build the Docker Image**  
```bash
docker build -t cisco-monitor .
```
  
2️⃣ **Run the Container**  
```bash
docker run -d -p 5000:5000 --name cisco-monitor cisco-monitor
```

3️⃣ **Access the Dashboard**  
- Open **http://your-server-ip:5000** in your browser.

---

This will run your app inside a **Docker container**, keeping it isolated from the rest of the system. Let me know if you need further adjustments! 🚀
