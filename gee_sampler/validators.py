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
            'point': {
                'type': 'list',
                'required': True,
                'items': [{'type': 'float', 'min':-180, 'max':180}, 
                          {'type': 'float', 'min':-90, 'max':90}]
            },
            'type':{
                'type': 'string',
                'required': True,
                'allowed': [
                    'segmentation'
                ]
            },
            'sources': {
                'type': 'list',
                'required': True,
                 'schema': {'type': 'dict', 
                            'schema': {'dataset': {'type': 'string', 
                                                    'required': True},
                                       'bands': {'type': 'list', 
                                                 'required': True,
                                                 'schema': {'type': 'dict',
                                                            'schema': {'name': {'type': 'string', 'required': True},
                                                                        'origin': {'type': 'string', 'required': True},
                                                                        'transform': {'type': 'string', 'required': False},
                                                                        'transformArg': {'type': 'dict', 
                                                                                         'required': False,
                                                                                         'schema': { 'min': {'type': 'float'},
                                                                                                    'max': {'type': 'float'}
                                                                                                    }
                                                                                         }
                                                                     }
                                                            }
                                                 }
                                   }
                           }
                },
            'target': {
                'type': 'dict',
                'required': True,
                'schema': {'dataset': {'type': 'string', 
                                                    'required': True},
                            'bands': {'type': 'list', 
                                      'required': True,
                                      'schema': {'type': 'dict',
                                                 'schema': {'name': {'type': 'string', 'required': True},
                                                            'origin': {'type': 'string', 'required': True},
                                                            'transform': {'type': 'string', 'required': False},
                                                            'transformArg': {'type': 'dict', 
                                                                             'required': False,
                                                                             'schema': { 'min': {'type': 'float'},
                                                                                         'max': {'type': 'float'}
                                                                                         }
                                                                            }
                                                            }
                                                    }
                                        }
                         }
            },
            'buffer': {
                'type': 'number',
                'required': False,
                'default': 300,
                'coerce': int,
                'min': 1,
                'max': 50000
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
