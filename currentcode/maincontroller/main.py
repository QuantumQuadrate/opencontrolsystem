#import ethernet/sockets communication libraries etc...
#import card class
import comm as comm
main_comm = comm.comm()

class main():
	def __init__(self):
		#setup communication with racks
		self._comm = comm.comm()
		#create a list of card objects that contain an address data (IP(Static IP!), card number)
		self._cards = []
		#Iterate through IP's or get list directly from DHCP server....
		for IP in all ips...:
			if valid rack IP...:
				for each valid rack_address (Card) in rack...:
					temp_card = card(IP, rack_address)
					self._cards.append(temp_card)
		
		#retrieve info about cards in json (iterate through cards and setup
		object variables based on json returned)
		for each card in cards:
			card.update_card()
	def get(self, global_id):
		#search through all cards till the one with that global id is found
		for card in self._cards:
			if card.global_id = global_id:
				return card
		raise Exception("Request for Invalid Card ID, double check the ID and make sure the card is connected")
		return None