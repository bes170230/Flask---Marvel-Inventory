from flask import Blueprint, request, jsonify
from marvel_inventory.helpers import token_required
from marvel_inventory.models import db, User, Marvel, marvel_schema, marvels_schema


api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return {'some': 'value'}



@api.route('/marvels', methods = ['POST'])
@token_required
def create_marvel(current_user_token):
    print(current_user_token)
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    runtime = request.json['runtime']
    release_date = request.json['release_date']
    rating = request.json['rating']
    director = request.json['director']
    budget = request.json['budget']
    user_token = current_user_token.token

    print(f"BIG TESTER: {current_user_token.token}")

    marvel = Marvel(name, description, price, runtime, release_date, rating, director, budget, user_token=user_token)

    db.session.add(marvel)
    db.session.commit()

    response = marvel_schema.dump(marvel)
    return jsonify(response)

@api.route('/marvels', methods=['GET'])
@token_required
def get_marvels(current_user_token):
    owner = current_user_token.token
    marvels = Marvel.query.filter_by(user_token = owner).all()
    response = marvels_schema.dump(marvels)
    return jsonify(response)

@api.route('/marvels/<id>', methods=['GET'])
@token_required
def get_marvel(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        marvel = Marvel.query.get(id)
        response = marvel_schema.dump(marvel)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid token required'}), 401

@api.route('/marvels/<id>', methods = ['POST', 'PUT'])
@token_required
def update_marvel(current_user_token, id):
    marvel = Marvel.query.get(id)
    marvel.name = request.json['name']
    marvel.description = request.json['description']
    marvel.price = request.json['price']
    marvel.runtime = request.json['runtime']
    marvel.release_date = request.json['release_date']
    marvel.rating = request.json['rating']
    marvel.director = request.json['director']
    marvel.budget = request.json['budget']
    marvel.user_token = current_user_token.token

    db.session.commit()
    response = marvel_schema.dump(marvel)
    return jsonify(response)

@api.route('/marvels/<id>', methods = ['DELETE'])
@token_required
def delete_marvel(current_user_token, id):
    marvel = Marvel.query.get(id)
    db.session.delete(marvel)
    db.session.commit()
    response = marvel_schema.dump(marvel)
    return jsonify(response)
