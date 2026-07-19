from rest_framework import serializers


class RecomendatiosQuerySerializer(serializers.Serializer):
    """
    Serializer that handle validation for the request parameters.
    """

    lat = serializers.FloatField()
    lng = serializers.FloatField()
    search_radious = serializers.IntegerField(required=False)
    category = serializers.IntegerField(required=False)
