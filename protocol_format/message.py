from dataclasses import dataclass

from protocol_format.body import Body
from protocol_format.header import Header
from utils.custom_erros import CustomErrorInvalidMessage


@dataclass
class Message:
    header: Header
    body: Body

    def to_string(self):
        if self.header.message_type in [
            "SENSOR_DATA",
            "SENSOR_REQUEST",
            "SENSOR_RESPONSE",
        ]:
            return f"{self.header.message_type}|{self.header.device_id}|{self.header.timestamp}|{self.body.value}"
        elif self.header.message_type == "ACTUATOR_COMMAND":
            return (
                f"{self.header.message_type}|{self.header.device_id}|{self.body.value}"
            )
        elif self.header.message_type in ["SENSOR_CONNECT", "ACTUATOR_CONNECT"]:
            return f"{self.header.message_type}|{self.header.device_id}"
        else:
            raise CustomErrorInvalidMessage(
                f"Tipo de mensagem desconhecido: {self.header.message_type}"
            )

    @staticmethod
    def from_string(string_msg):
        fields = string_msg.split("|")
        message_type = fields[0]
        device_id = fields[1]

        if message_type in ["SENSOR_DATA", "SENSOR_REQUEST", "SENSOR_RESPONSE"]:
            timestamp = fields[2]
            value = fields[3]
            return Message(
                Header(
                    version_protocol=1.0, message_type=message_type, timestamp=timestamp
                ),
                Body(value=value),
            )
        elif message_type == "ACTUATOR_COMMAND":
            value = fields[2]
            return Message(
                Header(
                    version_protocol=1.0, message_type=message_type, device_id=device_id
                ),
                Body(value=value),
            )
        elif message_type in ["SENSOR_CONNECT", "ACTUATOR_CONNECT"]:
            return Message(
                Header(
                    version_protocol=1.0, message_type=message_type, device_id=device_id
                )
            )
        else:
            raise CustomErrorInvalidMessage(
                f"Tipo de mensagem desconhecido: {message_type}"
            )


if __name__ == "__main__":
    message = Message(
        Header(message_type="SENSOR_CONNECT", device_id="sensor01"), Body()
    )
    print(message.header.message_type)
    print(message.header.version_protocol)
    print(message.header.message_type)
    print(message.body.value)

    print(message.to_string())
    print(Message.from_string("ACTUATOR_COMMAND|actuator_01|ON"))
