import requests
import json
import time

url = 'http://10.128.226.224/api'


def request(text):
	data = {"data":text}
	r = requests.post(url, data)
	return r.text 

def get(payload):
	r = requests.get(url, params=payload)
	#print(r.url)
	return r.text

def handle_remote_error(stack_trace):
	print(stack_trace)
	print('<------------Remote Code------------->')
	get_remote_code()

def remote_exec(code):
	payload = {'request':code}
	raw_result = get(payload)
	result  = json.loads(raw_result)
	if result.get('error'):
		handle_remote_error(result.get('error'))
	elif result.get('result'):
		return result.get('result')
	else:
		print("Unknown response")


def get_cards():
	remote_code = 'global_return = list_cards()'
	return remote_exec(remote_code)

def get_remote_code():
	remote_code = 'global_return = get_remote_code()'
	remote_server_file = remote_exec(remote_code)
	file_with_lines    = ''
	line_number        = 1
	for line in remote_server_file.split('\n'):
		print (('%3d' % line_number) + ':' + line)
		line_number = line_number + 1

def test_remote():
	remote_code = 'global_return = test()'
	return remote_exec(remote_code)

def benchmark():
	num_requests = 0
	start = int(round(time.time() * 1000))
	while True:
		#time.sleep(0.05)
		get_cards()
		num_requests += 1
		if(num_requests%100 == 0):
			now     = int(round(time.time() * 1000))
			delta_t = int((now - start)/float(1000))
			print(str(delta_t))
			delta_r = num_requests
			print(str(delta_r))
			rate    = float(delta_r)/float(delta_t)
			print(str(rate) + ' requests per second')
			num_requests = 0
			start = int(round(time.time() * 1000))

test_remote()




