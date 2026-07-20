from typing import Any, NotRequired, TypedDict


class PlaceQueryParams(TypedDict):
    lat: float
    lng: float
    search_radious: NotRequired[int]


OpenStreetMapPayload = dict[str, Any]
