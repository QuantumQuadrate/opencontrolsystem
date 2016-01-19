from flask import Flask, render_template, request
import datetime
import json
import sys, traceback
app = Flask(__name__, template_folder='./templates')

from api import serve_api

test_response = {'card1':[]}


global_return = ""

#default route that displays status
@app.route("/")
def main_serve():
	now  = datetime.datetime.now()
	timeString = now.strftime("%Y-%m-%d %H:%M:%S")
	template_data = {
	'status':'online',
	'time'  : timeString
	}

	return render_template('main.html', **template_data)

#Route to directly execute python
@app.route('/direct', methods = ['POST', 'GET'])
def hello3():
	if(request.method == 'POST'):
		data = request.form["data"]
		handle(data)
		return "Got request!"
	else:
		data = request.args.get('request', '')
		return direct_exec(request)

#Route for api
@app.route('/api', methods = ['GET', 'POST'])
def api():
	if(request.method == 'POST'):
		return "Expected GET parameters but got POST instead"
	elif(request.method == 'GET'):
		data = request.args
		return serve_api(data)
	else:
		return "No arguments provided"




def direct_exec(params):
	args = params.args
	request = args.get('request')
	print(request)
	try:
		exec(request)
		return_val = {'result': global_return}
		return json.dumps(return_val)
	except Exception, e:
		trace_back = traceback.format_exc()
		return_val = {'error': trace_back}
		return json.dumps(return_val)

def get_remote_code():
	f = open('server.py', 'r')
	return f.read()

def list_cards():
	cards = []
	for i in range(8, 10):
		cards.append("card"+str(i))
	r = json.dumps(cards)
	return r

def test():
	a = float(1)/0
	r = json.dumps(a)
	return r
if __name__ == "__main__":
	app.run(host='0.0.0.0', port = 80, debug= True)
