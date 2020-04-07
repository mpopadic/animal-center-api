import json
from flask import current_app as app
from flask import jsonify, request, Response

from models import Animal, Species


@app.route('/animals', methods=['GET'])
def get_animals():
    return jsonify({'animals': Animal.get_all_animals()})


@app.route('/animals/<int:id>')
def get_animal_by_id(id):
    animal = Animal.get_animal_by_id(id)
    return jsonify(animal)

@app.route('/animals', methods=['POST'])
def add_animal():
    request_data = request.get_json()
    if Animal.is_valid_object(request_data):
        species = Species.query.filter_by(id=request_data['species']).first()
        if species:
            Animal.add_animal(request_data['name'],
                              request_data['center_id'],
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


