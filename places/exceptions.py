from rest_framework.exceptions import APIException


class FourSquareResourceUnavailable(APIException):
    """
    Custom Exception when Foursquare service returns a different status than 200.
    """

    status_code = 503
    default_detail = "FourSquare resource is not available."
    default_code = "service_unavailable"
