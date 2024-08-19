from base_connect import Base


class Server(Base):
    def __init__(self, host="localhost", port=1456):
        super().__init__(host, port)
