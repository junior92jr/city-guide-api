from django.core.cache import cache

from places.services.cache import OpenStreetMapCache


def test_build_key_uses_location_and_radius():
    first_key = OpenStreetMapCache.build_key({
        "lat": 50.1101038,
        "lng": 8.6771586,
        "search_radious": 500,
    })
    second_key = OpenStreetMapCache.build_key({
        "lat": 50.1101038,
        "lng": 8.6771586,
        "search_radious": 1000,
    })

    assert first_key != second_key


def test_build_key_uses_default_radius(settings):
    settings.OPEN_STREET_MAP_DEFAULT_RADIUS_IN_METERS = 1000

    explicit_radius_key = OpenStreetMapCache.build_key({
        "lat": 50.1101038,
        "lng": 8.6771586,
        "search_radious": 1000,
    })
    default_radius_key = OpenStreetMapCache.build_key({
        "lat": 50.1101038,
        "lng": 8.6771586,
    })

    assert explicit_radius_key == default_radius_key


def test_get_payload_returns_none_when_cache_is_disabled(settings):
    settings.CACHE_TIMEOUT_IN_SECS = 0
    query_params = {"lat": 50.1101038, "lng": 8.6771586}
    cache.set(OpenStreetMapCache.build_key(query_params), {"elements": []})

    assert OpenStreetMapCache.get_payload(query_params) is None


def test_set_and_get_payload(settings):
    settings.CACHE_TIMEOUT_IN_SECS = 86400
    query_params = {"lat": 50.1101038, "lng": 8.6771586}
    payload = {"elements": [{"type": "node", "id": 1}]}

    OpenStreetMapCache.set_payload(query_params, payload)

    assert OpenStreetMapCache.get_payload(query_params) == payload
