import socket
import time

TARGET_IP = '10.1.116.86'
TARGET_PORT = 80
PATH = '/login'

start_len = 100
end_len = 2000
step = 100

def send_payload(length):
    payload = 'A' * length
    body = f"username=test&password={payload}"
    request = (
        f"POST {PATH} HTTP/1.1\r\n"
        f"Host: {TARGET_IP}\r\n"
        f"User-Agent: fuzz-client\r\n"
        f"Content-Type: application/x-www-form-urlencoded\r\n"
        f"Content-Length: {len(body)}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
        f"{body}"
    )

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((TARGET_IP, TARGET_PORT))
        s.sendall(request.encode())
        response = s.recv(1024)
        s.close()
        return len(response)
    except Exception as e:
        return None

if __name__ == '__main__':
    print("Starting fuzzing:")
    for length in range(start_len, end_len + 1, step):
        print(f"Testing length: {length}", end=' ')
        result = send_payload(length)
        if result is None:
            print("No response, possible crash")
            break
        else:
            print(f"OK (resp {result} bytes)")
        time.sleep(0.5)
    print("Fuzzing complete")

