"""API ROUTER"""

import logging

from flask import jsonify, Blueprint
from gee_sampler.routes.api import error
from gee_sampler.validators import validate_point_sample
from gee_sampler.middleware import parameters_to_kwargs
from gee_sampler.serializers import serialize_greeting
from gee_sampler.services.gee_service import GEEService
import json
import CTRegisterMicroserviceFlask

sampler_endpoints = Blueprint('sampler_endpoints', __name__)


@sampler_endpoints.route('/hello', strict_slashes=False, methods=['GET'])
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

@sampler_endpoints.route('/sample', strict_slashes=False, methods=['GET', 'POST'])
@parameters_to_kwargs
@validate_point_sample
def point_sample(**kwargs):
    """
    Samples a point on GEE
    """
    sampling_parameters = kwargs['post_body']
    logging.debug(f"sampling parameters are: {sampling_parameters}")
    try:
        sampling_result = GEEService.gee_point_sample(sampling_parameters)
    except Exception as e:
        return error(status=404, detail=str(e))
    return jsonify(data = sampling_result), 200
