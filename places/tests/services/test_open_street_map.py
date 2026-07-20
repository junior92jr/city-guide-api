import httpx
import pytest
from chainmock import mocker

from places.exceptions import OpenStreetMapResourceUnavailable
from places.services import open_street_map
from places.services.cache import OpenStreetMapCache
from places.services.open_street_map import OpenStreetMapClient


def test_build_request_payload_uses_radius_parameter():
    payload = OpenStreetMapClient.build_request_payload({
        "lat": 50.1101038,
        "lng": 8.6771586,
        "search_radious": 1000,
    })

    assert "around:1000,50.1101038,8.6771586" in payload["data"]
    assert '["amenity"]' in payload["data"]


def test_build_request_payload_uses_request_radius():
    payload = OpenStreetMapClient.build_request_payload({
        "lat": 50.1101038,
        "lng": 8.6771586,
        "search_radious": 250,
    })

    assert "around:250,50.1101038,8.6771586" in payload["data"]


def test_headers_uses_configured_user_agent(settings):
    settings.OPEN_STREET_MAP_USER_AGENT = "city-guide-tests"

    assert OpenStreetMapClient.headers() == {
        "Accept": "application/json",
        "User-Agent": "city-guide-tests",
    }


def test_request_places_calls_overpass(settings):
    settings.OPEN_STREET_MAP_OVERPASS_URL = "https://overpass.test/api"
    settings.OPEN_STREET_MAP_USER_AGENT = "city-guide-tests"
    response = httpx.Response(
        httpx.codes.OK,
        json={"elements": []},
        request=httpx.Request("GET", "https://overpass.test/api"),
    )

    mocker(open_street_map.httpx).mock("get").called_once().return_value(response)

    assert OpenStreetMapClient.request_places({
        "lat": 50.1101038,
        "lng": 8.6771586,
        "search_radious": 1000,
    }) == response


def test_request_places_raises_service_unavailable_for_request_errors():
    request = httpx.Request("GET", "https://overpass.test/api")
    mocker(open_street_map.httpx).mock("get").side_effect(
        httpx.ConnectError("connection failed", request=request)
    )

    with pytest.raises(OpenStreetMapResourceUnavailable):
        OpenStreetMapClient.request_places({
            "lat": 50.1101038,
            "lng": 8.6771586,
            "search_radious": 1000,
        })


def test_fetch_places_payload_returns_cached_payload():
    query_params = {
        "lat": 50.1101038,
        "lng": 8.6771586,
        "search_radious": 1000,
    }
    payload = {"elements": []}
    mocker(OpenStreetMapCache).mock("get_payload").called_once_with(
        query_params
    ).return_value(payload)
    mocker(OpenStreetMapClient).mock("request_places").not_called()

    assert OpenStreetMapClient.fetch_places_payload(query_params) == payload


def test_fetch_places_payload_caches_successful_payload():
    query_params = {
        "lat": 50.1101038,
        "lng": 8.6771586,
        "search_radious": 1000,
    }
    payload = {"elements": []}
    response = httpx.Response(
        httpx.codes.OK,
        json=payload,
        request=httpx.Request("GET", "https://overpass.test/api"),
    )
    mocker(OpenStreetMapCache).mock("get_payload").return_value(None)
    mocker(OpenStreetMapClient).mock("request_places").return_value(response)
    mocker(OpenStreetMapCache).mock("set_payload").called_once_with(
        query_params,
        payload,
    )

    assert OpenStreetMapClient.fetch_places_payload(query_params) == payload


def test_fetch_places_payload_raises_service_unavailable_for_error_status():
    response = httpx.Response(
        httpx.codes.INTERNAL_SERVER_ERROR,
        json={"remark": "runtime error"},
        request=httpx.Request("GET", "https://overpass.test/api"),
    )
    mocker(OpenStreetMapCache).mock("get_payload").return_value(None)
    mocker(OpenStreetMapClient).mock("request_places").return_value(response)

    with pytest.raises(OpenStreetMapResourceUnavailable):
        OpenStreetMapClient.fetch_places_payload({
            "lat": 50.1101038,
            "lng": 8.6771586,
            "search_radious": 1000,
        })


def test_fetch_places_payload_raises_service_unavailable_for_non_object_json():
    response = httpx.Response(
        httpx.codes.OK,
        json=[],
        request=httpx.Request("GET", "https://overpass.test/api"),
    )
    mocker(OpenStreetMapCache).mock("get_payload").return_value(None)
    mocker(OpenStreetMapClient).mock("request_places").return_value(response)

    with pytest.raises(OpenStreetMapResourceUnavailable):
        OpenStreetMapClient.fetch_places_payload({
            "lat": 50.1101038,
            "lng": 8.6771586,
            "search_radious": 1000,
        })
