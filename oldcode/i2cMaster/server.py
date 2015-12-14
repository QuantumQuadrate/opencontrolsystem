from flask import Flask
from controller import vme_controller
ctrlr = vme_controller()


app = Flask(__name__)


@app.route('/')
def hello_world():
	return 'You have reached the Open Controls Server'

@app.route('/init')
def init():
	ctrlr.init_routing_table()
	return("<p>Subrack ihitialized with " + str(ctrlr.num_devices()) + " devices!</p>")

@app.route('/list')
def list():
	address_array = ctrlr.poll_table()
	print("number of devices = " + str(len(address_array)) )
	html = ""
	html = html + "performing live address poll on subrack" + "</br>"
	for address in address_array:
		html = html + "found device with address:" + str(address) + "</br>"
	return html



#@app.route('/api', methods = ['POST','GET'])
#def api_handle():
	#if request.method =='GET'
		

if __name__ == '__main__':
	app.run(host='0.0.0.0')