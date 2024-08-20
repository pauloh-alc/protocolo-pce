from protocol_format.body import Body
from protocol_format.header import Header
from utils.custom_erros import CustomErrorInvalidMessage


class Message(Header, Body):
    def to_string(self):
        if self.message_type in ["SENSOR_DATA", "SENSOR_REQUEST", "SENSOR_RESPONSE"]:
            return f"{self.message_type}|{self.device_id}|{self.timestamp}|{self.value}"
        elif self.message_type == "ACTUATOR_COMMAND":
            return f"{self.message_type}|{self.device_id}|{self.value}"
        elif self.message_type in ["SENSOR_CONNECT", "ACTUATOR_CONNECT"]:
            return f"{self.message_type}|{self.device_id}"
        else:
            raise CustomErrorInvalidMessage(
                f"Tipo de mensagem desconhecido: {self.message_type}"
            )


if __name__ == "__main__":
    message = Message(message_type="SENSOR_CONNECT", device_id="sensor01")
    print(message.version_protocol)
    print(message.timestamp)
    print(message.message_type)

    print(message.to_string())
