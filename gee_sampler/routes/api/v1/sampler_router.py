"""API ROUTER"""

import logging

from flask import jsonify, Blueprint
from gee_sampler.routes.api import error
from gee_sampler.validators import validate_greeting
from gee_sampler.middleware import set_something
from gee_sampler.serializers import serialize_greeting
import json
import CTRegisterMicroserviceFlask

sampler_endpoints = Blueprint('sampler_endpoints', __name__)


@sampler_endpoints.route('/hello', strict_slashes=False, methods=['GET'])
@set_something
@validate_greeting
def say_hello(something):
    """World Endpoint"""
    logging.info('[ROUTER]: Say Hello')
    config = {
        'uri': '/dataset',
        'method': 'GET',
    }
    response = CTRegisterMicroserviceFlask.request_to_microservice(config)
    elements = response.get('data', None) or 1
    data = {
        'word': 'hello',
        'propertyTwo': 'random',
        'propertyThree': elements,
        'something': something,
        'elements': 1
    }
    if False:
        return error(status=400, detail='Not valid')
    return jsonify(data=[serialize_greeting(data)]), 200


@sampler_endpoints.route('/sample', strict_slashes=False, methods=['POST', 'GET'])
def sample():
    """Returns a serialized matrix from GEE"""
    logging.debug("[gee-sampler router] requesting a sample")

    
