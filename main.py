from flask import Flask, render_template, request, jsonify, make_response

# Create a flask app
app = Flask(
  __name__,
  template_folder='templates',
  static_folder='static'
)

# Index page
@app.route('/')
def hello():
  return render_template('index.html')


@app.route('/input', methods = ['POST', 'GET'])
def parse_requests():
  temperature = request.args.get('temperature')
  humidity = request.args.get('humidity')
  location = request.args.get('location')
  return "The temperature is {}, humidity is {}, location is {}".format(temperature, humidity, location)



if __name__ == '__main__':
  # Run the Flask app
  app.run(
	host='0.0.0.0',
	debug=True,
	port=8080
  )
