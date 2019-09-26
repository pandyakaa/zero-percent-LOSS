from packet import Packet

def main() :
    p1 = Packet(5,'ACK',3,'pandyakapandyakapandyakapandyakapandyakapandyakapandyakapandyakapandyakapandyaka'.encode())
    p1.printPacket()
    p1.printDiagram()
    print('=====================')
    p_id, p_type, p_seq, p_length, p_data = p1.parseDiagram()
    print(p_id)
    print(p_type)
    print(p_seq)
    print(p_length)
    print(p_data)

if __name__ == "__main__":
    main()