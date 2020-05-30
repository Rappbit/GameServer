import socket
import asyncio
from client import Client
from game_data import GameData

localIP = '0.0.0.0'
localPort = 20001
bufferSize = 1024

# Create datagram socket
serverSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

shouldListen = True
shouldBroadcast = True

clients = []


def main():
    # Bind to address and ip
    serverSocket.bind((localIP, localPort))

    print("UDP Server up and listening")

    # Create Tick Timer
    tickLoop = asyncio.get_event_loop()
    tickListenTask = tickLoop.create_task(tickListen())
    tickBroadcastTask = tickLoop.create_task(tickBroadcast())

    try:
        tickLoop.run_until_complete(tickListenTask)
        tickLoop.run_until_complete(tickBroadcastTask)
    except asyncio.CancelledError:
        pass


def listen():

    # Listen for incoming datagrams
    if shouldListen:
        bytesAddressPair = serverSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0].decode().strip()
        address = bytesAddressPair[1]
        parseMessage(message, address)

        # Sending reply to client

        # UDPServerSocket.sendto(bytesToSend, address)


def parseMessage(msg, address):
    if msg == "connect" and address not in clients:
        print ("client {} connected".format(address))
        clients.append(Client(address))


async def tickListen():
    print("Listening")
    while True:
        listen()
        await asyncio.sleep(0.1)


async def tickBroadcast():
    print("fasfa")
    while True:
        broadcast("test")
        await asyncio.sleep(0.1)


def broadcast(msg):
    print("broadcast")
    if shouldBroadcast:
        msg = msg.encode()
        for client in clients:
            address = client.address
            serverSocket.sendto(msg, address)


if __name__ == "__main__":
    main()
