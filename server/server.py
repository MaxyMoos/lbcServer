# -*- coding: utf-8 -*-

"""Main loop and interface to the world"""

import socket
import sys
import json
from _thread import start_new_thread

import query_manager
from item import LeBonCoinItemJSONEncoder

import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
log.addHandler(handler)


class LBCServer(object):
    """The server"""

    DEF_HOST = 'localhost'
    DEF_PORT = 8888

    ADD_CODE = '1'
    DELETE_CODE = '2'
    UPDATE_CODE = '3'

    def __init__(self, host=DEF_HOST, port=DEF_PORT):
        """Initialize instance"""
        self.host = host
        self.port = port
        self._mapping = {
                self.ADD_CODE: self.process_add,
                # self.DELETE_CODE: self.process_delete,
                # self.UPDATE_CODE: self.process_update
                }
        self.queries = []

    def run(self):
        """Main loop"""
        # Create socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket
        try:
            self.socket.bind((self.host, self.port))
        except OSError as e:
            if e.errno == 98:
                log.error(
                    "Address already in use ({}:{}), "
                    "terminating server".format(self.host, self.port)
                )
                return
            else:
                raise e
        except socket.error as msg:
            log.error(
                "Socket binding failed! Error code = {} - {}".format(
                    msg[0], msg[1]))
            return

        log.info(
            "Server started and listening on {}:{}".format(
                self.host, self.port
            )
        )
        self.socket.listen(10)

        while True:
            try:
                conn, addr = self.socket.accept()
                log.info("Connected with {}".format(addr[0]))

                start_new_thread(
                    self.process_incoming_request, (conn, addr[0])
                )
            except KeyboardInterrupt:
                log.info("\nServer terminated by user (keyboard interrupt)")
                self.close_socket()
                return
            except Exception as e:
                log.error(e)
                self.close_socket()
                return

    def close_socket(self):
        log.debug("Shutting down socket...")
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

    def process_incoming_request(self, conn, ip_addr):
        """Process a request received from a client"""
        greet = "Hello {}, you are connected to LBCServer".format(ip_addr)
        conn.send(greet.encode('utf-8'))

        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                try:
                    data = str(data, 'utf-8')
                    log.info("{} - Received data: {}".format(ip_addr, data))
                    data = json.loads(data)
                    ret = self.process_incoming_data(data)
                    if ret:
                        conn.send(json.dumps(ret).encode('utf-8'))
                except json.JSONDecodeError as e:
                    log.error(
                        "{} - Unsupported data received: {}".format(
                            ip_addr, data
                        )
                    )
            except ConnectionResetError:
                log.warning("Client {} was disconnected".format(ip_addr))
                break

        log.info("Client {} session terminated".format(ip_addr))
        conn.close()

    def process_incoming_data(self, data):
        """Process received JSON-formatted data"""
        ret = {}
        for code, code_data in data.items():
            ret[code] = self._mapping[code](code_data)  # Process the current node
        return ret

    def process_add(self, data):
        if not all(x in data.keys() for x in ('query', 'location', 'freq')):
            log.error("Badly formatted data node")

        query = data['query']
        location = data['location']
        freq = data['freq']

        new_qManager = query_manager.LeBonCoin_QueryManager(
            query, location, freq
        )
        self.queries.append(new_qManager)
        return json.dumps(new_qManager.run(), cls=LeBonCoinItemJSONEncoder)


if __name__ == "__main__":
    serv = LBCServer()
    serv.run()
