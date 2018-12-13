from functools import wraps
from flask import request
import logging
import json

from gee_sampler.routes.api import error
from gee_sampler.errors import DatasetNotFound, ProviderNotFound
from gee_sampler.services.dataset_service import GetDatasetService

def remove_keys(keys, dictionary):
    for key in keys:
        try:
            del dictionary[key]
        except KeyError:
            pass
    return dictionary

def parameters_to_kwargs(func):
    """Sets any queryparams in the kwargs"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            post_body = dict()
            if request.json:
                post_body.update(dict(request.json))
            # Exclude params like loggedUser here
            sanitized_post_body = remove_keys(['loggedUser'], post_body)
            kwargs['params'] = sanitized_post_body
        
        except DatasetNotFound:
            logging.debug(f"[MIDDLEWARE - sanitized_post_body]: {sanitized_post_body}")
            return error(status=404, detail='params not found')
        
        return func(*args, **kwargs)
    return wrapper

def get_dataset(func):
    """Get geodata"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            info = GetDatasetService.get('2da73658-31b6-44a9-9c05-ca951e50dbb0')

            logging.debug("[MIDDLEWARE - get_dataset]: " + str(info))
            kwargs["test"] = info
        
        except DatasetNotFound: 
            return error(status=404, detail='Geostore not found')
        except ProviderNotFound:
            return error(status=404, detail='Provider not found')
        
        return func(*args, **kwargs)
    return wrapper
