"""
Kamatera Deployment Script
Uses paramiko with explicit transport-level password auth
"""
import paramiko
import time
import socket

SERVER_IP = "104.238.214.91"
USERNAME = "root"
PASSWORD = "Zyanite777#628152"

def deploy():
    print(f"=" * 60)
    print(f"KAMATERA DEPLOYMENT - {SERVER_IP}")
    print(f"=" * 60)
    
    # Create transport directly for more control
    try:
        print("\n[1/5] Creating socket connection...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(30)
        sock.connect((SERVER_IP, 22))
        print("      Socket connected successfully")
        
        print("\n[2/5] Creating SSH transport...")
        transport = paramiko.Transport(sock)
        transport.connect(username=USERNAME, password=PASSWORD)
        print("      Transport authenticated!")
        
        print("\n[3/5] Opening SSH session channel...")
        ssh = paramiko.SSHClient()
        ssh._transport = transport
        
        # The deployment commands
        commands = [
            "cd /root/dbrx && git fetch origin main && git reset --hard origin/main",
            "cd /root/dbrx/docboxrx-final/docboxrx/docboxrx-backend && pip install --break-system-packages -q fastapi uvicorn cerebras-cloud-sdk nylas pydantic python-jose bcrypt python-multipart email-validator python-dotenv PyJWT",
            "cd /root/dbrx/docboxrx-final/docboxrx/docboxrx-backend && python create_tables.py",
            "pkill -f uvicorn || true",
            "cd /root/dbrx/docboxrx-final/docboxrx/docboxrx-backend && nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > /tmp/backend.log 2>&1 &"
        ]
        
        print("\n[4/5] Executing deployment commands...")
        for i, cmd in enumerate(commands):
            print(f"\n      [{i+1}/{len(commands)}] Running: {cmd[:60]}...")
            channel = transport.open_session()
            channel.exec_command(cmd)
            exit_status = channel.recv_exit_status()
            
            # Read any output
            stdout = channel.makefile('r', -1).read()
            stderr = channel.makefile_stderr('r', -1).read()
            
            if stdout:
                print(f"      Output: {stdout[:200]}")
            if stderr:
                print(f"      Error: {stderr[:200]}")
            print(f"      Exit: {exit_status}")
            channel.close()
            time.sleep(1)
        
        print("\n[5/5] Verifying backend is running...")
        channel = transport.open_session()
        channel.exec_command("curl -s http://localhost:8000/health || echo 'Backend starting...'")
        time.sleep(3)
        stdout = channel.makefile('r', -1).read()
        print(f"      Health check: {stdout}")
        channel.close()
        
        transport.close()
        sock.close()
        
        print("\n" + "=" * 60)
        print("DEPLOYMENT COMPLETE!")
        print(f"Backend URL: http://{SERVER_IP}:8000")
        print(f"API Docs: http://{SERVER_IP}:8000/docs")
        print("=" * 60)
        
    except paramiko.AuthenticationException as e:
        print(f"\n[ERROR] Authentication failed: {e}")
        print("The server rejected password login.")
        print("\nTry these manual steps:")
        print(f"  1. Open PowerShell and run: ssh root@{SERVER_IP}")
        print(f"  2. Enter password: {PASSWORD}")
        print(f"  3. Run: cd /root/dbrx && git pull && cd docboxrx-final/docboxrx/docboxrx-backend && nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 &")
        
    except socket.timeout:
        print(f"\n[ERROR] Connection timed out. Server may be unreachable.")
        
    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__}: {e}")

if __name__ == "__main__":
    deploy()
