#coding: utf-8

import socket

class MockClient(object):
    def __init__(self, host=None, port=None):
        self.host = host
        self.port = port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_connected = False

    def __del__(self):
        if self.is_connected:
            self._socket.shutdown(socket.SHUT_RDWR)
            self._socket.close()

    def connect(self):
        if self.host is not None and self.port is not None:
            self._socket.connect((self.host, self.port))
            self.is_connected = True

    def send(self, data):
        if self.is_connected and type(data) in (str, bytes):
            if type(data) == str:
                data = data.encode('utf-8')
            self._socket.send(data)
        elif not self.is_connected:
            print("MockClient: Cannot send data - no connection is active")
        else:
            print("MockClient: Cannot send data \"{}\": unsupported data type".format(data))


if __name__ == "__main__":
    try:
        client = MockClient(host="localhost", port=8888)
        client.connect()
        client.send("hello!")
    except Exception as e:
        print(e)
