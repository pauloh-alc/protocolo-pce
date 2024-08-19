from base_connect import Base

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
