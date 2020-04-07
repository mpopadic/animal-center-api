import json
from flask import current_app as app
from flask import jsonify, request, Response

from models import Species
from .center import token_required


@app.route('/species', methods=['GET'])
def get_species():
    return jsonify({'species': Species.get_all_species()})


@app.route('/species/<int:id>')
def get_speceies_by_id(id):
    species = Species.get_species_by_id(id)
    return jsonify(species)


@app.route('/species', methods=['POST'])
@token_required
def add_species():
    request_data = request.get_json()
    if Species.is_valid_object(request_data):
        try:
            Species.add_species(request_data['name'], request_data['description'], request_data['price'])
            response = Response('', status=201, mimetype='application/json')
            return response
        except TypeError as te:
            return Response(json.dumps({"error": "{}".format(te)}), 400, mimetype='application/json')
    else:
        invalid_obj = {
            'error': "Valid Species must contain: name, description and price"
        }
        response = Response(json.dumps(invalid_obj), 400)
        return response

