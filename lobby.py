import _thread
import time
from client import Client
from game_data import GameData


class Lobby:
    # Lobby Attributes
    shouldBroadcast = False
    tickRate = 10

    def __init__(self, id, gameData, creator, serverSocket):
        self.id = id
        self.gameData = gameData
        self.creator = creator
        self.clients = []
        self.clients.append(creator)
        self.serverSocket = serverSocket
        print("Lobby ID: {}".format(id))

    def join(self, client):
        self.broadcast("{} joined the lobby".format(client.address))
        self.clients.append(client)

    def receivePackage(self, package, client):
        if package == 'startBroadcast':
            self.startBroadcaster()
            return None

    def startBroadcaster(self):
        if not self.shouldBroadcast:
            print("Starting Broadcaster for Lobby {}".format(self.id))
            self.shouldBroadcast = True
            _thread.start_new_thread(self.broadcastTick, ())

    def broadcastTick(self):
        msg = self.gameData.value
        while self.shouldBroadcast:
            self.broadcast(msg)
            time.sleep(1.0 / self.tickRate)

    def broadcast(self, msg):
        print ("broadcasting: {}".format(msg))
        for client in self.clients:
            self.sendMessage(msg, client)

    def sendMessage(self, msg, client):
        # Encode msg to byte obj
        msg = msg.encode()
        address = client.address
        # send message to client
        self.serverSocket.sendto(msg, address)
