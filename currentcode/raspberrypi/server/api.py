import json
import random
#function to handle api parameters and return results
def serve_api(parameters):
	#get base request
	request = parameters.get('request','')

	#switch on request type to seperate handlers
	if not request:
		return api_error('No api request specified')
	elif(request=='getcards'):
		#return formatted list of cards in rack
		return get_cards(parameters)
	elif(request=='getcard'):
		#return info for a specific card, id should be encoded in rest of command
		return get_card(parameters)
	elif(request=='getparam'):
		#get parameter from system
		return get_param(parameters)
	elif(request=='setparam'):
		#Set parameter for system
		return set_param(parameters)
	else:
		return api_error('Unknown api request')

def api_error(error_string):
	return json.dumps({'error':error_string})

def get_cards(parameters):
	#will use control object to get real data in the future
	return test_get_cards(parameters)
def get_card(parameters):
	request_card_id = parameters.get('id','')
	if not request_card_id:
		return api_error('no card id provided for request')
	else:
		return test_get_card(request_card_id)

def get_param(parameters):
	return test_get_param(parameters)

#class to prvide test data back
def test_get_cards(parameters):
	cards = []
	for i in range(0, 20):
		test_id   = i*20 + 10000
		test_type = ''
		if((i%2)==0):
			test_type = 'ADC'
		else:
			test_type = 'DAC'

		test_card = {'id':test_id,'type':test_type}
		cards.append(test_card)
	return json.dumps(cards)

def test_get_card(card_id):
	if(card_id==str(123)):
		test_card = {'type':'ADC','uptime':'65.43.21'}
		return json.dumps(test_card)
	else:
		return api_error('card id not found in this rack')

def test_get_param(parameters):
	id = parameters.get('id', '')
	if not id:
		return api_error('no card id provided for request')
	else:
		#some card with id 123
		if(int(id) == 123):
			return test_get_voltage(parameters)
		else:
			return api_error('card id not found in this rack')	

def test_get_voltage(parameters):
	channel = parameters.get('channel')
	if not channel:
		voltages = []
		for j in range(0, 4):
			random_voltage = random.random()
			channel = j
			voltages.append({'channel':channel,'voltage':random_voltage})
		return_data = {'voltages':voltages}
		return json.dumps(return_data)
	else:
		random_voltage = random.random()
		return_data = {'voltage':random_voltage}
		return json.dumps(return_data)












