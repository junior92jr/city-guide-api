from rest_framework.exceptions import APIException


class OpenStreetMapResourceUnavailable(APIException):
    """
    Custom Exception when OpenStreetMap service returns a different status than 200.
    """

    status_code = 503
    default_detail = "OpenStreetMap resource is not available."
    default_code = "service_unavailable"
