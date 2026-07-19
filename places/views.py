
from rest_framework import viewsets

from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action

from .serializers import RecomendatiosQuerySerializer
from .resources import OpenStreetMapResource


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

        response = OpenStreetMapResource.search_places_by_location(serializer.data)
        category = serializer.data.get('category')
        search_radious = serializer.data.get('search_radious')
        
        if category:
            response = OpenStreetMapResource.filter_by_category(response, category)
        
        if search_radious:
            response = OpenStreetMapResource.range_query(response, search_radious)

        return Response(response)

    @action(methods=['get'], url_path=r'categories', detail=False)
    def categories(self, request):
        """
        Get method to retrieve all non repeated categories from requested places.
        """

        serializer = self.serializer_class(data=request.query_params)
        
        serializer.is_valid(raise_exception=True)

        categories = OpenStreetMapResource.get_categories(
            OpenStreetMapResource.search_places_by_location(serializer.data))

        return Response(categories)
