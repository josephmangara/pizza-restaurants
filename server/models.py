from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    restaurant_pizzas = db.relationship('RestaurantPizza', backref="restaurant")

class Pizza(db.Model):
    __tablename__ = 'pizzas'

    serialize_rules = ('-restaurant_pizzas.pizza',) 

    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String)
    ingredients = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    restaurant_pizzas = db.relationship('RestaurantPizza', backref="pizza")

class RestaurantPizza(db.Model):
    __tablename__ = 'restaurant_pizzas'

    id = db.Column(db.Integer, primary_key=True) 
    price = db.Column(db.Integer)
    pizza_id = db.Column(db.Integer, db.ForeignKey("pizzas.id"))
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('price')
    def validate_price(self, key, value):
        if value < 1 or value > 30:
            raise ValueError("The price should be between $1 and $30.")
        return value 
