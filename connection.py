import socket
import struct


class Player:

    def __init__(self, player, name, host='localhost'):
        # 0 if white 1 if black
        self.player = player
        self.name = name
        self.host = host
        if self.player == 1:
            self.port = 5801
        elif self.player == 0:
            self.port = 5800
        else:
            raise Exception('Select white (0) or black (1) player!')
        self.socket = self.connect()
        self.send(self.name)

    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        return sock

    def send(self, msg):
        msg = msg.encode('utf-8')
        self.socket.sendall(len(msg).to_bytes(4, 'big')+msg)

    def read(self):
        # Read message length and unpack it into an integer
        raw_msglen = self.recvall(4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Read the message data
        return self.recvall(msglen)

    def recvall(self, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = bytearray()
        while len(data) < n:
            packet = self.socket.recv(n - len(data))
            #print(data)
            if not packet:
                #print('bo')
                return None
            data.extend(packet)
        return data

