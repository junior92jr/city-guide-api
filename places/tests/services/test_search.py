import pytest
from chainmock import mocker

from places.services import search
from places.services.mappers import OpenStreetMapApiResponse

pytestmark = pytest.mark.django_db


def test_search_places_by_location_fetches_and_maps_payload():
    query_params = {
        "lat": 50.1101038,
        "lng": 8.6771586,
        "search_radious": 1000,
    }
    payload = {
        "version": 0.6,
        "elements": [
            {
                "type": "node",
                "id": 1,
                "lat": 51.9322712,
                "lon": 6.9442418,
                "tags": {
                    "historic": "wayside_shrine",
                    "name": "Heiliger Ludgerus",
                },
            }
        ],
    }
    mocker(search).mock(
        "fetch_places_payload"
    ).called_once_with(query_params).return_value(payload)

    response = search.search_places_by_location(query_params)

    assert isinstance(response, OpenStreetMapApiResponse)
    assert response.places[0].osm_id == 1
    assert response.places[0].name == "Heiliger Ludgerus"


def test_search_places_by_location_filters_by_category():
    query_params = {
        "lat": 50.1101038,
        "lng": 8.6771586,
        "search_radious": 1000,
        "category": "parking",
    }
    payload = {
        "elements": [
            {
                "type": "node",
                "id": 1,
                "lat": 51.9322712,
                "lon": 6.9442418,
                "tags": {"historic": "wayside_shrine"},
            },
            {
                "type": "way",
                "id": 2,
                "center": {"lat": 51.9428394, "lon": 6.9464483},
                "tags": {"amenity": "parking"},
            },
        ],
    }
    mocker(search).mock(
        "fetch_places_payload"
    ).called_once_with(query_params).return_value(payload)

    response = search.search_places_by_location(query_params)

    assert len(response.places) == 1
    assert response.places[0].category == "parking"
