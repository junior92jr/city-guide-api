from .mappers import OpenStreetMapApiResponse
from .open_street_map import PlaceQueryParams, fetch_places_payload


def search_places_by_location(
    query_params: PlaceQueryParams,
) -> OpenStreetMapApiResponse:
    payload = fetch_places_payload(query_params)
    response = OpenStreetMapApiResponse.from_api_response(payload)
    category = query_params.get("category")

    if category is None:
        return response

    return filter_places_by_category(response, category)


def filter_places_by_category(
    response: OpenStreetMapApiResponse,
    category: str,
) -> OpenStreetMapApiResponse:
    return OpenStreetMapApiResponse(
        places=[place for place in response.places if place.category == category]
    )
