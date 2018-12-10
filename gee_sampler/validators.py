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
        to_dict = lambda v: v.lower() in ('true', '1')
        validation_schema = {
            'geostore': {
                'type': 'string',
                'required': False
            },
            'trainIn': {
                'type': 'string',
                'allowed': [
                    'Sentinel2',
                    'Landsat7'
                ],
                'required': True
            },
            'trainOut': {
                'type': 'string',
                'allowed': [
                    'CroplandDataLayers'
                ],
                'required': True
            },
            'date': {
                'type': 'dict',
                'schema': {
                    'min': {'type': ['date', 'string']},
                    'max': {'type': ['date', 'string']}
                },
                'required': True
            },
            'buffer': {
                'type': 'number',
                'required': False,
                'default': 30,
                'coerce': int,
                'min': 1,
                'max': 50000
            },
            'scale': {
                'type': 'number',
                'required': False,
                'default': 30,
                'coerce': int,
                'min': 0
            }
        }
        logging.info(f"[VALIDATOR - sanitized_post_body]: {kwargs}")
        validator = Validator(validation_schema, allow_unknown = True)
        if not validator.validate(kwargs['params']):
            return error(status=400, detail=validator.errors)
        kwargs['sanitized_params'] = validator.normalized(kwargs['params'])
        logging.debug(f"sanitized_post_body: {kwargs['sanitized_params']}")
        return func(*args, **kwargs)
    return wrapper

def validate_geojson(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        validation_schema = {
            'keyschema': {'type': 'string', 'oneof':['geostore', 'geojson']},
            'geostore': {
                'type': 'string',
                'required': False
            },
            'geojson': {
                'type': 'string',
                'required': False
            },
            'trainIn': {
                'type': 'string',
                'allowed': [
                    'Sentinel2',
                    'Landsat7'
                ],
                'required': True
            },
            'trainOut': {
                'type': 'string',
                'allowed': [
                    'CroplandDataLayers'
                ],
                'required': True
            },
            'date': {
                'type': 'dict',
                'schema': {
                    'min': {'type': ['date', 'string']},
                    'max': {'type': ['date', 'string']}
                },
                'required': True
            },
            'buffer': {
                'type': 'number',
                'required': False,
                'default': 30,
                'min': 1,
                'max': 50000
            },
            'scale': {
                'type': 'number',
                'required': False,
                'default': 30,
                'min': 0
            }
        }
        validator = Validator(validation_schema, allow_unknown = True)
        if not validator.validate(kwargs['post_body']):
            return error(status=400, detail=validator.errors)
        kwargs['sanitized_post_body'] = validator.normalized(kwargs['post_body'])
        logging.debug(f"sanitized_post_body: {kwargs['sanitized_post_body']}")
        return func(*args, **kwargs)
    return wrapper
