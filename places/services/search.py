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
        return OpenStreetMapApiResponse.from_api_response(payload)
