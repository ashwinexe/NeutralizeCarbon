from flask import Flask, render_template, request
from replit import db



def push_db(temperature, humidity, location):
  db["temp"] = temperature
  db["humid"] = humidity
  db["loc"] = location



app = Flask(
  __name__,
  template_folder='templates',
  static_folder='static'
)

@app.route('/')
def hello():
  return render_template('index.html')



@app.route('/input', methods = ['POST', 'GET'])
def parse_requests():
  temperature = request.args.get('temperature')
  humidity = request.args.get('humidity')
  location = request.args.get('location')
  push_db(temperature, humidity, location)
  print(db['humid'])
  return "The temperature is {}, humidity is {}, location is {}.".format(temperature, humidity, location)



@app.route('/output')
def init_ml():
  # some code here
  return "model output here"



if __name__ == '__main__':
  # Run the Flask app
  app.run(
	host='0.0.0.0',
	debug=True,
	port=8080
  )
