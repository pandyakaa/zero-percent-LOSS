# Tugas Besar 1
# IF 3130 - Jaringan Komputer
# Zero Percent Loss
# Receiver File

import socket
import sys
import select
from packet import Packet

# Constant variable
localIP = 'localhost'
timeout = 3
max_packet_size = 33000

# Fungsi bindParam()
def bindParam():
    port = input('Masukkan port yang akan di-bind : ')

    # Cast port to integer
    port = int(port)

    return port

# Fungsi untuk parse ulang diagram
def parseDiagram(list):

    # Start parsing
    p_id = list[0] >> 4  # Parsing for Packet ID

    p_type = list[1] >> 4  # Parsing for Packet Type

    p_seq = (list[2] << 8) + list[3]  # Parsing for Packet Sequence
    p_length = (list[4] << 8) + list[5]  # Parsing for Packet Length
    p_data = list[8:max_packet_size]  # Parsing for Packet Data
    p_data = p_data.decode().rstrip('\x00')
    p_data = p_data.encode()
    p_cheksum = (list[6] << 8) + list[7]

    return p_id, p_type, p_seq, p_length, p_data, p_cheksum

# Fungsi untuk mencari checksum
def getChecksum(p_id, p_type, p_seq, p_length, p_data):
    diagram = bytearray(max_packet_size)

    diagram[0] = ((p_id << 4) & 255)
    diagram[1] = ((p_type << 4) & 255)
    diagram[2] = (p_seq >> 8)  # SEQUENCE NUMBER
    diagram[3] = p_seq & 255  # SEQUENCE NUMBER
    diagram[4] = (p_length >> 8)  # LENGTH
    diagram[5] = p_length & 255  # LENGTH

    # Assign data to diagram from index 8
    i = 8
    for b in p_data:
        diagram[i] = b
        i += 1

    # Assign checksum to diagram with index 7 and 8
    sumEven = 0
    sumOdd = 0
    for i in range(8, max_packet_size):
        if (i % 2 == 0):
            sumEven = sumEven ^ diagram[i]
        else:
            sumOdd = sumOdd ^ diagram[i]

    diagram[6] = diagram[0] ^ diagram[2] ^ diagram[4] ^ sumEven
    diagram[7] = diagram[1] ^ diagram[3] ^ diagram[5] ^ sumOdd

    checksum = (diagram[6] << 8) + diagram[7]
    return checksum

# Fungsi receiveData()
def receiveData():

    res = [[] for i in range(5)]
    filename = []

    # Create UDP Socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Call bindParam() function
    port = bindParam()

    # Binding sock with localIP and port
    sock.bind((localIP, port))

    # Receive data

    # Receive filename first
    while True:
        data, addr = sock.recvfrom(max_packet_size)
        if data:
            print('File name : ' + data.decode())
            file_name = data.decode().strip()
            filename.append(file_name)

        # Receive the data
        while True:
            ready = select.select([sock], [], [], timeout)
            if ready[0]:
                data, addr = sock.recvfrom(max_packet_size)
                if data:
                    p_id, p_type, p_seq, p_length, p_data, p_checksum = parseDiagram(data)
                    if (p_checksum == getChecksum(p_id, p_type, p_seq, p_length, p_data)):
                        p = Packet(p_id, 'ACK', p_seq, ''.encode())
                        sock.sendto(p.getDiagram(), addr)
                        print('ACK for packet ' + str(p_id) + ' sent')
                        res[p_id].append(p_data)
                    else:
                        print('checksum not valid')
            else:
                #print(file_name + ' finished')
                break
        break

    return res, filename


def main():
    res, filename = receiveData()
    with open('result.txt', 'wb') as f:
        for i in res:
            for j in i:
               f.write(j)


if __name__ == "__main__":
    main()
