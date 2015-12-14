#This class holds a routing table and performs operations on it
class routing_table:
	#instantiate routing table
	def __init__(self):
		#routing table maps hardware ids to addresses
		self.routing_table = dict()
		#Must keep track of unused addresses
		self.unused_addresses = []
		#I2C addresses go from 6 to 119 but 5 is reserved for initialization
		for x in range(6, 119):
			self.unused_addresses.append(x)

	#pop next availible address from list
	def get_next_unused_address(self):
		if(len(self.unused_addresses) == 0):
			print("No addresses available")
		return self.unused_addresses.pop()

	#Add new device by hardware id and return address
	def add_device(self,hardware_id):
		#add entry in dictionary object that maps the hardwareid key to an address
		new_address = self.get_next_unused_address()
		self.routing_table[hardware_id] = new_address
		return new_address

	#remove device by hardware id
	def remove_device_by_id(self,hardware_id):
		#get the address of the device about to be removed
		newly_added_address = self.routing_table.get(hardware_id)
		#delete the device from the routing table
		del self.routing_table[hardware_id]
		#add the deleted device's address to the list of available devices
		self.unused_addresses.append(newly_added_address)

	#remove device by address
	def remove_device_by_address(self,address):
		remove_device_by_id(self.address_to_id(address))

	#perform reverse lookup and get hardware id given an address
	def address_to_id(self,address):
		for hardware_id, address in self.routing_table.items():
			if(address == find_address):
				return hardware_id
		return False

	#Get address from device ID
	def id_to_address(self, id):
		if(has_device(id)):
			return self.routing_table.get(id)
		else:
			return False

	#return number of devices available
	def number_devices(self):
		return len(self.routing_table)

	#check if routing table contains a specific device id
	def has_device(self,device_id):
		return (device_id in self.routing_table)

	#check if routing table contains a specific address
	def has_address(self,address):
		if(self.address_to_id(address) == False):
			return False
		else:
			return True

	#clear the routing table
	def clear_table(self):
		self.routing_table.clear()
		self.self.unused_addresses.clear()
		for x in range(4, 119):
			self.unused_addresses.append(x)

	#Return number of available addresses
	def number_addresses_available(self):
		return len(self.unused_addresses)
		
	#print routing table
	def print_routing_table(self):
		print('|' + ('%5s' % 'mac') + '|' + ('%5s' % 'addr') + '|')
		print('-------------')
		for hardware_id, address in self.routing_table.items():
			print('|' + ('%5s' % str(hardware_id)) + '|' +('%5s' % str(address)) + '|')
			print('-------------')
		
	
		