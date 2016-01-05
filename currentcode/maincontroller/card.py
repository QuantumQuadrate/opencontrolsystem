#import communication library
import json
class card:
	def __init__(self, comm, ip, rack_address):
		#store communication info in card object
		self._comm          = comm
		self._ip            = ip
		self._rack_address  = rack_address
		self._info          = self.get_json_info()
		self._global_id     = self.get_global_id()
		self._registers     = self.get_registers()
		self._register_types= self.get_register_types()
	def get_json_info(self):
		#get raw json string from card
		json_text = self.get("info")
		#convert json into an object and return
		return json.loads(json_text)
	def get_global_id(self):
		#sudo code...
		return self._info["global_id"]
	#create dictionary mapping variable names to register locations (also datatype?)
	def get_registers(self):
		mapping = self._info["registers"]
		return mapping
	#map from name to datatype
	def get_register_types(self):
		map = dict()
		return map	
	#Send a request to this card and get the reponse text (move to comm layer)
	def get(self, request):
		return self._comm.send_request(self._ip, self._rack_address, request)
	def print_info(self):
		print("->" + "registers:")
		for register in self._registers:
			print("--->" + str(register))

		