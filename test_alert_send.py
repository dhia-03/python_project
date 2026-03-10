#!/usr/bin/env python3
"""
Test script to send a fake alert to the dashboard
"""
import requests
import json
from datetime import datetime

dashboard_url = "http://localhost:5000/api/alert"

# Create a test alert
alert = {
    'timestamp': datetime.now().isoformat(),
    'threat_type': 'signature',
    'rule': 'port_scan',
    'source_ip': '192.168.1.100',
    'destination_ip': '192.168.1.1',
    'confidence': 0.95,
    'details': {'test': True},
    'severity': 'critical'
}

print("Sending test alert to dashboard...")
print(f"URL: {dashboard_url}")
print(f"Alert: {json.dumps(alert, indent=2)}")

try:
    response = requests.post(dashboard_url, json=alert, timeout=2)
    print(f"\nResponse Status: {response.status_code}")
    print(f"Response Body: {response.text}")
    
    if response.status_code == 200:
        print("\n✓ Alert sent successfully!")
        print("Check the dashboard at: http://localhost:5000")
    else:
        print(f"\n✗ Failed to send alert")
except Exception as e:
    print(f"\n✗ Error: {e}")
