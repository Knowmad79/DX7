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
        # Force password authentication and disable keys/agent to avoid 'Authentication failed'
        ssh.connect(
            ip, 
            username=user, 
            password=password, 
            look_for_keys=False, 
            allow_agent=False, 
            timeout=30
        )
        print("Connected successfully.")
        
        # This giant block does EVERYTHING: Syncs code, builds frontend, configs Nginx, starts backend
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
        
        print("Executing full stack build. This will take ~2 minutes. Do not disconnect...")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        
        # Stream output so you know it's working
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode('utf-8', errors='ignore'), end='')
                sys.stdout.flush()
            if stderr.channel.recv_stderr_ready():
                print(stderr.channel.recv_stderr(1024).decode('utf-8', errors='ignore'), file=sys.stderr, end='')
                sys.stderr.flush()
            time.sleep(1)
            
        print(f"\nDEPLOYMENT COMPLETE. Exit code: {stdout.channel.recv_exit_status()}")
        ssh.close()
        return True
    except Exception as e:
        print(f"FATAL ERROR: {e}")
        return False

if __name__ == "__main__":
    deploy()
