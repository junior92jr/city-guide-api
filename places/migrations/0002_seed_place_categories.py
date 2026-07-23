from django.db import migrations


PLACE_CATEGORIES = (
    ("bar", "Bar", "amenity", "bar"),
    ("cafe", "Cafe", "amenity", "cafe"),
    ("fast-food", "Fast Food", "amenity", "fast_food"),
    ("parking", "Parking", "amenity", "parking"),
    ("pharmacy", "Pharmacy", "amenity", "pharmacy"),
    ("pub", "Pub", "amenity", "pub"),
    ("recycling", "Recycling", "amenity", "recycling"),
    ("restaurant", "Restaurant", "amenity", "restaurant"),
    ("shelter", "Shelter", "amenity", "shelter"),
    ("attraction", "Attraction", "tourism", "attraction"),
    ("gallery", "Gallery", "tourism", "gallery"),
    ("hotel", "Hotel", "tourism", "hotel"),
    ("museum", "Museum", "tourism", "museum"),
    ("bakery", "Bakery", "shop", "bakery"),
    ("beauty", "Beauty Salon", "shop", "beauty"),
    ("clothes", "Clothing Store", "shop", "clothes"),
    ("dry-cleaning", "Dry Cleaner", "shop", "dry_cleaning"),
    ("jewelry", "Jewelry Store", "shop", "jewelry"),
    ("kiosk", "Kiosk", "shop", "kiosk"),
    ("supermarket", "Supermarket", "shop", "supermarket"),
    ("garden", "Garden", "leisure", "garden"),
    ("nature-reserve", "Nature Reserve", "leisure", "nature_reserve"),
    ("park", "Park", "leisure", "park"),
    ("pitch", "Pitch", "leisure", "pitch"),
    ("memorial", "Memorial", "historic", "memorial"),
    ("wayside-shrine", "Wayside Shrine", "historic", "wayside_shrine"),
    ("protected-area", "Protected Area", "boundary", "protected_area"),
)


def seed_place_categories(apps, schema_editor):
    place_category = apps.get_model("places", "PlaceCategory")

    for sort_order, (slug, name, osm_key, osm_value) in enumerate(
        PLACE_CATEGORIES
    ):
        place_category.objects.update_or_create(
            slug=slug,
            defaults={
                "name": name,
                "osm_key": osm_key,
                "osm_value": osm_value,
                "is_active": True,
                "sort_order": sort_order,
            },
        )


def remove_place_categories(apps, schema_editor):
    place_category = apps.get_model("places", "PlaceCategory")
    slugs = [slug for slug, _name, _osm_key, _osm_value in PLACE_CATEGORIES]

    place_category.objects.filter(slug__in=slugs).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("places", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            seed_place_categories,
            reverse_code=remove_place_categories,
        ),
    ]
