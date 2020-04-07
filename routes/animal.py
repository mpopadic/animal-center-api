import json
from flask import current_app as app
from flask import jsonify, request, Response

from models import Animal


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
        Animal.add_animal(request_data['name'], request_data['center_id'], request_data['age'], request_data['species'], request_data['price'], request_data['description'])
        response = Response('', status=201, mimetype='application/json')
        return response
    else:
        invalid_obj = {
            'error': "Valid Animal must contain: name, center_id, age and species"
        }
        response = Response(json.dumps(invalid_obj), 400)
        return response

