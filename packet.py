# Tugas Besar 1
# IF 3130 - Jaringan Komputer
# Zero Percent Loss
# Packet File

class Packet :

    # Konstruktor kelas Packet
    def __init__(self, p_id, p_type, p_seq, p_data) :

        # Assign atribut dengan parameter
        self.p_id = p_id
        self.p_seq = p_seq
        self.p_data = p_data
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
        self.diagram = self.makeDiagram()

    # Getter diagram
    def getDiagram(self) :
        return self.diagram
    
    # Getter packet ID
    def getPID(self) :
        return self.p_id
    
    # Getter packet data
    def getData(self) :
        return self.p_data
    
    # Getter untuk sequence number
    def getSeqNum(self) :
        return self.p_seq
    
    # Getter untuk length data
    def getLength(self) :
        return self.p_length
    
    # Getter untuk packet type
    def getType(self) :
        return self.p_type

    # Fungsi isEqual
    def isEq(self,other) :
        return self.p_id == other.p_id

    # Fungsi isLessThan
    def isLT(self,other) :
        return self.p_seq < other.p_length 

    # Fungsi untuk membuat diagram 
    def makeDiagram(self) :
        max_size_packet = 33000
        diagram = bytearray(max_size_packet)

        diagram[0] = (self.p_id & 255) 
        diagram[1] = (self.p_type & 255)
        diagram[2] = (self.p_seq >> 8) # SEQUENCE NUMBER
        diagram[3] = self.p_seq & 255 # SEQUENCE NUMBER
        diagram[4] = (self.p_length >> 8) # LENGTH
        diagram[5] = self.p_length & 255 # LENGTH

        # Assign data to diagram from index 8
        i = 8
        for b in self.p_data :
            diagram[i] = b
            i+=1
        
        # Assign checksum to diagram with index 7 and 8
        sumEven = 0
        sumOdd = 0
        for i in range(8,max_size_packet) :
            if (i%2 == 0) :
                sumEven = sumEven ^ diagram[i]
            else :
                sumOdd = sumOdd ^ diagram[i]
        
        diagram[6] = diagram[0] ^ diagram[2] ^ diagram[4] ^ sumEven
        diagram[7] = diagram[1] ^ diagram[3] ^ diagram[5] ^ sumOdd

        return diagram

    # Fungsi untuk parse ulang diagram
    def parseDiagram(self) :
        max_size_packet = 33000

        # Start parsing
        p_id = self.diagram[0] >> 4 # Parsing for Packet ID

        p_type = self.diagram[1] >> 4 # Parsing for Packet Type
        if p_type == 0 :
            p_type = 'DATA'
        elif p_type == 1 :
            p_type = 'ACK'
        elif p_type == 2 :
            p_type = 'FIN'
        elif p_type == 3 :
            p_type = 'FIN-ACK'

        p_seq = (self.diagram[2] << 8) + self.diagram[3] # Parsing for Packet Sequence
        p_length = (self.diagram[4] << 8) + self.diagram[5] # Parsing for Packet Length
        p_data = bytes(self.diagram[8:max_size_packet+1]) # Parsing for Packet Data
        p_data = p_data.decode().rstrip('\x00') # Parsing for Packet Data

        return p_id,p_type,p_seq,p_length,p_data

    # Fungsi untuk print isi paket
    def printPacket(self) :
        print('Packet ID : ' + str(self.p_id))
        print('Packet Type : ' + str(self.p_type))
        print('Packet sequenceNumber : ' + str(self.p_seq))
        print('Packet Length : ' + str(self.p_length))
        print('Packet Data : ' + self.p_data.decode())
        print('Packet Diagram : ', end='')
        print(self.diagram)

    # Fungsi untuk print paket diagram
    def printDiagram(self) :
        print('ID + Type = ' + str(self.diagram[0]))
        print('Sequence Number 1 = ' + str(self.diagram[1]))
        print('Sequence Number 2 = ' + str(self.diagram[2]))
        print('Length 1 = ' + str(self.diagram[3]))
        print('Length 2 = ' + str(self.diagram[4]))
        print('Checksum 1 = ' + str(self.diagram[5]))
        print('Checksum 2 = ' + str(self.diagram[6]))