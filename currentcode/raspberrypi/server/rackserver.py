from flask import Flask, render_template
import datetime

app = Flask(__name__, template_folder='./templates')


@app.route("/")
def main_serve():
	now  = datetime.datetime.now()
	timeString = now.strftime("%Y-%m-%d %H:%M:%S")
	template_data = {
	'status':'online',
	'time'  : timeString
	}

	return render_template('main.html', **template_data)

@app.route("/somefolder/")
def hello3():
	return "This is a subfolder"

if __name__ == "__main__":
	app.run(host='0.0.0.0', port = 80, debug= True)