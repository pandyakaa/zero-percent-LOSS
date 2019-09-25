# Tugas Besar 1
# IF 3130 - Jaringan Komputer
# Zero Percent Loss
# Receiver File

import socket
import sys
import select

localIP = 'localhost'
timeout = 3
max_packet_size = 32780

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def main() :
   port = int(input("Masukkan port yang akan di-bind : "))
   sock.bind((localIP,port))

   while True :
      f = open('result.txt','w')

      data,addr = sock.recvfrom(max_packet_size)
      if data :
         print('File name : ' + data.decode())
         file_name = data.strip()

      while True:
        ready = select.select([sock], [], [], timeout)
        if ready[0]:
            data, addr = sock.recvfrom(max_packet_size)
            f.write(data.decode())
        else:
            print(file_name.decode() + ' Finish')
            break
         
if __name__ == "__main__":
   main()