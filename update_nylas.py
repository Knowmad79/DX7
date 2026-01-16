import paramiko
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('45.61.59.218', username='root', password='Charlesalexander777#', timeout=60)
print('Connected!')

script = '''#!/bin/bash
export DATABASE_URL="sqlite:///root/docboxrx.db"
export CEREBRAS_API_KEY="csk-kcphx6mm8pnfy56rn6fe3wcmhkw6wxc56jthekfvpk3fcmwt"
export NYLAS_API_KEY="ea4023faa408ac8f041f203116fee366"
export NYLAS_CLIENT_ID="599af06a28ca0f30ac6f05863e582811"
export NYLAS_API_URI="https://api.us.nylas.com"
export NYLAS_CALLBACK_URI="http://45.61.59.218/api/nylas/callback"
cd /root/dbrx/docboxrx-backend
exec uvicorn app.main:app --host 0.0.0.0 --port 80
'''

# Write script
stdin, stdout, stderr = ssh.exec_command("cat > /root/start_backend.sh << 'EOF'\n" + script + "\nEOF")
stdout.channel.recv_exit_status()

stdin, stdout, stderr = ssh.exec_command('chmod +x /root/start_backend.sh')
stdout.channel.recv_exit_status()

# Restart
stdin, stdout, stderr = ssh.exec_command('pkill -f uvicorn || true')
stdout.channel.recv_exit_status()
time.sleep(1)

stdin, stdout, stderr = ssh.exec_command('nohup /root/start_backend.sh > /root/backend.log 2>&1 &')
stdout.channel.recv_exit_status()
time.sleep(3)

stdin, stdout, stderr = ssh.exec_command('curl -s http://127.0.0.1/healthz')
print(stdout.read().decode())
ssh.close()
print('Done - Nylas creds updated!')
