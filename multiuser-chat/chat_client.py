import sys
import socket
import json
import threading
import os 
from chatui import init_windows, read_command, print_message, end_windows

WORD_LEN_SIZE = 2

def usage():
    print("Usage : python3 chat_client.py <nickname> <ip> <port>", file=sys.stderr)


def runner(s : socket.socket):
    packet_buffer = b''
    while True:
        while len(packet_buffer) < WORD_LEN_SIZE:
            data = s.recv(10)
            if not data:
                print_message("*** Connessione chiusa dal server ***")
                end_windows()
                os._exit(1)
            packet_buffer += data

        n = int.from_bytes(packet_buffer[:WORD_LEN_SIZE],"big")
        
        while len(packet_buffer) < WORD_LEN_SIZE + n:
            data = s.recv(10)
            if not data:
                print_message("*** Connessione chiusa dal server ***")
                end_windows()
                os._exit(1)
            packet_buffer += data
            
        packet        = packet_buffer[WORD_LEN_SIZE :WORD_LEN_SIZE+n]
        packet_buffer = packet_buffer[WORD_LEN_SIZE+n:]
        packet        = json.loads(packet.decode())
        match packet.get('type'):
            case 'join':
                print_message(f"*** {packet.get('nick')} has joined the chat")
            case 'leave':
                print_message(f"*** {packet.get('nick')} has leaved the chat")
            case 'chat':
                print_message(f"{packet.get('nick')}> {packet.get('message')}")
                

    
def main(argv : list):
    try:
        nickname =     sys.argv[1]
        host     =     sys.argv[2]
        port     = int(sys.argv[3])
    except:
        usage()
        return 1
    
    s = socket.socket()
    s.connect((host, port))

    data = {
        "type":  "hello",
        "nick": f"{nickname}"
    }
    json_string = json.dumps(data).encode()
    json_string = len(json_string).to_bytes(WORD_LEN_SIZE, "big") + json_string
    s.sendall(json_string)

    init_windows()
    t1 = threading.Thread(target=runner, args = (s,), daemon=True)
    t1.start()
    
    while True:
        try:
            message = read_command(f"{nickname}> ")
            print_message(f"{nickname}> {message}")
            data = {
                "type":     "chat",
                "message": f"{message}"
            }
            json_string = json.dumps(data).encode()
            json_string = len(json_string).to_bytes(WORD_LEN_SIZE, "big") + json_string
            s.sendall(json_string)
        except:
            break
    
    

if __name__ == "__main__":
    sys.exit(main(sys.argv))
