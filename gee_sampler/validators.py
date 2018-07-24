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
                ]
            },
            'date': {
                'type': 'dict',
                'schema': {
                    'min': {'type': ['date', 'string']},
                    'max': {'type': ['date', 'string']}
                }
            }
        }
        validator = Validator(validation_schema, allow_unknown = True)
        if not validator.validate(kwargs['post_body']):
            return error(status=400, detail=validator.errors)
        return func(*args, **kwargs)
    return wrapper
