import paramiko
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('45.61.59.218', username='root', password='Charlesalexander777#', timeout=60)
print('Connected!')

# Create startup script with env vars baked in
script = '''#!/bin/bash
export DATABASE_URL="sqlite:///root/docboxrx.db"
export CEREBRAS_API_KEY="csk-kcphx6mm8pnfy56rn6fe3wcmhkw6wxc56jthekfvpk3fcmwt"
export NYLAS_API_KEY="nyk_v0_lPt52DfSYzutwat78WlItFejHHj2MyyZQPm1pHYQcmHO5gDWb6pIAwTanwZpHhkM"
export NYLAS_CLIENT_ID="ec54cf83-8648-4e04-b547-3de100de9b48"
cd /root/dbrx/docboxrx-backend
exec uvicorn app.main:app --host 0.0.0.0 --port 80
'''

# Write startup script
stdin, stdout, stderr = ssh.exec_command(f'cat > /root/start_backend.sh << \'ENDSCRIPT\'\n{script}\nENDSCRIPT')
stdout.channel.recv_exit_status()

stdin, stdout, stderr = ssh.exec_command('chmod +x /root/start_backend.sh')
stdout.channel.recv_exit_status()

# Kill existing and start fresh
stdin, stdout, stderr = ssh.exec_command('pkill -f uvicorn || true')
stdout.channel.recv_exit_status()
time.sleep(1)

stdin, stdout, stderr = ssh.exec_command('nohup /root/start_backend.sh > /root/backend.log 2>&1 &')
stdout.channel.recv_exit_status()
print('Started backend script')
time.sleep(4)

# Check if running
stdin, stdout, stderr = ssh.exec_command('pgrep -f uvicorn')
pid = stdout.read().decode().strip()
print(f'PID: {pid}')

if not pid:
    stdin, stdout, stderr = ssh.exec_command('cat /root/backend.log')
    print('LOG:')
    print(stdout.read().decode()[-2000:])
else:
    stdin, stdout, stderr = ssh.exec_command('curl -s http://127.0.0.1:80/healthz')
    print('Health:', stdout.read().decode())
    print('SUCCESS! http://45.61.59.218')

ssh.close()
