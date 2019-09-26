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

# Fungsi untuk checkSum
def checkSum(list):

   checkOdd = 0
   checkEven = 0
   for i in range(8,max_packet_size) :
      if (i%2 == 0) :
         checkEven = checkEven ^ list[i]
      else :
         checkOdd = checkOdd ^ list[i]
   
   checkOdd = checkOdd ^ list[1] + list[3] + list[5]
   checkEven = checkEven ^ list[0] + list[2] + list[4]

   return (checkEven, checkOdd == list[6], list[7])

# Fungsi receiveData()
def main():
   
   # Create UDP socket
   sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   port = bindParam()

   sock.bind((localIP,port))


   while True :
      #checker = sock.recvfrom(max_packet_size)
      #print (checker)
      data, addr = sock.recvfrom(max_packet_size)
      seqVal = (data[2] << 8) + data[3]

      if (seqVal == 1) :
         filename = bytes(data[8:max_packet_size]).decode().rstrip('\00') + '-result.txt'
         print('Nama file ' + filename)
         f = open(filename,'wb')
      else :
         f.write(bytes(data[8:max_packet_size]).rstrip(b'\x00'))
         print('File ke ' + str(data[0]))
         print('Paket ke ' + str(seqVal-1))

      if checkSum(data) :
         if data[1] == 0 :
            ack = Packet(data[0], 'ACK', seqVal, ''.encode())
            sock.sendto(ack.getDiagram(),addr)
         elif data[1] == 2 :
            ack = Packet(data[0], 'FIN-ACK', seqVal, ''.encode())
            sock.sendto(ack.getDiagram(),addr)
            f.close()
            sock.close()
            break

if __name__ == "__main__":
    main()
