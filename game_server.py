import socket
import _thread
import time
from client import Client
from game_data import GameData
from lobby import Lobby


class GameServer:
    # GameServer Attributes
    localIP = '0.0.0.0'
    localPort = 20001
    bufferSize = 1024
    shouldListen = True
    lobbies = []

    # Create datagram socket
    serverSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def __init__(self):
        pass

    def start(self):
        print("Starting Game Server")

        # Bind to ip and port
        self.serverSocket.bind((self.localIP, self.localPort))
        # Start Listening Thread
        _thread.start_new_thread(self.listen, ())
        print("UDP Server up and listening")

    def listen(self):
        # Listen for incoming datagrams
        while self.shouldListen:
            bytesAddressPair = self.serverSocket.recvfrom(self.bufferSize)
            message = bytesAddressPair[0].decode().strip()
            address = bytesAddressPair[1]
            # Parse incoming message
            client = Client(address)
            self.parseMessage(message, client)

    def parseMessage(self, msg, client):
        print("parsing message: {} from {}".format(msg, client.address))
        if msg == "create_lobby":
            lobbyID = len(self.lobbies)
            print("{} created new lobby: {}".format(client.address, lobbyID))
            self.lobbies.append(Lobby(lobbyID, GameData(), client, self.serverSocket))
            self.sendMessage("Lobby created", client)
            return None
        if msg.__contains__("join_lobby_"):
            lobbyID = int(msg[msg.index("lobby_")+6:])
            if len(self.lobbies) > lobbyID:
                lobby = self.lobbies[lobbyID]
                lobby.join(client)
                self.sendMessage("Lobby joined", client)
            else:
                self.sendMessage("Lobby doesn't exist", client)
            return None
        if msg.__contains__("lID_"):
            # lobby specific package and parse lobbyID first
            tmp = msg[msg.index("lID_")+4:]
            lobbyID = int(tmp[:tmp.index("_")])
            if len(self.lobbies) > lobbyID:
                # redirect package to responsible lobby
                self.lobbies[lobbyID].receivePackage(tmp[tmp.index("_")+1:], client)


    def sendMessage(self, msg, client):
        # Encode msg to byte obj
        msg = msg.encode()
        address = client.address
        # send message to client
        self.serverSocket.sendto(msg, address)