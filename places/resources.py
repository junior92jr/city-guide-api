import requests

from django.conf import settings

from .decorators import store_response_in_cache
from .exceptions import FourSquareResourceUnavailable
from .mixins import FourSquareUtilsMixin
from .constants import (
    FOURSQUARE_API_PROTOCOL,
    FOURSQUARE_API_DOMAIN,
    FOURSQUARE_API_VERSION,
)


class FourSquareResource(FourSquareUtilsMixin):
    """
    FourSquare Resource class with functions to get data from external api.
    """

    api_url = '{protocol}://{domain}/{version}'.format(
        protocol=FOURSQUARE_API_PROTOCOL,
        domain=FOURSQUARE_API_DOMAIN,
        version=FOURSQUARE_API_VERSION
    )

    @classmethod
    @store_response_in_cache
    def four_square_request(cls, query_params):
        """
        Connection with Four square api service.
        
        :param query_params: Dictionary with parameters from original request.

        :return: Response object from requests library.
        """

        headers = {
            "Accept": "application/json",
            "Authorization": settings.FOURSQUARE_API_KEY
        }
        
        payload = {
            'll': '{lat},{lng}'.format(
                lat=query_params['lat'], 
                lng=query_params['lng']
            )
        }

        response = requests.get(
            '{api_url}/{endpoint}'.format(
                api_url=cls.api_url, 
                endpoint='places/search'), 
            headers=headers, params=payload
        )
        
        return response
    
    @classmethod
    def search_places_by_location(cls, query_params):
        """
        Get Places from External API.
        
        :param query_params: Dictionary with parameters from original request.

        :return: List of items accessed from original request.
        """

        response = cls.four_square_request(query_params)

        if response.status_code != 200:
            raise FourSquareResourceUnavailable()

        return response.json()['results']
