# coding: utf-8

import socket
import json
import time
import errno

class MockClient(object):
    def __init__(self, host=None, port=None):
        self.host = host
        self.port = port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setblocking(0)
        self.is_connected = False

    def __del__(self):
        if self.is_connected:
            self._socket.shutdown(socket.SHUT_RDWR)
            self._socket.close()

    def connect(self):
        if self.host is not None and self.port is not None:
            try:
                self._socket.connect((self.host, self.port))
            except BlockingIOError as e:
                if e.errno == errno.EINPROGRESS:
                    pass
                else:
                    raise e
            self.is_connected = True

    def send(self, data):
        if self.is_connected and type(data) in (str, bytes):
            if type(data) == str:
                data = data.encode('utf-8')
            self._socket.send(data)
        elif not self.is_connected:
            print("MockClient: Cannot send data - no connection is active")
        else:
            print("MockClient: Cannot send data \"{}\": "
                  "unsupported data type".format(data))

    def _recv(self, data_size):
        if self.is_connected:
            return self._socket.recv(data_size)
        else:
            print("MockClient: Cannot receive data - no connection is active")

    def receive_response(self, timeout=0.5):
        """Received arbitrary long response in batches

        :param timeout  Sets the maximum duration (in seconds) without receiving data
                        that will prompt the client to consider it has received all
                        expected data
        """

        full_data = []
        start_time = time.time()

        while(True):
            try:
                if len(full_data) > 0 and (time.time() - start_time > timeout):
                    break

                data = self._recv(1024)
                if len(data) > 0:
                    full_data.append(str(data, 'utf-8'))
                    start_time = time.time()
            except BlockingIOError as e:
                # Expected exception (for non-blocking sockets) that warns that the recv
                # operation is in progress
                if e.errno == errno.EINPROGRESS:
                    pass
            except ConnectionResetError:
                break

        if len(full_data) > 0:
            full_data = "".join(full_data)
            return full_data
        else:
            return ""


if __name__ == "__main__":
    try:
        # Connect the client and send a request to the server
        client = MockClient(host="localhost", port=8888)
        client.connect()

        # Display server greeting
        print(client.receive_response())

        # Send request
        data = {
            1:  {
                'query': u"Voiture",
                'location': u'Paris',
                'freq': 60,
            }
        }
        client.send(json.dumps(data))

        # Wait for response and print it
        print(json.loads(client.receive_response()))
    except Exception as e:
        print(e)
