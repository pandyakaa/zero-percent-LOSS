from packet import Packet

def main() :
    p1 = Packet(5,'ACK',3,'pandyakapandyakapandyakapandyakapandyakapandyakapandyakapandyakapandyakapandyaka'.encode())
    p1.printPacket()
    p1.printDiagram()

if __name__ == "__main__":
    main()