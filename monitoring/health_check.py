"""
Health monitoring script for all services
Run as cron job: */5 * * * * /path/to/health_check.py
"""

import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

SERVICES = {
    "MCP Server": "http://localhost:8001/mcp/health",
    "FastAPI": "http://localhost:8000/api/issues",
    "Streamlit": "http://localhost:8501"
}

ALERT_EMAIL = "admin@example.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "alerts@example.com"
SMTP_PASS = "your_password"

def check_service(name, url):
    try:
        response = requests.get(url, timeout=10)
        return response.status_code == 200
    except:
        return False

def send_alert(service_name):
    msg = MIMEText(f"ALERT: {service_name} is down!\nTime: {datetime.now()}")
    msg['Subject'] = f'Service Down: {service_name}'
    msg['From'] = SMTP_USER
    msg['To'] = ALERT_EMAIL
    
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
    except Exception as e:
        print(f"Failed to send alert: {e}")

def main():
    for service_name, url in SERVICES.items():
        if not check_service(service_name, url):
            print(f"❌ {service_name} is DOWN")
            send_alert(service_name)
        else:
            print(f"✅ {service_name} is UP")

if __name__ == "__main__":
    main()