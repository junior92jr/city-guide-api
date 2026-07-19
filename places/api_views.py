
from rest_framework import viewsets

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .serializers import RecomendatiosQuerySerializer
from .resources import FourSquareResource


class RecomendationViewSet(viewsets.GenericViewSet):
    """
    ViewSet that handle the connection the Foursquare API
    """

    serializer_class = RecomendatiosQuerySerializer
    permission_classes = (IsAuthenticated,)
    queryset = []

    @action(methods=['get'], url_path=r'places', detail=False)
    def places(self, request):
        """
        Get method to retrieve all places near a location.
        """

        serializer = self.serializer_class(data=request.query_params)
        
        serializer.is_valid(raise_exception=True)

        response = FourSquareResource.search_places_by_location(serializer.data)
        category = serializer.data.get('category')
        search_radious = serializer.data.get('search_radious')
        
        if category:
            response = FourSquareResource.filter_by_category(response, category)
        
        if search_radious:
            response = FourSquareResource.range_query(response, search_radious)

        return Response(response)

    @action(methods=['get'], url_path=r'categories', detail=False)
    def categories(self, request):
        """
        Get method to retrieve all non repeated categories from requested places.
        """

        serializer = self.serializer_class(data=request.query_params)
        
        serializer.is_valid(raise_exception=True)

        categories = FourSquareResource.get_categories(
            FourSquareResource.search_places_by_location(serializer.data))

        return Response(categories)
