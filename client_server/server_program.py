import threading

from client_server.base_connect import Base
import socket

from protocol_format.body import Body
from protocol_format.header import Header
from protocol_format.message import Message


class Server(Base):
    def __init__(self, host="localhost", port=1024):
        super().__init__(host, port)
        self.sensors_data = {}
        self.actuators_status = {}

    def init(self):
        ADDR_FAMILY_IPV4 = socket.AF_INET
        TCP_TYPE_SOCKET = socket.SOCK_STREAM

        server = socket.socket(ADDR_FAMILY_IPV4, TCP_TYPE_SOCKET)
        server.bind((self.host, self.port))
        server.listen()

        print(
            f"Servidor iniciado [porta: {self.port}]. Aguardando conexão com cliente ..."
        )

        while True:
            conn, adds = server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, adds))
            thread.start()

    def handle_client(self, conn, adds):
        print(f"Conectado em {adds}")
        while True:
            data = conn.recv(1024).decode("utf-8")
            if not data:
                break

            try:
                msg = Message.from_string(data)
                if msg.header.message_type == "SENSOR_CONNECT":
                    print(f"Sensor: {msg.header.device_id} conectado ao gerenciador.")
                    self.sensors_data[msg.header.device_id] = None

                    response_msg = Message(
                        header=Header(
                            version_protocol=msg.header.version_protocol,
                            message_type="SENSOR_RESPONSE",
                            device_id=msg.header.device_id,
                            timestamp=msg.header.timestamp,
                        ),
                        body=Body(value="Conexão bem-sucedida"),
                    )
                    conn.sendall(response_msg.to_string().encode("utf-8"))

                elif msg.header.message_type == "ACTUATOR_CONNECT":
                    print(f"Atuador: {msg.header.device_id} conectado ao gerenciado")
                    turn_off = "OFF"
                    self.actuators_status[msg.header.device_id] = turn_off

            except ValueError as e:
                print(f"Erro ao processar a mensagem do cliente!")

        conn.close()


if __name__ == "__main__":
    server = Server()
    server.init()
