
import hashlib
from django.core.cache import cache

from .constants import CACHE_TIMEOUT_IN_SECS


def store_response_in_cache(func):
    """
    Decorator to store in cache response from inner function.
    """
    
    def wrapper_func(*args, **kwargs):
        cache_key = '{sha1_key}'.format(
            sha1_key=hashlib.sha1(
                '{function_name}-{lat}-{lng}'.format(
                    function_name=func.__name__, 
                    lat=args[1]['lat'], 
                    lng=args[1]['lng']
                ).encode('utf-8')).hexdigest())

        if CACHE_TIMEOUT_IN_SECS != 0 and cache.get(cache_key):
            return cache.get(cache_key)
        else:
            response = func(*args, **kwargs)
            
            if CACHE_TIMEOUT_IN_SECS != 0 and response.status_code == 200:
                cache.set(cache_key, response, CACHE_TIMEOUT_IN_SECS)
            
        return response

    return wrapper_func
