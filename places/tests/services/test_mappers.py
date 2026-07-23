import pytest

from places.services.mappers import OpenStreetMapApiResponse

pytestmark = pytest.mark.django_db


def test_open_street_map_api_response_maps_flat_places():
    payload = {
        "version": 0.6,
        "generator": "Overpass API",
        "osm3s": {
            "timestamp_osm_base": "2026-07-20T19:38:18Z",
            "copyright": "ODbL",
        },
        "elements": [
            {
                "type": "node",
                "id": 331124761,
                "lat": 51.9322712,
                "lon": 6.9442418,
                "tags": {
                    "historic": "wayside_shrine",
                    "name": "Heiliger Ludgerus",
                },
            },
            {
                "type": "way",
                "id": 270799907,
                "center": {"lat": 51.9428394, "lon": 6.9464483},
                "tags": {"amenity": "parking"},
            },
        ],
    }

    response = OpenStreetMapApiResponse.from_api_response(payload)

    assert response.model_dump(exclude_none=True) == {
        "places": [
            {
                "osm_id": 331124761,
                "osm_type": "node",
                "name": "Heiliger Ludgerus",
                "latitude": 51.9322712,
                "longitude": 6.9442418,
                "category": "wayside-shrine",
                "category_name": "Wayside Shrine",
                "osm_uid": "osm-node-331124761",
            },
            {
                "osm_id": 270799907,
                "osm_type": "way",
                "name": "Unnamed Parking",
                "latitude": 51.9428394,
                "longitude": 6.9464483,
                "category": "parking",
                "category_name": "Parking",
                "osm_uid": "osm-way-270799907",
            },
        ]
    }


def test_open_street_map_api_response_maps_optional_flat_fields():
    response = OpenStreetMapApiResponse.from_api_response({
        "elements": [
            {
                "type": "way",
                "id": 1202107660,
                "center": {"lat": 51.9419245, "lon": 6.9468494},
                "tags": {
                    "addr:city": "Gescher",
                    "addr:housenumber": "41",
                    "addr:postcode": "48712",
                    "addr:street": "Estern",
                    "amenity": "recycling",
                    "name": "Wertstoffhof Gescher/Velen",
                    "opening_hours": "Mo-Fr 08:00-16:30; Sa 08:00-13:00",
                    "website": "https://www.egw.de",
                },
            }
        ],
    })
    place = response.places[0]

    assert place.name == "Wertstoffhof Gescher/Velen"
    assert place.address == "Estern, 41, 48712, Gescher"
    assert place.website == "https://www.egw.de"
    assert place.opening_hours == "Mo-Fr 08:00-16:30; Sa 08:00-13:00"


def test_open_street_map_api_response_skips_elements_without_coordinates():
    response = OpenStreetMapApiResponse.from_api_response({
        "elements": [
            {
                "type": "relation",
                "id": 19574608,
                "tags": {"name": "No coordinates"},
            }
        ],
    })

    assert response.places == []


def test_open_street_map_api_response_skips_unknown_categories():
    response = OpenStreetMapApiResponse.from_api_response({
        "elements": [
            {
                "type": "node",
                "id": 242701473,
                "lat": 51.941288,
                "lon": 6.9474951,
                "tags": {"amenity": "bench"},
            }
        ],
    })

    assert response.places == []
