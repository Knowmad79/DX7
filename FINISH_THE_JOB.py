import paramiko
import time
import sys
import json
import os
from datetime import datetime

LOG_PATH = r"d:\dbrx\.cursor\debug.log"

def log_to_file(hypothesis_id, location, message, data=None):
    entry = {
        "id": f"log_{int(time.time())}_{hypothesis_id}",
        "timestamp": int(time.time() * 1000),
        "location": location,
        "message": message,
        "data": data or {},
        "sessionId": "debug-session",
        "runId": "run1",
        "hypothesisId": hypothesis_id
    }
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")

def deploy():
    ip = "104.238.214.91"
    user = "root"
    password = "Zyanite777#628152"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    log_to_file("A", "FINISH_THE_JOB.py:15", "Attempting SSH connection", {"ip": ip, "user": user})

    try:
        print(f"Connecting to {ip}...")
        key_env = os.environ.get("KAMATERA_SSH_KEY")
        key_path = key_env or os.path.join(os.path.dirname(__file__), "kamatera_key")
        key_path = os.path.expanduser(key_path)
        key_path = os.path.abspath(key_path)
        # region agent log
        log_to_file("G", "FINISH_THE_JOB.py:19", "Resolved key path", {"key_path": key_path, "env_source": bool(key_env)})
        # endregion agent log
        if not os.path.isfile(key_path):
            # region agent log
            log_to_file("H", "FINISH_THE_JOB.py:20", "Key file missing", {"key_path": key_path})
            # endregion agent log
            print("SSH key not found. Please set KAMATERA_SSH_KEY or place kamatera_key beside this script.")
            return False
        key = paramiko.RSAKey.from_private_key_file(key_path)
        # region agent log
        log_to_file("I", "FINISH_THE_JOB.py:21", "About to connect to server", {"timeout": 60})
        # endregion agent log
        ssh.connect(ip, username=user, pkey=key, timeout=60)
        log_to_file("C", "FINISH_THE_JOB.py:19", "SSH connection successful", {"connected": True})
        print("Connected. Finalizing deployment...")

        # Absolute Payload using correct 'dbrx' folder
        cmd = (
            "cd ~ && rm -rf dbrx && git clone https://github.com/Knowmad79/docx.git dbrx && "
            "cd dbrx && pacman -Sy nodejs npm nginx --noconfirm && "
            "cd docboxrx-frontend && echo 'VITE_API_URL=http://104.238.214.91:8000' > .env.production && "
            "npm install && npm run build && "
            "printf 'events { worker_connections 1024; }\\nhttp {\\n    include mime.types;\\n    sendfile on;\\n    server {\\n        listen 80;\\n        location / {\\n            root /root/dbrx/docboxrx-frontend/dist;\\n            index index.html;\\n            try_files $uri $uri/ /index.html;\\n        }\\n    }\\n}\\n' > /etc/nginx/nginx.conf && "
            "systemctl enable nginx && systemctl restart nginx && "
            "cd /root/dbrx/docboxrx-backend && pip install --break-system-packages fastapi uvicorn cerebras-cloud-sdk nylas pydantic python-jose bcrypt python-multipart email-validator python-dotenv PyJWT && "
            "python create_tables.py && pkill uvicorn || true && "
            "nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &"
        )

        log_to_file("D", "FINISH_THE_JOB.py:21", "Executing remote command", {"cmd_length": len(cmd)})
        stdin, stdout, stderr = ssh.exec_command(cmd)
        exit_status = stdout.channel.recv_exit_status()
        log_to_file("E", "FINISH_THE_JOB.py:22", "Command execution result", {"exit_status": exit_status})

        print(f"Deployment finished with status: {exit_status}")
        ssh.close()
        print(f"URL: http://{ip}")
        return True
    except Exception as e:
        log_to_file("F", "FINISH_THE_JOB.py:24", "Exception during deployment", {"error": str(e), "error_type": type(e).__name__})
        print(f"FATAL ERROR: {e}")
        return False

if __name__ == "__main__":
    deploy()
