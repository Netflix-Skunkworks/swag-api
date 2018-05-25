from flask import jsonify


def not_found_response(swag_type):

	return {swag_type: 'Not found'}, 404