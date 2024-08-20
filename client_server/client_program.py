from base_connect import Base
import socket


class Client(Base):
    def __init__(self, host="localhost", port=5000, device_id="sensor01"):
        super().__init__(host, port)
        self.device_id = device_id

    def connect_to_manager(self):
        ADDR_FAMILY_IPV4 = socket.AF_INET
        TCP_TYPE_SOCKET = socket.SOCK_STREAM

        client = socket.socket(ADDR_FAMILY_IPV4, TCP_TYPE_SOCKET)
        client.connect((self.host, self.port))

        client.sendall(str.encode("Hello World"))
        data = client.recv(1024)
        print("Mensagem ecoada:", data.decode())


if __name__ == "__main__":
    client = Client()
    client.connect_to_manager()
