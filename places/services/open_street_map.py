from typing import ClassVar

import httpx

from django.conf import settings

from places.exceptions import OpenStreetMapResourceUnavailable

from .cache import OpenStreetMapCache
from .types import OpenStreetMapPayload, PlaceQueryParams


class OpenStreetMapClient:
    """
    OpenStreetMap client for requesting Overpass API responses.
    """

    category_tags: ClassVar[tuple[str, ...]] = (
        "amenity",
        "tourism",
        "shop",
        "leisure",
        "historic",
    )
    timeout_in_seconds: ClassVar[float] = 10.0

    @classmethod
    def request_places(cls, query_params: PlaceQueryParams) -> httpx.Response:
        """
        Connection with the OpenStreetMap Overpass API.

        :param query_params: Dictionary with parameters from original request.

        :return: Response object from httpx library.
        """

        try:
            return httpx.get(
                settings.OPEN_STREET_MAP_OVERPASS_URL,
                headers=cls.headers(),
                params=cls.build_request_payload(query_params),
                timeout=cls.timeout_in_seconds,
            )
        except httpx.RequestError as exc:
            raise OpenStreetMapResourceUnavailable() from exc

    @classmethod
    def fetch_places_payload(
        cls,
        query_params: PlaceQueryParams,
    ) -> OpenStreetMapPayload:
        cached_payload = OpenStreetMapCache.get_payload(query_params)

        if cached_payload is not None:
            return cached_payload

        response = cls.request_places(query_params)

        if response.status_code != httpx.codes.OK:
            raise OpenStreetMapResourceUnavailable()

        try:
            payload = response.json()
        except ValueError as exc:
            raise OpenStreetMapResourceUnavailable() from exc

        if not isinstance(payload, dict):
            raise OpenStreetMapResourceUnavailable()

        OpenStreetMapCache.set_payload(query_params, payload)

        return payload

    @classmethod
    def build_request_payload(
        cls,
        query_params: PlaceQueryParams,
    ) -> dict[str, str]:
        return {
            "data": cls.build_overpass_query(
                lat=query_params["lat"],
                lng=query_params["lng"],
                radius=query_params["search_radious"],
            )
        }

    @classmethod
    def build_overpass_query(cls, lat: float, lng: float, radius: int) -> str:
        filters = "\n".join(
            f'  nwr(around:{radius},{lat},{lng})["{tag}"];'
            for tag in cls.category_tags
        )

        return f"""
                [out:json][timeout:25];
                (
                {filters}
                );
                out center tags qt 50;
                """

    @classmethod
    def headers(cls) -> dict[str, str]:
        return {
            "Accept": "application/json",
            "User-Agent": settings.OPEN_STREET_MAP_USER_AGENT,
        }
