#!/usr/bin/env python3

from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Restaurant, RestaurantPizza, Pizza
from collections import OrderedDict

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
            restaurant_dict = OrderedDict([
                ("id", restaurant.id),
                ("name", restaurant.name),
                ("address", restaurant.address)
            ])
            restaurants.append(restaurant_dict)
            
        response = make_response(
            jsonify(restaurants),
            200,
        )
        return response

    
api.add_resource(Restaurants, '/restaurants')

class RestaurantById(Resource):
    # Get 
    def get(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()

        if restaurant:
            pizzas = []
            added_pizzas = set()

            for rp in restaurant.restaurant_pizzas:
                pizza_id = rp.pizza.id
                if pizza_id not in added_pizzas:
                    pizza_dict = {
                        "id": rp.pizza.id,
                        "name": rp.pizza.name,
                        "ingredients": rp.pizza.ingredients
                    }
                    pizzas.append(pizza_dict)
                    added_pizzas.add(pizza_id)

            restaurant_dict = {
                "id": restaurant.id,
                "name": restaurant.name,
                "address": restaurant.address,
                "pizzas": pizzas
            }
            response = make_response(
                jsonify(restaurant_dict),
                200,
            )
        else:
            response = make_response(
                jsonify({"error": "Restaurant not found"}),
                404
            )
        
        return response
    
    # Delete 
    def delete(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        
        if restaurant:
            RestaurantPizza.query.filter_by(restaurant_id=id).delete()
            db.session.commit()
            
            # Delete Restaurant
            db.session.delete(restaurant)
            db.session.commit()

            response = make_response("", 204)

        else:
            response = make_response(
                jsonify({"error": "Restaurant not found"}),
                404
            )
        return response
    
api.add_resource(RestaurantById, '/restaurants/<int:id>')

class Pizzas(Resource):
    def get(self):
        pizzas = []
        for a_pizza in Pizza.query.all():
            pizza_dict = {
                "id": a_pizza.id,
                "name": a_pizza.name,
                "ingredients": a_pizza.ingredients
            }
            pizzas.append(pizza_dict)
        response = make_response(
            jsonify(pizzas),
            200,
        )

        return response
api.add_resource(Pizzas, '/pizzas')

class RestaurantPizzas(Resource):
    def post(self):
        if pizza == 201:
            new_pizza_restaurant = RestaurantPizza(
                price=request.form['price'],
                pizza_id=request.form['pizza_id'],
                restaurant_id=request.form['restaurant_id'],
            ) 
            db.session.add(new_pizza_restaurant)
            db.session.commit()

            for pizza in Pizza.query.all():
                response_dict = {
                    "id": pizza.id,
                    "name": pizza.name,
                    "ingredients": pizza.ingredients
                }
            response = make_response(
                jsonify(response_dict),
                201,
            )
            return response 
        else:
            response = make_response(
                jsonify({"errors": ["validation errors"]}),
                205,)

api.resource(RestaurantPizzas, '/restaurant_pizzas')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
