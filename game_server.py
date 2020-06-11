#!/usr/bin/python3
import socket
import asyncio
import threading
import _thread
import time
from client import Client
from game_data import GameData
from broadcaster import Broadcaster

localIP = '0.0.0.0'
localPort = 20001
bufferSize = 1024
tickRate = 10

# Create datagram socket
serverSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

shouldListen = True
shouldBroadcast = True

gameData = GameData()


def main():
    # Bind to address and ip
    serverSocket.bind((localIP, localPort))
    gameData.serverSocket = serverSocket
    print("UDP Server up and listening")

    #listen()
   # broadcaster = Broadcaster(1, "Broadcast")
    #broadcaster.gameData = gameData
   # broadcaster.start()
    _thread.start_new_thread(listen, ())
    _thread.start_new_thread(broadcastTick(), ())
    while 1:
        pass
    # Create Tick Timer
    # tickLoop = asyncio.get_event_loop()
    # tickListenTask = tickLoop.create_task(tickListen())
    # tickBroadcastTask = tickLoop.create_task(tickBroadcast())

    # try:
    # tickLoop.run_until_complete(tickListenTask)
    # tickLoop.run_until_complete(tickBroadcastTask)


# except asyncio.CancelledError:
# pass


def listen():
    # Listen for incoming datagrams
    while shouldListen:
        bytesAddressPair = serverSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0].decode().strip()
        address = bytesAddressPair[1]
        parseMessage(message, address)

        # Sending reply to client

        # UDPServerSocket.sendto(bytesToSend, address)


def parseMessage(msg, address):
    print("parsing message: {}".format(msg))
    if msg == "connect" and address not in gameData.clients:
        print ("client {} connected".format(address))
        gameData.clients.append(Client(address))


# async def tickListen():
#     print("Listening")
#     while True:
#         listen()
#         await asyncio.sleep(0.1)
#
#
# async def tickBroadcast():
#     print("fasfa")
#     while True:
#         broadcast("test")
#         await asyncio.sleep(0.1)

def broadcastTick():
    msg = "Alex"
    while shouldBroadcast:
        broadcast(msg)
        time.sleep(1.0 / tickRate)


def broadcast(msg):
    print ("broadcasting: {}".format(msg))
    msg = msg.encode()
    for client in gameData.clients:
        address = client.address
        serverSocket.sendto(msg, address)


if __name__ == "__main__":
    main()
