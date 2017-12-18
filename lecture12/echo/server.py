import socket
import threading


def handle(client):
    while True:
        data = client.recv(1024)
        if not data:
            client.close()
            return
        print(data)
        client.sendall(data)


def start():
    server = socket.socket()
    server.bind(('127.0.0.1', 5000))
    server.listen(5)
    print('Waiting for connections...')
    while True:
        client, address = server.accept()
        print('Connected', address)
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


start()
