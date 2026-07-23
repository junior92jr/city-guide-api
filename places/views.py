from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from .serializers import RecomendatiosQuerySerializer
from .services import get_categories, search_places_by_location


class RecomendationViewSet(viewsets.GenericViewSet):
    """
    ViewSet that exposes OpenStreetMap place data.
    """

    serializer_class = RecomendatiosQuerySerializer
    permission_classes = (AllowAny,)
    queryset = []

    @action(methods=['get'], url_path=r'places', detail=False)
    def places(self, request: Request) -> Response:
        """
        Retrieve places near a location from OpenStreetMap.
        """

        response = search_places_by_location(self.get_query_params(request))

        return Response(response.model_dump(by_alias=True, exclude_none=True))

    @action(methods=['get'], url_path=r'categories', detail=False)
    def categories(self, request: Request) -> Response:
        """
        Retrieve the known categories supported by the places API.
        """

        return Response({"categories": get_categories()})

    def get_query_params(self, request: Request) -> dict:
        serializer = self.serializer_class(data=request.query_params)

        serializer.is_valid(raise_exception=True)

        return serializer.validated_data
