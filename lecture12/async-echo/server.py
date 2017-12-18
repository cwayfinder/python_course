import socket
import select


def handle(client):
    data = client.recv(1024)
    if not data:
        client.close()
        return
    print(data)
    client.sendall(data)


def start():
    server = socket.socket()
    server.bind(('127.0.0.1', 5001))
    server.setblocking(False)
    server.listen(5)
    connections = [server]
    print('Waiting for connections...')
    while True:
        reading_sockets, _, _ = select.select(connections, [], [])
        for reading_socket in reading_sockets:
            if reading_socket == server:
                client, address = server.accept()
                print('Connected', address)
                connections.append(client)
            else:
                handle(reading_socket)


start()
