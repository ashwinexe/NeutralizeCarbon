from flask import Flask, render_template, request
from replit import db
import sklearn
import pickle
import pandas as pd


def push_db(temperature, humidity, location, N, P, K, rainfall):
  db["temp"] = temperature
  db["humid"] = humidity
  db["loc"] = location
  db['N'] = N
  db['P'] = P
  db['K'] = K
  db['rain'] = rainfall



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
  loaded_model = pickle.load(open('Crop Recommendation/crop_model.sav', 'rb'))
  colm_names = ["N","P","K","temperature","humidity","ph","rainfall"]
  d = {}
  for i in range(len(colm_names)):
      print("Enter the value for " + colm_names[i])
      ipt = float(input())
      d[colm_names[i]] = ipt 

  x = pd.Series(d)
  x = x.values.reshape(1, -1)
  return "The predicted plant type is: {}".format(loaded_model.predict(x))



if __name__ == '__main__':
  # Run the Flask app
  app.run(
	host='0.0.0.0',
	debug=True,
	port=8080
  )
