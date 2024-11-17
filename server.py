import socket
import threading

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []


def sendall(message, nosend):

    for client in clients:
        if client != nosend:
            client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            sendall(message, client)
        except:

            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            sendall('{} left!'.format(nickname).encode('ascii'), client)
            nicknames.remove(nickname)
            break

def coms():
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        client.send('WHOAREYOU'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        sendall("{} joined!".format(nickname).encode('ascii'), client)
        client.send('Connected to server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

coms()