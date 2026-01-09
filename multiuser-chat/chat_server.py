import sys
import socket
import select
import json

WORD_LEN_SIZE = 2

def broadcast_json(socket_list, data, listener, sender = None):
    data = json.dumps(data).encode()
    data = len(data).to_bytes(WORD_LEN_SIZE, "big") + data
    for socket in socket_list:
        if socket != listener and socket != sender:
            socket.sendall(data)

def extract_packet(buf):
    if len(buf) < WORD_LEN_SIZE:
        return None, buf
    n = int.from_bytes(buf[:2],"big")
    
    if len(buf) < WORD_LEN_SIZE+n:        
        return None, buf
    else:        
        return buf[WORD_LEN_SIZE:WORD_LEN_SIZE+n], buf[WORD_LEN_SIZE+n:]
    
    

def run_server(port):
    
    listener = socket.socket()
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(('',port))
    listener.listen()
    
    read_set = set()
    read_set.add(listener)


    socket_registry = {}
    
    while True:
        ready_to_read, _, _ = select.select(read_set, {}, {})
        for s in ready_to_read:
            if s == listener:
                new_s = listener.accept()[0]
                read_set.add(new_s)
                socket_registry[new_s.fileno()] = [b'',b'']
            else:
                buf = s.recv(1)
                if len(buf) == 0 :
                    data = {
                                    "type":  "leave",
                                    "nick": f"{socket_registry[s.fileno()][0]}"
                    }
                    del socket_registry[s.fileno()]
                    read_set.remove(s)

                    broadcast_json(read_set, data, listener)
                else:
                    socket_registry[s.fileno()][1] += buf
                    packet, socket_registry[s.fileno()][1] = extract_packet(socket_registry[s.fileno()][1])
                    if packet != None:
                        packet = json.loads(packet.decode())
                        match packet.get('type'):
                            case 'hello':
                                nickname = packet.get('nick')
                                socket_registry[s.fileno()][0] = nickname
                                data = {
                                    "type":  "join",
                                    "nick": f"{socket_registry[s.fileno()][0]}"
                                }
                                broadcast_json(read_set, data, listener, s)
                            case 'chat':
                                data = {
                                    "type"   :  "chat",
                                    "nick"   : f"{socket_registry[s.fileno()][0]}",
                                    "message": f"{packet.get('message')}"
                                }
                                broadcast_json(read_set, data, listener, s)
                               



def usage():
    print("usage: chat_server.py port", file=sys.stderr)

def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    run_server(port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
