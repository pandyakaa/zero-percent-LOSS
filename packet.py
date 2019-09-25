# Tugas Besar 1
# IF 3130 - Jaringan Komputer
# Zero Percent Loss
# Packet File

class Packet :

    def __init__(self, p_id, p_type, p_seq, p_length, p_checksum, p_data) :
        self.p_id = p_id
        self.p_seq = p_seq
        self.p_length = p_length
        self.p_data = p_data

        # Assign p_type sesuai dengan type packet
        if (p_type == 'DATA') :
            self.p_type = 0x0
        elif (p_type == 'ACK') :
            self.p_type = 0x1
        elif (p_type == 'FIN') :
            self.p_type = 0x2
        elif (p_type == 'FIN-ACK') :
            self.p_type = 0x3
        
        # Assign p_checksum dengan passing parameter ke fungsi checksum
        self.p_checksum = self.checksum()
    
    def printPacket(self) :
        print('Packet ID : ' + str(self.p_id))
        print('Packet Type : ' + str(self.p_type))
        print('Packet sequenceNumber : ' + str(self.p_seq))
        print('Packet Length : ' + str(self.p_length))
        print('Packet Checksum : ' + str(self.p_checksum))
        print('Packet Data : ' + self.p_data)
    
    def checksum(self) :
        return 0x01