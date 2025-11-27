import socket
http_response = b"HTTP/1.1 200 OK"+b"\r\n"+\
                b"Content-Type: text/plain" +b"\r\n"+\
                b"Content-Length: 6"+b"\r\n"+\
                b"Connection: close"+b"\r\n\r\n"+\
                b"Hello!" + b"\r\n"
if __name__ == "__main__":
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('',28333))
    s.listen()
    while True:
        new_socket = s.accept()[0]
        print("new connection")
        buf = b''
        while b'\r\n\r\n' not in buf:
            data = new_socket.recv(4096)
            if not data:
                break
            buf += data
        new_socket.sendall(http_response)
        new_socket.close()
        
