import threading
from datetime import datetime

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
                    self._handle_sensor_connect(msg, conn)

                elif msg.header.message_type == "ACTUATOR_CONNECT":
                    self._handle_actuator_connect(msg)

                elif msg.header.message_type == "SENSOR_DATA":
                    self._handle_sensor_data(msg)

                elif msg.header.message_type == "ACTUATOR_COMMAND":
                    self._handle_actuator_command(msg)

                elif msg.header.message_type == "SENSOR_REQUEST":
                    self._handle_sensor_request(msg, conn)

            except ValueError as e:
                print(f"Erro ao processar a mensagem do cliente!")

        conn.close()

    def _handle_sensor_connect(self, message: Message, conn: socket.socket):
        print(f"Sensor: {message.header.device_id} conectado ao gerenciador.")
        self.sensors_data[message.header.device_id] = (None, None)

        response_msg = Message(
            header=Header(
                version_protocol=message.header.version_protocol,
                message_type="SENSOR_RESPONSE",
                device_id=message.header.device_id,
                timestamp=message.header.timestamp,
            ),
            body=Body(value="Conexão bem-sucedida"),
        )
        conn.sendall(response_msg.to_string().encode("utf-8"))

    def _handle_actuator_connect(self, message: Message):
        print(f"Atuador: {message.header.device_id} conectado ao gerenciador.")
        turn_off = "OFF"
        self.actuators_status[message.header.device_id] = turn_off

    def _handle_sensor_data(self, message: Message):
        print(
            f"Transmissão de dados: sensor - {message.header.device_id}, hora: {message.header.timestamp}, dado: {message.body.value}"
        )
        self.sensors_data[message.header.device_id] = (
            message.body.value,
            message.header.timestamp,
        )

    def _handle_actuator_command(self, message: Message):
        self.actuators_status[message.header.device_id] = message.body.value
        print(
            f"Comando enviado pelo atuador - {message.header.device_id} = {message.body.value}."
        )

    def _handle_sensor_request(self, message: Message, conn: socket.socket):
        value, timestamp_str = self.sensors_data.get(
            message.header.device_id, ("EMPTY", "EMPTY")
        )

        if timestamp_str in ["EMPTY", None]:
            timestamp = datetime.now()
        else:
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")

        response_msg = Message(
            header=Header(
                version_protocol=1.0,
                message_type="SENSOR_RESPONSE",
                timestamp=timestamp,
            ),
            body=Body(value=value),
        )
        conn.sendall(response_msg.to_string().encode("utf-8"))


if __name__ == "__main__":
    server = Server()
    server.init()
