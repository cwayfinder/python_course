import collections
import socket
import threading

from lecture12.tic_tac_toe.field import Field


def gameloop(player1, player2):
    field = Field()
    players = collections.deque([player1, player2])
    while not field.game_over():
        players[0].sendall((str(field) + '\n\r').encode())
        x, y = players[0].recv(1024).strip().split()
        field.set_symbol(int(x), int(y), 'X')
        players.rotate()
    player1.close()
    player2.close()


ADDRESS = ('127.0.0.1', 5003)

server = socket.socket()
server.bind(ADDRESS)
server.listen(5)

player1 = None

while True:
    client, _ = server.accept()
    if player1 is None:
        player1 = client
        print('Waiting for an opponent...')
    else:
        print('Second player has joined')
        player2 = client
        thread = threading.Thread(target=gameloop, args=(player1, player2))
        thread.start()
        player1 = None
