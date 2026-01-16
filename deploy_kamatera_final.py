import paramiko
import time
import sys

def deploy():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    password = "Zyanite777#628152"
    ip = "104.238.214.91"
    
    try:
        print(f'Attempting connection to {ip}...')
        ssh.connect(ip, username='root', password=password, timeout=10)
        print('Connected successfully.')
        
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
        
        print('Running full deployment payload...')
        stdin, stdout, stderr = ssh.exec_command(cmd)
        
        # We need to stay connected to see the build output
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                data = stdout.channel.recv(1024).decode('utf-8', errors='ignore')
                print(data, end='')
                sys.stdout.flush()
            if stderr.channel.recv_stderr_ready():
                err_data = stderr.channel.recv_stderr(1024).decode('utf-8', errors='ignore')
                print(err_data, file=sys.stderr, end='')
                sys.stderr.flush()
            time.sleep(0.1)
            
        exit_code = stdout.channel.recv_exit_status()
        print(f'\nDeployment finished. Exit code: {exit_code}')
        ssh.close()
        return exit_code == 0
    except Exception as e:
        print(f'\nERROR: {str(e)}', file=sys.stderr)
        return False

if __name__ == "__main__":
    deploy()
