import hashlib
from typing import cast

from django.core.cache import cache
from django.conf import settings

from .types import OpenStreetMapPayload, PlaceQueryParams


class OpenStreetMapCache:
    """
    Cache access for successful OpenStreetMap payloads.
    """

    @classmethod
    def get_payload(
        cls,
        query_params: PlaceQueryParams,
    ) -> OpenStreetMapPayload | None:
        if settings.CACHE_TIMEOUT_IN_SECS == 0:
            return None

        cached_payload = cache.get(cls.build_key(query_params))

        if cached_payload is None:
            return None

        return cast(OpenStreetMapPayload, cached_payload)

    @classmethod
    def set_payload(
        cls,
        query_params: PlaceQueryParams,
        payload: OpenStreetMapPayload,
    ) -> None:
        if settings.CACHE_TIMEOUT_IN_SECS == 0:
            return

        cache.set(
            cls.build_key(query_params),
            payload,
            settings.CACHE_TIMEOUT_IN_SECS,
        )

    @classmethod
    def build_key(cls, query_params: PlaceQueryParams) -> str:
        cache_key = (
            "open-street-map-"
            f"{query_params['lat']}-"
            f"{query_params['lng']}-"
            f"{query_params['search_radious']}"
        )

        return hashlib.sha1(cache_key.encode("utf-8")).hexdigest()
