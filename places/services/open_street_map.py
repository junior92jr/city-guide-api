from typing import Any, NotRequired, TypedDict

import httpx

from django.conf import settings
from rest_framework.exceptions import APIException

from . import cache
from .categories import get_active_osm_category_tags

TIMEOUT_IN_SECONDS = 10.0


class PlaceQueryParams(TypedDict):
    lat: float
    lng: float
    search_radious: int
    category: NotRequired[str]


OpenStreetMapPayload = dict[str, Any]


class OpenStreetMapResourceUnavailable(APIException):
    """
    Raised when the OpenStreetMap service is unavailable or returns bad data.
    """

    status_code = 503
    default_detail = "OpenStreetMap resource is not available."
    default_code = "service_unavailable"


def request_places(query_params: PlaceQueryParams) -> httpx.Response:
    """
    Connection with the OpenStreetMap Overpass API.
    """

    try:
        return httpx.get(
            settings.OPEN_STREET_MAP_OVERPASS_URL,
            headers=headers(),
            params=build_request_payload(query_params),
            timeout=TIMEOUT_IN_SECONDS,
        )
    except httpx.RequestError as exc:
        raise OpenStreetMapResourceUnavailable() from exc


def fetch_places_payload(
    query_params: PlaceQueryParams,
) -> OpenStreetMapPayload:
    cached_payload = cache.get_payload(query_params)

    if cached_payload is not None:
        return cached_payload

    response = request_places(query_params)

    if response.status_code != httpx.codes.OK:
        raise OpenStreetMapResourceUnavailable()

    try:
        payload = response.json()
    except ValueError as exc:
        raise OpenStreetMapResourceUnavailable() from exc

    if not isinstance(payload, dict):
        raise OpenStreetMapResourceUnavailable()

    cache.set_payload(query_params, payload)

    return payload


def build_request_payload(query_params: PlaceQueryParams) -> dict[str, str]:
    return {
        "data": build_overpass_query(
            lat=query_params["lat"],
            lng=query_params["lng"],
            radius=query_params["search_radious"],
        )
    }


def build_overpass_query(lat: float, lng: float, radius: int) -> str:
    osm_tags = get_active_osm_category_tags()

    if not osm_tags:
        raise OpenStreetMapResourceUnavailable()

    filters = "\n".join(
        f'  nwr(around:{radius},{lat},{lng})["{key}"="{value}"];'
        for key, value in osm_tags
    )

    return f"""
            [out:json][timeout:25];
            (
            {filters}
            );
            out center tags qt 50;
            """


def headers() -> dict[str, str]:
    return {
        "Accept": "application/json",
        "User-Agent": settings.OPEN_STREET_MAP_USER_AGENT,
    }
