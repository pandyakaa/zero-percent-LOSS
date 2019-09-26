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
def bindParam() :
   port = input('Masukkan port yang akan di-bind : ')

   #Cast port to integer
   port = int(port)

   return port

# Fungsi untuk parse ulang diagram
def parseDiagram(list) :
   max_size_packet = 33000

   # Start parsing
   p_id = list[0] >> 4 # Parsing for Packet ID

   p_type = list[1] >> 4 # Parsing for Packet Type
   if p_type == 0 :
      p_type = 'DATA'
   elif p_type == 1 :
      p_type = 'ACK'
   elif p_type == 2 :
      p_type = 'FIN'
   elif p_type == 3 :
      p_type = 'FIN-ACK'

   p_seq = (list[2] << 8) + list[3] # Parsing for Packet Sequence
   p_length = (list[4] << 8) + list[5] # Parsing for Packet Length
   p_data = bytes(list[8:max_size_packet+1]) # Parsing for Packet Data
   p_data = p_data.decode().rstrip('\x00') # Parsing for Packet Data

   return p_id,p_type,p_seq,p_length,p_data

# Fungsi receiveData()
def receiveData() :

   # Create UDP Socket
   sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

   # Call bindParam() function
   port = bindParam()

   # Binding sock with localIP and port
   sock.bind((localIP,port))

   # Receive data and write file
   with open('result.out','wb') :

      # Receive filename first
      while True :
         data, addr = sock.recvfrom(max_packet_size)
         #if data : 
            #print('File name : ' + data.decode())
            #file_name = data.decode().strip()
         
         # Receive the data
         while True :
            ready = select.select([sock],[],[],timeout)
            if ready[0] :
               data, addr = sock.recvfrom(max_packet_size)
               p_id, p_type, p_seq, p_length, p_data = parseDiagram(data)
               p = Packet(p_id,'ACK',p_seq,'asd'.encode())
               sock.sendto(p.getDiagram(),addr)
               print('ACK for packet ' + str(p_id) + ' sent')
            else :
               #print(file_name + ' finished')
               break

def main() :
   receiveData()

if __name__ == "__main__":
   main()