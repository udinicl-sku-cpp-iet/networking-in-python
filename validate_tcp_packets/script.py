def zero_checksum(filename:str):
    with open(filename,"rb") as f:
        data = f.read()
    return len(data), data[16:18], data[:16] + b'\x00\x00' + data[18:]

def ip_to_bytes(filename:str):
    buf = b''
    with open(filename,"r") as f:
        for ip in f.read().split():
            for chunk in ip.split('.'):
                buf += int(chunk).to_bytes()
    return buf

def ip_header(tcp_length, filename):
    buf =  ip_to_bytes(filename)
    buf += b'\x00'
    buf += b'\x06'
    if tcp_length <= 255 :
        buf += b'\x00'
    buf += tcp_length.to_bytes()
    return buf
def checksum(buf:bytes):
    if len(buf) % 2 == 1:
        buf += b'\x00'
    offset = 0
    total  = 0
    while offset < len(buf):
        word = int.from_bytes(buf[offset:offset + 2], "big")
        total += word
        total = (total & 0xffff) + (total >> 16)
        offset += 2   # Go to the next 2-byte value
    return (~total) & 0xffff



for i in range(10):
    tcp_length, original_checksum, zero_checksum_header = zero_checksum(f"tcp_data_{i}.dat")
    zero_checksum_header = ip_header(tcp_length, f"tcp_addrs_{i}.txt") + zero_checksum_header
    if int.from_bytes(original_checksum,"big") == checksum(zero_checksum_header):
        print("True")
    else:
        print("False")        
