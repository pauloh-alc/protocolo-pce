from datetime import datetime

from base_connect import Base
import socket

from protocol_format.body import Body
from protocol_format.header import Header
from protocol_format.message import Message


class Client(Base):
    def __init__(self, host="localhost", port=1024, device_id="sensor01"):
        super().__init__(host, port)
        self.device_id = device_id

    def connect_to_manager(self):
        ADDR_FAMILY_IPV4 = socket.AF_INET
        TCP_TYPE_SOCKET = socket.SOCK_STREAM

        client = socket.socket(ADDR_FAMILY_IPV4, TCP_TYPE_SOCKET)
        client.connect((self.host, self.port))

        connect_msg = Message(
            header=Header(
                version_protocol=1.0,
                message_type="SENSOR_CONNECT",
                device_id="sensor_01",
                timestamp=datetime.now(),
            ),
            body=Body(value=""),
        )
        # Enviando msg de conexão inicial
        client.sendall(connect_msg.to_string().encode("utf-8"))

        # Recebendo msg após a conexão ser estabelacida
        response = client.recv(1024).decode("utf-8")
        print(f"Resposta do servidor: {response}")


if __name__ == "__main__":
    client = Client()
    client.connect_to_manager()
