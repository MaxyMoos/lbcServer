# -*- coding: utf-8 -*-

"""Main loop and interface to the world"""

import socket
import sys
from _thread import *


class LBCServer(object):
	"""The server"""

	DEF_HOST = ''
	DEF_PORT = 8888

	def __init__(self, host=DEF_HOST, port=DEF_PORT):
		"""Initialize instance"""
		self.host = host
		self.port = port

	def process_incoming_request(self, conn, addr):
		"""Process a request received from a client"""
		greet = "Hello {}, you are connected to LBCServer".format(addr[0])
		conn.send(greet.encode('utf-8'))

		while True:
			try:
				data = conn.recv(1024)
				if not data:
					break
				print("Received data: {}".format(data))
			except ConnectionResetError:
				print("Client {} was disconnected".format(addr[0]))
				break

		print("Client {} session terminated".format(addr[0]))
		conn.close()

	def run(self):
		"""Main loop"""
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create socket

		# Bind the socket
		try:
			self.socket.bind((self.host, self.port))
		except socket.error as msg:
			print("Socket binding failed! Error code = {} - {}".format(msg[0], msg[1]))
			return

		self.socket.listen(10)

		while True:
			conn, addr = self.socket.accept()
			print("Connected with {}".format(addr[0]))

			start_new_thread(self.process_incoming_request, (conn, addr))

		self.socket.close()