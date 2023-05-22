"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    response_body = {
        "family": members
    }
    return jsonify(response_body), 200

@app.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member_by_id(member_id)
    if member is None:
        raise APIException("Member not found", status_code=404)
    return jsonify(member), 200

@app.route('/members', methods=['POST'])
def add_member():
    new_member = request.json  
    jackson_family.add_member(new_member)  
    return jsonify(new_member), 201 

@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    member = jackson_family.get_member_by_id(member_id)  # Obtener el miembro de la familia por su ID
    if member is None:
        raise APIException("Member not found", status_code=404)  # Si el miembro no se encuentra, lanzar una excepción

    jackson_family.delete_member(member_id)  # Eliminar el miembro de la familia

    return jsonify({"message": "Member deleted successfully"}), 200  # Devolver una respuesta JSON con un mensaje de éxito y el código de estado 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    personas = [
        {
            "first_name": "John",
            "age": 33,
            "lucky_numbers": [7, 13, 22]
        },
        {
            "first_name": "Jane",
            "age": 35,
            "lucky_numbers": [10, 14, 3]
        },
        {
            "first_name": "Jimmy",
            "age": 5,
            "lucky_numbers": [1]
        }
    ]

    for p in personas:
        jackson_family.add_member(p)

    app.run(host='0.0.0.0', port=PORT, debug=True)
