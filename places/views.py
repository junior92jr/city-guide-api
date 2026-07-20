from rest_framework import viewsets

from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action

from .serializers import RecomendatiosQuerySerializer
from .services import PlaceSearchService


class RecomendationViewSet(viewsets.GenericViewSet):
    """
    ViewSet that handles the connection to OpenStreetMap POI data.
    """

    serializer_class = RecomendatiosQuerySerializer
    permission_classes = (AllowAny,)
    queryset = []

    @action(methods=['get'], url_path=r'places', detail=False)
    def places(self, request):
        """
        Get method to retrieve all places near a location.
        """

        serializer = self.serializer_class(data=request.query_params)

        serializer.is_valid(raise_exception=True)

        response = PlaceSearchService.search_places_by_location(serializer.data)

        return Response(response.model_dump(by_alias=True, exclude_none=True))

    @action(methods=['get'], url_path=r'categories', detail=False)
    def categories(self, request):
        """
        Get method to retrieve the mapped OpenStreetMap response.
        """

        serializer = self.serializer_class(data=request.query_params)

        serializer.is_valid(raise_exception=True)

        response = PlaceSearchService.search_places_by_location(serializer.data)

        return Response(response.model_dump(by_alias=True, exclude_none=True))
