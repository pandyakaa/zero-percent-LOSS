# Tugas Besar 1
# IF 3130 - Jaringan Komputer
# Zero Percent Loss
# Sender File

import socket
import sys
import time
from packet import Packet

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
max_data_size = 32768
max_packet_size = 33000 # max_data_size + 2 checksum + 2 length + 2 sequence number + 0.5 type + 0.5 ID + x error

def main() :
    recv_ip = input("Masukkan IP dari address yang dituju : ")
    recv_port = input("Masukkan port dari address yang dituju : ")
    
    file_name = input("Masukkan file yang ingin dikirim : ")

    sock.sendto(file_name.encode(),(recv_ip.encode(),int(recv_port)))
    print('Sending ' + file_name + ' ...')

    f = open(file_name,'r')
    data = f.read(max_data_size)
    idx = 1

    while(data) :
        p = Packet(idx, 'DATA', 3, data)
        if (sock.sendto(p.getDiagram(),(recv_ip.encode(),int(recv_port)))) :
            data = f.read(max_data_size)
            time.sleep(0.02)

    sock.close()
    f.close()

if __name__ == "__main__":
    main()