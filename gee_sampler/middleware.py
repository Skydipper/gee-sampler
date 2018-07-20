
from functools import wraps
from flask import request, redirect

def set_something(func):
    """Set something"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        kwargs["something"] = "something"
        return func(*args, **kwargs)
    return wrapper

def get_sample_params(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        kwargs["something"] = "something"
        return func(*args, **kwargs)
    return wrapper
