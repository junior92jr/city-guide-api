from chainmock import mocker

from places.services.mappers import OpenStreetMapApiResponse
from places.services.open_street_map import OpenStreetMapClient
from places.services.search import PlaceSearchService


def test_search_places_by_location_fetches_and_maps_payload():
    query_params = {"lat": 50.1101038, "lng": 8.6771586}
    payload = {
        "version": 0.6,
        "elements": [{"type": "node", "id": 1}],
    }
    mocker(OpenStreetMapClient).mock(
        "fetch_places_payload"
    ).called_once_with(query_params).return_value(payload)

    response = PlaceSearchService.search_places_by_location(query_params)

    assert isinstance(response, OpenStreetMapApiResponse)
    assert response.version == 0.6
    assert response.elements[0].id == 1
