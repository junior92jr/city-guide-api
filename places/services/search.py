from .mappers import OpenStreetMapApiResponse
from .open_street_map import OpenStreetMapClient
from .types import PlaceQueryParams


class PlaceSearchService:
    """
    Coordinates place search through the OpenStreetMap client and response mapper.
    """

    @classmethod
    def search_places_by_location(
        cls,
        query_params: PlaceQueryParams,
    ) -> OpenStreetMapApiResponse:
        payload = OpenStreetMapClient.fetch_places_payload(query_params)
        response = OpenStreetMapApiResponse.from_api_response(payload)
        category = query_params.get("category")

        if category is None:
            return response

        return OpenStreetMapApiResponse(
            places=[
                place for place in response.places
                if place.category == category
            ]
        )
