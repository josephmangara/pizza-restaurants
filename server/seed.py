from app import app, db
from models import RestaurantPizza, Restaurant, Pizza
import random
from faker import Faker
from random import randint, choice

fake = Faker()

with app.app_context():
    # delete previous records
    Restaurant.query.delete()
    RestaurantPizza.query.delete()
    Pizza.query.delete()

    # restaurants
    restaurants = []
    for fake_res in range(8):
        fake_res = Restaurant(name=fake.name(),
                              address=fake.address())
        restaurants.append(fake_res)

    db.session.add_all(restaurants)

    # ingredients
    ingredients = ["Dough", "Tomato Sauce", "Lard", "Cheese", "Pineapple", "Pepperoni"]

    pizzas = []
    for pizza_name in ingredients:
        pizza_ingredients = random.sample([ing for ing in ingredients if ing != "Dough"], random.randint(2, len(ingredients) - 1))
        pizza_ingredients.append("Dough") 
        pizza = Pizza(
            name=pizza_name,
            ingredients=", ".join(pizza_ingredients)
        )
        pizzas.append(pizza)

    db.session.add_all(pizzas)
    
    # restaurant pizzas
    restaurant_pizzas = []
    for res in range(47):
        random_restaurant = choice(Restaurant.query.all())
        random_pizza = choice(Pizza.query.all())

        res = RestaurantPizza(
            price=randint(1, 30),
            restaurant_id=random_restaurant.id,
            pizza_id=random_pizza.id
        )
        restaurant_pizzas.append(res)

    db.session.add_all(restaurant_pizzas)
    db.session.commit()