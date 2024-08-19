from base_connect import Base


class Client(Base):
    def __init__(self, host="localhost", port=1456, device_id="sensor01"):
        super().__init__(host, port)
        self.device_id = device_id
