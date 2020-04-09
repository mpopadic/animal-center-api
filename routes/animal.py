import json
from flask import current_app as app
from flask import jsonify, request, Response

from models import Animal, Species, Center
from .center import token_required
from logger import write_to_log_file

@app.route('/animals', methods=['GET'])
def get_animals():
    return jsonify({'animals': Animal.get_all_animals()})


@app.route('/animals/<int:id>', methods=['GET'])
def get_animal_by_id(id):
    animal = Animal.get_animal_by_id(id)
    return jsonify(animal)


@app.route('/animals', methods=['POST'])
@token_required
def add_animal(caller_id):

    request_data = request.get_json()

    response = check_if_object_is_good(request_data)
    if response:
        return response

    # If request_data is ok, proceed with adding animal
    try:
        new_animal = Animal.add_animal(request_data['name'],
                                       caller_id,
                                       request_data['age'],
                                       request_data['species'],
                                       request_data['price'],
                                       request_data['description'])
        response = Response('', status=201, mimetype='application/json')
        write_to_log_file(request.method, request.path, caller_id, 'Animal', "create", new_animal.id)
        return response
    except TypeError as te:
        return Response(json.dumps({"error": "{}".format(te)}), 400, mimetype='application/json')


@app.route('/animals<int:id>', methods=['PATCH'])
@token_required
def update_animal(id, caller_id):
    request_data = request.get_json()
    try:
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
        write_to_log_file(request.method, request.path, caller_id, 'Animal', "update", id)
    except TypeError as te:
        return Response(json.dumps({"error": "{}".format(te)}), 400, mimetype='application/json')

    replaced_animal = Animal.query.filter_by(id=id).first()
    return Response(json.dumps({Animal.json(replaced_animal)}), status=201, mimetype='application/json')


@app.route('/animals/<int:id>', methods=['PUT'])
@token_required
def replace_animal(id, caller_id):
    request_data = request.get_json()

    response = check_if_object_is_good(request_data)
    if response:
        return response

    # If request_data is ok, proceed with replacing animal
    try:
        Animal.replace_animal(id,
                              caller_id,
                              request_data['name'],
                              request_data['age'],
                              request_data['species'],
                              request_data['price'],
                              request_data['description'])
        write_to_log_file(request.method, request.path, caller_id, 'Animal', "replace", replace_animal.id)
        return Response('', status=201, mimetype='application/json')
    except TypeError as te:
        return Response(json.dumps({"error": "{}".format(te)}), 400, mimetype='application/json')


@app.route('/animals/<int:id>', methods=['DELETE'])
@token_required
def delete_animal(id, caller_id):
    owner = Center.query.filter_by(id=caller_id).first()
    if id in [animal.id for animal in owner.animals]:
        if Animal.delete_animal(id):
            write_to_log_file(request.method, request.path, caller_id, 'Animal', "delete", id)
            return Response("", status=204)
    else:
        return Response(json.dumps({"error": "You don't have rights to delete this animal"}),
                        status=400,
                        mimetype='application/json')

    return Response(json.dumps({"error": "Unable to delete Animal with id {0}.".format(id)}),
                    status=400,
                    mimetype='application/json')


def check_if_object_is_good(request_data):
    # Check if all fields are there
    if not Animal.is_valid_object(request_data):
        invalid_obj = {
            'error': "Valid Animal must contain: name, center_id, age and species"
        }
        return Response(json.dumps(invalid_obj), 400)

    # Check if species with given id exist
    species = Species.query.filter_by(id=request_data['species']).first()
    if not species:
        error_object = {
            "error": "Species with id {} doesn't exist. You must create species first.".format(request_data['species'])
        }
        return Response(json.dumps(error_object), 400)

    return None
