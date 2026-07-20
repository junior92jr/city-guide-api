from places.services.mappers import OpenStreetMapApiResponse


def test_open_street_map_api_response_maps_metadata_and_elements():
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

    assert response.version == 0.6
    assert response.osm3s is not None
    assert response.osm3s.timestamp_osm_base == "2026-07-20T19:38:18Z"
    assert response.elements[0].lat == 51.9322712
    assert response.elements[0].tags["name"] == "Heiliger Ludgerus"
    assert response.elements[1].center is not None
    assert response.elements[1].center.lon == 6.9464483


def test_open_street_map_api_response_preserves_extra_fields():
    response = OpenStreetMapApiResponse.from_api_response({
        "elements": [
            {
                "type": "relation",
                "id": 19574608,
                "members": [{"type": "way", "ref": 123}],
            }
        ],
        "remark": "extra field",
    })
    dumped_response = response.model_dump()

    assert dumped_response["remark"] == "extra field"
    assert dumped_response["elements"][0]["members"] == [
        {"type": "way", "ref": 123}
    ]
