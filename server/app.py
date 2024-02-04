#!/usr/bin/env python3

from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Restaurant, RestaurantPizza, Pizza

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

app.json.compact = True 

migrate = Migrate(app, db)

db.init_app(app)

class Home(Resource):
    def get(self):
        return jsonify({"message": "welcome to my pizza restuarant API."})

api.add_resource(Home, '/')

class Restaurants(Resource):
    def get(self):
        restaurants = []
        for restaurant in Restaurant.query.all():
            restaurants_dict = {
                "id": restaurant.id,
                "name": restaurant.name,
                "address": restaurant.address,
            }
            restaurants.append(restaurants_dict)

        response = make_response(
            jsonify(restaurants),
            200,
        )
        return response
    
api.add_resource(Restaurants, '/restaurants')

# class Restaurants(Resource):
#     def get(self):
#         restaurants = []
#         for restaurant in Restaurant.query.all():
#             restaurants_dict = {
#                 "id": restaurant.id,
#                 "name": restaurant.name,
#                 "address": restaurant.address,
#                 "pizza": []
#         }
#         restaurants.append(restaurants_dict)
#         response = make_response(
#             jsonify(restaurants_dict),
#             200,
#         )
#         return response
    
# api.add_resource(Restaurants, '/restaurants')




if __name__ == '__main__':
    app.run(port=5555, debug=True)
