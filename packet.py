# Tugas Besar 1
# IF 3130 - Jaringan Komputer
# Zero Percent Loss
# Packet File

class Packet :

    def __init__(self, p_id, p_type, p_seq, p_data) :
        self.p_id = p_id
        self.p_seq = p_seq
        self.p_data = p_data.encode()
        self.p_length = len(p_data)

        # Assign p_type sesuai dengan type packet
        if (p_type == 'DATA') :
            self.p_type = 0x0
        elif (p_type == 'ACK') :
            self.p_type = 0x1
        elif (p_type == 'FIN') :
            self.p_type = 0x2
        elif (p_type == 'FIN-ACK') :
            self.p_type = 0x3
        
        # Parse input ke dalam diagram
        self.diagram = self.parseAndChecksum()
    
    def printPacket(self) :
        print('Packet ID : ' + str(self.p_id))
        print('Packet Type : ' + str(self.p_type))
        print('Packet sequenceNumber : ' + str(self.p_seq))
        print('Packet Length : ' + str(self.p_length))
        print('Packet Data : ' + self.p_data.decode())

    def printDiagram(self) :
        print(self.diagram)
    
    def parseAndChecksum(self) :
        max_size_packet = 33000
        diagram = bytearray(max_size_packet)

        diagram[0] = (self.p_type << 4) & 15 + self.p_id # TYPE dan ID
        diagram[1] = (self.p_seq >> 8 ) & 255 # SEQUENCE NUMBER
        diagram[2] = self.p_seq & 255 # SEQUENCE NUMBER
        diagram[3] = (self.p_length >> 8) & 255 # CHECKSUM
        diagram[4] = self.p_length & 255 # CHECKSUM

        i = 7
        for b in self.p_data :
            diagram[i] = b
            i+=1
        
        sumEven = 0
        sumOdd = 0
        for i in range(7,max_size_packet) :
            if (i%2 == 0) :
                sumEven = sumEven ^ diagram[i]
            else :
                sumOdd = sumOdd ^ diagram[i]
        
        diagram[5] = diagram[1] ^ diagram[3] ^ sumEven
        diagram[6] = diagram[0] ^ diagram[2] ^ diagram[4] ^ sumOdd

        return diagram

    def getDiagram(self) :
        return self.diagram