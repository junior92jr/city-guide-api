from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class OpenStreetMapMetadata(BaseModel):
    timestamp_osm_base: str | None = None
    timestamp_areas_base: str | None = None
    copyright: str | None = None


class OpenStreetMapCenter(BaseModel):
    lat: float
    lon: float


class OpenStreetMapElement(BaseModel):
    model_config = ConfigDict(extra="allow")

    type: str
    id: int
    lat: float | None = None
    lon: float | None = None
    center: OpenStreetMapCenter | None = None
    tags: dict[str, Any] = Field(default_factory=dict)


class OpenStreetMapApiResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    version: float | None = None
    generator: str | None = None
    osm3s: OpenStreetMapMetadata | None = None
    elements: list[OpenStreetMapElement] = Field(default_factory=list)

    @classmethod
    def from_api_response(cls, payload: dict[str, Any]) -> "OpenStreetMapApiResponse":
        return cls.model_validate(payload)
