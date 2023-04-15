import random
import threading
import time


class trafficGenerator:
    def __init__(self):
        self.boolIsRunning = False

        self.udp_IP = "127.0.0.1"  #localhost
        self.udp_PORT_BROAD = 7501
        self.udp_socket_Broad = None

        self.listIntIDRedTeam = None
        self.listIntIDGreenTeam = None

    def isRunning(self):
        return self.boolIsRunning

    def bindBroadcastingSocket(self, udp_socket_Broad):
        self.udp_socket_Broad = udp_socket_Broad

    def isBroadcastingSocketSet(self):
        return self.udp_socket_Broad is not None

    def startThread(self):
        self.boolIsRunning = True
        self.thread_UDP = threading.Thread(target=self.methodThread_loop, args=(), daemon=True)
        self.thread_UDP.start()

    def stopThread(self):
        self.boolIsRunning = False

    def setIDList(self, listIntIDRedTeam, listIntIDGreenTeam):
        self.listIntIDRedTeam = listIntIDRedTeam
        self.listIntIDGreenTeam = listIntIDGreenTeam

    def isIDListSet(self):
        return (self.listIntIDRedTeam is not None) and (self.listIntIDGreenTeam is not None)

    def getRandomIDRedTeam(self):
        if self.isIDListSet():
            return self.listIntIDRedTeam[random.randint(0, len(self.listIntIDRedTeam) - 1)]

    def getRandomIDGreenTeam(self):
        if self.isIDListSet():
            return self.listIntIDGreenTeam[random.randint(0, len(self.listIntIDGreenTeam) - 1)]

    def broadcastUDP(self, intIDPlayerFrom, intIDPlayerTo):
        strData = str(intIDPlayerFrom) + ":" + str(intIDPlayerTo)
        udpData = strData.encode()
        self.udp_socket_Broad.sendto(udpData, (self.udp_IP, self.udp_PORT_BROAD))

    def methodThread_loop(self):
        if self.isIDListSet() and self.isBroadcastingSocketSet():
            while (self.boolIsRunning):
                intIDRed = self.getRandomIDRedTeam()
                intIDGreen = self.getRandomIDGreenTeam()
                intWhoHitWho = random.randint(0, 1)
                if intWhoHitWho == 0:
                    self.broadcastUDP(intIDRed, intIDGreen)
                else:
                    self.broadcastUDP(intIDGreen, intIDRed)
                time.sleep(random.randint(1, 3))