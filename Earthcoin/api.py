from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)

# Product Class/Model
class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), unique=True)
  qty = db.Column(db.Integer)

  def __init__(self, name, qty):
    self.name = name
    self.qty = qty

# Product Schema
class ProductSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'qty')

# Init schema
product_schema = ProductSchema(strict=True)
products_schema = ProductSchema(many=True, strict=True)

# Create a User
@app.route('/newuser', methods=['POST'])
def add_product():
  name = request.json['name']
  qty = 0

  new_product = Product(name, qty)

  db.session.add(new_product)
  db.session.commit()

  return product_schema.jsonify(new_product)


# Get coins by ID
@app.route('/user/<id>', methods=['GET'])
def get_product(id):
  product = Product.query.get(id)
  return product_schema.jsonify(product)

# Update user
@app.route('/user/<id>', methods=['PUT'])
def update_product(id):
  product = Product.query.get(id)

  name = request.json['name']
  qty = request.json['qty']

  product.name = name
  product.qty = qty

  db.session.commit()

  return product_schema.jsonify(product)


# Run Server
if __name__ == '__main__':
  app.run(debug=True)
