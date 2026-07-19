from unittest.mock import patch
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

OPEN_STREET_MAP_RESPONSE_200 = {
    "elements": [
        {
            "type": "node",
            "id": 660490408,
            "lat": 50.9296019,
            "lon": 6.94194,
            "tags": {
                "historic": "memorial",
                "image": (
                    "https://commons.wikimedia.org/wiki/"
                    "File:Stolpersteine_Koeln_Kurt_Friedlich.jpg"
                ),
                "memorial": "stolperstein",
                "memorial:addr": "Weyerstrasse 122",
                "name": "Kurt Friedlich",
                "website": "https://nsdok.de/Stolpersteine-in-Koeln",
            },
        },
    ],
}

OPEN_STREET_MAP_RESPONSE_500 = {
    "remark": "runtime error",
}


class MockResponse:
    def __init__(self, status_code, payload):
        self.status_code = status_code
        self.payload = payload
        self.text = str(payload)

    def json(self):
        return self.payload


class RecommendationsTestCase(APITestCase):
    """
    Main test case class to handle unit test for the API.
    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test_user', 
            password='12test12', 
            email='test@example.com')
        self.user.save()

        auth_response = self.client.post(
            '/api/v1/api-token-auth/', 
            {'username': 'test_user', 'password': '12test12'}, 
            format='json'
        )

        self.client.credentials(
            HTTP_AUTHORIZATION='Token {token}'.format(
                token=auth_response.json().get('token'))
        )

    def test_get_places_by_location_200(self):
        with patch('requests.get') as mock_request:

            mock_request.return_value = MockResponse(
                status.HTTP_200_OK,
                OPEN_STREET_MAP_RESPONSE_200,
            )

            response = self.client.get(
                '/api/v1/places/', 
                {'lat': '50.1101038', 'lng': '8.6771586'}, 
                format='json'
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(type(response.json()), list)

    def test_get_places_by_location_without_auth_200(self):
        self.client.credentials()
        with patch('requests.get') as mock_request:

            mock_request.return_value = MockResponse(
                status.HTTP_200_OK,
                OPEN_STREET_MAP_RESPONSE_200,
            )

            response = self.client.get(
                '/api/v1/places/', 
                {'lat': '50.1101038', 'lng': '8.6771586'}, 
                format='json'
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_places_by_location_400(self):
        response = self.client.get(
            '/api/v1/places/', 
            {'lat': 'not_valid_param', 'lat': 'not_valid_param'}, 
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_get_places_by_location_500(self):
        with patch('requests.get') as mock_request:
            mock_request.return_value = MockResponse(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                OPEN_STREET_MAP_RESPONSE_500,
            )
            
            response = self.client.get(
                '/api/v1/places/', 
                {'lat': '50.1101038', 'lng': '5.6771586'},
                format='json'
            )

            self.assertEqual(
                response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
