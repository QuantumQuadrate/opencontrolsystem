import smbus
import time

#create I2C bus object on i2c port 1
bus = smbus.SMBus(1)

num_times = 0


def write_byte(addr, byte):
	bus.write_byte_data(addr, 0x55, byte)

def write_bytes(addr, bytes):
	for byte in list(bytes):
		write_byte(addr, byte)


#Write block to card (wrapper)
def write_block(address, block, tries=0):
	#sbus library expects first byte of block then rest of the block
	try:
		bus.write_i2c_block_data(address,block[0],block[1:])
	except IOError:
		if(tries<=5):
			#print(num_times)
			print("Error writing block, retrying")
			#time.sleep(0.05)
			write_block(address, block, tries+1)
		else:
			print("Error writing block, tried " + str(tries) + " times")

#Request block from card (wrapper)
def read_block(address, cmd, tries=0):
	#First byte is address, second byte is the command byte which is sent with the request
	try:
		return bus.read_i2c_block_data(address, cmd)
	except IOError:
		if(tries<=5):
			time.sleep(1)
			print("Error reading block from card, retrying " + str(tries) + " time")
			return read_block(address, cmd, tries+1)
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
	block_size = 31
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


def test_write():
	num_good = 0
	keep_going = True
	while(keep_going):
		try:
			time.sleep(0.1)
			write_block(5, [125])
			#print("block written")
			num_good = num_good+1
		except:
			keep_going = False
			print(num_good)

def test_read():
	num_good = 0
	keep_going = True
	while(keep_going):
		try:
			print(len(read_block(5, 5)))
			num_good = num_good+1
		except:
			keep_going = False
			print(num_good)

#test_read()


def read_string(addr, cmd = 0x55):
	read_finished = False
	return_string = ""
	while not read_finished:
		chunk = read_block(addr,cmd)
		chopped_chunk = chop_padding(chunk)
		return_string = return_string + int_to_str(chopped_chunk)
		if(10 in chopped_chunk):
			return return_string

print(read_string(5))
