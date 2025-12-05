import sys
import json
import math  # If you want to use math.inf for infinity

def ipv4_to_value(ipv4_addr:str) -> int:
    """
    Convert a dots-and-numbers IP address to a single 32-bit numeric
    value of integer type. Returns an integer type.

    Example:

    ipv4_addr: "255.255.0.0"
    return:    4294901760  (Which is 0xffff0000 hex)

    ipv4_addr: "1.2.3.4"
    return:    16909060  (Which is 0x01020304 hex)
    """

    # TODO -- write me!
    value = 0x00000000
    for i, chunk in enumerate(ipv4_addr.split('.')):
        value = value | (int(chunk) << (24 - (8 * i) ) )
    return value

def value_to_ipv4(addr:int) -> str:
    """
    Convert a single 32-bit numeric value of integer type to a
    dots-and-numbers IP address. Returns a string type.

    Example:

    There is only one input value, but it is shown here in 3 bases.

    addr:   0xffff0000 0b11111111111111110000000000000000 4294901760
    return: "255.255.0.0"

    addr:   0x01020304 0b00000001000000100000001100000100 16909060
    return: "1.2.3.4"
    """
    return str(addr>>24 & 0xff) + '.' + str(addr>>16 & 0xff) + '.' + str(addr>>8 & 0xff) + '.' + str(addr & 0xff)


def get_subnet_mask_value(slash:str) -> int:
    """
    Given a subnet mask in slash notation, return the value of the mask
    as a single number of integer type. The input can contain an IP
    address optionally, but that part should be discarded.

    Returns an integer type.

    Example:

    There is only one return value, but it is shown here in 3 bases.

    slash:  "/16"
    return: 0xffff0000 0b11111111111111110000000000000000 4294901760

    slash:  "10.20.30.40/23"
    return: 0xfffffe00 0b11111111111111111111111000000000 4294966784
    """

    # TODO -- write me!
    return int(('1' * int(slash[slash.find('/')+1:])) + ('0' * (32-int(slash[slash.find('/')+1:]))),2)



def ips_same_subnet(ip1:str, ip2:str, slash:str) -> bool:
    """
    Given two dots-and-numbers IP addresses and a subnet mask in slash
    notation, return true if the two IP addresses are on the same
    subnet.

    Returns a boolean.

    FOR FULL CREDIT: this must use your get_subnet_mask_value() and
    ipv4_to_value() functions. Don't do it with pure string
    manipulation.

    This needs to work with any subnet from /1 to /31

    Example:

    ip1:    "10.23.121.17"
    ip2:    "10.23.121.225"
    slash:  "/23"
    return: True
    
    ip1:    "10.23.230.22"
    ip2:    "10.24.121.225"
    slash:  "/16"
    return: False
    """

    # TODO -- write me!
    subnet = get_subnet_mask_value(slash) 
    return (subnet & ipv4_to_value(ip1)) == (subnet & ipv4_to_value(ip2))
    pass

def get_network(ip_value, netmask):
    """
    Return the network portion of an address value as integer type.

    Example:

    ip_value: 0x01020304
    netmask:  0xffffff00
    return:   0x01020300
    """

    # TODO -- write me!
    return ip_value & netmask

def find_router_for_ip(routers, ip):
    """
    Search a dictionary of routers (keyed by router IP) to find which
    router belongs to the same subnet as the given IP.

    Return None if no routers is on the same subnet as the given IP.

    FOR FULL CREDIT: you must do this by calling your ips_same_subnet()
    function.

    Example:

    [Note there will be more data in the routers dictionary than is
    shown here--it can be ignored for this function.]

    routers: {
        "1.2.3.1": {
            "netmask": "/24"
        },
        "1.2.4.1": {
            "netmask": "/24"
        }
    }
    ip: "1.2.3.5"
    return: "1.2.3.1"


    routers: {
        "1.2.3.1": {
            "netmask": "/24"
        },
        "1.2.4.1": {
            "netmask": "/24"
        }
    }
    ip: "1.2.5.6"
    return: None
    """
    for i in routers:
        if ips_same_subnet(i, ip, routers[i]['netmask']):
            return i 
    return None









def dijkstras_shortest_path(routers, src_ip, dest_ip):
    """
    This function takes a dictionary representing the network, a source
    IP, and a destination IP, and returns a list with all the routers
    along the shortest path.

    The source and destination IPs are **not** included in this path.

    Note that the source IP and destination IP will probably not be
    routers! They will be on the same subnet as the router. You'll have
    to search the routers to find the one on the same subnet as the
    source IP. Same for the destination IP. [Hint: make use of your
    find_router_for_ip() function from the last project!]

    The dictionary keys are router IPs, and the values are dictionaries
    with a bunch of information, including the routers that are directly
    connected to the key.

    This partial example shows that router `10.31.98.1` is connected to
    three other routers: `10.34.166.1`, `10.34.194.1`, and `10.34.46.1`:

    {
        "10.34.98.1": {
            "connections": {
                "10.34.166.1": {
                    "netmask": "/24",
                    "interface": "en0",
                    "ad": 70
                },
                "10.34.194.1": {
                    "netmask": "/24",
                    "interface": "en1",
                    "ad": 93
                },
                "10.34.46.1": {
                    "netmask": "/24",
                    "interface": "en2",
                    "ad": 64
                }
            },
            "netmask": "/24",
            "if_count": 3,
            "if_prefix": "en"
        },
        ...

    The "ad" (Administrative Distance) field is the edge weight for that
    connection.

    **Strong recommendation**: make functions to do subtasks within this
    function. Having it all built as a single wall of code is a recipe
    for madness.
    """
    # TODO Write me!
    to_visit,distance,parent = init(routers)
    
    distance[find_router_for_ip(routers,src_ip)] = 0

    while len(to_visit) > 0:
        current_node = find_nearest_node(to_visit, distance)
        to_visit.remove(current_node)
        for near in routers[current_node]["connections"]:
            if near in to_visit:
                computed_distance = routers[current_node]["connections"][near]["ad"] + distance[current_node]
                if computed_distance < distance[near]:
                    distance[near] = computed_distance
                    parent[near] = current_node
    path = []

    current_node = find_router_for_ip(routers,dest_ip)
    source_router = find_router_for_ip(routers,src_ip)
    if current_node == source_router: return []


    path.append(current_node)
    while current_node != source_router:
        current_node = parent[current_node]
        path.append(current_node)
    return path[::-1]

def init(routers)-> tuple :
    to_visit = set()
    distance = {}
    parent = {}
    for node in routers:
        to_visit.add(node)
        distance[node] = math.inf
        parent[node] = None
    return to_visit,distance,parent
    
def find_nearest_node(to_visit: set, distance: dict):
    smallest = math.inf
    for i in to_visit:
        if distance[i] < smallest:
            smallest,current_node = distance[i],i
    return current_node
    
#------------------------------
# DO NOT MODIFY BELOW THIS LINE
#------------------------------
def read_routers(file_name):
    with open(file_name) as fp:
        data = fp.read()
    return json.loads(data)

def find_routes(routers, src_dest_pairs):
    for src_ip, dest_ip in src_dest_pairs:
        path = dijkstras_shortest_path(routers, src_ip, dest_ip)
        print(f"{src_ip:>15s} -> {dest_ip:<15s}  {repr(path)}")

def usage():
    print("usage: dijkstra.py infile.json", file=sys.stderr)

def main(argv):
    try:
        router_file_name = argv[1]
    except:
        usage()
        return 1

    json_data = read_routers(router_file_name)
    
    routers = json_data["routers"]
    routes = json_data["src-dest"]

    find_routes(routers, routes)

if __name__ == "__main__":

    sys.exit(main(sys.argv))
    
