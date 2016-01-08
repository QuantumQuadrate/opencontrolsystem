import socket

class net(object):
	def __init__(self, port = 80):
		self._port = port
		self.sock  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


	#default function to handle incoming connections
	def default_handle(self, data):
		print("Handled message " + str(data))
		#default to echo server
		return(data)

	#setup socket as server
	#Pass function to handle the connection when it arrives
	def serve(self, handle = default_handle,host = '', port = 80):
		self.sock.bind((host, port))
		self.sock.listen(1)
		while 1:
			#Wait to accept connections
			conn, addr = self.sock.accept()
			print 'received connection from ', addr
			data = ''
			#get chunks from buffer until empty
			while 1:
				#Append chunk
				data += conn.recv(2048)
				if not data:
					print("end of transmission")
					break
				else:
					print("    received data chunk:" + str(data))
			#handle the data and send appropriate response
			conn.sendall(handle(data))
			#close the connection
			conn.close()


	def send(self, host='127.0.0.1', data = 'This is a message from a client'):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((host, self._port))
		print('connected to host ' + str(host))
		print('Sending data ' + data)
		s.sendall(data)
		data = s.recv(1024)
		print 'Received ', repr(data)
		print('closing connection')
		s.close()

n = net()

#n.send('10.128.226.224', "Hello world")
n.serve()
