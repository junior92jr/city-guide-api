from rest_framework import serializers

from .services.categories import get_category_by_slug

DEFAULT_SEARCH_RADIOUS = 1000


class RecomendatiosQuerySerializer(serializers.Serializer):
    """
    Serializer that handle validation for the request parameters.
    """

    lat = serializers.FloatField()
    lng = serializers.FloatField()
    search_radious = serializers.IntegerField(
        default=DEFAULT_SEARCH_RADIOUS,
        required=False,
    )
    category = serializers.CharField(required=False)

    def validate_category(self, value):
        if get_category_by_slug(value) is None:
            raise serializers.ValidationError("Unknown category.")

        return value
