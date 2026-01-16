import paramiko
import time
import sys

def deploy():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print('Connecting to 104.238.214.91...')
        ssh.connect('104.238.214.91', username='root', password='Zyanite777#628152')
        print('Connected. Executing deployment script...')
        
        # Use absolute paths and run everything in one go
        cmd = (
            'cd /root/docx && git pull origin main && '
            'cd docboxrx-frontend && echo "VITE_API_URL=http://104.238.214.91:8000" > .env.production && '
            'npm install && npm run build && '
            'pacman -Sy nginx --noconfirm && '
            'printf "events { worker_connections 1024; }\\nhttp {\\n    include mime.types;\\n    sendfile on;\\n    server {\\n        listen 80;\\n        location / {\\n            root /root/docx/docboxrx-frontend/dist;\\n            index index.html;\\n            try_files \$uri \$uri/ /index.html;\\n        }\\n    }\\n}\\n" > /etc/nginx/nginx.conf && '
            'systemctl enable nginx && systemctl restart nginx && '
            'cd /root/docx/docboxrx-backend && python create_tables.py && '
            'pkill uvicorn; nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &'
        )
        
        stdin, stdout, stderr = ssh.exec_command(cmd)
        
        # Stream the output
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode('utf-8', errors='ignore'), end='')
                sys.stdout.flush()
            if stderr.channel.recv_stderr_ready():
                print(stderr.channel.recv_stderr(1024).decode('utf-8', errors='ignore'), file=sys.stderr, end='')
                sys.stderr.flush()
            time.sleep(0.5)
            
        exit_code = stdout.channel.recv_exit_status()
        print(f'\nDeployment finished with exit code: {exit_code}')
        ssh.close()
        return exit_code == 0
    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)
        return False

if __name__ == "__main__":
    deploy()
