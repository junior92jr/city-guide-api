from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from places.models import PlaceCategory

from .categories import get_category_from_tags


class OpenStreetMapMetadata(BaseModel):
    timestamp_osm_base: str | None = None
    timestamp_areas_base: str | None = None
    copyright: str | None = None


class OpenStreetMapCenter(BaseModel):
    lat: float
    lon: float


class RawOpenStreetMapElement(BaseModel):
    model_config = ConfigDict(extra="allow")

    type: str
    id: int
    lat: float | None = None
    lon: float | None = None
    center: OpenStreetMapCenter | None = None
    tags: dict[str, Any] = Field(default_factory=dict)


class RawOpenStreetMapApiResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    version: float | None = None
    generator: str | None = None
    osm3s: OpenStreetMapMetadata | None = None
    elements: list[RawOpenStreetMapElement] = Field(default_factory=list)


class OpenStreetMapPlace(BaseModel):
    osm_id: int
    osm_type: str
    name: str
    latitude: float
    longitude: float
    category: str
    category_name: str
    osm_uid: str
    address: str | None = None
    website: str | None = None
    opening_hours: str | None = None

    @classmethod
    def from_element(
        cls,
        element: RawOpenStreetMapElement,
    ) -> "OpenStreetMapPlace | None":
        latitude = element.lat
        longitude = element.lon

        if element.center is not None:
            latitude = latitude if latitude is not None else element.center.lat
            longitude = longitude if longitude is not None else element.center.lon

        if latitude is None or longitude is None:
            return None

        category = get_category_from_tags(element.tags)

        if category is None:
            return None

        return cls(
            osm_id=element.id,
            osm_type=element.type,
            name=cls.name_from_tags(
                tags=element.tags,
                category=category,
            ),
            latitude=latitude,
            longitude=longitude,
            category=category.slug,
            category_name=category.name,
            osm_uid=f"osm-{element.type}-{element.id}",
            address=cls.address_from_tags(element.tags),
            website=element.tags.get("website") or element.tags.get("contact:website"),
            opening_hours=element.tags.get("opening_hours"),
        )

    @classmethod
    def name_from_tags(
        cls,
        tags: dict[str, Any],
        category: PlaceCategory,
    ) -> str:
        name = tags.get("name") or tags.get("official_name")

        if name:
            return str(name)

        return f"Unnamed {category.name}"

    @classmethod
    def address_from_tags(cls, tags: dict[str, Any]) -> str | None:
        direct_address = (
            tags.get("addr:full") or tags.get("memorial:addr") or tags.get("addr:place")
        )

        if direct_address:
            return str(direct_address)

        address_parts = [
            tags.get("addr:street"),
            tags.get("addr:housenumber"),
            tags.get("addr:postcode"),
            tags.get("addr:city"),
        ]
        address = ", ".join(str(part) for part in address_parts if part)

        return address or None


class OpenStreetMapApiResponse(BaseModel):
    places: list[OpenStreetMapPlace] = Field(default_factory=list)

    @classmethod
    def from_api_response(cls, payload: dict[str, Any]) -> "OpenStreetMapApiResponse":
        raw_response = RawOpenStreetMapApiResponse.model_validate(payload)
        places = [
            place
            for element in raw_response.elements
            if (place := OpenStreetMapPlace.from_element(element)) is not None
        ]

        return cls(places=places)
