from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import select

from globals import player_moves, opponent_moves, current_move

# Socket params
IP = "127.0.0.1"
PORT = 12345
ADDR = (IP, PORT)
FORMAT = "utf-8"
HEADER = 128


class Communication:
    def __init__(self, ip=IP, port=PORT, encode_format=FORMAT, header=HEADER):
        # Connection Data
        self.ip = ip
        self.port = port
        self.addr = (ip, port)

        # Socket Data
        self.format = encode_format
        self.header = header

        # Game Data
        self.side = None

        # Configure Socket
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.run = True

    def start(self):
        print("\n[CONNECTING] Connecting to server.")
        self.socket.connect(self.addr)

    def play(self):
        thread = Thread(target=self.send_player_moves())
        thread.start()

        while self.run:
            op_moves = tuple(self.receive_message().removeprefix("moves:(").removesuffix(")").split(","))
            opponent_moves.append(op_moves)

        self.socket.close()

    def get_side(self):
        while True:
            ready_fds, _, error_fds = select.select([self.socket], [], [], 1)
            if ready_fds:
                break
            # print("not ready")

        self.side = self.receive_message().removeprefix("side:")
        # print(self.side)
        return self.side

    def send_player_moves(self):
        while self.run:
            if len(player_moves):
                moves = player_moves.pop(0)
                message = self.create_moves_message(moves)
                self.send_message(message)

    def create_moves_message(self, moves):
        if moves == "won":
            return moves

        message = f"{self.side}:("
        for i, move in enumerate(moves):
            message += str(move)
            if i < len(moves) - 1:
                message += ","
        message += ")"
        return message

    def receive_message(self):
        msg_length = self.socket.recv(self.header).decode(self.format)
        if msg_length:
            msg_length = int(msg_length)
            data = self.socket.recv(msg_length).decode(self.format)
            return data
        return None

    def send_message(self, msg):
        message = msg.encode(self.format)
        msg_length = len(message)
        send_length = str(msg_length).zfill(self.header).encode()
        self.socket.send(send_length)
        self.socket.send(message)
