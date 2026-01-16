import paramiko
import time

def test_passwords():
    ip = "104.238.214.91"
    user = "root"
    passwords = [
        "Zyanite777#628152",
        "Zyanite777#628152 ",
        " Zyanite777#628152",
        "zyanite777#628152",
        "Zyanite777628152",
    ]
    
    for pwd in passwords:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            print(f"Trying password: {pwd}")
            ssh.connect(ip, username=user, password=pwd, timeout=5, look_for_keys=False, allow_agent=False)
            print(f"SUCCESS with {pwd}")
            ssh.close()
            return pwd
        except paramiko.AuthenticationException:
            print(f"FAILED with {pwd}")
        except Exception as e:
            print(f"ERROR with {pwd}: {e}")
    return None

if __name__ == "__main__":
    test_passwords()
