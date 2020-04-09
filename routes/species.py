import json
from flask import current_app as app
from flask import jsonify, request, Response

from models import Species
from .center import token_required
from logger import write_to_log_file

@app.route('/species', methods=['GET'])
def get_species():
    return jsonify({'species': Species.get_all_species()})


@app.route('/species/<int:id>')
def get_species_by_id(id):
    species = Species.get_species_by_id(id)
    return jsonify(species)


@app.route('/species', methods=['POST'])
@token_required
def add_species(caller_id):
    request_data = request.get_json()

    # Check if request_data is valid Species object
    if not Species.is_valid_object(request_data):
        invalid_obj = {
            'error': "Valid Species must contain: name, description and price"
        }
        return Response(json.dumps(invalid_obj), 400)

    # If all ok, try to create new species
    try:
        new_species = Species.add_species(request_data['name'], request_data['description'], request_data['price'])
        write_to_log_file(request.method, request.path, caller_id, 'Animal', "create", new_species.id)
        return Response('', status=201, mimetype='application/json')
    except TypeError as te:
        return Response(json.dumps({"error": "{}".format(te)}), 400, mimetype='application/json')
