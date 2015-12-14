import struct

class utils:
	#little endian
	def int_upper_byte(self, integer):
		return (integer>>8 & 0xff)
	#little endian
	def int_lower_byte(self, integer):
		return (integer>>0 & 0xff)
	#little endian
	def int_to_bytes(self, integer):
		return [self.int_lower_byte(integer), self.int_upper_byte(integer)]

	#get two bytes from an array and convert to unsigned int
	def bytes_to_unsigned_int(self, array, position = 0):
		return (256*array[position+1] + array[position])

	#get two bytes from an array and convert to unsigned int
	def bytes_to_int(self, array, position = 0):
		return struct.unpack('h', str(array[position:position + 2]))
	
	#get two bytes from an array and convert to unsigned int
	def bytes_to_long(self, array, position = 0):
		return struct.unpack('l', str(array[position:position + 4]))

	#place 16 bit integer into byte array at particular location
	def place_int(self, array, x, location):
		if((location<0)):
			print "you have requested a location less than zero"
		elif(len(array)<2):
			print "The array is too small to place an integer"
		elif((location + 2)> len(array)):
			print "the integer bytes go beyond the bounds of the array"
		else:
			low  = (x>>0 & 0xff)
			high = (x>>8 & 0xff)
			array[location] = low
			array[location+1] = high