#Communication class for main controller
#Wrapper for ethernet library that will be added later

class comm():
	def __init__(self):
		self._test_json = None

	def send_request(self, ip, rack_address, request):
		if(self._test_json):
			return self._test_json
		else:
			return None
	#setup a test response
	def set_test_response(self, test_json):
		self._test_json = test_json