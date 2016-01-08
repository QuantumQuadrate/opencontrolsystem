#Communication class for main controller
#Wrapper for other communication libraries that will be added later

class comm():
	def __init__(self, physical_layer == "ethernet"):
		self._test_json = None
		self._physical_layer = physical_layer
		self.init_comm()

	def send_request(self, ip, rack_address, request):
		if(self._test_json):
			return self._test_json
		else:
			pl = self._physical_layer
			if pl is "ethernet":
			#bind to ethernet ports etc...
		elif pl is "usb":
			#bind to serial port
		elif pl is "i2c":
			#setup i2c communication
		else:
			raise Exception("Invalid physical layer type")

	def init_comm(self):
		pl = self._physical_layer
		if pl is "ethernet":
			#bind to ethernet ports etc...
		elif pl is "usb":
			#bind to serial port
		elif pl is "i2c":
			#setup i2c communication
		else:
			raise Exception("Invalid physical layer type")
	

	#setup a test response
	def set_test_response(self, test_json):
		self._test_json = test_json