from packet import Packet

def main() :
    p1 = Packet(1,'ACK',3,10,3,'asdasd')
    p1.printPacket()

if __name__ == "__main__":
    main()