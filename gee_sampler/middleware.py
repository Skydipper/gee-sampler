from functools import wraps
from flask import request
import logging
import json

from gee_sampler.routes.api import error
from gee_sampler.services.geostore_service import GeostoreService
from gee_sampler.errors import GeostoreNotFound

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
        post_body = dict()
        if request.json:
            post_body.update(dict(request.json))
            logging.debug(f"[MIDDLEWARE - post_body]: {post_body}")
        if request.args:
            query_params = dict(request.args)
            logging.debug(f"[MIDDLEWARE - query_params]: {query_params}")
            post_body.update(query_params)
        # Exclude params like loggedUser here
        excluded_params = ['loggedUser']
        sanitized_post_body = remove_keys(excluded_params, post_body)
        logging.debug(f"[MIDDLEWARE - sanitized_post_body]: {sanitized_post_body}")
        kwargs['params'] = sanitized_post_body
        return func(*args, **kwargs)
    return wrapper

def get_geo_by_hash(func):
    """Get geodata"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.method == 'GET':
            geostore = request.args.get('geostore')
            logging.debug('[MIDDLEWARE - geostore]: ' + geostore)
            if not geostore:
                return error(status=400, detail='Geostore is required')
            try:
                geojson = GeostoreService.get(geostore)
            except GeostoreNotFound:
                return error(status=404, detail='Geostore not found')
            kwargs["geojson"] = geojson
        return func(*args, **kwargs)
    return wrapper
