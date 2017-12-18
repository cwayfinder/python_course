import socket
import time


server = socket.socket()
server.connect(('127.0.0.1', 5001))

try:
    while True:
        server.sendall(b'Hello')
        data = server.recv(1024)
        print(data)
        time.sleep(2)
except KeyboardInterrupt:
    pass
finally:
    server.close()

server.close()
