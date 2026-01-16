import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    ssh.connect("104.238.214.91", username="root", password="Zyanite777#628152")
    print("SUCCESS")
    ssh.close()
except Exception as e:
    print(f"FAILED: {e}")
