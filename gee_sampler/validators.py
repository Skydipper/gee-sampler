"""VALIDATORS"""

from functools import wraps
from gee_sampler.routes.api import error
import logging
from cerberus import Validator
from datetime import date, datetime

def validate_point_sample(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        validation_schema = {
            'id': {'type': 'string'},
            'type': {
                'type': 'string',
                'allowed': [
                    'Image',
                    'ImageCollection',
                    'FeatureCollection'
                ]
            }
        }

        validator = Validator(validation_schema, allow_unknown = True)
        logging.debug(kwargs['post_body'])
        logging.debug(validator.validate(kwargs['post_body']))
        
        if not validator.validate(kwargs['post_body']):
            logging.debug(validator.errors)
            return error(status=400, detail='Validating something in the middleware')
        return func(*args, **kwargs)
    return wrapper
