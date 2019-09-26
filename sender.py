# Tugas Besar 1
# IF 3130 - Jaringan Komputer
# Zero Percent Loss
# Sender File

import socket
import sys
import time
from packet import Packet

# Constant variable
max_data_size = 32768
# max_data_size + 2 checksum + 2 length + 2 sequence number + 0.5 type + 0.5 ID + x error
max_packet_size = 33000

# Fungsi input IP, port dan filename

def bindParam():

    recv_ip = input("Masukkan IP dari address yang dituju : ")
    recv_port = input("Masukkan port dari address yang dituju : ")
    file_name = input("Masukkan file yang ingin dikirim : ")

    # Cast recv_ip to bytes
    recv_ip = recv_ip.encode()
    # Cast recv_port to integer
    recv_port = int(recv_port)

    file_names = file_name.split("/")

    for x in range(len(file_names)):
        file_names[x] = file_names[x].encode()

    print (len(file_names))

    # Cast file_name  to bytes
    #file_names = file_name.encode()

    return recv_ip, recv_port, file_names

# Fungsi untuk parse ulang diagram
def parseDiagram(list):

    # Start parsing
    p_id = list[0] >> 4  # Parsing for Packet ID

    p_type = list[1] >> 4  # Parsing for Packet Type
    if p_type == 0:
        p_type = 'DATA'
    elif p_type == 1:
        p_type = 'ACK'
    elif p_type == 2:
        p_type = 'FIN'
    elif p_type == 3:
        p_type = 'FIN-ACK'

    p_seq = (list[2] << 8) + list[3]  # Parsing for Packet Sequence
    p_length = (list[4] << 8) + list[5]  # Parsing for Packet Length
    p_data = bytes(list[8:max_packet_size+1])  # Parsing for Packet Data
    p_data = p_data.decode().rstrip('\x00')  # Parsing for Packet Data
    p_checksum = (list[6] << 8) + list[7]

    return p_id, p_type, p_seq, p_length, p_data, p_checksum

# Fungsi sendData
def sendData():

    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Call bindParam() function
    recv_ip, recv_port, file_name = bindParam()
    #file_names = file_name.split("/")

    # Send file_name to receiver
    # TODO : create progress bar
    for x in range(len(file_name)):
        sock.sendto(file_name[x], (recv_ip, recv_port))
        file_name[x] = file_name[x].decode()
        print('Sending ' + file_name[x] + ' ...')

        # Read file and send the content
        with open(file_name[x], 'rb') as f:
            data = f.read(max_data_size)
            idx = 1
            seq = 1

            while(data):
                p = Packet(idx, 'DATA', seq, data)
                if (sock.sendto(p.getDiagram(), (recv_ip, recv_port))):
                    data = f.read(max_data_size)
                    time.sleep(0.02)
                datarcv, addr = sock.recvfrom(max_data_size+1000)
                if datarcv:
                    p_id, p_type, p_seq, p_length, p_data, p_checksum = parseDiagram(
                        datarcv)
                    print('ACK from packet ' + str(p_id) + ' Received')
                seq += 1

        
        f.close()
    sock.close()


def main():
    sendData()


if __name__ == "__main__":
    main()
