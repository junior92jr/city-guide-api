from typing import Any, NotRequired, TypedDict


class PlaceQueryParams(TypedDict):
    lat: float
    lng: float
    search_radious: int
    category: NotRequired[str]


OpenStreetMapPayload = dict[str, Any]
