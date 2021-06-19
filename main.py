from flask import Flask, render_template, request
from replit import db
import pickle
import pandas as pd



def push_db(temperature, humidity, location, N, P, K, rainfall, ph, points):
  db["temperature"] = temperature
  db["humidity"] = humidity
  db["location"] = location
  db['N'] = N
  db['P'] = P
  db['K'] = K
  db['rainfall'] = rainfall
  db['ph'] = ph
  db['points'] = points



def carbon_redemption(points):
  red_list = []
  tree = points / 100
  red_list.append(tree)
  cycle = points / 1.5
  red_list.append(cycle)
  return red_list



decoder = {
  '20': 'rice',
  '11': 'maize',
  '3': 'chickpea',
  '9': 'kidneybeans',
  '18': 'pigeonpeas',
  '13': 'mothbeans',
  '14': 'mungbean',
  '2': 'blackgram',
  '10': 'lentil',
  '19': 'pomegrenate',
  '1': 'banana',
  '12': 'mango',
  '7': 'grapes',
  '21': 'watermelon',
  '15': 'muskmelon',
  '0': 'apple',
  '16': 'orange',
  '17': 'papaya',
  '4': 'coconut',
  '6': 'cotton',
  '8': 'jute',
  '5': 'coffee'
}
points = 0

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
  N = request.args.get('N')
  P = request.args.get('P')
  K = request.args.get('K')
  rainfall = request.args.get('rainfall')
  ph = request.args.get('ph')
  vh = request.args.get('vh')
  rh = request.args.get('rh')
  ah = request.args.get('ah')
  points = int(vh) + int(rh) + int(ah) * 2
  push_db(temperature, humidity, location, N, P, K, rainfall, ph, points)
  return "The temperature is {}, humidity is {}, location is {}. Your carbon impact points are {}".format(temperature, humidity, location, points)



@app.route('/output')
def init_ml():
  loaded_model = pickle.load(open('Crop Recommendation/crop_model.sav', 'rb'))
  colm_names = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
  d = {}
  for i in range(len(colm_names)):
      ipt = db[''+colm_names[i]]
      d[colm_names[i]] = ipt
      
  x = pd.Series(d)
  x = x.values.reshape(1, -1)
  predict = decoder[''+str(loaded_model.predict(x)[0])]
  points = db['points']
  redeem = carbon_redemption(points)
  trees = redeem[0]
  drive = redeem[1]
  return "The recommended plant type is: {}. Your carbon impact points are {}. You can balance your carbon balance by planting {} trees or by replacing {} hours of driving by walking/bicycling. ".format(predict, points, trees, drive)



if __name__ == '__main__':
  app.run(
	host='0.0.0.0',
	debug=True,
	port=8080
  )
