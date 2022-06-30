from flask import Blueprint, request, jsonify
from food_inventory.helpers import token_required
from food_inventory.models import db, User, Recipe, recipe_schema, recipes_schema

api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return{'some':'value'}

# CREATE RECIPE ENDPOINT
@api.route('/recipes', methods = ['POST'])
@token_required
def create_recipe(current_user_token):
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    veggie = request.json['veggie']
    cooking_time = request.json['cooking_time']
    allergens = request.json['allergens']
    cooking_tools = request.json['cooking_tools']
    serving_size = request.json['serving_size']
    user_token = current_user_token.token

    print(f"BIG TESTER: {current_user_token.token}")

    recipe = Recipe(name, description, price, veggie, cooking_time, allergens, cooking_tools, serving_size, user_token = user_token  )

    db.session.add(recipe)
    db.session.commit()

    response = recipe_schema.dump(recipe)

    return jsonify(response)

# Retrieve all Recipe Endpoints
@api.route('/recipes', methods = ['GET'])
@token_required
def get_recipes(current_user_token):
    owner = current_user_token.token
    recipes = Recipe.query.filter_by(user_token = owner).all()
    response = recipes_schema.dump(recipes)
    return jsonify(response)


# Retrieve ONE Recipe Endpoint
@api.route('/recipes/<id>', methods = ['GET'])
@token_required
def get_recipe(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        recipe = Recipe.query.get(id)
        response = recipe_schema.dump(recipe)
        return jsonify(response)
    else:
        return jsonify({'message': "Valid Token Required"}), 401

# Update Recipe
@api.route('/recipes/<id>', methods = ['POST', 'PUT'])
@token_required
def update_recipe(current_user_token, id):
    recipe = Recipe.query.get(id)

    recipe.name = request.json['name']
    recipe.description = request.json['description']
    recipe.price = request.json['price']
    recipe.veggie = request.json['veggie']
    recipe.cooking_time = request.json['cooking_time']
    recipe.allergens = request.json['allergens']
    recipe.cooking_tools = request.json['cooking_tools']
    recipe.serving_size = request.json['serving_size']
    recipe.user_token = current_user_token.token
    
    db.session.commit()
    response = recipe_schema.dump(recipe)
    return jsonify(response)

# Delete Recipe
@api.route('/recipes/<id>', methods=['DELETE'])
@token_required
def delete_recipe(current_user_token, id):
    recipe = Recipe.query.get(id)
    db.session.delete(recipe)
    db.session.commit()
    response = recipe_schema.dump(recipe)
    return jsonify(response)