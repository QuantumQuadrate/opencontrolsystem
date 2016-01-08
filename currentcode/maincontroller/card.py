#import communication library
import json
class card:
	#initialize by passing in a comm object and setting ip and rack address
	def __init__(self, comm, ip, rack_address):
		#store communication info in card object
		self._comm          = comm
		self._ip            = ip
		self._rack_address  = rack_address
		self._info          = self.get_json_info()
		self._global_id     = self.get_global_id()
		self._registers     = self.get_registers()
		self._register_types= self.get_register_types()

	#Send a request to get the json format info from the card
	def get_json_info(self):
		#get raw json string from card
		json_text = self.net_get("info")
		#convert json into an object and return
		return json.loads(json_text)

	#Use the json from the card and parse out the global id
	def get_global_id(self):
		#sudo code...
		return self._info["global_id"]

	#Use the json info to create dictionary mapping variable names to register locations (also datatype?)
	def get_registers(self):
		mapping = self._info["registers"]
		return mapping

	#map from name to datatype
	def get_register_types(self):
		map = dict()
		return map

	#Wrapper for the comm object
	def net_get(self, request):
		return self._comm.send_request(self._ip, self._rack_address, request)

	#Print info for this card
	def print_info(self):
		print("->" + "registers:")
		for register in self._registers:
			print("--->" + str(register))

		