import paramiko
import time
import sys

def run_cmd(ssh, cmd):
    print(f"Executing: {cmd}")
    stdin, stdout, stderr = ssh.exec_command(cmd)
    exit_status = stdout.channel.recv_exit_status()
    out = stdout.read().decode('utf-8', errors='ignore')
    err = stderr.read().decode('utf-8', errors='ignore')
    if out: print(f"STDOUT: {out}")
    if err: print(f"STDERR: {err}")
    return exit_status

def deploy():
    ip = "104.238.214.91"
    user = "root"
    password = "Zyanite777#628152"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print(f"Connecting to {ip}...")
        ssh.connect(ip, username=user, password=password, look_for_keys=False, allow_agent=False, timeout=30)
        print("Connected successfully.")
        
        # 1. Update system and install base dependencies
        print("Step 1: Installing system dependencies...")
        run_cmd(ssh, "pacman -Sy nodejs npm nginx git python-pip --noconfirm")
        
        # 2. Ensure project exists and is up to date
        print("Step 2: Syncing code from GitHub...")
        ssh.exec_command("git clone https://github.com/Knowmad79/docx.git /root/docx || true")
        run_cmd(ssh, "cd /root/docx && git reset --hard && git pull origin main")
        
        # 3. Build Frontend
        print("Step 3: Building production frontend...")
        frontend_cmd = (
            "cd /root/docx/docboxrx-frontend && "
            "echo 'VITE_API_URL=http://104.238.214.91:8000' > .env.production && "
            "npm install && npm run build"
        )
        run_cmd(ssh, frontend_cmd)
        
        # 4. Configure Nginx
        print("Step 4: Configuring Nginx web server...")
        nginx_conf = """events { worker_connections 1024; }
http {
    include mime.types;
    sendfile on;
    server {
        listen 80;
        location / {
            root /root/docx/docboxrx-frontend/dist;
            index index.html;
            try_files $uri $uri/ /index.html;
        }
    }
}
"""
        # Escape $ for the shell command
        safe_conf = nginx_conf.replace('$', '\\$')
        ssh.exec_command(f"printf '{safe_conf}' > /etc/nginx/nginx.conf")
        run_cmd(ssh, "systemctl enable nginx && systemctl restart nginx")
        
        # 5. Install Backend dependencies
        print("Step 5: Installing backend dependencies...")
        run_cmd(ssh, "pip install --break-system-packages fastapi uvicorn cerebras-cloud-sdk nylas pydantic python-jose bcrypt python-multipart email-validator python-dotenv PyJWT")
        
        # 6. Initialize DB and Start Backend
        print("Step 6: Launching backend engine...")
        run_cmd(ssh, "cd /root/docx/docboxrx-backend && python create_tables.py")
        ssh.exec_command("pkill uvicorn || true")
        ssh.exec_command("cd /root/docx/docboxrx-backend && nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &")
        
        print("\n" + "="*40)
        print("DEPLOYMENT COMPLETE!")
        print(f"URL: http://{ip}")
        print("="*40)
        
        ssh.close()
        return True
    except Exception as e:
        print(f"FATAL ERROR: {e}")
        return False

if __name__ == "__main__":
    deploy()
