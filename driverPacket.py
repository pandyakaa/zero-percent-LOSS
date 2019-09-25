from packet import Packet

def main() :
    p1 = Packet(1,'ACK',3,'pandyaka')
    p1.printPacket()
    p1.printDiagram()

if __name__ == "__main__":
    main()