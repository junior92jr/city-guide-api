from unittest.mock import patch
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from .mocks.foursquare_places_v3_mock import (
    FOURSQUARE_PLACES_V3_MOCK_200, 
    FOURSQUARE_PLACES_V3_MOCK_500
)


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

            mock_request.return_value.status_code = status.HTTP_200_OK
            mock_request.return_value.content = FOURSQUARE_PLACES_V3_MOCK_200

            response = self.client.get(
                '/api/v1/places/', 
                {'lat': '50.1101038', 'lng': '8.6771586'}, 
                format='json'
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(type(response.json()), list)

    def test_get_places_by_location_401(self):
        self.client.credentials()
        with patch('requests.get') as mock_request:

            mock_request.return_value.status_code = status.HTTP_200_OK
            mock_request.return_value.content = FOURSQUARE_PLACES_V3_MOCK_200

            response = self.client.get(
                '/api/v1/places/', 
                {'lat': '50.1101038', 'lng': '8.6771586'}, 
                format='json'
            )
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_places_by_location_400(self):
        response = self.client.get(
            '/api/v1/places/', 
            {'lat': 'not_valid_param', 'lat': 'not_valid_param'}, 
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_get_places_by_location_500(self):
        with patch('requests.get') as mock_request:
            mock_request.return_value.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            mock_request.return_value.content = FOURSQUARE_PLACES_V3_MOCK_500
            
            response = self.client.get(
                '/api/v1/places/', 
                {'lat': '50.1101038', 'lng': '5.6771586'},
                format='json'
            )

            self.assertEqual(
                response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
