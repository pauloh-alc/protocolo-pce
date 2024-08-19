from base_connect import Base
import socket


class Server(Base):
    def __init__(self, host="localhost", port=5000):
        super().__init__(host, port)

    def init(self):
        ADDR_FAMILY_IPV4 = socket.AF_INET
        TCP_TYPE_SOCKET = socket.SOCK_STREAM

        server = socket.socket(ADDR_FAMILY_IPV4, TCP_TYPE_SOCKET)
        server.bind((self.host, self.port))
        server.listen()

        print(
            f"Servidor iniciado [porta: {self.port}]. Aguardando conexão com cliente ..."
        )
