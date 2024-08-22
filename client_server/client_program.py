import time
from datetime import datetime

from base_connect import Base
import socket

from protocol_format.body import Body
from protocol_format.header import Header
from protocol_format.message import Message


class Client(Base):
    def __init__(
        self, host="localhost", port=1024, device_id="sensor[temperatura-interna]"
    ):
        super().__init__(host, port)
        self.device_id = device_id

    def connect_to_manager(self):
        ADDR_FAMILY_IPV4 = socket.AF_INET
        TCP_TYPE_SOCKET = socket.SOCK_STREAM

        client = socket.socket(ADDR_FAMILY_IPV4, TCP_TYPE_SOCKET)
        client.connect((self.host, self.port))

        # SENSOR_CONNECT:
        connect_msg_sensor = Message(
            header=Header(
                version_protocol=1.0,
                message_type="SENSOR_CONNECT",
                device_id="sensor[temperatura_interna]",
                timestamp=datetime.now(),
            ),
            body=Body(value=""),
        )

        # Handshake inicial
        client.sendall(connect_msg_sensor.to_string().encode("utf-8"))
        response = client.recv(1024).decode("utf-8")
        print(f"Resposta do servidor: {response}")

        # ACTUACTOR_CONNECT:
        connect_msg_actuator = Message(
            header=Header(
                version_protocol=1.0,
                message_type="ACTUATOR_CONNECT",
                device_id="actuator[aquecedor]",
                timestamp=datetime.now(),
            ),
            body=Body(value=""),
        )

        client.sendall(connect_msg_actuator.to_string().encode("utf-8"))

        # SENSOR_DATA:
        count = 0
        while True:
            timestamp = datetime.now()
            msg_sensor_data = Message(
                header=Header(
                    version_protocol=1.0,
                    message_type="SENSOR_DATA",
                    device_id=self.device_id,
                    timestamp=timestamp,
                ),
                body=Body(value="12"),
            )
            client.sendall(msg_sensor_data.to_string().encode("utf-8"))
            time.sleep(1)
            count += 1
            if count == 10:
                break

        # ACTUATOR_COMMAND
        msg_actuator_command = Message(
            header=Header(
                version_protocol=1.0,
                message_type="ACTUATOR_COMMAND",
                device_id="actuator[Nível-de-CO2]",
            ),
            body=Body(value="ON"),
        )

        client.sendall(msg_actuator_command.to_string().encode("utf-8"))

        # SENSOR_REQUEST
        msg_sensor_request = Message(
            header=Header(
                version_protocol=1.0,
                message_type="SENSOR_REQUEST",
                device_id="sensor[temperatura_interna]",
                timestamp=datetime.now(),
            ),
            body=Body(value="request"),
        )

        client.sendall(msg_sensor_request.to_string().encode("utf-8"))
        response = client.recv(1024).decode("utf-8")
        print(f"Resposta do servidor: {response}")


if __name__ == "__main__":
    client = Client()
    client.connect_to_manager()
