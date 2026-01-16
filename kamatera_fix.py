import requests
import json
import time
import subprocess

CLIENT_ID = '7709dd8b46b3f0eec99366a07b7e1edb'
API_SECRET = 'ae7fdb5dec5ca50daac06363ccf1f206'
SERVER_PASS = 'Zyanite777#628152'
SERVER_IP = '104.238.214.91'
SERVER_NAME = 'hypernova7'

headers = {
    'AuthClientId': CLIENT_ID,
    'AuthSecret': API_SECRET,
    'Content-Type': 'application/json'
}

BASE = 'https://cloudcli.cloudwm.com'

print("=" * 60)
print("KAMATERA SERVER RECOVERY")
print("=" * 60)

# Step 1: Get server info by name
print(f"\n[1] Getting server info for '{SERVER_NAME}'...")
r = requests.post(
    f'{BASE}/service/server', 
    headers=headers, 
    json={'name': SERVER_NAME, 'password': SERVER_PASS}, 
    timeout=30
)
print(f"    Status: {r.status_code}")
print(f"    Response: {r.text[:500]}")

# Step 2: Try force reboot
print(f"\n[2] Force rebooting '{SERVER_NAME}'...")
r = requests.post(
    f'{BASE}/service/server/reboot',
    headers=headers,
    json={'name': SERVER_NAME, 'password': SERVER_PASS, 'force': True},
    timeout=30
)
print(f"    Status: {r.status_code}")
print(f"    Response: {r.text[:300]}")

# Step 3: Also try poweroff/poweron cycle
print(f"\n[3] Power cycling...")
for action in ['poweroff', 'poweron']:
    r = requests.post(
        f'{BASE}/service/server/{action}',
        headers=headers,
        json={'name': SERVER_NAME, 'password': SERVER_PASS},
        timeout=30
    )
    print(f"    {action}: {r.status_code} - {r.text[:150]}")
    if action == 'poweroff':
        time.sleep(10)

# Step 4: Wait for boot
print("\n[4] Waiting 60 seconds for boot...")
time.sleep(60)

# Step 5: Test connectivity
print("\n[5] Testing connectivity...")
# Try ping first
result = subprocess.run(['ping', '-n', '2', SERVER_IP], capture_output=True, text=True)
if 'Reply from' in result.stdout:
    print("    Ping: SUCCESS!")
else:
    print("    Ping: FAILED")

# Try SSH
print("\n[6] Testing SSH...")
result = subprocess.run(
    ['ssh', '-o', 'ConnectTimeout=15', '-o', 'StrictHostKeyChecking=no', 
     '-o', 'PasswordAuthentication=yes', f'root@{SERVER_IP}', 'echo SSH_SUCCESS'],
    capture_output=True, text=True, timeout=30
)
print(f"    Exit: {result.returncode}")
if result.stdout:
    print(f"    Output: {result.stdout}")
if result.stderr:
    print(f"    Error: {result.stderr[:200]}")

print("\n" + "=" * 60)
