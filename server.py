from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

IP = '0.0.0.0'
PORT = 12345
FORMAT = "utf-8"
HEADER = 128
MAX_CONNECTIONS = 2


class Server:
    def __init__(self, ip, port, encode_format, header, max_connections):
        # Connection Data
        self.ip = ip
        self.port = port
        self.addr = (ip, port)

        # Socket Data
        self.format = encode_format
        self.header = header
        self.max_connections = max_connections

        # Game Data
        self.clients = []

        # Configure Socket
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.run = True
        self.started = False

        # Start Server
        self.start()

    def start(self):
        self.socket.bind(self.addr)
        print("\n[STARTING] Server is starting...")

        self.socket.listen(self.max_connections)
        print(f"[LISTENING] Server is listening on {self.addr}")

        while self.run:
            client_socket, client_address = self.socket.accept()
            self.clients.append(client_socket)
            print(f"\n[NEW CONNECTION] Connection has been established with {client_address}\n")

            thread = Thread(target=self.handle_connection, args=(client_socket, client_address))
            try:
                thread.start()
            except Exception as e:
                break

        else:
            print("\n[ERROR] Server is shutting down Due to an error...\n")

        self.socket.close()
        print("\n[SHUTTING DOWN] Server is shut down.\n")

    @property
    def client_count(self):
        return len(self.clients)

    def get_client_side(self):
        if self.client_count == 1:
            return "left"
        elif self.client_count == 2:
            return "right"

    @property
    def left_client(self):
        return self.clients[0]

    @property
    def right_client(self):
        return self.clients[1]

    def receive_message(self, client_socket):
        msg_length = client_socket.recv(self.header).decode(self.format)
        if msg_length:
            msg_length = int(msg_length)
            data = client_socket.recv(msg_length).decode(self.format)
            return data
        return None

    def send_message(self, client_socket, msg):
        message = msg.encode(self.format)
        msg_length = len(message)
        send_length = str(msg_length).zfill(self.header).encode()
        client_socket.send(send_length)
        client_socket.send(message)

    def disconnect_client(self, client_socket, client_address):
        client_socket.close()
        self.clients.pop(client_socket)
        print(f"\n[DISCONNECTION] Connection has been terminated with {client_address}\n")

    def handle_connection(self, client_socket, client_address):
        # Send client his side
        client_side = self.get_client_side()
        print(f"[SIDE] Client side is {client_side}")

        while self.client_count < 2:
            pass

        print("[SENT SIDE] Sent client side.")
        msg = f"side:{client_side}"
        self.send_message(client_socket, msg)

        while self.run:
            # Receiving
            move = self.receive_message(client_socket)

            if move == "won":
                self.run = False

            if client_side == "left":
                message = move.replace("left", "moves", 1)
                self.send_message(self.right_client, message)

            elif client_side == "right":
                message = move.replace("right", "moves", 1)
                self.send_message(self.left_client, message)

        self.disconnect_client(client_socket, client_address)


if __name__ == "__main__":
    Server(IP, PORT, FORMAT, HEADER, MAX_CONNECTIONS)
