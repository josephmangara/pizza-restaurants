#!/usr/bin/env python3

from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate

from models import db, Restaurant, RestaurantPizza, Pizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

app.json.compact = True 

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return jsonify({"message": "welcome to my pizza restuarant API."})


if __name__ == '__main__':
    app.run(port=5555, debug=True)
