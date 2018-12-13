from functools import wraps
from flask import request
import logging
import json

from gee_sampler.routes.api import error
from gee_sampler.errors import DatasetNotFound, ProviderNotFound
from gee_sampler.services.dataset_service import GetDatasetService, GetFieldsService

def remove_keys(keys, dictionary):
    for key in keys:
        try:
            del dictionary[key]
        except KeyError:
            pass
    return dictionary

def gen_dict_extract(key, var):
    if hasattr(var,'items'):
        for k, v in var.items():
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in gen_dict_extract(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in gen_dict_extract(key, d):
                        yield result

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
            return error(status=404, detail='body params not found')
        
        return func(*args, **kwargs)
    return wrapper

def get_dataset(func):
    """Get geodata"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            listOfDatasets = list(set(gen_dict_extract('dataset', kwargs['params'])))
            
            info = [{"dataset": dataset, "data": GetDatasetService.get(dataset), "fields":GetFieldsService.get(dataset)} for dataset in listOfDatasets]

            logging.debug("[MIDDLEWARE - get_dataset]: " + str(info))
            kwargs["datasetsInfo"] = info
        
        except DatasetNotFound: 
            return error(status=404, detail='dataset not found')
        except ProviderNotFound:
            return error(status=404, detail='Provider not found')
        
        return func(*args, **kwargs)
    return wrapper
