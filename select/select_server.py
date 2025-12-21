# Example usage:
#
# python select_server.py 3490

import sys
import socket
import select

def run_server(port):
    # TODO--fill this in
    listener = socket.socket()
    listener.bind(('',port))
    listener.listen()
    
    read_set = set()
    read_set.add(listener)
    
    while True:
        ready_to_read, _, _ = select.select(read_set, {}, {})
        for s in ready_to_read:
            if s == listener:
                new_s, connection_info = listener.accept()
                print(connection_info, end = ": connected\n")
                read_set.add(new_s)
            else:
                buf = s.recv(4096)
                if len(buf) == 0 :
                    print(s.getpeername(), end = ": disconnected\n")
                    read_set.remove(s)
                else:
                    print(s.getpeername(), end = f"{len(buf)} bytes : {buf}\n")

                


#--------------------------------#
# Do not modify below this line! #
#--------------------------------#

def usage():
    print("usage: select_server.py port", file=sys.stderr)

def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    run_server(port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
