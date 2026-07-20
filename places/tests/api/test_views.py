import pytest
from chainmock import mocker
from rest_framework import status
from rest_framework.test import APIClient

from places.services.mappers import OpenStreetMapApiResponse
from places.views import PlaceSearchService


@pytest.fixture
def api_client():
    return APIClient()


def test_places_returns_mapped_open_street_map_response(api_client):
    query_params = {"lat": 50.1101038, "lng": 8.6771586}
    service_response = OpenStreetMapApiResponse.from_api_response({
        "version": 0.6,
        "generator": "Overpass API",
        "elements": [
            {
                "type": "node",
                "id": 331124761,
                "lat": 51.9322712,
                "lon": 6.9442418,
                "tags": {"name": "Heiliger Ludgerus"},
            },
        ],
    })
    mocker(PlaceSearchService).mock(
        "search_places_by_location"
    ).called_once_with(query_params).return_value(service_response)

    response = api_client.get("/api/v1/places/", {
        "lat": "50.1101038",
        "lng": "8.6771586",
    })

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "version": 0.6,
        "generator": "Overpass API",
        "elements": [
            {
                "type": "node",
                "id": 331124761,
                "lat": 51.9322712,
                "lon": 6.9442418,
                "tags": {"name": "Heiliger Ludgerus"},
            },
        ],
    }


def test_places_passes_optional_radius_to_search_service(api_client):
    query_params = {
        "lat": 50.1101038,
        "lng": 8.6771586,
        "search_radious": 250,
    }
    service_response = OpenStreetMapApiResponse.from_api_response({
        "elements": [],
    })
    mocker(PlaceSearchService).mock(
        "search_places_by_location"
    ).called_once_with(query_params).return_value(service_response)

    response = api_client.get("/api/v1/places/", {
        "lat": "50.1101038",
        "lng": "8.6771586",
        "search_radious": "250",
    })

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"elements": []}


def test_places_returns_bad_request_for_invalid_query_params(api_client):
    mocker(PlaceSearchService).mock("search_places_by_location").not_called()

    response = api_client.get("/api/v1/places/", {
        "lat": "not-a-float",
        "lng": "8.6771586",
    })

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "lat" in response.json()


def test_categories_endpoint_is_not_registered(api_client):
    response = api_client.get("/api/v1/categories/", {
        "lat": "50.1101038",
        "lng": "8.6771586",
    })

    assert response.status_code == status.HTTP_404_NOT_FOUND
