"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    serialized_users = list(map(lambda x: x.serialize(), users))
    return serialized_users, 200

@app.route('/users', methods=['POST'])
def create_user(): 
    request_body = request.get_json()
    newUser = User(email=request_body['email'], password=request_body['password'], is_active=False)
    db.session.add(newUser)
    db.session.commit()
    return jsonify(newUser.serialize()), 200

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id): 
    request_body = request.get_json()
    user_to_update = User.query.get(user_id)
    if (user_to_update is None):
        raise APIException('User not found', status_code=400)
    
    if ('email') in request_body:
        user_to_update.email = request_body['email']

    if ('password') in request_body:
        user_to_update.password = request_body['password']

    if ('is_active') in request_body:
        user_to_update.is_active = request_body['is_active']

    db.session.commit()
    return jsonify(user_to_update.serialize()), 200

@app.route('/users/favorites', methods=['GET'])
def get_favorites(): 
    user = User.query.get(1)
    return user.favorites_characters, 200

@app.route('/people', methods=['GET'])
def get_all_characters():
    characters = Character.query.all()
    serialized_characters = list(map(lambda x: x.serialize(), characters))
    return serialized_characters, 200

@app.route('/people/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Character.query.get(character_id)
    return character.serialize(), 200

@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    serialized_planets = list(map(lambda x: x.serialize(), planets))
    return serialized_planets, 200

@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_planet(planets_id):
    planet = Planet.query.get(planets_id)
    return planet.serialize(), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
