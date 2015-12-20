import smbus
import time

#create I2C bus object on i2c port 1
bus = smbus.SMBus(1)


#Write block to card (wrapper)
def write_block(address, block):
	#sbus library expects first byte of block then rest of the block
	bus.write_i2c_block_data(address,block[0],block[1:])

#Request block from card (wrapper)
def read_block(address, cmd, tries=0):
	#First byte is address, second byte is the command byte which is sent with the request
	try:
		return bus.read_i2c_block_data(address, cmd)
	except IOError:
		if(tries<=5):
			time.sleep(0.001)
			print("Error reading block from card, retrying")
			read_block(address, cmd,(tries+1))
		else:
			print("Resent read_command " + str(5) + " times without success")

def str_to_int(s):
	l = []
	for character in list(s):
		l.append(ord(character))
		#print(character + ":" + str(ord(character)))
	return l

def int_to_str(ints):
	s = ""
	for int in ints:
		s+=unichr(int)
	return s

def write_stream(addr, s):
	block_size = 16
	for i in range(0, len(s)/block_size):
		chunk = s[i*block_size:(i+1)*block_size]
		time.sleep(0.1)
		write_block(addr, str_to_int(chunk))
		#print(chunk)
	chunk = s[((len(s)/block_size)*block_size):] + '\n'
	time.sleep(0.1)
	write_block(addr, str_to_int(chunk))

def chop_padding(l):
	newline = []
	#remove padding from block
	for num in l:
		if(num != 255):
			print(str(num))
			newline.append(num)
	return newline
	
def read_stream(addr):
	stream = ""
	while(stream.find('\n') == -1):
		stream+=int_to_str(chop_padding(read_block(addr, 65)))
		#print(stream)
	return stream

#for j in range(0, 100):
#	time.sleep(0.1)
#	write_stream(5, "Hello my name is Josh Cherek. This is a test string for the open controls project.")


write_stream(5, "Hello my name is Josh Cherek. This is a test string for the open controls project.")

while(True):
	time.sleep(0.25)
	f = read_stream(5);
	print(f)
	write_stream(5,f)

#print(read_block(5, 44))
	
#write_block(5, str_to_int("Helloasdfaasdfkljsdaflkjsdlfkjslkdfjmadison\n"))

#b = read_block(5, 1)
#s = ""
#for c in b:
#	s+=unichr(c)
#print(s)