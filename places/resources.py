import math
import json
import zlib

import requests

from django.conf import settings

from .decorators import store_response_in_cache
from .exceptions import OpenStreetMapResourceUnavailable
from .mixins import PlaceResourceUtilsMixin
from .constants import (
    OPEN_STREET_MAP_DEFAULT_RADIUS_IN_METERS,
    OPEN_STREET_MAP_OVERPASS_URL,
    OPEN_STREET_MAP_USER_AGENT,
)


class OpenStreetMapResource(PlaceResourceUtilsMixin):
    """
    OpenStreetMap resource class with functions to get POI data from Overpass.
    """

    api_url = settings.OPEN_STREET_MAP_OVERPASS_URL
    category_tags = ("amenity", "tourism", "shop", "leisure", "historic")
    category_labels = {
        "amenity:bar": ("Bar", "Bars"),
        "amenity:cafe": ("Cafe", "Cafes"),
        "amenity:fast_food": ("Fast Food", "Fast Food"),
        "amenity:pharmacy": ("Pharmacy", "Pharmacies"),
        "amenity:pub": ("Pub", "Pubs"),
        "amenity:restaurant": ("Restaurant", "Restaurants"),
        "historic:memorial": ("Memorial", "Memorials"),
        "leisure:park": ("Park", "Parks"),
        "shop:bakery": ("Bakery", "Bakeries"),
        "shop:beauty": ("Beauty Salon", "Beauty Salons"),
        "shop:clothes": ("Clothing Store", "Clothing Stores"),
        "shop:dry_cleaning": ("Dry Cleaner", "Dry Cleaners"),
        "shop:jewelry": ("Jewelry Store", "Jewelry Stores"),
        "shop:kiosk": ("Kiosk", "Kiosks"),
        "shop:supermarket": ("Supermarket", "Supermarkets"),
        "tourism:attraction": ("Attraction", "Attractions"),
        "tourism:gallery": ("Gallery", "Galleries"),
        "tourism:hotel": ("Hotel", "Hotels"),
        "tourism:museum": ("Museum", "Museums"),
    }

    @classmethod
    @store_response_in_cache
    def open_street_map_request(cls, query_params):
        """
        Connection with the OpenStreetMap Overpass API.
        
        :param query_params: Dictionary with parameters from original request.

        :return: Response object from requests library.
        """

        radius = query_params.get(
            "search_radious",
            OPEN_STREET_MAP_DEFAULT_RADIUS_IN_METERS,
        )
        headers = {
            "Accept": "application/json",
            "User-Agent": settings.OPEN_STREET_MAP_USER_AGENT,
        }

        payload = {
            "data": cls.build_overpass_query(
                lat=query_params["lat"],
                lng=query_params["lng"],
                radius=radius,
            )
        }

        response = requests.get(cls.api_url, headers=headers, params=payload)

        try:
            print(json.dumps(response.json(), indent=2))
        except ValueError:
            print(response.text)
        
        return response

    @classmethod
    def build_overpass_query(cls, lat, lng, radius):
        filters = "\n".join(
            f'  nwr(around:{radius},{lat},{lng})["{tag}"];'
            for tag in cls.category_tags
        )

        return f"""
                [out:json][timeout:25];
                (
                {filters}
                );
                out center tags qt 50;
                """
    
    @classmethod
    def search_places_by_location(cls, query_params):
        """
        Get Places from External API.
        
        :param query_params: Dictionary with parameters from original request.

        :return: List of items accessed from original request.
        """

        response = cls.open_street_map_request(query_params)

        if response.status_code != 200:
            raise OpenStreetMapResourceUnavailable()

        return cls.normalize_places(
            response.json().get("elements", []),
            origin_lat=query_params["lat"],
            origin_lng=query_params["lng"],
        )

    @classmethod
    def normalize_places(cls, elements, origin_lat, origin_lng):
        places = []

        for element in elements:
            tags = element.get("tags", {})
            name = tags.get("name")

            if not name:
                continue

            lat = element.get("lat")
            lng = element.get("lon")

            if lat is None or lng is None:
                center = element.get("center", {})
                lat = center.get("lat")
                lng = center.get("lon")

            if lat is None or lng is None:
                continue

            categories = cls.build_categories(tags)

            if not categories:
                continue

            places.append({
                "fsq_id": f"osm-{element.get('type')}-{element.get('id')}",
                "name": name,
                "distance": cls.distance_in_meters(
                    origin_lat,
                    origin_lng,
                    lat,
                    lng,
                ),
                "categories": categories,
                "geocodes": {
                    "main": {
                        "latitude": lat,
                        "longitude": lng,
                    }
                },
                "location": {
                    "formatted_address": cls.formatted_address(tags),
                    "address": cls.address(tags),
                },
                "image": tags.get("image"),
                "website": tags.get("website") or tags.get("contact:website"),
                "tags": tags,
                "osm": {
                    "type": element.get("type"),
                    "id": element.get("id"),
                },
            })

        return sorted(places, key=lambda place: place["distance"])

    @classmethod
    def build_categories(cls, tags):
        categories = []

        for tag in cls.category_tags:
            value = tags.get(tag)

            if value:
                category_key = f"{tag}:{value}"
                category_name, plural_name = cls.category_display_names(
                    category_key,
                    value,
                )
                categories.append({
                    "id": zlib.crc32(category_key.encode("utf-8")),
                    "name": category_name,
                    "short_name": category_name,
                    "plural_name": plural_name,
                    "icon": {
                        "prefix": "",
                        "suffix": "",
                    },
                    "osm": {
                        "key": tag,
                        "value": value,
                    },
                })

        return categories

    @classmethod
    def category_display_names(cls, category_key, value):
        label = cls.category_labels.get(category_key)

        if label:
            return label

        name = value.replace("_", " ").title()
        return name, cls.pluralize(name)

    @staticmethod
    def pluralize(name):
        if name.endswith("y") and name[-2:].lower() not in {"ay", "ey", "oy"}:
            return f"{name[:-1]}ies"

        if name.endswith(("s", "x", "ch", "sh")):
            return f"{name}es"

        return f"{name}s"

    @staticmethod
    def formatted_address(tags):
        direct_address = (
            tags.get("addr:full")
            or tags.get("memorial:addr")
            or tags.get("addr:place")
        )

        if direct_address:
            return direct_address

        address_parts = [
            tags.get("addr:street"),
            tags.get("addr:housenumber"),
            tags.get("addr:postcode"),
            tags.get("addr:city"),
        ]

        return ", ".join(part for part in address_parts if part)

    @staticmethod
    def address(tags):
        return {
            "street": tags.get("addr:street"),
            "house_number": tags.get("addr:housenumber"),
            "postcode": tags.get("addr:postcode"),
            "city": tags.get("addr:city"),
            "full": (
                tags.get("addr:full")
                or tags.get("memorial:addr")
                or tags.get("addr:place")
            ),
        }

    @staticmethod
    def distance_in_meters(origin_lat, origin_lng, destination_lat, destination_lng):
        earth_radius_in_meters = 6371000
        origin_lat = math.radians(origin_lat)
        origin_lng = math.radians(origin_lng)
        destination_lat = math.radians(destination_lat)
        destination_lng = math.radians(destination_lng)

        lat_delta = destination_lat - origin_lat
        lng_delta = destination_lng - origin_lng

        a = (
            math.sin(lat_delta / 2) ** 2
            + math.cos(origin_lat)
            * math.cos(destination_lat)
            * math.sin(lng_delta / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return round(earth_radius_in_meters * c)
