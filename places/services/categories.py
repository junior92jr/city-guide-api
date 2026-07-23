from typing import Any

from places.models import PlaceCategory


def get_categories() -> list[dict[str, str]]:
    return [
        {"slug": category.slug, "name": category.name}
        for category in active_categories()
    ]


def get_category_by_slug(slug: str) -> PlaceCategory | None:
    return active_categories().filter(slug=slug).first()


def get_category_from_tags(tags: dict[str, Any]) -> PlaceCategory | None:
    for category in active_categories():
        if tags.get(category.osm_key) == category.osm_value:
            return category

    return None


def get_active_osm_category_tags() -> list[tuple[str, str]]:
    return [
        (category.osm_key, category.osm_value)
        for category in active_categories()
    ]


def active_categories():
    return PlaceCategory.objects.filter(is_active=True).order_by(
        "sort_order",
        "name",
    )
