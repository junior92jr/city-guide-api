from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class PlaceCategory:
    slug: str
    name: str
    osm_key: str
    osm_value: str

    def as_dict(self) -> dict[str, str]:
        return {
            "slug": self.slug,
            "name": self.name,
            "osm_key": self.osm_key,
            "osm_value": self.osm_value,
        }


PLACE_CATEGORIES = (
    PlaceCategory("bar", "Bar", "amenity", "bar"),
    PlaceCategory("cafe", "Cafe", "amenity", "cafe"),
    PlaceCategory("fast-food", "Fast Food", "amenity", "fast_food"),
    PlaceCategory("parking", "Parking", "amenity", "parking"),
    PlaceCategory("pharmacy", "Pharmacy", "amenity", "pharmacy"),
    PlaceCategory("pub", "Pub", "amenity", "pub"),
    PlaceCategory("recycling", "Recycling", "amenity", "recycling"),
    PlaceCategory("restaurant", "Restaurant", "amenity", "restaurant"),
    PlaceCategory("shelter", "Shelter", "amenity", "shelter"),
    PlaceCategory("attraction", "Attraction", "tourism", "attraction"),
    PlaceCategory("gallery", "Gallery", "tourism", "gallery"),
    PlaceCategory("hotel", "Hotel", "tourism", "hotel"),
    PlaceCategory("museum", "Museum", "tourism", "museum"),
    PlaceCategory("bakery", "Bakery", "shop", "bakery"),
    PlaceCategory("beauty", "Beauty Salon", "shop", "beauty"),
    PlaceCategory("clothes", "Clothing Store", "shop", "clothes"),
    PlaceCategory("dry-cleaning", "Dry Cleaner", "shop", "dry_cleaning"),
    PlaceCategory("jewelry", "Jewelry Store", "shop", "jewelry"),
    PlaceCategory("kiosk", "Kiosk", "shop", "kiosk"),
    PlaceCategory("supermarket", "Supermarket", "shop", "supermarket"),
    PlaceCategory("garden", "Garden", "leisure", "garden"),
    PlaceCategory("nature-reserve", "Nature Reserve", "leisure", "nature_reserve"),
    PlaceCategory("park", "Park", "leisure", "park"),
    PlaceCategory("pitch", "Pitch", "leisure", "pitch"),
    PlaceCategory("memorial", "Memorial", "historic", "memorial"),
    PlaceCategory("wayside-shrine", "Wayside Shrine", "historic", "wayside_shrine"),
    PlaceCategory("protected-area", "Protected Area", "boundary", "protected_area"),
)

PLACE_CATEGORIES_BY_SLUG = {
    category.slug: category for category in PLACE_CATEGORIES
}
PLACE_CATEGORIES_BY_OSM_TAG = {
    (category.osm_key, category.osm_value): category
    for category in PLACE_CATEGORIES
}


def get_categories() -> list[dict[str, str]]:
    return [category.as_dict() for category in PLACE_CATEGORIES]


def get_category_by_slug(slug: str) -> PlaceCategory | None:
    return PLACE_CATEGORIES_BY_SLUG.get(slug)


def get_category_from_tags(tags: dict[str, Any]) -> PlaceCategory | None:
    for (key, value), category in PLACE_CATEGORIES_BY_OSM_TAG.items():
        if tags.get(key) == value:
            return category

    return None
