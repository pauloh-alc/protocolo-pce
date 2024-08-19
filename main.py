from base_connect import Base
from client_program import Client
from server_program import Server

if __name__ == "__main__":
    print("Hello World")
    base_1 = Base()
    base_2 = Base("localhost", 1234)
    base_3 = Base(host="localhost", port=1234)

    print(base_1.host)
    print(base_2.host)
    print(base_3.host)

    print(base_1.port)
    print(base_2.port)
    print(base_3.port)

    server_1 = Server()
    server_2 = Server("localhost", 12345)
    server_3 = Server(port=1234, host="localhost")

    print(server_1.host)
    print(server_3.host)

    client_1 = Client()
    client_2 = Client("127.0.0.1", 2345)
    client_3 = Client(host="localhost", port=1234)

    print()
    print(client_1.host)
    print(client_3.device_id)
