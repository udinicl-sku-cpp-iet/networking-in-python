import socket
import sys

if __name__ == "__main__":
    s = socket.socket()
    s.connect((sys.argv[1], int(sys.argv[2])))
    http_request = "GET / HTTP/1.1"                    + "\r\n" +\
                  f"Host: {sys.argv[1]}:{sys.argv[2]}" + "\r\n" +\
                  "Connection: close"                 + "\r\n\r\n"
    http_request = http_request.encode('utf-8')
    s.sendall(http_request)
    buf = b""
    while True:
        data = s.recv(4096)
        if not data:
            break
        buf += data
    print(buf.decode('utf-8'))
