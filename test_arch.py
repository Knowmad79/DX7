import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    ssh.connect("104.238.214.91", username="arch", password="Zyanite777#628152", timeout=5)
    print("SUCCESS: arch")
    ssh.close()
except Exception as e:
    print(f"FAILED: arch - {e}")
