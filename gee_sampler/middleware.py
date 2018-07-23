from functools import wraps
from flask import request
import logging
import json

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
        post_body = dict(request.json)
        logging.debug(f"post_body: {post_body}")
        query_params = dict(request.args)
        logging.debug(f"query_params: {query_params}")
        post_body.update(query_params)
        # Exclude params like loggedUser here
        excluded_params = ['loggedUser']
        sanitized_post_body = remove_keys(excluded_params, post_body)
        logging.debug(f"sanitized_post_body: {sanitized_post_body}")
        kwargs['post_body'] = sanitized_post_body
        return func(*args, **kwargs)
    return wrapper
