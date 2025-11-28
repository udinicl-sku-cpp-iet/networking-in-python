import socket
import sys
import os

def port()->int:
    port = 28333
    if len(sys.argv) == 2:
        port = int(sys.argv[1])
    return port

def content_type(filename : str) -> str:
    match os.path.splitext(filename)[-1]:
            case ".txt":
                return "text/plain"
            case ".html":
                return "text/html"
            case ".pdf":
                return "application/pdf"
            case ".jpg":
                return "image/jpeg"
            case ".jpeg":
                return "image/jpeg"
            case ".gif":
                return "image/gif"
            case _:
                return "application/octet-stream"
def error404():
    data = b'404 not found'
    http_response =  ("HTTP/1.1 404 Not Found"     + "\r\n"    +\
                      "Content-Type: text/plain"   + "\r\n"    +\
                     f"Content-Length: {len(data)}"+ "\r\n"    +\
                      "Connection: close"          + "\r\n\r\n").encode('ISO-8859-1')
    return http_response, data

def response(data : bytes, mime_type : str):
   
    return  ("HTTP/1.1 200 OK"                    + "\r\n"+\
             f"Content-Type: {mime_type}"          + "\r\n"+\
             f"Content-Length:{len(data)} "        + "\r\n"+\
             "Connection: close"                   + "\r\n\r\n").encode('ISO-8859-1')


def directory_listing(dir_path, request_path):
    """
    Genera una pagina HTML con l'elenco dei file in dir_path.
    Ogni elemento è un link cliccabile.
    request_path serve per ricostruire correttamente gli URL.
    """

    items = os.listdir(dir_path)

    # Assicuriamoci che il path termini con '/'
    if not request_path.endswith("/"):
        request_path += "/"

    html = "<html><body><h1>Index of " + request_path + "</h1><ul>"

    for item in items:
        item_path = request_path + item

        # Se è una directory, aggiungi '/' alla fine
        if os.path.isdir(os.path.join(dir_path, item)):
            item_path += "/"
            display_name = item + "/"
        else:
            display_name = item

        html += f'<li><a href="{item_path}">{display_name}</a></li>'

    html += "</ul></body></html>"

    return html.encode("ISO-8859-1")


    
if __name__ == "__main__":
    server_root = os.path.abspath("./file")
    
    port = port()
    
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('',port))
    s.listen()
    
    while True:
        new_socket, (client_ip, client_port) = s.accept()
        print("New connection from:", client_ip, "port:", client_port)
        
        buf = b''
        while b'\r\n\r\n' not in buf:
            data = new_socket.recv(4096)
            if not data:
                break
            buf += data
            
        path_requested = buf.split(b'\r\n')[0].split()[1].decode("ISO-8859-1")
        file_requested = os.path.sep.join((server_root, path_requested))
        file_requested = os.path.abspath(file_requested)
        assert(file_requested.startswith(server_root))
        mime_type = content_type(file_requested)

        try:
            if os.path.isdir(file_requested):
                data = directory_listing(file_requested, path_requested)
                mime_type = "text/html"
            else:
                with open(file_requested, "rb") as f:
                    data = f.read()
            http_response = response(data, mime_type)
            
        except:
            http_response,data = error404()
                         
        new_socket.sendall(http_response + data)
