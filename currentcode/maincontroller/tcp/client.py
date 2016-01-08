# Echo client program
import socket
import time
HOST = '10.128.226.224'    # The remote host
PORT = 80             # The same port as used by the server
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


while 1:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	s.sendall('Hello, world')
	data = s.recv(1024)
	print 'Received', repr(data)
	time.sleep(0.1)
	s.close()