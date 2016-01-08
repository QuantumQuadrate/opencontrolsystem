import socket

class MySocket(object):
	"""demonstration class only
	- coded for clarity, not efficiency
	"""
	def __init__(self, sock=None):
		self.msglen = 1024
		if sock is None:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		else:
			self.sock = sock

	def connect(self, host, port):
		self.sock.connect((host, port))
	
	def serve(self):
		self.sock.bind(('', 80))
		self.sock.listen(1)
		while 1:
			client, address = self.sock.accept()
			print("Got a connection from " + str(address))
			while 1:
				data = self.sock.recv(1024)
				print(data)
				if not data:
					break
				client.sendall(data)
			client.close()
	
	def send(self, msg):
		totalsent = 0
		while totalsent < self.msglen:
			sent = self.sock.send(msg[totalsent:])
			if sent == 0:
				raise RuntimeError("socket connection broken")
			totalsent = totalsent + sent

	def receive(self):
		chunks = []
		bytes_recd = 0
		while bytes_recd < self.msglen:
			chunk = self.sock.recv(min(self.msglen - bytes_recd, 2048))
			if chunk == b'':
				raise RuntimeError("socket connection broken")
			chunks.append(chunk)
			bytes_recd = bytes_recd + len(chunk)
			return b''.join(chunks)



sock = MySocket()

sock.serve()