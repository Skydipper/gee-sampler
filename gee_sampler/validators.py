"""VALIDATORS"""

from functools import wraps
from gee_sampler.routes.api import error
import logging
from cerberus import Validator
from cerberus.errors import ValidationError
from datetime import date, datetime

def validate_point_sample(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        validation_schema = {
            'id': {
                'type': 'string',
                'required': True
            },
            'type': {
                'type': 'string',
                'allowed': [
                    'Image',
                    'ImageCollection',
                    'FeatureCollection'
                ],
                'required': True
            },
            'date': {
                'type': 'dict',
                'schema': {
                    'min': {'type': ['date', 'string']},
                    'max': {'type': ['date', 'string']}
                }
            },
            'reducer': {
                'type': 'string',
                'allowed': [
                    'mean',
                    'minMax'
                ],
                'required': True
            },
            'scale': {
                'type': 'number',
                'required': False,
                'default': 30
            },
            'scale': {
                'type': 'number',
                'required': False,
                'default': 5000
            }
        }
        validator = Validator(validation_schema, allow_unknown = True)
        if not validator.validate(kwargs['post_body']):
            return error(status=400, detail=validator.errors)
        kwargs['sanitized_post_body'] = validator.normalized(kwargs['post_body'])
        logging.debug(f"sanitized_post_body: {kwargs['sanitized_post_body']}")
        return func(*args, **kwargs)
    return wrapper
