import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    ssh.connect("104.238.214.91", username="admin", password="Zyanite777#628152", timeout=5)
    print("SUCCESS: admin")
    ssh.close()
except Exception as e:
    print(f"FAILED: admin - {e}")
