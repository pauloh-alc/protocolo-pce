import datetime

from protocol_format.body import Body
from protocol_format.header import Header


class Message(Header, Body):
    pass


if __name__ == "__main__":
    message = Message("SENSOR_CONNECT", "sensor01")
    print(message.version_protocol)
    print(message.timestamp)
    print(message.message_type)
