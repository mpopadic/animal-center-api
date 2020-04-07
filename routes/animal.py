import json
from flask import current_app as app
from flask import jsonify, request, Response

from models import Animal, Species
from .center import token_required


@app.route('/animals', methods=['GET'])
def get_animals():
    return jsonify({'animals': Animal.get_all_animals()})


@app.route('/animals/<int:id>')
def get_animal_by_id(id):
    animal = Animal.get_animal_by_id(id)
    return jsonify(animal)


@app.route('/animals', methods=['POST'])
@token_required
def add_animal(caller_id):
    request_data = request.get_json()
    if Animal.is_valid_object(request_data):
        species = Species.query.filter_by(id=request_data['species']).first()
        if species:
            Animal.add_animal(request_data['name'],
                              caller_id,
                              request_data['age'],
                              species.id,
                              request_data['price'],
                              request_data['description'])
            response = Response('', status=201, mimetype='application/json')
            return response
        else:
            error_object = {
                "error": "Species with id {} doesn't exist. You must create species first.".format(request_data['species'])
            }
            return Response(json.dumps(error_object), 400)

    else:
        invalid_obj = {
            'error': "Valid Animal must contain: name, center_id, age and species"
        }
        return Response(json.dumps(invalid_obj), 400)


@app.route('/animals<int:id>', methods=['PATCH'])
@token_required
def update_animal(id, caller_id):
    request_data = request.get_json()
    Animal.update_animal_center_id(id, caller_id)
    if 'name' in request_data:
        Animal.update_animal_name(id, request_data['name'])
    if 'age' in request_data:
        Animal.update_animal_age(id, request_data['age'])
    if 'species' in request_data:
        species = Species.query.filter_by(id=request_data['species']).first()
        if species:
            Animal.update_animal_species(id, request_data['species'])
    if 'price' in request_data:
        Animal.update_animal_price(id, request_data['price'])
    if 'description' in request_data:
        Animal.update_animal_description(id, request_data['description'])

    replaced_animal = Animal.query.filter_by(id=id).first()
    return Response(json.dumps({Animal.json(replaced_animal)}), status=201, mimetype='application/json')


@app.route('/animals/<int:id>', methods=['PUT'])
@token_required
def replace_animal(id, caller_id):
    request_data = request.get_json()
    if Animal.is_valid_object(request_data):
        species = Species.query.filter_by(id=request_data['species']).first()
        if species:
            Animal.replace_animal(id,
                                  caller_id,
                                  request_data['name'],
                                  request_data['age'],
                                  species.id,
                                  request_data['price'],
                                  request_data['description'])
            response = Response('', status=201, mimetype='application/json')
            return response
        else:
            error_object = {
                "error": "Species with id {} doesn't exist. You must create species first.".format(request_data['species'])
            }
            return Response(json.dumps(error_object), 400)
    else:
        invalid_obj = {
            'error': "Valid Animal must contain: name, center_id, age and species"
        }
        return Response(json.dumps(invalid_obj), 400)