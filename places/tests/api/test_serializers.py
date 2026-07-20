from places.serializers import RecomendatiosQuerySerializer


def test_recomendations_query_serializer_accepts_required_coordinates():
    serializer = RecomendatiosQuerySerializer(data={
        "lat": "50.1101038",
        "lng": "8.6771586",
    })

    assert serializer.is_valid()
    assert serializer.validated_data == {
        "lat": 50.1101038,
        "lng": 8.6771586,
        "search_radious": 1000,
    }


def test_recomendations_query_serializer_accepts_optional_filters():
    serializer = RecomendatiosQuerySerializer(data={
        "lat": "50.1101038",
        "lng": "8.6771586",
        "search_radious": "250",
        "category": "parking",
    })

    assert serializer.is_valid()
    assert serializer.validated_data == {
        "lat": 50.1101038,
        "lng": 8.6771586,
        "search_radious": 250,
        "category": "parking",
    }


def test_recomendations_query_serializer_requires_coordinates():
    serializer = RecomendatiosQuerySerializer(data={
        "lat": "50.1101038",
    })

    assert not serializer.is_valid()
    assert "lng" in serializer.errors


def test_recomendations_query_serializer_rejects_invalid_coordinates():
    serializer = RecomendatiosQuerySerializer(data={
        "lat": "not-a-float",
        "lng": "8.6771586",
    })

    assert not serializer.is_valid()
    assert "lat" in serializer.errors


def test_recomendations_query_serializer_rejects_unknown_category():
    serializer = RecomendatiosQuerySerializer(data={
        "lat": "50.1101038",
        "lng": "8.6771586",
        "category": "unknown",
    })

    assert not serializer.is_valid()
    assert "category" in serializer.errors
