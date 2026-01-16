import paramiko
import time
import sys

def deploy():
    ip = "104.238.214.91"
    user = "root"
    password = "Zyanite777#628152"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print(f"Connecting to {ip}...")
        # Reinforced connection flags
        ssh.connect(
            ip, 
            username=user, 
            password=password, 
            look_for_keys=False, 
            allow_agent=False, 
            timeout=60,
            banner_timeout=60,
            auth_timeout=60
        )
        print("Connected successfully.")
        
        # Giant execution block
        cmd = (
            "cd /root/docx && git fetch origin main && git reset --hard origin/main && "
            "pacman -Sy nodejs npm nginx git python-pip --noconfirm && "
            "cd docboxrx-frontend && echo 'VITE_API_URL=http://104.238.214.91:8000' > .env.production && "
            "npm install && npm run build && "
            "printf 'events { worker_connections 1024; }\\nhttp {\\n    include mime.types;\\n    sendfile on;\\n    server {\\n        listen 80;\\n        location / {\\n            root /root/docx/docboxrx-frontend/dist;\\n            index index.html;\\n            try_files $uri $uri/ /index.html;\\n        }\\n    }\\n}\\n' > /etc/nginx/nginx.conf && "
            "systemctl enable nginx && systemctl restart nginx && "
            "pip install --break-system-packages fastapi uvicorn cerebras-cloud-sdk nylas pydantic python-jose bcrypt python-multipart email-validator python-dotenv PyJWT && "
            "cd /root/docx/docboxrx-backend && python create_tables.py && "
            "pkill uvicorn || true && "
            "nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &"
        )
        
        print("Executing full stack build (2-3 minutes)...")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        
        # Keep connection alive and stream output
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode('utf-8', errors='ignore'), end='')
                sys.stdout.flush()
            if stderr.channel.recv_stderr_ready():
                print(stderr.channel.recv_stderr(1024).decode('utf-8', errors='ignore'), file=sys.stderr, end='')
                sys.stderr.flush()
            time.sleep(1)
            
        print(f"\nDEPLOYMENT FINISHED. Exit code: {stdout.channel.recv_exit_status()}")
        ssh.close()
        return True
    except Exception as e:
        print(f"FATAL ERROR: {e}")
        return False

if __name__ == "__main__":
    deploy()
