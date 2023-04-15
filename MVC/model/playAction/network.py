import socket
import threading


class Network:
    def __init__(self):
        self.boolHasStarted = False
        self.boolHasNewTransmission = False
        self.queueLastTransmissions = ""
        self.strPlayerHit = None
        self.setupUDP()

    def setupUDP(self):
        print("Setting up UDP socket")
        self.udp_IP = "127.0.0.1"  # localhost
        self.udp_PORT_BROAD = 7500
        self.udp_PORT_REC = 7501
        self.udp_socket_Rec = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.udp_socket_Rec.bind((self.udp_IP, self.udp_PORT_REC))
        print("Finished setting up UDP receiving socket: {}:{}".format(self.udp_IP, self.udp_PORT_REC))
        self.udp_socket_Broad = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        print("Finished setting up UDP broadcasting socket: {}:{}".format(self.udp_IP, self.udp_PORT_BROAD))

    def getBroadcastingSocket(self):
        return self.udp_socket_Broad

    def getReceivingSocket(self):
        return self.udp_socket_Rec

    def startThread(self):
        print("Starting network listening thread...")
        self.boolHasStarted = True
        self.thread_UDP = threading.Thread(target=self.methodThread_LoopUDP, args=(), daemon=True)
        self.thread_UDP.start()

    def hasNewTransmission(self):
        return self.boolHasNewTransmission

    def getLastTransmission(self):
        self.boolHasNewTransmission = False
        return self.strLastTransmission

    def methodThread_LoopUDP(self):
        while True:
            self.receiveUDP()
            self.strPlayerHit = self.getPlayerHit_internal(self.strLastTransmission)

    def receiveUDP(self):
        udpData, udpAddress = self.udp_socket_Rec.recvfrom(1024)
        self.strLastTransmission = udpData.decode()
        self.boolHasNewTransmission = True

    def getPlayerHit_internal(self, transmission):
        listDataSplit = transmission.split(":")
        if len(listDataSplit) > 1:
            return listDataSplit[1]
        return None

    def getPlayerHit(self):
        return self.strPlayerHit

    def broadcastUDP(self, strIDPlayerHit):
        udpData = str(strIDPlayerHit).encode()
        self.udp_socket_Broad.sendto(udpData, (self.udp_IP, self.udp_PORT_BROAD))