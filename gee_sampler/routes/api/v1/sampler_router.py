"""API ROUTER"""

import logging

from flask import jsonify, Blueprint
from gee_sampler.routes.api import error
from gee_sampler.validators import validate_point_sample
from gee_sampler.middleware import parameters_to_kwargs, get_dataset
from gee_sampler.serializers import serialize_greeting
from gee_sampler.services.gee_service import GEEService
import json
#import CTRegisterMicroserviceFlask

sampler_endpoints = Blueprint('sampler_endpoints', __name__)

@sampler_endpoints.route('/sample', strict_slashes=False, methods=['POST'])
@parameters_to_kwargs
@validate_point_sample
@get_dataset
def point_sample(**kwargs):
    """
    Samples a point on GEE
    """
    sampling_parameters = kwargs['params']
    logging.info('[SAMPLER ROUTER]: ' + str(sampling_parameters))
    try:
        #sampling_result = GEEService.gee_point_sample(sampling_parameters)
        sampling_result = sampling_parameters
    except Exception as e:
        return error(status=404, detail=str(e))
    
    return jsonify(data = sampling_result), 200
