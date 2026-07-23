import pytest

from places.services.categories import (
    get_categories,
    get_active_osm_category_tags,
    get_category_by_slug,
    get_category_from_tags,
)

pytestmark = pytest.mark.django_db


def test_get_categories_returns_known_category_catalog():
    categories = get_categories()

    assert categories[3] == {
        "slug": "parking",
        "name": "Parking",
    }
    assert categories[25] == {
        "slug": "wayside-shrine",
        "name": "Wayside Shrine",
    }


def test_get_category_by_slug_returns_known_category():
    category = get_category_by_slug("parking")

    assert category is not None
    assert category.osm_key == "amenity"
    assert category.osm_value == "parking"


def test_get_category_from_tags_matches_osm_tag():
    category = get_category_from_tags({"historic": "wayside_shrine"})

    assert category is not None
    assert category.slug == "wayside-shrine"


def test_get_category_from_tags_returns_none_for_unknown_tags():
    assert get_category_from_tags({"amenity": "bench"}) is None


def test_get_active_osm_category_tags_returns_known_osm_pairs():
    tags = get_active_osm_category_tags()

    assert ("amenity", "parking") in tags
    assert ("historic", "wayside_shrine") in tags
