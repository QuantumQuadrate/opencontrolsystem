from flask import Flask, render_template, request
import datetime
import json

app = Flask(__name__, template_folder='./templates')


test_response = {'card1':[]}

@app.route("/")
def main_serve():
	now  = datetime.datetime.now()
	timeString = now.strftime("%Y-%m-%d %H:%M:%S")
	template_data = {
	'status':'online',
	'time'  : timeString
	}

	return render_template('main.html', **template_data)

@app.route('/api', methods = ['POST', 'GET'])
def hello3():
	if(request.method == 'POST'):
		data = request.form["data"]
		handle(data)
		return "Got request!"
	else:
		data = request.args.get('request', '')
		return serve_api(request)


def serve_api(params):
	args = params.args
	request = args.get('request')
	if(request == "list cards"):
		return list_cards()

def list_cards():
	cards = []
	for i in range(0, 10):
		cards.append("card"+str(i))
	r = json.dumps(cards)
	return r
if __name__ == "__main__":
	app.run(host='0.0.0.0', port = 80, debug= True)
