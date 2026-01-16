import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('45.61.59.218', username='root', password='Charlesalexander777#', timeout=60)

# Check if backend is listening
stdin, stdout, stderr = ssh.exec_command('curl -s http://127.0.0.1:80/healthz')
print('Health check:', stdout.read().decode())

# Check ports
stdin, stdout, stderr = ssh.exec_command('ss -tlnp')
print('Listening ports:')
print(stdout.read().decode())

# Check backend log
stdin, stdout, stderr = ssh.exec_command('tail -20 /root/backend.log')
print('Backend log:')
print(stdout.read().decode())

ssh.close()
