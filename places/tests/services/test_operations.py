from places.services.operations import PlaceOperations


def test_range_query_filters_by_distance():
    places = [
        {"name": "Near", "distance": 250},
        {"name": "Far", "distance": 1500},
    ]

    assert PlaceOperations.range_query(places, 1000) == [
        {"name": "Near", "distance": 250},
    ]


def test_filter_by_category_returns_matching_places():
    places = [
        {"name": "Cafe", "categories": [{"id": 10}]},
        {"name": "Museum", "categories": [{"id": 20}]},
        {"name": "Empty", "categories": []},
    ]

    assert PlaceOperations.filter_by_category(places, 10) == [
        {"name": "Cafe", "categories": [{"id": 10}]},
    ]


def test_get_categories_returns_unique_categories():
    cafe = {"id": 10, "name": "Cafe"}
    museum = {"id": 20, "name": "Museum"}
    places = [
        {"categories": [cafe]},
        {"categories": [museum, cafe]},
    ]

    assert PlaceOperations.get_categories(places) == [museum, cafe]
