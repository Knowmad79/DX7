import paramiko
import socket

def check_banner():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("104.238.214.91", 22))
    print(s.recv(1024).decode())
    s.close()

if __name__ == "__main__":
    check_banner()
