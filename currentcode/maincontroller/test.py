import card as card_class
import comm
test_comm = comm.comm()

def test_card_init():
	ip = "192.168.1.23"
	rack_address = 10
	test_response = '{"global_id": 12345, "registers":[{"voltage": 53},{"temp": 34}]}'
	test_comm.set_test_response(test_response)
	c = card_class.card(test_comm, ip, rack_address)
	c.print_info()

test_card_init()